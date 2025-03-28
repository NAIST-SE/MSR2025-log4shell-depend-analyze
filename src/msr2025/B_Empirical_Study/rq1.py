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


ONE_DAY = 24 * 60 * 60 * 1000


def main() -> None:
    plt.clf()

    source_path = Path("output/A_Data_Preparation_and_Extraction/data_updates.json")

    with source_path.open() as f:
        results: list[Data] = json.load(f)

    # Create a histogram of the gaps
    gaps = [r["gap"] / ONE_DAY for r in results]
    plt.hist(gaps, bins=100)
    plt.xlabel(
        "Number of days from publication until packages using log4j 2.17.0 have been updated"
    )
    plt.ylabel("Number of packages")

    # Save the plot
    output_path = Path("output")
    output_path.mkdir(exist_ok=True)
    plt.rc("pdf", fonttype=42)
    plt.savefig(output_path / "rq1.pdf")

    total_packages = len(gaps)
    packages_updated_within_three_months = sum(1 for gap in gaps if gap < 90)
    packages_updated_within_a_year = sum(1 for gap in gaps if gap < 365)

    print(f"Total packages                   : {total_packages}")
    print(
        f"% of packages updated in 3 months: {packages_updated_within_three_months / total_packages:.2%}\n"
        f"% of packages updated in a year  : {packages_updated_within_a_year / total_packages:.2%}"
    )


if __name__ == "__main__":
    main()
