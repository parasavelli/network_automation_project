"""
SSH Utility

Encapsulates SSH connection logic using `paramiko`.

Contents:
  - fetch_running_config(): Connects to device and retrieves config.

Dependencies:
  - paramiko
  - tenacity
  - src.utils.env_utils

Notes:
  - Assumes username/password are provided via environment variables.
  - Uses exponential backoff with retry (3 attempts).
  - Errors are re-raised for service-level handling.
"""

import paramiko
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from src.utils.env_utils import get_env_var


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((paramiko.SSHException, OSError)),
    reraise=True,
)
def fetch_running_config(hostname: str) -> str:
    """
    Connects to a device via SSH and returns the running configuration.

    Args:
      hostname (str): Target device hostname or IP address.

    Returns:
      str: Raw config output from the device.

    Raises:
      paramiko.SSHException: On connection/authentication failure.
      IOError: On command execution failure or read error.

    Notes:
      - Uses retry with exponential backoff for network resilience.
      - Environment variables SSH_USERNAME and SSH_PASSWORD must be defined.
    """
    username = get_env_var("SSH_USERNAME", required=True)
    password = get_env_var("SSH_PASSWORD", required=True)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname, username=username, password=password, timeout=10)
        _, stdout, _ = client.exec_command("show running-config")
        return stdout.read().decode()
    finally:
        client.close()
