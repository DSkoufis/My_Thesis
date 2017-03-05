import json
import tweepy
from Utilities import client


def process_or_store(tweet):
    print(json.dumps(tweet))

api = client.set_api()

my_list = []
while True:
    try:
        for status in tweepy.Cursor(api.search, q="#NBA", lang="en", result_type="popular").items():
            process_or_store(status._json)
            my_list.append(json.dumps(status._json))
    except tweepy.RateLimitError:
        print("Rate Limit Error")
        print(len(my_list))
        continue
    except tweepy.TweepError as e:
        print(e.reason)
        print(len(my_list))
        continue