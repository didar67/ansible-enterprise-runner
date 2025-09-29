"""
Purpose: Handle only CLI argument parsing (no logging/config here).
"""

from __future__ import annotations
import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ansible Script Runner CLI (Enterprise Standard)",
        epilog=(
            "Example: python main.py --config config/config.yaml "
            "--playbook site.yml --inventory hosts.ini "
            "--extra-vars key1=val1 key2=val2 --dry-run"
        ),
    )

    # config remains required
    parser.add_argument("--config", required=True, help="Path to config.yaml")

    # Playbook/Inventory are now optional, allowing config fallbacks
    parser.add_argument(
        "--playbook", help="Playbook filename (optional, overrides config default)"
    )
    parser.add_argument(
        "--inventory", help="Inventory filename (optional, overrides config default)"
    )

    parser.add_argument(
        "--extra-vars",
        nargs="*",
        help="Extra vars as key=value pairs (space-separated)",
        default=[],
    )
    parser.add_argument(
        "--async", action="store_true", dest="use_async", help="Run asynchronously"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run playbook in dry-run (check) mode",
    )
    return parser.parse_args()
