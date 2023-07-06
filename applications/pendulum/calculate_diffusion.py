from multiprocessing import Pool
from pathlib import Path

import numpy as np
from pend import save_travelling_distances

from multiple_wave_transport._multiple_wave_transport import BoundaryType
from multiple_wave_transport.pendulum import (
    PerturbedPendulum,
    PerturbedPendulumWithLowFrequency,
    calculate_loss_times,
)

THIS_FOLDER = Path(__file__).parent
DATA_FOLDER = THIS_FOLDER / "data_diffusion"

# make sure the data folder exists
DATA_FOLDER.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    options = dict(
        x_min=-np.pi,
        x_max=np.pi,
        p_min=-0.8,
        p_max=0.8,
        tmax=120000,
        n_particles=1000,
    )

    def calc_and_save(amplitude):
        save_travelling_distances(amplitude, datafolder=DATA_FOLDER, **options)

    amplitudes = [
        (0.1, 0.1),
        (0.2, 0.2),
        (0.3, 0.3),
        (0.4, 0.4),
        (0.5, 0.5),
        (0.6, 0.6),
        (0.7, 0.7),
        (0.8, 0.8),
        (0.9, 0.9),
        (1.0, 1.0),
        (1.1, 1.1),
    ]

    with Pool(len(amplitudes)) as p:
        p.map(calc_and_save, amplitudes)
