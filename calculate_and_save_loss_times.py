from pathlib import Path
from typing import Tuple

from multiple_wave_transport.dynamics import calculate_loss_times

THIS_FOLDER = Path(__file__).parent
DATA_FOLDER = THIS_FOLDER / "data"

# make sure the data folder exists
DATA_FOLDER.mkdir(parents=True, exist_ok=True)


def calculate_and_save_loss_times(
    filename: str,
    t_max: float,
    amplitude: float,
    p_init_range: Tuple[float, float],
    p_max: float,
    n_particles: int,
):
    """
    Calculate the loss times and save them to a file
    """
    result = calculate_loss_times(t_max, amplitude, p_init_range, p_max, n_particles)
    with open(DATA_FOLDER / filename, "w") as f:
        f.write(result.to_json())


if __name__ == "__main__":
    amplitudes = [0.8, 1.2]
    t_max = 400.0
    p_init_range = (6.0, 17.0)
    p_max = 20
    n_particles = 200_000

    for amplitude in amplitudes:
        filename = f"loss_times_{amplitude:.1f}.json"
        calculate_and_save_loss_times(
            filename, t_max, amplitude, p_init_range, p_max, n_particles
        )
