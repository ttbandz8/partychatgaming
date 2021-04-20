import db
import time
import classes as data

now = time.asctime()

u = [
    {'DISNAME': 'johnd123', "IGN": [{'CODM': 'John Doe'}], "GAMES": ["CODM"]},
    {'DISNAME': 'bricks', "IGN": [{'CODM': 'John Doe'}], "GAMES": ["CODM"]}
]

d = {'DISNAME': 'bricks', "IGN": [{'CODM': 'John Doe'}], "GAMES": ["CODM"]}

# db.deleteUser(d)

# db.addUsers(data.newUser(u))

# print()

sessionlist = [
     { "Date": "4/20/21", "Game": "kingofthehill", "timestamp": now},
    { "Date": "4/21/21", "Game": "kingofthehill", "timestampe": now}
]

# insert_sessions = db.sessions_col.insert_many(sessionlist)