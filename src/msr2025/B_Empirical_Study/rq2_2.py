"""
Run RQ2-2 analysis.

RQ2-2: To what extent do response times to
critical CVEs vary across major, minor, and patch versions?

This script:
- Classifies updates into major, minor, and patch version changes.
- Draws box plots of update delays for each category (with and without outliers).
- Computes and prints the median delay for each type of version update.
"""

from typing import TYPE_CHECKING

import matplotlib.pyplot as plt

from .lib.constants import ONE_DAY
from .lib.files import load_source_file, save_plot

if TYPE_CHECKING:
    from .lib.type import Data


def main() -> None:
    """Run RQ2-2 analysis."""
    # Clear any existing plot
    plt.clf()

    # Load release transition data
    results: list[Data] = load_source_file()

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

    # Convert gaps to days and sort
    major_version_gaps = [r["gap"] / ONE_DAY for r in major_version_updates]
    minor_version_gaps = [r["gap"] / ONE_DAY for r in minor_version_updates]
    patch_version_gaps = [r["gap"] / ONE_DAY for r in patch_version_updates]

    # Plot boxplot (with outliers)
    major_version_gaps.sort()
    minor_version_gaps.sort()
    patch_version_gaps.sort()

    # Create a box plot of the gaps (with outliers)
    plt.boxplot(
        [major_version_gaps, minor_version_gaps, patch_version_gaps], showmeans=True
    )
    plt.xticks([1, 2, 3], ["Major", "Minor", "Patch"])
    plt.ylabel(
        "Number of days from publication until packages\n"
        "using log4j 2.17.0 have been updated"
    )
    save_plot("rq2_2.pdf")

    # Clear any existing plot
    plt.clf()

    # Create a box plot of the gaps (without outliers)
    plt.boxplot(
        [major_version_gaps, minor_version_gaps, patch_version_gaps],
        showmeans=True,
        sym="",
    )
    plt.xticks([1, 2, 3], ["Major", "Minor", "Patch"])
    plt.ylabel(
        "Number of days from publication until packages\n"
        "using log4j 2.17.0 have been updated"
    )
    save_plot("rq2_2_no_outlier.pdf")

    # Calculate medians (middle element from sorted list)
    major_version_median = major_version_gaps[len(major_version_gaps) // 2]
    minor_version_median = minor_version_gaps[len(minor_version_gaps) // 2]
    patch_version_median = patch_version_gaps[len(patch_version_gaps) // 2]

    # Output statistics
    print(f"Total packages       : {len(results)}")
    print(
        f"Major version updated: {len(major_version_updates)} "
        f"(Median: {major_version_median:.0f})"
    )
    print(
        f"Minor version updated: {len(minor_version_updates)} "
        f"(Median: {minor_version_median:.0f})"
    )
    print(
        f"Patch version updated: {len(patch_version_updates)} "
        f"(Median: {patch_version_median:.0f})"
    )


if __name__ == "__main__":
    main()
