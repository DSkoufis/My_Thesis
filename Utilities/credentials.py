# ----------------------------
# This module is to handle the credentials from the credentials.txt
# ----------------------------

# This method reads the credentials of the credentials.txt and returns a dictionary with them
def read():
    try:
        credentials = {} # we will return this dictionary
        path = "../credentials.txt" # path to our file. It is in the parent directory by default
        with open(path, "r") as creds:
            content = creds.readlines()  # this holds all credentials into a long list

            # this line deletes the line break character from the list
            content = [line.strip("\n") for line in open(path)]
            print ("Reading credentials...")
    # handling the errors
    except IOError as e:
        print ("I/O error({0}): {1}".format(e.errno, e.strerror))
        return None
    except:
        print("Error on reading file")
        return None

    # go through the list one by one
    for line in content:
        # if there is an empty line or a line not well formatted we don't want our program to crash!
        # so it will gonna throw an exception in the split line, and we catch the exception
        # to continue our operation normally
        try:
            line_i = line.split(":")  # split the content into a smaller list
            # every line is in name:tokens format
            credentials[line_i[0]] = line_i[1]  # from the smaller list, add the 1st element
            # into the dictionary with the key of the 0th element
        except:
            continue

    print("Done!")
    return credentials # return the dictionary

# this method returns a tuple with the formal names of the credentials.txt fields
def set_names():
    names = ("consumer_key",
             "consumer_secret",
             "access_token",
             "access_token_secret",)
    return names

