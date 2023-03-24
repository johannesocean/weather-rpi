#!/usr/bin/env python3
"""
Created on 2021-11-20 23:07

@author: johannes
"""
import os
import sqlite3
import pandas as pd
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import text

#"access+pyodbc:///?odbc_connect=Driver=Microsoft Access Driver (*.mdb, *.accdb);Dbq=C:\ProgramData\WeatherHome\WeatherHome.mdb;"
engine = create_engine(os.getenv("DB_CONNECTION_STRING", "access+pyodbc:///?odbc_connect=Driver=Microsoft Access Driver (*.mdb, *.accdb);Dbq=C:\ProgramData\WeatherHome\WeatherHome.mdb;"))
metadata = MetaData()
table = Table("Record", metadata, autoload_with=engine)
columns = [c.name for c in table.columns]


def query_data(query, columns=None):
    with engine.connect() as conn:
        result = conn.execute(text(query))
        data = result.fetchall()
    return pd.DataFrame(data=data, columns=columns)


class WeatherStationDB:

    def __init__(self):
        self._columns = None

    def get(self):
        return query_data(self.query, columns=self.columns)

    def get_recent_data(self, tag_today=None, tag_yesterday=None):
        return query_data(
            """select * from Record where (RecTime like '"""+tag_today+"""%' or RecTime like '"""+tag_yesterday+"""%')""",
            columns=self.columns
        )

    def get_new_data(self, timetag=None):
        return query_data(
            """select * from Record where RecTime >= DateValue('"""+timetag+"""')""",
            columns=self.columns
        )

    @property
    def query(self):
        # return """select * from Record where (RecTime like '"""+self.start_time+"""%')"""
        return """select * from Record"""
        # return """select * from Record where (RecTime like '2021-10-20%' or RecTime like '2021-11-21%')"""

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, values):
        self._columns = values


def get_db_conn():
    """Doc."""
    return sqlite3.connect(os.getenv('UTMDB'))


class RpiDB:
    """Doc."""

    def __init__(self):
        pass

    @staticmethod
    def post(data):
        """Doc."""
        conn = get_db_conn()
        data.to_sql('weather', conn, if_exists='append', index=False)

    @staticmethod
    def get():
        """Doc."""
        conn = get_db_conn()
        return pd.read_sql('select * from weather', conn)

    @staticmethod
    def get_last_timestamp():
        """Doc."""
        conn = get_db_conn()
        return pd.read_sql(
            'select MAX(timestamp) as ts from weather', conn
        )['ts'][0]

    @staticmethod
    def get_time_log():
        """Doc."""
        conn = get_db_conn()
        query = """select timestamp from weather"""
        return pd.read_sql(query, conn)

    @staticmethod
    def get_recent_time_log(tag_today=None, tag_yesterday=None):
        """Doc."""
        conn = get_db_conn()
        return pd.read_sql(
            """select timestamp from weather where (timestamp like '"""+tag_today+"""%' 
            or timestamp like '"""+tag_yesterday+"""%')""",
            conn
        )

    def get_data_for_time_period(self):
        """Doc."""
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


if __name__ == "__main__":
    w = WeatherStationDB()
    w.columns = columns
