##################################################################################################
# Module that is responsible to read the credentials and return the api item back to the program #
##################################################################################################
from tweepy import OAuthHandler, Stream, AppAuthHandler, API
from Utilities import read_write

LOG_NAME = "--> manage_credentials.py"


def get_stream(listener):
    credentials = read_write.read_credentials()

    try:
        auth = OAuthHandler(credentials["consumer_key"], credentials["consumer_secret"])
        auth.set_access_token(credentials["access_token"], credentials["access_token_secret"])
    except KeyError as error:
        print(LOG_NAME + " :: ERROR :: " + str(error))
        print(LOG_NAME + " :: FATAL :: Error on credentials. Please check the credentials.json file.")
        return None

    stream = Stream(auth, listener)  # and we setting the stream item
    return stream


def get_search():
    credentials = read_write.read_credentials()
    try:
        print(LOG_NAME + " :: INFO :: Trying to connect to Search API...")
        auth = AppAuthHandler(credentials["consumer_key"], credentials["consumer_secret"])
        api = API(auth_handler=auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        print(LOG_NAME + " :: INFO :: Connection successful")
        return api
    except Exception as e:
        print(LOG_NAME + " :: ERROR :: " + str(e))
