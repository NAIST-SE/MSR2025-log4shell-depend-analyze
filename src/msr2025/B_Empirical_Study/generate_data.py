import json
from pathlib import Path
from typing import TypedDict


class Release(TypedDict):
    rt: int  # release time
    rv: str  # release version
    lt: int  # dependency release time
    lv: str  # dependency release version


type Result = list[str | list[Release]]


type Source = list[Result]


LOG4J_TIMESTAMP_2_17_0 = 1639792690000


def main() -> None:
    source_path = Path("./output/result.json")

    with source_path.open() as f:
        results: Source = json.load(f)

    output_list: list[dict] = []

    for data in results:
        artifact_id: str = data[0]
        releases: list[Release] = data[1]

        old_releases = [r for r in releases if r["lt"] < LOG4J_TIMESTAMP_2_17_0]
        new_releases = [r for r in releases if r["lt"] >= LOG4J_TIMESTAMP_2_17_0]

        if not old_releases or not new_releases:
            continue

        previous_release = max(old_releases, key=lambda d: d["rt"])
        next_release = min(new_releases, key=lambda d: d["rt"])

        earliest_release = min(releases, key=lambda d: d["rt"])
        latest_release = max(releases, key=lambda d: d["rt"])

        total_release_timestamp_diff = latest_release["rt"] - earliest_release["rt"]

        release_frequency = total_release_timestamp_diff / (len(releases) - 1)

        output = {
            "artifact_id": artifact_id,
            "old_version": previous_release["rv"],
            "old_time": previous_release["rt"],
            "old_depend_version": previous_release["lv"],
            "new_version": next_release["rv"],
            "new_time": next_release["rt"],
            "new_depend_version": next_release["lv"],
            "gap": next_release["rt"] - LOG4J_TIMESTAMP_2_17_0,
            "release_frequency": release_frequency,
        }

        output_list.append(output)

    output_path = Path("data.json")

    with output_path.open("w") as f:
        json.dump(output_list, f, indent=2)


if __name__ == "__main__":
    main()
