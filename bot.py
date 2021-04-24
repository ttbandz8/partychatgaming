import db
import time
import classes as data

now = time.asctime()

'''User must have predefined roles of the games they play before creating users
   User input for IGN will be available after User is created and goes to join game events
   User input for TEAM will be available after User is created. There will be a command to add Team. '''
u = [
    {"DISNAME": "johnd123", "GAMES": ["CODM"]},
    {"DISNAME": "bricks", "GAMES": ["CODM"]}
]

new_user = {"DISNAME": "rocbambino"}

q =  {"DISNAME": "bricks", "GAMES": ["CODM"]}

team = {'TNAME': 'TEAM111111', 'MEMBERS': ['bricks']}

t = {'TNAME': 'TEAM1'}

user = 'bricks'

# new_value = {'$addToSet': {'MEMBERS': 'johnd123'}}

# db.createTeam(team, user)

# db.deleteTeam(t, user)

# db.addTeamMember(t, new_value, user)

# n =[x for x in new_value.values()][0]['MEMBERS']

# print(n)

# db.queryUser(q)

# db.queryTeam(t)

# db.createTeam(data.newTeam(team), user)

# db.createUsers(data.newUser(new_user))

session_team_test =  [
    {'TEAM1': ['PLAYER1', 'PLAYER2', 'PLAYER3', 'PLAYER4'], 'SCORE': 0},
    {'TEAM2': ['PLAYER1', 'PLAYER2', 'PLAYER3', 'PLAYER4'], 'SCORE': 0}
]

# s = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': '1V1', 'PLAYERS': ['']}
print(session_team_test[0]['TEAM1'][0])

