from time import time, mktime
from datetime import timedelta, datetime

def generate_timestamp (delta : int) -> int :

    now_timestamp = datetime.fromtimestamp(time())
    now_timestamp += timedelta(hours = delta)

    return mktime(now_timestamp.timetuple())

