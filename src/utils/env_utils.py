"""
Environment Utility

Handles resolution of environment variables using both `os.environ`
and `.env` via `python-dotenv`.

Contents:
  - get_env_var(): Loads environment variable with fallback, validation, and safety.

Dependencies:
  - os
  - dotenv (python-dotenv)

Notes:
  - Automatically loads `.env` from the project root using `load_dotenv()`.
  - Recommended for use in non-containerized or local development environments.
"""

import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


def get_env_var(
    name: str, default: Optional[str] = None, required: bool = False
) -> str:
    """
    Resolves and returns the value of an environment variable, with fallback and validation.

    Args:
      name (str): Environment variable key.
      default (Optional[str]): Fallback value if not found. Ignored if `required=True`.
      required (bool): If True, raise an error when variable is missing or empty.

    Returns:
      str: Final resolved value.

    Raises:
      EnvironmentError: If the variable is required and not found or empty.

    Notes:
      - Reads from `os.environ`, including values from a `.env` file (loaded at import).
      - Useful for secrets like SSH_USERNAME or API_KEY.
      - If both default and required=True are set, required takes precedence.
    """
    value = os.getenv(name, default)

    if required and not value:
        raise EnvironmentError(f"Missing required environment variable: {name}")

    return value
