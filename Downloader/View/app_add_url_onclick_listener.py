import tkinter
from functools import partial
from tkinter import *
from Downloader.Utils.human_readable import is_url_link_valid
from Downloader.Utils.log import Logging
import threading


@Logging
def on_click_add_url_listener(add_url_to_list):
    add_url_screen_dialog_title = 'Enter New Address/URL link To Download'

    add_url_dialog_window = Tk()

    # region add_url_dialog_window properties
    add_url_dialog_window.title(add_url_screen_dialog_title)
    add_url_dialog_window_width = 557
    add_url_dialog_window_height = 75
    add_url_dialog_window_geometry = f"{add_url_dialog_window_width}x{add_url_dialog_window_height}"
    add_url_dialog_window.geometry(add_url_dialog_window_geometry)
    add_url_dialog_window.resizable(0, 0)

    # endregion

    # region add_url dialog window's : on_click functions
    @Logging
    def download_url_address_on_click_listener(dialog_window, url_entry):
        url_to_download = url_entry.get()

        if len(url_to_download) == 0:
            return "You entered an invalid Address/URL link"

        print(f"Address or URL link, to Download : {url_to_download}")

        # todo add functionality
        def validate():
            if not is_url_link_valid(url_to_download):
                return

            dialog_window.destroy()

            print("download started...")
            add_url_to_list(url_to_download)

        thread = threading.Thread(target=validate)
        thread.start()

        pass

    # endregion

    frame_dialog_1 = tkinter.Frame(add_url_dialog_window, relief='ridge')
    frame_dialog_1.grid(column=0, row=0, padx=15, sticky="nsew")
    # region frame_dialog_1 widgets

    # region Address/URL link Label
    address_label_text = 'Address/URL link'
    address_label = Label(frame_dialog_1, text=address_label_text, padx=5, pady=5)
    address_label.grid(row=0, column=0)
    # endregion

    # region Address/URL link Entry
    url_address_link_to_download_entry_hint_text = 'Enter a "URL Address link"; to download from...'
    url_address_link_to_download_entry_width = 50
    url_address_link_to_download_entry = Entry(
        frame_dialog_1,
        text=url_address_link_to_download_entry_hint_text,
        width=url_address_link_to_download_entry_width
    )
    url_address_link_to_download_entry.grid(row=0, column=1)
    # endregion

    # endregion

    frame_dialog_2 = tkinter.Frame(add_url_dialog_window, relief='ridge')
    frame_dialog_2.grid(column=0, row=1, padx=15, sticky="nsew")
    # region frame_dialog_2 widgets

    # region OK submit Button
    address_submit_button_text = 'OK'
    address_submit_button = Button(
        frame_dialog_2,
        width=10,
        padx=10,
        pady=5,
        text=address_submit_button_text,
        command=partial(
            download_url_address_on_click_listener,
            add_url_dialog_window,
            url_address_link_to_download_entry
        )
    )
    address_submit_button.pack(side=RIGHT)
    # endregion

    # region Cancel Button
    address_cancel_button_text = 'Cancel'
    address_cancel_button = Button(
        frame_dialog_2,
        width=10,
        pady=5,
        text=address_cancel_button_text,
        command=lambda: add_url_dialog_window.destroy()
    )
    address_cancel_button.pack(side=RIGHT)
    # endregion

    # endregion

    add_url_dialog_window.mainloop()

    pass
