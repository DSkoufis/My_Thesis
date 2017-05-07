###############################################################
# Module that is responsible to write or read data from files #
###############################################################
import json
import os

LOG_NAME = "--> read_write.py"

file_path = os.path.abspath("Ufiles")


# function that returns the data in json format from mongo.json file
def read_mongo():
    try:
        with open(os.path.abspath(file_path + "/mongo.json")) as datafile:
            data = json.load(datafile)
    except FileNotFoundError as fe:
        print(LOG_NAME + " :: ERROR :: FileNotFoundError:" + str(fe))
        data = []
    return data


# function that returns the data in json format from last.json file
def read_last():
    try:
        with open(os.path.abspath(file_path + "/last.json")) as datafile:
            data = json.load(datafile)
    except FileNotFoundError as fe:
        print(LOG_NAME + " :: ERROR :: FileNotFoundError:" + str(fe))
        data = {}
    return data


# function that reads and returns the data from keywords.json file
def read_keywords():
    try:
        with open(os.path.abspath(file_path + "/keywords.json")) as datafile:
            data = json.load(datafile)
    except FileNotFoundError as fe:
        print(LOG_NAME + " :: ERROR :: FileNotFoundError:" + str(fe))
        data = []
    return data


# function that read credentials from credentials.json
def read_credentials():
    try:
        with open(os.path.abspath(file_path + "/credentials.json")) as datafile:
            credentials = json.load(datafile)
    except FileNotFoundError as fe:
        print(LOG_NAME + " :: ERROR :: FileNotFoundError:" + str(fe))
        credentials = {}
    return credentials


# function that writes the data in mongo.json file
def write_mongo(data):
    with open(os.path.abspath(file_path + "/mongo.json"), "w") as outfile:
        json.dump(data, outfile, sort_keys=True, indent=2)


# function that writes the data in last.json file
def write_last(data):
    with open(os.path.abspath(file_path + "/last.json"), "w") as outfile:
        json.dump(data, outfile, sort_keys=True, indent=2)


# function that writes the data in keywords.json file
# Unlike the other functions, this counts the length of the list, because we store only the 10 last keywords
def write_keywords(data):
    keywords = read_keywords()
    if data in keywords:  # if the keyword is already in the file
        return
    # we use a while loop, to catch if user enter manually some keywords in the json file
    while len(keywords) >= 10:  # if we have 10 keywords stored
        keywords.pop()  # pop the last out
    keywords.insert(0, data)  # and insert in the first position the new one
    with open(os.path.abspath(file_path + "/keywords.json"), "w") as outfile:
        json.dump(keywords, outfile, sort_keys=False, indent=2)


# function that gets as argument a window and sets a favicon to it
def set_favicon(root):
    root.iconbitmap(os.path.abspath("favicon.ico"))
