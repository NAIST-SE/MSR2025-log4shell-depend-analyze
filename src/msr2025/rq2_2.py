import json
from pathlib import Path
from typing import TypedDict

import matplotlib.pyplot as plt


class Data(TypedDict):
    artifact_id: str
    old_version: str
    old_time: int
    old_depend_version: str
    new_version: str
    new_time: int
    new_depend_version: str
    gap: int
    release_frequency: int


ONE_DAY = 24 * 60 * 60 * 1000


def main() -> None:
    source_path = Path("data.json")

    with source_path.open() as f:
        results: list[Data] = json.load(f)

    # Extract data where the major version has been updated
    major_version_updates = [
        r
        for r in results
        if r["old_version"].split(".")[0] != r["new_version"].split(".")[0]
    ]

    # Extract data where the minor version has been updated
    same_major_versions = [r for r in results if r not in major_version_updates]
    minor_version_updates = [
        r
        for r in same_major_versions
        if r["old_version"].split(".")[1] != r["new_version"].split(".")[1]
    ]

    # Extract data where the patch version has been updated
    patch_version_updates = [
        r for r in same_major_versions if r not in minor_version_updates
    ]

    major_version_gaps = [r["gap"] / ONE_DAY for r in major_version_updates]
    minor_version_gaps = [r["gap"] / ONE_DAY for r in minor_version_updates]
    patch_version_gaps = [r["gap"] / ONE_DAY for r in patch_version_updates]

    major_version_gaps.sort()
    minor_version_gaps.sort()
    patch_version_gaps.sort()

    output_path = Path("output")
    output_path.mkdir(exist_ok=True)

    plt.rc("pdf", fonttype=42)

    # Create a box plot of the gaps (with outliers)
    plt.boxplot(
        [major_version_gaps, minor_version_gaps, patch_version_gaps], showmeans=True
    )
    plt.xticks([1, 2, 3], ["Major", "Minor", "Patch"])
    plt.ylabel(
        "Number of days from publication until packages\nusing log4j 2.17.0 have been updated"
    )
    plt.savefig(output_path / "rq2_2.pdf")

    plt.clf()

    # Create a box plot of the gaps (without outliers)
    plt.boxplot(
        [major_version_gaps, minor_version_gaps, patch_version_gaps],
        showmeans=True,
        sym="",
    )
    plt.xticks([1, 2, 3], ["Major", "Minor", "Patch"])
    plt.ylabel(
        "Number of days from publication until packages\nusing log4j 2.17.0 have been updated"
    )
    plt.savefig(output_path / "rq2_2_no_outlier.pdf")

    major_version_median = major_version_gaps[len(major_version_gaps) // 2]
    minor_version_median = minor_version_gaps[len(minor_version_gaps) // 2]
    patch_version_median = patch_version_gaps[len(patch_version_gaps) // 2]

    print(f"Total packages       : {len(results)}")
    print(
        f"Major version updated: {len(major_version_updates)} (Median: {major_version_median:.0f})"
    )
    print(
        f"Minor version updated: {len(minor_version_updates)} (Median: {minor_version_median:.0f})"
    )
    print(
        f"Patch version updated: {len(patch_version_updates)} (Median: {patch_version_median:.0f})"
    )


if __name__ == "__main__":
    main()
