"""
Run RQ2-1 analysis.

RQ1: How promptly do packages integrating Log4j-Core address CVEs?

This script:
- Loads the processed data of packages and their dependent release dates.
- Plots a histogram of days packages took to update after log4j 2.17.0.
- Calculates and prints the percentage of packages updated within 3 months and 1 year.
"""

from typing import TYPE_CHECKING

import matplotlib.pyplot as plt

from .lib.constants import ONE_DAY
from .lib.files import load_source_file, save_plot

if TYPE_CHECKING:
    from .lib.type import Data


def main() -> None:
    """Run RQ2-1 analysis."""
    # Clear any existing plots
    plt.clf()

    # Load the release transition data
    results: list[Data] = load_source_file()

    # Create a histogram of update delays (in days)
    gaps = [r["gap"] / ONE_DAY for r in results]
    plt.hist(gaps, bins=100)
    plt.xlabel(
        "Number of days from publication until packages "
        "using log4j 2.17.0 have been updated",
    )
    plt.ylabel("Number of packages")

    # Save the histogram plot
    save_plot("rq1.pdf")

    # Calculate statistics
    total_packages = len(gaps)
    days_three_months = 90
    days_one_year = 365
    packages_updated_within_three_months = sum(
        1 for gap in gaps if gap < days_three_months
    )
    packages_updated_within_a_year = sum(1 for gap in gaps if gap < days_one_year)

    # Output results
    print(f"Total packages                   : {total_packages}")
    print(
        f"% of packages updated in 3 months: "
        f"{packages_updated_within_three_months / total_packages:.2%}\n"
        f"% of packages updated in a year  : "
        f"{packages_updated_within_a_year / total_packages:.2%}",
    )


if __name__ == "__main__":
    main()
