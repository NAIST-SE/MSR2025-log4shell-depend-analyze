import json
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


def save_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f)


def save_result():
    query: str = "\
        MATCH (r:Release_depend_SemVer) \
        WITH \
          r, \
          split(r.version, ').') AS parts \
        WITH \
          r.artifactId AS artifactId, \
          r.version AS lv, \
          r.timestamp AS lt, \
          r.targetVersion AS rv, \
          r.targetTimestamp AS rt, \
          toInteger(parts[0]) AS major, \
          toInteger(parts[1]) AS minor, \
          toInteger(parts[2]) AS patch \
        ORDER BY artifactId, major, minor, patch \
        WITH artifactId, lv, lt, rv, rt \
        RETURN artifactId, collect({lv: lv, lt: lt, rv: rv, rt: rt}) as versions"

    result: dict =  call_api(path='/cypher', params={
        'query': query,
        'addedValues': []
    })

    save_json(result, 'output/result_all.json')
