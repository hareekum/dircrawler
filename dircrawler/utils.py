import os
import datetime


def mod_ts_in_utc(filepath):
    t = os.path.getmtime(filepath)
    return datetime.datetime.utcfromtimestamp(t)


def file_contents(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath) as f:
        return f.read()
