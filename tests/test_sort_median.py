import pytest

from algorithms.median_sort import median


def test_returns_median_for_odd_length_sequence():
    assert median([3, 1, 2]) == 2.0


def test_returns_median_for_even_length_sequence():
    assert median([1, 2, 3, 4]) == 2.5


def test_returns_single_element_for_length_one():
    assert median([42]) == 42.0


def test_handles_already_sorted_sequence():
    assert median([1, 2, 3, 4, 5]) == 3.0


def test_handles_reverse_sorted_sequence():
    assert median([5, 4, 3, 2, 1]) == 3.0


def test_handles_all_equal_elements():
    assert median([7, 7, 7, 7, 7]) == 7.0


def test_handles_negative_values():
    assert median([-5, -1, -3]) == -3.0


def test_handles_float_values():
    assert median([1.5, 2.5, 3.5, 4.5]) == 3.0


def test_raises_value_error_for_empty_sequence():
    with pytest.raises(ValueError):
        median([])