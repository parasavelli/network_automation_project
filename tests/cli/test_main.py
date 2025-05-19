"""
Tests for CLI argument parsing and main function dispatch.

Covers:
  - Validates correct parsing of --devices-file
  - Verifies main() dispatches to service layer
"""

from argparse import Namespace
from unittest.mock import patch

from src.cli.main import main, parse_args


def test_parse_args_with_devices_file(monkeypatch) -> None:
    """
    Tests that CLI parser returns expected namespace when --devices-file is passed.
    """
    monkeypatch.setattr("sys.argv", ["prog", "--devices-file", "devices.yaml"])
    args = parse_args()
    assert isinstance(args, Namespace)
    assert args.devices_file == "devices.yaml"


@patch("src.cli.main.collect_device_configs")
def test_main_calls_collect_device_configs(mock_collect, monkeypatch) -> None:
    """
    Tests that main() dispatches to collect_device_configs when --diagnose is not used.
    """
    monkeypatch.setattr("sys.argv", ["prog", "--devices-file", "devices.yaml"])
    main()
    mock_collect.assert_called_once_with(
        devices_file_path="devices.yaml", dry_run=False
    )


@patch("src.cli.main.run_diagnostics")
def test_main_calls_diagnostics_when_flag_set(mock_diag, monkeypatch) -> None:
    """
    Tests that main() calls run_diagnostics() when --diagnose is used.
    """
    monkeypatch.setattr(
        "sys.argv", ["prog", "--devices-file", "devices.yaml", "--diagnose"]
    )
    main()
    mock_diag.assert_called_once_with(devices_file="devices.yaml")
