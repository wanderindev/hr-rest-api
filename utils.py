from datetime import datetime, time

def get_time(time_str):
    if time_str:
        return datetime.strptime(time_str, '%H:%M:%S').time()