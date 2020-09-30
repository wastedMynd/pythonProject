import os
import urllib
import requests

from Downloader.Utils import log
from Downloader.Utils.log import Logging


@Logging
def format_bytes(size):
    power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T', 5: 'P'}
    power = 2 ** 10  # 2**10 = 1024
    power_label_key = 0

    while size >= power:
        size /= power
        if power_label_key < len(power_labels):
            power_label_key += 1

    display_bytes = f" {round(size, 2)}{power_labels[power_label_key]}B "

    return display_bytes


@Logging
def is_url_link_valid(url):
    is_url_link_pattern_valid = False

    message = "You entered an invalid Address/URL link!"
    if not len(url):
        print(message)
        return is_url_link_pattern_valid

    try:
        print("validating...your provided latest_draw_result_url address: {} ".format(url))
        with requests.get(url) as response:
            is_url_link_pattern_valid = response.status_code == (200 or 206)

            message = "You entered a valid Address/URL link and exists on the internet." \
                if is_url_link_pattern_valid else message

        print(message)

    except requests.ConnectionError:
        print(message)

    return is_url_link_pattern_valid


@Logging
def official_file_name(on_path):
    return os.path.basename(on_path)


@Logging
def get_content_file_name_and_type(on_path):
    # if e.g latest_draw_result_url = temp/file.txt, and official_content_file_name = file.txt; after this...
    official_content_file_name = official_file_name(on_path)

    # because I'm interested in separating the file from .txt, this does it.
    file_and_ext_holder = os.path.splitext(official_content_file_name)

    # e.g content_file_name = file;
    content_file_name = file_and_ext_holder[0]

    # and the content_type, will equal to, e.g content_type = txt
    content_type = file_and_ext_holder[1][1:]

    return official_content_file_name, content_file_name, content_type


@Logging
def get_content_length_from_url(url):
    try:
        with urllib.request.urlopen(url) as meta:
            content_length = int(dict(meta.getheaders())["Content-Length"])
            log.current_datetime(f"Content-Length:{format_bytes(content_length)}")
    except urllib.error.HTTPError:
        content_length = 0

    return content_length
