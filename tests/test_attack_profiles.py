#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit Tests for Attack Profiles
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.attack_profiles import (
    AttackProfile,
    ProfileType,
    AttackProfiles,
    STEALTH,
    BALANCED,
    AGGRESSIVE
)
from src.core.http_methods import HTTPMethod

class TestAttackProfile(unittest.TestCase):
    """Test AttackProfile dataclass"""
    
    def test_profile_creation(self):
        """Test creating a profile"""
        profile = AttackProfile(
            name="Test",
            description="Test profile",
            threads=100,
            timeout=5,
            keep_alive_interval=3,
            http_method=HTTPMethod.GET,
            randomize_method=False,
            use_spoofing=True,
            delay_between_threads=0.01,
            delay_between_reconnect=0.5
        )
        
        self.assertEqual(profile.name, "Test")
        self.assertEqual(profile.threads, 100)
        self.assertEqual(profile.http_method, HTTPMethod.GET)
        self.assertTrue(profile.use_spoofing)
    
    def test_display_info(self):
        """Test profile display info"""
        profile = AttackProfiles.get_balanced()
        info = profile.display_info()
        
        self.assertIn("Balanced", info)
        self.assertIn("150", info)  # Thread count
        self.assertIn("GET", info)  # HTTP method

class TestProfileType(unittest.TestCase):
    """Test ProfileType enum"""
    
    def test_enum_values(self):
        """Test enum has correct values"""
        self.assertEqual(ProfileType.STEALTH.value, "stealth")
        self.assertEqual(ProfileType.BALANCED.value, "balanced")
        self.assertEqual(ProfileType.AGGRESSIVE.value, "aggressive")
        self.assertEqual(ProfileType.CUSTOM.value, "custom")

class TestAttackProfiles(unittest.TestCase):
    """Test AttackProfiles factory class"""
    
    def test_get_stealth(self):
        """Test stealth profile"""
        profile = AttackProfiles.get_stealth()
        
        self.assertEqual(profile.name, "Stealth")
        self.assertEqual(profile.threads, 50)
        self.assertEqual(profile.keep_alive_interval, 10)
        self.assertTrue(profile.randomize_method)
        self.assertTrue(profile.use_spoofing)
        self.assertEqual(profile.delay_between_reconnect, 2.0)
    
    def test_get_balanced(self):
        """Test balanced profile"""
        profile = AttackProfiles.get_balanced()
        
        self.assertEqual(profile.name, "Balanced")
        self.assertEqual(profile.threads, 150)
        self.assertEqual(profile.keep_alive_interval, 3)
        self.assertEqual(profile.http_method, HTTPMethod.GET)
        self.assertFalse(profile.randomize_method)
        self.assertTrue(profile.use_spoofing)
    
    def test_get_aggressive(self):
        """Test aggressive profile"""
        profile = AttackProfiles.get_aggressive()
        
        self.assertEqual(profile.name, "Aggressive")
        self.assertEqual(profile.threads, 300)
        self.assertEqual(profile.keep_alive_interval, 1)
        self.assertEqual(profile.http_method, HTTPMethod.POST)
        self.assertFalse(profile.randomize_method)
        self.assertEqual(profile.delay_between_reconnect, 0.1)
    
    def test_get_custom(self):
        """Test custom profile creation"""
        profile = AttackProfiles.get_custom(
            threads=200,
            timeout=5,
            keep_alive_interval=4,
            http_method=HTTPMethod.HEAD,
            randomize_method=True,
            use_spoofing=False,
            delay_between_threads=0.05,
            delay_between_reconnect=1.0
        )
        
        self.assertEqual(profile.name, "Custom")
        self.assertEqual(profile.threads, 200)
        self.assertEqual(profile.timeout, 5)
        self.assertEqual(profile.http_method, HTTPMethod.HEAD)
        self.assertTrue(profile.randomize_method)
        self.assertFalse(profile.use_spoofing)
    
    def test_get_custom_defaults(self):
        """Test custom profile with default values"""
        profile = AttackProfiles.get_custom()
        
        self.assertEqual(profile.name, "Custom")
        self.assertEqual(profile.threads, 100)
        self.assertTrue(profile.use_spoofing)
    
    def test_get_profile_by_type(self):
        """Test getting profile by ProfileType enum"""
        stealth = AttackProfiles.get_profile(ProfileType.STEALTH)
        balanced = AttackProfiles.get_profile(ProfileType.BALANCED)
        aggressive = AttackProfiles.get_profile(ProfileType.AGGRESSIVE)
        
        self.assertEqual(stealth.name, "Stealth")
        self.assertEqual(balanced.name, "Balanced")
        self.assertEqual(aggressive.name, "Aggressive")
    
    def test_list_profiles(self):
        """Test listing all profiles"""
        profiles = AttackProfiles.list_profiles()
        
        self.assertEqual(len(profiles), 3)
        names = [p.name for p in profiles]
        self.assertIn("Stealth", names)
        self.assertIn("Balanced", names)
        self.assertIn("Aggressive", names)
    
    def test_compare_profiles(self):
        """Test profile comparison output"""
        comparison = AttackProfiles.compare_profiles()
        
        self.assertIn("COMPARISON", comparison)
        self.assertIn("Stealth", comparison)
        self.assertIn("Balanced", comparison)
        self.assertIn("Aggressive", comparison)
        self.assertIn("50", comparison)   # Stealth threads
        self.assertIn("150", comparison)  # Balanced threads
        self.assertIn("300", comparison)  # Aggressive threads

class TestProfileConstants(unittest.TestCase):
    """Test convenience constants"""
    
    def test_stealth_constant(self):
        """Test STEALTH constant"""
        self.assertEqual(STEALTH.name, "Stealth")
        self.assertEqual(STEALTH.threads, 50)
    
    def test_balanced_constant(self):
        """Test BALANCED constant"""
        self.assertEqual(BALANCED.name, "Balanced")
        self.assertEqual(BALANCED.threads, 150)
    
    def test_aggressive_constant(self):
        """Test AGGRESSIVE constant"""
        self.assertEqual(AGGRESSIVE.name, "Aggressive")
        self.assertEqual(AGGRESSIVE.threads, 300)

class TestProfileCharacteristics(unittest.TestCase):
    """Test profile characteristics match intended use cases"""
    
    def test_stealth_is_stealthy(self):
        """Stealth should have characteristics for avoiding detection"""
        profile = AttackProfiles.get_stealth()
        
        # Low thread count
        self.assertLessEqual(profile.threads, 100)
        
        # Long intervals
        self.assertGreaterEqual(profile.keep_alive_interval, 10)
        
        # Randomization for diversity
        self.assertTrue(profile.randomize_method)
        
        # Slow reconnects
        self.assertGreaterEqual(profile.delay_between_reconnect, 1.0)
    
    def test_balanced_is_moderate(self):
        """Balanced should have moderate settings"""
        profile = AttackProfiles.get_balanced()
        
        # Medium thread count
        self.assertGreater(profile.threads, 100)
        self.assertLess(profile.threads, 250)
        
        # Standard intervals
        self.assertGreater(profile.keep_alive_interval, 1)
        self.assertLess(profile.keep_alive_interval, 10)
    
    def test_aggressive_is_intense(self):
        """Aggressive should have maximum impact settings"""
        profile = AttackProfiles.get_aggressive()
        
        # High thread count
        self.assertGreaterEqual(profile.threads, 300)
        
        # Short intervals
        self.assertLessEqual(profile.keep_alive_interval, 1)
        
        # Fast reconnects
        self.assertLessEqual(profile.delay_between_reconnect, 0.5)
        
        # POST for heavier requests
        self.assertEqual(profile.http_method, HTTPMethod.POST)

class TestProfileOrdering(unittest.TestCase):
    """Test that profiles are ordered from least to most aggressive"""
    
    def test_thread_count_ordering(self):
        """Thread counts should increase: stealth < balanced < aggressive"""
        stealth = AttackProfiles.get_stealth()
        balanced = AttackProfiles.get_balanced()
        aggressive = AttackProfiles.get_aggressive()
        
        self.assertLess(stealth.threads, balanced.threads)
        self.assertLess(balanced.threads, aggressive.threads)
    
    def test_interval_ordering(self):
        """Intervals should decrease: stealth > balanced > aggressive"""
        stealth = AttackProfiles.get_stealth()
        balanced = AttackProfiles.get_balanced()
        aggressive = AttackProfiles.get_aggressive()
        
        self.assertGreater(stealth.keep_alive_interval, balanced.keep_alive_interval)
        self.assertGreater(balanced.keep_alive_interval, aggressive.keep_alive_interval)
    
    def test_delay_ordering(self):
        """Reconnect delays should decrease: stealth > balanced > aggressive"""
        stealth = AttackProfiles.get_stealth()
        balanced = AttackProfiles.get_balanced()
        aggressive = AttackProfiles.get_aggressive()
        
        self.assertGreater(stealth.delay_between_reconnect, balanced.delay_between_reconnect)
        self.assertGreater(balanced.delay_between_reconnect, aggressive.delay_between_reconnect)

def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAttackProfile))
    suite.addTests(loader.loadTestsFromTestCase(TestProfileType))
    suite.addTests(loader.loadTestsFromTestCase(TestAttackProfiles))
    suite.addTests(loader.loadTestsFromTestCase(TestProfileConstants))
    suite.addTests(loader.loadTestsFromTestCase(TestProfileCharacteristics))
    suite.addTests(loader.loadTestsFromTestCase(TestProfileOrdering))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)
