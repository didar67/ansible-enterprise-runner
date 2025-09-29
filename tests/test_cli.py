"""
Tests for CLI argument parsing in cli.py
"""

import sys
import pytest
from ansible_runner.cli import parse_args


def test_cli_required_args(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ["script", "--config", "config.yaml", "--playbook", "playbook.yml", "--inventory", "hosts.ini"])
    args = parse_args()
    assert args.config == "config.yaml"
    assert args.playbook == "playbook.yml"
    assert args.inventory == "hosts.ini"
    assert args.dry_run is False


def test_cli_with_dry_run(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ["script", "--config", "config.yaml", "--playbook", "pb.yml", "--inventory", "inv.ini", "--dry-run"])
    args = parse_args()
    assert args.dry_run is True


def test_cli_with_extra_vars_json(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ["script", "--config", "config.yaml", "--playbook", "pb.yml", "--inventory", "inv.ini", "--extra-vars", '{"key":"value"}'])
    args = parse_args()
    # CLI parser returns a list of strings
    assert isinstance(args.extra_vars, list)
    assert args.extra_vars[0] == '{"key":"value"}'


def test_cli_with_extra_vars_keyvalue(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ["script", "--config", "config.yaml", "--playbook", "pb.yml", "--inventory", "inv.ini", "--extra-vars", "a=1", "b=2"])
    args = parse_args()
    # CLI parser returns a list of strings
    assert isinstance(args.extra_vars, list)
    assert "a=1" in args.extra_vars
    assert "b=2" in args.extra_vars


def test_cli_invalid_extra_vars(monkeypatch):
    # The CLI parser itself doesn't validate JSON - that's done in main.py
    # So this test should just check that the args are parsed correctly
    monkeypatch.setattr(sys, 'argv', ["script", "--config", "config.yaml", "--playbook", "pb.yml", "--inventory", "inv.ini", "--extra-vars", "{not-valid-json"])
    args = parse_args()
    assert isinstance(args.extra_vars, list)
    assert args.extra_vars[0] == "{not-valid-json"
