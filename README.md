# MSR2025-log4shell-depend-analyze

## Preparation

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/).
1. Run `git clone https://github.com/NAIST-SE/MSR2025-log4shell-depend-analyze.git`.
1. Run `cd MSR2025-log4shell-depend-analyze`.
1. Run `uv sync`.

## Usage

1. Put `result_all.json` in the project root.
1. Run `uv run generate`.
1. Run `uv run <rq_name>` (e.g. `uv run rq1`).
1. The result will be saved in `output/`.
