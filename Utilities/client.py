from Utilities import credentials
import tweepy


# this method gets the credentials from Utilities.credentials.py and save them at a dictionary named creds
def get_credentials():
    creds = credentials.read()  # this is a dictionary that holds the credentials
    return creds


# this method returns oauth item for authentication
def set_oath():
    creds = get_credentials()  # we get the credentials to our hands
    # we make the authentication
    auth = tweepy.OAuthHandler(creds["consumer_key"], creds["consumer_secret"])
    auth.set_access_token(creds["access_token"], creds["access_token_secret"])
    return auth


# this method returns an App OAuth item for better API call rate limit
def set_app_oath():
    creds = get_credentials()  # we get the credentials
    # and we authenticate
    auth = tweepy.AppAuthHandler(creds["consumer_key"], creds["consumer_secret"])
    return auth


# this method returns a Stream item for our StreamListener class. It is used to get API_calls API_calls
def set_stream(listener):
    auth = set_oath() # we make the authentication
    stream = tweepy.Stream(auth, listener) # and we setting the stream item
    return stream


def set_api():
    auth = set_app_oath()
    # the last 2 arguments, let tweepy to handle rate limit errors and just notify us
    # this makes the process easier for us!
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api
