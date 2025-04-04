"""
src/msr2025/B_Empirical_Study/rq1.py

RQ1: How promptly do packages integrating Log4j-Core address CVEs?

This script:
- Loads the processed data of packages and their dependent release dates.
- Plots a histogram showing how many days it took for packages to update after log4j 2.17.0.
- Calculates and prints the percentage of packages updated within 3 months and 1 year.
"""

import matplotlib.pyplot as plt

from .lib.constants import ONE_DAY
from .lib.files import load_source_file, save_plot
from .lib.type import Data


def main() -> None:
    # Clear any existing plots
    plt.clf()

    # Load the release transition data
    results: list[Data] = load_source_file()

    # Create a histogram of update delays (in days)
    gaps = [r["gap"] / ONE_DAY for r in results]
    plt.hist(gaps, bins=100)
    plt.xlabel(
        "Number of days from publication until packages using log4j 2.17.0 have been updated"
    )
    plt.ylabel("Number of packages")

    # Save the histogram plot
    save_plot("rq1.pdf")

    # Calculate statistics
    total_packages = len(gaps)
    packages_updated_within_three_months = sum(1 for gap in gaps if gap < 90)
    packages_updated_within_a_year = sum(1 for gap in gaps if gap < 365)

    # Output results
    print(f"Total packages                   : {total_packages}")
    print(
        f"% of packages updated in 3 months: {packages_updated_within_three_months / total_packages:.2%}\n"
        f"% of packages updated in a year  : {packages_updated_within_a_year / total_packages:.2%}"
    )


if __name__ == "__main__":
    main()
