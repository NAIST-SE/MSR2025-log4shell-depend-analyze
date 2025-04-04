# MSR2025-log4shell-depend-analyze

This repository contains the replication package for our paper which has been accepted for the Mining Challenge Track at the 22nd International Conference on Mining Software Repositories (MSR 2025).

Title: Mining for Lags in Updating Critical Security Threats: A Case Study of Log4j Library

Authors: Hidetake Tanaka, Kazuma Yamasaki, Momoka Hirose, Takashi Nakano, Youmei Fan, Kazumasa Shimari, Raula Gaikovina Kula, Kenichi Matsumoto

# How to Analyze?

Procedure for analyzing research questions using the extracted data.

## Preparation

1. Run [Neo4jWeaverDocker](https://github.com/Goblin-Ecosystem/Neo4jWeaverDocker) in default port.
1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/).
1. Run `git clone https://github.com/NAIST-SE/MSR2025-log4shell-depend-analyze.git`.
1. Run `cd MSR2025-log4shell-depend-analyze`.
1. Copy `.env.example` to `.emv`
1. Run `uv sync`.

## Usage

1. Run `uv run all`.
1. The result will be saved in `output/`.
