from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import uniform_filter1d
from scipy.optimize import curve_fit

from multiple_wave_transport.dynamics import LossTimeResult, generate_poincare_plot

THIS_FOLDER = Path(__file__).parent


def exp_decay(t, A, alpha):
    return A * alpha * np.exp(-t * alpha)


def get_spectrum(hist, times):
    """
    returns the spectrum of a histogram
    only the positive frequency part is returned
    """
    Y = np.fft.fft(hist)
    dt = times[1] - times[0]
    frequencies = np.fft.fftfreq(len(hist), dt)
    mask = frequencies >= 0
    return frequencies[mask], np.abs(Y[mask])


def filter_loss_times(loss_result):
    """
    get the actual loss times of the particles that are lost

    Particles that are not lost have a reported loss time equal to the integration time.
    These particles are left out of the result.
    """

    initial_states, loss_times = loss_result.initial_states, loss_result.loss_times
    p_init_v = np.array([s[1] for s in initial_states])

    actually_lost_mask = loss_times < loss_result.options["t_max"]

    actual_loss_times = loss_times[actually_lost_mask]

    ratio_of_lost_particles = actually_lost_mask.sum() / actually_lost_mask.size

    print(f"ratio of particles lost: {ratio_of_lost_particles:.2f}")
    print(actual_loss_times.size)
    print(loss_times.size)

    filtered_p_init_v = p_init_v[actually_lost_mask]

    return filtered_p_init_v, actual_loss_times


def calculate_current(lost_times, bins):
    """
    Calculate the current from the loss times

    The current is calculated by binning the loss times and dividing by the bin width

    Parameters:
        lost_times: the loss times of the Particles
        bins: the number of bins to use for the histogram

    Returns:
        times: the times at the center of the bins
        current: the current at the center of the bins
    """

    hist, times = np.histogram(lost_times, bins=bins)

    dt = times[1] - times[0]

    times = 0.5 * (times[:-1] + times[1:])
    current = hist / dt
    return times, current


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
    popt, pcov = curve_fit(exp_decay, times, averaged_current, p0=[A0, .1])

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
    axins.plot(times[mask], exp_decay(times[mask], *popt), color="r", linestyle="--", lw=2)
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
    filename = THIS_FOLDER / "data" / "loss_times_1.8.json"

    _, fig, estimated_parameters = process_and_plot_result(filename)
    
    print(estimated_parameters)

    plt.show()
