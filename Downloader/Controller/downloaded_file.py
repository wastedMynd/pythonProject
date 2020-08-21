import os
import time
from Downloader.Utils import log, file
from Downloader.Utils.human_readable import get_content_length_from_url
from Downloader.Utils.log import Logging


@Logging
def stitch_temp_files(download_threads_info):
    start_time = time.time()

    complete_downloaded_file_name = download_threads_info[0].official_name

    path_to_stitch = os.path.join(file.get_download_dir_for(complete_downloaded_file_name),
                                  complete_downloaded_file_name)

    temp_folder = file.get_temp_folder(download_threads_info[0].official_name)

    with open(path_to_stitch, "a+b") as complete_downloaded_file:
        chunk_size = 1
        for download_thread_info in download_threads_info:
            temporal_file = download_thread_info.content_file_name
            temporal_file_path =os.path.join(temp_folder, temporal_file)
            if not download_thread_info.did_download:
                continue
            try:
                with open(temporal_file_path, "rb") as temp_file:
                    chunk = temp_file.read(chunk_size)
                    while chunk:
                        complete_downloaded_file.write(bytes(chunk))
                        chunk = temp_file.read(chunk_size)

                    download_thread_info.did_stitch = True

                os.remove(temporal_file_path)
            except IOError:
                print(f"{download_thread_info.content_file_name} did not Stitch!")

    os.rmdir(temp_folder)

    downloaded_file_size = os.stat(path_to_stitch).st_size
    original_file_size = get_content_length_from_url(download_threads_info[0].url)

    is_complete_downloaded_file_stitched = downloaded_file_size >= original_file_size

    message = "Completed File Stitching, File Now Available" if is_complete_downloaded_file_stitched \
        else "File Stitching, Failed! File is Not Usable"
    log.current_datetime(log.elapsed_time(start_time, message))

    pass
