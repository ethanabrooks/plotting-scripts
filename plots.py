#! /usr/bin/env python

from pathlib import Path
import csv
from libtmux import Session, Server


def main(plots_data: Path, runs_data: Path, limit: int):
    with plots_data.open() as plots_file, runs_data.open() as runs_file:
        runs_reader = csv.DictReader(runs_file)
        rows = [r for r in runs_reader]
        plots_reader = csv.reader(plots_file)
        next(plots_reader)  # skip header
        names = [f"'{r['algorithm']}'" for r in rows]
        paths = [f"'{r['local path']}'" for r in rows]
        server = Server()
        session = server.new_session(session_name="plots", kill_session=True)
        for tag, path in plots_reader:
            cmd = " ".join(
                "plot --names".split()
                + names
                + ["--base-dir", "''"]
                + ["--paths"]
                + paths
                + ["--tag", tag, "--limit", str(limit), "--fname", path]
            )
            window = session.new_window(window_name=tag, attach=True, window_shell=cmd)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--plots-data", type=Path, default=Path("plots.csv"))
    parser.add_argument("--runs-data", type=Path, default=Path("runs.csv"))
    parser.add_argument("--limit", type=int, required=True)
    main(**vars(parser.parse_args()))
