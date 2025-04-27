"""src/msr2025/A_Data_Preparation_and_Extraction/data_extraction.py

Processes release timeline data for log4j-core dependencies from JSON input.

This script identifies which versions of each artifact depend on log4j-core
before and after the 2.17.0 patch (related to the Log4Shell vulnerability),
and calculates the time gap and release frequency between them.
"""

from pathlib import Path
from typing import TypedDict, cast

from ..lib.files import load_json, save_json


# Type: Information about a single release
class Release(TypedDict):
    dependent_time: int
    dependent_version: str
    log4j_time: int
    log4j_version: str


# Type Alias: Element of array in the input JSON file
type Result = list[str | list[Release]]

# Type Alias: Structure of the input JSON file
type Source = list[Result]

# Timestamp for log4j-core version 2.17.0 release (in milliseconds)
LOG4J_TIMESTAMP_2_17_0 = 1639792690000

# Input/output file paths
SOURCE_FILE_PATH = Path("./output/A_Data_Preparation_and_Extraction/data_releases.json")
SAVE_FILE_PATH = Path("./output/A_Data_Preparation_and_Extraction/data_updates.json")


def main() -> None:
    """Main function for processing the JSON data and extracting release transitions.

    For each artifact, finds the last version depending on log4j before 2.17.0
    and the first version after, computes the time gap and release frequency,
    and outputs the result to a new JSON file.
    """
    try:
        results: Source = cast(Source, load_json(SOURCE_FILE_PATH))
    except FileNotFoundError:
        raise FileNotFoundError(
            f"File '{SOURCE_FILE_PATH}' not found.\nYou must run 'uv run data_preparation' first."
        )

    output_list: list[dict[str, int | str | float | object]] = []

    for data in results:
        artifact_id: str = cast(str, data[0])
        releases: list[Release] = cast(list[Release], data[1])

        # Split releases based on whether they depend on log4j before or after 2.17.0
        old_releases = [r for r in releases if r["log4j_time"] < LOG4J_TIMESTAMP_2_17_0]
        new_releases = [
            r for r in releases if r["log4j_time"] >= LOG4J_TIMESTAMP_2_17_0
        ]

        # Skip if both old and new versions are not found
        if not old_releases or not new_releases:
            continue

        # Get the latest release before 2.17.0 and the earliest after 2.17.0
        previous_release = max(old_releases, key=lambda d: d["dependent_time"])
        next_release = min(new_releases, key=lambda d: d["dependent_time"])

        # Get first and last release timestamps
        earliest_release = min(releases, key=lambda d: d["dependent_time"])
        latest_release = max(releases, key=lambda d: d["dependent_time"])

        # Calculate Release Frequency
        total_release_timestamp_diff = (
            latest_release["dependent_time"] - earliest_release["dependent_time"]
        )
        release_frequency = total_release_timestamp_diff / (len(releases) - 1)

        # Build output entry
        output = {
            "artifact_id": artifact_id,
            "old_version": previous_release["dependent_version"],
            "old_time": previous_release["dependent_time"],
            "old_depend_version": previous_release["log4j_version"],
            "new_version": next_release["dependent_version"],
            "new_time": next_release["dependent_time"],
            "new_depend_version": next_release["log4j_version"],
            "gap": next_release["dependent_time"] - LOG4J_TIMESTAMP_2_17_0,
            "release_frequency": release_frequency,
        }

        output_list.append(output)

    # Save result to file
    save_json(cast(dict, output_list), SAVE_FILE_PATH)  # type: ignore
    print(f"Extracted data has been saved to: '{SAVE_FILE_PATH}'")


if __name__ == "__main__":
    main()
