from pathlib import Path

from multiple_wave_transport._multiple_wave_transport import BoundaryType
from multiple_wave_transport.pendulum import (
    PerturbedPendulum,
    PerturbedPendulumWithLowFrequency,
    calculate_loss_times,
)

THIS_FOLDER = Path(__file__).parent
DATA_FOLDER = THIS_FOLDER / "data"

# make sure the data folder exists
DATA_FOLDER.mkdir(parents=True, exist_ok=True)


def get_filename_w_low_frequency(amplitude):
    return f"loss_times_{amplitude[0]:.2f}_{amplitude[1]:.2f}.json"


def get_filename_without_low_frequency(amplitude):
    return f"loss_times_{amplitude:.2f}.json"


def get_filename(amplitude, pendulumtype):
    if pendulumtype == PerturbedPendulum:
        return get_filename_without_low_frequency(amplitude)
    elif pendulumtype == PerturbedPendulumWithLowFrequency:
        return get_filename_w_low_frequency(amplitude)
    else:
        raise ValueError("Invalid pendulum type")


def calculate_and_save_loss_times(
    t_max: float,
    amplitude: float | tuple[float, float],
    n_particles: int,
    data_folder: Path | str = DATA_FOLDER,
    boundary_type: BoundaryType = BoundaryType.X,
):
    """
    Calculate the loss times and save them to a file
    """
    print(f"Calculating loss times for amplitude {amplitude}")
    result = calculate_loss_times(t_max, amplitude, n_particles, boundary_type)
    filename = get_filename(amplitude, pendulumtype)
    with open(Path(data_folder) / filename, "w") as f:
        f.write(result.to_json())


opts = dict(
    t_max=500.0,
    n_particles=200_000,
)

if __name__ == "__main__":
    amplitudes = [
        0.6,
        0.7,
        0.8,
        0.9,
        1.0,
        1.1,
        1.2,
        1.3,
        1.4,
        1.5,
    ]

    for amplitude in amplitudes:
        calculate_and_save_loss_times(amplitude=amplitude, **opts)
