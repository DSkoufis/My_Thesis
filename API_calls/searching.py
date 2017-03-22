import tweepy
from Utilities import client
from Utilities import database

# this flag value holds the boolean value for the while loop
# that is responsible to call the Search API and get new tweets
flag = False


# we declare getter and setter to handle the value of our flag
def get_flag():
    return flag


def set_flag(value):
    global flag
    flag = value


def searching_proc(keyword):
    # we get the collection to add our documents
    db_collection = database.db_collection

    # we are getting a reference into API item
    api = client.set_api()

    query = keyword  # this is the keyword that user typed
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

    while get_flag():  # flag is True when we start this function from the search window
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
                # if we don't get any new tweets
                print("No more tweets found!")
                set_flag(False)  # and we setting the flag that is responsible for while loop
                break

            # logging some info into console
            tweet_count += len(new_tweets)  # we count how many tweets we got
            print("Downloaded {0} tweets till now".format(tweet_count))  # and we print them
            print("Storing them in DB...")

            # after many tests (near 30.000 tweets collection sample)
            # I found out that language is always "en" and all tweets have user data.
            # so there is no reason to validate here our data like we do in streaming.py
            # We can store them immediately
            # =======================================================================================#
            for tweet in new_tweets:
                # we pass our data into this method to clean them and keep only the necessary data
                our_tweet = process_tweet(tweet)
                store_tweet(our_tweet)  # we add our tweets into the active MongoDB instance

            print("Store complete.")
            max_ID = new_tweets[-1].id  # we need to re - set the max_ID for the new search query
        except tweepy.TweepError as error:
            print("Error: " + str(error))  # we log the error
            set_flag(False)  # and we setting the flag that is responsible for while loop
            break

