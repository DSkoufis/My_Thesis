import json
import tweepy
from Utilities import client
from Utilities import database


# TODO: move these 3 lines into calling module, to let user select his own values
# IMPORTANT: keep the same names though (db_client etc)
# we create this objects here, to have them in our hands during the "run" period and call them only once
db_client = database.get_client()
db_db = database.get_db(db_client, "test")
db_collection = database.get_collection(db_db, "search collection")

# we are getting a reference into API item
api = client.set_api()

# TODO: Left here, continue from here
# see http://www.karambelkar.info/2015/01/how-to-use-twitters-search-rest-api-most-effectively./
# to continue

# this just prints the tweets
# TODO: I don't really need this
def process_or_store(tweet):
    print(json.dumps(tweet))


# TODO: this is for demonstration, I must change it
# in this example, we are getting older tweets, until we hit rate limit. Then we just continue looping
my_list = []
while True:
    # if I reach rate limit, Cursor throws an RateLimitError exception, so we catch it
    try:
        for tweet in tweepy.Cursor(api.search, q="#NBA", lang="en", result_type="popular").items():
            process_or_store(tweet._json)
            my_list.append(json.dumps(tweet._json))
    except tweepy.TweepError as e: # this exception is both TweepError and RateLimitError
        print(e.reason)
        print(len(my_list))
        continue
