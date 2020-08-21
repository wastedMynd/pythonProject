import os
import random
import threading
import requests
from Downloader.FileDownload.download_thread_info import DownloadThreadInfo
from Downloader.Utils import log
from Downloader.Utils import file
from Downloader.Utils import human_readable as readable
from Downloader.Utils.log import Logging


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

    def download(self, download_thread_info):
        currentFileSize = 0

        # region check if Server can Resume Download; by Updating the Headers {'Range': 'byte= interruptPoint -
        # endPoint'}

        if os.path.exists(download_thread_info.content_file_name):
            log.current_datetime(f"Thread:{download_thread_info.id} temp file exists")
            currentFileSize = os.stat(download_thread_info.content_file_name).st_size

            if currentFileSize > 0:  # Interrupted Multi threaded download; start from byte; altered to currentFileSize.
                download_thread_info.fromByte = currentFileSize
                self.headers.update({'Range': f'bytes={currentFileSize}-{download_thread_info.toByte}'})
                str_from = readable.format_bytes(currentFileSize)
                str_to = readable.format_bytes(download_thread_info.toByte)
                message = f"temp file will resume...at bytes={str_from}-{str_to}"
                log.current_datetime(message, allow_display=False)

            if currentFileSize == download_thread_info.toByte:
                download_thread_info.on_change_thread_status(
                    DownloadThreadInfo.DownloadThreadStatus.NOT_ALLOWED_TO_PRECESS_TASK)
        # endregion

        isThreadAllowedToDownload = not (download_thread_info.thread_status
                                         == DownloadThreadInfo.DownloadThreadStatus.NOT_ALLOWED_TO_PRECESS_TASK)

        if isThreadAllowedToDownload:
            # region send a request to download file...
            with requests.request('GET', download_thread_info.url, headers=self.headers) as site:

                isThreadAllowedToDownload = (site.status_code == 206 or site.status_code == 200)

                if isThreadAllowedToDownload:
                    if currentFileSize > 0 and site.status_code == 206:  # Resuming Thread

                        log.current_datetime(f"""
                            Thread:{download_thread_info.id}, temp file will resume...
                            at bytes={readable.format_bytes(currentFileSize)}-{readable.format_bytes(
                            download_thread_info.toByte)}
                        """, allow_display=False)

                        self.headers.update({'Range': f'bytes={currentFileSize}-{download_thread_info.toByte}'})

                        download_thread_info.on_change_thread_status(
                            DownloadThreadInfo.DownloadThreadStatus.RESUMING)

                    elif self.downloadCounter >= 0 and site.status_code == 206:  # Multi-Threaded

                        log.current_datetime(f"Thread:{download_thread_info.id}, temp file will be created...",
                                             allow_display=False)

                    elif self.downloadCounter == 0 and site.status_code == 200:  # Single-Threaded
                        # New Single thread, start from byte; altered to origin.
                        log.current_datetime(f"Thread:{download_thread_info.id}, temp file will be created...",
                                             allow_display=False)
                        download_thread_info.fromByte = 0
                        download_thread_info.toByte = download_thread_info.maxByte
                        self.headers.update(
                            {'Range': f'bytes={download_thread_info.fromByte}-{download_thread_info.toByte}'})

                    fromByte = download_thread_info.fromByte
                    toByte = download_thread_info.toByte

                    message_byte_range = f"{readable.format_bytes(fromByte)}-{readable.format_bytes(toByte)}"
                    message = f"Thread:{download_thread_info.id}, temp file will start at... bytes={message_byte_range}"
                    log.current_datetime(message, allow_display=False)

                    self.headers.update({'Range': f'bytes={fromByte}-{toByte}'})
                    self.downloadCounter += 1

                    message = f"Thread:{download_thread_info.id}, is allowed to download"
                    log.current_datetime(message, allow_display=False)

                    total = toByte - fromByte
                    chunkCount = 0

                    # region Downloading in-progress..
                    try:
                        download_thread_info.on_change_thread_status(
                            DownloadThreadInfo.DownloadThreadStatus.PROCESSING_TASK)

                        temp_folder = file.create_temp_folder_for(download_thread_info.official_name)
                        temp_file = download_thread_info.content_file_name
                        temp_folder = os.path.join(temp_folder, temp_file)

                        with open(temp_folder, "a+b") as f:
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
                                    DownloadThreadInfo.DownloadThreadStatus.DONE)

                            except IOError:
                                download_thread_info.did_download = False
                                status = DownloadThreadInfo.DownloadThreadStatus.INTERRUPTED
                                download_thread_info.on_change_thread_status(status)

                    except IOError:
                        download_thread_info.did_download = False
                        status = DownloadThreadInfo.DownloadThreadStatus.INTERRUPTED
                        download_thread_info.on_change_thread_status(status)

                    # endregion

                else:
                    status = DownloadThreadInfo.DownloadThreadStatus.NOT_ALLOWED_TO_PRECESS_TASK
                    download_thread_info.on_change_thread_status(status)
                    message = f"Thread:{download_thread_info.id} is not allowed to download!"
                    log.current_datetime(message)
            #  endregion
        pass

    def get_download_threads(self, url, thread_count=16):
        threads = []

        official_file_name, content_file_name, content_mime = readable.get_content_file_name_and_type(url)
        content_length = readable.get_content_length_from_url(url)

        eachThreadMustDownloadContentLength = int(content_length / thread_count)
        log.current_datetime(f'Range: bytes= 0B - {readable.format_bytes(eachThreadMustDownloadContentLength)}',
                             allow_display=False)
        self.headers.update({'Range': f'bytes=0-{eachThreadMustDownloadContentLength}'})

        with requests.request('GET', url, headers=self.headers) as site:
            isMultiThreadingDownloadAllowed = (site.status_code == 206 and thread_count > 1)
            isSingleThreadingDownloadAllowed = site.status_code == 200

            if not isMultiThreadingDownloadAllowed and not isSingleThreadingDownloadAllowed:
                raise AssertionError(f"Server Status not supported {site.status_code}")  # 416 Range Not Satisfiable

        message = "MultiThreading Allowed!" if isMultiThreadingDownloadAllowed else "Single Threading Allowed!"
        log.current_datetime(message)

        if isSingleThreadingDownloadAllowed:
            eachThreadMustDownloadContentLength = content_length
            self.headers.update({'Range': f'bytes=0-{eachThreadMustDownloadContentLength}'})

        thread_count = thread_count if isMultiThreadingDownloadAllowed else 1
        downloadThreadsInfo = []

        try:
            if isMultiThreadingDownloadAllowed:
                for current_thread_id in range(thread_count):
                    downloadThread = DownloadThreadInfo(url, current_thread_id, content_file_name, content_mime,
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

                    downloadThread.on_change_thread_status(DownloadThreadInfo.DownloadThreadStatus.INITIALIZING)
                    downloadThreadsInfo.append(downloadThread)
                    threads.append(threading.Thread(target=self.download, args=[downloadThread]))

            elif isSingleThreadingDownloadAllowed:
                downloadThread = DownloadThreadInfo(url, thread_count - 1, content_file_name, content_mime,
                                                    content_length, eachThreadMustDownloadContentLength)
                downloadThread.fromByte = 0
                downloadThread.toByte = content_length

                downloadThread.on_change_thread_status(DownloadThreadInfo.DownloadThreadStatus.INITIALIZING)
                downloadThreadsInfo.append(downloadThread)
                threads.append(threading.Thread(target=self.download, args=[downloadThread]))

        except ZeroDivisionError:
            print("Download partition thread failed!")
        return threads, downloadThreadsInfo
