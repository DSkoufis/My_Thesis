from tkinter import *
from API_calls import searching
import threading

# This boolean, keeps track, if a new thread have created
# to not create new every time
new_thread = True


def get_new_thread():
    return new_thread


def set_new_thread(value):
    global new_thread
    new_thread = value


def start_search(keyword):
    # we do some validation here if user gave a value into Entry
    # if empty or stop_flag from searching.py is false, do not enter this
    if keyword is not "" and (not searching.get_stop_flag() or searching.get_pause_flag()):
        if get_new_thread():
            searching.set_stop_flag(True)
            searching.set_pause_flag(False)
            search_thread = threading.Thread(target=lambda: searching.searching_proc(keyword))
            print("Starting search process...")
            set_new_thread(False)
            search_thread.start()
        else:
            print("Continuing search...")
            searching.set_pause_flag(False)
    else:
        if keyword is "":
            print("Give a keyword to search Twitter.")
        else:
            print("Already searching Twitter!")


# with this function, we stop the Search API calls
def stop_search():
    if searching.get_stop_flag():  # if the stop_flag is True
        print("Terminating search...")
        searching.set_stop_flag(False)  # stop it
        searching.set_pause_flag(True)
        set_new_thread(True)
    else:
        print("Search already stopped")  # else do nothing


def pause_search():
    if not searching.get_pause_flag():
        print("Search paused!")
        searching.set_pause_flag(True)
    else:
        print("Search already paused.")


# with this function, we exit the window safely
def on_exit(root):
    stop_search()
    root.destroy()


# this function is called from main window to show searching window
def search_window():
    root = Tk()
    root.minsize(400, 200)
    root.title("--Searching API--")

    # initialize window frames
    label_frm = Frame(root)  # this frame holds the box that user writes
    buttons_frm = Frame(root)  # this frame holds start stop pause buttons
    exit_frm = Frame(root)  # this frame has exit button

    # pack the frames
    label_frm.pack(side=TOP, pady=10)
    buttons_frm.pack(pady=15)
    exit_frm.pack(anchor=SE, pady=30)

    # add widgets onto --- label_frm ---
    keyword_lbl = Label(label_frm, text="Keyword:")
    keyword_lbl.grid(column=2, row=0)
    keyword_entry = Entry(label_frm, width=30)
    keyword_entry.grid(column=3, row=0, padx=10)

    # add widgets onto --- buttons_frm ---
    start_button = Button(buttons_frm, text="Search", width=15,
                          command=lambda: start_search(keyword_entry.get()))
    start_button.grid(row=0, column=1, columnspan=2, padx=10, ipady=2)  # button to start stream
    pause_button = Button(buttons_frm, text="Pause", width=15,
                          command=lambda: pause_search())
    pause_button.grid(row=0, column=3, columnspan=2, padx=10, ipady=2)  # button to pause stream
    stop_button = Button(buttons_frm, text="Stop", width=15, command=lambda: stop_search())
    stop_button.grid(row=0, column=5, columnspan=2, padx=10, ipady=2)  # button to stop stream

    # add widgets onto --- exit_frm ---
    # TODO: if I want to close frames only, change this lambda
    exit_stream_button = Button(exit_frm, text="Exit", width=20,
                                command=lambda: on_exit(root))
    exit_stream_button.pack()

    # TODO: show into window console's messages

    root.protocol("WM_DELETE_WINDOW", lambda: on_exit(root))
    root.mainloop()
