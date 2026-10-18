#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit tests for IPGenerator
"""

import sys
sys.path.insert(0, '..')

from src.core.ip_generator import IPGenerator

def test_generate_public_ip():
    """Test IP generation"""
    print("Testing IP generation...")
    
    ips = set()
    for _ in range(100):
        ip = IPGenerator.generate_public_ip()
        ips.add(ip)
        
        # Validate format
        octets = ip.split('.')
        assert len(octets) == 4, "IP must have 4 octets"
        
        for octet in octets:
            num = int(octet)
            assert 0 <= num <= 255, f"Invalid octet: {num}"
    
    print(f"✓ Generated {len(ips)} unique IPs")
    print(f"  Sample: {list(ips)[:5]}")
    
def test_is_private_ip():
    """Test private IP detection"""
    print("\nTesting private IP detection...")
    
    test_cases = [
        ((10, 0, 0, 1), True, "10.0.0.1 - Private"),
        ((192, 168, 1, 1), True, "192.168.1.1 - Private"),
        ((127, 0, 0, 1), True, "127.0.0.1 - Loopback"),
        ((8, 8, 8, 8), False, "8.8.8.8 - Public"),
        ((203, 0, 113, 1), False, "203.0.113.1 - Public"),
    ]
    
    for ip_tuple, expected, desc in test_cases:
        result = IPGenerator.is_private_ip(ip_tuple)
        status = "✓" if result == expected else "✗"
        print(f"  {status} {desc}: {result == expected}")
        assert result == expected

def test_proxy_chain():
    """Test proxy chain generation"""
    print("\nTesting proxy chain generation...")
    
    for i in range(5):
        chain = IPGenerator.generate_proxy_chain()
        print(f"  {i+1}. {chain}")
        
        assert "HTTP" in chain, "Must contain HTTP protocol"
        assert len(chain) > 0, "Must not be empty"
    
    print("✓ Proxy chains generated successfully")

if __name__ == "__main__":
    print("="*60)
    print("IPGenerator Unit Tests")
    print("="*60)
    
    test_generate_public_ip()
    test_is_private_ip()
    test_proxy_chain()
    
    print("\n" + "="*60)
    print("All tests passed! ✓")
    print("="*60)
