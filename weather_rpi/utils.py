#!/usr/bin/env python3
"""
Created on 2021-11-21 12:33

@author: johannes
"""
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta


TIME_STRING_FMT: str = '%Y-%m-%d %H:%M:%S'
DATE_STRING_FMT: str = '%Y-%m-%d'


def get_file_logger(logger_name: str = "log_session"):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    file_handler = TimedRotatingFileHandler(f"{logger_name}.log", when="MIDNIGHT")
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s: %(message)s',
        datefmt='%Y-%b-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


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
