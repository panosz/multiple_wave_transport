from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

THIS_FOLDER = Path(__file__).parent

DATA_FOLDER = THIS_FOLDER / "data"

FIGURE_FOLDER = THIS_FOLDER / "figures"


df = pd.read_csv(DATA_FOLDER / "estimated_parameters.csv")

df.sort_values(by=["amplitude"], inplace=True)


fig, (ax_steady, ax_transient) = plt.subplots(2,1, figsize=(8, 6), sharex=True, constrained_layout=True)
ax_steady.errorbar(df.amplitude, df.alpha_steady, yerr=df.alpha_err_steady, fmt="--o", ecolor='r', capsize=5)
ax_steady.set_ylabel(r"$\alpha$")
ax_steady.set_xlabel("amplitude")
ax_steady.set_title("steady")

ax_transient.errorbar(df.amplitude, df.alpha_transient, yerr=df.alpha_err_transient, fmt="--o", ecolor='r', capsize=5)
ax_transient.set_ylabel(r"$\alpha$")
ax_transient.set_xlabel("amplitude")
ax_transient.set_title("transient")
fig.suptitle("alpha")
fig.savefig(FIGURE_FOLDER / "estimated_alpha.png")

fig, (ax_steady, ax_transient) = plt.subplots(2,1, figsize=(8, 6), sharex=True, constrained_layout=True)
ax_steady.errorbar(df.amplitude, df.A_steady, yerr=df.A_err_steady, fmt="--o", ecolor='r', capsize=5)
ax_steady.set_ylabel(r"$A$")
ax_steady.set_xlabel("amplitude")
ax_steady.set_title("steady")

ax_transient.errorbar(df.amplitude, df.A_transient, yerr=df.A_err_transient, fmt="--o", ecolor='r', capsize=5)
ax_transient.set_ylabel(r"$A$")
ax_transient.set_xlabel("amplitude")
ax_transient.set_title("transient")
fig.suptitle("A")

fig.savefig(FIGURE_FOLDER / "estimated_A.png")


plt.show()
