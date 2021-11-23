#!/usr/bin/env python3
"""
Created on 2021-11-21 16:00

@author: johannes
"""
import pandas as pd
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from weather_rpi.settings import Settings
from weather_rpi.data_handler import DataHandler
from weather_rpi.utils import get_timestamp_string

settings = Settings()
dh = DataHandler(settings)


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(updater, 'interval', minutes=5)
    scheduler.start()


def updater():
    print('updater', datetime.now())
    db_rpi = settings.pi_db()
    db_weather = settings.weatherstation_db()
    ts1 = get_timestamp_string(today=True)
    ts2 = get_timestamp_string(yesterday=True)
    time_log = db_rpi.get_recent_time_log(tag_today=ts1, tag_yesterday=ts2)
    weather_data = db_weather.get_recent_data(tag_today=ts1, tag_yesterday=ts2)
    dh.append(weather_data)
    new_data = dh.get_filterd_data(time_log.timestamp.values)
    if not new_data.empty:
        print('New data!')
        db_rpi.post(new_data)


if __name__ == '__main__':
    # start()
    import time

    # start_time = time.time()
    # df = db_weather.get_recent_data(
    #     tag_today=get_timestamp_string(today=True),
    #     tag_yesterday=get_timestamp_string(yesterday=True)
    # )
    # df = db_rpi.get_time_log()
    # df = db_rpi.get()
    # print("Timeit:--%.5f sec" % (time.time() - start_time))
    # new_data = db_weather.get()
    # dh.append(new_data)
    # db_rpi.post(dh.df)
