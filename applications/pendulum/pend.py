import matplotlib.pyplot as plt
import numpy as np

from multiple_wave_transport._multiple_wave_transport import (
    PerturbedPendulum,
    PerturbedPendulumWithLowFrequency,
    UnperturbedPendulum,
)
from multiple_wave_transport.math import angle_to_2pi, generate_random_pairs
from multiple_wave_transport.pendulum import (
    calculate_loss_times,
    generate_poincare_plot,
)

if __name__ == "__main__":
    options = dict(
        t_max=150000,
        amplitude=(0.4, 0.1),
        n_particles=10000,
    )

    #  result = calculate_loss_times(**options)

    #  initial_states, loss_times = result.initial_states, result.loss_times

    #  actual_loss_times = loss_times[loss_times < options["t_max"]]

    #  fig, (ax, ax_freq) = plt.subplots(2, 1)
    #  ax.hist(actual_loss_times[actual_loss_times < 500], bins=5000)

    #  hist, times = np.histogram(actual_loss_times[actual_loss_times < 500], bins=5000)
    #  Y = np.fft.fft(hist)
    #  dt = times[1] - times[0]
    #  frequencies = np.fft.fftfreq(len(hist), dt)

    #  # Plot the amplitudes
    #  # We usually plot the absolute value of the FFT output, as it can be complex
    #  # Also, usually the relevant part of the FFT is the positive frequencies (frequencies >= 0)
    #  mask = frequencies >= 0
    #  base_wave_freq = 1 / (4 * np.pi)
    #  ax_freq.plot(frequencies[mask] / base_wave_freq, np.abs(Y[mask]))
    #  ax_freq.set_xlabel("Frequency (base wave frequency)")

    fig, ax = plt.subplots()
    generate_poincare_plot(
        ax,
        amplitude=options["amplitude"],
        t_max=options["t_max"],
    )

    plt.show()
