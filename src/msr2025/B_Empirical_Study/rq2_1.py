import json
from pathlib import Path
from typing import TypedDict

import matplotlib.pyplot as plt
import numpy as np


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
    plt.clf()

    source_path = Path("output/A_Data_Preparation_and_Extraction/data_updates.json")

    with source_path.open() as f:
        results: list[Data] = json.load(f)

    # Create a scatter plot of the gaps and release frequencies
    gaps = [r["gap"] / ONE_DAY for r in results]
    release_frequencies = [r["release_frequency"] / ONE_DAY for r in results]
    plt.scatter(gaps, release_frequencies)
    plt.xlabel(
        "Number of days from publication until packages using log4j 2.17.0 have been updated"
    )
    plt.ylabel("Release frequency (days)")
    plt.xlim(0, 50)
    plt.ylim(0, 100)

    # Save the plot
    output_path = Path("output")
    output_path.mkdir(exist_ok=True)
    plt.rc("pdf", fonttype=42)
    plt.savefig(output_path / "rq2_1.pdf")

    # Calculate the correlation
    correlation = np.corrcoef(gaps, release_frequencies)[0, 1]
    print(f"Correlation: {correlation:.2f}")


if __name__ == "__main__":
    main()
