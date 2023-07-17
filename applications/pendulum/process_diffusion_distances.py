import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from pend import ResultOfTravellingDistances
from collections.abc import Iterable

from multiple_wave_transport.pendulum import build_pendulum

data = ResultOfTravellingDistances.from_json(
    "./data_diffusion/single_wave/distances1.0.json"
)


pendulum = build_pendulum(data.amplitude)

t = np.arange(0, data.tmax, pendulum.poincare_dt)

mean_distances = np.mean(data.distances, axis=1)


def load_data_collection_from_folder(folder):
    """
    load all json files in folder into a list of ResultOfTravellingDistances
    """
    files = Path(folder).glob("*.json")
    return [ResultOfTravellingDistances.from_json(f) for f in files]


def sort_by_amplitude(data_collection):
    """
    sort data_collection by amplitude
    """
    return sorted(data_collection, key=lambda x: x.amplitude[0] if isinstance(x.amplitude, tuple) else x.amplitude)


def load_traveling_distances(ampl):
    fname = f"./data_diffusion/distances({ampl}__{ampl}).json"
    return ResultOfTravellingDistances.from_json(fname)


def get_R(distances_data):
    mean_distances = np.mean(distances_data.distances, axis=1)
    pendulum = build_pendulum(distances_data.amplitude)
    t = np.arange(0, distances_data.tmax, pendulum.poincare_dt)
    return np.mean(mean_distances[-100:] / t[-100:])


def get_R_for_amplitude(ampl):
    data = load_traveling_distances(ampl)
    return get_R(data)


R = get_R(data)

data_collection = sort_by_amplitude(load_data_collection_from_folder("./data_diffusion/two_waves_both_increasing_ampl"))
amplitudes = [d.amplitude[0] if isinstance(d.amplitude, Iterable) else d.amplitude for d in data_collection]
Rs = [get_R(d) for d in data_collection]


plt.plot(t[1:], mean_distances[1:] / t[1:])
plt.axhline(R, color="red")

fig, ax = plt.subplots()
ax.plot(t, data.distances)

fig, ax = plt.subplots()
ax.plot(amplitudes, Rs, "o--")
plt.show()
