import pymongo 
import messages as m
from decouple import config

# PRODUCTION
TOKEN = config('MONGODB_URI')

# TEST
# TOKEN = config('MONGOTOKEN_TEST')
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
goc_col = db["GOC"]

vault_col =db["VAULT"]

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


'''Check If Vault exist'''
def vault_exist(data):
    collection_exists = col_exists("VAULT")
    if collection_exists:
        vault_does_exist = vault_col.find_one(data)
        if vault_does_exist:
            return True
        else:
            return False
    else:
        return False


'''New Vault'''
def createVault(vault):
    try:
        vaultexist = vault_exist({'OWNER': vault['OWNER']})
        if vaultexist:
            return False
        else:
            vault_col.insert_one(vault)
            return True
    except:
        return "Cannot create vault."

def queryAllVault():
    data = vault_col.find()
    return data

def queryVault(query):
    data = vault_col.find_one(query)
    return data


def altQueryVault(query):
    data = vault_col.find_one(query)
    return data

'''Delete Vault'''
def deleteVault(vaults):
    try:
        if isinstance(vaults, list):
            for vault in vaults:
                exists = vault_exist(vault)
                if exists:
                    vault_col.delete_one({'OWNER': vault['OWNER']})
                    return "Vault removed from the system. "
                else:
                    return "Vault does not exist in the system. "
        else:
            exists = vault_exist({'OWNER': vaults['OWNER']})
            if exists:
                vault_col.delete_one({'OWNER': vaults['OWNER']})
                return "Vault has been removed from the system. "
            else:
                return "Vault does not exist in the system. "

    except:
        print("Delete Vault failed.")


'''Update Vault With No Array Filters'''
def updateVaultNoFilter(query, new_value):
    exists = vault_exist({'OWNER': query['OWNER']})
    if exists:
        update = vault_col.update_one(query, new_value)
        return "Update completed. "
    else:
        return "Update failed. "


''' GOC '''
'''Check If Card Exists'''
def goc_exists(data):
    collection_exists = col_exists("GOC")
    if collection_exists:
        goc_does_exist = goc_col.find_one(data)
        if goc_does_exist:
            return True
        else:
            return False
    else:
        return False

def createGoc(query):
    exists = goc_exists(query)
    if exists:
        return "Gods of Cod already created. "
    else:
        response = goc_col.insert_one(query)
        return "Gods Of COD Created. "

def queryGoc(query):
    response = goc_col.find_one(query)
    return response

def deleteGoc(query):
    response = goc_col.delete_one(query)
    return response

def updateGoc(query, new_value):
    exists = goc_exists(query)
    if exists:
        data = goc_col.update_one(query, new_value)
    else:
        return m.TOURNEY_DOES_NOT_EXIST

def addTeamMember(query, add_to_team_query, user, new_user):
    exists = team_exists({'TNAME': query['TNAME']})
    if exists:
        team = teams_col.find_one(query)
        if user == team['OWNER']:
            teams_col.update_one(query, add_to_team_query, upsert=True)

             # Add Team to User Profile as well
            query = {'DISNAME': new_user}
            new_value = {'$set': {'TEAM': team['TNAME']}}
            users_col.update_one(query, new_value)
            return "User added to the team. "
        else:
            return "The Owner of the team can add new members. "
    else:
        return "Cannot add user to the team."


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

def deleteAllCards(user_query):
    exists = user_exists({'DISNAME': user_query['DISNAME']})
    if exists:
        cards_col.delete_many({})
        return 'All Cards Deleted'
    else:
        return 'Unable to Delete All Cards'

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

def queryTournamentCards():
    data = cards_col.find({'TOURNAMENT_REQUIREMENTS': {'$gt': 0}})
    return data

def queryShopCards():
    data = cards_col.find({'TOURNAMENT_REQUIREMENTS': 0})
    return data 

def altQueryShopCards(args):
    data = cards_col.find({'TOURNAMENT_REQUIREMENTS': 0})
    return data 

def queryCard(query):
    data = cards_col.find_one(query)
    return data

def updateCard(query, new_value):
    try:
        cardexists = card_exists({'PATH': query['PATH']})
        if cardexists:
            cards_col.update_one(query, new_value)
            return True
        else:
            return False
    except:
        return False

def deleteCard(card):
    try:
        cardexists = card_exists({'PATH': query['PATH']})
        if cardexists:
            cards_col.delete_one(card)
            return True
        else:
            return False
    except:
        return False


''' TITLES '''
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

def updateTitle(query, new_value):
    try:
        titleexists = title_exists({'TITLE': query['TITLE']})
        if titleexists:
            titles_col.update_one(query, new_value)
            return True
        else:
            return False
    except:
        return False

def deleteTitle(title):
    try:
        titleexists = title_exists({'TITLE': query['TITLE']})
        if titleexists:
            titles_col.delete_one(title)
            return True
        else:
            return False
    except:
        return False

def queryAllTitles():
    data = titles_col.find()
    return data

def queryTitle(query):
    data = titles_col.find_one(query)
    return data

def queryTournamentTitles():
    data = titles_col.find({'TOURNAMENT_REQUIREMENTS': {'$gt': 0}})
    return data

def queryShopTitles():
    data = titles_col.find({'TOURNAMENT_REQUIREMENTS': 0})
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
        return False

def queryAllUsers():
    data = users_col.find()
    return data

def createUsers(users):
    exists = user_exists({'DISNAME': users['DISNAME']})
    if exists:
        print("Does exist")
        return False
    else:
        data = users_col.insert_one(users)
        return True
    
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



''' TEAMS '''
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

def queryTeam(team):
    try:
        exists = team_exists({'TNAME': team['TNAME']})
        if exists:
            data = teams_col.find_one(team)
            return data
        else:
           return False
    except:
        print("Find team failed.")

def updateTeam(query, new_value):
    try:
        exists = team_exists({'TNAME': query['TNAME']})
        if exists:
            data = teams_col.update_one(query, new_value)
            return data
        else:
           return False
    except:
        print("Find team failed.")

def queryAllTeams(team):
    data = teams_col.find()
    return data

def createTeam(team, user):
    try:
        find_user = queryUser({'DISNAME': user})
        if find_user['TEAM'] and find_user['TEAM'] != 'PCG':
            return "User is already part of a team. "
        else:
            exists = team_exists({'TNAME': team['TNAME']})
            if exists:
                return "Team already exists."
            else:
                print("Inserting new Team.")
                teams_col.insert_one(team)

                # Add Team to User Profile as well
                query = {'DISNAME': user}
                new_value = {'$set': {'TEAM': team['TNAME']}}
                users_col.update_one(query, new_value)
                return "Team has been created. "
    except:
        return "Cannot create team."

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

def deleteTeamMember(query, value, user):
    try:
        exists = team_exists({'TNAME': query['TNAME']})
        if exists:
            team = teams_col.find_one(query)
            if user in team['MEMBERS']:

                update = teams_col.update_one(query, value, upsert=True)
                # Add Team to User Profile as well
                query = {'DISNAME': str(user)}
                new_value = {'$set': {'TEAM': 'PCG'}}
                users_col.update_one(query, new_value)
                return "User has been removed from team. "
            else:
                return "This user is not a member of the team."
        else:
            return "Team does not exist."

    except:
        print("Delete Team Member failed.")

def addTeamMember(query, add_to_team_query, user, new_user):
    exists = team_exists({'TNAME': query['TNAME']})
    if exists:
        team = teams_col.find_one(query)
        if user == team['OWNER']:
            teams_col.update_one(query, add_to_team_query, upsert=True)

             # Add Team to User Profile as well
            query = {'DISNAME': new_user}
            new_value = {'$set': {'TEAM': team['TNAME']}}
            users_col.update_one(query, new_value)
            return "User added to the team. "
        else:
            return "The Owner of the team can add new members. "
    else:
        return "Cannot add user to the team."

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



''' GAMES '''
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

def deleteGame(game):
    try:
        exists = game_exists({'GAME': game['GAME']})
        if exists:
            data = games_col.delete_one(game)
            return True
        else:
            return False
    except:
        print("Find Game failed.")

def query_all_games():
    games = games_col.find()
    if games:
        return games
    else:
        return False

def addGame(game):
    exists = game_exists({'GAME': game['GAME']})
    if exists:
        print("Game Already Exists.")
    else:
       added = games_col.insert_one(game)
       return("Game has been added")

def updateGame(query, new_value):
    exists = game_exists({'GAME': query['GAME']})
    if exists:
       added = games_col.update_one(query, new_value)
       return("Game has been added")
    else:
        return False


''' SESSIONS '''
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

def querySessionForUser(query):
    data = sessions_col.find(query)
    return data
   
def querySessionMembers(session):
    data = sessions_col.find_one(session)
    return data

def createSession(session):
    exists = session_exist({'OWNER': session['OWNER'], 'AVAILABLE': True})
    if exists:
        return "Session Already Exists."
    else:
        if session['TOURNAMENT']:
            sessions_col.insert_one(session)
            return "New Tournament Session has been created"
        else:       
            players_per_team_count = [x for x in session['TEAMS'][0]['TEAM']]
            if session['TYPE'] != len(players_per_team_count):

                return "Team and Session Type do not match. "
            else:
                sessions_col.insert_one(session)
                return "New Session started. "

def joinSession(session, query):
    sessionquery = querySession(session)
    matchtype = sessionquery['TYPE']
    if not sessionquery['IS_FULL']:
        if sessionquery['GOC'] and query['POSITION'] == 0:
            teaminsert = sessions_col.update_one(session, {'$addToSet': {'TEAMS': query}})
            return m.SESSION_JOINED
        else:
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
    else:
        return "Session is full. "

def joinExhibition(session, query):
    sessionquery = querySession(session)
    matchtype = sessionquery['TYPE']
    if len(query['TEAM']) != 3:
        if len(query['TEAM']) != 1:       
            # List of current teams in session
            p = [x for x in sessionquery['TEAMS']]
            
            # Check if team trying to join is part of a team already
            list_matching = [x for x in p[0]['TEAM'] if x in query['TEAM']]

            if len(list_matching) == 0:
                teaminsert = sessions_col.update_one(session, {'$addToSet': {'TEAMS': query}, '$set': {'IS_FULL': True}})

                return m.SESSION_JOINED
            else: 
                return 'Session full.'
        else:
            teaminsert = sessions_col.update_one(session, {'$addToSet': {'TEAMS': query}})
            return m.SESSION_JOINED

def joinKingsGambit(session, query):
    sessionquery = querySession(session)
    matchtype = sessionquery['TYPE']
    if len(query['TEAM']) != 3:
        if len(query['TEAM']) != 1:       
            # List of current teams in session
            p = [x for x in sessionquery['TEAMS']]
            
            # Check if team trying to join is part of a team already
            list_matching = [x for x in p[0]['TEAM'] if x in query['TEAM']]

            if len(list_matching) == 0:
                teaminsert = sessions_col.update_one(session, {'$addToSet': {'TEAMS': query}})

                return m.SESSION_JOINED
            else: 
                return 'Session full.'
        else:
            teaminsert = sessions_col.update_one(session, {'$addToSet': {'TEAMS': query}})
            return m.SESSION_JOINED

def endSession(session):
    exists = session_exist({'OWNER': session['OWNER'], 'AVAILABLE': True})
    if exists:
        sessions_col.update_one(session, {'$set': {'AVAILABLE': False}})
        return 'Session Ended'
    else:
        return 'Session Unavailable'

def deleteSession(session):
    exists = session_exist({'OWNER': session['OWNER'], 'AVAILABLE': True})
    if exists:
        sessions_col.delete_one({'OWNER': session['OWNER'], 'AVAILABLE': True})
        return 'Session Ended'
    else:
        return 'Session Unavailable'

def deleteAllSessions(user_query):
    exists = user_exists({'DISNAME': user_query['DISNAME']})
    if exists:
        sessions_col.delete_many({})
        return 'All Sessions Deleted'
    else:
        return 'Unable to Delete All Sessions'

def updateSession(session, query, update_query):
    exists = session_exist({'OWNER': session['OWNER'], 'AVAILABLE': True})
    if exists:
        sessions_col.update_one(query, update_query)
        return True
    else:
        return False




''' KINGS GAMBIT '''
def updatekg(session, query, update_query, arrayFilter):
    exists = session_exist({'OWNER': session['OWNER'], 'AVAILABLE': True, "KINGSGAMBIT": True})
    if exists:
        sessions_col.update_one(query, update_query,  array_filters=arrayFilter)
        return True
    else:
        return False