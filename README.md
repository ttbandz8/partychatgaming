# partychatgaming

# Classes 
    Whenever you see data.something() we are using the data classes to pass default values
    db.createTeam(data.newTeam(team), user)
    db.createUsers(data.newUser(new_user))

# Add New User
    db.addUsers(data.newUser(USER))

# Delete User
    db.deleteUser(DATA)

## Updating Lists Example
    USER = {"DISNAME": "Foo"}
    PUSH = { "$push": {"IGN": {'BRAWLSTARS': 'Bar'}}}
    ADDTOSET = {"$addToSet": {"TEAMS": 'Foo'}}
    db.updateUser(USER, ADDTOSET)
    db.updateUser(USER, PUSH)

    $addToInsert = Pushes to array only if doesn't exist
    $push = Pushes to array
    $pull = Removes from array (opposite of push)

# Create New Team
    db.addTeam(data.newTeam(TEAM))

# Add Team Member
    db.addTeamMember(QUERY, NEW_VALUE, USER)
    // USER is the user making the request
    // this ensures we check if the USER
    // is part of the team
    [x for x in new_value.values()][0]['MEMBERS']

# Delete Team
    The user is needed to first determine if the user is part of that team, in which he/she can then delete the team.
    db.deleteTeam(TEAM, USER)

# Delete Team Member
    The user is needed to first determine if the user is part of that team, in which he/she can then delete the team.
    db.deleteTeamMember(QUERY, MEMBER_TO_DELETE_QUERY, USER)
    pull = Removes from array (opposite of push)



# Session Logic
    TYPES:
        1V1
            * If flagged, user who wins also counts win toward his team during tourney for tourney points as it could be "Put ya mans up"
            * If TEAM_SESSION flag is True, the win will count toward the winners team
            * [{'PLAYER': 'foo', 'SCORE': 1}, {'PLAYER': 'bar', 'SCORE': 0}]

        2V2
            * If flagged, user who wins also counts win toward his team during tourney for tourney points as it could be "Put ya mans up"
            * If TEAM_SESSION flag is True, the win will count toward the winners team 
            * [{'TEAM1': ['PLAYER1', 'PLAYER2'], 'SCORE': 0}, {'TEAM2': ['PLAYER1', 'PLAYER2'], 'SCORE': 0}]

        3V3
            * If flagged, user who wins also counts win toward his team during tourney for tourney points as it could be "Put ya mans up"
            * If TEAM_SESSION flag is True, the win will count toward the winners team
            * [{'TEAM1': ['PLAYER1', 'PLAYER2', 'PLAYER3'], 'SCORE': 0}, {'TEAM2': ['PLAYER1', 'PLAYER2', 'PLAYER3'], 'SCORE': 0}]

        4V4
            * If flagged, user who wins also counts win toward his team during tourney for tourney points as it could be "Put ya mans up" 
            * If TEAM_SESSION flag is True, the win will count toward the winners team
            * [{'TEAM1': ['PLAYER1', 'PLAYER2', 'PLAYER3', 'PLAYER4'], 'SCORE': 0},{'TEAM2': ['PLAYER1', 'PLAYER2', 'PLAYER3', 'PLAYER4'], 'SCORE': 0}]

        5V5
            * If flagged, user who wins also counts win toward his team during tourney for tourney points as it could be "Put ya mans up" 
            * If TEAM_SESSION flag is True, the win will count toward the winners team
            * [{'TEAM1': ['PLAYER1', 'PLAYER2', 'PLAYER3', 'PLAYER4', 'PLAYER5'], 'SCORE': 0}, {'TEAM2': ['PLAYER1', 'PLAYER2', 'PLAYER3', 'PLAYER4', 'PLAYER5'], 'SCORE': 0}]

        KingsGambit
            * People can join and rotate via winners
            * If flagged, user who wins also counts win toward his team during tourney for tourney points


    

