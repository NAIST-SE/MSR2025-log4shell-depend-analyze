"""
Provides simple task execution utilities with CLI spinner animation.

Includes a spinner animation that runs in a separate thread while a task function
is executing, and shows a completion message when the task is done.
"""

import itertools
import sys
import threading
import time
from collections.abc import Callable
from typing import Any


def _spinner(label: str, done_event: threading.Event) -> None:
    """
    Show a spinner animation in the CLI while a task is running.

    This function loops through a sequence of spinner characters and displays
    them on the same line until the `done_event` is set.

    Args:
        label (str): A label to show alongside the spinner.
        done_event (threading.Event): Event object to indicate task completion.

    """
    spinner_cycle = itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])
    while not done_event.is_set():
        spin_char = next(spinner_cycle)
        sys.stdout.write(f"\r{spin_char} Running : {label}   ")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write(f"\r✔ Done    : {label}   \n")
    sys.stdout.flush()


def run_task(
    label: str, task: Callable[[], None] | Callable[[], list[dict[str, Any]]]
) -> None:
    """
    Run a task function with a CLI spinner animation.

    Starts the spinner in a background thread while executing the given task function.
    When the task is completed, the spinner stops and a success message is printed.

    Args:
        label (str): A label to display with the spinner.
        task (Callable): The task function to run.

    """
    done_event = threading.Event()
    spinner_thread = threading.Thread(target=_spinner, args=(label, done_event))
    spinner_thread.start()

    try:
        task()
    finally:
        done_event.set()
        spinner_thread.join()
