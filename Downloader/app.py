import tkinter
from tkinter import *
from Downloader.View.app_add_url_onclick_listener import on_click_add_url_listener
from Downloader.View.app_downloading_dialog import on_initialize_download
from Downloader.View.app_options_onclick_listener import on_click_options_listener
from Downloader.View.app_scheduler_onclick_listener import on_click_scheduler_listener

# Main Gui Entry Point


screenName = 'Internet Download Manager'

window = Tk()

# region window properties
window.title(screenName)
window_width = 1082
window_height = 640
window_geometry = f"{window_width}x{window_height}"
window.geometry(window_geometry)
window.resizable(0, 0)

# endregion

# region window widgets

frame0 = tkinter.Frame(window, borderwidth=2, relief='ridge')
frame0.grid(column=0, row=0, sticky="nsew")
# region frame 0 widgets

# region Tasks Label
tasks_label_text = 'Tasks'
tasks_label = Label(frame0, text=tasks_label_text, padx=5, pady=5)
tasks_label.grid(row=0, column=0)
# endregion

# region File Label
file_label_text = 'File'
file_label = Label(frame0, text=file_label_text, padx=5, pady=5)
file_label.grid(row=0, column=1)
# endregion

# region Downloads Label
downloads_label_text = 'Downloads'
downloads_label = Label(frame0, text=downloads_label_text, padx=5, pady=5)
downloads_label.grid(row=0, column=2)
# endregion

# region View Label
view_label_text = 'View'
view_label = Label(frame0, text=view_label_text, padx=5, pady=5)
view_label.grid(row=0, column=3)
# endregion

# region Help Label
help_label_text = 'Help'
help_label = Label(frame0, text=help_label_text, padx=5, pady=5)
help_label.grid(row=0, column=4)
# endregion

# endregion

frame1 = tkinter.Frame(window, borderwidth=2, relief='ridge')
frame1.grid(column=0, row=1, sticky="nsew")
# region frame 1 widgets

# region Add URL Button
add_url_button = Button(frame1, text='Add URL', command=lambda: on_click_add_url_listener(add_url_to_list))
add_url_button.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5)
# endregion

# region Add Resume Button
resume_button = Button(frame1, text='Resume')
resume_button.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=5)
# endregion

# region Add Stop Button
stop_button = Button(frame1, text='Stop')
stop_button.grid(row=0, column=2, padx=5, pady=5, ipadx=5, ipady=5)
# endregion

# region Add Stop All Button
stop_all_button = Button(frame1, text='Stop All')
stop_all_button.grid(row=0, column=3, padx=5, pady=5, ipadx=5, ipady=5)
# endregion

# region Add Delete Completed Downloads Button
delete_completed_downloads_button = Button(frame1, text='Delete Completed Downloads')
delete_completed_downloads_button.grid(row=0, column=4, padx=5, pady=5, ipadx=5, ipady=5)
# endregion

# region Add Options Button
options_button = Button(frame1, text='Options', command=on_click_options_listener)
options_button.grid(row=0, column=5, padx=5, pady=5, ipadx=5, ipady=5)
# endregion

# region Add Scheduler Button
scheduler_button = Button(frame1, text='Scheduler', command=on_click_scheduler_listener)
scheduler_button.grid(row=0, column=6, padx=5, pady=5, ipadx=5, ipady=5)
# endregion

# region Add Start Queue Button
start_queue_button = Button(frame1, text='Start Queue')
start_queue_button.grid(row=0, column=7, padx=5, pady=5, ipadx=5, ipady=5)
# endregion

# region Add Stop Queue Button
stop_queue_button = Button(frame1, text='Stop Queue')
stop_queue_button.grid(row=0, column=8, padx=5, pady=5, ipadx=5, ipady=5)
# endregion

# endregion

frame2 = tkinter.Frame(window, borderwidth=1, relief='ridge')
frame2.grid(column=0, row=2, sticky="nsew")

frame2_1 = tkinter.Frame(frame2, borderwidth=1, relief='ridge')
frame2_1.grid(column=0, row=0, sticky="nsew")
# region frame 2_1 widgets

# region Scrollable listbox
scrollbar1 = Scrollbar(frame2_1)
listbox1 = Listbox(frame2_1, width=30, height=30, selectmode=EXTENDED)

listbox1.pack(side=LEFT, fill='x')
scrollbar1.pack(side=RIGHT, fill='y')

for i in range(100):
    listbox1.insert(END, i)

# attach listbox to scrollbar
listbox1.config(yscrollcommand=scrollbar1.set)
scrollbar1.config(command=listbox1.yview)

# endregion

# endregion

frame2_2 = tkinter.Frame(frame2, borderwidth=1, relief='ridge')
frame2_2.grid(column=1, row=0, sticky="nsew", padx=5)
# region frame 2_2 widgets

# region Scrollable listbox
scrollbar2 = Scrollbar(frame2_2)
listbox2 = Listbox(frame2_2, width=99, height=30, selectmode=EXTENDED)

listbox2.pack(side=LEFT, fill='x')
scrollbar2.pack(side=RIGHT, fill='y')

# attach listbox to scrollbar
listbox2.config(yscrollcommand=scrollbar2.set)
scrollbar2.config(command=listbox2.yview)


# endregion

# endregion

# endregion

def add_url_to_list(url):
    listbox2.insert(END, url)
    on_initialize_download(url)


# window loop
window.mainloop()
