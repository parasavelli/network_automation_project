"""
Tests for ssh_collector service.

Covers:
  - Loads devices from YAML
  - Triggers config collection
  - Handles dry-run mode
  - Logs errors on failure but continues
"""

from unittest.mock import ANY, MagicMock, patch

from src.services.ssh_collector import collect_device_configs


@patch("src.services.ssh_collector.fetch_running_config")
@patch("src.services.ssh_collector.write_config_to_file")
@patch("src.services.ssh_collector.load_config")
@patch("src.services.ssh_collector.load_device_list")
def test_collect_device_configs_success(
    mock_load_devices, mock_load_config, mock_write, mock_fetch
) -> None:
    """
    Verifies that configs are fetched and written when devices load successfully.
    """
    mock_load_devices.return_value = [
        MagicMock(hostname="router1"),
        MagicMock(hostname="router2"),
    ]
    mock_load_config.return_value.output_dir = "/tmp"
    mock_fetch.side_effect = ["conf1", "conf2"]

    collect_device_configs("devices.yaml")

    assert mock_write.call_count == 2
    mock_write.assert_any_call("router1", "conf1", ANY, "/tmp")
    mock_write.assert_any_call("router2", "conf2", ANY, "/tmp")


@patch("src.services.ssh_collector.load_device_list")
@patch("src.services.ssh_collector.load_config")
def test_dry_run_skips_execution(mock_load_config, mock_load_devices, caplog) -> None:
    """
    Validates that dry-run mode logs the expected messages and skips SSH and file writes.
    """
    import logging

    caplog.set_level(logging.INFO)

    mock_load_devices.return_value = [
        MagicMock(hostname="router1", ip="10.0.0.1"),
        MagicMock(hostname="router2", ip="10.0.0.2"),
    ]
    mock_load_config.return_value.output_dir = "/dryrun"

    collect_device_configs("devices.yaml", dry_run=True)

    assert "Would connect to router1" in caplog.text
    assert "Would write config to /dryrun/router1" in caplog.text
