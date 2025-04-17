"""lib package for shared utility functions.

This package provides reusable tools for:
- loading environment variables from a .env file,
- saving and loading JSON files with automatic directory handling,
- running CLI tasks with spinner animations for visual feedback.
"""

from .envs import getenv
from .files import load_json, save_json
from .tasks import run_task

__all__ = [
    "getenv",
    "save_json",
    "load_json",
    "run_task",
]
