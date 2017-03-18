from tkinter import *
from UI import streaming_window


class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.grid()
        frame.pack(side=TOP)

    def init_widgets(self, frame):
        self.stream_btn = Button(frame, text="Start Streaming", command=streaming_window.stream_window)
        self.stream_btn.pack(side=TOP)

        self.exit_btn = Button(frame, text="Exit", command=frame.destroy)
        self.exit_btn.pack(side=TOP)

root = Tk()
root.minsize(400, 200)
root.title("--Twitter API--")

app = App(root)
app.init_widgets(root)

root.mainloop()