#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Attack Statistics Tracker
"""

import threading
import time
from collections import defaultdict
from typing import Dict, Optional

class AttackStatistics:
    """Theo dõi và hiển thị thống kê real-time"""
    
    def __init__(self):
        self.lock = threading.Lock()
        self.connections_established = 0
        self.connections_active = 0
        self.connections_failed = 0
        self.total_packets_sent = 0
        self.spoofed_ips_used = set()  # Track unique IPs used
        self.bypass_attempts = 0       # Số lần thử bypass
        self.error_types = defaultdict(int)
        self.start_time = time.time()
        
    def connection_established(self, spoofed_ip: Optional[str] = None):
        """
        Ghi nhận connection thành công
        
        Args:
            spoofed_ip: IP đã spoofed (nếu có)
        """
        with self.lock:
            self.connections_established += 1
            self.connections_active += 1
            if spoofed_ip:
                self.spoofed_ips_used.add(spoofed_ip)
                self.bypass_attempts += 1
            
    def connection_closed(self):
        """Ghi nhận connection bị đóng"""
        with self.lock:
            if self.connections_active > 0:
                self.connections_active -= 1
                
    def connection_failed(self, error_type: str = "unknown"):
        """
        Ghi nhận connection thất bại
        
        Args:
            error_type: Loại lỗi (timeout, ConnectionRefusedError, etc.)
        """
        with self.lock:
            self.connections_failed += 1
            self.error_types[error_type] += 1
            
    def packet_sent(self):
        """Ghi nhận packet đã gửi"""
        with self.lock:
            self.total_packets_sent += 1
            
    def get_stats(self) -> Dict:
        """
        Lấy tất cả thống kê hiện tại
        
        Returns:
            Dictionary chứa tất cả metrics
        """
        with self.lock:
            runtime = time.time() - self.start_time
            total_attempts = self.connections_established + self.connections_failed
            
            return {
                'runtime': runtime,
                'connections_established': self.connections_established,
                'connections_active': self.connections_active,
                'connections_failed': self.connections_failed,
                'total_packets': self.total_packets_sent,
                'packets_per_second': self.total_packets_sent / runtime if runtime > 0 else 0,
                'success_rate': (self.connections_established / total_attempts * 100) if total_attempts > 0 else 0,
                'unique_ips_used': len(self.spoofed_ips_used),
                'bypass_attempts': self.bypass_attempts,
                'bypass_diversity': len(self.spoofed_ips_used) / self.bypass_attempts * 100 if self.bypass_attempts > 0 else 0,
                'error_types': dict(self.error_types)
            }
    
    def reset(self):
        """Reset tất cả statistics"""
        with self.lock:
            self.connections_established = 0
            self.connections_active = 0
            self.connections_failed = 0
            self.total_packets_sent = 0
            self.spoofed_ips_used.clear()
            self.bypass_attempts = 0
            self.error_types.clear()
            self.start_time = time.time()
