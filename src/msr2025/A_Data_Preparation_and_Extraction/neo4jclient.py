from typing import List, Dict, Any, Optional

from neo4j import GraphDatabase
from .utils import save_json


class Neo4jClient:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def run_query(self, query) -> List[Dict[str, Any]]:
        with self.driver.session() as session:
            result = session.run(query)
            return [record for record in result]

    def run_query_with_clauses(
        self,
        clause_match: Optional[str] = None,
        clause_where: Optional[str] = None,
        clause_set: Optional[str] = None,
        clause_create: Optional[str] = None,
        clause_return: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        queries: Dict[str, Optional[str]] = {
            "MATCH": clause_match,
            "WHERE": clause_where,
            "SET": clause_set,
            "CREATE": clause_create,
            "RETURN": clause_return,
        }

        query: str = " ".join(f"{k} {v}" for k, v in queries.items() if v is not None)
        return self.run_query(query)

    def extract_data(self, query: str, path: str) -> None:
        result = self.run_query(query)
        save_json([record for record in result], path)
