# Ansible Script Runner (Enterprise-grade)

**Author:** Didarul Islam
**Python Version:** 3.13.3
**License:** MIT

---

## Overview

This project is a **professional-grade Ansible Script Runner** designed for **enterprise-ready automation**. It demonstrates modern Python best practices including async support, configuration validation, modular design, logging, and comprehensive unit testing.

Key highlights:

* Sync & async playbook execution
* Dry-run mode for safe testing
* Rotating logs with professional formatting
* CLI support with flexible options
* Config validation using **Pydantic v2**
* Comprehensive unit tests using `pytest` and `unittest.mock`
* Recruiter-ready modular project structure

---

## Features

* **Playbook Execution**: Run Ansible playbooks in both sync and async modes.
* **Dry-run mode**: Simulate execution without making actual changes.
* **Logging**: Rotating, configurable logs with console output.
* **CLI Support**: Send commands with extra-vars, inventory, and dry-run options.
* **Validation**: Pydantic v2 ensures config files are correct.
* **Unit Tested**: Safely refactor without breaking functionality.
* **Extensible Design**: Add new helpers or custom execution logic easily.

---

## Folder Structure

```text
ansible_script_runner/
├── config/
│   └── config.yaml                     # Main configuration for runner (inventory, playbook path, defaults)
│
├── ansible_runner/
│   ├── __init__.py                     # Package marker, version
│   ├── cli.py                          # CLI argument parsing (argparse, epilog)
│   ├── logger.py                       # Rotating logger setup (uses logger.hasHandlers guard)
│   ├── config_loader.py                # Load + validate config via Pydantic v2
│   ├── utils.py                        # Helper functions (file handling, path validation, safe join)
│   ├── runner.py                       # Core Ansible runner (sync & async, subprocess wrapper)
│   └── exceptions.py                   # Custom exceptions for clearer testing/handling
│
├── tests/
│   ├── test__init__.py                 # Marks tests folder as Python package
│   ├── test_runner.py                  # Unit tests for runner.py using pytest + unittest.mock
│   ├── test_utils.py                   # Unit tests for utils.py
│   ├── test_ansible_runner.py          # Integration-like tests for runner
│   ├── test_logger.py                  # Logger unit tests
│   ├── test_cli.py                     # CLI parser unit tests
│   └── test_config_loader.py           # Config loader unit tests
│
├── .pre-commit-config.yaml             # Pre-commit hooks for code quality (black, ruff, mypy)
├── .gitignore                           # Ignored files for Git
├── LICENSE                              # MIT License file
├── requirements-dev.txt                 # Development & testing dependencies
├── README.md                             # Project documentation
├── requirements.txt                      # Production dependencies
└── main.py                               # Entry point calling CLI and main execution
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/ansible-script-runner.git
cd ansible-script-runner
```

Create and activate Python virtual environment:

```bash
python3.13 -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Update `config/config.yaml` with your inventory, playbook paths, defaults, and other settings.

---

## Usage

### Run Playbook via CLI

Basic usage:

```bash
python main.py --playbook playbooks/site.yml --inventory inventory/hosts.ini
```

Dry-run mode (simulate execution without changes):

```bash
python main.py --playbook playbooks/site.yml --dry-run
```

Use extra-vars:

```bash
python main.py --playbook playbooks/site.yml --extra-vars '{"var1":"value1"}'
```

Enable verbose logging:

```bash
python main.py --verbose --playbook playbooks/site.yml
```

---

## Configuration

The runner uses a **YAML configuration file** (`config.yaml`) structured as:

```yaml
inventory: inventory/hosts.ini
playbook: playbooks/site.yml
working_dir: /absolute/path/to/workdir
extra_vars: {}
dry_run: false
logging:
  level: INFO
  log_file: logs/ansible_runner.log
  max_bytes: 5242880
  backup_count: 5
```

---

## Testing

Run all unit tests:

```bash
pytest tests/ -v
```

Tests cover:

* Playbook execution (sync, async, dry-run)
* CLI parsing
* Config loading and validation
* Logger creation
* Utility functions

---

## Logging

* Rotating log files with configurable levels
* Console output for quick debugging
* Supports debug, info, warning, and error levels

---

## Development

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

Pre-commit hooks ensure code quality:

```bash
pre-commit install
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to branch (`git push origin feature/my-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

⚠️ Note: Do not commit secrets or sensitive paths. Use `.gitignore` to keep them safe.

![Python](https://img.shields.io/badge/python-3.13-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)

---

## Notes

* Always test with dry-run mode before production execution.
* Keep inventory and playbook paths secure.
* Python 3.13.3 is required.
* Designed for professional, enterprise-ready Python automation.
* Modular and extensible: easily add new helpers or runners.
