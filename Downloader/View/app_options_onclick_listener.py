import tkinter
from tkinter import *
from tkinter import ttk
from Downloader.Utils.log import Logging


@Logging
def on_click_options_listener():
    options_dialog = Tk()

    # region options_dialog properties
    options_dialog_title = 'Configuration'
    options_dialog.title(options_dialog_title)
    options_dialog_width = 700
    options_dialog_height = 510
    options_dialog_geometry = f"{options_dialog_width}x{options_dialog_height}"
    options_dialog.geometry(options_dialog_geometry)
    options_dialog.resizable(0, 0)
    # endregion

    options_dialog_frame0 = tkinter.Frame(options_dialog, borderwidth=2, relief='ridge')
    options_dialog_frame0.pack(side=TOP, fill='both', expand=1)
    # region options_dialog_frame0 widgets
    tabControl = ttk.Notebook(options_dialog_frame0)

    connection_tab = ttk.Frame(tabControl)
    file_types_tab = ttk.Frame(tabControl)
    save_to_tab = ttk.Frame(tabControl)
    general_tab = ttk.Frame(tabControl)
    sounds_tab = ttk.Frame(tabControl)
    dial_up_vpn_tab = ttk.Frame(tabControl)
    sites_logins_tab = ttk.Frame(tabControl)
    proxy_socks_tab = ttk.Frame(tabControl)

    tabControl.add(connection_tab, text='Connection')
    tabControl.add(file_types_tab, text='File Types')
    tabControl.add(save_to_tab, text='Save to')
    tabControl.add(general_tab, text='General')
    tabControl.add(sounds_tab, text='Sounds')
    tabControl.add(dial_up_vpn_tab, text='Dial-Up / VPN')
    tabControl.add(sites_logins_tab, text='Sites Logins')
    tabControl.add(proxy_socks_tab, text='Proxy / Sockets')

    tabControl.select(save_to_tab)
    tabControl.enable_traversal()

    tabControl.pack(expand=1, fill="both")
    # endregion

    options_dialog_frame1 = tkinter.Frame(options_dialog, relief='ridge')
    options_dialog_frame1.pack(side=BOTTOM, fill='x')
    # region options_dialog_frame1 widgets

    # region Help Button
    options_dialog_help_button_text = 'Help'
    options_dialog_help_button = Button(
        options_dialog_frame1,
        width=10,
        padx=10,
        pady=5,
        text=options_dialog_help_button_text
    )
    options_dialog_help_button.pack(side=RIGHT)
    # endregion

    # region OK Button
    options_dialog_ok_button_text = 'OK'
    options_dialog_ok_button = Button(
        options_dialog_frame1,
        width=10,
        pady=5,
        text=options_dialog_ok_button_text
    )
    options_dialog_ok_button.pack(side=RIGHT)
    # endregion

    # endregion

    options_dialog.mainloop()
    pass

