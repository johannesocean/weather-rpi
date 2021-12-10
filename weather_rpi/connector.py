#!/usr/bin/env python3
"""
Created on 2021-11-20 23:07

@author: johannes
"""
import os
import sqlite3
import pyodbc
import pandas as pd


class WeatherStationDB:
    """Doc."""

    def __init__(self):
        self.conn = pyodbc.connect(
            DRIVER=os.getenv('WEATHERDBDRIVER'),
            DBQ=os.getenv('WEATHERDB')
        )

    def get(self):
        """Doc."""
        return pd.read_sql(self.query, self.conn)

    def get_recent_data(self, tag_today=None, tag_yesterday=None):
        """Doc."""
        return pd.read_sql(
            """select * from Record where (RecTime like '"""+tag_today+"""%' or RecTime like '"""+tag_yesterday+"""%')""",
            self.conn
        )

    @property
    def query(self):
        # return """select * from Record where (RecTime like '"""+self.start_time+"""%')"""
        # return """select * from Record"""
        return """select * from Record where (RecTime like '2021-10-20%' or RecTime like '2021-11-21%')"""


class RpiDB:
    """Doc."""

    def __init__(self):
        self.conn = sqlite3.connect(os.getenv('UTMDB'))

    def post(self, data):
        """Doc."""
        data.to_sql('weather', self.conn, if_exists='append', index=False)

    def get(self):
        """Doc."""
        return pd.read_sql('select * from weather', self.conn)

    def get_last_timestamp(self):
        """Doc."""
        return pd.read_sql(
            'select timestamp from weather order by rowid desc limit 1', self.conn
        )['timestamp'][0]

    def get_time_log(self):
        """Doc."""
        query = """select timestamp from weather"""
        return pd.read_sql(query, self.conn)

    def get_recent_time_log(self, tag_today=None, tag_yesterday=None):
        """Doc."""
        return pd.read_sql(
            """select timestamp from weather where (timestamp like '"""+tag_today+"""%' 
            or timestamp like '"""+tag_yesterday+"""%')""",
            self.conn
        )
