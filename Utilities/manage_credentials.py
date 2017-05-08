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
        message_er = LOG_NAME + " :: ERROR :: " + str(error)
        message_fatal = LOG_NAME + " :: FATAL :: Error on credentials. Please check the credentials.json file."
        print(message_er)
        print(message_fatal)
        read_write.log_message(message_er)
        read_write.log_message(message_fatal)
        return None

    stream = Stream(auth, listener)  # and we setting the stream item
    return stream


def get_search():
    credentials = read_write.read_credentials()
    try:
        message = LOG_NAME + " :: INFO :: Trying to connect to Search API..."
        print(message)
        read_write.log_message(message)
        auth = AppAuthHandler(credentials["consumer_key"], credentials["consumer_secret"])
        api = API(auth_handler=auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        message = LOG_NAME + " :: INFO :: Connection successful"
        print(message)
        read_write.log_message(message)
        return api
    except Exception as e:
        message = LOG_NAME + " :: ERROR :: " + str(e)
        print(message)
        read_write.log_message(message)
