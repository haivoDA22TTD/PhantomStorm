#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TLS/HTTPS Handler Module
========================

Provides SSL/TLS support for HTTPS attacks including:
- SSL socket wrapping
- TLS version selection
- SNI (Server Name Indication) support
- Certificate verification options
- SSL error handling

Usage:
    from src.core.tls_handler import TLSConfig, TLSHandler
    
    config = TLSConfig(
        use_https=True,
        verify_ssl=False,
        tls_version='TLS_1_2',
        sni_hostname='www.example.com'
    )
    
    handler = TLSHandler(config)
    secure_sock = handler.wrap_socket(raw_sock)
"""

import ssl
import socket
from dataclasses import dataclass
from typing import Optional
from enum import Enum

class TLSVersion(Enum):
    """Supported TLS versions"""
    TLS_1_0 = "TLS_1_0"
    TLS_1_1 = "TLS_1_1"
    TLS_1_2 = "TLS_1_2"
    TLS_1_3 = "TLS_1_3"
    AUTO = "AUTO"  # Let SSL module choose best available

@dataclass
class TLSConfig:
    """
    TLS/HTTPS configuration
    
    Attributes:
        use_https: Enable HTTPS mode
        verify_ssl: Verify SSL certificates (disable for self-signed)
        tls_version: TLS version to use (TLS_1_0, TLS_1_1, TLS_1_2, TLS_1_3, AUTO)
        sni_hostname: Server Name Indication hostname
        timeout: SSL handshake timeout
        ciphers: Custom cipher suite (None = default)
    """
    use_https: bool = False
    verify_ssl: bool = False
    tls_version: str = "AUTO"
    sni_hostname: Optional[str] = None
    timeout: int = 10
    ciphers: Optional[str] = None

class TLSHandler:
    """
    Handler for TLS/HTTPS connections
    
    Wraps raw sockets with SSL/TLS layer and handles SSL-specific configurations.
    """
    
    def __init__(self, config: TLSConfig):
        """
        Initialize TLS handler
        
        Args:
            config: TLS configuration object
        """
        self.config = config
        self.ssl_context = self._create_ssl_context()
    
    def _create_ssl_context(self) -> ssl.SSLContext:
        """
        Create SSL context with specified configuration
        
        Returns:
            Configured SSL context
        """
        # Select TLS version
        if self.config.tls_version == "TLS_1_0":
            protocol = ssl.PROTOCOL_TLSv1
        elif self.config.tls_version == "TLS_1_1":
            protocol = ssl.PROTOCOL_TLSv1_1
        elif self.config.tls_version == "TLS_1_2":
            protocol = ssl.PROTOCOL_TLSv1_2
        elif self.config.tls_version == "TLS_1_3":
            # TLS 1.3 uses PROTOCOL_TLS with minimum version set
            protocol = ssl.PROTOCOL_TLS
        else:  # AUTO
            protocol = ssl.PROTOCOL_TLS
        
        # Create context
        context = ssl.SSLContext(protocol)
        
        # Configure certificate verification
        if self.config.verify_ssl:
            context.check_hostname = True
            context.verify_mode = ssl.CERT_REQUIRED
            context.load_default_certs()
        else:
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
        
        # Set TLS 1.3 minimum version if specified
        if self.config.tls_version == "TLS_1_3":
            try:
                context.minimum_version = ssl.TLSVersion.TLSv1_3
            except AttributeError:
                # Python < 3.7 doesn't have TLSVersion
                pass
        
        # Set custom cipher suite if specified
        if self.config.ciphers:
            try:
                context.set_ciphers(self.config.ciphers)
            except ssl.SSLError:
                # Invalid cipher suite, use defaults
                pass
        
        return context
    
    def wrap_socket(self, sock: socket.socket, server_hostname: Optional[str] = None) -> ssl.SSLSocket:
        """
        Wrap a raw socket with SSL/TLS
        
        Args:
            sock: Raw socket to wrap
            server_hostname: Hostname for SNI (overrides config if provided)
        
        Returns:
            SSL-wrapped socket
        
        Raises:
            ssl.SSLError: If SSL handshake fails
            socket.timeout: If handshake times out
        """
        # Use provided hostname or config SNI hostname
        sni = server_hostname or self.config.sni_hostname
        
        # Wrap socket with SSL
        try:
            ssl_sock = self.ssl_context.wrap_socket(
                sock,
                server_hostname=sni,
                do_handshake_on_connect=True
            )
            return ssl_sock
        except ssl.SSLError as e:
            raise ssl.SSLError(f"SSL handshake failed: {e}")
        except socket.timeout as e:
            raise socket.timeout(f"SSL handshake timeout: {e}")
    
    def get_cipher_info(self, ssl_sock: ssl.SSLSocket) -> dict:
        """
        Get information about the negotiated cipher
        
        Args:
            ssl_sock: SSL socket to inspect
        
        Returns:
            Dictionary with cipher information
        """
        try:
            cipher = ssl_sock.cipher()
            if cipher:
                return {
                    'name': cipher[0],
                    'protocol': cipher[1],
                    'bits': cipher[2]
                }
        except:
            pass
        return {}
    
    def get_peer_certificate(self, ssl_sock: ssl.SSLSocket) -> Optional[dict]:
        """
        Get peer certificate information
        
        Args:
            ssl_sock: SSL socket to inspect
        
        Returns:
            Certificate information dict or None
        """
        try:
            cert = ssl_sock.getpeercert()
            return cert
        except:
            return None
    
    def get_protocol_version(self, ssl_sock: ssl.SSLSocket) -> str:
        """
        Get negotiated TLS protocol version
        
        Args:
            ssl_sock: SSL socket to inspect
        
        Returns:
            Protocol version string (e.g., "TLSv1.2")
        """
        try:
            return ssl_sock.version()
        except:
            return "Unknown"

class TLSHelper:
    """
    Helper functions for TLS operations
    """
    
    @staticmethod
    def is_https_port(port: int) -> bool:
        """
        Check if port is commonly used for HTTPS
        
        Args:
            port: Port number
        
        Returns:
            True if common HTTPS port
        """
        https_ports = [443, 8443, 9443, 8080]  # Common HTTPS ports
        return port in https_ports
    
    @staticmethod
    def extract_hostname_from_url(url: str) -> Optional[str]:
        """
        Extract hostname from URL for SNI
        
        Args:
            url: URL string
        
        Returns:
            Hostname or None
        """
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url if '//' in url else f'//{url}')
            return parsed.hostname
        except:
            return None
    
    @staticmethod
    def get_available_tls_versions() -> list:
        """
        Get list of TLS versions available in current Python
        
        Returns:
            List of available TLS version strings
        """
        versions = []
        
        # Check TLS 1.0
        try:
            ssl.PROTOCOL_TLSv1
            versions.append("TLS_1_0")
        except AttributeError:
            pass
        
        # Check TLS 1.1
        try:
            ssl.PROTOCOL_TLSv1_1
            versions.append("TLS_1_1")
        except AttributeError:
            pass
        
        # Check TLS 1.2
        try:
            ssl.PROTOCOL_TLSv1_2
            versions.append("TLS_1_2")
        except AttributeError:
            pass
        
        # Check TLS 1.3
        try:
            if hasattr(ssl, 'TLSVersion') and hasattr(ssl.TLSVersion, 'TLSv1_3'):
                versions.append("TLS_1_3")
        except:
            pass
        
        versions.append("AUTO")
        return versions
    
    @staticmethod
    def format_cipher_suite(cipher_info: dict) -> str:
        """
        Format cipher information for display
        
        Args:
            cipher_info: Cipher info dict from get_cipher_info()
        
        Returns:
            Formatted string
        """
        if not cipher_info:
            return "Unknown"
        
        return f"{cipher_info.get('name', 'Unknown')} ({cipher_info.get('bits', 0)} bits, {cipher_info.get('protocol', 'Unknown')})"
    
    @staticmethod
    def validate_tls_config(config: TLSConfig) -> tuple[bool, str]:
        """
        Validate TLS configuration
        
        Args:
            config: TLS configuration to validate
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check TLS version
        valid_versions = TLSHelper.get_available_tls_versions()
        if config.tls_version not in valid_versions:
            return False, f"Invalid TLS version. Available: {', '.join(valid_versions)}"
        
        # Check timeout
        if config.timeout <= 0:
            return False, "Timeout must be positive"
        
        return True, ""

# Convenience function
def create_https_socket(target_ip: str, target_port: int, config: TLSConfig) -> ssl.SSLSocket:
    """
    Create and connect an HTTPS socket in one call
    
    Args:
        target_ip: Target IP address
        target_port: Target port
        config: TLS configuration
    
    Returns:
        Connected SSL socket
    
    Raises:
        socket.error: Connection failed
        ssl.SSLError: SSL handshake failed
    """
    # Create raw socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(config.timeout)
    
    try:
        # Connect
        sock.connect((target_ip, target_port))
        
        # Wrap with SSL
        handler = TLSHandler(config)
        ssl_sock = handler.wrap_socket(sock)
        
        return ssl_sock
    except Exception as e:
        sock.close()
        raise

# Export commonly used items
__all__ = [
    'TLSVersion',
    'TLSConfig',
    'TLSHandler',
    'TLSHelper',
    'create_https_socket'
]
