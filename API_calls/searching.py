import json
import tweepy
from Utilities import client


# this just prints the tweets
# TODO: I don't really need this
def process_or_store(tweet):
    print(json.dumps(tweet))

# we are getting a reference into API item
api = client.set_api()

# TODO: this is for demonstration, I must change it
# in this example, we are getting older tweets, until we hit rate limit. Then we just continue looping
my_list = []
while True:
    # if I reach rate limit, Cursor throws an RateLimitError exception, so we catch it
    try:
        for status in tweepy.Cursor(api.search, q="#NBA", lang="en", result_type="popular").items():
            process_or_store(status._json)
            my_list.append(json.dumps(status._json))
    except tweepy.TweepError as e: # this exception is both TweepError and RateLimitError
        print(e.reason)
        print(len(my_list))
        continue
