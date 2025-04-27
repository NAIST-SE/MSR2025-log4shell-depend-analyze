"""
Main launcher for the MSR 2025 Mining Challenge project.

This script sequentially runs:
1. A_Data_Preparation_and_Extraction: Prepares and labels data in Neo4j.
2. B_Empirical_Study: Performs empirical analysis on the prepared data.
"""

from . import A_Data_Preparation_and_Extraction, B_Empirical_Study


def main() -> None:
    """
    Launch the MSR 2025 Mining Challenge pipeline.

    1. Prepare and extract data in Neo4j
    2. Perform empirical study on the prepared data
    """
    print("\n========================================")
    print(" Step 1: Data Preparation & Extraction ")
    print("========================================")
    A_Data_Preparation_and_Extraction.main()

    print("\n========================================")
    print(" Step 2: Empirical Study ")
    print("========================================")
    B_Empirical_Study.main()


if __name__ == "__main__":
    main()
