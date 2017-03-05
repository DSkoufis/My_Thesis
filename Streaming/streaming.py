from tweepy.streaming import StreamListener
from Utilities import client


# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


listener = StdOutListener()
stream = client.set_stream(listener) # this is the srteam item, responsible to open the stream for us

# This line filter Twitter Streams to capture data by the given keywords
# TODO: change this by user's keyword
stream.filter(track=['basketball'])
