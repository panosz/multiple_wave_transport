import numpy as np
import numpy.testing as nt

import multiple_wave_transport
from multiple_wave_transport.math import angle_to_2pi, generate_random_pairs


def test_version():
    assert multiple_wave_transport.__version__ == "0.0.1"


def test_positive_angle():
    nt.assert_allclose(angle_to_2pi(np.pi), np.pi)


def test_negative_angle():
    nt.assert_allclose(angle_to_2pi(-np.pi), np.pi)


def test_angle_over_2pi():
    nt.assert_allclose(angle_to_2pi(3 * np.pi), np.pi)


def test_zero_angle():
    nt.assert_allclose(angle_to_2pi(0), 0)


def test_multiple_2pi():
    for i in range(-10, 10):
        nt.assert_allclose(angle_to_2pi(i * 2 * np.pi), 0)


def test_generate_pairs_count():
    pairs = generate_random_pairs(10, 0, 1, 0, 1)
    assert len(pairs) == 10


def test_generate_pairs_ranges():
    pairs = generate_random_pairs(10, 1, 2, 3, 4)
    for x, y in pairs:
        assert 1 <= x <= 2
        assert 3 <= y <= 4


def test_generate_pairs_empty():
    pairs = generate_random_pairs(0, 0, 1, 0, 1)
    assert len(pairs) == 0
