# region imports

import os
import threading
import random
import time
import urllib
from enum import Enum
from shutil import copyfileobj
from tempfile import NamedTemporaryFile
import requests
import datetime


# endregion

# region utility functions
def log_elapsed_time(start_time, message, allow_display=True):
    elapsed_time = time.time() - start_time
    time_format = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    log_elapsed_time_ = f"{message}, took {time_format} second(s); to complete.\n"

    if allow_display:
        print(log_elapsed_time_)

    return log_elapsed_time_


def log_current_datetime(message, allow_display=True):
    log_current_datetime_ = f'{datetime.datetime.now()}, {message}\n'

    if allow_display:
        print(log_current_datetime_)

    return log_current_datetime_


def log_code_region(region, allow_display=True):
    log_code_region_ = "#####" * 5 + f" {region} " + "#####" * 5 + "\n"

    if allow_display:
        print(log_code_region_)

    return log_code_region_


# endregion

class Downloader:
    downloadCounter = 0

    user_agent_list = [
        ('Mozilla/5.0 (X11; Linux x86_64) '
         'AppleWebKit/537.36 (KHTML, like Gecko) '
         'Chrome/57.0.2987.110 '
         'Safari/537.36'),  # chrome
        ('Mozilla/5.0 (X11; Linux x86_64) '
         'AppleWebKit/537.36 (KHTML, like Gecko) '
         'Chrome/61.0.3163.79 '
         'Safari/537.36'),  # chrome
        ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
         'Gecko/20100101 '
         'Firefox/55.0'),  # firefox
        ('Mozilla/5.0 (X11; Linux x86_64) '
         'AppleWebKit/537.36 (KHTML, like Gecko) '
         'Chrome/61.0.3163.91 '
         'Safari/537.36'),  # chrome
        ('Mozilla/5.0 (X11; Linux x86_64) '
         'AppleWebKit/537.36 (KHTML, like Gecko) '
         'Chrome/62.0.3202.89 '
         'Safari/537.36'),  # chrome
        ('Mozilla/5.0 (X11; Linux x86_64) '
         'AppleWebKit/537.36 (KHTML, like Gecko) '
         'Chrome/63.0.3239.108 '
         'Safari/537.36'),  # chrome
    ]

    # Pick a random user agent
    user_agent = random.choice(user_agent_list)

    headers = {"User-Agent": user_agent,
               'Accept-Language': 'en-US,en;q=0.5',
               'DNT': '1',
               'Connection': 'keep-alive',
               'Upgrade-Insecure-Requests': '1',
               'Range': 'byte=0-1024'
               }

    class DownloadThreadInfo:

        class DownloadThreadStatus(Enum):
            PENDING = 100
            INITIALIZING = 101
            NOT_ALLOWED_TO_PRECESS_TASK = 600
            RESUMING = 204
            PROCESSING_TASK = 250
            INTERRUPTED = 450
            DONE = 500

        def __init__(self, url, thread_id, file_name, mime, content_length, thread_byte_contract):
            log_code_region("DownloadThreadInfo __init__")
            log_current_datetime(f"Thread:{thread_id} constructing...")
            start_time = time.time()
            self.url = url
            self.official_name = f"{file_name}.{mime}"
            self.id = thread_id
            self.content_file_name = f"{thread_id}_{file_name}.{mime}"
            self.fromByte = 0
            self.toByte = 0
            self.thread_byte_contract = thread_byte_contract
            self.maxByte = content_length
            self.thread_status = self.DownloadThreadStatus.PENDING
            self.thread_status_progression = [self.thread_status]
            self.did_download = False
            self.did_stitch = False
            log_elapsed_time(start_time, f"{self.__str__()}, Created! ")
            log_code_region("end-of DownloadThreadInfo __init__")

        def __str__(self):
            return f"""
            DownloadThreadInfo:\n\t\t\t
            Thread:{self.id}\n\t\t\t
            Url:{self.url}\n\t\t\t
            Temp Filename:{self.content_file_name}\n\t\t\t
            Start Byte(s):{self.fromByte}\n\t\t\t
            End Byte(s):{self.toByte}\n\t\t\t
            Thread Will Attempt to download Bytes:{self.thread_byte_contract}\n\t\t\t
            Download Content Bytes:{self.maxByte}\n\t\t\t
            Did Thread Download:{self.did_download if "Yes" else "No"}\n\t\t\t
            Did Thread Stitch:{self.did_stitch if "Yes" else "No"}\n\t\t\t
            Thread Status:{self.thread_status}\n
            """

        def on_change_thread_status(self, to_thread_status):
            self.thread_status = to_thread_status
            self.thread_status_progression.append(to_thread_status)

        pass

    def download(self, download_thread_info):
        log_code_region("start-of download")
        log_current_datetime(f"function invoked, using download_thread_info={download_thread_info}")
        startTime = time.time()
        currentFileSize = 0

        # region check if Server can Resume Download; by Updating the Headers {'Range': 'byte= interruptPoint -
        # endPoint'}

        if os.path.exists(download_thread_info.content_file_name):
            print("temp file exists...")
            currentFileSize = os.stat(download_thread_info.content_file_name).st_size

            if currentFileSize > 0:  # Interrupted Multi threaded download; start from byte; altered to currentFileSize.
                download_thread_info.fromByte = currentFileSize
                print(f"temp file will resume... at bytes={currentFileSize}-{download_thread_info.toByte}")
                self.headers.update({'Range': f'bytes={currentFileSize}-{download_thread_info.toByte}'})

            if currentFileSize == download_thread_info.toByte:
                download_thread_info.on_change_thread_status(self.DownloadThreadInfo.
                                                             DownloadThreadStatus.NOT_ALLOWED_TO_PRECESS_TASK)
        # endregion

        isThreadAllowedToDownload = not (download_thread_info.thread_status
                                         == self.DownloadThreadInfo.DownloadThreadStatus.NOT_ALLOWED_TO_PRECESS_TASK)

        if isThreadAllowedToDownload:
            # region send a request to download file...
            with requests.request('GET', download_thread_info.url, headers=self.headers) as site:

                isMultiThreadingDownloadAllowed = (site.status_code == 206 and self.downloadCounter >= 0)

                isSingleThreadedDownloadAllowed = (site.status_code == 200 and self.downloadCounter == 0)

                isThreadAllowedToDownload = isMultiThreadingDownloadAllowed or isSingleThreadedDownloadAllowed

                if isThreadAllowedToDownload:

                    # region initialize Download Byte Range; for Interrupted, and new thread.

                    if self.downloadCounter == 0 and site.status_code == 200:  # Allowed for, Single threaded download.

                        download_thread_info.toByte = download_thread_info.maxByte

                        if currentFileSize > 0:  # Interrupted Single thread, end to bytes; altered to origin.
                            print(f"temp file will resume... at bytes={currentFileSize}-{download_thread_info.toByte}")
                            self.headers.update({'Range': f'bytes={currentFileSize}-{download_thread_info.toByte}'})
                            download_thread_info.on_change_thread_status(self.DownloadThreadInfo.
                                                                         DownloadThreadStatus.RESUMING)

                        else:  # New Single thread, start from byte; altered to origin.
                            print("temp file will be created...")
                            download_thread_info.fromByte = 0

                    fromByte = download_thread_info.fromByte
                    toByte = download_thread_info.toByte

                    print(f"temp file will start at... bytes={fromByte}-{toByte}")
                    self.headers.update({'Range': f'bytes={fromByte}-{toByte}'})
                    self.downloadCounter += 1

                    print(f"Thread:{download_thread_info.id} is allowed to download... status {site.status_code}")

                    total = toByte - fromByte
                    chunkCount = 0

                    # endregion

                    # region Downloading in-progress..
                    try:
                        download_thread_info.on_change_thread_status(
                            self.DownloadThreadInfo.DownloadThreadStatus.PROCESSING_TASK)
                        with open(download_thread_info.content_file_name, "wb") as f:
                            const_text = f'Thread:{download_thread_info.id} Downloading... {total} on '
                            try:
                                chunk_size = 8
                                for chunk in site.iter_content(chunk_size):
                                    chunkCount = chunkCount + chunk_size
                                    f.write(chunk)

                                    # region ux design suite for logging downloading progress...
                                    percentage = round(float(chunkCount) * (100.0 / total), 9)
                                    percentage_const = f"{chunkCount} @ {percentage}"
                                    dynamic_text = "{}%\r".format(percentage_const)
                                    print(const_text + dynamic_text, end="")
                                    # endregion

                                download_thread_info.did_download = True
                                download_thread_info.on_change_thread_status(
                                    self.DownloadThreadInfo.DownloadThreadStatus.DONE)

                            except IOError:
                                download_thread_info.did_download = False
                                download_thread_info.on_change_thread_status(self.DownloadThreadInfo.
                                                                             DownloadThreadStatus.INTERRUPTED)
                    except IOError:
                        download_thread_info.on_change_thread_status(self.DownloadThreadInfo.
                                                                     DownloadThreadStatus.INTERRUPTED)
                    # endregion
                else:
                    download_thread_info.on_change_thread_status(self.DownloadThreadInfo.
                                                                 DownloadThreadStatus.NOT_ALLOWED_TO_PRECESS_TASK)
                    print(f"Thread:{download_thread_info.id} is not allowed to download! status {site.status_code}")

            #  endregion

        # region log elapsed time for threads; that are allowed to download
        if isThreadAllowedToDownload:
            log_elapsed_time(startTime, f"Thread:{download_thread_info.id}")
        # endregion
        log_code_region("end-of download")
        pass

    def get_content_file_name_and_type(self, url):
        log_code_region("start-of get_content_file_name_and_type")
        log_current_datetime(f"function invoked, using param:url={url}")
        startTime = time.time()

        tempUrlSegs = url.split("/")

        tempUrlSegs_ = tempUrlSegs[len(tempUrlSegs) - 1].split(".")
        content_file_name = tempUrlSegs_[0]
        for i in range(1, len(tempUrlSegs_) - 1):
            content_file_name = f"{content_file_name}_{tempUrlSegs_[i]}"
        print(f"Content-File-Name:{content_file_name}")

        content_type = tempUrlSegs[len(tempUrlSegs) - 1].split(".")
        content_type = content_type[len(content_type) - 1]
        print(f"Content-Type:{content_type}")

        log_elapsed_time(startTime, "Content FileName, and Type Query")
        log_code_region("end-of get_content_file_name_and_type")
        return content_file_name, content_type

    def get_content_length(self, url):
        log_code_region("start-of get_content_length")
        log_current_datetime(f"function invoked, using param:url={url}")
        start_query_time = time.time()

        with urllib.request.urlopen(url) as meta:
            content_length = int(dict(meta.getheaders())["Content-Length"])
            print(f"Content-Length:{content_length}")

        log_elapsed_time(start_query_time, "Querying")
        log_code_region("end-of get_content_length")
        return content_length

    def get_download_threads(self, url, thread_count=2):
        log_code_region("start-of get_download_threads")
        log_current_datetime(f"function invoked, using param:url={url},thread_count={thread_count}")
        start_time = time.time()
        threads = []

        content_file_name, content_mime = self.get_content_file_name_and_type(url)
        content_length = self.get_content_length(url)

        with requests.request('GET', url, headers=self.headers) as site:

            isMultiThreadingDownloadAllowed = (site.status_code == 206 and self.downloadCounter >= 0)

            thread_count = thread_count if isMultiThreadingDownloadAllowed else 1

        downloadThreadsInfo = []

        try:
            eachThreadMustDownloadContentLength = content_length / thread_count

            if isMultiThreadingDownloadAllowed and thread_count > 1:
                for current_thread_id in range(thread_count):
                    downloadThread = self.DownloadThreadInfo(url, current_thread_id, content_file_name, content_mime,
                                                             content_length,
                                                             eachThreadMustDownloadContentLength)

                    if current_thread_id == 0:
                        downloadThread.fromByte = 0
                        downloadThread.toByte = eachThreadMustDownloadContentLength
                    else:
                        previous_thread_id = current_thread_id - 1
                        previousDownloadThread = downloadThreadsInfo[previous_thread_id]
                        downloadThread.fromByte = previousDownloadThread.toByte
                        downloadThread.toByte = downloadThread.fromByte + eachThreadMustDownloadContentLength

                    downloadThread.on_change_thread_status(self.DownloadThreadInfo.DownloadThreadStatus.INITIALIZING)
                    downloadThreadsInfo.append(downloadThread)
                    threads.append(threading.Thread(target=self.download, args=[downloadThread]))
            else:
                downloadThread = self.DownloadThreadInfo(url, thread_count - 1, content_file_name, content_mime,
                                                         content_length, eachThreadMustDownloadContentLength)
                downloadThread.fromByte = 0
                downloadThread.toByte = content_length

                downloadThread.on_change_thread_status(self.DownloadThreadInfo.DownloadThreadStatus.INITIALIZING)
                downloadThreadsInfo.append(downloadThread)
                threads.append(threading.Thread(target=self.download, args=[downloadThread]))

        except ZeroDivisionError:
            print("Download partition thread failed!")

        log_elapsed_time(start_time, "get_download_threads")
        log_code_region("end-of get_download_threads")
        return threads, downloadThreadsInfo


# region sample url links, for testing...

# link = "https://releases.ubuntu.com/18.04/ubuntu-18.04.4-desktop-amd64.iso"

# region sample url link; to 10MB MP4, test file
link = "https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_1280_10MG.mp4"


# endregion

# endregion

# region App Interface Demo Config : GUI, UX Design walk-through

def start_download(download_from_url_links):
    log_code_region("start-of start_download")
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
        print(f"Thread:{download_thread_info.id}, progression history {status_progression}")

    log_elapsed_time(startDownloadTime, "Download")

    stitch_temp_files(download_threads_info)

    log_code_region("end-of start_download")
    pass


def stitch_temp_files(download_threads_info):
    log_code_region("start-of stitch_temp_files")
    log_current_datetime(f"function invoked, using param:download_threads_info={download_threads_info}")
    start_time = time.time()

    complete_downloaded_file_name = download_threads_info[0].official_name

    is_complete_downloaded_file_stitched = True

    with open(complete_downloaded_file_name, "wb") as complete_downloaded_file:
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

    if is_complete_downloaded_file_stitched:
        log_current_datetime(
            log_elapsed_time(start_time, "Completed File Stitching, File Now Available", allow_display=False))
    else:
        log_current_datetime(
            log_elapsed_time(start_time, "File Stitching, Failed! File is Not Usable", allow_display=False))

    log_code_region("end-of stitch_temp_files")
    pass


def run_download(download_from_url_link):
    thread = threading.Thread(target=start_download, args=[download_from_url_link])
    thread.start()


try:
    run_download(link)
except urllib.error.URLError:
    print("No Internet Connection!!")

# endregion
