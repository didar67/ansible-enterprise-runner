"""
Custom exceptions for Ansible Script Runner.

Keep domain-specific exceptions here so test code can assert on them.
"""


class RunnerError(Exception):
    """Base exception for runner errors."""

    pass


class ConfigValidationError(RunnerError):
    """Raised when configuration validation fails."""

    pass


class ProcessExecutionError(RunnerError):
    """Raised when subprocess execution fails with non-zero exit code."""

    def __init__(self, returncode: int, stdout: str = "", stderr: str = ""):
        super().__init__(f"Process failed with exit code {returncode}")
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
