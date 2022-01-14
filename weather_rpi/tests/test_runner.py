#!/usr/bin/env python3
"""
Created on 2021-11-21 16:00

@author: johannes
"""
import os
import requests
import json
import time
import pandas as pd
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from weather_rpi.settings import Settings
from weather_rpi.data_handler import DataHandler
from weather_rpi import utils

settings = Settings()
dh = DataHandler(settings)


def start_job(func, minutes_interval=5):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func, 'interval', minutes=minutes_interval)
    scheduler.start()


def updater():
    print('updater', utils.get_now_timestring())
    db_rpi = settings.pi_db()
    db_weather = settings.weatherstation_db()
    ts1 = utils.get_today_timestring()
    ts2 = utils.get_yesterday_timestring()
    time_log = db_rpi.get_recent_time_log(tag_today=ts1, tag_yesterday=ts2)
    weather_data = db_weather.get_recent_data(tag_today=ts1, tag_yesterday=ts2)
    dh.append(weather_data)
    new_data = dh.get_filtered_data(time_log.timestamp.values)
    if not new_data.empty:
        print('new_data')
        db_rpi.post(new_data)


def updater_v2():
    print('updater', utils.get_now_timestring())
    db_rpi = settings.pi_db()
    db_weather = settings.weatherstation_db()

    ts1 = utils.get_today_timestring()
    ts2 = utils.get_yesterday_timestring()
    weather_data = db_weather.get_recent_data(tag_today=ts1, tag_yesterday=ts2)
    dh.append(weather_data)

    last_recorded_timestamp = db_rpi.get_last_timestamp()
    new_data = dh.get_filtered_data(None, last_ts=last_recorded_timestamp)

    if not new_data.empty:
        print('new_data')
        db_rpi.post(new_data)


def link(data):
    return requests.request(
        "PUT", '',
        data=json.dumps(data),
        headers={
            'Content-type': 'application/json',
            'apikey': ""
        }
    )


def api_timelog_call():
    url = ""
    return requests.request(
        "GET", url,
        headers={
            "Content-Type": "text",
            "apikey": ""
        }
    )


def poster():
    print('poster', datetime.now())
    db_rpi = settings.pi_db()
    df = db_rpi.get()
    data = {key: df[key].to_list() for key in df.columns}
    link(data)


def puter():
    db_rpi = settings.pi_db()
    data = db_rpi.get()
    data['presrel'] = data['presrel'].round(1)
    ts_serie = data['timestamp'].apply(pd.Timestamp)
    resp = api_timelog_call()
    last_timestamp = pd.Timestamp(resp.json()['time_log'][-1])
    boolean = ts_serie > last_timestamp
    print(last_timestamp)
    put_data = {key: data.loc[boolean, key].to_list() for key in data.columns}
    print(put_data)
    return link(put_data)


if __name__ == '__main__':
    # ts_resp = api_timelog_call()
    # print(ts_resp.json()['time_log'][-1])
    # resp = puter()
    db_rpi = settings.pi_db()
    db_weather = settings.weatherstation_db()
    last_ts = db_rpi.get_last_timestamp()
    last_ts = pd.Timestamp(last_ts)
    weather_data = db_weather.get_new_data(timetag=last_ts.strftime('%Y-%m-%d'))
    dh.append(weather_data)
    new_data = dh.get_filtered_data(last_ts=last_ts)
    if not new_data.empty:
        print('new_data')
        db_rpi.post(new_data)
    # start_time = time.time()
    # df = db_rpi.get_last_timestamp()
    # df = db_rpi.get_time_log()
    # l = api_timtreuelog_call()
    # print("Timeit:--%.5f sec" % (time.time() - start_time))

    # print('started: {}'.format(datetime.now()))
    #start_job(updater)
    #time.sleep(60)
    # start_job(poster)
    # df = db_weather.get_recent_data(
    #     tag_today=get_timestamp_string(today=True),
    #     tag_yesterday=get_timestamp_string(yesterday=True)
    # )
    # df = db_rpi.get_time_log()
    # df = db_rpi.get()

    # new_data = db_weather.get()
    # dh.append(new_data)
    # db_rpi.post(dh.df)
