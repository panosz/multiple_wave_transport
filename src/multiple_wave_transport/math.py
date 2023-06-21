from typing import Tuple

"""
Useful math functions
"""
import numpy as np


def angle_to_2pi(angle):
    """
    convert angle to 0 to 2pi. make sure it works for negative angles as well
    """
    return np.mod(angle, 2 * np.pi)


def generate_random_pairs(n, xmin, xmax, ymin, ymax) -> list[Tuple[float, float]]:
    """
    Generate n random pairs of numbers in the ranges [xmin, xmax] and [ymin, ymax]
    """
    x_values = np.random.uniform(xmin, xmax, n)

    y_values = np.random.uniform(ymin, ymax, n)

    pairs = list(zip(x_values, y_values))

    return pairs
