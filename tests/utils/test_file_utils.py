"""
Tests for file_utils.

Covers:
  - Successful config file creation
  - File content correctness
"""

from src.utils.file_utils import write_config_to_file


def test_write_config_creates_expected_file(tmp_path) -> None:
    """
    Verifies that write_config_to_file creates a correctly named .cfg file with the given content.
    """
    output_dir = tmp_path / "output"
    device_name = "test-device"
    content = "sample-config"
    date = "20250518"

    write_config_to_file(device_name, content, date, output_dir=str(output_dir))

    expected_file = output_dir / f"{device_name}_{date}.cfg"

    assert expected_file.exists()
    assert expected_file.read_text() == content
