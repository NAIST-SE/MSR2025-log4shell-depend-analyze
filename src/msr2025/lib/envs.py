"""
Utility to load environment variables from a .env file and retrieve a value by key.

Typical usage example:

    value = getenv("DATABASE_URL")
"""

import os

from dotenv import load_dotenv


def getenv(key: str) -> str:
    """
    Retrieve an environment variable from the .env file.

    This function loads environment variables using `python-dotenv` and
    retrieves the value associated with the specified key. If the key
    is not found, it raises a KeyError.

    Args:
        key (str): The name of the environment variable to retrieve.

    Returns:
        str: The value of the specified environment variable.

    Raises:
        KeyError: If the specified key is not found in the environment.

    """
    load_dotenv()
    value = os.getenv(key)

    if value is None:
        error_message = f"Environment variable '{key}' not found."
        raise KeyError(error_message)

    return value
