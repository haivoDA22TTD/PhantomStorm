#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Attack Profiles Demo - Showcase different attack profiles

This example demonstrates the 3 predefined attack profiles:
1. Stealth - Slow & hard to detect
2. Balanced - Good mix of speed & stealth
3. Aggressive - Fast & heavy impact

Usage:
    python examples/attack_profiles_demo.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core import AttackProfiles, ProfileType

def main():
    print("="*80)
    print(" PHANTOM STORM - ATTACK PROFILES DEMONSTRATION ".center(80))
    print("="*80)
    
    # Get all profiles
    profiles = AttackProfiles.list_profiles()
    
    print("\n📋 Available Profiles:\n")
    for i, profile in enumerate(profiles, 1):
        print(f"{i}. {profile.name}")
    
    # Display comparison
    print(AttackProfiles.compare_profiles())
    
    # Show individual profile details
    print("\n" + "="*80)
    print(" DETAILED PROFILE INFORMATION ".center(80))
    print("="*80)
    
    print("\n1️⃣  STEALTH PROFILE")
    print("─" * 80)
    stealth = AttackProfiles.get_stealth()
    print(stealth.display_info())
    print("\n💡 Best for:")
    print("   • Long-term testing without triggering alarms")
    print("   • Bypassing IDS/IPS systems")
    print("   • Testing defense detection capabilities")
    print("   • Avoiding rate limiting")
    
    print("\n2️⃣  BALANCED PROFILE")
    print("─" * 80)
    balanced = AttackProfiles.get_balanced()
    print(balanced.display_info())
    print("\n💡 Best for:")
    print("   • General purpose DoS testing")
    print("   • Standard penetration testing scenarios")
    print("   • Good balance between impact and stealth")
    print("   • Most common use cases")
    
    print("\n3️⃣  AGGRESSIVE PROFILE")
    print("─" * 80)
    aggressive = AttackProfiles.get_aggressive()
    print(aggressive.display_info())
    print("\n💡 Best for:")
    print("   • Maximum resource exhaustion")
    print("   • Quick impact assessment")
    print("   • Stress testing server capacity")
    print("   • Finding breaking points")
    
    # Usage examples
    print("\n" + "="*80)
    print(" COMMAND LINE USAGE EXAMPLES ".center(80))
    print("="*80)
    
    print("\n🔹 Stealth Attack (Slow & Stealthy):")
    print("   python phantom_storm_v2.py 192.168.1.100 80 50 --profile=stealth")
    
    print("\n🔹 Balanced Attack (General Purpose):")
    print("   python phantom_storm_v2.py 192.168.1.100 80 150 --profile=balanced")
    
    print("\n🔹 Aggressive Attack (Maximum Impact):")
    print("   python phantom_storm_v2.py 192.168.1.100 80 300 --profile=aggressive")
    
    print("\n" + "="*80)
    print(" PROFILE SELECTION GUIDE ".center(80))
    print("="*80)
    
    print("""
┌─────────────────────────────────────────────────────────────────────────┐
│ SCENARIO                           │ RECOMMENDED PROFILE                │
├────────────────────────────────────┼────────────────────────────────────┤
│ Testing IDS/IPS detection          │ 🟢 Stealth                         │
│ Long-term sustained attack         │ 🟢 Stealth                         │
│ Bypassing rate limiting            │ 🟢 Stealth                         │
├────────────────────────────────────┼────────────────────────────────────┤
│ General DoS testing                │ 🟡 Balanced                        │
│ Standard pentest scenarios         │ 🟡 Balanced                        │
│ Quick initial assessment           │ 🟡 Balanced                        │
├────────────────────────────────────┼────────────────────────────────────┤
│ Stress testing server capacity     │ 🔴 Aggressive                      │
│ Finding resource limits            │ 🔴 Aggressive                      │
│ Maximum impact demonstration       │ 🔴 Aggressive                      │
└────────────────────────────────────┴────────────────────────────────────┘
""")
    
    print("\n⚠️  IMPORTANT NOTES:")
    print("   • Always get written authorization before testing")
    print("   • Start with Stealth profile to avoid detection")
    print("   • Monitor target server resources during testing")
    print("   • Use Aggressive profile only in isolated lab environments")
    print("   • Custom profiles can be created programmatically")
    
    # Show how to create custom profile
    print("\n" + "="*80)
    print(" CREATING CUSTOM PROFILES ".center(80))
    print("="*80)
    
    print("\n📝 Python Code Example:")
    print("""
from src.core import AttackProfiles, HTTPMethod

# Create a custom profile
custom = AttackProfiles.get_custom(
    threads=200,
    timeout=3,
    keep_alive_interval=5,
    http_method=HTTPMethod.POST,
    randomize_method=False,
    use_spoofing=True,
    delay_between_threads=0.05,
    delay_between_reconnect=1.0
)

print(custom.display_info())
""")
    
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()
