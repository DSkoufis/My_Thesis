from tkinter import *
from Streaming import streaming
import threading


class Stream:

    def __init__(self, master):
        frame = Frame(master)
        frame.grid()
        frame.pack(side=TOP)

        self.start_button = Button(frame, text="Stream", command=start_stream)
        self.start_button.pack(side=LEFT)

        self.stop_button = Button(frame, text="Stop", command=stop_stream)
        self.stop_button.pack(side=RIGHT)


def start_stream():
    my_thread = threading.Thread(target=streaming.streaming_proc)
    print("Starting stream...")
    my_thread.start()
    streaming.flag = True


def stop_stream():
    streaming.flag = False


def stream_window():
    root = Tk()
    root.minsize(300, 150)
    root.title("--Streaming API--")

    app = Stream(root)

    root.mainloop()