from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from Utilities import credentials

creds = credentials.read() # this is a dictionary that holds the credentials
creds_names = credentials.set_names() # this is a tuple that holds some strings with formal names

# we gather our credential tokens into these variable to authenticate with twitter API
consumer_key = creds[creds_names[0]]
consumer_secret = creds[creds_names[1]]
access_token = creds[creds_names[2]]
access_token_secret = creds[creds_names[3]]


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the given keywords
    # TODO: change this by user's keyword
    stream.filter(track=['basketball'])

