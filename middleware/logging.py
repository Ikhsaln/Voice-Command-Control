"""
Logging Module for Voice Relay System
Provides centralized logging configuration and utilities.
"""

import logging
import os
from datetime import datetime
from typing import Optional

def setup_logging(log_level: int = logging.INFO) -> logging.Logger:
    """
    Setup logging configuration with file and console handlers.

    Args:
        log_level: Logging level (e.g., logging.INFO, logging.DEBUG)

    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Create logger
    logger = logging.getLogger('voice_relay')
    logger.setLevel(log_level)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create file handler
    log_file = os.path.join(log_dir, f'voice_relay_{datetime.now().strftime("%Y%m%d")}.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def log_simple(message: str, level: str = "INFO") -> None:
    """
    Simple logging function for backward compatibility.

    Args:
        message: Log message
        level: Log level string (DEBUG, INFO, WARNING, ERROR, CRITICAL, SUCCESS)
    """
    logger = logging.getLogger('voice_relay')
    if not logger.handlers:
        logger = setup_logging()

    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
        "SUCCESS": logging.INFO  # Treat SUCCESS as INFO
    }

    logger.log(level_map.get(level.upper(), logging.INFO), message)
