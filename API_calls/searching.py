import tweepy
from Utilities import client
from Utilities import database

# TODO: make this callable from a GUI window
# as long as flag equals True, API runs
flag = True

# TODO: move these 3 lines into calling module, to let user select his own values
# IMPORTANT: keep the same names though (db_client etc)
# we create this objects here, to have them in our hands during the "run" period and call them only once
db_client = database.get_client()
db_db = database.get_db(db_client, "test")
db_collection = database.get_collection(db_db, "search collection")

# we are getting a reference into API item
api = client.set_api()

query = "trump"  # TODO: let the user pick this
tweets_per_query = 100  # how many tweets we can ask for

since_ID = None
max_ID = -1

tweet_count = 0  # this shows how many tweets have stored already


# in this method we keep only the values we need from our tweet
def process_tweet(tweet):
    # see "anatomy of a tweet" for more details
    # IMPORTANT: tweepy.api.search method, returns SearchResult Object
    # we can't parse it like json, but it does the parsing itself for us
    # only thing remaining is to call it's values like that.
    # we again create the dictionary to store the document to MongoDB
    formatted_tweet = {"created_at": tweet.created_at,
                       "favourite_count": tweet.favorite_count,
                       "id_str": tweet.id_str,
                       "retweet_count": tweet.retweet_count,
                       "text": tweet.text,
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


# this method inserts the tweet into the active MongoDB instance that is passed through arguments
def store_tweet(tweet):
    db_collection.insert(tweet)

while flag:
    try:
        if max_ID <= 0:
            if not since_ID:
                new_tweets = api.search(q=query, count=tweets_per_query, lang="en",)
            else:
                new_tweets = api.search(q=query, count=tweets_per_query, lang="en", since_id=since_ID)
        else:
            if not since_ID:
                new_tweets = api.search(q=query, count=tweets_per_query, lang="en", max_id=str(max_ID - 1))
            else:
                new_tweets = api.search(q=query, count=tweets_per_query, lang="en",
                                        max_id=str(max_ID - 1), since_id=since_ID)

        if not new_tweets:
            print("No more tweets found!")
            flag = False
            break

        # logging some info into console
        tweet_count += len(new_tweets)
        print("Downloaded {0} tweets till now".format(tweet_count))
        print("Storing them in DB...")

        # after many tests (near 30.000 tweets sample)
        # I found out that language is always "en" and all tweets have user data.
        # so there is no reason to validate here our data like we do in streaming.py
        # We can store them immediately
        # =======================================================================================#
        for tweet in new_tweets:
            # we pass our data into this method to clean them and keep only the necessary
            our_tweet = process_tweet(tweet)
            store_tweet(our_tweet)  # we add our tweets into the active MongoDB instance

        print("Store complete.")
        max_ID = new_tweets[-1].id
    except tweepy.TweepError as error:
        print("Error: " + str(error))
        flag = False
        break

