######################################################################
# Module that operates and is responsible for the MongoDB connection #
######################################################################
from tkinter import messagebox
from Utilities import frames, read_write
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConfigurationError, DuplicateKeyError

LOG_NAME = " (db_utils) : "

collection = None
database = None
client = None


def can_connect(frame):
    if isinstance(frame, frames.HostFrame):
        host = frame.host_entry.get()  # get the host number
        try:
            port = int(frame.port_entry.get())  # getting the port, if it is not an int, we will have en exception
        except ValueError as e:
            messagebox.showerror(title="Error", message="Port must be an integer", parent=frame.root)
            message = "[ERROR]" + LOG_NAME + "ValueError:" + str(e)
            print(message)
            read_write.log_message(message)
            return False

        try:  # try connect to the MongoDB
            connection = MongoClient(host=host, port=port, serverSelectionTimeoutMS=10000, tz_aware=True)
        except ConfigurationError as e:  # if host is not appropriate
            messagebox.showerror(title="Error", message=str(e), parent=frame.root)
            message = "[ERROR]" + LOG_NAME + "ConfigurationError:" + str(e)
            print(message)
            read_write.log_message(message)
            return False
        except TypeError as e:  # if port result to an error
            messagebox.showerror(title="Error", message=str(e), parent=frame.root)
            message = "[ERROR]" + LOG_NAME + "TypeError:" + str(e)
            print(message)
            read_write.log_message(message)
            return False

        # to see if we can connect to the MongoDB, we make a test query to see if we can write in it
        a_db = connection["a_name_that_no_one_ever_have_as_database_name_1982465"]
        a_collection = a_db["a_name_that_no_one_ever_have_as_collection_name_1982465"]

        try:  # we give the client, 10 seconds to connect
            read_write.log_message("[INFO]" + LOG_NAME + "Trying to connect to MongoDB with host: " +
                                   host + " and port: " + str(port))
            a_collection.insert({"test":1})
        except ServerSelectionTimeoutError as e:
            messagebox.showerror(title="Error", message="Can't connect", parent=frame.root)
            message = "[ERROR]" + LOG_NAME + "ServerSelectionTimeoutError:" + str(e)
            print(message)
            read_write.log_message(message)
            return False

        # if all OK, drop the test database
        connection.drop_database(a_db)
        # but make a global variable of the client, because we reference to it many times
        global client
        client = connection
        read_write.log_message("[INFO]" + LOG_NAME + "Successfully connected")
        return True


def store_tweet(tweet):
    global collection
    try:
        collection.insert(tweet)
        return True
    except DuplicateKeyError as e:
        message = "[ERROR]" + LOG_NAME + "DuplicateKeyError:" + str(e)
        print(message)
        return False


# this function, return the active MongoDB connection client
def get_client():
    global client
    return client


# getters and setters for database and collection
def set_database(name):
    global database
    database = name


def get_database():
    global database
    return database


def set_collection(name):
    global collection
    collection = name


def get_collection():
    global collection
    return collection
