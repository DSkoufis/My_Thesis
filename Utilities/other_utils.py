#####################################################################################################
# Module that is responsible to some useful functionality into the project like text tokenizing etc #
#####################################################################################################
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from datetime import datetime
import string
from pymongo.errors import ServerSelectionTimeoutError, AutoReconnect
from pymongo import TEXT
from tkinter import Toplevel, Listbox, messagebox, VERTICAL, S, N, E, W, TclError
from tkinter.ttk import Frame, Button, Entry, Label, Scrollbar, Sizegrip
from Utilities import read_write, db_utils
import re

LOG_NAME = "--> other_utils.py"

stops = stopwords.words('english')
punctuation = list(string.punctuation)
punctuation.append("''")
punctuation.append("``")
punctuation.append("—")
punctuation.append("…")
punctuation.append("...")
punctuation.append("--")
punctuation.append("..")
stops.extend(punctuation)
stops.append("rt")
alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
            "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

regexes = [
    re.compile('#.*'),  # finding hashtags
    re.compile('.*http[s]?://.*'),  # finding urls
    re.compile('@.*'),  # finding mentions
]


# function to clear the text of a tweet into two lists, one for text and one for stop_words
def clear_text(text):
    # building the lists or dictionaries that hold our data
    response = {}  # final object of response
    words = []  # this list holds all the meaningful words
    stop_words = []  # this list holds all the stop words
    punctuations = []  # this list holds all the punctuation marks
    characters_map = []  # this dictionary will hold how many times each character appears in the tweet
    entities = []  # this list holds all mentions, hastags and urls

    # tokenize the text into a list
    text = word_tokenize(text)

    # re-build the string because NLTK does not understand mentions or hashtags etc
    text = re_build_text(text)

    counter = 0
    for word in text:
        word = word.lower()
        counter += 1
        # tweets that are more than 140 characters, show … character at the end of the word
        # we choose, not to save these
        if len(word) > 1 and word.endswith("…"):
            continue

        # for some strange reason, "https" or "http" string escapes the clearing, so I excluded it manually
        if word == "https" or word == "http":
            continue

        # and distribute the word into the matching list
        if any(regex.match(word) for regex in regexes):
            entities.append(word)
        else:
            # find out how many times each alphabet character exists
            characters_map = map_characters(word, characters_map)
            if word not in stops:
                entry = {"value": word}
                words.append(entry)
            else:
                if word in punctuation:
                    punctuations.append(word)
                else:
                    stop_words.append(word)

    response["entities"] = entities
    response["characters_map"] = characters_map
    response["punctuation"] = punctuations
    response["words"] = words
    response["stop_words"] = stop_words

    return response


# function that maps into a list all the characters of a tweet, for later reference
# format is like: [ { "char" : "a", "value" : 4 }. { "char" : "b", "value" : 3 }, ... ]
# because this is better if we want to group them later
def map_characters(word, a_list):
    # this is a little complicated, so let's take it slowly
    # we create a dictionary, which will hold our characters
    # in format like { "a": 1, "b":4, ...}
    temp_dict = {}

    # we iterate through the word characters
    for char in word:
        if char in alphabet:  # and if this character is from the alphabet
            if char in temp_dict:  # and if this character already exists in this
                # temp dictionary, we increase it's value by 1
                temp_dict[char] += 1
            else:  # else, it is a new value,
                # so, add a new key, with value of 1
                temp_dict[char] = 1

    # now to get the format we want, we iterate through the keys
    for key in temp_dict:
        # and if we don't find the key, in any index of the list (remember how the list looks like?)
        if not any(d["char"] == key for d in a_list):
            # we create a new entry
            in_value = {"char": key, "value": temp_dict[key]}
            a_list.append(in_value)  # and add it to the list
        else:  # else if key already exists in the list
            for value in a_list:  # find it
                if value["char"] is key:  # and add 1 to it's value field
                    value["value"] += 1
                    break

    return a_list


# function that re-builds the tokens list, because some words are not acceptable by word_tokenizer of NLTK
# such as @mentions or #hashtags or https://urls
def re_build_text(text):
    escape_symbols = ["@", "#"]
    counter = 0
    for index in text:
        # building hashtags and mentions into one item
        if index in escape_symbols:
            try:
                index = index + text[counter + 1]
                text.remove(text[counter + 1])

                # if there is a : symbol, it connects with the previous word, that now is -1 indexes behind
                # because we removed the previous one
                if text[counter + 1] is ":":
                    index = index + ":"
                    text.remove(text[counter + 1])
            except IndexError:
                pass
            text[counter] = index  # save the index into the current item, but have the others removed
        # building the urls into one item
        elif index == "http" or index == "https":
            try:
                index += text[counter + 1]
                text.remove(text[counter + 1])
            except IndexError:
                pass
            try:
                index += text[counter + 1]
                text.remove(text[counter + 1])
            except IndexError:
                pass
            text[counter] = index
        # building n't endings, into one item with previous one
        elif index == "n't":
            # if previous word ends with vowel, add the "n" at the end of the word
            if text[counter - 1][-1:] in ["a", "e", "i", "o", "u"]:
                text[counter - 1] = text[counter - 1] + "n"
            text[counter] = "not"
        elif index == "'re":
            text[counter] = "are"

        counter += 1

    return text


# function that returns the current datetime. I do it here, because this is needed in
# search and stream utils
def get_timestamp():
    now = datetime.now()
    now = now.replace(microsecond=0)
    return now


# this function will create a new text index for the given collection
def create_text_index(collection):
    collection.create_index([("whole_text", TEXT)])
    read_write.log_message(LOG_NAME + " :: INFO :: Text index created for collection: " + collection.name)


# this function is used if user creates an index. We replace the old frame with the new one, that let the user
# search for a keyword after we create a text index for this collection
def change_frames(collection, frame, root):
    try:
        create_text_index(collection)
    except AutoReconnect as e:
        # if we have disconnected from the DB, return
        read_write.log_message(LOG_NAME + " :: ERROR :: AutoReconnect:" + str(e))
        messagebox.showerror("Error", "Lost Connection to the DB")
        return
    frame.destroy()
    pack_has_index_frame(root)


# we use this function every time we want to pack the HasIndexFrame. This is used in stats_utils too, so that's why
# I made it
def pack_has_index_frame(root):
    frame = HasIndexFrame(root)  # we get the frame
    frame.search_btn.config(command=lambda: search_in_db(frame, root))
    frame.pack()


# this function is called when user clicks on the search DB button from the "search tweets" window
# it gets the value of the entry and executes the query. At the end, if results are too many, informs the user
def search_in_db(frame, root):
    collection = db_utils.get_collection()

    keyword = frame.keyword_entry.get()
    # if user don't specified a keyword, show an error and return
    if keyword.strip(" ") is "":
        messagebox.showerror("Error", "You must specify a keyword")
        return

    # query = {"$text": {"$search": '"' + keyword + '"'}}
    # projection = ({"whole_text": 1, "_id": 0})
    # results = collection.find(query, projection)  # perform a find query in the collection
    read_write.log_message(LOG_NAME + " (search_in_db) :: INFO :: Searching db for " + keyword)
    pipeline = [{"$match":
                     {"$text":
                          {"$search": '"' + keyword + '"'
                           }
                      }
                 },
                {"$group":
                     {"_id": "$whole_text"
                      }
                 },
                {"$count": "count"
                 }]
    try:
        # this returns how many different results we have {"count": 2045}
        results = collection.aggregate(pipeline)
    except ServerSelectionTimeoutError as e:
        # if we have disconnected from the DB, return
        read_write.log_message(LOG_NAME + " :: ERROR :: AutoReconnect:" + str(e))
        messagebox.showerror("Error", "Lost Connection to the DB")
        return

    results_count = 0  # his is for safety, if results are empty
    # the only drawback of the aggregation is that we cannot count the results by calling .count()
    # it is just an iterable cursor, with dictionary
    # although these kind of queries are very fast
    for item in results:
        results_count = item["count"]

    # we show the results, if we have any, in a new window
    if 0 < results_count:
        read_write.log_message(LOG_NAME + " :: INFO :: Found %d results" % results_count)
        # getting the results to show them
        pipeline = [{"$match":
                         {"$text":
                              {"$search": '"' + keyword + '"'
                               }
                          }
                     },
                    {"$group":
                         {"_id": "$whole_text"
                          }
                     }]
        # this returns the different results
        results = collection.aggregate(pipeline)
        show_results(results, results_count, root)
    else:
        messagebox.showinfo("Empty", "No results found for " + keyword + "!")
        message = LOG_NAME + " :: WARNING :: No results found for " + keyword
        read_write.log_message(message)


def show_results(results, results_count, root):
    # we start the toplevel
    top_level = Toplevel(root)
    top_level.minsize(800, 400)
    read_write.set_favicon(top_level)
    top_level.title("-- Twitter API --  search results")

    # because frames don't have scrollbars, we place the results into a listbox
    # solution found on the tkinter documentation
    # http://www.tkdocs.com/tutorial/morewidgets.html#scrollbar
    l = Listbox(top_level, height=5)
    l.grid(column=0, row=0, sticky=(N, W, E, S))
    s = Scrollbar(top_level, orient=VERTICAL, command=l.yview)
    s.grid(column=1, row=0, sticky=(N, S))
    l['yscrollcommand'] = s.set
    Sizegrip(top_level).grid(column=1, row=1, sticky=(S, E))
    top_level.grid_columnconfigure(0, weight=1)
    top_level.grid_rowconfigure(0, weight=1)

    # messages to inform the user
    message = "######     Found %d unique results in the DB     ######" % results_count
    l.insert('end', message)
    l.insert('end', ' ')

    # we show the results
    counter = 1  # counter to keep track of the lines
    for tweet in results:
        # we only show the first 1000 results
        if counter <= 1000:
            # there are times that text is not Unicode formatted, show we catch the exception
            try:
                # we try to insert the text into the listbox
                l.insert('end', "%d  ->> " % counter + tweet["_id"])
                counter += 1
            except TclError as e:
                read_write.log_message(LOG_NAME + " (show_results) :: WARN :: TclError:" + str(e))
                pass
        else:
            # if we show 1000 tweets, inform the user how many we didn't show
            remaining = results_count - counter
            message = "######     Remaining %d " % remaining + "more tweets. "
            message += "Too many to show them!     ######"
            l.insert('end', ' ')
            l.insert('end', message)
            break

    top_level.mainloop()


# two classes here, to use them in the "search tweets" pane. We can't use them in frames.py, because of the imports
class NoIndexFrame(Frame):
    def __init__(self, master):
        super(NoIndexFrame, self).__init__(master)
        root = master

        main_frm = Frame(self)
        main_frm.grid(row=0, column=0, pady=20)
        exit_frm = Frame(self)
        exit_frm.grid(row=2, column=0, pady=10)

        Label(main_frm, text="No text index have been created. You must\ncreate one to search the collection"). \
            grid(row=1, column=0, padx=10, pady=5)
        self.create_index_btn = Button(main_frm, text="Create index")
        self.create_index_btn.grid(row=2, column=0, pady=15, ipadx=3, ipady=2)

        # Build the widget for exit_frm
        exit_btn = Button(exit_frm, text="Exit", command=root.destroy)
        exit_btn.grid(row=0, column=3, ipadx=5, ipady=3, padx=15, pady=10)


class HasIndexFrame(Frame):
    def __init__(self, master):
        super(HasIndexFrame, self).__init__(master)
        root = master

        main_frm = Frame(self)
        main_frm.grid(row=0, column=0, pady=20)
        exit_frm = Frame(self)
        exit_frm.grid(row=2, column=0, pady=10)

        Label(main_frm, text="Enter search phrase\nor keywords:").grid(row=0, column=0, padx=20, pady=10)
        self.keyword_entry = Entry(main_frm, width=30)
        self.keyword_entry.grid(column=1, row=0, pady=10)

        self.search_btn = Button(main_frm, text="Search DB")
        self.search_btn.grid(column=0, columnspan=2, row=1, padx=10, ipadx=3, ipady=2)

        # Build the widget for exit_frm
        exit_btn = Button(exit_frm, text="Exit", command=root.destroy)
        exit_btn.grid(row=0, column=3, ipadx=5, ipady=3, padx=15, pady=10)
