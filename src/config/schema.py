"""
Configuration Schema Definitions

Defines the Pydantic schema used to validate and structure values loaded from settings.yaml.

Contents:
  - SSHConfig: SSH-specific parameters.
  - AppConfig: Root container for application settings.

Dependencies:
  - pydantic

Notes:
  - This schema ensures type safety and required fields.
  - Used by config.py to construct validated settings from YAML input.
"""

from pydantic import BaseModel, Field


class SSHConfig(BaseModel):
    """
    Schema for SSH-related configuration settings.

    Attributes:
      timeout (int): SSH connection timeout in seconds.
      command (str): Command to run on the remote device.
    """

    timeout: int = Field(default=10, description="SSH connection timeout in seconds")
    command: str = Field(
        default="show running-config", description="Command to run on remote host"
    )


class AppConfig(BaseModel):
    """
    Root schema for all application-level configuration.

    Attributes:
      env (str): Runtime environment (e.g., dev, prod).
      output_dir (str): Directory to save collected .cfg files.
      ssh (SSHConfig): Nested SSH configuration block.
    """

    env: str = Field(default="dev", description="Application environment")
    output_dir: str = Field(
        default="configs", description="Directory to save .cfg files"
    )
    ssh: SSHConfig = Field(..., description="SSH connection config block")
