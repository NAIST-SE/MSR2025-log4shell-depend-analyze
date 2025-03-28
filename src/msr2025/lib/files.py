"""
src/msr2025/lib/files.py

Provides utility functions for file operations such as saving data in JSON format.
"""

import json
import os
from pathlib import Path


def save_json(data, path: Path) -> None:
    """
    Save data to a file in JSON format.

    This function creates any necessary parent directories, and then writes the given
    data to the specified path in JSON format with an indentation of 2 spaces.

    Args:
        data: The data to be serialized and saved as JSON.
        path (Path): The destination file path where the JSON will be saved.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
