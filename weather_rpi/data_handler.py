#!/usr/bin/env python3
"""
Created on 2021-11-21 12:56

@author: johannes
"""
import pandas as pd
import numpy as np


class DataHandler:
    """Doc."""

    def __init__(self, settings):
        self.settings = settings
        self.df = None
        self.reset_dataframe()

    def reset_dataframe(self):
        """Doc."""
        self.df = pd.DataFrame(columns=self.settings.db_fields)

    def append(self, data):
        """Doc."""
        if type(data) == pd.DataFrame:
            if not data.empty:
                self.reset_dataframe()
                for db_name, cfig in self.settings.mapper.items():
                    weather_db_field = cfig.get('weather_db_field')
                    if 'converter' in cfig:
                        converter = cfig['converter'](data[weather_db_field], db_name)
                        self.df[db_name] = converter()
                    else:
                        self.df[db_name] = data[weather_db_field]
                self._qc()

    def _qc(self):
        """Doc."""
        for db_name, cfig in self.settings.qc.items():
            routine = cfig['routine'](self.df[db_name], cfig.get('range'))
            self.df[db_name] = routine()

        self.df = self.df.replace({np.nan: None})

    def get_filtered_data(self, exclude_timestamps, last_ts=None):
        """Doc."""
        if last_ts:
            return self.df.loc[self.df['timestamp'] > last_ts, :]
        else:
            return self.df.loc[~self.df['timestamp'].isin(exclude_timestamps), :]
