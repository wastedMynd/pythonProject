import time
import datetime
import logging
import os


def current_datetime(message, allow_display=True):
    log_current_datetime_ = f'{datetime.datetime.now()}, {message}\n'

    if allow_display:
        print("{}\r", end=f"{log_current_datetime_}")

    return log_current_datetime_


def elapsed_time(start_time, message):
    time_format = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
    log_elapsed_time_ = f"{message}, took {time_format} second(s); to complete."
    return log_elapsed_time_


class Logging(object):
    def __init__(self, your_function):
        self.your_function = your_function

        this_dir = os.path.abspath("log.py")
        parent_dir =os.path.dirname(this_dir)

        log_file = 'app.log'

        log_path = os.path.join(parent_dir, log_file)
        log_format = '%(asctime)s - %(message)s'
        logging.basicConfig(filename=log_path, filemode='w', format=log_format, level=logging.DEBUG)

    def __call__(self, *args, **kwargs):
        logging.debug(f"method: {self.your_function.__name__}, was invoked.")
        function = self.your_function(*args, **kwargs) if not kwargs == "" else self.your_function(*args)
        logging.debug(elapsed_time(time.time(), message=self.your_function.__name__))
        logging.debug(f"method: {self.your_function.__name__}, finished.\n")
        return function
