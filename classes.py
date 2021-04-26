from dataclasses import dataclass, asdict, field
import time 

now = time.asctime()

@dataclass(frozen=True, order=True)
class USER():
    DISNAME: str
    AVATAR: list[str] = field(default_factory=lambda: [''])
    IGN: list[str] = field(default_factory=lambda: [{'DEFAULT': 'PCG'}])
    GAMES: list[str] = field(default_factory=lambda: ['PCG'])
    TEAMS: list[str] = field(default_factory=lambda: ['PCG'])
    TITLES: list[str] = field(default_factory=lambda: ['PCG'])
    RWINS: list = field(default_factory=lambda: [{'1V1': 0}, {'2V2': 0}, {'3V3': 0}, {'4V4': 0}, {'5V5': 0}])
    RLOSSES: list = field(default_factory=lambda: [{'1V1': 0}, {'2V2': 0}, {'3V3': 0}, {'4V4': 0}, {'5V5': 0}])
    URWINS: list = field(default_factory=lambda: [{'1V1': 0}, {'2V2': 0}, {'3V3': 0}, {'4V4': 0}, {'5V5': 0}])
    URLOSSES: list = field(default_factory=lambda: [{'1V1': 0}, {'2V2': 0}, {'3V3': 0}, {'4V4': 0}, {'5V5': 0}])
    TOURNAMENT_WINS: int = field(default_factory=lambda: 0)
    TIMESTAMP: str = now

@dataclass(frozen=True, order=True)
class TEAMS():
    OWNER: str
    TNAME: str
    MEMBERS: list
    TOURNAMENT_WINS: int = field(default_factory=lambda: 0)
    RWINS: list = field(default_factory=lambda: [{'1V1': 0}, {'2V2': 0}, {'3V3': 0}, {'4V4': 0}, {'5V5': 0}])
    RLOSSES: list = field(default_factory=lambda: [{'1V1': 0}, {'2V2': 0}, {'3V3': 0}, {'4V4': 0}, {'5V5': 0}])
    URWINS: list = field(default_factory=lambda: [{'1V1': 0}, {'2V2': 0}, {'3V3': 0}, {'4V4': 0}, {'5V5': 0}])
    URLOSSES: list = field(default_factory=lambda: [{'1V1': 0}, {'2V2': 0}, {'3V3': 0}, {'4V4': 0}, {'5V5': 0}])
    GAMES: list[str] = field(default_factory=lambda: ['PCG'])
    BADGES: list[str] = field(default_factory=lambda: ['PCG'])
    TIMESTAMP: str = now

@dataclass(frozen=True, order=True)
class SESSIONS():
    OWNER: str
    GAME: str
    TYPE: int
    TEAMS: list[str] = field(default_factory=lambda: [])
    # PLAYERS: list[str] = field(default_factory=lambda: [])
    # TEAM_SESSION: bool = field(default_factory=lambda: False)
    RANKED: bool = field(default_factory=lambda: False)
    GOC: bool = field(default_factory=lambda: False)
    KINGSGAMBIT: str = field(default_factory=lambda: False)
    AVAILABLE: bool = field(default_factory=lambda: True)
    MATCHES: list[str] = field(default_factory=lambda: [])
    WINNER: str = field(default_factory=lambda: 'N/A')
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
    GAME: str
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

def newSession(session):
    s = SESSIONS(**session)
    return asdict(s)



