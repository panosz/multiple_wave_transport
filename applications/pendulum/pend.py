import matplotlib.pyplot as plt
import numpy as np

from multiple_wave_transport.pendulum import calculate_loss_times

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
