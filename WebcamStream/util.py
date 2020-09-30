import time


def get_elapsed_time(start_time):
    return time.strftime(" Elapsed Time %H:%M:%S", time.gmtime(time.time() - start_time))


def get_current_time():
    return {
        "today_date": time.strftime("%Y-%m-%d"),
        "today_weekday": time.strftime("%a"),
        "today_time": time.strftime("%Hh%M")
    }


def get_time_string(start_time=time.time()):
    current_time = get_current_time()
    current_time_display = f'{current_time["today_weekday"]} {current_time["today_date"]} {current_time["today_time"]}'
    elapsed_time_display = get_elapsed_time(start_time)
    return current_time_display if elapsed_time_display != "00:00:00" else current_time_display + elapsed_time_display
