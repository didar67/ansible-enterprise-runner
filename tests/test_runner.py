"""
Purpose: Unit tests for AnsibleRunner class.
Covers _build_command, run_playbook (sync), and run_playbook_async (async).
"""

import asyncio
import json
import pytest
from unittest.mock import patch, MagicMock

from ansible_runner.runner import AnsibleRunner


@pytest.fixture
def runner(tmp_path):
    return AnsibleRunner(working_dir=tmp_path)


def test_build_command_with_inventory_and_vars(runner, tmp_path):
    pb = tmp_path / "playbook.yml"
    inv = tmp_path / "hosts.ini"
    pb.write_text("fake playbook")
    inv.write_text("fake inventory")

    cmd = runner._build_command("playbook.yml", "hosts.ini", {"foo": "bar"})
    assert "ansible-playbook" in cmd[0]
    assert "--extra-vars" in cmd
    assert json.dumps({"foo": "bar"}) in cmd


def test_build_command_missing_file(runner):
    with pytest.raises(FileNotFoundError):
        runner._build_command("missing.yml")


@patch("subprocess.Popen")
def test_run_playbook_success(mock_popen, runner, tmp_path):
    pb = tmp_path / "playbook.yml"
    pb.write_text("fake playbook")

    mock_proc = MagicMock()
    mock_proc.stdout = None  # No stdout captured in live streaming
    mock_proc.stderr = None  # No stderr captured in live streaming
    mock_proc.returncode = 0
    mock_proc.wait.return_value = None
    mock_popen.return_value = mock_proc

    rc = runner.run_playbook("playbook.yml")
    assert rc == 0
    mock_popen.assert_called_once()


@patch("subprocess.Popen")
def test_run_playbook_failure(mock_popen, runner, tmp_path):
    pb = tmp_path / "playbook.yml"
    pb.write_text("fake playbook")

    mock_proc = MagicMock()
    mock_proc.stdout = None
    mock_proc.stderr = None
    mock_proc.returncode = 2
    mock_proc.wait.return_value = None
    mock_popen.return_value = mock_proc

    with pytest.raises(Exception):  # Should raise ProcessExecutionError
        runner.run_playbook("playbook.yml")


@pytest.mark.asyncio
@patch("asyncio.create_subprocess_exec")
async def test_run_playbook_async_success(mock_exec, runner, tmp_path):
    pb = tmp_path / "playbook.yml"
    pb.write_text("fake playbook")

    # Create async iterators for stdout and stderr
    async def async_stdout():
        yield b"hello\n"

    async def async_stderr():
        yield b""

    mock_proc = MagicMock()
    mock_proc.stdout = async_stdout()
    mock_proc.stderr = async_stderr()
    mock_proc.wait = MagicMock(return_value=asyncio.Future())
    mock_proc.wait.return_value.set_result(0)
    mock_exec.return_value = mock_proc

    rc = await runner.run_playbook_async("playbook.yml")
    assert rc == 0
