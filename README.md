# partychatgaming

# Classes 
    Whenever you see data.something() we are using the data classes to pass default values
    db.createTeam(data.newTeam(team), user)
    db.createUsers(data.newUser(new_user))

# Add New User
    db.addUsers(data.newUser(USER))

# Delete User
    db.deleteUser(DATA)

## Example
    USER = {"DISNAME": "Foo"}
    PUSH = { "$push": {"IGN": {'BRAWLSTARS': 'Bar'}}}
    ADDTOSET = {"$addToSet": {"TEAMS": 'Foo'}}
    db.updateUser(USER, ADDTOSET)
    db.updateUser(USER, PUSH)


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


# How To Make Updates
    $addToInsert = Pushes to array only if doesn't exist
    $push = Pushes to array