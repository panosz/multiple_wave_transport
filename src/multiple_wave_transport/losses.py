"""
This module contains functionality related to loss times
"""
import json
from dataclasses import asdict, dataclass
from typing import Tuple

import numpy as np


def to_json(s):
    """
    Convert a dataclass to a JSON string
    """

    def converter(x):
        try:
            return asdict(x)
        except TypeError:
            try:
                return x.tolist()
            except AttributeError:
                return x

    return json.dumps(s, default=converter)


@dataclass
class LossTimeResult:
    """
    Result of the loss time calculation
    """

    initial_states: list[Tuple[float, float]] | np.ndarray
    loss_times: np.ndarray
    options: dict

    @classmethod
    def from_json(cls, s):
        """
        Create a LossTimeResult from a JSON string
        """
        d = json.loads(s)
        d["initial_states"] = [tuple(s) for s in d["initial_states"]]
        d["loss_times"] = np.array(d["loss_times"])

        return cls(**d)

    @classmethod
    def from_file(cls, filename):
        """
        Create a LossTimeResult from a JSON file
        """
        with open(filename, "r") as f:
            return cls.from_json(f.read())

    def to_json(self):
        """
        Convert the result to a JSON string
        """
        return to_json(self)
