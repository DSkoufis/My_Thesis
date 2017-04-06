import pymongo
import json


# this method returns a MongoClient object. This is the db connection in other words
def get_client(host, port):
    client = pymongo.MongoClient(host=host, port=port)
    # MongoClient throws TypeError, InvalidURI, ConfigurationError, OperationFailure, ConnectionFailure
    # etc
    return client


# this method gets a MongoClient item as first argument and a string with a db name as second.
# it returns a db with the given name. If it doesn't exists, it creates one and it returned
def get_db(client, db_name):
    db = client[db_name]
    return db


# this method returns a specific collection of a MongoDB database. If it doesn't exists, it creates one
def get_collection(db_name, collection_name):
    collection = db_name[collection_name]
    return collection

# reading the data from the mongo.json file which stores values regarding MongoDB connection
with open("mongo.json") as data_file:
    data = json.load(data_file)

# these are used from other modules that make use of database.py
host = data["host"]
port = data["port"]
database = data["database"]  # we get the database name into hands
collection = data["collection"]  # we get collection's name into hands
db_client = get_client(host=host, port=port)  # we initialize the database client
db_name = get_db(db_client, database)  # we initialize the database
db_collection = get_collection(db_name, collection)  # we initialize the collection
