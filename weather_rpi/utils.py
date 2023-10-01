#!/usr/bin/env python3
"""
Created on 2021-11-21 12:33

@author: johannes
"""
import os
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta


TIME_STRING_FMT: str = '%Y-%m-%d %H:%M:%S'
DATE_STRING_FMT: str = '%Y-%m-%d'


class Log:

    def __init__(self, log_directory=None):
        """Initialize."""
        if log_directory:
            if not os.path.exists(log_directory):
                os.mkdir(log_directory)

            self.log_path = os.path.join(
                log_directory, 'log_session_{}.txt'.format(datetime.now().strftime('%Y%m%d%H%M%S'))
            )
            with open(self.log_path, "w") as file:
                file.write('{}\n= Log session initialized: {} =\n{}\n'.format(
                    '='*48, self.time_now, '='*48
                ))
        else:
            self.log_path = None

    def write(self, head, message):
        """Write."""
        if self.log_path:
            with open(self.log_path, "a") as file:
                file.write('{}: {} - {}\n'.format(self.time_now, head, message))
        else:
            print('No logfile to write to? log_directory was not given at init. Sad face..')

    @property
    def time_now(self):
        """Return time."""
        return get_now_timestring()


def round_value(value, nr_decimals=3):
    return float(Decimal(str(value)).quantize(
        Decimal('%%1.%sf' % nr_decimals % 1),
        rounding=ROUND_HALF_UP)
    )


def get_base_folder():
    return os.path.dirname(os.path.realpath(__file__))


def get_now_timestring():
    return datetime.now().strftime(TIME_STRING_FMT)


def get_today_timestring():
    return datetime.now().strftime(DATE_STRING_FMT)


def get_yesterday_timestring():
    return (datetime.now() - timedelta(days=1)).strftime(DATE_STRING_FMT)
