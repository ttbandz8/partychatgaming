import pymongo 
from decouple import config


TOKEN = config('MONGOTOKEN_TEST')
mongo = pymongo.MongoClient(TOKEN)

db = mongo["PCGTEST"]
users_col = db["USERS"]
teams_col = db["TEAMS"]
sessions_col = db["SESSIONS"]
games_col = db["GAMES"]
matches_col = db["MATCHES"]
tournaments_col = db["TOURNAMENTS"]

'''Check if Collection Exists'''
def col_exists(col):
    collections = db.list_collection_names()
    if col in collections:
        return True
    else:
        return False

'''Check If User Exists'''
def user_exists(data):
    collection_exists = col_exists("USERS")
    if collection_exists:
        userexists = users_col.find_one(data)
        if userexists:
            return True
        else:
            return False
    else:
        return False


'''Add new User'''
def addUsers(users):
    try:
        if isinstance(users, list):
            for user in users:
                exists = user_exists({'DISNAME': user['DISNAME']})
                if exists:
                    print("User already exists.")
                else:
                    print("Inserting new user.")
                    users_col.insert_one(user)
        else:
            exists = user_exists({'DISNAME': users['DISNAME']})
            if exists:
                print("User already exists.")
            else:
                print("Inserting new user.")
                users_col.insert_one(users)
    except:
        print("Add Users failed.")

'''Delete User'''
def deleteUser(users):
    try:
        if isinstance(users, list):
            for user in users:
                exists = user_exists(user)
                if exists:
                    users_col.delete_one({'DISNAME': user['DISNAME']})
                    print("User deleted.")
                else:
                    print("User does not exist.")
        else:
            exists = user_exists({'DISNAME': users['DISNAME']})
            if exists:
                users_col.delete_one({'DISNAME': users['DISNAME']})
                print("User deleted.")
            else:
                print("User does not exist.")

    except:
        print("Delete User failed.")

'''Updates User data'''
def updateUser(query, new_value):
    exists = user_exists({'DISNAME': query['DISNAME']})
    if exists:
        update = users_col.update_one(query, new_value, upsert=True)
        print(update)
    else:
        print("Cannot update.")

'''Check If Teams Exists'''
def team_exists(data):
    collection_exists = col_exists("TEAMS")
    if collection_exists:
        teamexists = teams_col.find_one(data)
        if teamexists:
            return True
        else:
            return False
    else:
        return False

'''Add new Team'''
def addTeam(team):
    try:
        exists = team_exists({'TNAME': team['TNAME']})
        if exists:
            print("Team already exists.")
        else:
            print("Inserting new Team.")
            teams_col.insert_one(team)
    except:
        print("Cannot add team failed.")



