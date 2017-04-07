from tweepy.streaming import StreamListener
from Utilities import client
from Utilities import database
from datetime import datetime
import json

# this flags variables hold the boolean values to terminate or pause the stream.
# When we call this var from streaming_window, we change this value into True to start the stream
stop_flag = False  # If this become False, stream closes (Authentication needed again)
pause_flag = False  # If this become False, stream pause (No need to re-authenticate when start)


# getters and setters for the flags
def get_stop_flag():
    return stop_flag


def set_stop_flag(value):
    global stop_flag
    stop_flag = value


def get_pause_flag():
    return pause_flag


def set_pause_flag(value):
    global pause_flag
    pause_flag = value


# this method starts the streaming API. To finish it, just make it's stop_flag variable equals False
# It gets as an argument the search keyword that the user gives
def streaming_proc(search_keyword):
    # we are getting in our hands the collection to save incoming data
    db_collection = database.get_collection()

    # in this method we keep only the values we need from our tweet
    def process_tweet(tweet):
        # see "anatomy of a tweet" for more details
        formatted_tweet = {"created_at": datetime.strptime(tweet["created_at"], "%a %b %d %H:%M:%S %z %Y"),
                           "favourite_count": tweet["favorite_count"],
                           "id_str": tweet["id_str"],
                           "retweet_count": tweet["retweet_count"],
                           "text": tweet["text"],
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

    # this method inserts the tweet into the active MongoDB instance that is passed through arguments
    def store_tweet(tweet):
        print("A tweet has stored")
        db_collection.insert(tweet)

    # This is a basic listener that just prints received tweets to stdout.
    class StdOutListener(StreamListener):
        def on_data(self, data):
            if not get_stop_flag():  # check if the stop_flag value became False.
                return False  # if yes, then return False to terminate the streaming loop
            if not get_pause_flag():
                return True  # if user wants to pause, don't do anything with new data
            data = json.loads(data)
            if "user" not in data:  # if tweet has no user, we don't want this tweet
                print("No user data - ignoring tweet.")
                return True
            if data["lang"] != "en":  # we deal only with English language text based tweets
                print("Tweet's language is not English - ignoring tweet.")
                return True
            # we pass our data into this method to clean them and keep only the necessary
            our_tweet = process_tweet(data)
            store_tweet(our_tweet)  # we add our tweets into the active MongoDB instance
            return True

        def on_error(self, status):
            print(status)

    listener = StdOutListener()
    stream = client.set_stream(listener)  # this is the stream item, responsible to open the stream for us

    # This line filter Twitter Streams to capture data by the given keywords
    print("Searching Twitter for '" + search_keyword + "'.")
    stream.filter(track=[search_keyword])


