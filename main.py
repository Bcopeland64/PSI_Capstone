#!/usr/bin/env python3
"""SecTriage entry point.

Usage:
    python main.py full sample_data/sample_evidence --log sample_data/sample_auth.log --csv sample_data/sample_traffic.csv
    python main.py processes
    python main.py files sample_data/sample_evidence
    python main.py logs sample_data/sample_auth.log
    python main.py network sample_data/sample_traffic.csv
    python main.py history

Run `python main.py --help` or `python main.py <subcommand> --help` for details.
"""

import sys

from sectriage.cli import main

if __name__ == "__main__":
    sys.exit(main())
