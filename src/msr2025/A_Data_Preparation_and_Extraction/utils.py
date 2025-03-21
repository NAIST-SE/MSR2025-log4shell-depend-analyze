import os
from typing import Optional
from urllib.parse import urljoin
import requests
from dotenv import load_dotenv
from requests import Response
import itertools
import threading
import time
import sys


load_dotenv()

def call_api(path: str, params: dict) -> dict:
    base_url = os.getenv('WEAVER_REST_API_BASE_URL')
    if not base_url:
        raise ValueError("Environment variable 'WEAVER_REST_API_BASE_URL' is not set")

    url: str = urljoin(base_url.rstrip('/') + '/', path.lstrip('/'))

    response: Response = requests.post(url, json=params)
    response.raise_for_status()

    return response.json()


def run_cypher(
        clause_match: Optional[str] = None,
        clause_where: Optional[str] = None,
        clause_set: Optional[str] = None,
        clause_create: Optional[str] = None,
        clause_return: Optional[str] = None,
) -> dict:

    queries: dict[str, Optional[str]] = {
        'MATCH': clause_match,
        'WHERE': clause_where,
        'SET': clause_set,
        'CREATE': clause_create,
        'RETURN': clause_return,
    }

    query: str = " ".join(f"{k} {v}" for k, v in queries.items() if v is not None)

    return call_api(path='/cypher', params={
        'query': query,
        'addedValues': []
    })


def spinner(label: str, done_event: threading.Event):
    spinner_cycle = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
    while not done_event.is_set():
        spin_char = next(spinner_cycle)
        sys.stdout.write(f"\r{spin_char} Running : {label}   ")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write(f"\r✔ Done    : {label}   \n")
    sys.stdout.flush()

def run_task(label: str, task):
    done_event = threading.Event()
    spinner_thread = threading.Thread(target=spinner, args=(label, done_event))
    spinner_thread.start()

    try:
        task()
    finally:
        done_event.set()
        spinner_thread.join()