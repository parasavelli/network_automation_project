"""
Tests for configuration loader and schema validation.

Covers:
  - Successful loading of valid settings.yaml
  - Handling of missing file errors
  - Optional: malformed YAML or schema mismatch
"""

import pytest

from src.config.config import load_config
from src.config.schema import AppConfig


def test_load_config_success(tmp_path) -> None:
    """
    Tests that load_config correctly parses a valid YAML config file.
    """
    config_file = tmp_path / "settings.yaml"
    config_file.write_text(
        """
env: test
output_dir: /tmp/configs
ssh:
  timeout: 5
  command: echo config
"""
    )

    config = load_config(config_path=str(config_file))
    assert isinstance(config, AppConfig)
    assert config.env == "test"
    assert config.output_dir == "/tmp/configs"
    assert config.ssh.timeout == 5
    assert config.ssh.command == "echo config"


def test_load_config_file_not_found(tmp_path) -> None:
    """
    Tests that load_config raises FileNotFoundError for a missing config file.
    """
    nonexistent_path = tmp_path / "nonexistent.yaml"
    with pytest.raises(FileNotFoundError):
        load_config(config_path=str(nonexistent_path))


def test_load_config_schema_validation_error(tmp_path) -> None:
    """
    Tests that load_config raises a validation error for invalid schema structure.
    """
    invalid_config = tmp_path / "invalid.yaml"
    invalid_config.write_text("not_a_dict: true")

    with pytest.raises(Exception):  # Pydantic validation error is fine here
        load_config(config_path=str(invalid_config))
