"""src/msr2025/B_Empirical_Study/lib/__init__.py

Initializes the empirical study utility library.

This package provides:
- Constants used across the empirical study phase.
- File-related utility functions for loading data and saving plots.
- Type definitions for structured data representation.
"""

from .constants import ONE_DAY, SOURCE_FILE_PATH
from .files import load_source_file, save_plot
from .type import Data

__all__ = [
    "ONE_DAY",
    "SOURCE_FILE_PATH",
    "load_source_file",
    "save_plot",
    "Data",
]
