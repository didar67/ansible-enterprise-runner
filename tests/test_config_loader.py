"""
Tests for ConfigLoader in config_loader.py
"""

import pytest
import yaml
from ansible_runner.config_loader import load_config, ConfigValidationError


def test_load_valid_config(tmp_path):
    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text(
        yaml.safe_dump(
            {
                "ansible": {
                    "binary": "ansible-playbook",
                    "default_playbook": "site.yml",
                    "default_inventory": "hosts.ini",
                    "default_extra_vars": {},
                    "working_dir": str(tmp_path),
                },
                "logging": {
                    "level": "INFO",
                    "file": "logs/ansible_runner.log",
                    "max_bytes": 10485760,
                    "backup_count": 5,
                },
                "runner": {
                    "timeout_seconds": 3600,
                    "enable_async": False,
                },
            }
        )
    )

    config = load_config(str(cfg_file))
    assert config.ansible.default_inventory == "hosts.ini"
    assert config.ansible.default_playbook == "site.yml"
    assert config.ansible.working_dir == str(tmp_path)


def test_missing_required_field(tmp_path):
    cfg_file = tmp_path / "bad.yaml"
    cfg_file.write_text(yaml.safe_dump({"inventory": "hosts.ini"}))

    with pytest.raises(ConfigValidationError):
        load_config(str(cfg_file))


def test_invalid_yaml(tmp_path):
    cfg_file = tmp_path / "bad.yaml"
    cfg_file.write_text(":::not-valid-yaml:::")
    with pytest.raises(ConfigValidationError):
        load_config(str(cfg_file))
