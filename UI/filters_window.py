from tkinter import *
import Utilities.database as db


def filters_window():
    root = Tk()
    root.minsize(400, 200)
    root.title("--Stats--")

    stats_frame = Frame(root)
    stats_frame.pack(fill=X, side=TOP)
    sum_lbl = Label(stats_frame, text="Tweets collected: ")
    sum_lbl.grid(row=0, column=1, padx=10)
    tweets_sum = str(db.db_collection.count())
    sum_txt = Label(stats_frame, text=tweets_sum)
    sum_txt.grid(row=0, column=2)

    root.mainloop()
