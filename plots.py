#! /usr/bin/env python

from pathlib import Path
import csv
from libtmux import Session, Server
import subprocess


def path_to_str(p):
    return str(Path(p).expanduser())


def main(plots_data: Path, runs_data: Path, limit: int, perform_copy: bool):
    with plots_data.open() as plots_file, runs_data.open() as runs_file:
        names = []
        paths = []

        def copy(origin_path, local_path, **_):
            subprocess.run(
                ["rsync", "-av", path_to_str(origin_path), path_to_str(local_path)]
            )

        def append(algorithm, local_path, **_):
            names.append(f"'{algorithm}'")
            paths.append(f"'{local_path}'")

        for row in csv.DictReader(runs_file):
            if perform_copy:
                copy(**row)
            append(**row)

        plots_reader = csv.DictReader(plots_file)
        next(plots_reader)  # skip header
        session = Server().new_session(session_name="plots", kill_session=True)

        def new_window(tag, path):
            cmd = " ".join(
                ["plot"]
                + ["--names", *names]
                + ["--base-dir", "''"]
                + ["--paths", *paths]
                + ["--tag", tag]
                + ["--limit", str(limit)]
                + ["--fname", path_to_str(path)]
            )
            window = session.new_window(window_name=tag, attach=True, window_shell=cmd)

        for row in plots_reader:
            new_window(**row)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--plots-data", type=Path, default=Path("plots.csv"))
    parser.add_argument("--runs-data", type=Path, default=Path("runs.csv"))
    parser.add_argument("--limit", type=int, required=True)
    parser.add_argument("--no-copy", dest="perform_copy", action="store_false")
    main(**vars(parser.parse_args()))
