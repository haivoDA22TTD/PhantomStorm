#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Smart IP Generator - Generates public IPs for spoofing
"""

import random
from typing import Tuple
from ..config import PRIVATE_IP_RANGES

class IPGenerator:
    """Smart IP generator - tránh private/reserved ranges"""
    
    @staticmethod
    def is_private_ip(ip_tuple: Tuple[int, int, int, int]) -> bool:
        """
        Kiểm tra xem IP có phải private/reserved không
        
        Args:
            ip_tuple: Tuple (octet1, octet2, octet3, octet4)
            
        Returns:
            True nếu IP thuộc dải private
        """
        for start_end in PRIVATE_IP_RANGES:
            start = start_end[:4]
            end = start_end[4:]
            if (start <= ip_tuple <= end):
                return True
        return False
    
    @staticmethod
    def generate_public_ip() -> str:
        """
        Generate random public IP address
        
        Returns:
            IP address string (e.g., "203.45.67.89")
        """
        max_attempts = 50
        for _ in range(max_attempts):
            ip_tuple = (
                random.randint(1, 223),    # Tránh 224-255 (multicast/reserved)
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(1, 254)     # Tránh .0 và .255
            )
            
            if not IPGenerator.is_private_ip(ip_tuple):
                return f"{ip_tuple[0]}.{ip_tuple[1]}.{ip_tuple[2]}.{ip_tuple[3]}"
        
        # Fallback - trả về IP public bất kỳ
        return f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
    
    @staticmethod
    def generate_proxy_chain() -> str:
        """
        Generate chuỗi proxy giả cho Via header
        
        Returns:
            Via header value (e.g., "HTTP/1.1 203.45.67.89, HTTP/2.0 156.78.90.12")
        """
        proxy_count = random.randint(1, 3)
        proxies = []
        
        protocols = ["HTTP/1.1", "HTTP/1.0", "HTTP/2.0"]
        
        for _ in range(proxy_count):
            protocol = random.choice(protocols)
            proxy_ip = IPGenerator.generate_public_ip()
            proxies.append(f"{protocol} {proxy_ip}")
        
        return ", ".join(proxies)
