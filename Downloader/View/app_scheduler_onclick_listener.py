import tkinter
from tkinter import *
from tkinter import ttk
from Downloader.Utils.human_readable import official_file_name
from Downloader.Utils.log import Logging


@Logging
def on_click_scheduler_listener():
    scheduler_dialog = Tk()

    # region scheduler_dialog properties
    scheduler_dialog_title = 'Scheduler'
    scheduler_dialog.title(scheduler_dialog_title)
    scheduler_dialog_width = 800
    scheduler_dialog_height = 620
    scheduler_dialog_geometry = f"{scheduler_dialog_width}x{scheduler_dialog_height}"
    scheduler_dialog.geometry(scheduler_dialog_geometry)
    scheduler_dialog.resizable(0, 0)
    # scheduler_dialog.overrideredirect(1) # will remove the top badge of window
    # endregion

    scheduler_dialog_frame0 = tkinter.Frame(scheduler_dialog, borderwidth=2, relief='ridge')
    scheduler_dialog_frame0.pack(side=LEFT, fill='both', expand=1)

    scheduler_dialog_frame0_0 = tkinter.Frame(scheduler_dialog_frame0, borderwidth=2, relief='ridge')
    scheduler_dialog_frame0_0.pack(side=LEFT, fill='both')
    # region  scheduler_dialog_frame0_0 widgets

    scheduler_dialog_frame0_0_0 = tkinter.Frame(scheduler_dialog_frame0_0, borderwidth=2, relief='ridge')
    scheduler_dialog_frame0_0_0.pack(side=TOP, fill='x')
    # region Queues Label
    queue_label = Label(scheduler_dialog_frame0_0_0, text='Queues')
    queue_label.pack()
    # endregion

    scheduler_dialog_frame0_0_1 = tkinter.Frame(scheduler_dialog_frame0_0, borderwidth=2, relief='ridge')
    scheduler_dialog_frame0_0_1.pack(fill='x')
    # region Scrollable listbox
    scrollbar_listbox_queues = Scrollbar(scheduler_dialog_frame0_0_1)
    listbox_queues = Listbox(scheduler_dialog_frame0_0_1, width=30, height=30, selectmode=EXTENDED)

    listbox_queues.pack(side=LEFT, fill='both')
    scrollbar_listbox_queues.pack(side=RIGHT, fill='y')

    queues = ['Main Download Queue', 'Synchronized Download Queue']
    for queue in queues:
        listbox_queues.insert(END, queue)

    # attach listbox to scrollbar
    listbox_queues.config(yscrollcommand=scrollbar_listbox_queues.set)
    scrollbar_listbox_queues.config(command=listbox_queues.yview)

    # endregion

    scheduler_dialog_frame0_0_2 = tkinter.Frame(scheduler_dialog_frame0_0, borderwidth=2, relief='ridge')
    scheduler_dialog_frame0_0_2.pack(side=BOTTOM, fill='x')
    # region New Queue, and Delete Queue Button(s)
    new_queue_button = Button(scheduler_dialog_frame0_0_2, text='New Queue')
    new_queue_button.pack(side=LEFT)

    delete_queue_button = Button(scheduler_dialog_frame0_0_2, text='Delete Queue')
    delete_queue_button.pack(side=RIGHT)
    # endregion

    # endregion

    scheduler_dialog_frame0_1 = tkinter.Frame(scheduler_dialog_frame0, borderwidth=2, relief='ridge')
    scheduler_dialog_frame0_1.pack(side=RIGHT, fill='both', expand=1)
    # region  scheduler_dialog_frame0_1 widgets

    scheduler_dialog_frame0_1_0 = tkinter.Frame(scheduler_dialog_frame0_1, borderwidth=2, relief='ridge')
    scheduler_dialog_frame0_1_0.pack(side=TOP, fill='x')
    # region Main Download Queue Label
    scheduler_queue_label = Label(scheduler_dialog_frame0_1_0, text='Main Download Queue')
    scheduler_queue_label.pack()
    # endregion

    scheduler_dialog_frame0_1_1 = tkinter.Frame(scheduler_dialog_frame0_1, borderwidth=2, relief='ridge')
    scheduler_dialog_frame0_1_1.pack(fill='both')
    # region Main Download Queue Notebook
    tabControl = ttk.Notebook(scheduler_dialog_frame0_1_1, height=520)

    schedule_tab = ttk.Frame(tabControl)
    file_in_the_queue_tab = ttk.Frame(tabControl)
    # region file_in_the_queue_tab content widgets
    file_in_the_queue_tab_frame0 = tkinter.Frame(file_in_the_queue_tab, relief='ridge')
    file_in_the_queue_tab_frame0.pack(side=TOP, fill='x', padx=15, pady=15)
    # region file_in_the_queue_tab_frame0 widgets
    ttk.Label(file_in_the_queue_tab_frame0, text="Download").pack(side=LEFT)
    files_in_the_queue_entry = ttk.Entry(file_in_the_queue_tab_frame0, width=5)
    files_in_the_queue_entry.insert(0, '4')
    files_in_the_queue_entry.pack(side=LEFT, padx=5)
    ttk.Label(file_in_the_queue_tab_frame0, text="Files at the same time.").pack(side=LEFT)
    # endregion

    file_in_the_queue_tab_frame2 = tkinter.Frame(file_in_the_queue_tab, width=30, relief='ridge')
    file_in_the_queue_tab_frame2.pack(side=BOTTOM, fill='x', padx=15, pady=5)
    # region file_in_the_queue_tab_frame2 widgets

    # region 'Move Down' Button
    file_in_the_queue_tab_move_down_button_text = 'Move Down'
    file_in_the_queue_tab_move_down_button = Button(
        file_in_the_queue_tab_frame2,
        width=10,
        padx=5,
        pady=5,
        text=file_in_the_queue_tab_move_down_button_text
    )
    file_in_the_queue_tab_move_down_button.pack(side=LEFT)
    # endregion

    # region 'Move Up' Button
    file_in_the_queue_tab_move_up_button_text = 'Move Up'
    file_in_the_queue_tab_move_up_button = Button(
        file_in_the_queue_tab_frame2,
        width=10,
        padx=5,
        pady=5,
        text=file_in_the_queue_tab_move_up_button_text
    )
    file_in_the_queue_tab_move_up_button.pack(side=LEFT)
    # endregion

    # region 'Remove Item' Button
    file_in_the_queue_tab_remove_item_button_text = 'Remove Item'
    file_in_the_queue_tab_remove_item_button = Button(
        file_in_the_queue_tab_frame2,
        width=10,
        padx=5,
        pady=5,
        text=file_in_the_queue_tab_remove_item_button_text
    )
    file_in_the_queue_tab_remove_item_button.pack(side=LEFT)
    # endregion

    # endregion

    file_in_the_queue_tab_frame1 = tkinter.Frame(file_in_the_queue_tab, relief='ridge')
    file_in_the_queue_tab_frame1.pack(fill='both', padx=15, pady=5)
    # region file_in_the_queue_tab_frame1 widgets
    # region Scrollable listbox
    file_in_the_queue_tab_scrollbar = Scrollbar(file_in_the_queue_tab_frame1)
    file_in_the_queue_tab_listbox = Listbox(file_in_the_queue_tab_frame1, width=30, height=30, selectmode=EXTENDED)

    file_in_the_queue_tab_listbox.pack(side=TOP, ipadx=30, ipady=5, fill='both')
    file_in_the_queue_tab_scrollbar.pack(side=RIGHT, fill='y')

    url_links = [  # Place holder
        "https://releases.ubuntu.com/18.04/ubuntu-18.04.4-desktop-amd64.iso",
        "https://files03.tchspt.com/temp/MicrosoftEdgeStableSetup.msi",
        "http://mirrors.evowise.com/linuxmint/debian/lmde-4-cinnamon-32bit.iso",
        "https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_1280_10MG.mp4"
    ]
    for url_link in url_links:
        file_name = official_file_name(url_link)
        file_in_the_queue_tab_listbox.insert(END, file_name)

    # attach listbox to scrollbar
    file_in_the_queue_tab_listbox.config(yscrollcommand=file_in_the_queue_tab_scrollbar.set)
    file_in_the_queue_tab_scrollbar.config(command=file_in_the_queue_tab_listbox.yview)

    # endregion
    # endregion
    # endregion

    tabControl.add(schedule_tab, text='Schedule')
    tabControl.add(file_in_the_queue_tab, text='Files in The Queue')

    tabControl.select(schedule_tab)
    tabControl.enable_traversal()

    tabControl.pack(expand=1, fill="both")
    # endregion

    scheduler_dialog_frame0_1_2 = tkinter.Frame(scheduler_dialog_frame0_1, borderwidth=2, relief='ridge')
    scheduler_dialog_frame0_1_2.pack(side=BOTTOM, fill='x')
    # region scheduler_dialog_frame1 widgets

    # region 'Start now' Button
    scheduler_dialog_start_now_button_text = 'Start Now'
    scheduler_dialog_start_now_button = Button(
        scheduler_dialog_frame0_1_2,
        width=10,
        padx=10,
        pady=5,
        text=scheduler_dialog_start_now_button_text
    )
    scheduler_dialog_start_now_button.pack(side=LEFT)
    # endregion

    # region 'Stop' Button
    scheduler_dialog_stop_button_text = 'Stop'
    scheduler_dialog_stop_button = Button(
        scheduler_dialog_frame0_1_2,
        width=10,
        padx=10,
        pady=5,
        text=scheduler_dialog_stop_button_text
    )
    scheduler_dialog_stop_button.pack(side=LEFT)
    # endregion

    # region 'Help' Button
    scheduler_dialog_help_button_text = 'Help'
    scheduler_dialog_help_button = Button(
        scheduler_dialog_frame0_1_2,
        width=10,
        padx=10,
        pady=5,
        text=scheduler_dialog_help_button_text
    )
    scheduler_dialog_help_button.pack(side=LEFT)
    # endregion

    # region 'Apply' Button
    scheduler_dialog_apply_button_text = 'Apply'
    scheduler_dialog_apply_button = Button(
        scheduler_dialog_frame0_1_2,
        width=10,
        padx=10,
        pady=5,
        text=scheduler_dialog_apply_button_text
    )
    scheduler_dialog_apply_button.pack(side=LEFT)
    # endregion

    # region Close Button
    scheduler_dialog_close_button_text = 'Close'
    scheduler_dialog_close_button = Button(
        scheduler_dialog_frame0_1_2,
        width=10,
        pady=5,
        text=scheduler_dialog_close_button_text,
        command=lambda: scheduler_dialog.destroy()
    )
    scheduler_dialog_close_button.pack(side=LEFT)
    # endregion

    # endregion

    # endregion

    scheduler_dialog.mainloop()
    pass
