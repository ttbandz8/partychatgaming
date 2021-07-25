import pymongo 
import messages as m
from decouple import config

if config('ENV') == "production":
    # PRODUCTION
    use_database = "PCGPROD"
else:
    # TEST
    use_database = "PCGTEST"

TOKEN = config('MONGOTOKEN_TEST')
mongo = pymongo.MongoClient(TOKEN)

print(use_database)

db = mongo[use_database]
users_col = db["USERS"]
teams_col = db["TEAMS"]
family_col = db["FAMILY"]
sessions_col = db["SESSIONS"]
games_col = db["GAMES"]
matches_col = db["MATCHES"]
tournaments_col = db["TOURNAMENTS"]
cards_col = db["CARDS"]
titles_col = db["TITLES"]
gods_col = db["GODS"]
arm_col = db["ARM"]
universe_col = db['UNIVERSE']
boss_col = db['BOSS']
pet_col = db['PET']
vault_col =db["VAULT"]
house_col =db["HOUSE"]

'''Check if Collection Exists'''
def col_exists(col):
    collections = db.list_collection_names()
    if col in collections:
        return True
    else:
        return False

#########################################################################
''' FAMILY '''
def family_exists(data):
    collection_exists = col_exists("FAMILY")
    if collection_exists:
        familyexists = family_col.find_one(data)
        if familyexists:
            return True
        else:
            return False
    else:
        return False

def updateManyFamily(new_value):
    family_col.update_many({}, new_value)
    return True

def queryFamily(family):
    try:
        exists = family_exists({'HEAD': family['HEAD']})
        if exists:
            data = family_col.find_one(family)
            return data
        else:
           return False
    except:
        print("Find family failed.")

def updateFamily(query, new_value):
    try:
        exists = family_exists({'HEAD': query['HEAD']})
        if exists:
            data = family_col.update_one(query, new_value)
            return data
        else:
           return False
    except:
        print("Find family failed.")

def queryAllFamily(family):
    data = family_col.find()
    return data

def createFamily(family, user):
    try:
        find_user = queryUser({'DISNAME': user})
        if find_user['FAMILY'] and find_user['FAMILY'] != 'PCG':
            return "User is already part of a Family. "
        else:
            exists = family_exists({'HEAD': family['HEAD']})
            if exists:
                return "Family already exists."
            else:
                print("Inserting new Family.")
                family_col.insert_one(family)

                # Add Team to User Profile as well
                query = {'DISNAME': user}
                new_value = {'$set': {'FAMILY': family['HEAD']}}
                users_col.update_one(query, new_value)
                return "Family has been created. "
    except:
        return "Cannot create Family."

def deleteFamily(family, user):
    try:
        exists = family_exists({'HEAD': family['HEAD']})
        if exists:
            family = family_col.find_one(family)
            if user == family['HEAD']:
                users_col.update_many({'FAMILY': family['HEAD']}, {'$set': {'FAMILY': 'PCG'}})
                family_col.delete_one({'HEAD': family['HEAD']})
                return "Family deleted."
            else:
                return "This user is not a member of the Family."
        else:
            return "Family does not exist."

    except:
        return "Delete Family failed."

def deleteFamilyMember(query, value, user, new_user):
    try:
        exists = family_exists({'HEAD': query['HEAD']})
        if exists:
            family = family_col.find_one(query)
            if user == family['HEAD']:
                update = family_col.update_one(query, value, upsert=True)
                # Add Team to User Profile as well
                query = {'DISNAME': str(new_user)}
                new_value = {'$set': {'FAMILY': 'PCG'}}
                users_col.update_one(query, new_value)
                return "User has been removed from family. "
            else:
                return "This user is not a member of the family."
        else:
            return "Family does not exist."

    except:
        print("Delete Team Member failed.")

def deleteFamilyMemberAlt(query, value, user):
    try:
        exists = family_exists({'HEAD': query['HEAD']})
        if exists:
            family = family_col.find_one(query)
            if user in family['KIDS']:
                update = family_col.update_one(query, value, upsert=True)
                # Add Team to User Profile as well
                query = {'DISNAME': str(user)}
                new_value = {'$set': {'FAMILY': 'PCG'}}
                users_col.update_one(query, new_value)
                return "User has been removed from family. "
            else:
                return "This user is not a member of the family."
        else:
            return "Family does not exist."

    except:
        print("Delete Team Member failed.")


def addFamilyMember(query, add_to_family_query, user, new_user):
    exists = family_exists({'HEAD': query['HEAD']})
    if exists:
        family = family_col.find_one(query)
        if user == family['HEAD']:
            family_col.update_one(query, add_to_family_query, upsert=True)

             # Add Team to User Profile as well
            query = {'DISNAME': new_user}
            new_value = {'$set': {'FAMILY': family['HEAD']}}
            users_col.update_one(query, new_value)
            return "User added to the Family. "
        else:
            return "The Owner of the Family can add new members. "
    else:
        return "Cannot add user to the Family."

#########################################################################
''' MATCHES '''
def matches_exists(data):
    collection_exists = col_exists("MATCHES")
    if collection_exists:
        matchexists = matches_col.find_one(data)
        if matchexists:
            return True
        else:
            return False
    else:
        return False

def updateManyMatches(new_value):
    matches_col.update_many({}, new_value)
    return True

def queryMatch(matches):
    try:
        exists = matches_exists({'CARD': matches['CARD']})
        if exists:
            data = matches_col.find_one(matches)
            return data
        else:
           return False
    except:
        print("Find matches failed.")

def queryManyMatches(matches):
    try:
        exists = matches_exists({'CARD': matches['CARD']})
        if exists:
            data = matches_col.find(matches)
            return data
        else:
           return False
    except:
        print("Find matches failed.")

def queryManyMatchesPerPlayer(matches):
    try:
        exists = matches_exists({'PLAYER': matches['PLAYER']})
        if exists:
            data = matches_col.find(matches)
            return data
        else:
           return False
    except:
        print("Find matches failed.")

def queryAllMatches(matches):
    data = matches_col.find()
    return data

def createMatch(match):
    resp = matches_col.insert_one(match)
    if resp:
        return True
    else:
        return False

#########################################################################
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

def updateManyVaults(new_value):
    vault_col.update_many({}, new_value)
    return True


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

def updateVault(query, new_value, arrayFilters):
    exists = vault_exist({'OWNER': query['OWNER']})
    if exists:
        update = vault_col.update_one(query, new_value, array_filters=arrayFilters)
        return True
    else:
        return False

'''Update Vault With No Array Filters'''
def updateVaultNoFilter(query, new_value):
    exists = vault_exist({'OWNER': query['OWNER']})
    if exists:
        update = vault_col.update_one(query, new_value)
        return "Update completed. "
    else:
        return "Update failed. "


def gods_exists(data):
    collection_exists = col_exists("GODS")
    if collection_exists:
        gods_does_exist = gods_col.find_one(data)
        if gods_does_exist:
            return True
        else:
            return False
    else:
        return False

def createGods(query):
    exists = gods_exists(query)
    if exists:
        return "Gods already created. "
    else:
        response = gods_col.insert_one(query)
        return "Gods Created. "

def queryGods(query):
    response = gods_col.find_one(query)
    return response

def deleteGods(query):
    response = gods_col.delete_one(query)
    return response

def updateGods(query, new_value):
    exists = gods_exists(query)
    if exists:
        data = gods_col.update_one(query, new_value)
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

# def deleteAllCards(user_query):
#     exists = user_exists({'DISNAME': user_query['DISNAME']})
#     if exists:
#         cards_col.delete_many({'UNIVERSE': 'Dragon Ball Z'})
#         return 'All Cards Deleted'
#     else:
#         return 'Unable to Delete All Cards'

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

def queryAllCardsBasedOnUniverse(query):
    data = cards_col.find(query)
    return data

def queryTournamentCards():
    data = cards_col.find({'TOURNAMENT_REQUIREMENTS': {'$gt': 0}, 'AVAILABLE': True})
    return data

def queryShopCards():
    data = cards_col.find({'EXCLUSIVE': False, 'AVAILABLE': True, 'HAS_COLLECTION': False})
    return data 

def altQueryShopCards(args):
    data = cards_col.find({'EXCLUSIVE': False, 'AVAILABLE': True})
    return data 

def queryDropCards(args):
    data = cards_col.find({'UNIVERSE': args, 'EXCLUSIVE': False, 'AVAILABLE': True})
    return data 

def queryExclusiveDropCards(args):
    data = cards_col.find({'UNIVERSE': args, 'EXCLUSIVE': True, 'AVAILABLE': True})
    return data 

def queryCard(query):
    data = cards_col.find_one(query)
    return data

def updateCard(query, new_value):
    try:
        cardexists = card_exists({'NAME': query['NAME']})
        if cardexists:
            cards_col.update_one(query, new_value)
            return True
        else:
            return False
    except:
        return False

def updateManyCards(new_value):
    cards_col.update_many({}, new_value)
    return True


def deleteCard(card):
    try:
        cardexists = card_exists({'PATH': card['PATH']})
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

def updateManyTitles(new_value):
    titles_col.update_many({}, new_value)
    return True

def deleteTitle(title):
    try:
        titleexists = title_exists({'TITLE': title['TITLE']})
        if titleexists:
            titles_col.delete_one(title)
            return True
        else:
            return False
    except:
        return False

def deleteAllTitles(user_query):
    exists = user_exists({'DISNAME': user_query['DISNAME']})
    if exists:
        titles_col.delete_many({})
        return 'All Titles Deleted'
    else:
        return 'Unable to Delete All Titles'

def queryAllTitles():
    data = titles_col.find()
    return data

def queryAllTitlesBasedOnUniverses(query):
    data = titles_col.find(query)
    return data

def queryTitle(query):
    data = titles_col.find_one(query)
    return data

def queryDropTitles(args):
    data = titles_col.find({'UNIVERSE': args, 'EXCLUSIVE': False, 'AVAILABLE': True})
    return data 

def queryExclusiveDropTitles(args):
    data = titles_col.find({'UNIVERSE': args, 'EXCLUSIVE': True, 'AVAILABLE': True})
    return data 

def queryTournamentTitles():
    data = titles_col.find({'TOURNAMENT_REQUIREMENTS': {'$gt': 0}, 'AVAILABLE': True})
    return data

def queryShopTitles():
    data = titles_col.find({'EXCLUSIVE': False, 'AVAILABLE': True})
    return data 



''' ARM '''
def arm_exists(data):
    collection_exists = col_exists("ARM")
    if collection_exists:
        arm_does_exist = arm_col.find_one(data)
        if arm_does_exist:
            return True
        else:
            return False
    else:
        return False

def createArm(arm):
    try:
        armexists = arm_exists({'ARM': arm['ARM']})
        if armexists:
            return "ARM already exists."
        else:
            arm_col.insert_one(arm)
            return "New ARM created."
    except:
        return "Cannot create ARM."

def updateArm(query, new_value):
    try:
        armexists = arm_exists({'ARM': query['ARM']})
        if armexists:
            arm_col.update_one(query, new_value)
            return True
        else:
            return False
    except:
        return False

def updateManyArms(new_value):
    arm_col.update_many({}, new_value)
    return True

def deleteArm(query):
    try:
        armexists = arm_exists({'ARM': query['ARM']})
        if armexists:
            arm_col.delete_one(query)
            return True
        else:
            return False
    except:
        return False

def queryAllArms():
    data = arm_col.find()
    return data

def queryAllArmsBasedOnUniverses(query):
    data = arm_col.find(query)
    return data

def queryArm(query):
    data = arm_col.find_one(query)
    return data

def queryDropArms(args):
    data = arm_col.find({'UNIVERSE': args, 'EXCLUSIVE': False, 'AVAILABLE': True})
    return data 

def queryExclusiveDropArms(args):
    data = arm_col.find({'UNIVERSE': args, 'EXCLUSIVE': True, 'AVAILABLE': True})
    return data 

def queryTournamentArms():
    data = arm_col.find({'TOURNAMENT_REQUIREMENTS': {'$gt': 0}, 'AVAILABLE': True})
    return data

def queryShopArms():
    data = arm_col.find({'EXCLUSIVE': False, 'AVAILABLE': True})
    return data 


''' HOUSE '''
def house_exist(data):
    collection_exists = col_exists("HOUSE")
    if collection_exists:
        house_does_exist = house_col.col.find_one(data)
        if house_does_exist:
            return True
        else:
            return False
    else:
        return False

def createHouse(house):
    try:
        houseexists = house_exist({'HOUSE': house['HOUSE']})
        if houseexists:
            return "HOUSE already exists."
        else:
            house_col.insert_one(house)
            return "New HOUSE created."
    except:
        return "Cannot create HOUSE."

def updateHouse(query, new_value):
    try:
        houseexists = house_exist({'HOUSE': query['HOUSE']})
        if houseexists:
            house_col.update_one(query, new_value)
            return True
        else:
            return False
    except:
        return False

def updateManyHouses(new_value):
    house_col.update_many({}, new_value)
    return True

def deleteHouse(query):
    try:
        houseexists = house_exist({'HOUSE': query['HOUSE']})
        if houseexists:
            house_col.delete_one(query)
            return True
        else:
            return False
    except:
        return False

def queryAllHouses():
    data = house_col.find()
    return data


def queryHouse(query):
    data = house_col.find_one(query)
    return data


''' PETS '''
def pet_exists(data):
    collection_exists = col_exists("PET")
    if collection_exists:
        pet_does_exist = pet_col.find_one(data)
        if pet_does_exist:
            return True
        else:
            return False
    else:
        return False

def createPet(pet):
    try:
        petexists = pet_exists({'PET': pet['PET']})
        if petexists:
            return "Pet already exists."
        else:
            pet_col.insert_one(pet)
            return "New Pet created."
    except:
        return "Cannot create Pet."

def updatePet(query, new_value):
    try:
        petexists = pet_exists({'PET': query['PET']})
        if petexists:
            pet_col.update_one(query, new_value)
            return True
        else:
            return False
    except:
        return False

def updateManyPets(new_value):
    pet_col.update_many({}, new_value)
    return True

def deletePet(pet):
    try:
        petexists = pet_exists({'PET': pet['PET']})
        if petexists:
            pet_col.delete_one(pet)
            return True
        else:
            return False
    except:
        return False

def deleteAllPet(pet_query):
    exists = pet_exists({'PET': pet_query['PET']})
    if exists:
        pet_col.delete_many({})
        return 'All Pets Deleted'
    else:
        return 'Unable to Delete All Pets'

def queryAllPets():
    data = pet_col.find()
    return data

def queryPet(query):
    data = pet_col.find_one(query)
    return data

def queryDropPets(args):
    data = pet_col.find({'UNIVERSE': args,  'EXCLUSIVE': False,  'AVAILABLE': True})
    return data 

def queryExclusiveDropPets(args):
    data = pet_col.find({'UNIVERSE': args, 'EXCLUSIVE': True, 'AVAILABLE': True})
    return data 

def queryAllPetsBasedOnUniverses(query):
    data = pet_col.find(query)
    return data


''' UNIVERSE '''
def universe_exists(data):
    collection_exists = col_exists("UNIVERSE")
    if collection_exists:
        universe_does_exist = universe_col.find_one(data)
        if universe_does_exist:
            return True
        else:
            return False
    else:
        return False

def updateManyUniverses(new_value):
    universe_col.update_many({}, new_value)
    return True

def createUniverse(universe):
    try:
        universeexists = universe_exists({'TITLE': universe['TITLE']})
        if universeexists:
            return "Universe already exists."
        else:
            universe_col.insert_one(universe)
            return "New Universe created."
    except:
        return "Cannot create Universe."

def updateUniverse(query, new_value):
    try:
        universeexists = universe_exists({'TITLE': query['TITLE']})
        if universeexists:
            universe_col.update_one(query, new_value)
            return True
        else:
            return False
    except:
        return False

def deleteUniverse(query):
    try:
        universeexists = universe_exists({'TITLE': query['TITLE']})
        if universeexists:
            universe_col.delete_one(query)
            return True
        else:
            return False
    except:
        return False

def queryAllUniverse():
    data = universe_col.find()
    return data

def queryUniverse(query):
    data = universe_col.find_one(query)
    return data


''' BOSS '''
def boss_exists(data):
    collection_exists = col_exists("BOSS")
    if collection_exists:
        boss_does_exist = boss_col.find_one(data)
        if boss_does_exist:
            return True
        else:
            return False
    else:
        return False

def updateManyBosses(new_value):
    boss_col.update_many({}, new_value)
    return True

def createBoss(boss):
    try:
        bossexists = boss_exists({'NAME': boss['NAME']})
        if bossexists:
            return "Boss already exists."
        else:
            boss_col.insert_one(boss)
            return "New Boss created."
    except:
        return "Cannot create Boss."

def updateBoss(query, new_value):
    try:
        bossexists = boss_exists({'NAME': query['NAME']})
        if bossexists:
            boss_col.update_one(query, new_value)
            return True
        else:
            return False
    except:
        return False

def deleteBoss(query):
    try:
        bossexists = boss_exists({'NAME': query['NAME']})
        if bossexists:
            boss_col.delete_one(query)
            return True
        else:
            return False
    except:
        return False

def queryAllBosses():
    data = boss_col.find()
    return data

def queryBoss(query):
    data = boss_col.find_one(query)
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

def updateManyUsers(new_value):
    users_col.update_many({}, new_value)
    return True



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

def updateManyTeams(new_value):
    teams_col.update_many({}, new_value)
    return True

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
                users_col.update_many({'TEAM': team['TNAME']}, {'$set': {'TEAM': "PCG"}})
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

def updateManyGames(new_value):
    games_col.update_many({}, new_value)
    return True



''' GAMES '''
def queryGame(game):
    try:
        exists = game_exists({'ALIASES': game['ALIASES']})
        if exists:
            data = games_col.find_one(game)
            return data
        else:
            return False
    except:
        return False

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
        return m.ALREADY_IN_SESSION
    else:
        if session['GAME'] == "Crown Unlimited":
            response = sessions_col.insert_one(session)
            return response
        else:
            if len(session['TEAMS']) == 0:
                sessions_col.insert_one(session)
                return "New Lobby has been created"
            elif session['TOURNAMENT']:
                sessions_col.insert_one(session)
                return "New Tournament Session has been created"
            else:       
                players_per_team_count = [x for x in session['TEAMS'][0]['TEAM']]
                print(players_per_team_count)
                print(session['TYPE'])
                if session['TYPE'] != len(players_per_team_count):

                    return "Team and Session Type do not match. "
                else:
                    sessions_col.insert_one(session)
                    return "New Session started. "

def joinSession(session, query):
    sessionquery = querySession(session)
    matchtype = sessionquery['TYPE']
    if not sessionquery['IS_FULL']:
        if sessionquery['GODS'] and query['POSITION'] == 0:
            teaminsert = sessions_col.update_one(session, {'$addToSet': {'TEAMS': query}})
            return m.SESSION_JOINED
        elif query['POSITION'] == 0:
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

                    return m.SESSION_JOINED
                else: 
                    return 'Lobby full.'
            elif matchtype < len(query['TEAM']):
                return 'Too many players in team'
            elif matchtype > len(query['TEAM']):
                return 'Not enough players in team'
    else:
        return "Lobby is full. "

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
                return m.LOBBY_IS_FULL
        else:
            teaminsert = sessions_col.update_one(session, {'$addToSet': {'TEAMS': query}})
            return m.SESSION_JOINED

def endSession(session):
    exists = session_exist({'OWNER': session['OWNER'], 'AVAILABLE': True})
    if exists:
        sessions_col.update_one(session, {'$set': {'AVAILABLE': False}})
        return m.SESSION_HAS_ENDED
    else:
        return m.SESSION_DOES_NOT_EXIST

def deleteSession(session):
    exists = session_exist({'OWNER': session['OWNER'], 'AVAILABLE': True})
    if exists:
        sessions_col.delete_one({'OWNER': session['OWNER'], 'AVAILABLE': True})
        return m.SESSION_HAS_ENDED
    else:
        return m.SESSION_DOES_NOT_EXIST

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