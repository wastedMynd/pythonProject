from enum import Enum
from Downloader.Utils import human_readable as readable


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

    def __str__(self):
        return f"""
        DownloadThreadInfo:\n\t\t\t
        Thread:{self.id}\n\t\t\t
        Url:{self.url}\n\t\t\t
        Official Filename:{self.official_name}\n\t\t\t
        Temp Filename:{self.content_file_name}\n\t\t\t
        Download Content Bytes:{readable.format_bytes(self.maxByte)}\n\t\t\t
        Start Byte(s):{readable.format_bytes(self.fromByte)}\n\t\t\t
        End Byte(s):{readable.format_bytes(self.toByte)}\n\t\t\t
        Thread Will Attempt to download Bytes:{readable.format_bytes(self.thread_byte_contract)}\n\t\t\t
        Did Thread Download:{"Yes" if self.did_download else "No"}\n\t\t\t
        Did Thread Stitch:{"Yes" if self.did_stitch else "No"}\n\t\t\t
        Thread Status:{self.thread_status.name}\n
        """

    def on_change_thread_status(self, to_thread_status):
        self.thread_status = to_thread_status
        self.thread_status_progression.append(to_thread_status)

    pass
