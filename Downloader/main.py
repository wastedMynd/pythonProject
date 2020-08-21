import threading
import time
import urllib

from Downloader.Controller.downloaded_file import stitch_temp_files
from Downloader.Controller.downloader import Downloader
from Downloader.Utils import log
from Downloader.Utils.log import Logging

# region sample url links, for testing...

# link = "https://releases.ubuntu.com/18.04/ubuntu-18.04.4-desktop-amd64.iso"
# link = "https://files03.tchspt.com/temp/MicrosoftEdgeStableSetup.msi"
# link = "http://mirrors.evowise.com/linuxmint/debian/lmde-4-cinnamon-32bit.iso"

# region sample url link; to 10MB MP4, test file
link = "https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_1280_10MG.mp4"


# endregion

# endregion

# region App Interface Demo Config: CLI walk-through

@Logging
def start_download(download_from_url_links, update_download_progress=None):
    startDownloadTime = time.time()

    threads, download_threads_info = Downloader() \
        .get_download_threads(download_from_url_links, update_download_progress=update_download_progress)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    for download_thread_info in download_threads_info:
        status_progression = ""
        for status in download_thread_info.thread_status_progression:
            status_progression = status.name if status_progression == '' else f'{status_progression}, {status.name}'
        log.current_datetime(f"Thread:{download_thread_info.id}, progression history {status_progression}",
                             allow_display=False)

    log.current_datetime(log.elapsed_time(startDownloadTime, __name__))

    stitching_thread = threading.Thread(target=stitch_temp_files, args=[download_threads_info])
    stitching_thread.start()
    stitching_thread.join()
    pass


@Logging
def run_main(download_from_url_link, update_download_progress=None):
    thread = threading.Thread(target=start_download, args=[download_from_url_link, update_download_progress])
    thread.start()
# endregion
