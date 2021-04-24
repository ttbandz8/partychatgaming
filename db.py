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

'''Query User'''
def queryUser(user):
    try:
        exists = user_exists({'DISNAME': user['DISNAME']})
        if exists:
            data = users_col.find_one(user)
            print(data)
            return data
        else:
            print("User doesn't exist.")
           
    except:
        print("Find user failed.")


'''Create User'''
def createUsers(users):
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


'''Query Team'''
def queryTeam(team):
    try:
        exists = team_exists({'TNAME': team['TNAME']})
        if exists:
            data = teams_col.find_one(team)
            print(data)
            return data
        else:
            print("Team doesn't exist.")
           
    except:
        print("Find team failed.")

'''Add new Team'''
def createTeam(team, user):
    try:
        user_exist = user_exists({'DISNAME': user})
        if user_exist:
            exists = team_exists({'TNAME': team['TNAME']})
            if exists:
                print("Team already exists.")
            else:
                print("Inserting new Team.")
                teams_col.insert_one(team)

                # Add Team to User Profile as well
                query = {'DISNAME': user}
                new_value = {'$addToSet': {'TEAMS': team['TNAME']}}
                users_col.update_one(query, new_value)
                print("Team added to user profile")
        else:
            print("User does not exist. Create profile.")
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
                users_col.update_many({'TEAMS': team['TNAME']}, {'$pull': {'TEAMS':  team['TNAME']}})
                print("Team deleted from user profile.")
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
def addTeamMember(query, new_value, user):
    exists = team_exists({'TNAME': query['TNAME']})
    if exists:
        team = teams_col.find_one(query)
        if user in team['MEMBERS']:
            teams_col.update_one(query, new_value, upsert=True)
            print("User added to the team.")


             # Add Team to User Profile as well
            add_user = [x for x in new_value.values()][0]['MEMBERS']
            query = {'DISNAME': add_user}
            new_value = {'$addToSet': {'TEAMS': team['TNAME']}}
            users_col.update_one(query, new_value)
            print("Team added to user profile")
        else:
            print("This user is not a member of the team.")
    else:
        print("Cannot update.")







'''Check If Teams Exists'''
def session_exist(data):
    collection_exists = col_exists("SESSIONS")
    if collection_exists:
        sessionexists = sessions_col.find_one(data)
        if sessionexists:
            return True
        else:
            return False
    else:
        return False

'''Create Session'''
def createSession(session):
    exists = session_exist({'OWNER': session['OWNER'], 'AVAILABLE': True})
    if exists:
        print("Unable to create session.")
    else:
        print("Inserting new user.")
        # users_col.insert_one(users)


