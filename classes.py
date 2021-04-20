from dataclasses import dataclass, asdict, field
import time 

now = time.asctime()

@dataclass(frozen=True, order=True)
class USER():
    DISNAME: str
    IGN: list
    GAMES: list[str]
    TEAMS: list[str] = field(default_factory=lambda: ['PARTYCHATGAMING'])
    TIMESTAMP: str = now

@dataclass(frozen=True, order=True)
class TEAMS():
    NAME: str
    MEMBERS: list
    GAME: str
    TIMESTAMP: str = now

@dataclass(frozen=True, order=True)
class SESSIONS():
    ADMIN: str
    TITLE: str
    TEAMS: list
    USERS: list
    MATCHES: list
    TIMESTAMP: str = now

@dataclass(frozen=True, order=True)
class MATCHES():
    USER: str
    MATCHES: list
    TIMESTAMP: str = now

@dataclass(frozen=True, order=True)
class TOURNAMENTS():
    ADMIN: str
    USERS: list
    TITLE: str
    MATCHES: list
    TIMESTAMP: str = now

@dataclass(frozen=True, order=True)
class SCORES():
    TOTAL: int
    MATCHES: list
    TIMESTAMP: str = now



''' Data Functions'''
def newUser(users):
    userList = []
    if isinstance(users, list):
        for user in users:
            u = USER(user['DISNAME'], user['IGN'], user['GAMES'])
            userList.append(asdict(u))
    else:
        u = USER(users['DISNAME'], users['IGN'], users['GAMES'])
        return asdict(u)
    return userList



