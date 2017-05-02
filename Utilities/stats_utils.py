########################################################################
# Module that is responsible to show windows to let user apply filters #
# before show the graphs and calculate the data for these graphs       #
########################################################################
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from Utilities import graph_utils

LOG_NAME = "--> stats_util.py"


# function that builds a TopLevel Window to let user exclude some values from tweets/time_zone graph
def show_tweets_per_tz_graph(root):
    # we start the toplevel
    top_level = Toplevel(root)
    top_level.minsize(400, 200)
    top_level.title("-- Twitter API --  time zones graph")

    # in this we will have a labelframe
    exclude_frm = Labelframe(top_level, text="Exclude patterns")
    exclude_frm.pack(side=TOP, padx=5, pady=10, fill=X)

    Label(exclude_frm, text="Values more than:").grid(row=0, column=0, padx=10, pady=2, sticky=W)
    more_than_entry = Entry(exclude_frm, width=30)
    more_than_entry.grid(row=0, column=1, pady=2, sticky=W)

    Label(exclude_frm, text="Values less than:").grid(row=1, column=0, padx=10, pady=2, sticky=W)
    less_than_entry = Entry(exclude_frm, width=30)
    less_than_entry.grid(row=1, column=1, pady=2, sticky=W)

    Label(exclude_frm, text="Exclude TZs:").grid(row=2, column=0, padx=10, pady=2, sticky=W)
    exclude_tz_entry = Entry(exclude_frm, width=30)
    exclude_tz_entry.grid(row=2, column=1, pady=2, sticky=W)
    Label(exclude_frm, text="*").grid(row=2, column=2, pady=2, sticky=W)
    Label(exclude_frm, text="*separate time zones with commas").grid(row=3, column=0, padx=10, pady=2, sticky=W)

    calculate_btn = Button(top_level, text="Show Graph", command=lambda: calculate_graph(more_than_entry.get(),
                                                                                         less_than_entry.get(),
                                                                                         exclude_tz_entry.get()))
    calculate_btn.pack(ipady=2, pady=20, padx=30, fill=X)

    exit_btn = Button(top_level, text="Exit", command=top_level.destroy)
    exit_btn.pack(side=BOTTOM, ipadx=3, pady=10, ipady=2, after=calculate_btn)

    top_level.mainloop()


# this function checks if user gave correct values into the Entries and if yes,
# we pass the data into graph_utils.show_tz_distribution function to build the bar plot
def calculate_graph(more_than_str, less_than_str, exclude_tzs_str):
    # if user left this entry empty, we have the minimum value
    if more_than_str.strip(" ") is "":
        more_than_value = 0
    else:
        try:
            # else try to convert the value into string
            more_than_value = int(more_than_str)
        except ValueError as ve:
            # and if not succeed, inform the user
            print(LOG_NAME + " :: ERROR :: " + str(ve))  # we log the error
            messagebox.showerror("Error", "'More than' value must be an integer number!")
            return

    # if user left this entry empty, we have the maximum init value
    if less_than_str.strip(" ") is "":
        less_than_value = 1000000
    else:
        try:
            # else try to convert the value into string
            less_than_value = int(less_than_str)
        except ValueError as ve:
            # and if not succeed, inform the user
            print(LOG_NAME + " :: ERROR :: " + str(ve))  # we log the error
            messagebox.showerror("Error", "'Less than' value must be an integer number!")
            return

    # build the list with zones to exclude
    if exclude_tzs_str.strip(" ") is "":
        # if user gave no data, this is an empty list
        exclude_tzs_list = []
    else:
        # else, split these values with commas, as requested
        exclude_tzs_list = exclude_tzs_str.split(",")

    exclude_tzs_list_final = []
    # but strip the values, if the have trailing or leading whitespaces that may
    # prevent us from correct filtering
    for tz in exclude_tzs_list:
        stripped_tz = tz.lstrip()  # strips leading ws
        stripped_tz = stripped_tz.rstrip()  # strips trailing ws
        exclude_tzs_list_final.append(stripped_tz)

    graph_utils.show_tz_distribution(more_than_value, less_than_value, exclude_tzs_list_final)
