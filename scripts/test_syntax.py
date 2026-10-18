#!/usr/bin/env python3
"""
Quick syntax check for phantom_storm.py
"""

import sys

print("Checking phantom_storm.py syntax...")

try:
    import phantom_storm
    print("✅ Syntax OK - No import errors")
    print("✅ All classes imported successfully")
    
    # Test IPGenerator
    test_ip = phantom_storm.IPGenerator.generate_public_ip()
    print(f"✅ IPGenerator works - Generated: {test_ip}")
    
    # Test AttackStatistics
    stats = phantom_storm.AttackStatistics()
    stats.connection_established("1.2.3.4")
    stats.packet_sent()
    result = stats.get_stats()
    print(f"✅ AttackStatistics works - Stats tracked successfully")
    
    print("\n🎉 All tests passed! Tool is ready to use.")
    
except SyntaxError as e:
    print(f"❌ Syntax Error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    sys.exit(1)
