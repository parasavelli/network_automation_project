"""
Script Entry Point

Wraps the CLI dispatcher for standalone execution. Intended for use in cron jobs,
manual runs, or Docker-based invocations.

Example:
  python scripts/run_ssh_backup.py --devices-file=src/config/devices.yaml
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.cli.main import main

if __name__ == "__main__":
    main()
