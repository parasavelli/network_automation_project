"""
File Output Utility

Handles writing configuration data to `.cfg` files using a standardized naming format.

Contents:
  - write_config_to_file(): Writes raw config data to a timestamped .cfg file.

Dependencies:
  - pathlib

Notes:
  - Files are saved in <output_dir>/<hostname>_<YYYYMMDD>.cfg format.
  - Output directory is created if it does not exist.
  - Filename is sanitized only at higher levels (assumes valid hostnames here).

Warnings:
  - If output_dir is not writable, this will raise an OSError.
  - Config data is written as-is — no filtering or parsing is performed.
"""

from pathlib import Path


def write_config_to_file(
    hostname: str, config_data: str, date_stamp: str, output_dir: str
) -> None:
    """
    Writes a raw device config string to a local `.cfg` file using the hostname and date stamp.

    Args:
      hostname (str): Device hostname to be used in the output filename.
      config_data (str): Raw configuration text to write.
      date_stamp (str): Timestamp (YYYYMMDD) used in the filename.
      output_dir (str): Destination directory for writing the config file.

    Returns:
      None

    Raises:
      OSError: If directory creation or file writing fails.

    Notes:
      - Example output filename: `router1_20250518.cfg`
      - Caller is responsible for ensuring unique hostnames to avoid overwrite.
    """
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    file_path = out_path / f"{hostname}_{date_stamp}.cfg"
    file_path.write_text(config_data)
