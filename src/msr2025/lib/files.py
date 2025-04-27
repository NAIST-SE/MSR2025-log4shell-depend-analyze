"""Utility functions for file operations: saving and loading JSON data."""

import json
from pathlib import Path


def save_json(data: dict, path: Path) -> None:  # type: ignore[type-arg]
    """
    Save data to a file in JSON format.

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
        error_message = f"Failed to save JSON to '{path}': {e}"
        raise OSError(error_message) from e
    except TypeError as e:
        error_message = f"Data is not JSON serializable: {e}"
        raise TypeError(error_message) from e


def load_json(path: Path) -> dict:  # type: ignore[type-arg]
    """
    Load data from a JSON file.

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
        error_message = f"File not found: '{path}'"
        raise FileNotFoundError(error_message)

    with Path.open(path) as f:
        return json.load(f)  # type: ignore[no-any-return]
