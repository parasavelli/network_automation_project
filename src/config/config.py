"""
Configuration Loader

Loads structured settings from `settings.yaml` using Pydantic for schema validation.

Contents:
  - load_config(): Loads, parses, and validates the application configuration.

Dependencies:
  - yaml
  - pathlib
  - pydantic
  - src.config.schema.AppConfig

Notes:
  - YAML config is validated against AppConfig schema.
  - Secrets like SSH credentials must go in .env, not YAML.
  - Called at runtime by orchestrator and CLI entrypoints.
"""

from pathlib import Path

import yaml

from src.config.schema import AppConfig


def load_config(config_path: str = "src/config/settings.yaml") -> AppConfig:
    """
    Loads and validates the YAML application configuration using Pydantic.

    Args:
      config_path (str): Path to the YAML config file (default: src/config/settings.yaml).

    Returns:
      AppConfig: Validated configuration object.

    Raises:
      FileNotFoundError: If the file does not exist.
      yaml.YAMLError: If the file cannot be parsed.
      ValidationError: If schema validation fails.

    Notes:
      - Config schema is defined in src/config/schema.py
      - Always use yaml.safe_load() for security.
    """
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with config_file.open("r") as f:
        raw = yaml.safe_load(f)

    return AppConfig(**raw)
