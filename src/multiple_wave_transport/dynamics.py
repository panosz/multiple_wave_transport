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

    options = dict(
        t_max=t_max,
        amplitude=amplitude,
        p_init_range=p_init_range,
        p_max=p_max,
        n_particles=n_particles,
    )

    return LossTimeResult(initial_states, loss_times, options)


def generate_poincare_plot(amplitude: float):
    tws = ThreeWaveSystem(amplitude)
    fig, ax = plt.subplots(1, 1)
    for p_init in np.linspace(1, 30, 20):
        pc = tws.poincare([0, p_init], 10000)
        ax.plot(angle_to_2pi(pc[0]), pc[1], "k,")  # type: ignore

    return fig, ax
