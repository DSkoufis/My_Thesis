########################################################################
# Module that is responsible to show windows to let user apply filters #
# before show the graphs and calculate the data for these graphs       #
########################################################################
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from Utilities import graph_utils, read_write

LOG_NAME = "--> stats_util.py"


# function that builds a TopLevel Window to let user exclude some values from tweets/time_zone graph
def show_tweets_per_tz_graph(root):
    # we start the toplevel
    top_level = Toplevel(root)
    top_level.minsize(400, 200)
    read_write.set_favicon(top_level)
    top_level.title("-- Twitter API --  time zones graph")

    # in this we will have a labelframe to exclude
    exclude_frm = Labelframe(top_level, text="Exclude patterns")
    exclude_frm.pack(side=TOP, padx=5, pady=10, fill=X)

    Label(exclude_frm, text="Exclude values more than:").grid(row=0, column=0, padx=10, pady=2, sticky=W)
    exclude_more_than_entry = Entry(exclude_frm, width=30)
    exclude_more_than_entry.grid(row=0, column=1, pady=2, sticky=W)

    Label(exclude_frm, text="Exclude values less than:").grid(row=1, column=0, padx=10, pady=2, sticky=W)
    exclude_less_than_entry = Entry(exclude_frm, width=30)
    exclude_less_than_entry.grid(row=1, column=1, pady=2, sticky=W)

    Label(exclude_frm, text="Exclude TZs:").grid(row=2, column=0, padx=10, pady=2, sticky=W)
    exclude_tz_entry = Entry(exclude_frm, width=30)
    exclude_tz_entry.grid(row=2, column=1, pady=2, sticky=W)
    Label(exclude_frm, text="*").grid(row=2, column=2, pady=2, sticky=W)
    Label(exclude_frm, text="*separate time zones with commas").grid(row=3, column=0, padx=10, pady=2, sticky=W)

    # and a label frame to include specific time zones
    include_frm = Labelframe(top_level, text="Include patterns")
    include_frm.pack(padx=5, pady=10, fill=X)

    Label(include_frm, text="Include specific TZs:").grid(row=0, column=0, padx=10, pady=2, sticky=W)
    include_tz_entry = Entry(include_frm, width=30)
    include_tz_entry.grid(row=0, column=1, pady=2, sticky=W)
    Label(include_frm, text="*").grid(row=0, column=2, pady=2, sticky=W)
    Label(include_frm, text="*separate time zones with commas").grid(row=1, column=0, padx=10, pady=2, sticky=W)

    calculate_btn = Button(top_level, text="Show Graph",
                           command=lambda: calculate_tzs_graph(exclude_more_than_entry.get(),
                                                               exclude_less_than_entry.get(),
                                                               exclude_tz_entry.get(),
                                                               include_tz_entry.get()))
    calculate_btn.pack(ipady=2, pady=20, padx=30, fill=X)

    exit_btn = Button(top_level, text="Exit", command=top_level.destroy)
    exit_btn.pack(side=BOTTOM, ipadx=3, pady=10, ipady=2, after=calculate_btn)

    top_level.mainloop()


# this function checks if user gave correct values into the Entries and if yes,
# we pass the data into graph_utils.show_tz_distribution function to build the bar plot
def calculate_tzs_graph(exclude_more_than_str, exclude_less_than_str, exclude_tzs_str, include_tzs_str):
    # if user left this entry empty, we have the maximum value
    if exclude_more_than_str.strip(" ") is "":
        more_than_value = 1000000000
    else:
        try:
            # else try to convert the value into string
            more_than_value = int(exclude_more_than_str)
        except ValueError as ve:
            message = LOG_NAME + " (TZ Graph) :: ERROR :: " + str(ve)
            # and if not succeed, inform the user
            print(message)  # we log the error
            read_write.log_message(message)
            messagebox.showerror("Error", "'More than' value must be an integer number!")
            return

    # if user left this entry empty, we have the minimum init value
    if exclude_less_than_str.strip(" ") is "":
        less_than_value = 0
    else:
        try:
            # else try to convert the value into string
            less_than_value = int(exclude_less_than_str)
        except ValueError as ve:
            message = LOG_NAME + " (TZ Graph) :: ERROR :: " + str(ve)
            # and if not succeed, inform the user
            print(message)  # we log the error
            read_write.log_message(message)
            messagebox.showerror("Error", "'Less than' value must be an integer number!")
            return

    # if exclude values are set wrong, return the error
    if more_than_value < less_than_value:
        message = LOG_NAME + " (TZ Graph) :: ERROR :: " + "Values are set wrong."
        print(message)
        read_write.log_message(message)
        messagebox.showwarning("Warning", "Can't set 'Less than' value bigger than 'More than' value.")
        return

    # build the list with zones to exclude
    if exclude_tzs_str.strip(" ") is "":
        # if user gave no data, this is an empty list
        exclude_tzs_list = []
    else:
        # else, split these values with commas, as requested
        exclude_tzs_list = exclude_tzs_str.split(",")

    # build the list with the zones to include
    if include_tzs_str.strip(" ") is "":
        # if user gave no data, pass an empty list
        include_tzs_list = []
    else:
        # else split the values with commas
        include_tzs_list = include_tzs_str.split(",")

    exclude_tzs_list_final = []
    # but strip the values, if the have trailing or leading whitespaces that may
    # prevent us from wrong filtering
    for ex_tz in exclude_tzs_list:
        ex_stripped_tz = ex_tz.lstrip()  # strips leading ws
        ex_stripped_tz = ex_stripped_tz.rstrip()  # strips trailing ws
        exclude_tzs_list_final.append(ex_stripped_tz)

    include_tzs_list_final = []
    # but strip the values, if the have trailing or leading whitespaces that may
    # prevent us from wrong filtering
    for in_tz in include_tzs_list:
        in_stripped_tz = in_tz.lstrip()  # strips leading ws
        in_stripped_tz = in_stripped_tz.rstrip()  # strips trailing ws
        include_tzs_list_final.append(in_stripped_tz)

    graph_utils.show_tz_distribution(more_than_value, less_than_value, exclude_tzs_list_final, include_tzs_list_final)


# function that build a TopLevel window to let the user apply some filters before showing word graph
def show_words_graph(root):
    # we start the toplevel
    top_level = Toplevel(root)
    top_level.minsize(400, 200)
    read_write.set_favicon(top_level)
    top_level.title("-- Twitter API --  words graph")

    # in this we will have a labelframe to exclude
    exclude_frm = Labelframe(top_level, text="Exclude patterns")
    exclude_frm.pack(side=TOP, padx=5, pady=10, fill=X)

    Label(exclude_frm, text="Exclude words with occurrences more than:").grid(row=0, column=0, padx=10, pady=2,
                                                                              sticky=W)
    exclude_more_than_entry = Entry(exclude_frm, width=30)
    exclude_more_than_entry.grid(row=0, column=1, pady=2, sticky=W)

    Label(exclude_frm, text="Exclude words with occurrences less than:").grid(row=1, column=0, padx=10, pady=2,
                                                                              sticky=W)
    exclude_less_than_entry = Entry(exclude_frm, width=30)
    exclude_less_than_entry.grid(row=1, column=1, pady=2, sticky=W)

    Label(exclude_frm, text="Exclude words:").grid(row=2, column=0, padx=10, pady=2, sticky=W)
    exclude_words_entry = Entry(exclude_frm, width=30)
    exclude_words_entry.grid(row=2, column=1, pady=2, sticky=W)
    Label(exclude_frm, text="*").grid(row=2, column=2, pady=2, sticky=W)
    Label(exclude_frm, text="*separate words with commas").grid(row=3, column=0, padx=10, pady=2, sticky=W)

    # and a label frame to include specific time zones
    include_frm = Labelframe(top_level, text="Include patterns")
    include_frm.pack(padx=5, pady=10, fill=X)

    Label(include_frm, text="Include specific words:").grid(row=0, column=0, padx=10, pady=2, sticky=W)
    include_words_entry = Entry(include_frm, width=30)
    include_words_entry.grid(row=0, column=1, pady=2, sticky=W)
    Label(include_frm, text="*").grid(row=0, column=2, pady=2, sticky=W)
    Label(include_frm, text="*separate words with commas").grid(row=1, column=0, padx=10, pady=2, sticky=W)

    calculate_btn = Button(top_level, text="Show Graph",
                           command=lambda: calculate_words_graph(exclude_more_than_entry.get(),
                                                                 exclude_less_than_entry.get(),
                                                                 exclude_words_entry.get(),
                                                                 include_words_entry.get()))
    calculate_btn.pack(ipady=2, pady=20, padx=30, fill=X)

    exit_btn = Button(top_level, text="Exit", command=top_level.destroy)
    exit_btn.pack(side=BOTTOM, ipadx=3, pady=10, ipady=2, after=calculate_btn)

    top_level.mainloop()


# this function checks if user gave correct values into the Entries and if yes,
# we pass the data into graph_utils.show_words_distribution function to build the bar plot for the words
def calculate_words_graph(exclude_more_than_str, exclude_less_than_str, exclude_words_list_str, include_words_list_str):
    # if user left this entry empty, we have the maximum value
    if exclude_more_than_str.strip(" ") is "":
        more_than_value = 1000000000
    else:
        try:
            # else try to convert the value into string
            more_than_value = int(exclude_more_than_str)
        except ValueError as ve:
            message = LOG_NAME + " (Words Graph) :: ERROR :: " + str(ve)
            # and if not succeed, inform the user
            print(message)  # we log the error
            read_write.log_message(message)
            messagebox.showerror("Error", "'More than' value must be an integer number!")
            return

    # if user left this entry empty, we have the minimum init value
    if exclude_less_than_str.strip(" ") is "":
        less_than_value = 0
    else:
        try:
            # else try to convert the value into string
            less_than_value = int(exclude_less_than_str)
        except ValueError as ve:
            message = LOG_NAME + " (Words Graph) :: ERROR :: " + str(ve)
            # and if not succeed, inform the user
            print(message)  # we log the error
            read_write.log_message(message)
            messagebox.showerror("Error", "'Less than' value must be an integer number!")
            return

    # if exclude values are set wrong, return the error
    if more_than_value < less_than_value:
        message = LOG_NAME + " (Words Graph) :: ERROR :: " + "Values are set wrong."
        print(message)
        read_write.log_message(message)
        messagebox.showwarning("Warning", "Can't set 'Less than' value bigger than 'More than' value.")
        return

    # build the list with zones to exclude
    exclude_words_list_final = []  # the final exclude list that we will deliver into matplotlib
    if exclude_words_list_str.strip(" ") is "":
        # if user gave no data, this is an empty list
        exclude_words_list = []
    else:
        # else, split these values with commas, as requested
        exclude_words_list = exclude_words_list_str.split(",")

        # but strip the values, if the have trailing or leading whitespaces that may
        # prevent us from correct filtering
        for excluded_word in exclude_words_list:
            excluded_word = excluded_word.lstrip()  # strips leading ws
            excluded_word = excluded_word.rstrip()  # strips trailing ws
            exclude_words_list_final.append(excluded_word)

    # build the list with the zones to include
    include_words_list_final = []  # the final include list that we will deliver into matplotlib
    if include_words_list_str.strip(" ") is "":
        # if user gave no data, pass an empty list
        include_words_list = []
    else:
        # else split the values with commas
        include_words_list = include_words_list_str.split(",")

        # but strip the values, if the have trailing or leading whitespaces that may
        # prevent us from wrong filtering
        for included_word in include_words_list:
            included_word = included_word.lstrip()  # strips leading ws
            included_word = included_word.rstrip()  # strips trailing ws
            include_words_list_final.append(included_word)

    graph_utils.show_word_distribution(more_than_value, less_than_value,
                                       exclude_words_list_final, include_words_list_final)


# show a Toplevel windown, that user can enter a keyword, with which we will search the collection
# and show the tweet's text in a new pane
def keyword_search(root):
    return
