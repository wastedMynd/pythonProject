# region imports

import datetime
import os
import random
import threading
import time
import urllib
from enum import Enum
from shutil import copyfileobj
from tempfile import NamedTemporaryFile

import requests

from utils import log_elapsed_time as logelap,\
    log_current_datetime as logtime,\
    log_code_region as logreg,\
    format_bytes as formbytes


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
               'Range': 'bytes=0-0'
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

            logreg("DownloadThreadInfo __init__")
            logtime(f"Thread:{thread_id} constructing...")

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

            logtime(logelap(start_time, f"Thread:{thread_id}, creation", allow_display=False))
            logreg("end-of DownloadThreadInfo __init__")

        def __str__(self):
            return f"""
            DownloadThreadInfo:\n\t\t\t
            Thread:{self.id}\n\t\t\t
            Url:{self.url}\n\t\t\t
            Official Filename:{self.official_name}\n\t\t\t
            Temp Filename:{self.content_file_name}\n\t\t\t
            Download Content Bytes:{formbytes(self.maxByte)}\n\t\t\t
            Start Byte(s):{formbytes(self.fromByte)}\n\t\t\t
            End Byte(s):{formbytes(self.toByte)}\n\t\t\t
            Thread Will Attempt to download Bytes:{formbytes(self.thread_byte_contract)}\n\t\t\t
            Did Thread Download:{"Yes" if self.did_download else "No"}\n\t\t\t
            Did Thread Stitch:{"Yes" if self.did_stitch else "No"}\n\t\t\t
            Thread Status:{self.thread_status.name}\n
            """

        def on_change_thread_status(self, to_thread_status):
            self.thread_status = to_thread_status
            self.thread_status_progression.append(to_thread_status)

        pass

    def download(self, download_thread_info):
        logreg("start-of download",allow_display=False)
        startTime = time.time()
        currentFileSize = 0

        # region check if Server can Resume Download; by Updating the Headers {'Range': 'byte= interruptPoint -
        # endPoint'}

        if os.path.exists(download_thread_info.content_file_name):
            logtime(f"Thread:{download_thread_info.id} temp file exists")
            currentFileSize = os.stat(download_thread_info.content_file_name).st_size

            if currentFileSize > 0:  # Interrupted Multi threaded download; start from byte; altered to currentFileSize.
                download_thread_info.fromByte = currentFileSize
                self.headers.update({'Range': f'bytes={currentFileSize}-{download_thread_info.toByte}'})
                str_from = formbytes(currentFileSize)
                str_to = formbytes(download_thread_info.toByte)
                message = f"temp file will resume...at bytes={str_from}-{str_to}"
                logtime(message)

            if currentFileSize == download_thread_info.toByte:
                download_thread_info.on_change_thread_status(self.DownloadThreadInfo.
                                                             DownloadThreadStatus.NOT_ALLOWED_TO_PRECESS_TASK)
        # endregion

        isThreadAllowedToDownload = not (download_thread_info.thread_status
                                         == self.DownloadThreadInfo.DownloadThreadStatus.NOT_ALLOWED_TO_PRECESS_TASK)

        if isThreadAllowedToDownload:
            # region send a request to download file...
            with requests.request('GET', download_thread_info.url, headers=self.headers) as site:

                isThreadAllowedToDownload = (site.status_code == 206 or site.status_code == 200)

                if isThreadAllowedToDownload:
                    if currentFileSize > 0 and site.status_code == 206:  # Resuming Thread

                        logtime(f"""
                            Thread:{download_thread_info.id}, temp file will resume...
                            at bytes={formbytes(currentFileSize)}-{formbytes(download_thread_info.toByte)}
                        """)

                        self.headers.update({'Range': f'bytes={currentFileSize}-{download_thread_info.toByte}'})

                        download_thread_info.on_change_thread_status(self.DownloadThreadInfo.
                                                                     DownloadThreadStatus.RESUMING)

                    elif self.downloadCounter >= 0 and site.status_code == 206:  # Multi-Threaded

                        logtime(f"Thread:{download_thread_info.id}, temp file will be created...")

                    elif self.downloadCounter == 0 and site.status_code == 200:  # Single-Threaded
                        # New Single thread, start from byte; altered to origin.
                        logtime(f"Thread:{download_thread_info.id}, temp file will be created...")
                        download_thread_info.fromByte = 0
                        download_thread_info.toByte = download_thread_info.maxByte
                        self.headers.update(
                            {'Range': f'bytes={download_thread_info.fromByte}-{download_thread_info.toByte}'})

                    fromByte = download_thread_info.fromByte
                    toByte = download_thread_info.toByte

                    message_byte_range = f"{formbytes(fromByte)}-{formbytes(toByte)}"
                    message = f"Thread:{download_thread_info.id}, temp file will start at... bytes={message_byte_range}"
                    logtime(message)

                    self.headers.update({'Range': f'bytes={fromByte}-{toByte}'})
                    self.downloadCounter += 1

                    message = f"Thread:{download_thread_info.id}, is allowed to download"
                    logtime(message)

                    total = toByte - fromByte
                    chunkCount = 0

                    # endregion

                    # region Downloading in-progress..
                    try:
                        download_thread_info.on_change_thread_status(
                            self.DownloadThreadInfo.DownloadThreadStatus.PROCESSING_TASK)
                        with open(download_thread_info.content_file_name, "a+b") as f:
                            const_text = f'Thread:{download_thread_info.id} Downloading...'
                            try:
                                chunk_size = 8
                                for chunk in site.iter_content(chunk_size):
                                    chunkCount = chunkCount + chunk_size
                                    f.write(chunk)

                                    # region ux design suite for logging downloading progress...
                                    percentage = round(float(chunkCount) * (100.0 / total))
                                    percentage_const = f"{percentage}%"
                                    dynamic_text = "{}\r"
                                    print(dynamic_text, end=f"{const_text}{percentage_const}")
                                    # endregion

                                download_thread_info.did_download = True
                                download_thread_info.on_change_thread_status(
                                    self.DownloadThreadInfo.DownloadThreadStatus.DONE)

                            except IOError:
                                download_thread_info.did_download = False
                                status = self.DownloadThreadInfo.DownloadThreadStatus.INTERRUPTED
                                download_thread_info.on_change_thread_status(status)

                    except IOError:
                        download_thread_info.did_download = False
                        status = self.DownloadThreadInfo.DownloadThreadStatus.INTERRUPTED
                        download_thread_info.on_change_thread_status(status)

                    # endregion
                else:
                    status = self.DownloadThreadInfo.DownloadThreadStatus.NOT_ALLOWED_TO_PRECESS_TASK
                    download_thread_info.on_change_thread_status(status)
                    message = f"Thread:{download_thread_info.id} is not allowed to download!"
                    logtime(message)
            #  endregion

        # region log elapsed time for threads; that are allowed to download
        if isThreadAllowedToDownload:
            message = f"Thread:{download_thread_info.id}"
            logtime(logelap(startTime, message, allow_display=False), allow_display=False)
        # endregion
        logreg("end-of download",allow_display=False)
        pass

    def get_content_file_name_and_type(self, url):
        logreg("start-of get_content_file_name_and_type")
        startTime = time.time()

        # if e.g url = temp/file.txt, and official_content_file_name = file.txt; after this...
        official_content_file_name = os.path.basename(url)
        logtime(f"Official-Content-File-Name:{official_content_file_name}")

        # because I'm interested in separating the file from .txt, this does it.
        file_and_ext_holder = os.path.splitext(official_content_file_name)

        # e.g content_file_name = file;
        content_file_name = file_and_ext_holder[0]
        logtime(f"Content-File-Name:{content_file_name}", allow_display=False)

        # and the content_type, will equal to, e.g content_type = txt
        content_type = file_and_ext_holder[1][1:]
        logtime(f"Content-Type:{content_type}", allow_display=False)

        logtime(logelap(startTime, "Content FileName, and Type Query", allow_display=False))
        logreg("end-of get_content_file_name_and_type")
        return official_content_file_name, content_file_name, content_type

    def get_content_length(self, url):
        logreg("start-of get_content_length")
        start_query_time = time.time()

        try:
            with urllib.request.urlopen(url) as meta:
                content_length = int(dict(meta.getheaders())["Content-Length"])
                logtime(f"Content-Length:{formbytes(content_length)}")
        except urllib.error.HTTPError:
            content_length = 0

        logtime(logelap(start_query_time, "Querying", allow_display=False))
        logreg("end-of get_content_length")

        return content_length

    def get_download_threads(self, url, thread_count=16):
        logreg("start-of get_download_threads")
        logtime(f"function invoked, using param:url={url}  thread_count={thread_count}")
        start_time = time.time()
        threads = []

        official_file_name, content_file_name, content_mime = self.get_content_file_name_and_type(url)
        content_length = self.get_content_length(url)

        eachThreadMustDownloadContentLength = int(content_length / thread_count)
        logtime(f'Range: bytes=0-{formbytes(eachThreadMustDownloadContentLength)}')
        self.headers.update({'Range': f'bytes=0-{eachThreadMustDownloadContentLength}'})

        with requests.request('GET', url, headers=self.headers) as site:
            isMultiThreadingDownloadAllowed = (site.status_code == 206 and thread_count > 1)
            isSingleThreadingDownloadAllowed = site.status_code == 200

            if not isMultiThreadingDownloadAllowed and not isSingleThreadingDownloadAllowed:
                raise AssertionError(f"Server Status not supported {site.status_code}")  # 416 Range Not Satisfiable

        message = "MultiThreading Allowed!" if isMultiThreadingDownloadAllowed else "Single Threading Allowed!"
        logtime(message)

        if isSingleThreadingDownloadAllowed:
            eachThreadMustDownloadContentLength = content_length
            self.headers.update({'Range': f'bytes=0-{eachThreadMustDownloadContentLength}'})

        thread_count = thread_count if isMultiThreadingDownloadAllowed else 1
        downloadThreadsInfo = []

        try:
            if isMultiThreadingDownloadAllowed:
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
            elif isSingleThreadingDownloadAllowed:
                downloadThread = self.DownloadThreadInfo(url, thread_count - 1, content_file_name, content_mime,
                                                         content_length, eachThreadMustDownloadContentLength)
                downloadThread.fromByte = 0
                downloadThread.toByte = content_length

                downloadThread.on_change_thread_status(self.DownloadThreadInfo.DownloadThreadStatus.INITIALIZING)
                downloadThreadsInfo.append(downloadThread)
                threads.append(threading.Thread(target=self.download, args=[downloadThread]))
        except ZeroDivisionError:
            print("Download partition thread failed!")

        logtime(logelap(start_time, "get_download_threads", allow_display=False))
        logreg("end-of get_download_threads")
        return threads, downloadThreadsInfo


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
        logtime(f"Thread:{download_thread_info.id}, progression history {status_progression}")

    logtime(logelap(startDownloadTime, "Download", allow_display=False))

    stitching_thread = threading.Thread(target=stitch_temp_files, args=[download_threads_info])
    stitching_thread.start()
    stitching_thread.join()

    logreg("end-of start_download")
    pass


def stitch_temp_files(download_threads_info):
    logreg("start-of stitch_temp_files")
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
    logreg("end-of stitch_temp_files")
    pass


def run_download(download_from_url_link):
    thread = threading.Thread(target=start_download, args=[download_from_url_link])
    thread.start()


try:
    run_download(link)
except urllib.error.URLError:
    logtime("No Internet Connection!!")

# endregion
