#!/usr/bin/env python3
"""
Created on 2021-11-21 12:56

@author: johannes
"""
from datetime import datetime

from weather_rpi.utils import TIME_STRING_FMT


class DataHandler:

    def __init__(self, settings):
        self.settings = settings
        self.df = None
        self.reset_dataframe()

    def reset_dataframe(self):
        self.df = {col: [] for col in self.settings.db_fields}

    def append(self, data):
        if isinstance(data, dict):
            if data[self.settings.db_fields[0]]:
                self.reset_dataframe()
                for db_name, cfig in self.settings.mapper.items():
                    weather_db_field = cfig.get('weather_db_field')
                    if 'converter' in cfig:
                        converter = cfig['converter'](data[weather_db_field], db_name)
                        self.df[db_name] = converter()
                    else:
                        self.df[db_name] = data[weather_db_field]
                self._qc()

                # sorting data based on timestamp
                pairs = list(zip(*data.values()))
                pairs.sort()
                self.df = {k: list(v) for k, v in zip(data.keys(), zip(*pairs))}

    def _qc(self):
        for db_name, cfig in self.settings.qc.items():
            routine = cfig['routine'](self.df[db_name], cfig.get('range'))
            self.df[db_name] = routine()

    def get_filtered_data(self, last_ts: datetime = None) -> dict:
        if last_ts:
            dt_serie = [datetime.strptime(t, TIME_STRING_FMT) for t in self.df['timestamp']]
            idx = next((i for i, dt in enumerate(dt_serie) if dt > last_ts), None)
            return {key: values[idx:] for key, values in self.df.items()}
        return {}
