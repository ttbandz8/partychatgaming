# USER DATA
new_user = {"DISNAME": "rocbambino"}
user1 = 'bricks'





# TEAM DATA

team = {'TNAME': 'TEAM11111', 'MEMBERS': ['bricks']}

t = {'TNAME': 'TEAM'}





# SESSION DATA

# Query Session
session_query = {'OWNER': 'bricks'}
joining_sessions = ['johnd123']

# Non Flagged Data
OneVsOne = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': 1, 'TEAMS': [{'TEAM': ['bricks'], 'SCORE': 0, 'POSITION': 0}]}
OneVsOne_query = {'OWNER': 'bricks'}
addOne = {'TEAM': ['Tim'], 'SCORE': 0}

TwoVsTwo = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': 2, 'TEAMS': [{'TEAM': ['bricks', 'rocbambino'], 'SCORE': 0, 'POSITION': 0}]}

ThreeVsThree = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': 3, 'TEAMS': [{'TEAM': ['bricks', 'rocbambino', 'james'], 'SCORE': 0}, {'TEAM': ['Tim', 'John', 'luke'], 'SCORE': 0}]}

FourVsFour = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': 4, 'TEAMS': [{'TEAM': ['bricks', 'rocbambino', 'james', 'Will'], 'SCORE': 0}, {'TEAM': ['Tim', 'John', 'luke', 'Charles'], 'SCORE': 0}]}

# Flagged Data (Ranked)
OneVsOneRanked = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': 1, 'TEAMS': [{'TEAM': ['bricks'], 'SCORE': 0}, {'TEAM': ['Tim'], 'SCORE': 0}], 'RANKED': True}

TwoVsTwoRanked = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': 2, 'TEAMS': [{'TEAM': ['bricks', 'rocbambino'], 'SCORE': 0}, {'TEAM': ['Tim', 'John'], 'SCORE': 0}], 'RANKED': True}

ThreeVsThreeRanked = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': 3, 'TEAMS': [{'TEAM': ['bricks', 'rocbambino', 'james'], 'SCORE': 0}, {'TEAM': ['Tim', 'John', 'luke'], 'SCORE': 0}], 'RANKED': True}

# Flagged Data (GOC)
OneVsOneGoc = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': '1V1', 1: [{'TEAM': ['bricks'], 'SCORE': 0}, {'TEAM': ['Tim'], 'SCORE': 0}], 'RANKED': True, 'GOC': True}

TwoVsTwoGoc = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': '2V2', 2: [{'TEAM': ['bricks', 'rocbambino'], 'SCORE': 0}, {'TEAM': ['Tim', 'John'], 'SCORE': 0}], 'RANKED': True, 'GOC': True}

ThreeVsThreeGoc = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': '3V3', 3: [{'TEAM': ['bricks', 'rocbambino', 'james'], 'SCORE': 0}, {'TEAM': ['Tim', 'John', 'luke'], 'SCORE': 0}], 'RANKED': True, 'GOC': True}


# Flagged Data (Available False)
OneVsOneAvailFalse = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': '1V1', 1: [{'TEAM': ['bricks'], 'SCORE': 0}, {'TEAM': ['Tim'], 'SCORE': 0}], 'RANKED': True, 'GOC': True, 'AVAILABLE': False}

TwoVsTwoAvailFalse = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': '2V2', 2: [{'TEAM': ['bricks', 'rocbambino'], 'SCORE': 0}, {'TEAM': ['Tim', 'John'], 'SCORE': 0}], 'RANKED': True, 'GOC': True, 'AVAILABLE': False}

ThreeVsThreeAvailFalse = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': '3V3', 3: [{'TEAM': ['bricks', 'rocbambino', 'james'], 'SCORE': 0}, {'TEAM': ['Tim', 'John', 'luke'], 'SCORE': 0}], 'RANKED': True, 'GOC': True, 'AVAILABLE': False}

# Flagged Data (Winner)
OneVsOneWinner = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': 1, 'TEAMS': [{'TEAM': ['bricks'], 'SCORE': 0}, {'TEAM': ['Tim'], 'SCORE': 0}], 'RANKED': True, 'GOC': True, 'AVAILABLE': False, 'WINNER': {'TEAM' : ['bricks']}}

TwoVsTwoWinner = {'OWNER': 'bricks', 'GAME': 'CODM', 'TYPE': 2, 'TEAMS': [{'TEAM': ['bricks', 'rocbambino'], 'SCORE': 0}, {'TEAM': ['Tim', 'John'], 'SCORE': 0}], 'RANKED': True, 'GOC': True, 'AVAILABLE': False, 'WINNER': {'TEAM': ['bricks', 'rocbambino']}}
