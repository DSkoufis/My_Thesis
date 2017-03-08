import pymongo


# this method returns a MongoClient object. This is the db connection in other words
# TODO: add args (user selection of host and port)
def get_client():
    client = pymongo.MongoClient("localhost", 27017)
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

