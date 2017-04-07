from tkinter import *
import pymongo
import Utilities.database as db


# this window shows the db's data analysis or some stats
def filters_window():
    root = Tk()
    root.minsize(400, 200)
    root.title("--Stats--")

    db_collection = db.get_collection()

    # we have a frame that holds some basic stats
    stats_frame = Frame(root)
    stats_frame.pack(fill=X, side=TOP)

    # How many tweets we stored so far in this collection
    sum_lbl = Label(stats_frame, text="Tweets collected: ")
    sum_lbl.grid(row=0, column=1, padx=10, pady=1, sticky=W)
    tweets_sum = str(db_collection.count())
    sum_txt = Label(stats_frame, text=tweets_sum)
    sum_txt.grid(row=0, column=2, sticky=W)

    # How many verified users we have in our collection
    verified_lbl = Label(stats_frame, text="Verified users: ")
    verified_lbl.grid(row=1, column=1, padx=10, pady=1, sticky=W)
    verified_sum = str(db_collection.find(filter={"user.verified": True}).count())
    verified_txt = Label(stats_frame, text=verified_sum)
    verified_txt.grid(row=1, column=2, sticky=W)

    # Times the most retweeted tweet retweeted
    max_rt_lbl = Label(stats_frame, text="Most RTs of a tweet: ")
    max_rt_lbl.grid(row=2, column=1, padx=10, pady=1, sticky=W)
    max_rt_sum_cursor = db_collection.find().sort("retweet_count", pymongo.DESCENDING).limit(limit=1)  # a cursor is returned
    max_rt_sum_json = max_rt_sum_cursor[0]  # we apply the first item because it is a cursor and we must iterate
    max_rt_sum = str(max_rt_sum_json["retweet_count"])  # we parse it into a string
    max_rt_txt = Label(stats_frame, text=max_rt_sum)
    max_rt_txt.grid(row=2, column=2, sticky=W)

    # User's most statuses
    max_status_lbl = Label(stats_frame, text="User's most statuses: ")
    max_status_lbl.grid(row=3, column=1, padx=10, pady=1, sticky=W)
    max_status_sum_cursor = db_collection.find().sort("user.statuses_count", pymongo.DESCENDING).limit(limit=1)
    max_status_sum_json = max_status_sum_cursor[0]
    max_status_sum = str(max_status_sum_json["user"]["statuses_count"])
    max_status_txt = Label(stats_frame, text=max_status_sum)
    max_status_txt.grid(row=3, column=2, sticky=W)

    root.mainloop()
