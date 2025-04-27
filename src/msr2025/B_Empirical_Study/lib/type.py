"""
Defines shared data types used in the empirical study phase.

Includes:
- Data: A dictionary-like structure representing a single release transition,
  including versions, timestamps, and their gap.
"""

from typing import TypedDict


class Data(TypedDict):
    """
    A dictionary-like structure representing a single release transition.

    Attributes:
        artifact_id (str): Unique identifier of the artifact.
        old_version (str): Previous dependent version.
        old_time (int): Timestamp of the previous release.
        old_depend_version (str): Log4j version at the previous release.
        new_version (str): Updated dependent version.
        new_time (int): Timestamp of the new release.
        new_depend_version (str): Log4j version at the new release.
        gap (int): Time difference in milliseconds between the new release and baseline.
        release_frequency (float): Frequency of releases.

    """

    artifact_id: str
    old_version: str
    old_time: int
    old_depend_version: str
    new_version: str
    new_time: int
    new_depend_version: str
    gap: int
    release_frequency: float
