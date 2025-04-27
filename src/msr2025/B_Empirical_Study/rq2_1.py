"""
Run RQ2-1 analysis.

RQ2-1: To what extent is release frequency associated
with the response time to critical CVEs?

This script:
- Loads the dataset of package updates.
- Plots a scatter graph showing update delay vs. release frequency.
- Computes the Pearson correlation coefficient between the two.
"""

from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np

from .lib.constants import ONE_DAY
from .lib.files import load_source_file, save_plot

if TYPE_CHECKING:
    from .lib.type import Data


def main() -> None:
    """Run RQ2-1 analysis."""
    # Clear any existing plot
    plt.clf()

    # Load release data
    results: list[Data] = load_source_file()

    # Extract update delays and release frequencies (converted to days)
    gaps = [r["gap"] / ONE_DAY for r in results]
    release_frequencies = [r["release_frequency"] / ONE_DAY for r in results]

    # Plot scatter plot
    plt.scatter(gaps, release_frequencies)
    plt.xlabel(
        "Number of days from publication until"
        "packages using log4j 2.17.0 have been updated"
    )
    plt.ylabel("Release frequency (days)")
    plt.xlim(0, 50)
    plt.ylim(0, 100)

    # Save the plot
    save_plot("rq2_1.pdf")

    # Calculate and print the Pearson correlation coefficient
    correlation = np.corrcoef(gaps, release_frequencies)[0, 1]
    print(f"Correlation: {correlation:.2f}")


if __name__ == "__main__":
    main()
