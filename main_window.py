from tkinter import *
from tkinter import messagebox as mb
from UI import streaming_window as stream
from UI import searching_window as search
from UI import filters_window as fw
from Utilities import window_utils as wu
import json


# this is the main frame of the Application (menu)
class MainFrame(Frame):
    def __init__(self, master):
        super(MainFrame, self).__init__(master)
        self.root = master
        self.init_widgets()

    def init_widgets(self):
        # adding the buttons into Application frame
        stream_btn = Button(self, text="Start Streaming", command=stream.stream_window, pady=3)
        stream_btn.pack(pady=3)

        search_btn = Button(self, text="Start Search API", command=search.search_window, pady=3)
        search_btn.pack(pady=3)

        filters_btn = Button(self, text="Show Stats", command=fw.filters_window, pady=3)
        filters_btn.pack(pady=3)

        back_btn = Button(self, text="Back", command=lambda: pack_init_frame(self.root, self))
        back_btn.pack(pady=3)

        exit_btn = Button(self, text="Exit", command=lambda: wu.close_window(self.root), pady=3)
        exit_btn.pack(pady=3)


# with this frame we initialize the data for the connection with MongoDB
class DbFrame(Frame):
    def __init__(self, master):
        super(DbFrame, self).__init__(master)
        self.root = master

        # labels first
        host_lbl = Label(self, text="host:")
        host_lbl.grid(column=2, row=0, pady=2, padx=10)
        port_lbl = Label(self, text="port:")
        port_lbl.grid(column=2, row=1, pady=2, padx=10)
        db_lbl = Label(self, text="database:")
        db_lbl.grid(column=2, row=2, pady=2, padx=10)
        collection_lbl = Label(self, text="collection:")
        collection_lbl.grid(column=2, row=3, pady=2, padx=10)

        # then entries
        self.host_entry = Entry(self, width=30)  # entry for host selection
        self.host_entry.insert(0, "e.g localhost")  # adding a place holder
        self.host_entry.bind('<FocusIn>', wu.on_host_click)
        self.host_entry.bind('<FocusOut>', wu.on_host_out)
        self.host_entry.config(fg='grey')
        self.host_entry.grid(column=3, row=0)

        self.port_entry = Entry(self, width=30)  # entry for port selection
        self.port_entry.insert(0, "e.g 27017")  # adding a place holder
        self.port_entry.bind('<FocusIn>', wu.on_port_click)
        self.port_entry.bind('<FocusOut>', wu.on_port_out)
        self.port_entry.config(fg='grey')
        self.port_entry.grid(column=3, row=1)

        self.database_entry = Entry(self, width=30)  # entry for database selection
        self.database_entry.insert(0, "name of the database")  # adding a place holder
        self.database_entry.bind('<FocusIn>', wu.on_database_click)
        self.database_entry.bind('<FocusOut>', wu.on_database_out)
        self.database_entry.config(fg='grey')
        self.database_entry.grid(column=3, row=2)

        self.collection_entry = Entry(self, width=30)  # entry for collection selection
        self.collection_entry.insert(0, "collection's name")  # adding a place holder
        self.collection_entry.bind('<FocusIn>', wu.on_collection_click)
        self.collection_entry.bind('<FocusOut>', wu.on_collection_out)
        self.collection_entry.config(fg='grey')
        self.collection_entry.grid(column=3, row=3)

        # apply button widgets for next and exit
        next_btn = Button(self, text="Next", width=20, command=lambda: pack_main_frame(self.root, self))
        next_btn.grid(column=2, row=5, columnspan=2, pady=10, ipady=2)

        exit_btn = Button(self, text="Exit", width=20, command=lambda: wu.close_window(self.root))
        exit_btn.grid(column=2, row=6, columnspan=2, ipady=2)

    # this method to get the values of the frame's entries
    def get_entries(self):
        temp_dict = {}
        host = self.host_entry.get()
        port = self.port_entry.get()
        database = self.database_entry.get()
        collection = self.collection_entry.get()

        # add the data into dictionary
        temp_dict["host"] = host
        temp_dict["port"] = port
        temp_dict["database"] = database
        temp_dict["collection"] = collection

        return temp_dict

    # these methods are setting each entry individually. They are used from check_if_data function
    # to set each entry, with data from mongo.json file
    def set_host(self, data):
        self.host_entry.delete(0, "end")  # delete all the text in the entry
        self.host_entry.insert(0, data)  # Insert host name from mongo.json
        self.host_entry.config(fg='black')

    def set_port(self, data):
        self.port_entry.delete(0, "end")
        self.port_entry.insert(0, data)
        self.port_entry.config(fg='black')

    def set_database(self, data):
        self.database_entry.delete(0, "end")
        self.database_entry.insert(0, data)
        self.database_entry.config(fg='black')

    def set_collection(self, data):
        self.collection_entry.delete(0, "end")
        self.collection_entry.insert(0, data)
        self.collection_entry.config(fg='black')


# this function is called when db frame is shown, to fill with previous data the cells
def check_if_data(db_frm):
    with open("mongo.json") as data_file:
        data = json.load(data_file)

    # if mongo.json have previous data, show them
    if data["host"] != "":
        db_frm.set_host(data["host"])
    if data["port"] != 0:
        db_frm.set_port(data["port"])
    if data["database"] != "":
        db_frm.set_database(data["database"])
    if data["collection"] != "":
        db_frm.set_collection(data["collection"])


# this method hides the current window and shows Mongo initialization
def pack_main_frame(root, hide_frm):
    data = hide_frm.get_entries()
    # check if user gave values
    if (data["host"] != "e.g localhost") and (data["port"] != "e.g 27017") \
            and (data["database"] != "name of the database") and (data["collection"] != "collection's name"):
        # if user gave values, check if port is integer
        try:
            data["port"] = int(data["port"])
        except ValueError:
            mb.showerror("Error", "Wrong port number!")
            return
    else:
        mb.showerror("Error", "Wrong values!")
        return
    # if all are OK, continue
    write_json(data)  # write the dictionary into mongo.json file
    # and show the other window
    hide_frm.pack_forget()
    main_frm = MainFrame(root)
    main_frm.pack()


# this method hides the Application window and shows main window
def pack_init_frame(root, hide_frm):
    hide_frm.pack_forget()
    db_frm = DbFrame(root)
    check_if_data(db_frm)
    db_frm.pack()


# this function is responsible to write back to mongo.json file the values of the entries' fields
def write_json(data):
    with open("mongo.json", "w") as outfile:
        json.dump(data, outfile, sort_keys=True, indent=2)


""" starting the main window  -- Program starts -- """
root = Tk()
root.minsize(400, 200)
root.title("--Twitter API--")

# build the starting frame
db_frm = DbFrame(root)  # this frame holds the starting screen in which user selects database and collection
check_if_data(db_frm)
db_frm.pack()


root.protocol("WM_DELETE_WINDOW", lambda: wu.close_window(root))

root.mainloop()
