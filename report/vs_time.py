import matplotlib
matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

import argparse
import matplotlib.pyplot as plt
import numpy as np
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

    parser.add_argument(
        "-x",
        "--x_axis",
        type=str,
        help="Label to put on the x axis",
        required=True
    )

    args = parser.parse_args()

    te = pd.read_csv(os.path.join(WSL_PATH, args.path, "all_tes.csv"))
    te = te.where(te["attacker?"] == False)

    te = te.drop(["#id", "run"], axis=1)
    te["TE"] /= 100

    te = te.dropna()

    grouped = te.groupby(args.vars + ["tick"])
    means = grouped.aggregate("mean").unstack(0).to_numpy()
    stddevs = grouped.aggregate("std").unstack(0)

    fig, ax = plt.subplots()

    colours = plt.cm.jet(np.linspace(0,1,means.shape[1]))

    for i in range(means.shape[1]):
        ax.plot(means[:, i], color=colours[i])

    # Horrible code
    if "sybil" in args.path:
        legend_title_x = 146
        legend_range = range(20)
        legend_fontsize = 8
    elif "mu_bound" in args.path:
        legend_title_x = 145
        legend_range = range(1, 17)
        legend_fontsize = 10

    ax.text(legend_title_x, 0.55, args.x_axis)

    ax.legend(legend_range, loc=(1.04, 0), fontsize=legend_fontsize)
    ax.set_xlabel("Tick")
    ax.set_ylabel("Average Trajectory Error (m)")

    plt.savefig(os.path.join("graphs", f"{args.name}.pdf"),  bbox_inches="tight")

