from typing import Tuple

import numpy as np

from multiple_wave_transport._multiple_wave_transport import ThreeWaveSystem
from multiple_wave_transport.math import angle_to_2pi, generate_random_pairs
from .losses import LossTimeResult


def _calculate_loss_time_for_state(
    state: Tuple[float, float],
    p_max: float,
    t_max: float,
    amplitude: float,
):
    tws = ThreeWaveSystem(amplitude)
    return tws.get_loss_time(state, p_max, t_max)


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

    initial_states = generate_random_pairs(n_particles, 0, 2 * np.pi, *p_init_range)

    loss_times = np.array(
        [
            _calculate_loss_time_for_state(s, p_max, t_max, amplitude)
            for s in initial_states
        ]
    )

    options = dict(
        t_max=t_max,
        amplitude=amplitude,
        p_init_range=p_init_range,
        p_max=p_max,
        n_particles=n_particles,
    )

    return LossTimeResult(initial_states, loss_times, options)


def generate_poincare_plot(ax, amplitude: float):
    tws = ThreeWaveSystem(amplitude)
    s_init_vect = generate_random_pairs(100, 0, 2 * np.pi, 3, 24)
    for s in s_init_vect:
        pc = tws.poincare(s, 3000)
        ax.plot(angle_to_2pi(pc[0]), pc[1], "k,", alpha=0.5)  # type: ignore

    return ax
