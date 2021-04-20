import db
import time

now = time.asctime()

users = [
    { "IGN": "ttbandz", "Discord Name": "lowkey lowkey", "timestamp": now},
    { "IGN": "johndoe", "Discord Name:": "johnd123", "timestamp": now}
]

db.addUsers(users)

sessionlist = [
     { "Date": "4/20/21", "Game": "kingofthehill", "timestamp": now},
    { "Date": "4/21/21", "Game": "kingofthehill", "timestampe": now}
]

insert_sessions = db.sessions_col.insert_many(sessionlist)