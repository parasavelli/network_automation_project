"""
CLI Entrypoint Module

Parses command-line arguments and triggers either diagnostics or SSH config collection.
Supports dry-run mode and YAML-based device input.

Contents:
  - parse_args(): Parses CLI arguments into a structured namespace.
  - main(): CLI dispatcher that invokes service logic.

Dependencies:
  - argparse
  - src.services.ssh_collector.collect_device_configs
  - src.services.ssh_collector.run_diagnostics

Notes:
  - Use --devices-file to provide the input device list (YAML format).
  - Use --diagnose to run validation checks without making SSH connections.
"""

import argparse

from src.services.ssh_collector import collect_device_configs, run_diagnostics


def parse_args() -> argparse.Namespace:
    """
    Parses command-line arguments and returns the parsed namespace.

    Returns:
      argparse.Namespace: Parsed arguments including flags and paths.
    """
    parser = argparse.ArgumentParser(description="SSH Config Collector CLI")

    parser.add_argument(
        "--devices-file",
        required=True,
        help="Path to the YAML file containing the list of devices",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the run without performing SSH or writing configs",
    )
    parser.add_argument(
        "--diagnose",
        action="store_true",
        help="Validate environment, config, and device file (no SSH execution)",
    )

    return parser.parse_args()


def main() -> None:
    """
    Main CLI dispatcher that invokes diagnostics or config collection based on arguments.
    """
    args = parse_args()

    if args.diagnose:
        run_diagnostics(devices_file=args.devices_file)
    else:
        collect_device_configs(
            devices_file_path=args.devices_file, dry_run=args.dry_run
        )


if __name__ == "__main__":
    main()
