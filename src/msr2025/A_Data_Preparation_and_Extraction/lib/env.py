"""
Utility module for retrieving Neo4j connection credentials from environment variables.

This module provides a function `get_neo4j_envs` that loads the Neo4j URI,
username, and password from a .env file using `getenv`.
"""

from ...lib.envs import getenv


def get_neo4j_envs() -> tuple[str, str, str]:
    """
    Retrieve Neo4j connection credentials from environment variables.

    Loads the values of `NEO4J_URI`, `NEO4J_USERNAME`, and `NEO4J_PASSWORD`
    from a .env file using the `getenv` function. If any of the variables
    are not found, a KeyError is raised.

    Returns:
        Tuple[str, str, str]: A tuple containing the URI, username, and password,
        in that order.

    Raises:
        KeyError: If any of the required environment variables are missing.

    """
    uri = getenv("NEO4J_URI")
    username = getenv("NEO4J_USERNAME")
    password = getenv("NEO4J_PASSWORD")
    return uri, username, password
