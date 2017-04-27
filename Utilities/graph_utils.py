import matplotlib.pyplot as plt
import numpy as np
from Utilities import db_utils, other_utils


# this function shows a distribution of collected letters
def show_letter_distro():
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
