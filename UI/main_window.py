from tkinter import *
from UI import streaming_window


class App:

    def __init__(self, master):
        frame = Frame(master)
        frame.grid()
        frame.pack(side=TOP)

        self.button = Button(frame, text="Stream", command=streaming_window.stream_window)
        self.button.pack(side=TOP)

root = Tk()
root.minsize(300, 150)
root.title("--Twitter API--")

app = App(root)

root.mainloop()