import pymongo 
from decouple import config


TOKEN = config('MONGOTOKEN')
myclient = pymongo.MongoClient(TOKEN)

kohdb = myclient["kingofthehilldb"]

usercol = kohdb["users"]

userlist = [
    { "IGN": "ttbandz", "Discord Name": "lowkey lowkey", "Score": "1"},
    { "IGN:": "johndoe", "Discord Name:": "johnd123", "Score": "2"}
]

user = usercol.insert_many(userlist)

#print(user.inserted_ids)

sessioncol = kohdb["sessions"]

sessionlist = [
     { "Date": "4/20/21", "Game": "kingofthehill"},
    { "Date": "4/21/21", "Game": "kingofthehill"}
]   

session = sessioncol.insert_many(sessionlist)

#print(session.inserted_ids)