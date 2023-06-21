import json
from dataclasses import asdict, dataclass
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np

from multiple_wave_transport._multiple_wave_transport import ThreeWaveSystem
from multiple_wave_transport.math import angle_to_2pi, generate_random_pairs


def to_json(s):
    """
    Convert a dataclass to a JSON string
    """

    def converter(x):
        try:
            return asdict(x)
        except TypeError:
            try:
                return x.tolist()
            except AttributeError:
                return x

    return json.dumps(s, default=converter)


@dataclass
class IntegrationOptions:
    """
    Options for the integration
    """

    t_max: float
    amplitude: float
    p_init_range: Tuple[float, float]
    p_max: float
    n_particles: int


def calculate_loss_times(
    t_max: float,
    amplitude: float,
    p_init_range: Tuple[float, float],
    p_max: float,
    n_particles: int,
):
    """
    Calculate the loss times for a set of initial conditions
    """
    tws = ThreeWaveSystem(amplitude)

    initial_states = generate_random_pairs(n_particles, 0, 2 * np.pi, *p_init_range)

    loss_times = np.array(
        [tws.get_loss_time(s, p_max=p_max, t_max=t_max) for s in initial_states]
    )
    return initial_states, loss_times


def generate_poincare_plot(amplitude: float):
    tws = ThreeWaveSystem(amplitude)
    fig, ax = plt.subplots(1, 1)
    for p_init in np.linspace(1, 30, 20):
        pc = tws.poincare([0, p_init], 10000)
        ax.plot(angle_to_2pi(pc[0]), pc[1], "k,")  # type: ignore

    return fig, ax


options = dict(
    t_max=500.,
    amplitude=3.8,
    p_init_range=(6., 17.),
    p_max=20,
    n_particles=200,
)

initial_states, loss_times = calculate_loss_times(**options)

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

fig, ax = generate_poincare_plot(options["amplitude"])

print(to_json(options))
plt.show()
