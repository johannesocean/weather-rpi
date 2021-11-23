#!/usr/bin/env python3
"""
Created on 2021-11-21 18:22

@author: johannes
"""
import pandas as pd


class QCDates:
    """Doc."""

    def __init__(self, serie, _):
        self.serie = serie.copy()

    def __call__(self):
        """Return time object.

        time_type:
            'year'
            'hour'
            'day'
            'hour'
        """
        boolean = pd.isnull(self.serie)
        if boolean.any():
            self.serie[boolean] = None
        return self.serie
