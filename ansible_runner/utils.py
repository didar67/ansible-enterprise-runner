"""
Utility helpers used across the project: path validation, safe joins, and subprocess helpers.

Recruiter notes:
- Keep functions small, testable, and documented.
- Use explicit exceptions rather than broad Exception for clarity.
"""

from pathlib import Path
import shutil
import os
from .exceptions import RunnerError


def ensure_file_readable(path: str) -> Path:
    """
    Ensure the given path exists and is readable. Return a Path object.
    Raises FileNotFoundError or PermissionError if there is a problem.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if not os.access(p, os.R_OK):
        raise PermissionError(f"File not readable: {path}")
    return p


def safe_join(base: str, *paths: str) -> str:
    """
    Safely join base and supplied paths, preventing path traversal.
    Returns a string path.
    """
    base_path = Path(base).resolve()
    candidate = base_path.joinpath(*paths).resolve()
    if str(candidate).startswith(str(base_path)):
        return str(candidate)
    raise RunnerError(f"Attempted path traversal: {candidate}")


def which(binary_name: str) -> str | None:
    """
    Return absolute path to a binary or None if not found.
    """
    result = shutil.which(binary_name)
    return result
