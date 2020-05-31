#! /usr/bin/env python

# stdlib
import argparse
from pathlib import Path
from typing import List, Optional, Tuple

# third party
import matplotlib.pyplot as plt
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
    parser.add_argument("--column", type=int)
    parser.add_argument("--line-length-range", nargs=2, type=int)
    parser.add_argument("--fname", type=str, default="plot")
    parser.add_argument("--quality", type=int)
    parser.add_argument("--dpi", type=int, default=256)
    main(**vars(parser.parse_args()))


def main(
    names: List[str],
    paths: List[Path],
    column: int,
    limit: Optional[int],
    line_length_range: Tuple[int, int],
    quiet: bool,
    **kwargs,
):

    assert len(names) == len(paths)

    def get_dfs():
        for name, path in zip(names, paths):
            if not path.exists():
                if not quiet:
                    print(f"{path} does not exist")

            for hdf5_path in path.glob("**/*.hdf5"):
                print("Reading", hdf5_path)
                f = h5py.File(hdf5_path, "r")
                dset = f["dataset"]
                array = np.array(dset)
                low, high = line_length_range
                lengths = array[:, 3]
                data = array[np.logical_and(low <= lengths, lengths <= high)]
                yield pd.DataFrame(
                    dict(step=data[:, 0], value=data[:, column], algorithm=name)
                ).sort_values("step")

    data = pd.concat(get_dfs())
    print("Plotting...")
    sns.lineplot(x="step", y="value", hue="algorithm", data=data)
    plt.legend(data["algorithm"].unique())
    plt.axes().ticklabel_format(style="sci", scilimits=(0, 0), axis="x")
    plt.tight_layout()
    plt.savefig(**kwargs)


if __name__ == "__main__":
    cli()
