from pathlib import Path

from calculate_and_save_loss_times import (
    BoundaryType,
    PerturbedPendulum,
    PerturbedPendulumWithLowFrequency,
    calculate_and_save_loss_times,
)

THIS_FOLDER = Path(__file__).parent
DATA_FOLDER = THIS_FOLDER / "data_w_low_freq"

# make sure the data folder exists
DATA_FOLDER.mkdir(parents=True, exist_ok=True)

amplitudes = [
    (1.0, 0.1),
    (1.4, 0.1),
    (2.4, 0.1),
]

opts = dict(
    t_max=1000.0,
    n_particles=200_000,
)

for amplitude in amplitudes:
    calculate_and_save_loss_times(
        amplitude=amplitude,
        **opts,
        data_folder=DATA_FOLDER,
        boundary_type=BoundaryType.X,
        pendulumtype=PerturbedPendulumWithLowFrequency,
    )
