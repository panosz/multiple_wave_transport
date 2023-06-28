from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import uniform_filter1d
from scipy.optimize import curve_fit

from multiple_wave_transport.losses import (
    LossTimeResult,
    calculate_current,
    filter_loss_times,
    get_spectrum,
)
from multiple_wave_transport.pendulum import generate_poincare_plot

THIS_FOLDER = Path(__file__).parent


def exp_decay(t, A, alpha):
    return A * alpha * np.exp(-t * alpha)


def fit_exp_decay(times, current, guess):
    popt, pcov = curve_fit(exp_decay, times, current, p0=guess)

    A_opt, alpha_opt = popt
    print(
        "Optimal parameters are: A = {}, alpha_opt = {}".format(
            A_opt,
            alpha_opt,
        )
    )

    errors = np.sqrt(np.diag(pcov))
    print("Errors on the parameters are: A = {}, alpha = {}".format(*errors))
    return popt, errors


def process_and_plot_result(filename, t_poincare):
    """
    Process the result of a loss time calculation and plot the results
    """
    print(filename)

    result = LossTimeResult.from_json(filename.read_text())

    options = result.options

    _, actual_loss_times = filter_loss_times(result)

    times, current = calculate_current(actual_loss_times, bins=10000)

    A0 = actual_loss_times.size

    # Fit the current to an exponential decay after taking a rolling average
    averaged_current = uniform_filter1d(current, size=505)
    popt, errors = fit_exp_decay(
        times[times > 200], averaged_current[times > 200], guess=(A0, 0.001)
    )

    print("transient parameters:")
    popt_transient, errors_transient = fit_exp_decay(
        times[times < 200], averaged_current[times < 200], guess=(A0, 0.001)
    )

    estimated_parameters = {
        "A_steady": popt[0],
        "alpha_steady": popt[1],
        "A_err_steady": errors[0],
        "alpha_err_steady": errors[1],
        "A_transient": popt_transient[0],
        "alpha_transient": popt_transient[1],
        "A_err_transient": errors_transient[0],
        "alpha_err_transient": errors_transient[1],
    }

    fig = plt.figure(figsize=(15, 6), constrained_layout=True)
    gs = fig.add_gridspec(2, 2)

    ax_poincare = fig.add_subplot(gs[:, 0])
    ax_current = fig.add_subplot(gs[0, 1])
    ax_spectrum = fig.add_subplot(gs[1, 1])

    ax_current.plot(times, current, alpha=0.8, lw=0.5)
    ax_current.set_ylabel("current (particles/s)")
    ax_current.set_xlabel("time (s)")
    ax_current.plot(times, exp_decay(times, *popt), color="r", lw=1, alpha=0.8)
    ax_current.plot(
        times, exp_decay(times, *popt_transient), color="y", lw=1, alpha=0.8
    )
    ax_current.plot(times, averaged_current, color="g", lw=1, alpha=0.8)
    axins = ax_current.inset_axes([0.5, 0.5, 0.47, 0.47])
    mask = np.logical_and(times > 200, times < 800)
    axins.plot(times[mask], current[mask], alpha=0.8, lw=0.5)
    axins.plot(times[mask], exp_decay(times[mask], *popt), color="r", lw=2, alpha=0.8)
    axins.plot(
        times[mask], exp_decay(times[mask], *popt_transient), color="y", lw=2, alpha=0.8
    )
    axins.set_ylim(-0.1, exp_decay(times[mask], *popt).max() * 1.1)
    axins.plot(times[mask], averaged_current[mask], color="g", lw=2, alpha=0.8)
    ax_current.indicate_inset_zoom(axins, edgecolor="black")

    frequencies, spectrum = get_spectrum(current, times)

    base_wave_freq = 1 / (4 * np.pi)
    frequencies = frequencies / base_wave_freq

    ax_spectrum.plot(frequencies, spectrum / spectrum.max())
    ax_spectrum.set_xlim(-0.1, 8)
    ax_spectrum.set_xlabel("frequency (f/f0)")
    ax_spectrum.set_ylabel("spectrum (a.u.)")

    generate_poincare_plot(ax_poincare, options["amplitude"], t_max=t_poincare)
    ax_poincare.set_xlim(0, 2 * np.pi)
    ax_poincare.set_ylim(-2.5, 2.5)
    ax_poincare.set_xlabel("$x$")
    ax_poincare.set_ylabel("$p$")
    fig.suptitle(f"amplitude: {options['amplitude']:.2f}")
    return result, estimated_parameters, fig


if __name__ == "__main__":
    filename = THIS_FOLDER / "data" / "loss_times_0.45.json"

    _, estimated_parameters, fig = process_and_plot_result(filename, t_poincare=25000)

    print(estimated_parameters)

    plt.show()