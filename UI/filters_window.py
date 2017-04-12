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

    # TODO: This is for testing
    '''
    this is for test
    
    it works!
    '''
    # a button that finds all different time zones and print them
    def calculate_time_zone():
        zones = []
        query_cursor = db_collection.find()
        counter = 0
        for item in query_cursor:
            counter += 1
            zone = item["user"]["time_zone"]
            if zone is not None and zone not in zones:
                zones.append(zone)
        for zone in zones:
            print(zone)
        print("Length: " + str(len(zones)))
        print(counter)

    time_zones_btn = Button(stats_frame, text="Calculate & Print",command=calculate_time_zone)
    time_zones_btn.grid(row=4, column=2, columnspan=2, pady=10)

    # TODO: This is for testing
    '''
    this is for test
    
    and it works!!
    '''
    # button that finds distribution of retweets and shows histogram
    import matplotlib.pyplot as plt

    def calculate_retweets_map():
        count = {}  # this is a dict that indicates how many times a retweet occurred. e.g 255 retweet_count found 25
        olist = []  # this list holds the different retweet_count e.g 1,2,3,4,5,6 so we will sort it later
        population = []  # this list is the same as count, but it holds only the values
        bins = []  # bins, that show which numbers are shown in histogram
        query_cursor = db_collection.find()  # make our query
        for item in query_cursor:
            retweets = item["retweet_count"]  # get the int
            # this is because, I found 205 retweets happened in ~600 tweets (just visual)
            if retweets is not 205:
                population.append(retweets)  # we must have the whole population e.g [0,0,0,4,5,0...]
                if str(retweets) not in count:  # here we build the count dict - if there is no previous entry
                    count[str(retweets)] = 1  # make one with the retweet int as key
                    olist.append(retweets)  # but we need to sort it later (we need only keys in this list)
                else:
                    count[str(retweets)] += 1
        olist.sort()
        # this is again for visual (ignore it)
        counter = 0
        while counter <= 29:
            population.append(205)
            counter += 1

        low = 1000000  # a big integer, with this, we find where the bins start
        for key in olist:
            # with this, we show the values that are between 15 and 600 (visual again)
            if 15 < count[str(key)] < 600:
                print(str(key) + " retweets: " + str(count[str(key)]))
                if key < low:  # we must find the lowest number to start for the bins
                    low = key
        while low <= 1132:
            bins.append(low)  # we build the bins to hold all values between the low, and a random number (visual again)
            low += 1

        print(str(len(bins)))
        print(str(len(population)))

        plt.hist(population, bins, color='green')
        plt.xlabel("Retweets count")
        plt.title("Retweet count distribution")
        plt.show()

    retweets_map_btn = Button(stats_frame, text="Calculate Retweets", command=calculate_retweets_map)
    retweets_map_btn.grid(row=5, column=2, columnspan=2, pady=10)

    root.mainloop()
