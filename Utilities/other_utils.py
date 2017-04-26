from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import re

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
    characters_map = {}  # this dictionary will hold how many times each character appears in the tweet
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
                words.append(word)
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


# function that maps into a dictionary all the characters of a tweet, for later reference
def map_characters(text, map_):
    for char in text:
        if char in alphabet:
            if char in map_:
                map_[char] += 1
            else:
                map_[char] = 1
    return map_


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
