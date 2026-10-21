#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit Tests for TLS/HTTPS Handler
"""

import unittest
import socket
import ssl
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.tls_handler import (
    TLSVersion,
    TLSConfig,
    TLSHandler,
    TLSHelper,
    create_https_socket
)

class TestTLSVersion(unittest.TestCase):
    """Test TLSVersion enum"""
    
    def test_enum_values(self):
        """Test enum has correct values"""
        self.assertEqual(TLSVersion.TLS_1_0.value, "TLS_1_0")
        self.assertEqual(TLSVersion.TLS_1_1.value, "TLS_1_1")
        self.assertEqual(TLSVersion.TLS_1_2.value, "TLS_1_2")
        self.assertEqual(TLSVersion.TLS_1_3.value, "TLS_1_3")
        self.assertEqual(TLSVersion.AUTO.value, "AUTO")

class TestTLSConfig(unittest.TestCase):
    """Test TLSConfig dataclass"""
    
    def test_default_config(self):
        """Test default TLS configuration"""
        config = TLSConfig()
        
        self.assertFalse(config.use_https)
        self.assertFalse(config.verify_ssl)
        self.assertEqual(config.tls_version, "AUTO")
        self.assertIsNone(config.sni_hostname)
        self.assertEqual(config.timeout, 10)
        self.assertIsNone(config.ciphers)
    
    def test_custom_config(self):
        """Test custom TLS configuration"""
        config = TLSConfig(
            use_https=True,
            verify_ssl=True,
            tls_version="TLS_1_2",
            sni_hostname="www.example.com",
            timeout=5,
            ciphers="HIGH:!aNULL"
        )
        
        self.assertTrue(config.use_https)
        self.assertTrue(config.verify_ssl)
        self.assertEqual(config.tls_version, "TLS_1_2")
        self.assertEqual(config.sni_hostname, "www.example.com")
        self.assertEqual(config.timeout, 5)
        self.assertEqual(config.ciphers, "HIGH:!aNULL")
    
    def test_https_config(self):
        """Test HTTPS-enabled configuration"""
        config = TLSConfig(use_https=True)
        
        self.assertTrue(config.use_https)
        # Other defaults should remain
        self.assertFalse(config.verify_ssl)
        self.assertEqual(config.tls_version, "AUTO")

class TestTLSHandler(unittest.TestCase):
    """Test TLSHandler class"""
    
    def test_handler_creation(self):
        """Test creating TLS handler"""
        config = TLSConfig(use_https=True)
        handler = TLSHandler(config)
        
        self.assertIsNotNone(handler)
        self.assertEqual(handler.config, config)
        self.assertIsNotNone(handler.ssl_context)
    
    def test_handler_without_https(self):
        """Test handler with HTTPS disabled"""
        config = TLSConfig(use_https=False)
        handler = TLSHandler(config)
        
        # Should still create handler
        self.assertIsNotNone(handler)
    
    def test_ssl_context_creation_auto(self):
        """Test SSL context with AUTO version"""
        config = TLSConfig(use_https=True, tls_version="AUTO")
        handler = TLSHandler(config)
        
        self.assertIsInstance(handler.ssl_context, ssl.SSLContext)
    
    def test_ssl_context_creation_tls12(self):
        """Test SSL context with TLS 1.2"""
        config = TLSConfig(use_https=True, tls_version="TLS_1_2")
        handler = TLSHandler(config)
        
        self.assertIsInstance(handler.ssl_context, ssl.SSLContext)
    
    def test_ssl_context_no_verify(self):
        """Test SSL context without certificate verification"""
        config = TLSConfig(use_https=True, verify_ssl=False)
        handler = TLSHandler(config)
        
        self.assertEqual(handler.ssl_context.verify_mode, ssl.CERT_NONE)
        self.assertFalse(handler.ssl_context.check_hostname)
    
    def test_ssl_context_with_verify(self):
        """Test SSL context with certificate verification"""
        config = TLSConfig(use_https=True, verify_ssl=True)
        handler = TLSHandler(config)
        
        self.assertEqual(handler.ssl_context.verify_mode, ssl.CERT_REQUIRED)
        self.assertTrue(handler.ssl_context.check_hostname)
    
    def test_wrap_socket_mock(self):
        """Test socket wrapping (mock test)"""
        config = TLSConfig(use_https=True, verify_ssl=False)
        handler = TLSHandler(config)
        
        # We can't actually wrap without a real connection
        # Just verify the handler has the method
        self.assertTrue(hasattr(handler, 'wrap_socket'))
        self.assertTrue(callable(handler.wrap_socket))
    
    def test_get_cipher_info_method_exists(self):
        """Test get_cipher_info method exists"""
        config = TLSConfig(use_https=True)
        handler = TLSHandler(config)
        
        self.assertTrue(hasattr(handler, 'get_cipher_info'))
        self.assertTrue(callable(handler.get_cipher_info))
    
    def test_get_peer_certificate_method_exists(self):
        """Test get_peer_certificate method exists"""
        config = TLSConfig(use_https=True)
        handler = TLSHandler(config)
        
        self.assertTrue(hasattr(handler, 'get_peer_certificate'))
        self.assertTrue(callable(handler.get_peer_certificate))
    
    def test_get_protocol_version_method_exists(self):
        """Test get_protocol_version method exists"""
        config = TLSConfig(use_https=True)
        handler = TLSHandler(config)
        
        self.assertTrue(hasattr(handler, 'get_protocol_version'))
        self.assertTrue(callable(handler.get_protocol_version))

class TestTLSHelper(unittest.TestCase):
    """Test TLSHelper utility functions"""
    
    def test_is_https_port(self):
        """Test HTTPS port detection"""
        # Common HTTPS ports
        self.assertTrue(TLSHelper.is_https_port(443))
        self.assertTrue(TLSHelper.is_https_port(8443))
        self.assertTrue(TLSHelper.is_https_port(9443))
        self.assertTrue(TLSHelper.is_https_port(8080))
        
        # HTTP port
        self.assertFalse(TLSHelper.is_https_port(80))
        self.assertFalse(TLSHelper.is_https_port(8000))
    
    def test_extract_hostname_from_url(self):
        """Test hostname extraction from URL"""
        # Full URL
        hostname = TLSHelper.extract_hostname_from_url("https://www.example.com/path")
        self.assertEqual(hostname, "www.example.com")
        
        # HTTP URL
        hostname = TLSHelper.extract_hostname_from_url("http://example.com:8080")
        self.assertEqual(hostname, "example.com")
        
        # Just hostname
        hostname = TLSHelper.extract_hostname_from_url("www.example.com")
        self.assertEqual(hostname, "www.example.com")
        
        # IP address
        hostname = TLSHelper.extract_hostname_from_url("https://192.168.1.1")
        self.assertEqual(hostname, "192.168.1.1")
    
    def test_get_available_tls_versions(self):
        """Test getting available TLS versions"""
        versions = TLSHelper.get_available_tls_versions()
        
        self.assertIsInstance(versions, list)
        self.assertGreater(len(versions), 0)
        self.assertIn("AUTO", versions)
        
        # Should have at least TLS 1.2 in modern Python
        self.assertIn("TLS_1_2", versions)
    
    def test_format_cipher_suite_empty(self):
        """Test formatting empty cipher info"""
        result = TLSHelper.format_cipher_suite({})
        self.assertEqual(result, "Unknown")
    
    def test_format_cipher_suite_with_data(self):
        """Test formatting cipher info with data"""
        cipher_info = {
            'name': 'ECDHE-RSA-AES256-GCM-SHA384',
            'protocol': 'TLSv1.2',
            'bits': 256
        }
        
        result = TLSHelper.format_cipher_suite(cipher_info)
        self.assertIn('ECDHE-RSA-AES256-GCM-SHA384', result)
        self.assertIn('256', result)
        self.assertIn('TLSv1.2', result)
    
    def test_validate_tls_config_valid(self):
        """Test validating valid TLS config"""
        config = TLSConfig(
            use_https=True,
            tls_version="TLS_1_2",
            timeout=10
        )
        
        is_valid, error = TLSHelper.validate_tls_config(config)
        self.assertTrue(is_valid)
        self.assertEqual(error, "")
    
    def test_validate_tls_config_invalid_version(self):
        """Test validating config with invalid TLS version"""
        config = TLSConfig(
            use_https=True,
            tls_version="TLS_9_9",  # Invalid
            timeout=10
        )
        
        is_valid, error = TLSHelper.validate_tls_config(config)
        self.assertFalse(is_valid)
        self.assertIn("Invalid TLS version", error)
    
    def test_validate_tls_config_invalid_timeout(self):
        """Test validating config with invalid timeout"""
        config = TLSConfig(
            use_https=True,
            tls_version="AUTO",
            timeout=-5  # Invalid
        )
        
        is_valid, error = TLSHelper.validate_tls_config(config)
        self.assertFalse(is_valid)
        self.assertIn("Timeout must be positive", error)
    
    def test_validate_tls_config_zero_timeout(self):
        """Test validating config with zero timeout"""
        config = TLSConfig(
            use_https=True,
            timeout=0  # Invalid
        )
        
        is_valid, error = TLSHelper.validate_tls_config(config)
        self.assertFalse(is_valid)
        self.assertIn("Timeout must be positive", error)

class TestTLSConfigScenarios(unittest.TestCase):
    """Test common TLS configuration scenarios"""
    
    def test_lab_environment_config(self):
        """Test config for lab with self-signed certificates"""
        config = TLSConfig(
            use_https=True,
            verify_ssl=False,  # Accept self-signed
            tls_version="AUTO",
            timeout=10
        )
        
        handler = TLSHandler(config)
        self.assertEqual(handler.ssl_context.verify_mode, ssl.CERT_NONE)
    
    def test_production_config(self):
        """Test config for production with valid certificates"""
        config = TLSConfig(
            use_https=True,
            verify_ssl=True,  # Verify certificates
            tls_version="TLS_1_2",
            sni_hostname="www.production.com",
            timeout=5
        )
        
        handler = TLSHandler(config)
        self.assertEqual(handler.ssl_context.verify_mode, ssl.CERT_REQUIRED)
        self.assertEqual(config.sni_hostname, "www.production.com")
    
    def test_tls12_only_config(self):
        """Test forcing TLS 1.2 only"""
        config = TLSConfig(
            use_https=True,
            tls_version="TLS_1_2"
        )
        
        handler = TLSHandler(config)
        self.assertIsNotNone(handler.ssl_context)
    
    def test_virtual_hosting_config(self):
        """Test config for virtual hosting with SNI"""
        config = TLSConfig(
            use_https=True,
            sni_hostname="site1.example.com",
            verify_ssl=False
        )
        
        self.assertEqual(config.sni_hostname, "site1.example.com")

class TestTLSVersionCompatibility(unittest.TestCase):
    """Test TLS version compatibility"""
    
    def test_all_versions_create_context(self):
        """Test that all TLS versions can create SSL context"""
        versions = ["TLS_1_0", "TLS_1_1", "TLS_1_2", "TLS_1_3", "AUTO"]
        
        for version in versions:
            config = TLSConfig(use_https=True, tls_version=version)
            handler = TLSHandler(config)
            
            # Should create context without error
            self.assertIsNotNone(handler.ssl_context)
            self.assertIsInstance(handler.ssl_context, ssl.SSLContext)

class TestCreateHTTPSSocket(unittest.TestCase):
    """Test convenience function create_https_socket"""
    
    def test_function_exists(self):
        """Test create_https_socket function exists"""
        self.assertTrue(callable(create_https_socket))
    
    def test_function_signature(self):
        """Test function has correct signature"""
        import inspect
        sig = inspect.signature(create_https_socket)
        params = list(sig.parameters.keys())
        
        self.assertIn('target_ip', params)
        self.assertIn('target_port', params)
        self.assertIn('config', params)

class TestTLSExports(unittest.TestCase):
    """Test module exports"""
    
    def test_all_exports(self):
        """Test __all__ contains expected items"""
        from src.core import tls_handler
        
        self.assertTrue(hasattr(tls_handler, '__all__'))
        
        expected = [
            'TLSVersion',
            'TLSConfig',
            'TLSHandler',
            'TLSHelper',
            'create_https_socket'
        ]
        
        for item in expected:
            self.assertIn(item, tls_handler.__all__)

def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestTLSVersion))
    suite.addTests(loader.loadTestsFromTestCase(TestTLSConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestTLSHandler))
    suite.addTests(loader.loadTestsFromTestCase(TestTLSHelper))
    suite.addTests(loader.loadTestsFromTestCase(TestTLSConfigScenarios))
    suite.addTests(loader.loadTestsFromTestCase(TestTLSVersionCompatibility))
    suite.addTests(loader.loadTestsFromTestCase(TestCreateHTTPSSocket))
    suite.addTests(loader.loadTestsFromTestCase(TestTLSExports))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)
