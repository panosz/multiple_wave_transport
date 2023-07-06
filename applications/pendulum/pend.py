import matplotlib.pyplot as plt
from dataclasses import dataclass
import numpy as np
from typing import Union

from multiple_wave_transport._multiple_wave_transport import (
    PerturbedPendulum,
    PerturbedPendulumWithLowFrequency,
    UnperturbedPendulum,
)
from multiple_wave_transport.losses import to_json
from multiple_wave_transport.math import angle_to_2pi, generate_random_pairs
from multiple_wave_transport.pendulum import build_pendulum


def _get_travelling_distance(pendulum, s, t_max):
    """
    returns the distance from the initial state s0 until time tmax
    at snapshots equally spaced in time with time step equal to pendulum.poincare_dt
    """
    snapshots = pendulum.poincare(s, t_max)

    translations = snapshots.T - snapshots[:, 0]

    distances = np.hypot(translations[:, 0], translations[:, 1])
    return distances


# A dataclass to store the results of the function below and be exportable to json
@dataclass
class ResultOfTravellingDistances:
    """
    A dataclass to store the results of the function below and be exportable to json
    """

    amplitude: Union[float, tuple[float, float]]
    x_min: float
    x_max: float
    p_min: float
    p_max: float
    tmax: float
    n_particles: int
    distances: np.ndarray

    def to_json(self):
        return to_json(self)


# Add type hints to the function below
def get_travelling_distances(amplitude, x_min, x_max, p_min, p_max, tmax, n_particles):
    """
    returns the distance from the initial state s0 until time tmax
    at snapshots equally spaced in time with time step equal to pendulum.poincare_dt

    The type of the pendulum is inferred from the amplitude argument.

    If amplitude is a float, the pendulum  unperturbed by a single wave.
    If amplitude is a tuple, the pendulum is perturbed by two waves.

    Parameters:
    -----------
    amplitude: float or (float, float)
        amplitude of the pendulum
    x_min: float
        minimum value of the initial angle
    x_max: float
        maximum value of the initial angle
    p_min: float
        minimum value of the initial momentum
    p_max: float
        maximum value of the initial momentum
    tmax: float
        maximum time
    n_particles: int
        number of particles
    """

    pendulum = build_pendulum(amplitude)
    initial_states = generate_random_pairs(n_particles, x_min, x_max, p_min, p_max)
    distances = [_get_travelling_distance(pendulum, s0, tmax) for s0 in initial_states]
    distances = np.column_stack(distances)

    return ResultOfTravellingDistances(
        amplitude=amplitude,
        x_min=x_min,
        x_max=x_max,
        p_min=p_min,
        p_max=p_max,
        tmax=tmax,
        n_particles=n_particles,
        distances=distances,
    )


if __name__ == "__main__":
    t_max = 1500
    amplitude = (0.6, 0.6)
    n_particles = 100

    pendulum = build_pendulum(amplitude)
    initial_states = generate_random_pairs(n_particles, 0, 2 * np.pi, -0.8, 0.8)

    distances = [_get_travelling_distance(pendulum, s0, t_max) for s0 in initial_states]

    distances = np.column_stack(distances)

    mean_distances = np.mean(distances, axis=1)

    t = np.arange(0, t_max, pendulum.poincare_dt)

    plt.plot(t, mean_distances / t)

    plt.show()
