"""
Synthetic salary data generator.

This module centralizes the generation of salary datasets used in
median benchmark experiments.

"""
from __future__ import annotations

import numpy as np

import random
from typing import Final

INPUT_SIZES: Final[tuple[int, ...]] = tuple(
    dict.fromkeys(
        int(n)
        for n in np.logspace(3, 6, num=100)
    )
)

MIN_SALARY: Final[float] = 1_000.0


MAX_SALARY: Final[float] = 50_000.0


def generate_salaries(
    n: int,
    seed: int | None = None,
) -> list[float]:
    """
    Generate a synthetic salary dataset.

    Parameters
    ----------
    n : int
        Number of salary values to generate.
    seed : int | None, default=None
        Optional random seed used to guarantee reproducibility.
        When the same seed and size are provided, the generated
        dataset will be identical across executions.

    Returns
    -------
    list[float]
        List containing ``n`` salary values sampled uniformly
        between MIN_SALARY and MAX_SALARY.
    """
    if n < 1:
        raise ValueError("n must be greater than zero.")

    rng = random.Random(seed)

    return [
        rng.uniform(MIN_SALARY, MAX_SALARY)
        for _ in range(n)
    ]