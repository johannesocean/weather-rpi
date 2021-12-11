#!/usr/bin/env python3
"""
Created on 2021-11-21 16:00

@author: johannes
"""
import requests
import json
import time
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
    requests.request("PATCH", 'http://localhost:5000/import',
                     data=json.dumps(data),
                     headers={'Content-type': 'application/json'}
                     )


def poster():
    print('poster', datetime.now())
    db_rpi = settings.pi_db()
    df = db_rpi.get()
    data = {key: df[key].to_list() for key in df.columns}
    data['utmid'] = 'JA'
    link(data)


if __name__ == '__main__':
    db_rpi = settings.pi_db()
    start_time = time.time()

    df = db_rpi.get_last_timestamp()
    # df = db_rpi.get_time_log()

    print("Timeit:--%.5f sec" % (time.time() - start_time))

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
