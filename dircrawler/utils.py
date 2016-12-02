# -*- coding: utf-8 -*-

"""
dircrawler.utils

This module contains all utility functions used by dircrawler
"""

import os
from datetime import datetime
import time


def mod_ts_in_utc(filepath):
    t = os.path.getmtime(filepath)
    return datetime.utcfromtimestamp(t)


def file_contents(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath) as f:
        return f.read()


def datetime_to_timestamp(dt):
    return time.mktime(dt.timetuple())


def timestamp_to_datetime(ts):
    return datetime.fromtimestamp(ts)
