import matplotlib
matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import argparse
import pandas as pd
import os


WSL_PATH = "//wsl.localhost//Ubuntu-20.04//home//akshat//projects//thesis//ikura//"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="summarise.py",
        description="Summarises the results of an experiment "
    )

    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="Path to the experiment",
        dest="path",
        required=True,
    )

    parser.add_argument(
        "-n",
        "--name",
        type=str,
        help="Name of the boxplot",
        dest="name",
        required=True
    )

    parser.add_argument(
        "-v",
        "--vars",
        nargs="*",
        help="Independent variables",
        dest="vars",
        required=False,
        default=[]
    )

    args = parser.parse_args()

    te = pd.read_csv(os.path.join(WSL_PATH, args.path, "all_tes.csv"))
    te = te.where(te["attacker?"] == False)
    te["TE"] /= 100
    
    te = te.where(te["tick"].le(20))

    te = te.dropna()
    for var in args.vars:
        te[var] = te[var].astype("int")

    te.drop(columns=["#id", "run", "tick"], inplace=True)

    grouped = te.groupby(args.vars).aggregate("mean")
    arr = grouped.unstack(0)

    fig, ax = plt.subplots()

    # Draw the boxplot
    heatmap = ax.imshow(arr, cmap=cm.coolwarm)

    cbar = plt.colorbar(heatmap, ticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
    cbar.set_label("Average Trajectory Error (m)")

    # Set x-axis tick labels
    ax.set_xlabel("History Size")
    ax.set_xticks(range(20))
    ax.set_xticklabels(range(2, 22))

    ax.set_ylabel("Startup Delay")
    ax.set_yticks(range(21))
    ax.set_yticklabels(range(21))
    ax.set_ylim(0, 20)

    plt.savefig(os.path.join("graphs", f"{args.name}.pdf"))