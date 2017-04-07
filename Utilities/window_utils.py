

# this method closes the window (master) that passed as argument
def close_window(master):
    master.destroy()


# function that gets called whenever an entry is clicked in main_window
def on_host_click(event):
    entry = event.widget
    if entry.get() == "e.g localhost" :
        entry.delete(0, "end")  # delete all the text in the entry
        entry.insert(0, '')  # Insert blank for user input
        entry.config(fg='black')


def on_host_out(event):
    entry = event.widget
    if entry.get() == '':
        entry.insert(0, "e.g localhost")
        entry.config(fg='grey')


# function that gets called whenever port entry is clicked in main_window
def on_port_click(event):
    entry = event.widget
    if entry.get() == "e.g 27017":
        entry.delete(0, "end")  # delete all the text in the entry
        entry.insert(0, '')  # Insert blank for user input
        entry.config(fg='black')


def on_port_out(event):
    entry = event.widget
    if entry.get() == '':
        entry.insert(0, "e.g 27017")
        entry.config(fg='grey')


# function that gets called whenever database entry is clicked in main_window
def on_database_click(event):
    entry = event.widget
    if entry.get() == "name of the database":
        entry.delete(0, "end")  # delete all the text in the entry
        entry.insert(0, '')  # Insert blank for user input
        entry.config(fg='black')


def on_database_out(event):
    entry = event.widget
    if entry.get() == '':
        entry.insert(0, "name of the database")
        entry.config(fg='grey')


# function that gets called whenever collection entry is clicked in main_window
def on_collection_click(event):
    entry = event.widget
    if entry.get() == "collection's name":
        entry.delete(0, "end")  # delete all the text in the entry
        entry.insert(0, '')  # Insert blank for user input
        entry.config(fg='black')


def on_collection_out(event):
    entry = event.widget
    if entry.get() == '':
        entry.insert(0, "collection's name")
        entry.config(fg='grey')


# this method hides a frame and shows the other
def change_frames(hide_frm, show_frm):
    hide_frm.pack_forget()
    show_frm.pack()
