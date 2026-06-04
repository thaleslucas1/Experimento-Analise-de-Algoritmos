"""
Plot generation for the median benchmark experiment.
Reads reports/benchmark_results.csv and saves plots to plots/.
"""

from pathlib import Path
import csv

import matplotlib.pyplot as plt
import numpy as np


CSV_PATH = Path("reports/benchmark_results.csv")

EMPIRICAL_PLOT_PATH = Path("plots/mean_time_vs_input_size.png")
THEORETICAL_PLOT_PATH = Path("plots/empirical_vs_theoretical.png")


def load_results() -> dict:
    """Load benchmark results from CSV grouped by algorithm."""
    results = {
        "sort_median": {
            "n": [],
            "mean_time": [],
            "std_time": [],
        },
        "quickselect_median": {
            "n": [],
            "mean_time": [],
            "std_time": [],
        },
    }

    with CSV_PATH.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            algorithm = row["algorithm"]

            results[algorithm]["n"].append(
                int(row["n"])
            )

            results[algorithm]["mean_time"].append(
                float(row["mean_time"])
            )

            results[algorithm]["std_time"].append(
                float(row["std_time"])
            )

    return results


def plot_empirical(results: dict) -> None:
    """Generate empirical execution time plot with error bars."""
    plt.figure(figsize=(10, 6))

    for algorithm, data in results.items():
        plt.errorbar(
            data["n"],
            data["mean_time"],
            yerr=data["std_time"],
            marker="o",
            capsize=4,
            label=algorithm,
        )

    plt.xscale("log")

    plt.xlabel("Input size (n)")
    plt.ylabel("Mean time (s)")
    plt.title("Mean execution time with error bars")

    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.savefig(EMPIRICAL_PLOT_PATH)
    plt.close()

    print(f"File saved: {EMPIRICAL_PLOT_PATH}")


def plot_theoretical(results: dict) -> None:
    """Generate empirical vs theoretical complexity plot."""
    plt.figure(figsize=(10, 6))

    sort_data = results["sort_median"]
    quick_data = results["quickselect_median"]

    n_sort = np.array(sort_data["n"], dtype=float)
    n_quick = np.array(quick_data["n"], dtype=float)

    time_sort = np.array(sort_data["mean_time"])
    time_quick = np.array(quick_data["mean_time"])

    plt.plot(
        n_sort,
        time_sort,
        marker="o",
        label="sort_median (empirical)",
    )

    plt.plot(
        n_quick,
        time_quick,
        marker="o",
        label="quickselect_median (empirical)",
    )

    ref_nlogn = (
        time_sort[0]
        * (n_sort * np.log2(n_sort))
        / (n_sort[0] * np.log2(n_sort[0]))
    )

    ref_n = (
        time_quick[0]
        * n_quick
        / n_quick[0]
    )

    plt.plot(
        n_sort,
        ref_nlogn,
        "--",
        label="O(n log n)",
    )

    plt.plot(
        n_quick,
        ref_n,
        "--",
        label="O(n)",
    )

    plt.xscale("log")

    plt.xlabel("Input size (n)")
    plt.ylabel("Time (s)")
    plt.title("Empirical vs theoretical growth")

    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.savefig(THEORETICAL_PLOT_PATH)
    plt.close()

    print(f"File saved: {THEORETICAL_PLOT_PATH}")


def main() -> None:
    """Generate all benchmark plots."""
    results = load_results()

    plot_empirical(results)
    plot_theoretical(results)


if __name__ == "__main__":
    main()