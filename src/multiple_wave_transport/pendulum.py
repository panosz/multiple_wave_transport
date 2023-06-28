"""
this module contains functionality for studying the pendulum dynamics
"""
import numpy as np
from ._multiple_wave_transport import PerturbedPendulum, UnperturbedPendulum
from .losses import LossTimeResult
from multiple_wave_transport.math import generate_random_pairs
from scipy.special import ellipk
from .math import angle_to_2pi


def kappa_sq(s):
    return 0.5 * (1 + UnperturbedPendulum().energy(s))


def unperturbed_omega(s):
    k_sq = kappa_sq(s)
    if k_sq < 1:
        return np.pi / 2 / ellipk(k_sq)  # this is ok. scipy ellipk takes k^2
    else:
        k = np.sqrt(k_sq)
        return np.pi * k / ellipk(1 / k_sq)


def unperturbed_period(s):
    return 2 * np.pi / unperturbed_omega(s)


def generate_random_init_trapped_states(n):
    """
    Generate n random initial states that are trapped in the unperturbed potential.
    The states are uniformly distributed in the energy level and the canonical angle of the action angle pair.
    """
    init_pairs = generate_random_pairs(n, -1, 1, 0, 2 * np.pi)

    trapped_states = []

    for E, theta in init_pairs:
        x0 = np.pi
        p = np.sqrt(2 * (E + 1))
        s0 = (x0, p)
        omega = unperturbed_omega(s0)

        s = UnperturbedPendulum().integrate(s0, theta / omega)
        trapped_states.append(s)

    return trapped_states


def calculate_loss_times(
    t_max: float,
    amplitude: float,
    n_particles: int,
):
    """
    Calculate the loss times for a set of initial conditions
    """
    pert = PerturbedPendulum(amplitude)
    init_trapped_states = generate_random_init_trapped_states(n_particles)
    loss_times = np.array([pert.get_loss_time(s, t_max) for s in init_trapped_states])

    options = dict(
        t_max=t_max,
        amplitude=amplitude,
        n_particles=n_particles,
    )
    return LossTimeResult(init_trapped_states, loss_times, options)


def generate_poincare_plot(ax, amplitude, t_max=2500):
    pendulum = PerturbedPendulum(amplitude)
    initial_states = generate_random_pairs(100, 0, 2 * np.pi, -1.5, 1.5)
    for s in initial_states:
        pc = pendulum.poincare(s, t_max)
        ax.plot(angle_to_2pi(pc[0]), pc[1], "k,", alpha=0.5)  # type: ignore

