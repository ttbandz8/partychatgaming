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
cards_col = db["CARDS"]
titles_col = db["TITLES"]

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
        user_does_exist = users_col.find_one(data)
        if user_does_exist:
            return True
        else:
            return False
    else:
        return False

'''Check If Card Exists'''
def card_exists(data):
    collection_exists = col_exists("CARDS")
    if collection_exists:
        card_does_exist = cards_col.find_one(data)
        if card_does_exist:
            return True
        else:
            return False
    else:
        return False

'''New Card'''
def createCard(card):
    try:
        cardexists = card_exists({'PATH': card['PATH']})
        if cardexists:
            return "Card already exists."
        else:
            cards_col.insert_one(card)
            return "New Card created."
    except:
        return "Cannot create card."

def queryAllCards():
    data = cards_col.find()
    return data

def queryCard(query):
    data = cards_col.find_one(query)
    return data


'''Check If Title Exists'''
def title_exists(data):
    collection_exists = col_exists("TITLES")
    if collection_exists:
        title_does_exist = titles_col.find_one(data)
        if title_does_exist:
            return True
        else:
            return False
    else:
        return False

'''New Title'''
def createTitle(title):
    try:
        titleexists = title_exists({'TITLE': title['TITLE']})
        if titleexists:
            return "Title already exists."
        else:
            titles_col.insert_one(title)
            return "New Title created."
    except:
        return "Cannot create Title."

def queryAllTitles():
    data = titles_col.find()
    return data

def queryTitle(query):
    data = titles_col.find_one(query)
    return data





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
def updateUser(query, new_value, arrayFilters):
    exists = user_exists({'DISNAME': query['DISNAME']})
    if exists:
        update = users_col.update_one(query, new_value, array_filters=arrayFilters)
        return "Update completed. "
    else:
        return "Update failed. "

def updateUserNoFilter(query, new_value):
    exists = user_exists({'DISNAME': query['DISNAME']})
    if exists:
        update = users_col.update_one(query, new_value)
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
                return "Team already exists."
            else:
                print("Inserting new Team.")
                teams_col.insert_one(team)

                # Add Team to User Profile as well
                query = {'DISNAME': user}
                new_value = {'$set': {'TEAMS': [team['TNAME']]}}
                users_col.update_one(query, new_value)
                return "Team has been created. "
        else:
            return "User does not exist. Create profile."
    except:
        return "Cannot create team."

'''Delete Team'''
def deleteTeam(team, user):
    try:
        exists = team_exists({'TNAME': team['TNAME']})
        if exists:
            team = teams_col.find_one(team)
            if user == team['OWNER']:
                users_col.update_many({'TEAMS': team['TNAME']}, {'$set': {'TEAMS': ['PCG']}})
                teams_col.delete_one({'TNAME': team['TNAME']})
                return "Team deleted."
            else:
                return "This user is not a member of the team."
        else:
            return "Team does not exist."

    except:
        return "Delete Team failed."

'''Delete Team Member'''
def deleteTeamMember(query, value, user):
    try:
        exists = team_exists({'TNAME': query['TNAME']})
        if exists:
            team = teams_col.find_one(query)
            if user in team['MEMBERS']:

                update = teams_col.update_one(query, value, upsert=True)
                # Add Team to User Profile as well
                query = {'DISNAME': user}
                new_value = {'$set': {'TEAMS': ['PCG']}}
                users_col.update_one(query, new_value)

            else:
                return "This user is not a member of the team."
        else:
            return "Team does not exist."

    except:
        print("Delete Team Member failed.")

'''Updates Team data'''
def addTeamMember(query, add_to_team_query, user, new_user):
    exists = team_exists({'TNAME': query['TNAME']})
    if exists:
        team = teams_col.find_one(query)
        if user == team['OWNER']:
            teams_col.update_one(query, add_to_team_query, upsert=True)

             # Add Team to User Profile as well
            query = {'DISNAME': new_user}
            new_value = {'$set': {'TEAMS': [team['TNAME']]}}
            users_col.update_one(query, new_value)
            return "User added to the team. "
        else:
            return "The Owner of the team can add new members. "
    else:
        return "Cannot add user to the team."


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
        
'''Query Session Members'''
def querySessionMembers(session):
    data = sessions_col.find_one(session)
    return data

'''Create Session'''
def createSession(session):
    exists = session_exist({'OWNER': session['OWNER'], 'AVAILABLE': True})
    if exists:
        return "Session Already Exists."
    else:
        players_per_team_count = [x for x in session['TEAMS'][0]['TEAM']]
        if session['TYPE'] != len(players_per_team_count):

            return "Team and Session Type do not match. "
        else:
            sessions_col.insert_one(session)
            return "New Session started. "

'''Join Session'''
def joinSession(session, query):
    sessionquery = querySession(session)
    matchtype = sessionquery['TYPE']
    if matchtype == len(query['TEAM']):
        # List of current teams in session
        p = [x for x in sessionquery['TEAMS']]
        
        # Check if team trying to join is part of a team already
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



'''Join Kings Gambit'''
def joinKingsGambit(session, query):
    sessionquery = querySession(session)
    matchtype = sessionquery['TYPE']
    if matchtype == len(query['TEAM']):
        # List of current teams in session
        p = [x for x in sessionquery['TEAMS']]
        
        # Check if team trying to join is part of a team already
        list_matching = [x for x in p[0]['TEAM'] if x in query['TEAM']]

        if len(list_matching) == 0:
            teaminsert = sessions_col.update_one(session, {'$addToSet': {'TEAMS': query}})

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

'''End Session'''
def deleteSession(session):
    exists = session_exist({'OWNER': session['OWNER'], 'AVAILABLE': True})
    if exists:
        sessions_col.delete_one({'OWNER': session['OWNER'], 'AVAILABLE': True})
        return 'Session Ended'
    else:
        return 'Session Unavailable'

'''Update Session'''
def updateSession(session, query, update_query):
    exists = session_exist({'OWNER': session['OWNER'], 'AVAILABLE': True})
    if exists:
        sessions_col.update_one(query, update_query)
        return True
    else:
        return False