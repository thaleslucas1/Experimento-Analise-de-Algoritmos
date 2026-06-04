"""
Median calculation using full sorting.

This module implements median computation by sorting all elements
with Merge Sort and then selecting the middle value(s).

Expected complexity:
    Time: O(n log n)
    Space: O(n)
"""

from typing import Sequence


def _merge(left: list[float], right: list[float]) -> list[float]:

    merged: list[float] = []

    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])

    return merged


def _merge_sort(values: list[float]) -> list[float]:

    if len(values) <= 1:
        return values

    middle = len(values) // 2

    left = _merge_sort(values[:middle])
    right = _merge_sort(values[middle:])

    return _merge(left, right)


def median(values: Sequence[float]) -> float:
    """
    Compute the median of a sequence using full sorting.

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

    data = _merge_sort(list(values))

    n = len(data)
    middle = n // 2

    if n % 2 == 1:
        return float(data[middle])

    return (data[middle - 1] + data[middle]) / 2.0