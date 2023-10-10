#!/usr/bin/env python3
"""
Created on 2021-11-21 14:59

@author: johannes
"""
from datetime import datetime
from weather_rpi.utils import TIME_STRING_FMT


class DateFormatter:

    def __init__(self, serie, time_type):
        self.serie = serie
        self.time_type = time_type

    def __call__(self):
        """Return time object.

        time_type:
            'year'
            'hour'
            'day'
            'hour'
        """
        return [
            getattr(datetime.strptime(t, TIME_STRING_FMT), self.time_type)
            for t in self.serie
        ]
