# USER DATA
new_user = {"DISNAME": "rocbambino"}
user1 = 'bricks'





# TEAM DATA

team = {'TNAME': 'TEAM111111', 'MEMBERS': ['bricks']}

t = {'TNAME': 'TEAM1'}





# SESSION DATA

# Query Session
session_query = {'OWNER': 'bricks'}
session_add_member = ['john', 'will', 'bricks']

# Command idea for joining sessions
# $pcg recruit @player @player

# Non Flagged Data

OneVsOne = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': '1V1', 'TEAMS': [{'TEAM1': ['bricks'], 'SCORE': 0}]}
OneVsOne_query = {'OWNER': 'bricks'}
addOne = {'TEAM2': ['Tim'], 'SCORE': 0}

TwoVsTwo = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': '2V2', 'TEAMS': [{'TEAM1': ['bricks', 'rocbambino'], 'SCORE': 0}, {'TEAM2': ['Tim', 'John'], 'SCORE': 0}]}

ThreeVsThree = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': '3V3', 'TEAMS': [{'TEAM1': ['bricks', 'rocbambino', 'james'], 'SCORE': 0}, {'TEAM2': ['Tim', 'John', 'luke'], 'SCORE': 0}]}

FourVsFour = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': '3V3', 'TEAMS': [{'TEAM1': ['bricks', 'rocbambino', 'james', 'Will'], 'SCORE': 0}, {'TEAM2': ['Tim', 'John', 'luke', 'Charles'], 'SCORE': 0}]}


# Flagged Data (Ranked)
OneVsOneRanked = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': '1V1', 'TEAMS': [{'TEAM1': ['bricks'], 'SCORE': 0}, {'TEAM2': ['Tim'], 'SCORE': 0}], 'RANKED': True}

TwoVsTwoRanked = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': '2V2', 'TEAMS': [{'TEAM1': ['bricks', 'rocbambino'], 'SCORE': 0}, {'TEAM2': ['Tim', 'John'], 'SCORE': 0}], 'RANKED': True}

ThreeVsThreeRanked = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': '3V3', 'TEAMS': [{'TEAM1': ['bricks', 'rocbambino', 'james'], 'SCORE': 0}, {'TEAM2': ['Tim', 'John', 'luke'], 'SCORE': 0}], 'RANKED': True}

# Flagged Data (GOC)
OneVsOneGoc = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': '1V1', 'TEAMS': [{'TEAM1': ['bricks'], 'SCORE': 0}, {'TEAM2': ['Tim'], 'SCORE': 0}], 'RANKED': True, 'GOC': True}

TwoVsTwoGoc = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': '2V2', 'TEAMS': [{'TEAM1': ['bricks', 'rocbambino'], 'SCORE': 0}, {'TEAM2': ['Tim', 'John'], 'SCORE': 0}], 'RANKED': True, 'GOC': True}

ThreeVsThreeGoc = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': '3V3', 'TEAMS': [{'TEAM1': ['bricks', 'rocbambino', 'james'], 'SCORE': 0}, {'TEAM2': ['Tim', 'John', 'luke'], 'SCORE': 0}], 'RANKED': True, 'GOC': True}


# Flagged Data (Available False)
OneVsOneAvailFalse = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': '1V1', 'TEAMS': [{'TEAM1': ['bricks'], 'SCORE': 0}, {'TEAM2': ['Tim'], 'SCORE': 0}], 'RANKED': True, 'GOC': True, 'AVAILABLE': False}

TwoVsTwoAvailFalse = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': '2V2', 'TEAMS': [{'TEAM1': ['bricks', 'rocbambino'], 'SCORE': 0}, {'TEAM2': ['Tim', 'John'], 'SCORE': 0}], 'RANKED': True, 'GOC': True, 'AVAILABLE': False}

ThreeVsThreeAvailFalse = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': '3V3', 'TEAMS': [{'TEAM1': ['bricks', 'rocbambino', 'james'], 'SCORE': 0}, {'TEAM2': ['Tim', 'John', 'luke'], 'SCORE': 0}], 'RANKED': True, 'GOC': True, 'AVAILABLE': False}

# Flagged Data (Winner)
OneVsOneWinner = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': '1V1', 'TEAMS': [{'TEAM1': ['bricks'], 'SCORE': 0}, {'TEAM2': ['Tim'], 'SCORE': 0}], 'RANKED': True, 'GOC': True, 'AVAILABLE': False, 'WINNER': {'TEAM1' : ['bricks']}}

TwoVsTwoWinner = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': '2V2', 'TEAMS': [{'TEAM1': ['bricks', 'rocbambino'], 'SCORE': 0}, {'TEAM2': ['Tim', 'John'], 'SCORE': 0}], 'RANKED': True, 'GOC': True, 'AVAILABLE': False, 'WINNER': {'TEAM1': ['bricks', 'rocbambino']}}
