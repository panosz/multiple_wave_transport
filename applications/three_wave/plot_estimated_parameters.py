from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

THIS_FOLDER = Path(__file__).parent

DATA_FOLDER = THIS_FOLDER / "data"

FIGURE_FOLDER = THIS_FOLDER / "figures"


df = pd.read_csv(DATA_FOLDER / "estimated_parameters.csv")

df.sort_values(by=["amplitude"], inplace=True)


fig, ax = plt.subplots(figsize=(8, 6))
ax.errorbar(df.amplitude, df.alpha, yerr=df.alpha_err, fmt="o", ecolor='r', capsize=5)
ax.set_ylabel(r"$\alpha$")
ax.set_xlabel("amplitude")
fig.suptitle("alpha")
fig.savefig(FIGURE_FOLDER / "estimated_parameters.png")


plt.show()
