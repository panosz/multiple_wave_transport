import matplotlib.pyplot as plt
import numpy as np
from scipy.special import ellipk

from multiple_wave_transport._multiple_wave_transport import (
    PerturbedPendulum,
    UnperturbedPendulum,
)
from multiple_wave_transport.losses import LossTimeResult
from multiple_wave_transport.math import angle_to_2pi, generate_random_pairs


def kappa_sq(s):
    return 0.5 * (1 + UnperturbedPendulum().energy(s))


def unperturbed_omega(s):
    k_sq = kappa_sq(s)
    if k_sq < 1:
        return np.pi / 2 / ellipk(k_sq)  # this is ok. scipy ellipk takes k^2
    else:
        k = np.sqrt(k_sq)
        return np.pi * k / ellipk(1 / k_sq)


def unperturbed_period(s):
    return 2 * np.pi / unperturbed_omega(s)


def generate_random_init_trapped_states(n):
    """
    Generate n random initial states that are trapped in the unperturbed potential.
    The states are uniformly distributed in the energy level and the canonical angle of the action angle pair.
    """
    init_pairs = generate_random_pairs(n, -1, 1, 0, 2 * np.pi)

    trapped_states = []

    for E, theta in init_pairs:
        x0 = np.pi
        p = np.sqrt(2 * (E + 1))
        s0 = (x0, p)
        omega = unperturbed_omega(s0)

        s = UnperturbedPendulum().integrate(s0, theta / omega)
        trapped_states.append(s)

    return trapped_states


def calculate_loss_times(
    t_max: float,
    amplitude: float,
    n_particles: int,
):
    """
    Calculate the loss times for a set of initial conditions
    """
    pert = PerturbedPendulum(amplitude)
    init_trapped_states = generate_random_init_trapped_states(n_particles)
    loss_times = np.array([pert.get_loss_time(s, t_max) for s in init_trapped_states])

    options = dict(
        t_max=t_max,
        amplitude=amplitude,
        n_particles=n_particles,
    )
    return LossTimeResult(init_trapped_states, loss_times, options)


if __name__ == "__main__":
    options = dict(
        t_max=500,
        amplitude=4.8,
        n_particles=10000,
    )

    result = calculate_loss_times(**options)

    initial_states, loss_times = result.initial_states, result.loss_times

    actual_loss_times = loss_times[loss_times < options["t_max"]]

    fig, (ax, ax_freq) = plt.subplots(2, 1)
    ax.hist(actual_loss_times[actual_loss_times < 500], bins=5000)

    hist, times = np.histogram(actual_loss_times[actual_loss_times < 500], bins=5000)
    Y = np.fft.fft(hist)
    dt = times[1] - times[0]
    frequencies = np.fft.fftfreq(len(hist), dt)

    # Plot the amplitudes
    # We usually plot the absolute value of the FFT output, as it can be complex
    # Also, usually the relevant part of the FFT is the positive frequencies (frequencies >= 0)
    mask = frequencies >= 0
    base_wave_freq = 1 / (4 * np.pi)
    ax_freq.plot(frequencies[mask] / base_wave_freq, np.abs(Y[mask]))
    ax_freq.set_xlabel("Frequency (base wave frequency)")

    plt.show()
