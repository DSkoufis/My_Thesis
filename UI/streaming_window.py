from tkinter import *
from API_calls import streaming
import threading


class Stream:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack(side=TOP)

        self.keyword_lbl = Label(frame, text="Keyword:")
        self.keyword_lbl.pack(side=TOP)

        self.user_keyword = Entry(frame, width=30)
        self.user_keyword.pack()

        self.start_button = Button(frame, text="Stream",
                                   command=lambda: start_stream(self.user_keyword.get()), width=30)
        self.start_button.pack()

        self.stop_button = Button(frame, text="Stop", command=lambda: stop_stream())
        self.stop_button.pack()

        self.pause_stream_button = Button(frame, text="Pause", command=lambda: pause_stream())


def start_stream(search_keyword):
    if search_keyword is not "" and streaming.flag is False:
        streaming.flag = True
        global stream_thread
        stream_thread = threading.Thread(target=lambda: streaming.streaming_proc(search_keyword))
        event_listener = threading.Event()
        print("Starting stream...")
        stream_thread.start()

    else:
        if search_keyword is "":
            print("Give a keyword to search Twitter.")
        else:
            print("Stream already running!")


def pause_stream():
    streaming.flag = False


def stop_stream():
    # TODO: this must change to stop the thread
    # maybe reference to https://www.safaribooksonline.com/library/view/python-cookbook-2nd/0596007973/ch09s03.html
    streaming.flag = False


def on_exit(root):
    stop_stream()
    root.destroy()


def stream_window():
    root = Tk()
    root.minsize(400, 200)
    root.title("--Streaming API--")
    app = Stream(root)

    # TODO: let the user choose a db and collection name + if new db -> host and port
    # TODO: show into window console's messages

    root.protocol("WM_DELETE_WINDOW", lambda: on_exit(root))
    root.mainloop()