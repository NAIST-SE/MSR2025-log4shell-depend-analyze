import json
from pathlib import Path
from typing import TypedDict
from ..lib.files import save_json


class Release(TypedDict):
    dependent_time: int
    dependent_version: str
    log4j_time: int
    log4j_version: str


type Result = list[str | list[Release]]


type Source = list[Result]

LOG4J_TIMESTAMP_2_17_0 = 1639792690000

SOURCE_FILE_PATH = Path("./output/A_Data_Preparation_and_Extraction/data_releases.json")
SAVE_FILE_PATH = Path("./output/A_Data_Preparation_and_Extraction/data_updates.json")


def main() -> None:

    with SOURCE_FILE_PATH.open() as f:
        results: Source = json.load(f)

    output_list: list[dict] = []

    for data in results:
        artifact_id: str = data[0]
        releases: list[Release] = data[1]

        old_releases = [r for r in releases if r["log4j_time"] < LOG4J_TIMESTAMP_2_17_0]
        new_releases = [r for r in releases if r["log4j_time"] >= LOG4J_TIMESTAMP_2_17_0]

        if not old_releases or not new_releases:
            continue

        previous_release = max(old_releases, key=lambda d: d["dependent_time"])
        next_release = min(new_releases, key=lambda d: d["dependent_time"])

        earliest_release = min(releases, key=lambda d: d["dependent_time"])
        latest_release = max(releases, key=lambda d: d["dependent_time"])

        total_release_timestamp_diff = latest_release["dependent_time"] - earliest_release["dependent_time"]

        release_frequency = total_release_timestamp_diff / (len(releases) - 1)

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

    save_json(output_list, SAVE_FILE_PATH)
    print(f"Extracted data has been saved to: '{SAVE_FILE_PATH}'")


if __name__ == "__main__":
    main()