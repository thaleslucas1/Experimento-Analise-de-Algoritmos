"""
Median calculation using full sorting.

This module implements median computation by sorting all elements
and then selecting the middle value(s).

Expected complexity:
    Time: O(n log n)
    Space: O(n)
"""

from typing import Sequence


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

    data = sorted(values)
    n = len(data)
    middle = n // 2

    if n % 2 == 1:
        return float(data[middle])

    return (data[middle - 1] + data[middle]) / 2.0