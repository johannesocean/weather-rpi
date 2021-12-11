#!/usr/bin/env python3
# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-12-11 15:17

@author: johannes

COPY THIS FILE TO WHEREVER YOU WOULD LIKE TO RUN IT.
"""
import time
from weather_rpi.settings import Settings
from weather_rpi.data_handler import DataHandler
from weather_rpi import utils

settings = Settings()
dh = DataHandler(settings)
LOG = utils.Log(log_directory='log_sessions')


def updater():
    """Update the primary database with data from the weather station database."""
    db_rpi = settings.pi_db()
    db_weather = settings.weatherstation_db()
    dh.reset_dataframe()

    ts1 = utils.get_today_timestring()
    ts2 = utils.get_yesterday_timestring()
    weather_data = db_weather.get_recent_data(tag_today=ts1, tag_yesterday=ts2)
    dh.append(weather_data)

    last_recorded_timestamp = db_rpi.get_last_timestamp()
    new_data = dh.get_filtered_data(None, last_ts=last_recorded_timestamp)

    if not new_data.empty:
        db_rpi.post(new_data)
        LOG.write('success', 'new data imported to database')


if __name__ == '__main__':
    while True:
        try:
            updater()
        except Exception as e:
            LOG.write('error', str(e))

        time.sleep(300)  # Pause for 2 min..
