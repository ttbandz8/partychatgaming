from dataclasses import dataclass, asdict, field
import time 

now = time.asctime()

@dataclass(frozen=True, order=True)
class USER():
    DISNAME: str
    IGN: list[str] = field(default_factory=lambda: [{'DEFAULT': 'PCG'}])
    GAMES: list[str] = field(default_factory=lambda: ['PCG'])
    TEAMS: list[str] = field(default_factory=lambda: ['PCG'])
    WINS: int = field(default_factory=lambda: 0)
    LOSSES: int = field(default_factory=lambda: 0)
    TOURNAMENT_WINS: int = field(default_factory=lambda: 0)
    TIMESTAMP: str = now

@dataclass(frozen=True, order=True)
class TEAMS():
    TNAME: str
    MEMBERS: list
    TOURNAMENT_WINS: int = field(default_factory=lambda: 0)
    WINS: int = field(default_factory=lambda: 0)
    LOSSES: int = field(default_factory=lambda: 0) 
    GAMES: list[str] = field(default_factory=lambda: ['PCG'])
    BADGES: list[str] = field(default_factory=lambda: ['PCG'])
    TIMESTAMP: str = now

@dataclass(frozen=True, order=True)
class SESSIONS():
    OWNER: str
    TITLE: str
    TYPE: str
    PLAYERS: list
    MATCHES: list
    TEAMS: list
    TEAM_SESSION: bool = field(default_factory=lambda: False)
    AVAILABLE: bool = field(default_factory=lambda: True)
    TIMESTAMP: str = now

@dataclass(frozen=True, order=True)
class MATCHES():
    USER: str
    MATCHES: list
    TIMESTAMP: str = now

@dataclass(frozen=True, order=True)
class TOURNAMENTS():
    OWNER: str
    PLAYERS: list
    TEAMS: list
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
    user_list = []
    if isinstance(users, list):
        for user in users:
            u = USER(**user)
            user_list.append(asdict(u))
    else:
        u = USER(**users)
        return asdict(u)
    return user_list

def newTeam(team):
    t = TEAMS(**team)
    return asdict(t)



