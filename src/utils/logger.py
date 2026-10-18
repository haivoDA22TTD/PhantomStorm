#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Logging utilities for Phantom Storm
"""

import logging
import os
from typing import Optional

def setup_logging(log_file: Optional[str] = None):
    """
    Cấu hình logging system
    
    Args:
        log_file: Tên file log (sẽ tạo trong thư mục logs/)
    """
    log_format = '%(asctime)s - [%(levelname)s] - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    handlers = [logging.StreamHandler()]
    
    if log_file:
        # Create logs directory if not exists
        os.makedirs('logs', exist_ok=True)
        file_handler = logging.FileHandler(
            f'logs/{log_file}', 
            mode='a', 
            encoding='utf-8'
        )
        handlers.append(file_handler)
    
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=handlers
    )
    
    return logging.getLogger(__name__)
