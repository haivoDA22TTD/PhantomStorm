#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit tests for HTTP Methods
"""

import sys
sys.path.insert(0, '..')

from src.core.http_methods import HTTPMethodBuilder, HTTPMethod

def test_get_request():
    """Test GET request building"""
    print("Testing GET request...")
    
    request = HTTPMethodBuilder.build_get(
        target_ip="192.168.1.100",
        path="/test",
        spoofed_ip="203.45.67.89"
    )
    
    assert "GET /test HTTP/1.1" in request
    assert "Host: 192.168.1.100" in request
    assert "X-Forwarded-For: 203.45.67.89" in request
    assert "Connection: keep-alive" in request
    
    print("✓ GET request builds correctly")

def test_post_request():
    """Test POST request building"""
    print("\nTesting POST request...")
    
    request = HTTPMethodBuilder.build_post(
        target_ip="192.168.1.100",
        path="/submit",
        body_data="test=data",
        spoofed_ip="203.45.67.89"
    )
    
    assert "POST /submit HTTP/1.1" in request
    assert "Content-Type: application/x-www-form-urlencoded" in request
    assert "Content-Length:" in request
    assert "test=data" in request
    assert "X-Forwarded-For: 203.45.67.89" in request
    
    print("✓ POST request builds correctly")

def test_head_request():
    """Test HEAD request building"""
    print("\nTesting HEAD request...")
    
    request = HTTPMethodBuilder.build_head(
        target_ip="192.168.1.100",
        path="/api"
    )
    
    assert "HEAD /api HTTP/1.1" in request
    assert "Host: 192.168.1.100" in request
    assert "Connection: keep-alive" in request
    
    print("✓ HEAD request builds correctly")

def test_options_request():
    """Test OPTIONS request building"""
    print("\nTesting OPTIONS request...")
    
    request = HTTPMethodBuilder.build_options(
        target_ip="192.168.1.100"
    )
    
    assert "OPTIONS" in request
    assert "Host: 192.168.1.100" in request
    
    print("✓ OPTIONS request builds correctly")

def test_random_request():
    """Test random request generation"""
    print("\nTesting random request generation...")
    
    requests = []
    for _ in range(10):
        request = HTTPMethodBuilder.build_random(
            target_ip="192.168.1.100",
            spoofed_ip="203.45.67.89"
        )
        # Extract method from first line
        method = request.split(' ')[0]
        requests.append(method)
    
    # Should have multiple different methods
    unique_methods = set(requests)
    print(f"  Generated methods: {unique_methods}")
    
    assert len(unique_methods) >= 2, "Should generate different methods"
    
    print("✓ Random request generation works")

def test_spoofing_headers():
    """Test IP spoofing headers"""
    print("\nTesting IP spoofing headers...")
    
    spoofed_ip = "203.45.67.89"
    
    request = HTTPMethodBuilder.build_get(
        target_ip="192.168.1.100",
        spoofed_ip=spoofed_ip
    )
    
    # Check all spoofing headers present
    required_headers = [
        "X-Forwarded-For:",
        "X-Real-IP:",
        "X-Client-IP:",
        "X-Originating-IP:",
        "Client-IP:",
        "True-Client-IP:",
        "CF-Connecting-IP:",
        "X-ProxyUser-IP:",
        "Via:"
    ]
    
    for header in required_headers:
        assert header in request, f"Missing header: {header}"
        assert spoofed_ip in request, f"Missing spoofed IP in {header}"
    
    print(f"  All 9 spoofing headers present")
    print("✓ Spoofing headers work correctly")

def test_no_spoofing():
    """Test request without spoofing"""
    print("\nTesting request without spoofing...")
    
    request = HTTPMethodBuilder.build_get(
        target_ip="192.168.1.100",
        spoofed_ip=None  # No spoofing
    )
    
    assert "GET / HTTP/1.1" in request
    assert "X-Forwarded-For:" not in request
    
    print("✓ Non-spoofed request works correctly")

if __name__ == "__main__":
    print("="*60)
    print("HTTP Methods Unit Tests")
    print("="*60)
    
    test_get_request()
    test_post_request()
    test_head_request()
    test_options_request()
    test_random_request()
    test_spoofing_headers()
    test_no_spoofing()
    
    print("\n" + "="*60)
    print("All tests passed! ✓")
    print("="*60)
