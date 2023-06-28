from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import uniform_filter1d
from scipy.optimize import curve_fit

from multiple_wave_transport.three_wave import generate_poincare_plot
from multiple_wave_transport.losses import (
    LossTimeResult,
    calculate_current,
    filter_loss_times,
    get_spectrum,
)

THIS_FOLDER = Path(__file__).parent


def exp_decay(t, A, alpha):
    return A * alpha * np.exp(-t * alpha)


def process_and_plot_result(filename):
    """
    Process the result of a loss time calculation and plot the results
    """
    print(filename)

    result = LossTimeResult.from_json(filename.read_text())

    options = result.options

    _, actual_loss_times = filter_loss_times(result)

    times, current = calculate_current(
        actual_loss_times[actual_loss_times < 100], bins=5000
    )

    A0 = actual_loss_times.size

    # Fit the current to an exponential decay after taking a rolling average
    averaged_current = uniform_filter1d(current, size=105)
    popt, pcov = curve_fit(exp_decay, times, averaged_current, p0=[A0, 0.1])

    A_opt, alpha_opt = popt
    print("Optimal parameters are: A = {}, alpha_opt = {}".format(A_opt, alpha_opt))

    errors = np.sqrt(np.diag(pcov))
    print("Errors on the parameters are: A = {}, alpha = {}".format(*errors))

    estimated_parameters = {
        "A": A_opt,
        "alpha": alpha_opt,
        "A_err": errors[0],
        "alpha_err": errors[1],
    }

    fig = plt.figure(figsize=(15, 6), constrained_layout=True)
    gs = fig.add_gridspec(2, 2)

    ax_poincare = fig.add_subplot(gs[:, 0])
    ax_current = fig.add_subplot(gs[0, 1])
    ax_spectrum = fig.add_subplot(gs[1, 1])

    ax_current.plot(times, current)
    ax_current.set_ylabel("current (particles/s)")
    ax_current.set_xlabel("time (s)")
    ax_current.plot(times, exp_decay(times, *popt), color="r", linestyle="--", lw=2)
    ax_current.plot(times, averaged_current, color="g", linestyle="--", lw=2)
    axins = ax_current.inset_axes([0.5, 0.5, 0.47, 0.47])
    mask = np.logical_and(times > 2, times < 7)
    axins.plot(times[mask], current[mask])
    axins.plot(
        times[mask], exp_decay(times[mask], *popt), color="r", linestyle="--", lw=2
    )
    axins.plot(times[mask], averaged_current[mask], color="g", linestyle="--", lw=2)
    ax_current.indicate_inset_zoom(axins, edgecolor="black")

    frequencies, spectrum = get_spectrum(current, times)
    ax_spectrum.plot(frequencies, spectrum / spectrum.max())
    ax_spectrum.set_xlim(-0.1, 8)
    ax_spectrum.set_xlabel("frequency (Hz)")
    ax_spectrum.set_ylabel("spectrum (a.u.)")

    generate_poincare_plot(ax_poincare, options["amplitude"])
    ax_poincare.hlines(
        result.options["p_max"], 0, 2 * np.pi, color="r", linestyle="-", lw=2
    )
    ax_poincare.axhspan(*result.options["p_init_range"], color="r", alpha=0.2)
    ax_poincare.set_xlim(0, 2 * np.pi)
    ax_poincare.set_ylim(1, 26)
    ax_poincare.set_xlabel("$x$")
    ax_poincare.set_ylabel("$p$")
    fig.suptitle(f"amplitude: {options['amplitude']:.2f}")
    return result, estimated_parameters, fig


if __name__ == "__main__":
    filename = THIS_FOLDER / "data" / "loss_times_10.3.json"

    _, estimated_parameters, fig = process_and_plot_result(filename)

    print(estimated_parameters)

    plt.show()
