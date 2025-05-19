"""
Device Model

Defines structured device metadata using Pydantic for validation and typing.

Contents:
  - Device: Represents a device with hostname and optional metadata fields.

Dependencies:
  - pydantic.BaseModel
  - typing.Optional

Notes:
  - Used to parse and validate devices listed in devices.yaml.
  - Supports future extensions like group, region, or credentials.
"""

from typing import Optional

from pydantic import BaseModel


class Device(BaseModel):
    """
    Represents a single device entry from the input YAML.

    Args:
      hostname (str): Device hostname (required).
      ip (Optional[str]): IP address of the device (optional).
      location (Optional[str]): Location, region, or datacenter (optional).
      type (Optional[str]): Device type such as router, switch, firewall (optional).
    """

    hostname: str
    ip: Optional[str] = None
    location: Optional[str] = None
    type: Optional[str] = None
