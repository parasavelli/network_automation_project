"""
Tests for env_utils.

Covers:
  - get_env_var returns value when set
  - get_env_var raises error if required var is missing
"""

import pytest

from src.utils.env_utils import get_env_var


def test_get_env_var_returns_value_if_present(monkeypatch) -> None:
    """
    Ensures get_env_var returns the correct value when the variable is set.
    """
    monkeypatch.setenv("TEST_KEY", "test-value")
    result = get_env_var("TEST_KEY")
    assert result == "test-value"


def test_get_env_var_raises_if_required_missing(monkeypatch) -> None:
    """
    Ensures get_env_var raises EnvironmentError if required variable is missing.
    """
    monkeypatch.delenv("MISSING_KEY", raising=False)
    with pytest.raises(EnvironmentError):
        get_env_var("MISSING_KEY", required=True)
