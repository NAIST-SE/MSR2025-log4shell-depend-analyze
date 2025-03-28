import os

from dotenv import load_dotenv


def get_env(key: str) -> str:
    load_dotenv()
    value = os.getenv(key)

    if value is None:
        raise KeyError

    return value
