#######################################################################################
# Module that is responsible to connect to the REST API and gather the tweets #
#######################################################################################
from Utilities import db_utils, read_write, manage_credentials, other_utils
from tkinter import messagebox
from threading import Thread, Event
from tweepy import TweepError
from pymongo.errors import ServerSelectionTimeoutError, AutoReconnect

LOG_NAME = " (search_util) : "


class SearchController(object):
    def __init__(self):
        self.search_thread = None
        self.search_keyword = None

        self.pause_search = False

        self.stop_thread = Event()
        read_write.log_message("[INFO]" + LOG_NAME + "SearchController initialized")

    def combine(self):
        self.stop_thread.clear()

        # if not, set the flag to False ( so that we do not break the search loop )
        self.unpause()
        # and finally build and start the Thread
        self.search_thread = Thread(target=self.search)
        self.search_thread.start()

    def search(self):
        api = manage_credentials.get_search()

        query = self.search_keyword
        # write the keyword back in the keywords.json
        read_write.write_keywords(query)

        print("#### Gathering tweets for '" + query + "' keyword. ####")
        read_write.log_message("[INFO]" + LOG_NAME + "#### Gathering tweets for '" + query + "' keyword. ####")
        tweets_per_query = 100  # how many tweets we can ask for
        read_write.log_message("[INFO]" + LOG_NAME + "Tweets per query = " + str(tweets_per_query))

        since_ID = None
        max_ID = -1

        tweet_count = 0  # this shows how many tweets have stored already
        ignored_count = 0

        while not self.stop_thread.is_set():
            if self.pause_search:  # if pause search have been set into True, we pause the search
                continue

            try:
                if max_ID <= 0:
                    if not since_ID:
                        new_tweets = api.search(q=query, count=tweets_per_query, lang="en", )
                    else:
                        new_tweets = api.search(q=query, count=tweets_per_query, lang="en", since_id=since_ID)
                else:
                    if not since_ID:
                        new_tweets = api.search(q=query, count=tweets_per_query, lang="en", max_id=str(max_ID - 1))
                    else:
                        new_tweets = api.search(q=query, count=tweets_per_query, lang="en",
                                                max_id=str(max_ID - 1), since_id=since_ID)

                if not new_tweets:
                    # if we don't get any new tweets
                    raise TweepError("No more tweets found! Terminating search...")

                for tweet in new_tweets:
                    our_tweet = other_utils.process_and_clear_tweet(tweet, method="search")
                    if db_utils.store_tweet(our_tweet):
                        tweet_count += 1  # we count how many tweets we got
                    else:
                        ignored_count += 1

                # logging some info into console
                print("Saved {0} tweets till now".format(tweet_count))  # and we print them

                max_ID = new_tweets[-1].id  # we need to re - set the max_ID for the new search query
            except TweepError as e:
                message = "[ERROR]" + LOG_NAME + "TweepError: " + str(e)
                print(message)  # we log the error
                read_write.log_message(message)
                break
            except AttributeError as e:
                message_1 = "[ERROR]" + LOG_NAME + "AttributeError: " + str(e)
                read_write.log_message(message_1)
                message_2 = "[REASON]" + LOG_NAME + "Can't connect to Twitter Server."
                print(message_1 + "\n" + message_2)
                read_write.log_message(message_2)
                break
            except ServerSelectionTimeoutError as e:
                read_write.log_message("[ERROR]" + LOG_NAME + "ServerSelectionTimeoutError: " + str(e))
                messagebox.showerror("Error", "Lost Connection to the DB")
                break
            except AutoReconnect as e:
                read_write.log_message("[ERROR]" + LOG_NAME + "AutoReconnect: " + str(e))
                messagebox.showerror("Error", "Lost Connection to the DB")
                break
        read_write.log_message("[INFO]" + LOG_NAME + "Search stopped successfully.")
        message = "[INFO]" + LOG_NAME + "Gathered " + str(tweet_count) + " tweets - Ignored "
        message += str(ignored_count) + " tweets"
        read_write.log_message(message)
        print("Search stopped successfully.")

    def stop(self):
        self.stop_thread.set()
        print("Stopping search...")
        self.search_thread = None

    def pause(self):
        self.pause_search = True

    def unpause(self):
        self.pause_search = False

    def get_pause_flag(self):
        return self.pause_search

# this controller, is initialized once the program starts, and we manage to handle the REST Search API
# through his methods
search_controller = SearchController()


# function to start the Search API
def start_search(frame):
    global search_controller  # get the instance in hands
    # check if user gave a keyword
    if frame.keyword_entry.get().strip(" ") is not "":
        # change the GUI into more favorable way
        frame.mng_search_btn.config(text="Stop Search", command=lambda: stop_search(frame))
        frame.pause_search_btn.grid()  # show the pause button
        frame.pause_search_btn.config(command=lambda: pause_unpause(frame))
        search_controller.search_keyword = frame.keyword_entry.get()  # and set the keyword into controller,
        search_controller.combine()  # to start the stream
    else:
        messagebox.showerror("Error", "Enter a keyword")


# function to stop the search thread
def stop_search(frame):
    global search_controller
    frame.mng_search_btn.config(text="Start Search", command=lambda: start_search(frame))
    frame.pause_search_btn.grid_remove()
    search_controller.stop()  # by calling the search controller


# function to handle the Pause/Un-pause button events
def pause_unpause(frame):
    global search_controller
    if search_controller.get_pause_flag():  # if flag is True, it means that we already paused the search
        search_controller.unpause()  # so un-pause it and change the GUI
        read_write.log_message("[INFO]" + LOG_NAME + "Search unpaused...")
        frame.pause_search_btn.config(text="Pause Search")
    else:
        # but if it false, it means we press the Pause Search button, so set it accordingly
        search_controller.pause()
        frame.pause_search_btn.config(text="Continue Search")
        read_write.log_message("[INFO]" + LOG_NAME + "Search paused...")
        print("Search paused...")
