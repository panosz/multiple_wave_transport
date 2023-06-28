from calculate_and_save_loss_times import calculate_and_save_loss_times

amplitudes = [
    0.48,
]

opts = dict(
    t_max=1000.0,
    n_particles=200_000,
)


for amplitude in amplitudes:
    calculate_and_save_loss_times(amplitude=amplitude, **opts)
