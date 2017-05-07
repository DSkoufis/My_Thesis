#######################################################################################
# Module that is responsible to connect to the Streaming Server and gather the tweets #
#######################################################################################
from tweepy import StreamListener
import json
from tkinter import messagebox
from datetime import datetime
from Utilities import db_utils, manage_credentials, read_write, other_utils

LOG_NAME = "--> stream_util.py"


# Class that inherits StreamListener and handles the data.
class StdOutListener(StreamListener):
    def __init__(self):
        super(StdOutListener, self).__init__()
        self.flag = False  # this flag indicates if stream must stop or not. As long as it is False, we keep stream open
        self.pause_flag = False  # as long as false, pause is closed
        self.store_counter = None  # this counter, counts how many tweets stored to the DB so far

    def on_connect(self):
        global stream_controller
        print(LOG_NAME + " :: SUCCESS :: connected to Streaming Server!\n#### Gathering tweets for '"
              + stream_controller.search_keyword + "' keyword. ####")
        self.store_counter = 0  # initialize the counter
        # and save the keyword to the keywords.json file
        keywords_list = [x for x in stream_controller.search_keyword.split(",")]
        for keyword in keywords_list:
            keyword = keyword.lstrip()
            keyword = keyword.rstrip()
            read_write.write_keywords(keyword)

    def on_data(self, data):
        if self.flag:  # flag keep track if we want to stop the stream
            return False  # return False to terminate the loop
        if self.pause_flag:  # pause flag keeps track if we want to pause the stream
            return True  # return True and do nothing with the data. It's a virtual pause.

        data = json.loads(data)  # turn the incoming data into json format

        if "user" not in data:  # if tweet has no user, we don't want this tweet
            print("No user data - ignoring tweet.")
            return True
        if data["lang"] != "en":  # we deal only with English language text based tweets
            print("Non English - ignoring tweet.")
            return True

        # we pass our data into this static method to clean them and keep only the necessary
        our_tweet = self.process_tweet(data)

        # this method try to save our tweet to the active connection to Mongo and returns the outcome
        # If all are OK, returns True, but if it fail, it returns False. With this way, we keep track
        # how many tweets we stored so far
        if db_utils.store_tweet(our_tweet):
            self.store_counter += 1  # increase the counter
            if self.store_counter % 100 == 0:  # and if we reach a multiply of 100, we print the result
                print("Stored " + str(self.store_counter) + " tweets so far.")
        # return True to continue the loop
        return True

    def on_error(self, status):
        # statuses take from here:
        # https://dev.twitter.com/overview/api/response-codes
        if status == 401:
            print(LOG_NAME + " :: HTTP_ERROR :: 401 Unauthorized - Missing or incorrect authentication credentials.")
        elif status == 304:
            print(LOG_NAME + " :: HTTP_ERROR :: 304 Not Modified - There was no new data to return.")
        elif status == 403:
            print(LOG_NAME + " :: HTTP_ERROR :: 403 Forbidden - The request is understood, " +
                  "but it has been refused or access is not allowed.")
        elif status == 420:
            print(LOG_NAME + " :: HTTP_ERROR :: 420 Enhance Your Calm - Returned when you are being rate limited.")
        elif status == 500:
            print(LOG_NAME + " :: HTTP_ERROR :: 500 Internal Server Error - Something is broken.")
        elif status == 503:
            print(LOG_NAME + " :: HTTP_ERROR :: 503 Service Unavailable - The Twitter servers are up, " +
                  "but overloaded with requests. Try again later.")
        elif status == 504:
            print(LOG_NAME + " :: HTTP_ERROR :: 504 Gateway timeout - The Twitter servers are up, but " +
                  "the request couldn’t be serviced due to some failure within our stack. Try again later.")
        else:
            print(LOG_NAME + " :: HTTP_ERROR :: " + status + " Unknown.")

        return False  # and stop the stream

    def on_disconnect(self, notice):
        status = json.loads(notice)
        print("Error on " + type(self).__name__ + " :: Name=" + status["stream_name"] +
              ", Reason=" + status["reason"] + ", Code=" + str(status["code"]))
        return False

    # setters for the flags
    def set_flag(self, value):
        self.flag = value

    def set_pause(self, value):
        self.pause_flag = value

    def process_tweet(self, tweet):
        # clearing the text of a tweet into two lists
        text = other_utils.clear_text(tweet["text"])

        # check if this tweet is a retweet
        if "rt" in text["stop_words"]:
            is_retweet = True
        else:
            is_retweet = False

        formatted_tweet = {"created_at": datetime.strptime(tweet["created_at"], "%a %b %d %H:%M:%S %z %Y"),
                           "favourite_count": tweet["favorite_count"],
                           "_id": tweet["id"],  # this will make the tweet's id, ObjectID
                           "retweet_count": tweet["retweet_count"],
                           "coordinates": tweet["coordinates"],
                           "timestamp": other_utils.get_timestamp(),
                           "is_retweet": is_retweet,
                           "text": text,
                           "whole_text": tweet["text"],
                           "user": {
                               "favourites_count": tweet["user"]["favourites_count"],
                               "followers_count": tweet["user"]["followers_count"],
                               "friends_count": tweet["user"]["friends_count"],
                               "id_str": tweet["user"]["id_str"],
                               "statuses_count": tweet["user"]["statuses_count"],
                               "verified": tweet["user"]["verified"],
                               "created_at": datetime.strptime(tweet["user"]["created_at"], "%a %b %d %H:%M:%S %z %Y"),
                               "geo_enabled": tweet["user"]["geo_enabled"],
                               "location": tweet["user"]["location"],
                               "time_zone": tweet["user"]["time_zone"],
                               "utc_offset": tweet["user"]["utc_offset"]
                           }}
        return formatted_tweet


# class that is responsible to start or close the threads of the stream
class StreamController(object):
    def __init__(self):
        self.search_keyword = None
        self.listener = StdOutListener()

    # method that starts the Streaming API
    def combine(self):
        # if not, set the flags to False ( so that we will be able to iterate at the Listener class )
        self.listener.set_flag(False)
        self.listener.set_pause(False)
        # and finally we start the stream
        self.stream()

    def stop(self):
        # setting only this flag to True, means that we break out of the streaming loop
        self.listener.set_flag(True)
        print("Stream stopped successfully.")

    def pause(self):
        self.listener.set_pause(True)

    def unpause(self):
        self.listener.set_pause(False)

    def stream(self):
        stream = manage_credentials.get_stream(listener=self.listener)
        # this is a try-except block, because if there is something wrong in the Listener class,
        # like e.g internet connection failure, it raises the exception inside the active thread
        try:
            # user can give more than one keywords for searching, we just add them to a list
            # he must separate them with commas, so we can split them and remove the whitespace with strip
            search_list = [x.strip() for x in self.search_keyword.split(",")]

            print(LOG_NAME + " :: INFO :: Trying to connect to the Streaming Server...")
            stream.filter(track=search_list,
                          async=True)  # start the loop, async sets the Streaming in a new Thread
        except AttributeError as e:
            print(LOG_NAME + " :: ERROR :: " + str(e))
            messagebox.showerror("Fatal error", "No credentials were found. Please close the script, " +
                                 "add the file and try again!")
        except Exception as e:
            print(LOG_NAME + " :: ERROR :: " + str(repr(e)))
            pass


# this controller, is initialized once the program starts, and we manage to handle the Streaming API
# through his methods
stream_controller = StreamController()


# function to start the Streaming API
def start_stream(frame):
    global stream_controller  # get the instance in hands
    # check if user gave a keyword
    if frame.keyword_entry.get().strip(" ") is not "":
        # change the GUI into more favorable way
        frame.mng_stream_btn.config(text="Stop Stream", command=lambda: stop_stream(frame))
        frame.pause_stream_btn.grid()  # show the pause button
        frame.pause_stream_btn.config(command=lambda: pause_unpause(frame))
        stream_controller.search_keyword = frame.keyword_entry.get()  # and set the keyword into controller,
        stream_controller.combine()  # to start the stream
    else:
        messagebox.showerror("Error", "Enter a keyword")


# function to handle the Pause/Un-pause button events
def pause_unpause(frame):
    global stream_controller
    if stream_controller.listener.pause_flag:  # if flag is True, it means that we already paused the stream
        stream_controller.unpause()  # so un-pause it and change the GUI
        frame.pause_stream_btn.config(text="Pause Stream")
    else:
        # but if it false, it means we press the Pause Stream button, so set it accordingly
        stream_controller.pause()
        frame.pause_stream_btn.config(text="Continue Stream")
        print("Stream paused...")


# function to close the stream
def stop_stream(frame):
    global stream_controller
    frame.mng_stream_btn.config(text="Start Stream", command=lambda: start_stream(frame))
    frame.pause_stream_btn.grid_remove()
    print("Terminating stream...")
    stream_controller.stop()  # by calling the stream controller
