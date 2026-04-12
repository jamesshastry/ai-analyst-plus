#!/usr/bin/env python3
"""Single entry point for all data generation in this repo.

Runs both:
  1. NovaMart world generator (generate.py) — practice + capstone datasets
  2. Experiment lab generator (experiments/generate_experiment_data.py) — 12 A/B test CSVs

Outputs:
  data/practice/       13 tables, CSV + DuckDB (novamart_practice.duckdb)
  data/capstone/       13 tables with landmines, CSV + DuckDB (novamart_capstone.duckdb)
  data/experiments/    12 experiment CSVs + _answers/ with ground-truth JSON keys

Usage:
    python data-generation/generate_all.py           # both
    python data-generation/generate_all.py --world   # novamart practice + capstone only
    python data-generation/generate_all.py --experiments  # experiment lab only
"""

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(label: str, script: Path) -> int:
    print(f"\n{'=' * 60}\n  {label}\n  {script}\n{'=' * 60}")
    result = subprocess.run([sys.executable, str(script)], cwd=script.parent)
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--world", action="store_true", help="only the NovaMart world")
    parser.add_argument("--experiments", action="store_true", help="only the experiment lab")
    args = parser.parse_args()

    both = not (args.world or args.experiments)
    rc = 0

    if args.world or both:
        rc |= run("NovaMart world (practice + capstone)", HERE / "generate.py")

    if args.experiments or both:
        rc |= run("Experiment lab (12 A/B + causal datasets)", HERE / "experiments" / "generate_experiment_data.py")

    print(f"\n{'=' * 60}\n  All generators finished (exit {rc})\n{'=' * 60}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
