from datetime import date

import pytest

from scripts.pull_trip_data import month_range


def test_month_range_includes_both_ends():
    assert month_range("2022-02", "2022-04") == [
        date(2022, 2, 1),
        date(2022, 3, 1),
        date(2022, 4, 1),
    ]


def test_month_range_crosses_year_boundary():
    assert month_range("2022-12", "2023-01") == [date(2022, 12, 1), date(2023, 1, 1)]


def test_month_range_rejects_inverted_range():
    with pytest.raises(ValueError):
        month_range("2023-01", "2022-12")
