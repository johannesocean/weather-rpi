#!/usr/bin/env python3
"""
Created on 2021-11-21 15:32

@author: johannes
"""
import os
import glob
import yaml
import copy
from weather_rpi import utils


class BaseSettings:
    """Doc."""

    def __init__(self):
        super(BaseSettings, self).__init__()
        self.db_fields = None
        self.mapper = None
        self.qc_routines = None
        self.qc = None
        self.converters = None
        self.pi_db = None
        self.weatherstation_db = None


class Settings(BaseSettings):
    """Doc."""

    def __init__(self):
        super(Settings, self).__init__()
        base = utils.get_base_folder()
        for fpath in glob.glob(os.path.join(base, r'etc\*.yaml')):
            with open(fpath) as fd:
                data = yaml.load(fd, Loader=yaml.FullLoader)
            for key, item in data.items():
                setattr(self, key, item)

    def __setattr__(self, name, value):
        """Define the setattr for self."""
        if isinstance(value, dict) and name in ('mapper', 'qc'):
            data = copy.deepcopy(value)
            for v_key, v_value in value.items():
                if 'converter' in v_value and hasattr(self, 'converters'):
                    data[v_key]['converter'] = self.converters.get(v_value['converter'])
                elif 'routine' in v_value and hasattr(self, 'qc_routines'):
                    data[v_key]['routine'] = self.qc_routines.get(v_value['routine'])
            super().__setattr__(name, data)
        else:
            super().__setattr__(name, value)


if __name__ == '__main__':
    s = Settings()
