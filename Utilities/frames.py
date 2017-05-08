######################################################
# Module that holds all Frame object for the program #
######################################################
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from Utilities import read_write, db_utils, stream_util, search_util, graph_utils, stats_utils
from pymongo import DESCENDING

LOG_NAME = "--> frames.py"


# Frame responsible to show the main menu of the Application. It has 5 buttons. If user press "Stream"
# the StreamFrame will show up. If "Search" is pressed, SearchFrame. With "Show Stats", StatsFrame, with
# "Back", DbFrame will show and with "Exit", Application closes
class MainFrame(Frame):
    def __init__(self, master):
        super(MainFrame, self).__init__(master)
        self.root = master

        # build the widgets
        self.stream_btn = Button(self, text="Start Stream", width=30)
        self.search_btn = Button(self, text="Start Search", width=30)
        self.stats_btn = Button(self, text="Show Stats", width=30)
        self.back_btn = Button(self, text="Back", width=30)
        self.exit_btn = Button(self, text="Exit", width=30, command=self.root.destroy)

        # add the widgets
        self.stream_btn.grid(row=0, column=2, columnspan=2, pady=10, ipady=3)
        self.search_btn.grid(row=1, column=2, columnspan=2, pady=10, ipady=3)
        self.stats_btn.grid(row=2, column=2, columnspan=2, pady=10, ipady=3)
        self.back_btn.grid(row=3, column=2, columnspan=2, pady=10, ipady=3)
        self.exit_btn.grid(row=4, column=2, columnspan=2, pady=10, ipady=3)


# Frame that let the user choose a host and make a successful connection to a database. If succeed
# next Frame will be DbFrame
class HostFrame(Frame):
    def __init__(self, master):
        super(HostFrame, self).__init__(master)
        self.root = master

        # get any previous data on last.json
        previous_data = read_write.read_last()

        # Three frames will hold the widgets
        label_frm = Frame(self)  # this will hold the labels
        label_frm.grid(row=0, pady=10, padx=50)
        button_frm = Frame(self)  # this will hold the buttons
        button_frm.grid(row=1, pady=5, padx=50)
        self.hosts_frm = Frame(self)  # this will hold the previous hosts
        self.hosts_frm.grid(row=2, pady=5, padx=50)
        self.hosts_frm.grid_remove()  # but we need to show it, only if user wants

        # Build the widgets for label_frm
        Label(label_frm, text="Host:").grid(column=2, row=0, pady=10, padx=5)
        Label(label_frm, text="Port:").grid(column=2, row=1, padx=5)
        self.host_entry = Entry(label_frm, width=30)
        self.host_entry.grid(column=3, row=0, pady=10)
        self.port_entry = Entry(label_frm, width=30)
        self.port_entry.grid(column=3, row=1)

        # Add data to entries if any data on last.json
        try:
            if previous_data["host"] is not "":
                self.host_entry.insert(0, previous_data["host"])
                self.port_entry.insert(0, previous_data["port"])
        except KeyError as e:
            print(LOG_NAME + " :: ERROR :: KeyError " + str(e))

        # Build the widgets for button_frm
        self.next_btn = Button(button_frm, text="Next")
        self.next_btn.grid(column=2, row=0, pady=10, padx=4, ipadx=2, ipady=2)
        self.exit_btn = Button(button_frm, text="Exit", command=self.root.destroy)
        self.exit_btn.grid(column=4, row=0, pady=10, padx=4, ipadx=2, ipady=2)
        self.show_previous_btn = Button(button_frm, text="Show previous hosts", command=self.show_hosts)
        self.show_previous_btn.grid(column=2, row=1, columnspan=3, ipadx=2, ipady=2)

        # Build the widgets for hosts_frm
        def select_host():
            selected_data = str(var.get()).split(":")
            self.host_entry.delete(0, "end")
            self.host_entry.insert(0, selected_data[0])
            self.port_entry.delete(0, "end")
            self.port_entry.insert(0, selected_data[1])

        # populate the hosts_frm with Radio-buttons that show previous connections
        data = read_write.read_mongo()

        var = StringVar()
        counter = 0  # this will show in which row each radio-button will be on the frame
        for json_object in data:
            if json_object["host"] is not "":
                option = json_object["host"] + ":" + str(json_object["port"])  # format host:port
                r = Radiobutton(self.hosts_frm, text=option, variable=var, value=option, command=select_host)
                r.grid(row=counter, column=2, pady=2)
                counter += 1

    # these 2 methods, will show or hide the populated hosts on hosts_frm radio-buttons
    def show_hosts(self):
        self.show_previous_btn.config(command=self.hide_hosts, text="Hide previous hosts")
        self.hosts_frm.grid()

    def hide_hosts(self):
        self.show_previous_btn.config(command=self.show_hosts, text="Show previous hosts")
        self.hosts_frm.grid_remove()


# Frame that let the user choose the database and collection names. If validations pass, then next Frame will be
# MainFrame. User can drop databases and collections from here too.
class DbFrame(Frame):
    def __init__(self, master):
        super(DbFrame, self).__init__(master)
        self.root = master
        self.client = db_utils.get_client()

        # get any previous data on last.json
        previous_data = read_write.read_last()

        # Two frames will hold the widgets
        label_frm = Frame(self)  # the labels and entries
        label_frm.grid(row=0, pady=10, padx=50)
        button_frm = Frame(self)  # the buttons
        button_frm.grid(row=1, pady=5, padx=50)

        # Build the widgets for label_frm
        Label(label_frm, text="Database:").grid(column=2, row=0, pady=10, padx=5)
        Label(label_frm, text="Collection:").grid(column=2, row=1, padx=5)
        self.db_entry = Entry(label_frm, width=30)
        self.db_entry.grid(column=3, row=0, pady=10)
        self.collection_entry = Entry(label_frm, width=30)
        self.collection_entry.grid(column=3, row=1)

        # Add data to entries if any data on last.json
        try:
            if previous_data["database"] is not "":
                self.db_entry.insert(0, previous_data["database"])
        except KeyError as e:
            print(LOG_NAME + " :: ERROR :: KeyError " + str(e))
        try:
            if previous_data["collection"] is not "":
                self.collection_entry.insert(0, previous_data["collection"])
        except KeyError as e:
            print(LOG_NAME + " :: ERROR :: KeyError " + str(e))

        # Build the widgets for button_frm
        self.next_btn = Button(button_frm, text="Next")
        self.next_btn.grid(column=2, row=0, pady=10, padx=4, ipadx=2, ipady=2)
        self.back_btn = Button(button_frm, text="Back")
        self.back_btn.grid(column=4, row=0, pady=10, padx=4, ipadx=2, ipady=2)
        self.previous_dbs_btn = Button(button_frm, text="Show databases", command=self.show_dbs)
        self.previous_dbs_btn.grid(column=2, row=1, ipadx=2, ipady=2)
        self.previous_collection_btn = Button(button_frm, text="Show collections", command=self.show_collections)
        self.previous_collection_btn.grid(column=4, row=1, ipadx=2, ipady=2)

        # Build the widgets for dbs_frm
        self.selected_db_var = StringVar()
        self.selected_collection_var = StringVar()

    # this method populates the dbs radio-buttons. This happen every time, show_dbs method runs
    def populate_dbs(self):
        def select_db():
            self.selected_db_var = db_var
            selected_db = str(db_var.get())
            self.db_entry.delete(0, "end")
            self.db_entry.insert(0, selected_db)
            # we add the drop button, only if a radio-button is pressed
            self.drop_db_btn = Button(self.dbs_frm, text="Drop database",
                                      command=self.drop_db)
            self.drop_db_btn.grid(row=db_counter, column=2, pady=10, ipadx=5, ipady=2)

        db_var = StringVar()

        db_list = self.client.database_names()  # we get the available database names of this connection

        db_counter = 0
        for name in db_list:
            r = Radiobutton(self.dbs_frm, text=name, variable=db_var, value=name, command=select_db)
            r.grid(row=db_counter, column=2, pady=2)
            db_counter += 1

    # this method populates the collection radio-buttons. This happen every time, show_collections method runs
    def populate_collections(self):
        def select_collection():
            self.selected_collection_var = collection_var
            selected_collection = str(collection_var.get())
            self.collection_entry.delete(0, "end")
            self.collection_entry.insert(0, selected_collection)
            # we add the drop button, only if a radio-button is pressed
            self.drop_collection_btn = Button(self.collections_frm, text="Drop collection",
                                              command=self.drop_collection)
            self.drop_collection_btn.grid(row=collection_counter, column=2, pady=10, ipadx=5, ipady=2)

        collection_var = StringVar()
        collection_list = []  # we get the available collection names of this connection but
        # only if a database name already exists
        if self.db_entry.get() is not "":
            collection_list = self.client[self.db_entry.get()].collection_names(include_system_collections=False)

        collection_counter = 0  # this counter is responsible to place the radio-buttons into correct row
        for name in collection_list:
            r = Radiobutton(self.collections_frm, text=name, variable=collection_var,
                            value=name, command=select_collection)
            r.grid(row=collection_counter, column=2, pady=2)
            collection_counter += 1

    def show_dbs(self):
        # create the frame
        self.dbs_frm = Frame(self)  # the frame that will show the dbs
        self.dbs_frm.grid(row=2, pady=5, padx=50)
        self.populate_dbs()

        try:  # if collections already shown, we need to hide them, but if not, this will raise an exception
            self.hide_collections()
        except AttributeError:
            pass

        # change the button's text and grid the frame
        self.previous_dbs_btn.config(command=self.hide_dbs, text="Hide databases")
        self.dbs_frm.grid()

    def hide_dbs(self):
        self.previous_dbs_btn.config(command=self.show_dbs, text="Show databases")
        self.dbs_frm.grid_remove()

    def show_collections(self):
        # create the frame
        self.collections_frm = Frame(self)  # the frame that will show the collections
        self.collections_frm.grid(row=2, pady=5, padx=50)
        self.populate_collections()

        try:  # if dbs already shown, we need to hide them, but if not, this will raise an exception
            self.hide_dbs()
        except AttributeError:
            pass

        # change the button's text and grid the frame
        self.previous_collection_btn.config(command=self.hide_collections, text="Hide collections")
        self.collections_frm.grid()

    def hide_collections(self):
        self.previous_collection_btn.config(command=self.show_collections, text="Show collections")
        self.collections_frm.grid_remove()

    def drop_db(self):
        name = self.selected_db_var.get()
        answer = messagebox.askokcancel(title="Are you sure?", message="Are you sure you want to delete " + name,
                               default="cancel", parent=self.root)
        if answer:
            self.client.drop_database(name)
            self.hide_dbs()
            self.show_dbs()

    def drop_collection(self):
        name = self.selected_collection_var.get()
        answer = messagebox.askokcancel(title="Are you sure?", message="Are you sure you want to delete " + name,
                               default="cancel", parent=self.root)
        if answer:
            db_name = self.db_entry.get()
            self.client[db_name].drop_collection(name)
            self.hide_collections()
            self.show_collections()


class StreamFrame(Frame):
    def __init__(self, master):
        super(StreamFrame, self).__init__(master)
        self.root = master

        # These frames will hold the widgets
        label_frm = Frame(self)  # this for the label and entry
        label_frm.grid(row=0, column=2, padx=10, pady=10, ipady=20, ipadx=20)
        self.keywords_frm = Frame(self)  # this will be hidden until user wants to see previous keywords
        self.keywords_frm.grid(row=0, column=3, rowspan=3, pady=15)

        # Build the widgets for label_frm
        Label(label_frm, text="Keyword:").grid(row=0, column=0, padx=20)
        self.keyword_entry = Entry(label_frm, width=30)
        self.keyword_entry.grid(row=0, column=1, columnspan=3)

        # Build the widgets for button_frm
        self.mng_stream_btn = Button(label_frm, text="Start Stream")  # this will change from start to stop
        self.mng_stream_btn.grid(row=1, column=1, ipadx=5, ipady=3, pady=20)
        self.pause_stream_btn = Button(label_frm, text="Pause Stream")  # this will show up, only if user start stream
        self.pause_stream_btn.grid(row=1, column=3, ipadx=5, ipady=3, padx=10, pady=20)
        self.pause_stream_btn.grid_remove()

        # Build the widgets for exit_frm
        self.back_btn = Button(label_frm, text="Back")
        self.back_btn.grid(row=2, column=1, ipadx=5, ipady=3, pady=15)
        self.exit_btn = Button(label_frm, text="Exit", command=self.safe_exit)
        self.exit_btn.grid(row=2, column=3, ipadx=5, ipady=3, padx=15, pady=10)

        # Build the widgets for keywords_frm
        self.manage_keywords_btn = Button(self.keywords_frm, command=self.show_keywords,
                                          text=">>>")  # this will change into "<<<" when user clicks it
        self.manage_keywords_btn.grid(row=0, column=0, ipadx=5, ipady=3, padx=10)

    # this method creates a new list box and populates it with the data from keywords.json
    def show_keywords(self):
        # first re-configure the button to show the desired text and change the command into hiding method
        self.manage_keywords_btn.config(text="<<<", command=self.hide_keywords)

        self.previous_keywords = read_write.read_keywords()  # get any previous keywords

        # if there are keywords and the list is not empty
        if len(self.previous_keywords) > 0:
            # build the list box
            self.keyword_lb = Listbox(self.keywords_frm, height=10)
            self.keyword_lb.grid(column=1, row=0, pady=10, padx=5, sticky=(N, S, E, W))
            # add a binding method
            self.keyword_lb.bind('<Double-1>', self.select_keyword)
            # and add the OK button. This happens here, because we don'w want a button without a list box
            self.select_keyword_btn = Button(self.keywords_frm, text="OK", command=self.select_keyword)
            self.select_keyword_btn.grid(row=3, column=1, ipady=3, ipadx=5, pady=10)

            # adding the keywords to the list box
            counter = 0
            for keyword in self.previous_keywords:
                self.keyword_lb.insert(counter, keyword)
                counter += 1

            # Colorize alternating lines of the listbox
            for i in range(0, len(self.previous_keywords), 2):
                self.keyword_lb.itemconfigure(i, background='#f0f0ff')

    # this method changes the button again and it is called to hide the list box
    def hide_keywords(self):
        self.manage_keywords_btn.config(text=">>>", command=self.show_keywords)
        try:
            # this may result to an error, because we can call hide_keywords before we initialize
            # the list box. This happening if no keywords are present in keywords.json
            self.keyword_lb.destroy()
            self.select_keyword_btn.destroy()
        except AttributeError:
            pass

    def select_keyword(self, *args):
        idxs = self.keyword_lb.curselection()
        if len(idxs) == 1:
            idx = int(idxs[0])
            name = self.previous_keywords[idx]
            self.keyword_entry.delete(0, "end")
            self.keyword_entry.insert(0, name)

    def safe_exit(self):
        x = messagebox.askyesno(title="Exit", message="Are you sure you want to exit?",
                                icon="question")
        if x:
            stream_util.stream_controller.stop()
            read_write.log_message(stream_util.LOG_NAME + " :: INFO :: Exiting...")
            self.root.destroy()


class SearchFrame(Frame):
    def __init__(self, master):
        super(SearchFrame, self).__init__(master)
        self.root = master

        # These frames will hold the widgets
        label_frm = Frame(self)  # this for the label and entry
        label_frm.grid(row=0, column=2, padx=10, pady=10, ipady=20, ipadx=20)
        self.keywords_frm = Frame(self)  # this will be hidden until user wants to see previous keywords
        self.keywords_frm.grid(row=0, column=3, rowspan=3, pady=15)

        # Build the widgets for label_frm
        Label(label_frm, text="Keyword:").grid(row=0, column=0, padx=20)
        self.keyword_entry = Entry(label_frm, width=30)
        self.keyword_entry.grid(row=0, column=1, columnspan=3)

        # Build the widgets for button_frm
        # this will change from start to stop when user press it
        self.mng_search_btn = Button(label_frm, text="Start Search")
        self.mng_search_btn.grid(row=1, column=1, ipadx=5, ipady=3, pady=20)
        self.pause_search_btn = Button(label_frm, text="Pause Search")  # this will show up only if user starts a search
        self.pause_search_btn.grid(row=1, column=3, ipadx=5, ipady=3, padx=10, pady=20)
        self.pause_search_btn.grid_remove()

        # Build the widgets for exit_frm
        self.back_btn = Button(label_frm, text="Back")
        self.back_btn.grid(row=2, column=1, ipadx=5, ipady=3, pady=15)
        self.exit_btn = Button(label_frm, text="Exit", command=self.safe_exit)
        self.exit_btn.grid(row=2, column=3, ipadx=5, ipady=3, padx=15, pady=10)

        # Build the widgets for keywords_frm
        self.manage_keywords_btn = Button(self.keywords_frm, command=self.show_keywords,
                                          text=">>>")  # this will change into "<<<" when user clicks it
        self.manage_keywords_btn.grid(row=0, column=0, ipadx=5, ipady=3, padx=10)

    # this method creates a new list box and populates it with the data from keywords.json
    def show_keywords(self):
        self.manage_keywords_btn.config(text="<<<", command=self.hide_keywords)

        self.previous_keywords = read_write.read_keywords()

        if len(self.previous_keywords) > 0:
            self.keyword_lb = Listbox(self.keywords_frm, height=10)
            self.keyword_lb.grid(column=1, row=0, pady=10, padx=5, sticky=(N, S, E, W))

            self.keyword_lb.bind('<Double-1>', self.select_keyword)

            self.select_keyword_btn = Button(self.keywords_frm, text="OK", command=self.select_keyword)
            self.select_keyword_btn.grid(row=3, column=1, ipady=3, ipadx=5, pady=10)

        counter = 0
        for keyword in self.previous_keywords:
            self.keyword_lb.insert(counter, keyword)
            counter += 1

        # Colorize alternating lines of the listbox
        for i in range(0, len(self.previous_keywords), 2):
            self.keyword_lb.itemconfigure(i, background='#f0f0ff')

    def hide_keywords(self):
        self.manage_keywords_btn.config(text=">>>", command=self.show_keywords)
        try:
            self.keyword_lb.destroy()
            self.select_keyword_btn.destroy()
        except AttributeError:
            pass

    def select_keyword(self, *args):
        idxs = self.keyword_lb.curselection()
        if len(idxs) == 1:
            idx = int(idxs[0])
            name = self.previous_keywords[idx]
            self.keyword_entry.delete(0, "end")
            self.keyword_entry.insert(0, name)

    def safe_exit(self):
        x = messagebox.askyesno(title="Exit", message="Are you sure you want to exit?",
                                icon="question")
        if x:
            search_util.search_controller.stop()
            read_write.log_message(search_util.LOG_NAME + " :: INFO :: Exiting...")
            self.root.destroy()


class StatsFrame(Frame):
    def __init__(self, master):
        super(StatsFrame, self).__init__(master)
        self.root = master
        self.collection = db_utils.get_collection()

        all_documents = self.collection.find()  # this is a Cursor object

        quick_facts_frm = Frame(self)
        quick_facts_frm.grid(row=0, column=0, pady=10)
        show_graphs_frm = Frame(self)
        show_graphs_frm.grid(row=1, column=0, pady=10)
        exit_frm = Frame(self)
        exit_frm.grid(row=2, column=0, pady=10)

        Label(quick_facts_frm, text="Total unique tweets stored:").grid(row=0, column=0, padx=10, pady=2, sticky=W)
        tweets_sum = all_documents.count()
        read_write.log_message(LOG_NAME + " (StatsFrame) :: INFO :: Found " + str(tweets_sum) + " tweets in the DB")
        Label(quick_facts_frm, text=str(tweets_sum)).grid(row=0, column=2, pady=2, sticky=W)

        # if we use a collection with no stored tweets, we do not show any data or metric
        if tweets_sum > 0:

            Label(quick_facts_frm, text="Number of entries that\nare retweets:").grid(row=1, column=0, padx=10, pady=2,
                                                                                      sticky=W)
            number_of_retweets = self.collection.find({"is_retweet": True}).count()
            Label(quick_facts_frm, text=str(number_of_retweets)).grid(row=1, column=2, pady=2, sticky=W)

            # the rest of the "quick facts" will only be shown, only if db's size is smaller than 100.000 documents
            # otherwise, they will not be so "quick"!!
            if tweets_sum <= 100000:
                # iterate the cursor once here and find all values you want
                unique_users = []  # how many unique users we have
                max_counter = 0  # the most statuses count from a user

                for item in all_documents:  # for all items in the db
                    if item["user"]["id_str"] not in unique_users:  # check the user.id_str
                        unique_users.append(item["user"]["id_str"])
                    if item["user"]["statuses_count"] > max_counter:  # check the user.statuses_count
                        max_counter = item["user"]["statuses_count"]
                users_sum = len(unique_users)

                # showing the number of unique users
                Label(quick_facts_frm, text="Number of unique users:").grid(row=2, column=0, padx=10, pady=2, sticky=W)
                Label(quick_facts_frm, text=str(users_sum)).grid(row=2, column=2, pady=2, sticky=W)

                # showing the number of verified users
                Label(quick_facts_frm, text="Verified users:").grid(row=3, column=0, padx=10, pady=2, sticky=W)
                verified_users_sum = self.collection.find(filter={"user.verified": True}).count()
                Label(quick_facts_frm, text=str(verified_users_sum)).grid(row=3, column=2, pady=2, sticky=W)

                # showing the oldest tweet
                Label(quick_facts_frm, text="Oldest created tweet\nstored in the database:").grid(row=4, column=0,
                                                                                                  padx=10, pady=2,
                                                                                                  sticky=W)
                oldest_tweet_cursor = self.collection.find().sort("created_at", DESCENDING).limit(1)
                oldest_tweet = [item["created_at"] for item in oldest_tweet_cursor]
                Label(quick_facts_frm, text=oldest_tweet).grid(row=4, column=2, pady=2, sticky=W)

                # showing the most statuses by a user
                Label(quick_facts_frm, text="Most statuses by a user:").grid(row=5, column=0, padx=10, pady=2, sticky=W)
                Label(quick_facts_frm, text=str(max_counter)).grid(row=5, column=2, pady=2, sticky=W)
            else:
                read_write.log_message(LOG_NAME + " (StatsFrame) :: WARNING :: Found more than " +
                                       "100000 tweets in the DB. No 'Quick Facts' are shown")

            # build the widgets for show_graphs_frm
            # letters distribution graph
            self.letters_distro_btn = Button(show_graphs_frm, text="Letters Distribution Graph",
                                             command=graph_utils.show_letter_distribution)
            self.letters_distro_btn.grid(row=0, column=1, pady=10, ipadx=5)

            # tweets per time zone graph (we open a new Toplevel window, to apply some filters
            self.tweets_per_tz_btn = Button(show_graphs_frm, text="Tweets per Time Zone Graph",
                                            command=lambda: stats_utils.show_tweets_per_tz_graph(self.root))
            self.tweets_per_tz_btn.grid(row=1, column=1, pady=10, ipadx=5)

            # a map with points on coordinates
            self.coordinates_map_btn = Button(show_graphs_frm, text="Show map with coordinates",
                                              command=graph_utils.show_coordinates_map)
            self.coordinates_map_btn.grid(row=2, column=1, pady=10, ipadx=5)

            # words distribution graph
            self.words_graph_btn = Button(show_graphs_frm, text="Words Distribution Graph",
                                          command=lambda: stats_utils.show_words_graph(self.root))
            self.words_graph_btn.grid(row=3, column=1, pady=10, ipadx=5)
        else:  # if we have an empty collection
            message = "No documents found in this collection."
            read_write.log_message(LOG_NAME + " (StatsFrame) :: WARNING :: " + message)
            message += "\nPlease enter some data first."
            Label(quick_facts_frm, text=message).grid(row=1, column=0, padx=10, pady=5)

        # Build the widgets for exit_frm
        self.back_btn = Button(exit_frm, text="Back")
        self.back_btn.grid(row=0, column=1, ipadx=5, ipady=3, pady=15)
        self.exit_btn = Button(exit_frm, text="Exit", command=self.safe_exit)
        self.exit_btn.grid(row=0, column=3, ipadx=5, ipady=3, padx=15, pady=10)

    def safe_exit(self):
        x = messagebox.askyesno(title="Exit", message="Are you sure you want to exit?",
                                icon="question")
        if x:
            read_write.log_message(LOG_NAME + " (StatsFrame) :: INFO :: Exiting...")
            self.root.destroy()
