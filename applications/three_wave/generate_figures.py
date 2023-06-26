from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from process_loss_data import process_and_plot_result

THIS_FOLDER = Path(__file__).parent

DATA_FOLDER = THIS_FOLDER / "data"

FIGURE_FOLDER = THIS_FOLDER / "figures"

FIGURE_FOLDER.mkdir(parents=True, exist_ok=True)

files = (
    "loss_times_34.8.json",
    "loss_times_27.8.json",
    "loss_times_22.8.json",
    "loss_times_18.8.json",
    "loss_times_16.8.json",
    "loss_times_14.8.json",
    "loss_times_12.8.json",
    "loss_times_9.8.json",
    "loss_times_8.8.json",
    "loss_times_7.8.json",
    "loss_times_6.8.json",
    "loss_times_4.8.json",
    "loss_times_2.8.json",
    "loss_times_1.5.json",
    "loss_times_3.8.json",
    "loss_times_42.0.json",
    "loss_times_38.0.json",
    "loss_times_30.8.json",
    "loss_times_25.8.json",
    "loss_times_20.8.json",
    "loss_times_15.8.json",
    "loss_times_10.8.json",
    "loss_times_5.8.json",
    "loss_times_1.8.json",
    "loss_times_10.3.json",
    "loss_times_9.3.json",
    "loss_times_8.3.json",
    "loss_times_7.3.json",
    "loss_times_6.3.json",
    "loss_times_5.3.json",
    "loss_times_4.3.json",
    "loss_times_3.3.json",
    "loss_times_2.3.json",
    "loss_times_15.3.json",
    "loss_times_14.3.json",
    "loss_times_13.8.json",
    "loss_times_13.3.json",
    "loss_times_12.3.json",
    "loss_times_11.8.json",
    "loss_times_11.3.json",
    "loss_times_24.3.json",
    "loss_times_17.8.json",
)


estimated_parameters = []

for filename in files:
    (
        result,
        estimated_parameters_i,
        fig,
    ) = process_and_plot_result(DATA_FOLDER / filename)
    figurename = f"plots_amp_{result.options['amplitude']:.1f}.png"
    fig.savefig(FIGURE_FOLDER / figurename)
    plt.close(fig)
    ampl = result.options["amplitude"]
    estimated_parameters_i["amplitude"] = ampl
    estimated_parameters.append(estimated_parameters_i)

estimated_parameters = pd.DataFrame(estimated_parameters)

estimated_parameters.to_csv(DATA_FOLDER / "estimated_parameters.csv", index=False)
