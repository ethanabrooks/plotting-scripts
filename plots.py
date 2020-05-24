#! /usr/bin/env python

from rl_utils import plot
from pathlib import Path
import csv
import subprocess


def main(plots_data: Path, runs_data: Path, limit: int):
    with plots_data.open() as plots_file, runs_data.open() as runs_file:
        plots_reader = csv.reader(plots_file)
        for tag, fname in plots_reader:
            subprocess.run(["ls", "-l"])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--plots-data", type=Path, default=Path("plots.csv"))
    parser.add_argument("--runs-data", type=Path, default=Path("runs.csv"))
    parser.add_argument("--limit", type=int, required=True)
    main(**vars(parser.arg_parse()))
