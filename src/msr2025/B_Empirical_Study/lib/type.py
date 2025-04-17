"""src/msr2025/B_Empirical_Study/lib/type.py

Defines shared data types used in the empirical study phase.

Includes:
- Data: A dictionary-like structure representing a single release transition,
  including versions, timestamps, and their gap.
"""

from typing import TypedDict


# A dictionary-like structure representing a single release transition
class Data(TypedDict):
    artifact_id: str
    old_version: str
    old_time: int
    old_depend_version: str
    new_version: str
    new_time: int
    new_depend_version: str
    gap: int
    release_frequency: float
