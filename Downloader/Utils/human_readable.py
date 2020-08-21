import os
import time
import Utils.log as log


def format_bytes(size):
    # region setup logs
    log.log_code_region("start-of format_bytes", allow_display=False)
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

    display_bytes = f" {round(size, 2)}{power_labels[power_label_key]}B "
    # endregion

    # region display resultant logs
    log.log_current_datetime(log.log_elapsed_time(log_start_time, f"format_bytes={display_bytes}",
                                                  allow_display=False), allow_display=False)

    log.log_code_region("end-of format_bytes", allow_display=False)
    # endregion

    return display_bytes


def official_file_name(self, on_path):
    # region setup logs
    log.log_code_region("start-of official_file_name", allow_display=False)
    log_start_time = time.time()
    # endregion

    # region type your code, below this...
    official_content_file_name = os.path.basename(on_path)
    # endregion

    # region display resultant logs

    log.log_current_datetime(log.log_elapsed_time(log_start_time, "official_file_name",
                                                  allow_display=False), allow_display=False)
    log.log_code_region("end-of official_file_name", allow_display=False)

    # endregion

    return official_content_file_name


def get_content_file_name_and_type(on_path):
    log.log_code_region("start-of get_content_file_name_and_type", allow_display=False)
    startTime = time.time()

    # if e.g url = temp/file.txt, and official_content_file_name = file.txt; after this...
    official_content_file_name = official_file_name(on_path)
    log.log_current_datetime(f"Official-Content-File-Name:{official_content_file_name}")

    # because I'm interested in separating the file from .txt, this does it.
    file_and_ext_holder = os.path.splitext(official_content_file_name)

    # e.g content_file_name = file;
    content_file_name = file_and_ext_holder[0]
    log.log_current_datetime(f"Content-File-Name:{content_file_name}")

    # and the content_type, will equal to, e.g content_type = txt
    content_type = file_and_ext_holder[1][1:]
    log.log_current_datetime(f"Content-Type:{content_type}")

    log.log_current_datetime(log.log_elapsed_time(startTime, "Content FileName, and Type Query",
                                                  allow_display=False), allow_display=False)
    log.log_code_region("end-of get_content_file_name_and_type", allow_display=False)

    return official_content_file_name, content_file_name, content_type


def get_content_length_from_url(url):
    log.log_code_region("start-of get_content_length", allow_display=False)
    start_query_time = time.time()

    try:
        import urllib
        with urllib.request.urlopen(url) as meta:
            content_length = int(dict(meta.getheaders())["Content-Length"])
            log.log_current_datetime(f"Content-Length:{format_bytes(content_length)}")
    except urllib.error.HTTPError:
        content_length = 0

    log.log_current_datetime(log.log_elapsed_time(start_query_time, "Querying", allow_display=False),
                             allow_display=False)
    log.log_code_region("end-of get_content_length", allow_display=False)

    return content_length
