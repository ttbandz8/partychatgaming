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

'''Delete Team'''
def deleteTeam(team, user):
    try:
        exists = team_exists({'TNAME': team['TNAME']})
        if exists:
            team = teams_col.find_one(team)
            if user in team['MEMBERS']:
                teams_col.delete_one({'TNAME': team['TNAME']})
                print("Team deleted.")
            else:
                print("This user is not a member of the team.")
        else:
            print("Team does not exist.")

    except:
        print("Delete Team failed.")

'''Delete Team Member'''
def deleteTeamMember(query, value, user):
    try:
        exists = team_exists({'TNAME': query['TNAME']})
        if exists:
            team = teams_col.find_one(query)
            if user in team['MEMBERS']:
                update = teams_col.update_one(query, value, upsert=True)
                print(update)
            else:
                print("This user is not a member of the team.")
        else:
            print("Team does not exist.")

    except:
        print("Delete Team Member failed.")

'''Updates Team data'''
def updateTeam(query, new_value, user):
    exists = team_exists({'TNAME': query['TNAME']})
    if exists:
        team = teams_col.find_one(query)
        if user in team['MEMBERS']:
            update = teams_col.update_one(query, new_value, upsert=True)
            print(update)
        else:
            print("This user is not a member of the team.")
    else:
        print("Cannot update.")



