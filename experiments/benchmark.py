"""
Benchmark runner for median algorithms.

This module executes controlled performance experiments comparing
different median implementations over synthetic salary datasets.
"""

from __future__ import annotations

import csv
import math
import statistics
import time
from pathlib import Path
from typing import Callable

from algorithms import quickselect_median, sort_median
from data_gen import INPUT_SIZES, generate_salaries


REPETITIONS = 30

# Representative subset used only for correctness validation.
# Correctness is independent of input size, so validating on every
# benchmark size (especially 500k and 1M) would only increase startup
# cost without providing meaningful additional confidence.
VALIDATION_SIZES = INPUT_SIZES[:3]

OUTPUT_FILE = Path("reports") / "benchmark_results.csv"


def verify_correctness() -> None:
    """
    Verify that both median algorithms produce equivalent results.

    Raises
    ------
    ValueError
        If the algorithms return different medians for the same input.
    """
    for n in VALIDATION_SIZES:
        print(f"Validating correctness for n={n:,}")

        for seed in range(REPETITIONS):
            data = generate_salaries(n, seed=seed)

            result_sort = sort_median(data)
            result_quick = quickselect_median(data)

            if not math.isclose(
                result_sort,
                result_quick,
                rel_tol=1e-12,
                abs_tol=1e-12,
            ):
                raise ValueError(
                    "Median algorithms returned different results.\n"
                    f"n={n}, seed={seed}\n"
                    f"sort_median={result_sort}\n"
                    f"quickselect_median={result_quick}"
                )


def measure_algorithm(
    algorithm: Callable[[list[float]], float],
    datasets: list[list[float]],
) -> tuple[float, float]:
    """
    Measure execution time statistics for a median algorithm.

    Parameters
    ----------
    algorithm : Callable[[list[float]], float]
        Median function to benchmark.
    datasets : list[list[float]]
        Input datasets used for measurement.

    Returns
    -------
    tuple[float, float]
        Mean execution time and standard deviation (seconds).
    """
    execution_times: list[float] = []

    for data in datasets:
        # Defensive copy outside timed region.
        # Guarantees benchmark correctness even if a future algorithm
        # implementation mutates its input in-place.
        working_data = data.copy()

        start = time.perf_counter()
        algorithm(working_data)
        end = time.perf_counter()

        execution_times.append(end - start)

    mean_time = statistics.mean(execution_times)

    std_time = (
        statistics.stdev(execution_times)
        if len(execution_times) > 1
        else 0.0
    )

    return mean_time, std_time


def build_datasets(n: int) -> list[list[float]]:
    """
    Generate all datasets for a benchmark size.
    """
    return [
        generate_salaries(n, seed=seed)
        for seed in range(REPETITIONS)
    ]


def save_results(rows: list[dict]) -> None:
    """
    Save benchmark results to CSV.
    """
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open(
        mode="w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "n",
                "algorithm",
                "mean_time",
                "std_time",
            ],
        )

        writer.writeheader()
        writer.writerows(rows)


def run_benchmark() -> None:
    """
    Execute the complete benchmark experiment.

    The procedure is:

    1. Validate algorithm correctness.
    2. Generate datasets for each input size.
    3. Benchmark both algorithms.
    4. Save results to CSV.
    """
    print("=" * 60)
    print("MEDIAN ALGORITHM BENCHMARK")
    print("=" * 60)

    print("\nStep 1: Correctness validation")
    verify_correctness()
    print("Validation successful.\n")

    rows: list[dict] = []

    total_sizes = len(INPUT_SIZES)

    for index, n in enumerate(INPUT_SIZES, start=1):
        print(
            f"[{index}/{total_sizes}] "
            f"Processing n={n:,}"
        )

        datasets = build_datasets(n)

        sort_mean, sort_std = measure_algorithm(
            sort_median,
            datasets,
        )

        quick_mean, quick_std = measure_algorithm(
            quickselect_median,
            datasets,
        )

        rows.append(
            {
                "n": n,
                "algorithm": "sort_median",
                "mean_time": sort_mean,
                "std_time": sort_std,
            }
        )

        rows.append(
            {
                "n": n,
                "algorithm": "quickselect_median",
                "mean_time": quick_mean,
                "std_time": quick_std,
            }
        )

        print(
            f"  sort_median       "
            f"mean={sort_mean:.6f}s "
            f"std={sort_std:.6f}s"
        )

        print(
            f"  quickselect_median "
            f"mean={quick_mean:.6f}s "
            f"std={quick_std:.6f}s"
        )

    save_results(rows)

    print("\nBenchmark completed successfully.")
    print(f"Results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    run_benchmark()