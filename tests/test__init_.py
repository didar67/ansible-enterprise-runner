"""
tests package initializer for Ansible Script Runner.

Purpose:
- Marks the tests folder as a Python package.
- Provides light test-time logging guard so test runs don't accidentally add duplicate handlers.
- Recruiter Standard Comment Style: concise purpose, maintainability hint, and where to put heavier test fixtures.

Notes:
- For shared fixtures prefer placing them in `tests/conftest.py`.
- This file intentionally keeps logic minimal to avoid side-effects during discovery.
"""

from __future__ import annotations

import logging

# Add a NullHandler to the package logger to avoid spamming test output and to
# prevent the package-level get_logger() factory from adding duplicate handlers
# when tests import modules repeatedly. This is a safe, minimal test-time guard.
logging.getLogger("ansible_runner").addHandler(logging.NullHandler())

__all__ = []
