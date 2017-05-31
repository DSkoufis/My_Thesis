##################################################################################################
# Module that is responsible to read the credentials and return the api item back to the program #
##################################################################################################
from Utilities import read_write
from tweepy import OAuthHandler, Stream, AppAuthHandler, API
import sys

# try:
#     from tweepy import OAuthHandler, Stream, AppAuthHandler, API
# except ImportError as e:
#     read_write.log_message("[FATAL] (manage_credentials) : ImportError: " + str(e))
#     sys.exit(str(e) + ". Please install this module to continue")


LOG_NAME = " (manage_credentials) : "


def get_stream(listener):
    credentials = read_write.read_credentials()

    try:
        auth = OAuthHandler(credentials["consumer_key"], credentials["consumer_secret"])
        auth.set_access_token(credentials["access_token"], credentials["access_token_secret"])
    except KeyError as error:
        message_er = "[ERROR]" + LOG_NAME + "KeyError : " + str(error)
        message_fatal = "[FATAL]" + LOG_NAME + "Error on credentials. Please check the credentials.json file."
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
        message = "[INFO]" + LOG_NAME + "Trying to connect to Search API..."
        print(message)
        read_write.log_message(message)
        auth = AppAuthHandler(credentials["consumer_key"], credentials["consumer_secret"])
        api = API(auth_handler=auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        message = "[INFO]" + LOG_NAME + "Connection successful"
        print(message)
        read_write.log_message(message)
        return api
    except Exception as e:
        message = "[ERROR]" + LOG_NAME + str(e)
        print(message)
        read_write.log_message(message)
