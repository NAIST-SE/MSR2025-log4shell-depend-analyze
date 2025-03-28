"""
lib package for shared utility functions.

This package includes tools for:
- loading environment variables from a .env file,
- saving JSON files with directory handling,
- running CLI tasks with spinner animations.
"""

from .envs import getenv
from .files import save_json
from .tasks import run_task

__all__ = [
    "getenv",
    "save_json",
    "run_task",
]