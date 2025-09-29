"""
Purpose: Core class to run Ansible playbooks with sync/async & dry-run support.
"""

from __future__ import annotations
import asyncio
import json
import logging
import subprocess
from pathlib import Path
from typing import Optional

# NOTE: Assuming core imports are correctly aliased or fixed in your local setup
# based on the package name `ansible_runner`
from ansible_runner.utils import ensure_file_readable, safe_join
from ansible_runner.exceptions import ProcessExecutionError

logger = logging.getLogger(__name__)


class AnsibleRunner:
    """
    Run Ansible playbooks with support for sync, async, and dry-run.

    Now Accepts 'ansible_binary' from configuration.
    """

    # Accept ansible_binary in __init__
    def __init__(self, working_dir: Path, ansible_binary: str = "ansible-playbook"):
        self.working_dir = working_dir
        self.ansible_binary = ansible_binary  # Stored from config


    def _build_command(
        self,
        playbook: str,
        inventory: Optional[str] = None,
        extra_vars: Optional[dict] = None,
        dry_run: bool = False,
    ) -> list[str]:
        """
        Build ansible-playbook command safely.
        """
        playbook_path = ensure_file_readable(safe_join(str(self.working_dir), playbook))

        # Use the configured binary (self.ansible_binary) 
        cmd = [self.ansible_binary, str(playbook_path)]

        if inventory:
            inv_path = ensure_file_readable(safe_join(str(self.working_dir), inventory))
            cmd.extend(["-i", str(inv_path)])

        if extra_vars:
            # Note: Ensure extra_vars passed to json.dumps is not None
            vars_json = json.dumps(extra_vars) if extra_vars else "{}"
            cmd.extend(["--extra-vars", vars_json])

        if dry_run:
            cmd.append("--check")

        return cmd

    def run_playbook( 
        self,
        playbook: str,
        inventory: Optional[str] = None,
        extra_vars: Optional[dict] = None,
        dry_run: bool = False,
    ) -> int:
        """
        Run playbook synchronously with real-time output.
        Raises ProcessExecutionError if return code != 0.
        """
        cmd = self._build_command(playbook, inventory, extra_vars, dry_run)
        cmd_str = " ".join(cmd)
        logger.info("Executing: %s", cmd_str)

        # Use subprocess.Popen for live streaming output (professional standard)
        process = subprocess.Popen(
            cmd,
            cwd=self.working_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Stream live output
        if process.stdout:
            for line in process.stdout:  
                logger.info(line.strip())
        if process.stderr:
            for line in process.stderr:  
                logger.error(line.strip())

        process.wait()

        # Remove trailing whitespace line (flake8 W293)
        
        if process.returncode != 0:
            # Includes stdout/stderr in the exception for better debugging/testing
            raise ProcessExecutionError(
                process.returncode,
                stdout=" (Not captured here, streamed live)",
                stderr=" (Not captured here, streamed live)",
            )
        return process.returncode

    async def run_playbook_async(
        self,
        playbook: str,
        inventory: Optional[str] = None,
        extra_vars: Optional[dict] = None,
        dry_run: bool = False,
    ) -> int:
        """
        Run playbook asynchronously using asyncio.
        """
        cmd = self._build_command(playbook, inventory, extra_vars, dry_run)
        cmd_str = " ".join(cmd)
        logger.info("Executing async: %s", cmd_str)

        # Use asyncio for non-blocking execution
        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=self.working_dir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        # Stream async output
        # NOTE: Decoding is necessary here as asyncio process streams raw bytes
        if process.stdout:
            async for line in process.stdout:
                logger.info(line.decode().strip())
        if process.stderr:
            async for line in process.stderr:
                logger.error(line.decode().strip())
                
        rc = await process.wait()
        if rc != 0:
            # Don't have direct access to full captured stdout/stderr here
            raise ProcessExecutionError(rc)
        return rc
