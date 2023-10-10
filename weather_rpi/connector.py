#!/usr/bin/env python3
"""
Created on 2021-11-20 23:07

@author: johannes
"""
import os
import sqlite3
import pyodbc
from datetime import datetime, timedelta

from weather_rpi.utils import TIME_STRING_FMT


ACCESS_DB_COLUMNS = [
    'DevID', 'RecTime', 'InTemp', 'InHumi', 'Ch1Temp', 'Ch2Temp', 'Ch3Temp', 'Ch4Temp', 'Ch5Temp', 'Ch6Temp', 'Ch7Temp',
    'Ch8Temp', 'Ch1Humi', 'Ch2Humi', 'Ch3Humi', 'Ch4Humi', 'Ch5Humi', 'Ch6Humi', 'Ch7Humi', 'Ch8Humi', 'Ch1DewPoint',
    'Ch2DewPoint', 'Ch3DewPoint', 'Ch4DewPoint', 'Ch5DewPoint', 'Ch6DewPoint', 'Ch7DewPoint', 'Ch8DewPoint',
    'Ch1FeelLike', 'Ch2FeelLike', 'Ch3FeelLike', 'Ch4FeelLike', 'Ch5FeelLike', 'Ch6FeelLike', 'Ch7FeelLike',
    'Ch8FeelLike', 'AbsBaro', 'RelBaro', 'Wind', 'Gust', 'WindDir', 'Rain1', 'Rain2', 'Rain3', 'Rain4', 'Rain5',
    'Rain6', 'Rain7', 'Rain8'
]


def get_weather_db_conn():
    return pyodbc.connect(
        DRIVER=os.getenv('WEATHERDBDRIVER'),
        DBQ=os.getenv('WEATHERDB')
    )


def dict_factory(data: list[tuple], columns: list[str]):
    """Return dict with data as lists."""
    return {column: list(column_data) for column, column_data in zip(columns, zip(*data))}


def get_weather_db_data(query: str) -> dict:
    conn = get_weather_db_conn()
    cursor = conn.cursor()
    cursor.execute(query)
    _data = cursor.fetchall()
    _data = dict_factory(_data, ACCESS_DB_COLUMNS)
    return _data


class WeatherStationDB:

    def get_recent_data(self, tag_today=None, tag_yesterday=None):
        query = """select * from Record where (RecTime like '"""+tag_today+"""%' or RecTime like '"""+tag_yesterday+"""%')"""  # noqa E501
        return get_weather_db_data(query)

    def get_new_data(self, timetag=None):
        query = """
        select * from Record where RecTime >= DateValue('"""+timetag+"""')
        """
        return get_weather_db_data(query)

    @property
    def query(self):
        # return """select * from Record where (RecTime like '"""+self.start_time+"""%')"""
        return """select * from Record"""
        # return """select * from Record where (RecTime like '2021-10-20%' or RecTime like '2021-11-21%')"""


def get_db_conn():
    return sqlite3.connect(os.getenv('UTMDB', r"C:\utv_privat\weather-rpi\weather_rpi\db\utm.db"))


def get_sqlite_data(query: str) -> dict:
    """Return data from sqlite db."""
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    data = dict_factory(data, columns)
    return data


class RpiDB:

    def __init__(self, start_time=None, end_time=None):
        self._start_time = start_time
        self._end_time = end_time

    @staticmethod
    def post(data):
        conn = get_db_conn()
        data.to_sql('weather', conn, if_exists='append', index=False)

    @staticmethod
    def get():
        data = get_sqlite_data('select * from weather')
        return data

    @staticmethod
    def get_last_timestamp():
        data = get_sqlite_data('select MAX(timestamp) as ts from weather')
        return data['ts'][0]

    @staticmethod
    def get_time_log():
        data = get_sqlite_data('select timestamp from weather')
        return data

    @staticmethod
    def get_recent_time_log(tag_today=None, tag_yesterday=None):
        query = """select timestamp from weather where (timestamp like '"""+tag_today+"""%' or timestamp like '"""+tag_yesterday+"""%')"""  # noqa E501
        data = get_sqlite_data(query)
        return data

    def get_data_for_time_period(self):
        query = """select * from weather where timestamp between '"""+self.start_time+"""%' and '"""+self.end_time+"""%'"""  # noqa E501
        data = get_sqlite_data(query)
        return data

    @property
    def start_time(self):
        """Return start of time window."""
        return self._start_time

    @start_time.setter
    def start_time(self, period):
        if isinstance(period, str):
            ts = datetime.strptime(period, TIME_STRING_FMT)
        else:
            ts = period
        self._start_time = (ts - timedelta(hours=1)).strftime(TIME_STRING_FMT)

    @property
    def end_time(self):
        """Return end of time window."""
        return self._end_time

    @end_time.setter
    def end_time(self, period):
        if isinstance(period, str):
            ts = datetime.strptime(period, TIME_STRING_FMT)
        else:
            ts = period
        self._end_time = (ts + timedelta(hours=1)).strftime(TIME_STRING_FMT)


if __name__ == '__main__':
    os.environ['WEATHERDBDRIVER'] = 'Microsoft Access Driver (*.mdb, *.accdb)'
    os.environ['WEATHERDB'] = "C:/ProgramData/WeatherHome/WeatherHome.mdb"
    rip = RpiDB()
    data = rip.get()
    # ts = rip.get_last_timestamp()
    # ts_log = rip.get_time_log()
    # data = get_weather_db_data("""select * from Record""")

    pairs = list(zip(*data.values()))
    pairs.sort()
    sorted_data = {k: list(v) for k, v in zip(data.keys(), zip(*pairs))}
