"""
Make sure that dates are in the correct order.

This module can be deleted if dates are no longer hardcoded in since.py.
"""
from datetime import date

from since import SOME_HISTORICAL_DATES


def test_dates():
    last_date = date.min

    for entry in SOME_HISTORICAL_DATES:
        assert entry[0] > last_date, 'Dates must be in chronological order'
        last_date = entry[0]
