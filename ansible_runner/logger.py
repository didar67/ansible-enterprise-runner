"""
Logging configuration for Ansible Script Runner.

Must use rotating file handler for production readiness.
Contains a get_logger() factory to avoid global state issues.
"""

from logging import Logger, getLogger, Formatter, INFO
from logging.handlers import RotatingFileHandler
import logging
import os
from typing import Optional


def get_logger(
    name: str = "ansible_runner",
    level: int = INFO,
    logfile: Optional[str] = None,
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5,
) -> Logger:
    """
    Return a configured logger instance using RotatingFileHandler.
    Uses `if not logger.hasHandlers()` guard to prevent duplicate handlers.
    """
    logger = getLogger(name)
    logger.setLevel(level)

    # Prevent adding handlers multiple times in interactive environments/tests
    if not logger.handlers:
        fmt = Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        # Console handler
        console = logging.StreamHandler()
        console.setFormatter(fmt)
        logger.addHandler(console)

        # Optional file handler
        if logfile:
            os.makedirs(os.path.dirname(logfile), exist_ok=True)
            file_handler = RotatingFileHandler(
                logfile, maxBytes=max_bytes, backupCount=backup_count
            )
            file_handler.setFormatter(fmt)
            logger.addHandler(file_handler)

    return logger
