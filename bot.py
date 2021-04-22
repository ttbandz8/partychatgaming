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

team = {'TNAME': 'TEAM1', 'MEMBERS': ['bricks']}

d_team = {'TNAME': 'TEAM1'}
# db.addTeam(team)
user = 'bricks'

# new_user = {'$addToSet': {'MEMBERS': 'Rocbambino'}}

# query = {'TNAME': 'TEAM1'}

new_user = {'$pull': {'MEMBERS': 'Rocbambino'}}

query = {'TNAME': 'TEAM1'}


db.deleteTeamMember(query, new_user, user)
# db.updateTeam(query, new_user, user)

# db.deleteTeam(d_team, user)