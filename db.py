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
            return data
        else:
            return False
           
    except:
        return "Find user failed. "


'''Create User'''
def createUsers(users):
    try:
        if isinstance(users, list):
            for user in users:
                exists = user_exists({'DISNAME': user['DISNAME']})
                if exists:
                    print("User already exists.")
                else:
                    data = users_col.insert_one(user)
                    return data
        else:
            exists = user_exists({'DISNAME': users['DISNAME']})
            if exists:
                return "User already registered. "
            else:
                print("Inserting new user.")
                data = users_col.insert_one(users)
                return "Registration complete. "
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
                    return "User removed from the system. "
                else:
                    return "User does not exist in the system. "
        else:
            exists = user_exists({'DISNAME': users['DISNAME']})
            if exists:
                users_col.delete_one({'DISNAME': users['DISNAME']})
                return "User has been removed from the system. "
            else:
                return "User does not exist in the system. "

    except:
        print("Delete User failed.")

'''Updates User data'''
def updateUser(query, new_value):
    exists = user_exists({'DISNAME': query['DISNAME']})
    if exists:
        update = users_col.update_one(query, new_value, upsert=True)
        return "Update completed. "
    else:
        return "Update failed. "





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


'''Check If Games Exists'''
def game_exists(game):
    collection_exists = col_exists("GAMES")
    if collection_exists:
        gamesexist = games_col.find_one(game)
        if gamesexist:
            return True
        else:
            return False
    else:
        return False

'''Query Game'''
def queryGame(game):
    try:
        exists = game_exists({'ALIASES': game['ALIASES']})
        if exists:
            data = games_col.find_one(game)
            return data
        else:
            print("Game doesn't exist.")
    except:
        print("Find Game failed.")

'''Query Game'''
def query_all_games():
    games = games_col.find()
    return games

'''Add Game'''
def add_game(game):
    exists = game_exists({'GAME': game['GAME']})
    if exists:
        print("Game Already Exists.")
    else:
       added = games_col.insert_one(game)
       return("Game has been added")





'''Check If Sessions Exists'''
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

'''Query Session'''
def querySession(session):
    try:
        exists = session_exist({'OWNER': session['OWNER'], 'AVAILABLE': True})
        if exists:
            data = sessions_col.find_one(session)
            return data
        else:
            return False
           
    except:
        return "Find Session failed."

'''Create Session'''
def createSession(session):
    exists = session_exist({'OWNER': session['OWNER'], 'AVAILABLE': True})
    if exists:
        return "Session Already Exists."
    else:
        players_per_team_count = [x for x in session['TEAMS'][0]['TEAM']]
        if session['TYPE'] != len(players_per_team_count):
            print(players_per_team_count)
            return "Team and Session Type do not match. "
        else:
            sessions_col.insert_one(session)
            return "New Session started. "

'''Join Session'''
def joinSession(session, query):
    sessionquery = querySession(session)
    matchtype = sessionquery['TYPE']
    if matchtype == len(query['TEAM']):
        p = [x for x in sessionquery['TEAMS']]
        list_matching = [x for x in p[0]['TEAM'] if x in query['TEAM']]
        if len(list_matching) == 0:
            teaminsert = sessions_col.update_one(session, {'$addToSet': {'TEAMS': query}, '$set': {'IS_FULL': True}})
            return 'Session Joined'
        else: 
            return 'Session full.'
    elif matchtype < len(query['TEAM']):
        return 'Too many players in team'
    elif matchtype > len(query['TEAM']):
        return 'Not enough players in team'

'''End Session'''
def endSession(session):
    exists = session_exist({'OWNER': session['OWNER'], 'AVAILABLE': True})
    if exists:
        sessions_col.update_one(session, {'$set': {'AVAILABLE': False}})
        return 'Session Ended'
    else:
        return 'Session Unavailable'
