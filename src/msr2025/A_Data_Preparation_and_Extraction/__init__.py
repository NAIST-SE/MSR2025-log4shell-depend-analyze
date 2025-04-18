"""
src/msr2025/A_Data_Preparation_and_Extraction/__init__.py

Combines the data preparation and extraction steps for Neo4j-based analysis.

This module sequentially executes:
1. Labeling and enriching the Neo4j database (data_preparation).
2. Analyzing version transitions and exporting results (data_extraction).
"""

from . import data_preparation, data_extraction


def main():
    """Run both data preparation and extraction steps in order."""

    print("\n**** Data Preparation ****")
    data_preparation.main()

    print("\n**** Data Extraction ****")
    data_extraction.main()


if __name__ == "__main__":
    main()
