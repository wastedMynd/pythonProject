import os

from enum import Enum
from Downloader.Utils import human_readable as readable
from Downloader.Utils.log import Logging


class FileMime(Enum):
    MUSIC = "Music"
    VIDEOS = "Videos"
    COMPRESSED = "Compressed"
    PROGRAMS = "Programs"
    DOCUMENTS = "Documents"
    PICTURES = "Pictures"
    MISC = "misc"


@Logging
def _get_download_dir_path():
    """Returns the default downloads path for linux or windows."""
    return os.path.join(os.path.expanduser('~'), 'Downloads')


@Logging
def _get_resolved_file_mime_for(file_name):
    mime = FileMime.MISC

    your_file_extension = str(os.path.splitext(file_name)[1]).split('.')[1].lower()

    file_extension_dictionary = {
        FileMime.MUSIC.name: ['mp3', 'wav', 'wma', 'mpa', 'ram', 'ra', 'aac', 'aif', 'm4a', 'tsa'],
        FileMime.VIDEOS.name: ['avi', 'mpg', 'mpe', 'mpeg', 'asf', 'wmv', 'mov', 'qt', 'rm', 'mp4', 'flv', 'm4v',
                               'webm', 'ogv', 'ogg', 'mkv', 'ts', 'tsv'],
        FileMime.PICTURES.name: ['jpg', 'png', 'gif', 'webp', 'tiff', 'psd', 'raw', 'bmp', 'heif', 'indd', 'jpeg'],
        FileMime.DOCUMENTS.name: ['txt', 'csv', 'doc', 'pdf', 'ppt', 'pps', 'docx', 'pptx', 'py', 'java', 'c', 'class',
                                  'cpp', 'cs', 'h', 'pl', 'sh', 'html'],
        FileMime.PROGRAMS.name: ['exe', 'msi', 'deb', 'apk'],
        FileMime.COMPRESSED.name: ['zip', 'rar', 'arj', 'gz', 'sit', 'sitx', 'sea', 'ace', 'bz2', '7z']
    }

    mime_found = False
    for file_extension_key, file_extensions in file_extension_dictionary.items():

        if mime_found:
            break

        for file_extension in file_extensions:
            if your_file_extension == file_extension:
                mime = FileMime[file_extension_key]
                mime_found = True
                break

    return mime


@Logging
def get_download_dir_for(official_filename):
    mime = _get_resolved_file_mime_for(official_filename)

    path = os.path.join(_get_download_dir_path(), mime.value)

    return path


@Logging
def create_folder_for(official_filename):
    path_to_official_filename = get_download_dir_for(official_filename)

    if not os.path.exists(path_to_official_filename):
        os.makedirs(path_to_official_filename)

    return path_to_official_filename


@Logging
def get_temp_folder(official_filename):
    official_content_file_name, content_file_name, content_type \
        = readable.get_content_file_name_and_type(official_filename)

    mime_path = create_folder_for(official_content_file_name)

    content_temp_dir = os.path.join(mime_path, content_file_name)

    return content_temp_dir


@Logging
def create_temp_folder_for(official_filename):
    content_temp_dir = get_temp_folder(official_filename)

    try:
        os.mkdir(content_temp_dir)
    except FileExistsError:
        print("{}\r".format(f"path exists {content_temp_dir}"), end="")

    return content_temp_dir

