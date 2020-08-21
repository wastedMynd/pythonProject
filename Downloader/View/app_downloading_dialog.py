import multiprocessing
import threading
from tkinter import *
from tkinter.ttk import Progressbar

from Downloader.Utils.human_readable import official_file_name
from Downloader.main import start_download, run_main


def on_initialize_download(url):
    download_file_name = official_file_name(url)

    dialog = Tk()

    # region dialog_window properties
    dialog.title(' 0% ' + download_file_name)
    dialog_window_width = 557
    dialog_window_height = 75
    dialog_window_geometry = f"{dialog_window_width}x{dialog_window_height}"
    dialog.geometry(dialog_window_geometry)
    dialog.resizable(0, 0)
    # endregion

    progress_frame = Frame(dialog, relief='ridge')
    progress_frame.pack(side=TOP, fill='x')

    progress = Progressbar(progress_frame, orient=HORIZONTAL, length=100, mode='determinate')

    function_frame = Frame(dialog, relief='ridge')
    function_frame.pack(side=BOTTOM, fill='x')

    pause_button = Button(function_frame, text='Pause', command=lambda: pause_button_on_click_listener())
    pause_button.pack(side=LEFT)

    cancel_button = Button(function_frame, text='Cancel', command=lambda: dialog.destroy())
    cancel_button.pack(side=RIGHT)

    def update_download_progress(percentage, id=0):
        progress['value'] = percentage
        progress_frame.update_idletasks()

    thread = multiprocessing.Process(target=run_main, args=(url, update_download_progress))
    thread.start()

    def pause_button_on_click_listener():
        if pause_button['text'] == 'Pause':
            pause_button['text'] = 'Start'
            thread.terminate()
            print("Stopped!")
        else:
            pause_button['text'] = 'Pause'
            thread.start()
            print("Download Started...")

    dialog.mainloop()
