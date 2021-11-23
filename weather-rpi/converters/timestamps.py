#!/usr/bin/env python3
"""
Created on 2021-11-21 14:59

@author: johannes
"""
import pandas as pd


class DateFormatter:
    """Doc."""

    def __init__(self, serie, time_type):
        self.serie = serie.apply(pd.Timestamp)
        self.time_type = time_type

    def __call__(self):
        """Return time object.

        time_type:
            'year'
            'hour'
            'day'
            'hour'
        """
        return self.serie.dt.__getattribute__(self.time_type)
