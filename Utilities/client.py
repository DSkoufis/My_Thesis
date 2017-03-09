from Utilities import credentials
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy


# this method gets the credentials from Utilities.credentials.py and save them at a dictionary named creds
def get_credentials():
    creds = credentials.read()  # this is a dictionary that holds the credentials
    return creds


# this method returns oauth item for authentication
def set_oath():
    creds = get_credentials()  # we get the credentials to our hands
    # we make the authentication
    auth = OAuthHandler(creds["consumer_key"], creds["consumer_secret"])
    auth.set_access_token(creds["access_token"], creds["access_token_secret"])
    return auth


# this method returns a Stream item for our StreamListener class. It is used to get Streaming API calls
def set_stream(listener):
    auth = set_oath() # we make the authentication
    stream = Stream(auth, listener) # and we setting the stream item
    return stream


def set_api():
    auth = set_oath()
    return tweepy.API(auth)
