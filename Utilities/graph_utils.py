import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from Utilities import db_utils, other_utils
from operator import itemgetter


# this function shows a distribution of collected letters
def show_letter_distribution():
    collection = db_utils.get_collection()

    # this is what we request from the MongoDB, we use the aggregation framework
    pipeline = [{"$unwind": "$text.characters_map"},
                {"$group": {"_id": "$text.characters_map.char",
                            "counter": {"$sum": "$text.characters_map.value"}
                            }
                 }]
    results = collection.aggregate(pipeline)  # we get the cursor
    all_results = {}  # this is where the results will be
    # we couldn't keep the results, because we can't use a cursor

    for item in results:
        # we add all results into the new dictionary
        # results are in the format [{"_id": "a", "counter": 4}, ... ]
        all_results[item["_id"]] = item["counter"]

    alphabet = other_utils.alphabet

    my_xticks = []  # this will be needed to show letters instead of numbers in x axis
    population = []  # this is the amount of occurrences of every letter
    bins = []  # this is the x axis ( in plt, we must use numbers for axis, so we convert them later into letters )
    counter = 1  # this will help us, to have same amount on both x and y axis

    # we sort our data to appear in alphabetical order
    for letter in alphabet:
        # if any of the keys of all_results dictionary is equal as the current letter
        # ( we do this, because if user have a very small sample, not all letters may have caught )
        if any(d == letter for d in all_results):
            population.append(all_results[letter])  # we save the number
            bins.append(counter)  # we add a number(letter) every time we save a number
            counter += 1
            my_xticks.append(letter)

    x = np.array(bins)
    y = np.array(population)

    plt.xticks(x, my_xticks)
    plt.plot(x, y)
    plt.show()


# this function shows a plot, with the time zones in the x axis and the number of tweets of each time zone in y axis
# @param more_than, a value that indicates from which value and above we keep our results
# @param less_than, a value that indicates from which value and downwards we keep our results
# @param exclude_list, a list which holds all time zones values, that the user wants to exclude from the final graph
def show_tz_distribution(exclude_more_than, exclude_less_than, exclude_list, include_list):
    collection = db_utils.get_collection()

    # this is what we request from the MongoDB, we use the aggregation framework
    pipeline = [{"$unwind": "$user.time_zone"},
                {"$group": {"_id": "$user.time_zone",
                            "sum": {"$sum": 1}
                            }
                 }]

    results = collection.aggregate(pipeline)  # we get the cursor from the database

    # in here we store all results, because PyMongo returns us a cursor
    all_results_list = []

    for item in results:
        # the results from the aggregation are in the format: [{"_id": "time zone name", "sum": 208"}, ... ]
        # with this for, we store all data in the all_results dictionary like above,
        # because we need a list, to be able to sort our data
        # we must clear the data, if user applied filter in here
        # so if item is in exclude list, do not calculate anything
        if item["_id"] not in exclude_list:
            # but if it is not in exclude list, check if it is in include list
            # before clear it with more_than and less_than borders
            if item["_id"] in include_list:
                all_results_list.append(item)
            else:
                if item["sum"] > exclude_less_than:
                    if item["sum"] < exclude_more_than:
                        all_results_list.append(item)

    # sort the list by sum number in descending order
    all_results_sorted = sorted(all_results_list, key=itemgetter("sum"), reverse=True)

    time_zones = []  # this list holds all time zones after the sorting
    values = []  # this list holds all sum values of each time zone after the sorting
    for item in all_results_sorted:
        time_zones.append(item["_id"])
        values.append(item["sum"])

    y_pos = np.arange(len(time_zones))

    plt.bar(y_pos, values, color='r', align='center', alpha=0.5)
    plt.xticks(y_pos, time_zones, rotation=45)  # rotate the strings 45 degrees
    plt.ylabel("Number of tweets")
    plt.title("Number of tweets per time zone")
    plt.show()


# this functions, queries the DB and gets all the documents that has as 'coordinates' field != null. It creates a
# map, using the Basemap extension library and it paints in every location a point which represents the coordinate
# of each tweet, according to the Twitter response.
def show_coordinates_map():
    collection = db_utils.get_collection()

    # we query the db and get the results
    results = collection.find({"coordinates.coordinates":
                                   {"$ne": None}
                               },
                              {"coordinates": 1,
                               "_id": 0})

    # creating the map
    m = Basemap(projection='mill',
                llcrnrlat=-90,
                llcrnrlon=-180,
                urcrnrlat=90,
                urcrnrlon=180,
                resolution='c')

    m.drawcoastlines(linewidth=1)
    m.drawcountries(linewidth=0.5)

    # we iterate with the cursor and we save every element on the plot
    for coordinate in results:
        lon = coordinate["coordinates"]["coordinates"][0]  # we need longitude
        lat = coordinate["coordinates"]["coordinates"][1]  # and latitude
        xpt, ypt = m(lon, lat)
        m.plot(xpt, ypt, 'ro', markersize=2)  # and we create the point on the map

    sample_sum = str(results.count())
    plt.title("Results of " + sample_sum + " tweets sample.")
    plt.show()


# function that is responsible to show a graph with word distribution after applying the desired filters
def show_word_distribution(exclude_more_than, exclude_less_than, exclude_word_list, include_word_list):
    collection = db_utils.get_collection()

    # this is what we request from the MongoDB, we use the aggregation framework
    pipeline = [{"$unwind": "$text.words"},
                {"$group": {"_id": "$text.words.value",
                            "counter": {"$sum": 1}
                            }
                 }]

    results = collection.aggregate(pipeline)  # we get the cursor from the database

    # in here we store all results, because PyMongo returns us a cursor
    all_results_list = []

    for word in results:
        # the results from the aggregation are in the format: [{"_id": "a word", "sum": 208"}, ... ]
        # with this for, we store all data in the all_results dictionary like above,
        # because we need a list, to be able to sort our data
        # we must clear the data, if user applied filter in here
        # so if item is in exclude list, do not calculate anything
        if word["_id"] not in exclude_word_list:
            # but if it is not in exclude list, check if it is in include list
            # before clear it with more_than and less_than borders
            if word["_id"] in include_word_list:
                all_results_list.append(word)
            else:
                if word["counter"] > exclude_less_than:
                    if word["counter"] < exclude_more_than:
                        all_results_list.append(word)

    # sort the list by sum number in descending order
    all_results_sorted = sorted(all_results_list, key=itemgetter("counter"), reverse=True)

    all_words = []  # this list holds all words after the sorting
    values = []  # this list holds all counter values of each word after the sorting
    for word in all_results_sorted:
        all_words.append(word["_id"])
        values.append(word["counter"])

    y_pos = np.arange(len(all_words))

    plt.bar(y_pos, values, color='g', align='center', alpha=0.5)
    plt.xticks(y_pos, all_words, rotation=45)  # rotate the strings 45 degrees
    plt.ylabel("Number of occurrences in tweets")
    plt.title("Words occurrences")
    plt.show()
