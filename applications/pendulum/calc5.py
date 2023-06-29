from calculate_and_save_loss_times import calculate_and_save_loss_times, BoundaryType
from pathlib import Path

THIS_FOLDER = Path(__file__).parent
DATA_FOLDER = THIS_FOLDER / "data_p_boundary"

# make sure the data folder exists
DATA_FOLDER.mkdir(parents=True, exist_ok=True)

amplitudes = [
    0.4,
    1.8,
    2.9,
]

opts = dict(
    t_max=1000.0,
    n_particles=200_000,
)


for amplitude in amplitudes:
    calculate_and_save_loss_times(amplitude=amplitude, **opts, data_folder=DATA_FOLDER, boundary_type=BoundaryType.P)
