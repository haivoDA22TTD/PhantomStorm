#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration constants for Phantom Storm v2.5 Ultimate
"""

# User-Agent pool
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/109.0 Firefox/109.0"
]

# Private IP ranges to avoid when generating spoofed IPs
PRIVATE_IP_RANGES = [
    (10, 0, 0, 0, 10, 255, 255, 255),      # 10.0.0.0/8
    (172, 16, 0, 0, 172, 31, 255, 255),    # 172.16.0.0/12
    (192, 168, 0, 0, 192, 168, 255, 255),  # 192.168.0.0/16
    (127, 0, 0, 0, 127, 255, 255, 255),    # 127.0.0.0/8 (loopback)
]

# Default settings
DEFAULT_TIMEOUT = 4
DEFAULT_KEEP_ALIVE_INTERVAL = 3
STATS_UPDATE_INTERVAL = 2

# Version info
VERSION = "2.5"
VERSION_NAME = "Ultimate Edition"
