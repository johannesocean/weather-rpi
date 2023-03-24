#!/usr/bin/env python3
"""
Created on 2021-12-11 15:17

@author: johannes

COPY THIS FILE TO WHEREVER YOU WOULD LIKE TO RUN IT.
"""
from dotenv import load_dotenv
load_dotenv()
import os
import time
import requests
import json
import pandas as pd
from weather_rpi.settings import Settings
from weather_rpi.data_handler import DataHandler
from weather_rpi import utils

settings = Settings()
dh = DataHandler(settings)
LOG = utils.Log(log_directory='log_sessions')


def api_put(data):
    return requests.request(
        "PUT", os.getenv('API_IMPORT_URL'),
        data=json.dumps(data),
        headers={
            'Content-type': 'application/json',
            'apikey': os.getenv('API_KEY')
        }
    )


def api_timelog_call():
    return requests.request(
        "GET", os.getenv('API_TIMELOG_URL'),
        headers={
            "Content-Type": "text",
            "apikey": os.getenv('API_KEY')
        }
    )


def local_updater():
    """Update the primary database.

    Using data from the weather station database.
    """
    db_rpi = settings.pi_db()
    db_weather = settings.weatherstation_db()
    db_weather.columns = settings.weather_db_fields
    dh.reset_dataframe()

    last_ts = db_rpi.get_last_timestamp()
    last_ts = pd.Timestamp(last_ts)
    weather_data = db_weather.get_new_data(timetag=last_ts.strftime('%Y-%m-%d'))

    dh.append(weather_data)
    new_data = dh.get_filtered_data(last_ts=last_ts)

    if not new_data.empty:
        db_rpi.post(new_data)
        LOG.write('success', 'new data imported to database')


def api_updater():
    """Update the API database with data from the primary database."""
    db_rpi = settings.pi_db()
    resp_timelog = api_timelog_call()
    api_last_timestamp = pd.Timestamp(resp_timelog.json()['time_log'][-1])
    db_rpi.start_time = api_last_timestamp
    db_rpi.end_time = pd.Timestamp.now()
    data = db_rpi.get_data_for_time_period()
    ts_serie = data['timestamp'].apply(pd.Timestamp)
    boolean = ts_serie > api_last_timestamp
    data = data.loc[boolean, :]

    if not data.empty:
        put_data = {key: data[key].to_list() for key in data.columns}
        resp = api_put(put_data)

        if resp.status_code == 200:
            LOG.write('success', 'new data sent to server')
        else:
            LOG.write(
                'WARNING',
                'data could not be sent due to error code {}'.format(resp.status_code)
            )


if __name__ == '__main__':
    tl = api_timelog_call()
    print(tl.json())
    # while True:
    #     try:
    #         local_updater()
    #     except Exception as e:
    #         LOG.write('error-LOCAL', str(e))
    #
    #     time.sleep(150)  # Pause for 2.30 min..
    #
    #     try:
    #         api_updater()
    #     except Exception as e:
    #         LOG.write('error-API', str(e))
    #
    #     time.sleep(150)  # Pause for 2.30 min..
