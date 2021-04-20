import pymongo 
from decouple import config


TOKEN = config('MONGOTOKEN_TEST')
mongo = pymongo.MongoClient(TOKEN)
db = mongo["PCGTEST"]
users_col = db["USERS"]
sessions_col = db["SESSIONS"]
games_col = db["GAMES"]
matches_col = db["MATCHES"]
tournaments_col = db["TOURNAMENTS"]

# Check if Collection exists
def col_exists(col):
    collections = db.list_collection_names()
    if col in collections:
        return True

# Check if User exists
def user_exists(data):
    collection_exists = col_exists("USERS")
    if collection_exists:
        exists = users_col.find_one(data)
        if exists:
            return True
        else:
            return False
    else:
        return False


# Adds Multiple Users
def addUsers(users):
    try:
        for user in users:
            exists = user_exists({"IGN": user["IGN"]})
            if exists:
                print("User already exists.")
            else:
                print("Inserting new user.")
                users_col.insert_one(user)
    except:
        print("Add Users failed.")

# Deletes Users
def deleteUser(users):
    try:
        for user in users:
            exists = user_exists(user)
            if exists:
                users_col.delete_one(user)
            else:
                print("User does not exist.")
    except:
        print("Delete User failed.")

# Updates User data
def updateUser(query, newvalues):
    exists = user_exists(query)
    if exists:
        users_col.update_one(query, newvalues)
    else:
        print("Cannot update.")


