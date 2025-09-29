"""
Tests for logger.py using pytest.
Focuses on: get_logger function, handler setup, rotating file handler.
"""

import pytest
import logging
import logging.handlers
import tempfile
import os
from pathlib import Path
from ansible_runner import logger


def test_get_logger_default():
    """Test get_logger with default parameters."""
    test_logger = logger.get_logger("test_default")
    assert test_logger.name == "test_default"
    assert test_logger.level == logging.INFO
    assert len(test_logger.handlers) == 1  # Only console handler by default
    assert isinstance(test_logger.handlers[0], logging.StreamHandler)


def test_get_logger_with_logfile(tmp_path):
    """Test get_logger with logfile parameter adds file handler."""
    logfile = tmp_path / "test.log"
    test_logger = logger.get_logger("test_file", logfile=str(logfile))
    assert len(test_logger.handlers) == 2  # Console and file
    file_handler = None
    for handler in test_logger.handlers:
        if isinstance(handler, logging.handlers.RotatingFileHandler):
            file_handler = handler
            break
    assert file_handler is not None
    assert file_handler.baseFilename == str(logfile)


def test_get_logger_no_duplicate_handlers():
    """Test that calling get_logger multiple times doesn't add duplicate handlers."""
    test_logger = logger.get_logger("test_duplicate")
    initial_count = len(test_logger.handlers)
    # Call again
    logger.get_logger("test_duplicate")
    assert len(test_logger.handlers) == initial_count


def test_get_logger_custom_level():
    """Test get_logger with custom log level."""
    test_logger = logger.get_logger("test_level", level=logging.DEBUG)
    assert test_logger.level == logging.DEBUG


def test_get_logger_rotating_file_params(tmp_path):
    """Test get_logger with custom max_bytes and backup_count."""
    logfile = tmp_path / "test_rotate.log"
    max_bytes = 1024
    backup_count = 3
    test_logger = logger.get_logger(
        "test_rotate",
        logfile=str(logfile),
        max_bytes=max_bytes,
        backup_count=backup_count,
    )
    file_handler = None
    for handler in test_logger.handlers:
        if isinstance(handler, logging.handlers.RotatingFileHandler):
            file_handler = handler
            break
    assert file_handler is not None, "RotatingFileHandler was not found in logger handlers"
    assert file_handler.maxBytes == max_bytes
    assert file_handler.backupCount == backup_count

def test_get_logger_creates_logfile_directory(tmp_path):
    """Test that get_logger creates the directory for logfile if it doesn't exist."""
    subdir = tmp_path / "logs" / "subdir"
    logfile = subdir / "test.log"
    assert not subdir.exists()
    test_logger = logger.get_logger("test_dir", logfile=str(logfile))
    assert subdir.exists()
