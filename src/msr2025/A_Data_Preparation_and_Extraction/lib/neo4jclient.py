"""src/msr2025/A_Data_Preparation_and_Extraction/lib/neo4jclient.py

Provides a Neo4jClient class for interacting with a Neo4j graph database.

This module defines a context-manager-enabled client class for running Cypher queries,
including support for building dynamic queries and exporting results to JSON.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, cast

from neo4j import GraphDatabase

from ...lib.files import save_json


class Neo4jClient:
    def __init__(self, uri: str, user: str, password: str) -> None:
        """Initialize the Neo4j client with connection credentials.

        Args:
           uri (str): The URI of the Neo4j database.
           user (str): Username for authentication.
           password (str): Password for authentication.

        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def __enter__(self) -> Neo4jClient:
        """Enter the runtime context for use with 'with' statements.

        Returns:
            Neo4jClient: The initialized client instance.

        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the runtime context and close the database connection."""
        self.close()

    def close(self) -> None:
        """Close the Neo4j database connection."""
        self.driver.close()

    def run_query(self, query) -> list[dict[str, Any]]:
        """Run a raw Cypher query and return the results.

        Args:
            query (str): The Cypher query string.

        Returns:
            List[Dict[str, Any]]: List of result records.

        """
        with self.driver.session() as session:
            result = session.run(query)
            return cast(list[dict[str, Any]], [record for record in result])

    def run_query_with_clauses(
        self,
        clause_match: str | None = None,
        clause_where: str | None = None,
        clause_set: str | None = None,
        clause_create: str | None = None,
        clause_return: str | None = None,
    ) -> list[dict[str, Any]]:
        """Construct and run a Cypher query from individual clauses.

        Any clause (MATCH, WHERE, SET, CREATE, RETURN) can be optionally provided.
        The query will be dynamically built and executed.

        Args:
            clause_match (Optional[str]): MATCH clause.
            clause_where (Optional[str]): WHERE clause.
            clause_set (Optional[str]): SET clause.
            clause_create (Optional[str]): CREATE clause.
            clause_return (Optional[str]): RETURN clause.

        Returns:
            List[Dict[str, Any]]: List of result records.

        """
        queries: dict[str, str | None] = {
            "MATCH": clause_match,
            "WHERE": clause_where,
            "SET": clause_set,
            "CREATE": clause_create,
            "RETURN": clause_return,
        }

        query: str = " ".join(f"{k} {v}" for k, v in queries.items() if v is not None)
        return self.run_query(query)

    def extract_data(self, query: str, path: Path) -> None:
        """Run a query and export the results to a JSON file.

        Args:
            query (str): The Cypher query to run.
            path (Path): Path to save the resulting JSON file.

        """
        result = self.run_query(query)
        save_json(cast(dict, [record for record in result]), path)
