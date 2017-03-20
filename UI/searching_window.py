from tkinter import *
from API_calls import searching
from Utilities import window_utils
import threading


# this class is a Frame class with some buttons (formally the search window)
class Search(Frame):
    def __init__(self, master):
        super(Search, self).__init__(master)  # we call the super constructor
        self.root = master
        self.grid()
        self.init_widgets()  # and we initialize our widgets

    def init_widgets(self):
        # init widgets
        keyword_lbl = Label(self, text="Keyword:")
        keyword_lbl.pack()

        self.search_keyword = Entry(self, width=30)  # this Entry gets the keyword that the user gives
        self.search_keyword.pack()

        # when we press this button, search starts
        # by calling start_search function with keyword argument
        # that we get from Entry
        self.start_search_btn = Button(self, text="Stream",
                                   command=lambda: start_search(self.search_keyword.get()), width=30)
        self.start_search_btn.pack()

        # when we press this button, search stops
        # by calling stop_search function
        self.stop_search_btn = Button(self, text="Stop", command=lambda: stop_search())
        self.stop_search_btn.pack()

        # when we press this button, window closes
        # by calling main_window.close_window(root window) method
        self.close_window_btn = Button(self, text="Exit", command=lambda: window_utils.close_window(self.root))
        self.close_window_btn.pack()


def start_search(keyword):
    # we do some validation here if user gave a value into Entry
    # if empty or flag from searching.py is false, do not enter this
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


# with this function, we stop the Search API calls
def stop_search():
    if searching.get_flag():  # if the flag is True
        print("API_calls stopped!")
        searching.set_flag(False)  # stop it
    else:
        print("Search already stopped")  # else do nothing


# with this function, we exit the window
def on_exit(root):
    stop_search()
    root.destroy()


# this function is called from main window to show searching window
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
