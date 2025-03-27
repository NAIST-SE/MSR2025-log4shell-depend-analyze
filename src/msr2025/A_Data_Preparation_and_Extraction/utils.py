import json
import os
import itertools
import threading
import time
import sys
from neo4j import GraphDatabase


def spinner(label: str, done_event: threading.Event):
    spinner_cycle = itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])
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
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
