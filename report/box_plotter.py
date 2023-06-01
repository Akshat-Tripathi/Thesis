import matplotlib
matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})


import matplotlib.pyplot as plt
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

    parser.add_argument(
        "-s",
        "--skip",
        type=int,
        help="Number of ticks to skip",
        default=0
    )

    parser.add_argument(
        "-x",
        "--x_axis",
        type=str,
        help="Label to put on the x axis",
        required=True
    )
    
    parser.add_argument(
        "-y",
        "--y_axis",
        type=str,
        help="Label to put on the y axis",
        default="Average Trajectory Error (m)"
    )

    args = parser.parse_args()

    te = pd.read_csv(os.path.join(WSL_PATH, args.path, "all_tes.csv"))
    te = te.where(te["attacker?"] == False)
    te = te.where(te["tick"].ge(args.skip))
    te["TE"] /= 100

    # Just for contagion
    if "contagion" in args.path:
        te = te.where(te["attackers"] == True)
        te["hops"] = abs(te["#id"] - 5)

    te = te.dropna()
    for var in args.vars:
        te[var] = te[var].astype("int")

    grouped = te.groupby(args.vars)
    
    group_values = [list(group["TE"]) for _, group in grouped]

    fig, ax = plt.subplots()

    # Draw the boxplot
    ax.boxplot(group_values)

    # Set x-axis tick labels
    ax.set_xticklabels(grouped.groups.keys())

    # Add labels and title
    ax.set_xlabel(args.x_axis)
    ax.set_ylabel(args.y_axis)

    plt.savefig(os.path.join("graphs", f"{args.name}.pdf"))
