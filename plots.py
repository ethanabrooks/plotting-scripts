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
            cmd = f"""\
rsync -avr  --include="**/" --include="**/*.hdf5" --exclude="*" {origin_path} {Path(local_path).expanduser()}\
"""
            subprocess.run([cmd], shell=True)

        def append(algorithm, local_path, **_):
            names.append(f"'{algorithm}'")
            paths.append(f"'{path_to_str(local_path)}'")

        for row in csv.DictReader(runs_file):
            if perform_copy:
                copy(**row)
            append(**row)

        plots_reader = csv.DictReader(plots_file)
        session = Server().new_session(session_name="plots", kill_session=True)

        def new_window(column, start, stop, path):
            cmd = " ".join(
                ["python", "plot.py"]
                + ["--names", *names]
                + ["--line-length-range", start, stop]
                + ["--paths", *paths]
                + ["--column", column]
                + ["--limit", str(limit)]
                + ["--fname", path_to_str(path)]
            )
            print(cmd)
            window = session.new_window(
                window_name=str(path), attach=True, window_shell=cmd
            )

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
