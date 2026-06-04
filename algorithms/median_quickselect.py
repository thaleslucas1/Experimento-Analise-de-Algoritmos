"""
Median calculation using QuickSelect.

This module implements median computation through the QuickSelect
selection algorithm, avoiding full sorting.

Expected complexity:
    Average Time: O(n)
    Worst-case Time: O(n²)
    Space: O(n)
"""

import random
from typing import Sequence


def _partition(arr: list[float], left: int, right: int) -> int:
    """
    Partition the array around a randomly chosen pivot.

    Parameters
    ----------
    arr : list[float]
        Working array.
    left : int
        Left boundary.
    right : int
        Right boundary.

    Returns
    -------
    int
        Final pivot position.
    """
    pivot_index = random.randint(left, right)

    arr[pivot_index], arr[right] = arr[right], arr[pivot_index]

    pivot = arr[right]
    store_index = left

    for i in range(left, right):
        if arr[i] <= pivot:
            arr[store_index], arr[i] = arr[i], arr[store_index]
            store_index += 1

    arr[store_index], arr[right] = arr[right], arr[store_index]

    return store_index


def _quickselect(arr: list[float], k: int) -> float:
    """
    Find the k-th smallest element using QuickSelect.

    Parameters
    ----------
    arr : list[float]
        Working array.
    k : int
        Target index.

    Returns
    -------
    float
        k-th smallest value.
    """
    left = 0
    right = len(arr) - 1

    while True:
        pivot_index = _partition(arr, left, right)

        if pivot_index == k:
            return arr[pivot_index]

        if k < pivot_index:
            right = pivot_index - 1
        else:
            left = pivot_index + 1


def median(values: Sequence[float]) -> float:
    """
    Compute the median using QuickSelect.

    Parameters
    ----------
    values : Sequence[float]
        Non-empty sequence of numeric values.

    Returns
    -------
    float
        Median value.

    Raises
    ------
    ValueError
        If the input sequence is empty.
    """
    if not values:
        raise ValueError("Cannot compute median of an empty sequence.")

    n = len(values)
    middle = n // 2

    if n % 2 == 1:
        data = list(values)
        return float(_quickselect(data, middle))

    data_left = list(values)
    data_right = list(values)

    lower = _quickselect(data_left, middle - 1)
    upper = _quickselect(data_right, middle)

    return (lower + upper) / 2.0