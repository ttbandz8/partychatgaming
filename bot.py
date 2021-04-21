import db
import time
import classes as data

now = time.asctime()

u = [
    {"DISNAME": "johnd123", "IGN": [{'CODM': 'John Doe'}], "GAMES": ["CODM"], "TEAMS": [{"NAME": "TESTTEAM"}]},
    {"DISNAME": "bricks", "IGN": [{'CODM': 'John Doe'}], "GAMES": ["CODM"]}
]

d = {"DISNAME": "johnd123", "IGN": [{'CODM': 'John Doe'}], "GAMES": ["CODM"], "TEAMS": [{"NAME": "TESTTEAM"}]}

# db.deleteUser(d)

db.addUsers(data.newUser(u))

# list = []
# for key in d.keys():
#     list.append(key)
# print(list)

sessionlist = [
     { "Date": "4/20/21", "Game": "kingofthehill", "timestamp": now},
    { "Date": "4/21/21", "Game": "kingofthehill", "timestampe": now}
]

# insert_sessions = db.sessions_col.insert_many(sessionlist)