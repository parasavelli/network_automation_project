"""
SSH Collector Service

Responsible for orchestrating SSH collection jobs across a list of devices.

Contents:
  - collect_device_configs(): Loads devices, connects, collects, saves configs
  - run_diagnostics(): Validates environment, config, and input YAML

Dependencies:
  - src.utils.logger_utils
  - src.utils.file_utils
  - src.utils.ssh_utils
  - src.utils.device_loader
  - src.config.config

Notes:
  - Uses dry-run, config-based output path, and retry-safe SSH.
  - Skips unreachable devices gracefully; logs summary at end.
"""

import getpass
import platform
import socket
from datetime import datetime, timezone
from pathlib import Path

from src.config.config import load_config
from src.utils.device_loader import load_device_list
from src.utils.env_utils import get_env_var
from src.utils.file_utils import write_config_to_file
from src.utils.logger_utils import get_logger
from src.utils.ssh_utils import fetch_running_config

logger = get_logger(__name__)


def collect_device_configs(devices_file_path: str, dry_run: bool = False) -> None:
    """
    Connects to devices via SSH and writes their running configs to .cfg files.

    Args:
      devices_file_path (str): Path to a YAML file with device metadata list.
      dry_run (bool): If True, skips actual SSH and file output.

    Returns:
      None

    Raises:
      FileNotFoundError: If the input YAML file is missing or malformed.

    Notes:
      - Output files are named <hostname>_<YYYYMMDD>.cfg
      - A full summary is logged at the end of the run.
    """
    logger.info("=== Job Metadata ===")
    logger.info(f"User: {getpass.getuser()}")
    logger.info(f"Host: {platform.node()}")
    logger.info(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")

    date_stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    config = load_config()
    output_dir = config.output_dir
    devices = load_device_list(devices_file_path)

    success_count = 0
    failure_count = 0
    skipped_count = 0

    for device in devices:
        hostname = device.hostname

        if dry_run:
            logger.info(
                f"[DRY-RUN] Would connect to {hostname} ({device.ip or 'no IP'})"
            )
            logger.info(
                f"[DRY-RUN] Would write config to {output_dir}/{hostname}_{date_stamp}.cfg"
            )
            skipped_count += 1
            continue

        try:
            logger.info(f"Connecting to {hostname}...")
            config_text = fetch_running_config(hostname)
            write_config_to_file(hostname, config_text, date_stamp, output_dir)
            logger.info(f"✅ Config saved for {hostname}")
            success_count += 1
        except Exception as exc:
            logger.exception(f"❌ Failed to fetch config from {hostname}: {exc}")
            failure_count += 1

    logger.info("=== SSH Collection Summary ===")
    logger.info(f"Total devices: {len(devices)}")
    logger.info(f"Successes:     {success_count}")
    logger.info(f"Failures:      {failure_count}")
    logger.info(f"Dry-run/skips: {skipped_count}")


def run_diagnostics(devices_file: str) -> None:
    """
    Performs diagnostics for environment, config, device file, and network reachability.

    Args:
      devices_file (str): Path to devices.yaml

    Returns:
      None
    """
    logger.info("=== Running Diagnostics ===")

    try:
        username = get_env_var("SSH_USERNAME", required=True)
        password = get_env_var("SSH_PASSWORD", required=True)
        logger.info(f"✅ .env loaded. SSH_USERNAME: {username}")
    except Exception as e:
        logger.error(f"❌ .env check failed: {e}")

    try:
        config = load_config()
        logger.info(f"✅ settings.yaml loaded. Output dir: {config.output_dir}")
    except Exception as e:
        logger.error(f"❌ settings.yaml check failed: {e}")
        return

    try:
        devices = load_device_list(devices_file)
        logger.info(f"✅ Loaded {len(devices)} device(s) from devices.yaml")
    except Exception as e:
        logger.error(f"❌ devices.yaml check failed: {e}")
        return

    # Output path write check
    output_path = Path(config.output_dir)
    try:
        output_path.mkdir(exist_ok=True, parents=True)
        test_file = output_path / ".write_test"
        test_file.write_text("test")
        test_file.unlink()
        logger.info(f"✅ Output directory is writable: {output_path}")
    except Exception as e:
        logger.error(f"❌ Output directory write check failed: {e}")

    # DNS resolution test
    for device in devices:
        try:
            socket.gethostbyname(device.hostname)
            logger.info(f"✅ {device.hostname} resolves")
        except Exception:
            logger.warning(f"⚠️  DNS resolution failed for: {device.hostname}")

    logger.info("=== Diagnostics Complete ===")
