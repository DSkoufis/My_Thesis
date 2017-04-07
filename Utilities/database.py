import pymongo
import json


# TODO: make one global client, database and collection that are served to the world through getters and setters

# this method returns a MongoClient object. This is the db connection in other words
def return_client(host, port):
    client = pymongo.MongoClient(host=host, port=port)
    # MongoClient throws TypeError, InvalidURI, ConfigurationError, OperationFailure, ConnectionFailure
    # etc
    return client


# this method gets a MongoClient item as first argument and a string with a db name as second.
# it returns a db with the given name. If it doesn't exists, it creates one and it returned
def return_db(client, db_name):
    db = client[db_name]
    return db


# this method returns a specific collection of a MongoDB database. If it doesn't exists, it creates one
def return_collection(db_name, collection_name):
    collection = db_name[collection_name]
    return collection


# function to read mongo.json data and return our collection
def init_connection():
    # reading the data from the mongo.json file which stores values regarding MongoDB connection
    with open("mongo.json") as data_file:
        data = json.load(data_file)

    # these are used from other modules that make use of database.py
    host = data["host"]
    port = data["port"]
    database = data["database"]  # we get the database name into hands
    collection = data["collection"]  # we get collection's name into hands
    db_client = return_client(host=host, port=port)  # we initialize the database client
    db_name = return_db(db_client, database)  # we initialize the database
    db_collection = return_collection(db_name, collection)  # we initialize the collection
    return db_collection


# simple function to return the collection to stream or search windows
def get_collection():
    return init_connection()
