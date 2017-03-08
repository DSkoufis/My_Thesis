from tweepy.streaming import StreamListener
from Utilities import client
from Utilities import database
import json


# we create this objects here, to have them in our hands during the "run" period and call them only once
db_client = database.get_client()
db_db = database.get_db(db_client, "test")
db_collection = database.get_collection(db_db, "test collection2")


# in this method we keep only the values we need from our tweet
def process_tweet(tweet):
    # see "anatomy of a tweet" for more details
    formatted_tweet = {"created_at": tweet["created_at"],
                       "favourite_count": tweet["favorite_count"],
                       "id_str": tweet["id_str"],
                       "lang": tweet["lang"],
                       "retweet_count": tweet["retweet_count"],
                       "text": tweet["text"],
                       "user": {
                           "favourites_count": tweet["user"]["favourites_count"],
                           "followers_count": tweet["user"]["followers_count"],
                           "friends_count": tweet["user"]["friends_count"],
                           "id_str": tweet["user"]["id_str"],
                           "statuses_count": tweet["user"]["statuses_count"],
                           "verified": tweet["user"]["verified"],
                       }}
    return formatted_tweet


# this method inserts the tweet into the active MongoDB instance
def store_tweet(tweet):
    print("A tweet has stored")
    db_collection.insert(tweet)


# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        data = json.loads(data)
        if "user" not in data:  # if tweet has no user, we don't want this tweet
            print("No user data - ignoring tweet.")
            return True
        if data["lang"] != "en":  # we deal only with English language text based tweets
            print("Tweet's language is not English - ignoring tweet.")
            return True
        our_tweet = process_tweet(data)  # we pass our data into this method to clean them and keep only the necessary
        store_tweet(our_tweet)  # we add our tweets into the active MongoDB instance
        return True

    def on_error(self, status):
        print(status)


listener = StdOutListener()
stream = client.set_stream(listener)  # this is the stream item, responsible to open the stream for us

# This line filter Twitter Streams to capture data by the given keywords
# TODO: change this by user's keyword
stream.filter(track=["basketball"])
