import time
from dataclasses import dataclass
from typing import Union

import matplotlib.pyplot as plt
import numpy as np

from multiple_wave_transport._multiple_wave_transport import (
    PerturbedPendulum,
    PerturbedPendulumWithLowFrequency,
    UnperturbedPendulum,
)
from multiple_wave_transport.losses import to_json
from multiple_wave_transport.pendulum import build_pendulum, generate_random_init_trapped_states


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
    E_min: float
    E_max: float
    tmax: float
    n_particles: int
    distances: np.ndarray

    def to_json(self):
        return to_json(self)


# Add type hints to the function below
def get_travelling_distances(amplitude, E_min, E_max, tmax, n_particles):
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
    E_min: float
        minimum energy
    E_max: float
        maximum energy
    tmax: float
        maximum time
    n_particles: int
        number of particles
    """

    pendulum = build_pendulum(amplitude)
    initial_states = generate_random_init_trapped_states(n_particles, E_min, E_max)
    distances = [_get_travelling_distance(pendulum, s0, tmax) for s0 in initial_states]
    distances = np.column_stack(distances)

    return ResultOfTravellingDistances(
        amplitude=amplitude,
        E_min=E_min,
        E_max=E_max,
        tmax=tmax,
        n_particles=n_particles,
        distances=distances,
    )


def save_travelling_distances(
    amplitude, E_min, E_max, tmax, n_particles, fname=None,
    datafolder=None
):
    if fname is None:
        fname = f"distances{amplitude}.json".replace(" ", "_").replace(",", "_")

    if datafolder is not None:
        fname = datafolder / fname

    print(f"Computing travelling distances for {amplitude}")

    res = get_travelling_distances(
        amplitude, E_min=E_min, E_max=E_max, tmax=tmax, n_particles=n_particles
    )

    print(f"Saving to {fname}")

    with open(fname, "w") as f:
        f.write(res.to_json())

    return res


if __name__ == "__main__":
    t_max = 120000
    amplitude = (0.6, 0.6)
    n_particles = 1000

    # time this function in miliseconds
    time_start = time.time()
    res = get_travelling_distances(
        amplitude, E_min=-1, E_max=0.8, tmax=t_max, n_particles=n_particles
    )
    delta_time = time.time() - time_start
    print(f"Time elapsed in second: {delta_time}")

    fname = f"distances{res.amplitude}.json".replace(" ", "_").replace(",", "_")

    with open(fname, "w") as f:
        f.write(res.to_json())

    mean_distances = np.mean(res.distances, axis=1)

    pendulum = build_pendulum(res.amplitude)
    t = np.arange(0, t_max, pendulum.poincare_dt)

    plt.plot(t[1:], mean_distances[1:] / t[1:])

    plt.show()
