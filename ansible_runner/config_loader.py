"""
Configuration loader using pydantic v2 for validation.
Validates and provides a typed configuration object.
"""

from pydantic import BaseModel, Field, ValidationError
from typing import Dict, Any
import yaml
from pathlib import Path
from .exceptions import ConfigValidationError


class AnsibleConfig(BaseModel):
    binary: str = Field(..., description="Path or name of ansible-playbook binary")
    default_playbook: str
    default_inventory: str
    default_extra_vars: Dict[str, Any] = {}
    working_dir: str = "."


class LoggingConfig(BaseModel):
    level: str = "INFO"
    file: str = "logs/ansible_runner.log"
    max_bytes: int = 10 * 1024 * 1024
    backup_count: int = 5


class RunnerConfig(BaseModel):
    timeout_seconds: int = 3600
    enable_async: bool = False


class AppConfig(BaseModel):
    ansible: AnsibleConfig
    logging: LoggingConfig
    runner: RunnerConfig


def load_config(path: str) -> AppConfig:
    """
    Load YAML config from `path` and validate using Pydantic v2 models.
    Raises ConfigValidationError on problems for clear unit testing.
    """
    p = Path(path)
    try:
        content = p.read_text(encoding="utf-8")
    except FileNotFoundError as e:
        raise ConfigValidationError(f"Config file not found: {path}") from e
    try:
        raw = yaml.safe_load(content) or {}
        cfg = AppConfig.model_validate(raw)
        return cfg
    except ValidationError as e:
        # Wrap pydantic's validation error for application-level handling
        raise ConfigValidationError(f"Invalid configuration: {e}") from e
