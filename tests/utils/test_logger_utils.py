"""
Tests for logger_utils.

Covers:
  - get_logger returns a Logger instance
  - Logger has stream and file handlers attached
  - Logger does not duplicate handlers on repeated calls
"""

import logging

from src.utils.logger_utils import get_logger


def test_get_logger_returns_logger_instance() -> None:
    """
    Verifies that get_logger returns a logging.Logger object.
    """
    logger = get_logger("test_logger")
    assert isinstance(logger, logging.Logger)


def test_get_logger_has_expected_handlers() -> None:
    """
    Verifies that returned logger has both stream and file handlers attached once.
    """
    logger_name = "handler_logger"

    # Clear any existing handlers for test safety
    existing_logger = logging.getLogger(logger_name)
    existing_logger.handlers.clear()

    logger = get_logger(logger_name)

    handler_types = [type(h).__name__ for h in logger.handlers]
    assert "StreamHandler" in handler_types
    assert any("RotatingFileHandler" in h for h in handler_types)


def test_get_logger_idempotent() -> None:
    """
    Ensures get_logger does not attach duplicate handlers on repeated calls.
    """
    logger1 = get_logger("repeat_logger")
    initial_handler_count = len(logger1.handlers)

    logger2 = get_logger("repeat_logger")
    assert logger1 is logger2
    assert len(logger2.handlers) == initial_handler_count
