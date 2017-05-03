#######################################################################################
# Module that is responsible to connect to the REST API and gather the tweets #
#######################################################################################
from Utilities import db_utils, read_write, manage_credentials, other_utils
from tkinter import messagebox
from threading import Thread, Event
from tweepy import TweepError

LOG_NAME = "--> search_util.py"


class SearchController(object):
    def __init__(self):
        self.search_thread = None
        self.search_keyword = None

        self.pause_search = False

        self.stop_thread = Event()

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
        tweets_per_query = 100  # how many tweets we can ask for

        since_ID = None
        max_ID = -1

        tweet_count = 0  # this shows how many tweets have stored already

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
                    our_tweet = self.process_tweet(tweet)
                    if db_utils.store_tweet(our_tweet):
                        tweet_count += 1  # we count how many tweets we got

                # logging some info into console
                print("Saved {0} tweets till now".format(tweet_count))  # and we print them

                max_ID = new_tweets[-1].id  # we need to re - set the max_ID for the new search query
            except TweepError as error:
                print(LOG_NAME + " :: ERROR :: " + str(error))  # we log the error
                break
            except AttributeError as e:
                print(LOG_NAME + " :: ERROR :: " + str(e) + "\n" + LOG_NAME + " :: REASON :: Can't connect to server.")
                break
        print("Search stopped successfully.")

    # in this method we keep only the values we need from our tweet
    def process_tweet(self, tweet):
        # Fact: For a strange reason, in search mode, very few tweets have coordinates field.

        # clearing the text of a tweet into two lists
        cleared_text = other_utils.clear_text(tweet.text)

        # check if this tweet is a retweet
        if "RT" in cleared_text["stop_words"]:
            is_retweet = True
        else:
            is_retweet = False

        # see "anatomy of a tweet" for more details
        # IMPORTANT: tweepy.api.search method, returns SearchResult Object
        # we can't parse it like json, but it does the parsing itself for us
        # only thing remaining is to call it's values like that.
        # we again create the dictionary to store the document to MongoDB
        formatted_tweet = {"created_at": tweet.created_at,
                           "favourite_count": tweet.favorite_count,
                           "_id": tweet.id,
                           "retweet_count": tweet.retweet_count,
                           "text": cleared_text,
                           "whole_text": tweet.text,
                           "is_retweet": is_retweet,
                           "coordinates": tweet.coordinates,
                           "timestamp": other_utils.get_timestamp(),
                           "user": {
                               "favourites_count": tweet.user.favourites_count,
                               "followers_count": tweet.user.followers_count,
                               "friends_count": tweet.user.friends_count,
                               "id_str": tweet.user.id_str,
                               "statuses_count": tweet.user.statuses_count,
                               "verified": tweet.user.verified,
                               "created_at": tweet.user.created_at,
                               "geo_enabled": tweet.user.geo_enabled,
                               "location": tweet.user.location,
                               "time_zone": tweet.user.time_zone,
                               "utc_offset": tweet.user.utc_offset,
                           }}
        return formatted_tweet

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
        frame.pause_search_btn.config(text="Pause Search")
    else:
        # but if it false, it means we press the Pause Search button, so set it accordingly
        search_controller.pause()
        frame.pause_search_btn.config(text="Continue Search")
        print("Search paused...")
