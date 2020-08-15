import time
import datetime


# region utility functions

# region log functions: log_elapsed_time, log_current_datetime, log_code_region

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


# endregion

# region byte format, human readable byte number representation
def format_bytes(size):

    # region setup logs
    log_code_region("start-of format_bytes", allow_display=False)
    log_start_time = time.time()
    # endregion

    # region type your code, below this...

    power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T', 5: 'P'}
    power = 2 ** 10  # 2**10 = 1024
    power_label_key = 0

    while size >= power:
        size /= power
        if power_label_key < len(power_labels):
            power_label_key += 1

    power_label_key = len(power_labels) - 1 if power_label_key > len(power_labels) - 1 else power_label_key

    display_bytes = f" {round(size, 2)}{power_labels[power_label_key]}B "
    # endregion

    # region display resultant logs
    log_current_datetime(log_elapsed_time(log_start_time, f"format_bytes={display_bytes}", allow_display=False),
                         allow_display=False)
    log_code_region("end-of format_bytes", allow_display=False)
    # endregion

    return display_bytes

# endregion

# endregion
