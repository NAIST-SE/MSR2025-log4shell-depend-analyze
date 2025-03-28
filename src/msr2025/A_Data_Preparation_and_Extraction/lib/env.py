import os
from typing import Optional, Tuple

from dotenv import load_dotenv


def get_neo4j_envs() -> Tuple[Optional[str], Optional[str], Optional[str]]:
    load_dotenv()
    uri = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")
    return uri, username, password
