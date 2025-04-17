"""src/msr2025/lib/files.py

Provides utility functions for file operations such as saving and loading JSON data.
"""

import json
from pathlib import Path


def save_json(data: dict, path: Path) -> None:
    """Save data to a file in JSON format.

    This function creates any necessary parent directories, and then writes the given
    data to the specified path in JSON format with an indentation of 2 spaces.

    Args:
        data (dict): The data to be serialized and saved as JSON.
        path (Path): The destination file path where the JSON will be saved.

    Raises:
        OSError: If the directory or file cannot be created or written.
        TypeError: If the data is not JSON serializable.

    """
    try:
        Path.mkdir(path.parent, parents=True, exist_ok=True)
        with Path.open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except OSError as e:
        raise OSError(f"Failed to save JSON to '{path}': {e}") from e
    except TypeError as e:
        raise TypeError(f"Data is not JSON serializable: {e}") from e


def load_json(path: Path) -> dict:
    """Load data from a JSON file.

    Reads the specified JSON file and returns the parsed Python object.

    Args:
        path (Path): The path to the JSON file to read.

    Returns:
        Any: The data parsed from the JSON file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If the file content is not valid JSON.

    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: '{path}'")

    with Path.open(path) as f:
        return json.load(f)
