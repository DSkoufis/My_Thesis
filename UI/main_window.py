from tkinter import *
from UI import streaming_window
from UI import searching_window
from UI import filters_window
from Utilities import window_utils


class App(Frame):
    def __init__(self, master):
        super(App, self).__init__(master)
        self.root = master
        self.grid()
        self.init_widgets()

    def init_widgets(self):
        stream_btn = Button(self, text="Start Streaming", command=streaming_window.stream_window, pady=3)
        stream_btn.pack(pady=3)

        search_btn = Button(self, text="Start Search API", command=searching_window.search_window, pady=3)
        search_btn.pack(pady=3)

        filters_btn = Button(self, text="Show Stats", command=filters_window.filters_window, pady=3)
        filters_btn.pack(pady=3)

        exit_btn = Button(self, text="Exit", command=lambda: window_utils.close_window(self.root), pady=3)
        exit_btn.pack(pady=3)

root = Tk()
root.minsize(400, 200)
root.title("--Twitter API--")

app = App(root)
app.pack()

root.mainloop()