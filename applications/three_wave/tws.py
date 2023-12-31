import matplotlib.pyplot as plt
import numpy as np

from multiple_wave_transport.losses import LossTimeResult, to_json

from multiple_wave_transport.three_wave import (
    calculate_loss_times,
    generate_poincare_plot,
)

options = dict(
    t_max=500.0,
    amplitude=7.8,
    p_init_range=(6.0, 17.0),
    p_max=20,
    n_particles=20000,
)

result = calculate_loss_times(**options)

result2 = LossTimeResult.from_json(to_json(result))

assert np.allclose(result2.loss_times, result.loss_times)
assert result2.options["t_max"] == options["t_max"]


initial_states, loss_times = result.initial_states, result.loss_times

p_init_v = np.array([s[1] for s in initial_states])

actual_loss_times = loss_times[loss_times < options["t_max"]]


fig, ax = plt.subplots(1, 1)
ax.plot(p_init_v[loss_times < options["t_max"]], actual_loss_times, "k.")  # type: ignore

fig, (ax, ax_freq) = plt.subplots(2, 1)
ax.hist(actual_loss_times[actual_loss_times < 100], bins=1000)

hist, times = np.histogram(actual_loss_times[actual_loss_times < 100], bins=1000)
Y = np.fft.fft(hist)
dt = times[1] - times[0]
frequencies = np.fft.fftfreq(len(hist), dt)

# Plot the amplitudes
# We usually plot the absolute value of the FFT output, as it can be complex
# Also, usually the relevant part of the FFT is the positive frequencies (frequencies >= 0)
mask = frequencies >= 0
ax_freq.plot(frequencies[mask], np.abs(Y[mask]))

fig, ax = plt.subplots(1, 1)
generate_poincare_plot(ax, options["amplitude"])

print(to_json(options))
plt.show()
