from tkinter import *
from tkinter import messagebox
from Utilities import *
from pymongo.errors import ServerSelectionTimeoutError, AutoReconnect

# variable that helps on logging
LOG_NAME = " (main) : "


def goto_host_frame(root, frame):
    frame.destroy()
    host_selection = frames.HostFrame(root)
    # we add functionality to the next button of HostFrame
    host_selection.next_btn.config(command=lambda: goto_db_frame(root=root, frame=host_selection))
    root.title("-- Twitter API --  host selection")
    host_selection.pack()


def goto_db_frame(root, frame):
    # if we come from HostFrame, we need to check some things first!
    if isinstance(frame, frames.HostFrame):
        response = db_utils.can_connect(frame.host_entry.get(), frame.port_entry.get())
        if response["connect"]:  # validate the connection
            host = response["host"]
            port = response["port"]
            # we add the new data into last.json, because a connection happened
            data = read_write.read_last()
            data["host"] = host
            data["port"] = port
            read_write.write_last(data)

            # search if this entry can be found on mongo.json
            found = False
            data = read_write.read_mongo()
            for entry in data:
                if entry["host"] == host:
                    found = True
                    read_write.write_last(entry)  # if found, add previous data, into last.json for later access
            if not found:  # and if not found, append it on the list
                read_write.log_message("[INFO]" + LOG_NAME + "Connection not found on mongo.json, trying to add it.")
                data.append({"host": host, "port": port})
                read_write.write_mongo(data)
        else:
            # if we can't connect, return and do not pack the new DbFrame
            # and show the errors occurred
            messagebox.showerror(title="Error", message=response["errors"], parent=frame.root)
            return

    # show the DbFrame
    frame.destroy()
    db_selection = frames.DbFrame(root)
    # add functionality on next and back buttons
    db_selection.back_btn.config(command=lambda: goto_host_frame(root=root, frame=db_selection))
    db_selection.next_btn.config(command=lambda: goto_main_frame(root=root, frame=db_selection))
    root.title("-- Twitter API --  database selection")
    db_selection.pack()


def goto_stream_frame(root, frame):
    frame.destroy()
    stream_frame = frames.StreamFrame(root)
    stream_frame.back_btn.config(command=lambda: goto_main_frame(root=root, frame=stream_frame))
    stream_frame.mng_stream_btn.config(command=lambda: stream_util.start_stream(frame=stream_frame))
    root.title("-- Twitter API --  Streaming API")
    stream_frame.pack()


def goto_search_frame(root, frame):
    frame.destroy()
    search_frame = frames.SearchFrame(root)
    search_frame.back_btn.config(command=lambda: goto_main_frame(root=root, frame=search_frame))
    search_frame.mng_search_btn.config(command=lambda: search_util.start_search(frame=search_frame))
    root.title("-- Twitter API --  REST Search API")
    search_frame.pack()


def goto_stats_frame(root, frame):
    try:
        stats_frame = frames.StatsFrame(root)
    except ServerSelectionTimeoutError as e:
        read_write.log_message("[ERROR]" + LOG_NAME + "ServerSelectionTimeoutError: " + str(e))
        messagebox.showerror("Error", "Lost Connection to the DB")
        return
    except AutoReconnect as e:
        read_write.log_message("[ERROR]" + LOG_NAME + "AutoReconnect: " + str(e))
        messagebox.showerror("Error", "Lost Connection to the DB")
        return

    frame.destroy()
    stats_frame.back_btn.config(command=lambda: goto_main_frame(root=root, frame=stats_frame))
    root.title("-- Twitter API --  Stats & Quick Facts")
    stats_frame.pack()


def goto_main_frame(root, frame):
    if isinstance(frame, frames.StreamFrame):
        stream_util.stream_controller.stop()  # stop the stream if any

    elif isinstance(frame, frames.SearchFrame):
        search_util.search_controller.stop()  # stop the search api if open

    elif isinstance(frame, frames.DbFrame):
        # if we are on DbFrame, we need to validate if names are OK, to save them on last.json and mongo.json
        database = frame.db_entry.get()
        db_validation = re.match(r"[a-zA-Z0-9]", database)  # regular expression that validates the name of the db

        collection = frame.collection_entry.get()
        # regular expression that validates the name of the collection
        collection_validation = re.match(r"[a-zA-Z]", collection)

        if db_validation is not None:
            if collection_validation is not None:
                read_write.log_message("[INFO]" + LOG_NAME + "Using database: '" +
                                       database + "' - collection: '" + collection + "'")
                client = db_utils.get_client()
                try:
                    temp = client.address
                except ServerSelectionTimeoutError as e:
                    read_write.log_message("[ERROR]" + LOG_NAME + "ServerSelectionTimeoutError: " + str(e))
                    messagebox.showerror("Error", "Lost Connection to the DB")
                    return
                except AutoReconnect as e:
                    read_write.log_message("[ERROR]" + LOG_NAME + "AutoReconnect: " + str(e))
                    messagebox.showerror("Error", "Lost Connection to the DB")
                    return
                host = temp[0]

                # write the selected values into last.json
                data = read_write.read_last()
                data["database"] = database
                data["collection"] = collection
                read_write.write_last(data)

                # add them in mongo.json too
                data = read_write.read_mongo()
                for entry in data:
                    if entry["host"] == host:
                        entry["database"] = database
                        entry["collection"] = collection
                        read_write.write_mongo(data)

                # make instances of the active database and collection
                active_database = client[database]
                active_collection = active_database[collection]
                db_utils.set_database(active_database)
                db_utils.set_collection(active_collection)

            else:  # collection level errors
                # these are all errors, but we try to find what causes the error
                temp_collection = frame.collection_entry.get().strip(" ")
                if temp_collection is "":
                    message = "[ERROR]" + LOG_NAME + "Collection field was blank."
                    print(message)
                    read_write.log_message(message)
                    messagebox.showerror(title="Error", message="Give a collection name to continue", parent=root)
                else:
                    message = "[ERROR]" + LOG_NAME + "Invalid collection name."
                    print(message)
                    read_write.log_message(message)
                    messagebox.showerror(title="Error", parent=root,
                                         message="Collection's name must start with a letter!")
                # if we found an error, we must exit this function
                return

        else:  # database level errors
            # these are all errors, but we try to find what causes the error
            temp_db = frame.db_entry.get().strip(" ")
            if temp_db is "":
                message = "[ERROR]" + LOG_NAME + "Database field was blank."
                print(message)
                read_write.log_message(message)
                messagebox.showerror(title="Error", message="Give a database name to continue", parent=root)
            else:
                message = "[ERROR]" + LOG_NAME + "Invalid database name."
                print(message)
                read_write.log_message(message)
                messagebox.showerror(title="Error", parent=root,
                                     message="Database's name must start with a letter or number!")
            # if we found an error, we must exit this function
            return
    # if no errors, we reach here, so we pack the MainFrame
    frame.destroy()
    main_menu = frames.MainFrame(root)
    # add functionality on back, search, stream and stats buttons from MainFrame
    main_menu.back_btn.config(command=lambda: goto_db_frame(root=root, frame=main_menu))
    main_menu.stream_btn.config(command=lambda: goto_stream_frame(root=root, frame=main_menu))
    main_menu.search_btn.config(command=lambda: goto_search_frame(root=root, frame=main_menu))
    main_menu.stats_btn.config(command=lambda: goto_stats_frame(root=root, frame=main_menu))
    root.title("-- Twitter API --  Main menu")
    main_menu.pack(pady=10)


# this is the first function to be called. It initialize the window with the first Frame
def main():
    root = Tk()
    root.title("-- Twitter API --  host selection")
    root.minsize(400, 200)

    # first frame on the program will be HostFrame. After this, we change frames from different goto functions
    host_selection = frames.HostFrame(root)
    host_selection.next_btn.config(command=lambda: goto_db_frame(root=root, frame=host_selection))
    host_selection.pack()

    # add a favicon
    read_write.set_favicon(root)
    root.mainloop()


'''
Program starts here
'''
if __name__ == '__main__':
    read_write.log_message("[INFO]" + LOG_NAME + "Program starts")
    main()
