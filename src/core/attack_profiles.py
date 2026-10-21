#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Attack Profiles - Predefined attack configurations
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional
from .http_methods import HTTPMethod

class ProfileType(Enum):
    """Available attack profiles"""
    STEALTH = "stealth"          # Slow & Stealthy - Hard to detect
    BALANCED = "balanced"        # Balanced approach
    AGGRESSIVE = "aggressive"    # Fast & Heavy attack
    CUSTOM = "custom"            # User-defined

@dataclass
class AttackProfile:
    """
    Attack profile configuration
    
    Attributes:
        name: Profile name
        description: Profile description
        threads: Number of threads
        timeout: Socket timeout
        keep_alive_interval: Interval between garbage headers
        http_method: HTTP method to use (None = random)
        randomize_method: Use random methods
        use_spoofing: Enable IP spoofing
        delay_between_threads: Delay when creating threads
        delay_between_reconnect: Delay before reconnecting
    """
    name: str
    description: str
    threads: int
    timeout: int
    keep_alive_interval: int
    http_method: Optional[HTTPMethod]
    randomize_method: bool
    use_spoofing: bool
    delay_between_threads: float
    delay_between_reconnect: float
    
    def display_info(self) -> str:
        """Get formatted profile information"""
        method_str = "RANDOM" if self.randomize_method else (
            self.http_method.value if self.http_method else "GET"
        )
        
        return f"""
Profile: {self.name}
Description: {self.description}
─────────────────────────────────────────
Threads               : {self.threads}
Socket Timeout        : {self.timeout}s
Keep-Alive Interval   : {self.keep_alive_interval}s
HTTP Method           : {method_str}
IP Spoofing           : {'ENABLED' if self.use_spoofing else 'DISABLED'}
Thread Creation Delay : {self.delay_between_threads}s
Reconnect Delay       : {self.delay_between_reconnect}s
"""

class AttackProfiles:
    """Predefined attack profiles"""
    
    @staticmethod
    def get_stealth() -> AttackProfile:
        """
        Stealth Profile - Slow & Hard to Detect
        
        Characteristics:
        - Low thread count (50-100)
        - Long intervals (10s keep-alive)
        - Random methods for diversity
        - IP spoofing enabled
        - Slow thread creation
        - Long reconnect delays
        
        Best for:
        - Bypassing IDS/IPS
        - Long-term sustained attacks
        - Avoiding rate limits
        - Testing defense effectiveness
        """
        return AttackProfile(
            name="Stealth",
            description="Slow & stealthy attack - hard to detect",
            threads=50,
            timeout=8,
            keep_alive_interval=10,
            http_method=None,
            randomize_method=True,
            use_spoofing=True,
            delay_between_threads=0.1,
            delay_between_reconnect=2.0
        )
    
    @staticmethod
    def get_balanced() -> AttackProfile:
        """
        Balanced Profile - Good Mix of Speed & Stealth
        
        Characteristics:
        - Medium thread count (150-200)
        - Standard intervals (3s keep-alive)
        - GET method (standard)
        - IP spoofing enabled
        - Normal thread creation
        - Standard reconnect delay
        
        Best for:
        - General purpose testing
        - Balanced resource usage
        - Standard DoS testing
        - Most common scenarios
        """
        return AttackProfile(
            name="Balanced",
            description="Balanced approach - speed & stealth",
            threads=150,
            timeout=4,
            keep_alive_interval=3,
            http_method=HTTPMethod.GET,
            randomize_method=False,
            use_spoofing=True,
            delay_between_threads=0.01,
            delay_between_reconnect=0.5
        )
    
    @staticmethod
    def get_aggressive() -> AttackProfile:
        """
        Aggressive Profile - Maximum Impact
        
        Characteristics:
        - High thread count (300-500)
        - Short intervals (1s keep-alive)
        - POST method (heavier)
        - IP spoofing enabled
        - Fast thread creation
        - Minimal reconnect delay
        
        Best for:
        - Maximum resource exhaustion
        - Quick impact testing
        - Stress testing
        - Capacity limit discovery
        """
        return AttackProfile(
            name="Aggressive",
            description="Fast & heavy attack - maximum impact",
            threads=300,
            timeout=2,
            keep_alive_interval=1,
            http_method=HTTPMethod.POST,
            randomize_method=False,
            use_spoofing=True,
            delay_between_threads=0.001,
            delay_between_reconnect=0.1
        )
    
    @staticmethod
    def get_custom(
        threads: int = 100,
        timeout: int = 4,
        keep_alive_interval: int = 3,
        http_method: Optional[HTTPMethod] = None,
        randomize_method: bool = False,
        use_spoofing: bool = True,
        delay_between_threads: float = 0.01,
        delay_between_reconnect: float = 0.5
    ) -> AttackProfile:
        """
        Custom Profile - User-defined configuration
        
        Args:
            threads: Number of threads
            timeout: Socket timeout
            keep_alive_interval: Keep-alive interval
            http_method: HTTP method (None for random)
            randomize_method: Randomize methods
            use_spoofing: Enable IP spoofing
            delay_between_threads: Thread creation delay
            delay_between_reconnect: Reconnect delay
            
        Returns:
            Custom attack profile
        """
        return AttackProfile(
            name="Custom",
            description="User-defined custom configuration",
            threads=threads,
            timeout=timeout,
            keep_alive_interval=keep_alive_interval,
            http_method=http_method,
            randomize_method=randomize_method,
            use_spoofing=use_spoofing,
            delay_between_threads=delay_between_threads,
            delay_between_reconnect=delay_between_reconnect
        )
    
    @staticmethod
    def get_profile(profile_type: ProfileType) -> AttackProfile:
        """
        Get profile by type
        
        Args:
            profile_type: Profile type enum
            
        Returns:
            Attack profile
        """
        profile_map = {
            ProfileType.STEALTH: AttackProfiles.get_stealth,
            ProfileType.BALANCED: AttackProfiles.get_balanced,
            ProfileType.AGGRESSIVE: AttackProfiles.get_aggressive,
        }
        
        getter = profile_map.get(profile_type)
        if getter:
            return getter()
        else:
            # Default to balanced
            return AttackProfiles.get_balanced()
    
    @staticmethod
    def list_profiles() -> list[AttackProfile]:
        """
        Get list of all predefined profiles
        
        Returns:
            List of attack profiles
        """
        return [
            AttackProfiles.get_stealth(),
            AttackProfiles.get_balanced(),
            AttackProfiles.get_aggressive()
        ]
    
    @staticmethod
    def compare_profiles() -> str:
        """
        Get comparison table of all profiles
        
        Returns:
            Formatted comparison string
        """
        profiles = AttackProfiles.list_profiles()
        
        output = """
╔════════════════════════════════════════════════════════════════════════╗
║                    ATTACK PROFILES COMPARISON                          ║
╚════════════════════════════════════════════════════════════════════════╝

┌────────────────┬─────────────┬─────────────┬──────────────────┐
│ Feature        │ Stealth     │ Balanced    │ Aggressive       │
├────────────────┼─────────────┼─────────────┼──────────────────┤
│ Threads        │ 50          │ 150         │ 300              │
│ Timeout        │ 8s          │ 4s          │ 2s               │
│ Keep-Alive Int │ 10s         │ 3s          │ 1s               │
│ HTTP Method    │ RANDOM      │ GET         │ POST             │
│ IP Spoofing    │ YES         │ YES         │ YES              │
│ Thread Delay   │ 0.1s        │ 0.01s       │ 0.001s           │
│ Reconnect      │ 2.0s        │ 0.5s        │ 0.1s             │
├────────────────┼─────────────┼─────────────┼──────────────────┤
│ Detection Risk │ LOW         │ MEDIUM      │ HIGH             │
│ Impact Speed   │ SLOW        │ MEDIUM      │ FAST             │
│ Resource Usage │ LOW         │ MEDIUM      │ HIGH             │
└────────────────┴─────────────┴─────────────┴──────────────────┘

RECOMMENDATIONS:
───────────────
• Stealth      → Long-term testing, bypass IDS/IPS
• Balanced     → General purpose, most scenarios
• Aggressive   → Maximum impact, stress testing
"""
        return output

# Convenience shortcuts
STEALTH = AttackProfiles.get_stealth()
BALANCED = AttackProfiles.get_balanced()
AGGRESSIVE = AttackProfiles.get_aggressive()
