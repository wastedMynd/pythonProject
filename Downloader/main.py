# region imports

import datetime
import os
import threading
import time
import urllib
from enum import Enum
import random
from shutil import copyfileobj
from tempfile import NamedTemporaryFile

import requests

import Utils.log as log
import Utils.human_readable as readable


# endregion



# region sample url links, for testing...

# link = "https://releases.ubuntu.com/18.04/ubuntu-18.04.4-desktop-amd64.iso"
# link = "https://files03.tchspt.com/temp/MicrosoftEdgeStableSetup.msi"
# link = "http://mirrors.evowise.com/linuxmint/debian/lmde-4-cinnamon-32bit.iso"


# region sample url link; to 10MB MP4, test file
link = "https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_1280_10MG.mp4"


# endregion

# endregion

# region App Interface Demo Config : GUI, UX Design walk-through

def start_download(download_from_url_links):
    logreg("start-of start_download")
    startDownloadTime = time.time()

    threads, download_threads_info = Downloader().get_download_threads(download_from_url_links)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    for download_thread_info in download_threads_info:
        status_progression = ""
        for status in download_thread_info.thread_status_progression:
            status_progression = status.name if status_progression == '' else f'{status_progression}, {status.name}'
        logtime(f"Thread:{download_thread_info.id}, progression history {status_progression}", allow_display=False)

    logtime(logelap(startDownloadTime, "Download", allow_display=False))

    stitching_thread = threading.Thread(target=stitch_temp_files, args=[download_threads_info])
    stitching_thread.start()
    stitching_thread.join()

    logreg("end-of start_download")
    pass


def stitch_temp_files(download_threads_info):
    logreg("start-of stitch_temp_files", allow_display=False)
    start_time = time.time()

    complete_downloaded_file_name = download_threads_info[0].official_name

    is_complete_downloaded_file_stitched = True

    with open(complete_downloaded_file_name, "a+b") as complete_downloaded_file:
        chunk_size = 1
        for download_thread_info in download_threads_info:
            if not download_thread_info.did_download:
                continue
            try:
                with open(download_thread_info.content_file_name, "rb") as temp_file:
                    chunk = temp_file.read(chunk_size)
                    while chunk:
                        complete_downloaded_file.write(bytes(chunk))
                        chunk = temp_file.read(chunk_size)

                    download_thread_info.did_stitch = True
            except IOError:
                print(f"{download_thread_info.content_file_name} did not Stitch!")

    for download_thread_info in download_threads_info:
        if not download_thread_info.did_stitch:
            is_complete_downloaded_file_stitched = False
            break
        else:
            os.remove(download_thread_info.content_file_name)

    message = "Completed File Stitching, File Now Available" if is_complete_downloaded_file_stitched \
        else "File Stitching, Failed! File is Not Usable"
    logtime(logelap(start_time, message, allow_display=False))
    logreg("end-of stitch_temp_files", allow_display=False)
    pass


def run_download(download_from_url_link):
    thread = threading.Thread(target=start_download, args=[download_from_url_link])
    thread.start()


try:
    run_download(link)
except urllib.error.URLError:
    logtime("No Internet Connection!!")

# endregion
