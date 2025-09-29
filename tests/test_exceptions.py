"""
Tests for exceptions.py using pytest.
Focuses on: RunnerError, ConfigValidationError, ProcessExecutionError.
"""

import pytest
from ansible_runner.exceptions import (
    RunnerError,
    ConfigValidationError,
    ProcessExecutionError,
)


def test_runner_error_is_exception():
    """Test that RunnerError is a subclass of Exception."""
    assert issubclass(RunnerError, Exception)


def test_config_validation_error_inherits_from_runner_error():
    """Test that ConfigValidationError inherits from RunnerError."""
    assert issubclass(ConfigValidationError, RunnerError)


def test_process_execution_error_inherits_from_runner_error():
    """Test that ProcessExecutionError inherits from RunnerError."""
    assert issubclass(ProcessExecutionError, RunnerError)


def test_process_execution_error_attributes():
    """Test ProcessExecutionError stores returncode, stdout, stderr."""
    returncode = 1
    stdout = "some output"
    stderr = "some error"
    error = ProcessExecutionError(returncode, stdout, stderr)
    assert error.returncode == returncode
    assert error.stdout == stdout
    assert error.stderr == stderr
    assert str(error) == f"Process failed with exit code {returncode}"


def test_process_execution_error_default_values():
    """Test ProcessExecutionError with default stdout and stderr."""
    error = ProcessExecutionError(2)
    assert error.returncode == 2
    assert error.stdout == ""
    assert error.stderr == ""
    assert str(error) == "Process failed with exit code 2"
