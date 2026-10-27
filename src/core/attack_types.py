#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Attack Types - Different DoS attack methods
============================================

Defines various attack types supported by Phantom Storm:
- Slowloris (default) - Keep-alive exhaustion
- Slow POST - POST body slowdown
- Slow Read - Response read slowdown
- Range Header - Apache Killer style
- Cache Bypass - Backend overload
"""

from enum import Enum

class AttackType(Enum):
    """
    Supported attack types
    """
    SLOWLORIS = "slowloris"          # Default: Keep-alive exhaustion
    SLOW_POST = "slow-post"           # POST body sent extremely slowly
    SLOW_READ = "slow-read"           # Read response extremely slowly
    RANGE_HEADER = "range-header"     # Multiple byte ranges (Apache Killer)
    CACHE_BYPASS = "cache-bypass"     # Random parameters to bypass cache
    
    @classmethod
    def get_description(cls, attack_type: 'AttackType') -> str:
        """Get human-readable description of attack type"""
        descriptions = {
            cls.SLOWLORIS: "Keep-Alive exhaustion - Hold connections with slow headers",
            cls.SLOW_POST: "Slow POST - Send POST body extremely slowly to exhaust upload handlers",
            cls.SLOW_READ: "Slow Read - Read server response extremely slowly to exhaust memory",
            cls.RANGE_HEADER: "Range Header - Request multiple byte ranges to spike CPU (Apache Killer)",
            cls.CACHE_BYPASS: "Cache Bypass - Random parameters to hit backend directly"
        }
        return descriptions.get(attack_type, "Unknown attack type")
    
    @classmethod
    def list_all(cls) -> list:
        """List all available attack types"""
        return [attack.value for attack in cls]

__all__ = ['AttackType']
