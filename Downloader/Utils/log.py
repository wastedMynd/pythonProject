import time
import datetime


def log_elapsed_time(start_time, message, allow_display=True):
    elapsed_time = time.time() - start_time
    time_format = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    log_elapsed_time_ = f"{message}, took {time_format} second(s); to complete.\n"

    if allow_display:
        print("{}\r", end=f"{log_elapsed_time_}")

    return log_elapsed_time_


def log_current_datetime(message, allow_display=True):
    log_current_datetime_ = f'{datetime.datetime.now()}, {message}\n'

    if allow_display:
        print("{}\r", end=f"{log_current_datetime_}")

    return log_current_datetime_


def log_code_region(region, allow_display=True):
    log_code_region_ = "#####" * 5 + f" {region} " + "#####" * 5 + "\n"

    if allow_display:
        print("{}\r", end=f"{log_code_region_}")

    return log_code_region_
