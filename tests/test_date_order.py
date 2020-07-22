"""
Make sure that dates are in the correct order.

This module can be deleted if dates are no longer hardcoded in history.py.
"""
from datetime import date

from since.history import DATES


def test_dates():
    last_date = date.min

    for test_date in DATES:
        assert test_date > last_date, 'Dates must be in chronological order'
        last_date = test_date
