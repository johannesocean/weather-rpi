#!/usr/bin/env python3
"""
Created on 2021-11-20 23:07

@author: johannes
"""
import os
import sqlite3
import pyodbc
import pandas as pd


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


class WeatherStationDB:

    def get(self):
        conn = get_weather_db_conn()
        return pd.read_sql(self.query, conn)

    def get_recent_data(self, tag_today=None, tag_yesterday=None):
        conn = get_weather_db_conn()
        return pd.read_sql(
            """select * from Record where (RecTime like '"""+tag_today+"""%' or RecTime like '"""+tag_yesterday+"""%')""",
            conn
        )
        # # rewrite using only pydbc and raw python
        # cursor = conn.cursor()
        # cursor.execute(
        #     """select * from Record where (RecTime like '"""+tag_today+"""%' or RecTime like '"""+tag_yesterday+"""%')"""
        # )
        # data = cursor.fetchall()
        # columns = [column[0] for column in cursor.description]  # this did not give me the right columns...


    def get_new_data(self, timetag=None):
        conn = get_weather_db_conn()
        query = """
        select * from Record where RecTime >= DateValue('"""+timetag+"""')
        """
        return pd.read_sql(query, conn)

    @property
    def query(self):
        # return """select * from Record where (RecTime like '"""+self.start_time+"""%')"""
        return """select * from Record"""
        # return """select * from Record where (RecTime like '2021-10-20%' or RecTime like '2021-11-21%')"""


def get_db_conn():
    return sqlite3.connect(os.getenv('UTMDB'))


class RpiDB:

    @staticmethod
    def post(data):
        conn = get_db_conn()
        data.to_sql('weather', conn, if_exists='append', index=False)

    @staticmethod
    def get():
        conn = get_db_conn()
        return pd.read_sql('select * from weather', conn)

    @staticmethod
    def get_last_timestamp():
        conn = get_db_conn()
        return pd.read_sql(
            'select MAX(timestamp) as ts from weather', conn
        )['ts'][0]

    @staticmethod
    def get_time_log():
        conn = get_db_conn()
        query = """select timestamp from weather"""
        return pd.read_sql(query, conn)

    @staticmethod
    def get_recent_time_log(tag_today=None, tag_yesterday=None):
        conn = get_db_conn()
        return pd.read_sql(
            """select timestamp from weather where (timestamp like '"""+tag_today+"""%' 
            or timestamp like '"""+tag_yesterday+"""%')""",
            conn
        )

    def get_data_for_time_period(self):
        conn = get_db_conn()
        return pd.read_sql(
            """select * from weather where timestamp between 
            '"""+self.start_time+"""%' and '"""+self.end_time+"""%'""",
            conn
        )

    @property
    def start_time(self):
        """Return start of time window (pandas.Timestamp)"""
        return self._start_time

    @start_time.setter
    def start_time(self, period):
        self._start_time = (pd.Timestamp(period) - pd.Timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')

    @property
    def end_time(self):
        """Return end of time window (pandas.Timestamp)"""
        return self._end_time

    @end_time.setter
    def end_time(self, period):
        self._end_time = (pd.Timestamp(period) + pd.Timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    os.environ['WEATHERDBDRIVER'] = 'Microsoft Access Driver (*.mdb, *.accdb)'
    os.environ['WEATHERDB'] = "C:/ProgramData/WeatherHome/WeatherHome.mdb"
    conn = get_weather_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        """select * from Record"""
    )
    data = cursor.fetchall()
