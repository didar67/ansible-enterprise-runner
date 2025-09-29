"""
Purpose: Single entrypoint — loads config, sets up logger, parses CLI, runs playbook.
"""

from __future__ import annotations

import asyncio
import logging
import sys
from pathlib import Path

# Using the correct package name for standard imports
from ansible_runner.config_loader import load_config, ConfigValidationError
from ansible_runner.runner import AnsibleRunner
from ansible_runner.logger import get_logger, INFO
from ansible_runner.cli import parse_args
from ansible_runner.exceptions import RunnerError, ProcessExecutionError


def setup_logging(logging_cfg):
    """Initializes the primary application logger based on configuration."""
    level = logging_cfg.level.upper()
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
    }

    # Initialize the main runner logger
    get_logger(
        name="ansible_runner",
        level=level_map.get(level, INFO),
        logfile=logging_cfg.file,
        max_bytes=logging_cfg.max_bytes,
        backup_count=logging_cfg.backup_count,
    )

    # Set root logger level as well
    logging.getLogger().setLevel(level_map.get(level, INFO))


def main() -> int:
    # Use a basic logger for CLI/Config errors before main logging is set up
    temp_logger = logging.getLogger("pre_config")
    temp_logger.setLevel(logging.INFO)
    if not temp_logger.hasHandlers():
        temp_logger.addHandler(logging.StreamHandler(sys.stdout))

    args = parse_args()

    try:
        # Load config and initialize logging
        cfg = load_config(args.config)
        setup_logging(cfg.logging)
        logger = logging.getLogger("ansible_runner")

        # Instantiate runner with working_dir AND configured binary 
        runner = AnsibleRunner(
            working_dir=Path(cfg.ansible.working_dir), ansible_binary=cfg.ansible.binary
        )

        # Implement configuration fallback logic
        # 1. Playbook/Inventory: Use CLI value, otherwise use config default
        playbook_to_run = (
            args.playbook if args.playbook else cfg.ansible.default_playbook
        )
        inventory_to_use = (
            args.inventory if args.inventory else cfg.ansible.default_inventory
        )

        # 2. Extra Vars: Start with config defaults, then override with CLI vars
        extra_vars = cfg.ansible.default_extra_vars.copy()

        # Parse extra_vars from CLI: support key=value pairs or JSON string
        if args.extra_vars:
            # If single JSON string, parse it
            if len(args.extra_vars) == 1 and args.extra_vars[0].startswith("{") and args.extra_vars[0].endswith("}"):
                import json

                try:
                    extra_vars.update(json.loads(args.extra_vars[0]))
                except json.JSONDecodeError:
                    logger.error("Invalid JSON format for --extra-vars")
                    return 1
            else:
                # Parse key=value pairs
                for kv in args.extra_vars:
                    if "=" not in kv:
                        logger.error(
                            "Invalid --extra-vars format. Use key=value (e.g., host=web01)"
                        )
                        return 1
                    k, v = kv.split("=", 1)
                    extra_vars[k] = v

        # 3. Dry Run/Async: CLI argument takes precedence over config setting
        dry_run_flag = args.dry_run
        use_async_flag = args.use_async or cfg.runner.enable_async

        if use_async_flag:
            return asyncio.run(
                runner.run_playbook_async(
                    playbook_to_run, inventory_to_use, extra_vars, dry_run_flag
                )
            )
        else:
            return runner.run_playbook(
                playbook_to_run, inventory_to_use, extra_vars, dry_run_flag
            )

    except (RunnerError, ConfigValidationError, ProcessExecutionError) as e:
        log = (
            logging.getLogger("ansible_runner") if "logger" in locals() else temp_logger
        )
        log.error("Execution failed: %s", e)
        return 1
    except Exception as e:
        log = (
            logging.getLogger("ansible_runner") if "logger" in locals() else temp_logger
        )
        log.exception("Unexpected error: %s", e)
        return 1


if __name__ == "__main__":
    # Ensure the current directory is in sys.path for package imports
    # This allows 'ansible_runner' package to be found when running 'python main.py'
    if str(Path(__file__).parent) not in sys.path:
        sys.path.insert(0, str(Path(__file__).parent))

    sys.exit(main())
