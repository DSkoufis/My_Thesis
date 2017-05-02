import matplotlib.pyplot as plt
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
def show_tz_distribution(more_than, less_than, exclude_list):
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
        if item["_id"] not in exclude_list:
            if item["sum"] > more_than:
                if item["sum"] < less_than:
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
