"""
Plot generation for the median benchmark experiment.

This script reads benchmark results from reports/benchmark_results.csv
and generates:

1. Empirical execution time plot with error bars.
2. Empirical vs theoretical complexity plot.

Generated files:
    plots/mean_time_vs_input_size.png
    plots/empirical_vs_theoretical.png
"""

from pathlib import Path
import csv

import matplotlib.pyplot as plt
import numpy as np


CSV_PATH = Path("reports/benchmark_results.csv")

EMPIRICAL_PLOT_PATH = Path("plots/mean_time_vs_input_size.png")
THEORETICAL_PLOT_PATH = Path("plots/empirical_vs_theoretical.png")


def carregar_resultados() -> dict:
    """
    Load benchmark results from CSV.

    Returns
    -------
    dict
        Benchmark data grouped by algorithm.
    """
    resultados = {
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

    with CSV_PATH.open("r", newline="", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            algoritmo = linha["algorithm"]

            resultados[algoritmo]["n"].append(
                int(linha["n"])
            )

            resultados[algoritmo]["mean_time"].append(
                float(linha["mean_time"])
            )

            resultados[algoritmo]["std_time"].append(
                float(linha["std_time"])
            )

    return resultados


def gerar_grafico_empirico(resultados: dict) -> None:
    """
    Generate empirical execution time plot with error bars.

    Parameters
    ----------
    resultados : dict
        Benchmark results grouped by algorithm.
    """
    plt.figure(figsize=(10, 6))

    for algoritmo, dados in resultados.items():
        plt.errorbar(
            dados["n"],
            dados["mean_time"],
            yerr=dados["std_time"],
            marker="o",
            capsize=4,
            label=algoritmo,
        )

    plt.xscale("log")

    plt.xlabel("Tamanho da entrada (n)")
    plt.ylabel("Tempo médio (s)")
    plt.title("Tempo médio de execução com barras de erro")

    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.savefig(EMPIRICAL_PLOT_PATH)
    plt.close()

    print(f"Arquivo gerado: {EMPIRICAL_PLOT_PATH}")


def gerar_grafico_teorico(resultados: dict) -> None:
    """
    Generate empirical vs theoretical growth plot.

    Parameters
    ----------
    resultados : dict
        Benchmark results grouped by algorithm.
    """
    plt.figure(figsize=(10, 6))

    sort_data = resultados["sort_median"]
    quick_data = resultados["quickselect_median"]

    n_sort = np.array(sort_data["n"], dtype=float)
    n_quick = np.array(quick_data["n"], dtype=float)

    tempo_sort = np.array(sort_data["mean_time"])
    tempo_quick = np.array(quick_data["mean_time"])

    plt.plot(
        n_sort,
        tempo_sort,
        marker="o",
        label="sort_median (empírico)",
    )

    plt.plot(
        n_quick,
        tempo_quick,
        marker="o",
        label="quickselect_median (empírico)",
    )

    referencia_nlogn = (
        tempo_sort[0]
        * (n_sort * np.log2(n_sort))
        / (n_sort[0] * np.log2(n_sort[0]))
    )

    referencia_n = (
        tempo_quick[0]
        * n_quick
        / n_quick[0]
    )

    plt.plot(
        n_sort,
        referencia_nlogn,
        "--",
        label="O(n log n)",
    )

    plt.plot(
        n_quick,
        referencia_n,
        "--",
        label="O(n)",
    )

    plt.xscale("log")

    plt.xlabel("Tamanho da entrada (n)")
    plt.ylabel("Tempo (s)")
    plt.title("Crescimento empírico versus crescimento teórico")

    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.savefig(THEORETICAL_PLOT_PATH)
    plt.close()

    print(f"Arquivo gerado: {THEORETICAL_PLOT_PATH}")


def main() -> None:
    """
    Generate all benchmark plots.
    """
    resultados = carregar_resultados()

    gerar_grafico_empirico(resultados)
    gerar_grafico_teorico(resultados)


if __name__ == "__main__":
    main()