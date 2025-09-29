"""
Tests for utils.py using pytest.
Focuses on: ensure_file_readable, safe_join, which (mockable if needed).
"""

import pytest
from ansible_runner import utils
from pathlib import Path
import os
from ansible_runner.exceptions import RunnerError


def test_safe_join_allows_subpath(tmp_path):
    base = tmp_path / "base"
    base.mkdir()
    child = "sub/dir/file.txt"
    joined = utils.safe_join(str(base), child)
    assert str(Path(joined)).startswith(str(base.resolve()))


def test_safe_join_disallows_traversal(tmp_path):
    base = tmp_path / "base"
    base.mkdir()
    # Attempt to traverse outside base
    with pytest.raises(RunnerError):
        utils.safe_join(str(base), "../etc/passwd")


def test_ensure_file_readable_missing(tmp_path):
    missing = tmp_path / "nope.txt"
    with pytest.raises(FileNotFoundError):
        utils.ensure_file_readable(str(missing))


def test_which_returns_none_for_nonexistent_binary(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda x: None)
    assert utils.which("some_nonexistent_binary_1234") is None
