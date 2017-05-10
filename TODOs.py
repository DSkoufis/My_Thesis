# TODO: add a scrollbar on HostFrame on hosts_frm

# TODO: THINK! maybe index "text" field of twitter to be able to query this field and do it faster
# see http://stackoverflow.com/questions/33541290/how-can-i-create-an-index-with-pymongo

# TODO: Format the numbers so they will be something like: 3.456.123,12

# TODO: Make a script to validate and store credentials

# TODO: Make a window, which prints all tweets with the given keyword (user gives it)
# db.ss.find(
#     {"text.words":
#         {"$all":
#              [{"value": "stupid"},
#               {"value": "jack"}
#               ]
#          },
#      "text.stop_words" :
#          {"$all":
#               ["just"]
#           }
#      },
#     {"_id": 0,
#      "whole_text": 1
#      }
# )

# TODO: Make stream and search log messages, printed on a toplevel window

# TODO: Make a 2 axis graph -> x axis: year, y axis: user_count

# TODO: Make a 2 axis graph -> x axis: users, y axis: followers-statuses-friends
