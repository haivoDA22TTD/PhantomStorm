#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Phantom Storm v2.5 Ultimate Edition
Layer 7 HTTP Keep-Alive DoS Testing Tool with IP Spoofing
"""

__version__ = "2.5"
__author__ = "Phantom Storm Dev Team"
__license__ = "MIT"

from .core.attack_worker import AttackWorker
from .core.statistics import AttackStatistics
from .core.ip_generator import IPGenerator
from .utils.colors import Colors
from .utils.logger import setup_logging
from . import config

__all__ = [
    'AttackWorker',
    'AttackStatistics',
    'IPGenerator',
    'Colors',
    'setup_logging',
    'config'
]
