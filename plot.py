#! /usr/bin/env python

# stdlib
import argparse
from pathlib import Path
from typing import List, Optional, Tuple

# third party
import matplotlib.pyplot as plt
import itertools
import pandas as pd
import numpy as np
import seaborn as sns
import tensorflow as tf
import h5py
from tensorflow.python.framework.errors_impl import DataLossError


def cli():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--names", nargs="*", type=Path)
    parser.add_argument("--paths", nargs="*", type=Path)
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--tag", type=str)
    parser.add_argument("--line-length-range", nargs=2, type=int)
    parser.add_argument("--fname", type=str, default="plot")
    parser.add_argument("--quality", type=int)
    parser.add_argument("--dpi", type=int, default=256)
    main(**vars(parser.parse_args()))


def main(
    names: List[str],
    paths: List[Path],
    tag: str,
    limit: Optional[int],
    line_length_range: Tuple[int, int],
    quiet: bool,
    **kwargs,
):

    assert len(names) == len(paths)

    def get_dfs(low, high):
        for name, path in zip(names, paths):
            if not path.exists():
                if not quiet:
                    print(f"{path} does not exist")

            for hdf5_path in path.glob("**/*.hdf5"):
                print("Reading", hdf5_path)
                with h5py.File(hdf5_path, "r") as f:
                    dset = f["dataset"]
                    array = None
                    for i in itertools.count():
                        try:
                            array = np.array(dset[:-i] if i > 0 else dset)
                            break
                        except OSError as e:
                            print(f"Corrupt data at index -{i}.")
                            print(e)
                df = pd.DataFrame(
                    array, columns=["step", "progress", "reward", "length"]
                )
                ix = (low <= df["length"]) & (df["length"] <= high)
                if limit:
                    ix &= df["step"] < limit
                df = df[ix].groupby("step", sort=False).mean()
                df["name"] = name
                yield df

    data = pd.concat(get_dfs(*line_length_range))
    print("Plotting...")
    sns.lineplot(x=data.index, y=tag, hue="name", data=data)
    plt.legend(data["name"].unique())
    plt.axes().ticklabel_format(style="sci", scilimits=(0, 0), axis="x")
    plt.tight_layout()
    plt.savefig(**kwargs)


if __name__ == "__main__":
    cli()
