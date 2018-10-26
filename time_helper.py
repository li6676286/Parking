import  datetime,time

def now():
    return time.time()

def datetime_to_timestamp(dt):
    return time.mktime(dt.timetuple())