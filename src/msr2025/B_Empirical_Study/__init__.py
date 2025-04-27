"""
Entry point for executing empirical study scripts.

This module runs:
- RQ1: Update delays after log4j 2.17.0.
- RQ2.1: Correlation between update delay and release frequency.
- RQ2.2: Comparison of update delays by version change type (major, minor, patch).
"""

from . import rq1, rq2_1, rq2_2


def main() -> None:
    """Run all empirical study scripts sequentially."""
    print("\n**** RQ 1 ****")
    rq1.main()

    print("\n**** RQ 2.1 ****")
    rq2_1.main()

    print("\n**** RQ 2.2 ****")
    rq2_2.main()


if __name__ == "__main__":
    main()
