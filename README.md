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

# How To Make Updates
    $addToInsert = Pushes to array only if doesn't exist
    $push = Pushes to array

## Example
    USER = {"DISNAME": "Foo"}
    PUSH = { "$push": {"IGN": {'BRAWLSTARS': 'Bar'}}}
    ADDTOSET = {"$addToSet": {"TEAMS": 'Foo'}}
    db.updateUser(USER, ADDTOSET)
    db.updateUser(USER, PUSH)
    