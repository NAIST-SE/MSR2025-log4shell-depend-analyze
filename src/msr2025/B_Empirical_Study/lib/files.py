"""
Provides file-related utilities for the empirical study phase.

Includes:
- Loading preprocessed JSON data from the preparation step.
- Saving matplotlib plots with consistent formatting.
"""

from pathlib import Path
from typing import cast

from matplotlib import pyplot as plt

from ...lib import load_json
from .constants import SOURCE_FILE_PATH
from .type import Data


def load_source_file() -> list[Data]:
    """
    Load the JSON data file used in the empirical study.

    This function attempts to load preprocessed data. If the file does not exist,
    it provides a helpful error message suggesting to run the preparation step.

    Returns:
        list[Data]: A list of data records loaded from the JSON file.

    Raises:
        FileNotFoundError: If the expected file is not found.

    """
    try:
        return cast("list[Data]", load_json(SOURCE_FILE_PATH))
    except FileNotFoundError as err:
        error_message = (
            f"File '{SOURCE_FILE_PATH}' not found.\n"
            "You must run 'uv run data_preparation_and_extraction' first."
        )
        raise FileNotFoundError(error_message) from err


def save_plot(
    filename: str, output_dir: Path = Path("output/B_Empirical_Study")
) -> None:
    """
    Save the current matplotlib plot to the specified file.

    If the file format is PDF, sets the font type to 42 to ensure
    compatibility with vector graphics tools (e.g., Illustrator).

    Args:
        filename (str): The file name to save the plot to (e.g., 'plot.pdf').
        output_dir (Path): Path to save plot (default: './output/B_Empirical_Study').

    Raises:
        ValueError: If the filename does not include an extension.

    """
    if "." not in filename:
        error_message = "Filename must include a file extension (e.g., '.pdf', '.png')"
        raise ValueError(error_message)

    output_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(filename).suffix.lower()
    if ext == ".pdf":
        plt.rc("pdf", fonttype=42)

    plt.savefig(output_dir / filename)
