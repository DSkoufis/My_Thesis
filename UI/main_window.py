from tkinter import *
from UI import streaming_window
from UI import searching_window
from Utilities import window_utils


class App(Frame):
    def __init__(self, master):
        super(App, self).__init__(master)
        self.root = master
        self.grid()
        self.init_widgets()

    def init_widgets(self):
        stream_btn = Button(self, text="Start Streaming", command=streaming_window.stream_window)
        stream_btn.pack(side=TOP)

        search_btn = Button(self, text="Start Search API", command=searching_window.search_window)
        search_btn.pack(side=TOP)

        exit_btn = Button(self, text="Exit", command=lambda: window_utils.close_window(self.root))
        exit_btn.pack(side=TOP)

root = Tk()
root.minsize(400, 200)
root.title("--Twitter API--")

app = App(root)
app.pack()

root.mainloop()