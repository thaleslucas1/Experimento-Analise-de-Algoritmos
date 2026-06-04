import math

from algorithms import sort_median, quickselect_median
from data_gen import generate_salaries


SPECIAL_CASES = [
    [3, 1, 2],
    [1, 2, 3, 4],
    [42],
    [1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1],
    [7, 7, 7, 7, 7],
    [-5, -1, -3],
    [1.5, 2.5, 3.5, 4.5],
]


def assert_same_median(values):
    sort_result = sort_median(values)
    quick_result = quickselect_median(values)

    assert math.isclose(
        sort_result,
        quick_result,
        rel_tol=1e-12,
        abs_tol=1e-12,
    )


def test_algorithms_return_same_result_for_special_cases():
    for values in SPECIAL_CASES:
        assert_same_median(values)


def test_algorithms_return_same_result_for_generated_data():
    sizes = (
        1_000,
        5_000,
        10_000,
    )

    seeds = range(5)

    for n in sizes:
        for seed in seeds:
            values = generate_salaries(n, seed=seed)
            assert_same_median(values)