# TODO: add a scrollbar on HostFrame on hosts_frm

# TODO: THINK! maybe index "text" field of twitter to be able to query this field and do it faster
# see http://stackoverflow.com/questions/33541290/how-can-i-create-an-index-with-pymongo

# TODO: Format the numbers so they will be something like: 3.456.123,12

# TODO: Make a script to validate and store credentials

# TODO: Make a word graph
"""
pipeline = db.ss.aggregate([{$unwind : "$text.words"}, 
                            { $group : 
                                { "_id" : "$text.words.value", 
                                        "counter" : { $sum : 1 } 
                                }
                            }
                           ])
                           
results : { "_id" : "appreciate", "counter" : 1 }
"""

# TODO: Make a window, which prints all tweets with the given keyword (user gives it)
