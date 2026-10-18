#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit tests for AttackStatistics
"""

import sys
sys.path.insert(0, '..')

from src.core.statistics import AttackStatistics
import time

def test_basic_tracking():
    """Test basic stat tracking"""
    print("Testing basic stat tracking...")
    
    stats = AttackStatistics()
    
    # Simulate some activity
    stats.connection_established("203.45.67.89")
    stats.connection_established("89.123.45.67")
    stats.packet_sent()
    stats.packet_sent()
    stats.connection_failed("timeout")
    
    result = stats.get_stats()
    
    assert result['connections_established'] == 2
    assert result['connections_failed'] == 1
    assert result['total_packets'] == 2
    assert result['unique_ips_used'] == 2
    
    print("✓ Basic tracking works")

def test_diversity_calculation():
    """Test IP diversity calculation"""
    print("\nTesting IP diversity calculation...")
    
    stats = AttackStatistics()
    
    # 5 unique IPs out of 10 attempts = 50% diversity
    for i in range(5):
        stats.connection_established(f"1.2.3.{i}")
    for i in range(5):
        stats.connection_established("1.2.3.1")  # Duplicate
    
    result = stats.get_stats()
    
    print(f"  Unique IPs: {result['unique_ips_used']}")
    print(f"  Bypass Attempts: {result['bypass_attempts']}")
    print(f"  Diversity: {result['bypass_diversity']:.2f}%")
    
    assert result['unique_ips_used'] == 5
    assert result['bypass_attempts'] == 10
    assert 49 <= result['bypass_diversity'] <= 51  # ~50%
    
    print("✓ Diversity calculation correct")

def test_success_rate():
    """Test success rate calculation"""
    print("\nTesting success rate calculation...")
    
    stats = AttackStatistics()
    
    # 7 success, 3 failures = 70%
    for _ in range(7):
        stats.connection_established()
    for _ in range(3):
        stats.connection_failed()
    
    result = stats.get_stats()
    
    print(f"  Success Rate: {result['success_rate']:.2f}%")
    
    assert 69 <= result['success_rate'] <= 71  # ~70%
    
    print("✓ Success rate calculation correct")

def test_active_connections():
    """Test active connection tracking"""
    print("\nTesting active connection tracking...")
    
    stats = AttackStatistics()
    
    stats.connection_established()
    stats.connection_established()
    assert stats.get_stats()['connections_active'] == 2
    
    stats.connection_closed()
    assert stats.get_stats()['connections_active'] == 1
    
    stats.connection_closed()
    assert stats.get_stats()['connections_active'] == 0
    
    print("✓ Active connection tracking works")

if __name__ == "__main__":
    print("="*60)
    print("AttackStatistics Unit Tests")
    print("="*60)
    
    test_basic_tracking()
    test_diversity_calculation()
    test_success_rate()
    test_active_connections()
    
    print("\n" + "="*60)
    print("All tests passed! ✓")
    print("="*60)
