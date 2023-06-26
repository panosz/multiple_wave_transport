"""
This module contains functionality related to loss times
"""
import json
from dataclasses import asdict, dataclass
from typing import Tuple

import numpy as np


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

    initial_states: list[Tuple[float, float]] | np.ndarray
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
