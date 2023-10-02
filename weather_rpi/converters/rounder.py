#!/usr/bin/env python3
"""
Created on 2022-01-09 18:31

@author: johannes
"""
from weather_rpi.utils import round_value


class RounderFormatter:
    """Doc."""

    def __init__(self, serie, _):
        self.serie = serie

    def __call__(self):
        """Return rounded values (1 decimal)."""
        return [round_value(x, nr_decimals=1) for x in self.serie]
