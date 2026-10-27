#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Core modules for Phantom Storm
"""

from .attack_worker import AttackWorker
from .statistics import AttackStatistics
from .ip_generator import IPGenerator
from .http_methods import HTTPMethodBuilder, HTTPMethod
from .attack_profiles import (
    AttackProfile,
    ProfileType,
    AttackProfiles,
    STEALTH,
    BALANCED,
    AGGRESSIVE
)
from .tls_handler import (
    TLSVersion,
    TLSConfig,
    TLSHandler,
    TLSHelper,
    create_https_socket
)
from .attack_types import AttackType
from .slow_post import SlowPostAttack, SlowPostHelper

__all__ = [
    'AttackWorker',
    'AttackStatistics',
    'IPGenerator',
    'HTTPMethodBuilder',
    'HTTPMethod',
    'AttackProfile',
    'ProfileType',
    'AttackProfiles',
    'STEALTH',
    'BALANCED',
    'AGGRESSIVE',
    'TLSVersion',
    'TLSConfig',
    'TLSHandler',
    'TLSHelper',
    'create_https_socket',
    'AttackType',
    'SlowPostAttack',
    'SlowPostHelper',
]
