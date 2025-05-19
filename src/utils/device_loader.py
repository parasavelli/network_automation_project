"""
Device Loader Utility

Parses a structured YAML file and returns a list of validated device objects.

Contents:
  - load_device_list(): Loads device list from a YAML file and returns validated Device models.

Dependencies:
  - yaml
  - pathlib
  - pydantic
  - src.models.device_model

Notes:
  - Device input format must be a top-level key: `devices: [ {hostname: ...}, ... ]`
  - YAML schema is validated against the Device model (Pydantic).
"""

from pathlib import Path
from typing import List

import yaml

from src.models.device_model import Device


def load_device_list(yaml_path: str) -> List[Device]:
    """
    Loads device metadata from a YAML file and parses it into Device models.

    Args:
      yaml_path (str): Path to the YAML file with a `devices:` top-level list.

    Returns:
      List[Device]: Validated list of Device objects.

    Raises:
      FileNotFoundError: If the YAML file does not exist.
      ValidationError: If any device entry fails validation.

    Notes:
      - The file must be structured as:
        devices:
          - hostname: router1
            ip: 10.0.0.1
            type: core
      - Skips empty list if `devices:` is missing, but will not raise.
    """
    file_path = Path(yaml_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Device list not found: {yaml_path}")

    with file_path.open("r") as f:
        raw = yaml.safe_load(f) or {}

    raw_devices = raw.get("devices", [])
    return [Device(**entry) for entry in raw_devices]
