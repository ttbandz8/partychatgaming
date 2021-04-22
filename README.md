# partychatgaming

# USER
    DISNAME: str
    IGN: list[str] = field(default_factory=lambda: [{'DEFAULT': 'PARTYCHATGAMING'}])
    GAMES: list[str] = field(default_factory=lambda: ['PARTYCHATGAMING'])
    TEAMS: list[str] = field(default_factory=lambda: ['PARTYCHATGAMING'])
    TIMESTAMP: str = now

# Add New User
    db.addUsers(data.newUser(DATA))

# Delete User
    db.deleteUser(DATA)

## Example
    USER = {"DISNAME": "Foo"}
    PUSH = { "$push": {"IGN": {'BRAWLSTARS': 'Bar'}}}
    ADDTOSET = {"$addToSet": {"TEAMS": 'Foo'}}
    db.updateUser(USER, ADDTOSET)
    db.updateUser(USER, PUSH)


# Add New Team
    db.addTeam(DATA)

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