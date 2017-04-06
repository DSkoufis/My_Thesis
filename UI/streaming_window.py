from tkinter import *
from API_calls import streaming
import threading

# This boolean, keeps track, if a new thread have created
# to not create new every time
new_thread = True


def get_new_thread():
    return new_thread


def set_new_thread(value):
    global new_thread
    new_thread = value


# this method called when "Stream" button is pressed
# it checks if previous stream stopped or paused and do accordingly
def start_stream(search_keyword):
    # if user gave keyword and stream is not running do:
    if search_keyword is not "" and (streaming.get_stop_flag() is False or streaming.get_pause_flag() is False):
        if get_new_thread():
            print("Starting stream...")
            # we initialize the flags
            streaming.set_stop_flag(True)
            streaming.set_pause_flag(True)
            set_new_thread(False)  # we make global variable into False, because thread already created
            # start the new thread
            stream_thread = threading.Thread(target=lambda: streaming.streaming_proc(search_keyword))
            stream_thread.start()
        else:
            print("Continuing stream...")
            streaming.set_pause_flag(True)
    else:  # else check what is the problem and print
        if search_keyword is "":
            print("Give a keyword to search Twitter.")
        else:
            print("Stream already running!")


def stop_stream():
    if streaming.get_stop_flag():
        print("Terminating stream...")
        # on stop, we need to terminate both flags
        streaming.set_pause_flag(False)
        streaming.set_stop_flag(False)
        set_new_thread(True)
    else:
        print("Stream already stopped.")


def pause_stream():
    if streaming.get_pause_flag():
        print("Stream paused!")
        streaming.set_pause_flag(False)
    else:
        print("Stream already paused.")


def on_exit(root):
    stop_stream()
    root.destroy()


def stream_window():
    root = Tk()
    root.minsize(400, 200)
    root.title("--Streaming API--")

    # initialize window's frames
    # TODO: (idea) if in future want 1 frame that hides away, put all frames into master frame
    # master_frm = Frame(root) \n  label_frm = Frame(master_frm) etc
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
    start_button = Button(buttons_frm, text="Stream", width=15,
                          command=lambda: start_stream(keyword_entry.get()))
    start_button.grid(row=0, column=1, columnspan=2, padx=10, ipady=2)  # button to start stream
    pause_button = Button(buttons_frm, text="Pause", width=15,
                          command=lambda: pause_stream())
    pause_button.grid(row=0, column=3, columnspan=2, padx=10, ipady=2)  # button to pause stream
    stop_button = Button(buttons_frm, text="Stop", width=15, command=lambda: stop_stream())
    stop_button.grid(row=0,  column=5, columnspan=2, padx=10, ipady=2)  # button to stop stream

    # add widgets onto --- exit_frm ---
    # TODO: if I want to close frames only, change this lambda
    exit_stream_button = Button(exit_frm, text="Exit", width=20,
                                command=lambda: on_exit(root))
    exit_stream_button.pack()

    # TODO: show into window console's messages

    root.protocol("WM_DELETE_WINDOW", lambda: on_exit(root))
    root.mainloop()
