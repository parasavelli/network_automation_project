"""
Tests for ssh_utils.

Covers:
  - fetch_running_config returns expected output when SSH succeeds
  - raises exception when connection fails
"""

from unittest.mock import MagicMock, patch

import paramiko
import pytest

from src.utils.ssh_utils import fetch_running_config


@patch("paramiko.SSHClient")
def test_fetch_running_config_success(mock_ssh_client, monkeypatch) -> None:
    """
    Verifies that fetch_running_config returns config output on successful SSH session.
    """
    monkeypatch.setenv("SSH_USERNAME", "admin")
    monkeypatch.setenv("SSH_PASSWORD", "secret")

    mock_client = MagicMock()
    mock_stdout = MagicMock()
    mock_stdout.read.return_value = b"config-output"

    mock_client.exec_command.return_value = (None, mock_stdout, None)
    mock_ssh_client.return_value = mock_client

    result = fetch_running_config("router1")

    assert result == "config-output"
    mock_client.connect.assert_called_once()
    mock_client.close.assert_called_once()


@patch("paramiko.SSHClient")
def test_fetch_running_config_raises_on_failure(mock_ssh_client, monkeypatch) -> None:
    """
    Ensures fetch_running_config raises an exception when SSH connection fails,
    and that retry logic attempts connection multiple times.
    """
    monkeypatch.setenv("SSH_USERNAME", "admin")
    monkeypatch.setenv("SSH_PASSWORD", "secret")

    mock_client = MagicMock()
    mock_client.connect.side_effect = paramiko.SSHException("connection failed")
    mock_ssh_client.return_value = mock_client

    with pytest.raises(paramiko.SSHException):
        fetch_running_config("unreachable-device")

    assert mock_client.connect.call_count == 3  # due to tenacity retry
    assert mock_client.close.call_count == 3  # each retry closes
