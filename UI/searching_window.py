from tkinter import *
from API_calls import searching
import threading


class Search(Frame):
    start_search_btn = Button()
    stop_search_btn = Button()
    search_keyword = Entry()

    def __init__(self, master):
        super(Search, self).__init__(master)
        self.grid()
        self.init_widgets()

    def init_widgets(self):
        # init widgets
        keyword_lbl = Label(self, text="Keyword:")
        keyword_lbl.pack()

        self.search_keyword = Entry(self, width=30)
        self.search_keyword.pack()

        self.start_search_btn = Button(self, text="Stream",
                                   command=lambda: start_search(self.search_keyword.get()), width=30)
        self.start_search_btn.pack()

        self.stop_search_btn = Button(self, text="Stop", command=lambda: stop_search())
        self.stop_search_btn.pack()


def start_search(keyword):
    if keyword is not "" and not searching.get_flag():
        searching.set_flag(True)
        search_thread = threading.Thread(target=lambda: searching.searching_proc(keyword))
        print("Starting search process...")
        search_thread.start()
    else:
        if keyword is "":
            print("Give a keyword to search Twitter.")
        else:
            print("Already searching Twitter!")


def stop_search():
    print("API_calls stopped!")
    searching.set_flag(False)


def on_exit(root):
    stop_search()
    root.destroy()


def search_window():
    root = Tk()
    root.minsize(400, 200)
    root.title("--Searching API--")
    search_frame = Search(root)
    search_frame.pack()

    # TODO: let the user choose a db and collection name + if new db -> host and port
    # TODO: show into window console's messages

    root.protocol("WM_DELETE_WINDOW", lambda: on_exit(root))
    root.mainloop()
