import matplotlib
matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

WSL_PATH = "//wsl.localhost//Ubuntu-20.04//home//akshat//projects//thesis//ikura//"
path = f"{WSL_PATH}//experiments//results//mu_bound"

te = pd.read_csv(os.path.join(WSL_PATH, path, "all_tes.csv"))
te = te.where(te["attacker?"] == False)

te = te.drop(["#id", "run"], axis=1)
te["TE"] /= 100

te = te.dropna()

grouped = te.groupby(["onramp", "tick"])
means = grouped.aggregate("mean").unstack(0).to_numpy()
stddevs = grouped.aggregate("std").unstack(0)

fig, ax = plt.subplots()

colours = plt.cm.jet(np.linspace(0,1,16))

for i in range(16):
    ax.plot(means[:, i], color=colours[i])

ax.text(145, 0.55, "Onramp Size")

ax.legend(range(1, 17), loc=(1.04, 0))
ax.set_xlabel("Tick")
ax.set_ylabel("Average Trajectory Error (m)")


plt.savefig(os.path.join("graphs", f"mu_bound_vs_time.pdf"),  bbox_inches="tight")

