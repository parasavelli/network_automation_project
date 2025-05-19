"""
Logging Utility

Initializes a standardized logger that outputs to both terminal and file.

Contents:
  - get_logger(): Returns a pre-configured logger instance.

Dependencies:
  - logging
  - pathlib

Notes:
  - Logs to terminal at INFO level and above.
  - Logs to file at DEBUG level and above (rotating).
  - File logs are stored under ./logs/network_automation.log
  - Uses RotatingFileHandler (max 1MB per file, 5 backups).
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def get_logger(name: str) -> logging.Logger:
    """
    Creates or retrieves a logger instance with dual output handlers:
    one for console and one for rotating log file.

    Args:
      name (str): Logger name, typically `__name__`

    Returns:
      logging.Logger: Configured logger instance with handlers attached

    Notes:
      - Terminal logs are shown at INFO level.
      - File logs capture full DEBUG+ level data.
      - Prevents duplicate handlers on re-import.
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Terminal stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    # Rotating file handler
    logs_dir = Path("logs")
    logs_dir.mkdir(parents=True, exist_ok=True)

    file_handler = RotatingFileHandler(
        logs_dir / "network_automation.log",
        maxBytes=1_048_576,  # 1MB
        backupCount=5,
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Register both handlers
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger
