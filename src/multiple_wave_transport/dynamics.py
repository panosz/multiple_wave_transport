import json
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, dataclass
from itertools import repeat
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
class LossTimeResult:
    """
    Result of the loss time calculation
    """

    initial_states: list[Tuple[float, float]]
    loss_times: np.ndarray
    options: dict

    @classmethod
    def from_json(cls, s):
        """
        Create a LossTimeResult from a JSON string
        """
        d = json.loads(s)
        d["initial_states"] = [tuple(s) for s in d["initial_states"]]
        d["loss_times"] = np.array(d["loss_times"])

        return cls(**d)

    @classmethod
    def from_file(cls, filename):
        """
        Create a LossTimeResult from a JSON file
        """
        with open(filename, "r") as f:
            return cls.from_json(f.read())

    def to_json(self):
        """
        Convert the result to a JSON string
        """
        return to_json(self)


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
