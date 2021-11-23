#!/usr/bin/env python3
"""
Created on 2021-11-21 12:33

@author: johannes
"""
import os
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP


def round_value(value, nr_decimals=3):
    """Docen."""
    return float(Decimal(str(value)).quantize(
        Decimal('%%1.%sf' % nr_decimals % 1),
        rounding=ROUND_HALF_UP)
    )


def get_base_folder():
    """Docen."""
    return os.path.dirname(os.path.realpath(__file__))


def get_timestamp_string(today=False, yesterday=False, fmt='%Y-%m-%d'):
    """Docen."""
    if today:
        return pd.Timestamp.today().strftime(fmt)
    elif yesterday:
        return (pd.Timestamp.today() - pd.Timedelta(days=1)).strftime(fmt)
