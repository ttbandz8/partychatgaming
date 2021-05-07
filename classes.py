from dataclasses import dataclass, asdict, field
import time 

now = time.asctime()

@dataclass(frozen=True, order=True)
class USER():
    DISNAME: str
    NAME: str
    DID: str 
    AVATAR: list[str] = field(default_factory=lambda: [''])
    IGN: list[str] = field(default_factory=lambda: [{'DEFAULT': 'PCG'}])
    GAMES: list[str] = field(default_factory=lambda: ['PCG'])
    TEAM: str = field(default_factory=lambda: 'PCG')
    TITLE: str = field(default_factory=lambda: 'PCG')
    CARD: str = field(default_factory=lambda: "Dark")
    RANKED: list = field(default_factory=lambda: [{'1V1': [0, 0, 0]}, {'2V2': [0, 0, 0]}, {'3V3': [0, 0, 0]}, {'4V4': [0, 0, 0]}, {'5V5': [0, 0, 0]}])
    NORMAL: list = field(default_factory=lambda: [{'1V1': [0, 0, 0]}, {'2V2': [0, 0, 0]}, {'3V3': [0, 0, 0]}, {'4V4': [0, 0, 0]}, {'5V5': [0, 0, 0]}])
    TOURNAMENT_WINS: int = field(default_factory=lambda: 0)
    # TOURNAMENT_LOSSES: int = field(default_factory=lambda: 0)
    AVAILABLE: bool = field(default_factory=lambda: True)
    TIMESTAMP: str = now


@dataclass(frozen=True, order=True)
class TEAMS():
    OWNER: str
    TNAME: str
    MEMBERS: list
    TOURNAMENT_WINS: int = field(default_factory=lambda: 0)
    SCRIM_WINS: int = field(default_factory=lambda: 0)
    SCRIM_LOSSES: int = field(default_factory=lambda: 0)
    GAMES: list[str] = field(default_factory=lambda: ['PCG'])
    LOGO_URL:  str = field(default_factory=lambda: '')
    LOGO_FLAG: bool = field(default_factory=lambda: False)
    BADGES: list[str] = field(default_factory=lambda: ['New Team'])
    TIMESTAMP: str = now

@dataclass(frozen=True, order=True)
class SESSIONS():
    OWNER: str
    GAME: str
    TYPE: int
    TEAMS: list[str] = field(default_factory=lambda: [])
    RANKED: bool = field(default_factory=lambda: False)
    GOC: bool = field(default_factory=lambda: False)
    GOC_TITLE: str = field(default_factory=lambda: 'N/A')
    TOURNAMENT: str = field(default_factory=lambda: False)
    SCRIM: bool = field(default_factory=lambda: False)
    KINGSGAMBIT: str = field(default_factory=lambda: False)
    AVAILABLE: bool = field(default_factory=lambda: True)
    IS_FULL: bool = field(default_factory=lambda: False)
    WINNING_TEAM: str = field(default_factory=lambda: 'N/A')
    LOSING_TEAM: str = field(default_factory=lambda: 'N/A')
    WINNER: str = field(default_factory=lambda: 'N/A')
    LOSER: str = field(default_factory=lambda: 'N/A')
    TIMESTAMP: str = now

@dataclass(frozen=True, order=True)
class MATCHES():
    USER: str
    RANKED: bool = field(default_factory=lambda: False)
    NORMAL: bool = field(default_factory=lambda: True)
    WIN: bool = field(default_factory=lambda: False)
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
class CARDS():
    PATH: str
    NAME: str
    PRICE: int = field(default_factory=lambda: 0)
    TOURNAMENT_REQUIREMENTS: int = field(default_factory=lambda: 0)
    TIMESTAMP: str = now

@dataclass(frozen=True, order=True) 
class TITLES():
    TITLE: str
    PRICE: int = field(default_factory=lambda: 0)
    TOURNAMENT_REQUIREMENTS: int = field(default_factory=lambda: 0)
    TIMESTAMP: str = now

@dataclass(frozen=True, order=True) 
class SCORES():
    TOTAL: int
    MATCHES: list
    TIMESTAMP: str = now

@dataclass(frozen=True, order=True) 
class GAMES():
    GAME: str
    IMAGE_URL: str
    TYPE: list[int] = field(default_factory=lambda: [])
    IGN: bool = field(default_factory=lambda: False)
    ALIASES: list[str] = field(default_factory=lambda: [])
    TIMESTAMP: str = now

@dataclass(frozen=True, order=True) 
class GOC():
    TITLE: str
    TYPE: int
    IMG_URL: str
    REWARD: int
    ARCHIVED: bool = field(default_factory=lambda: False)
    TEAM_FLAG: bool = field(default_factory=lambda: False)
    AVAILABLE: bool = field(default_factory=lambda: False)
    REGISTRATION: bool = field(default_factory=lambda: False)
    PARTICIPANTS: list[str] = field(default_factory=lambda: [])
    WINNER: str = field(default_factory=lambda: '')  
    TIMESTAMP: str = now

@dataclass(frozen=True, order=True)
class VAULT():
    OWNER: str
    BALANCE: int = field(default_factory=lambda: 1000)
    CARDS: list[str] = field(default_factory=lambda: ['Dark'])
    TITLES: list[str] = field(default_factory=lambda: ['Starter'])




''' Data Functions'''
def newCard(card):
    c = CARDS(**card)
    return asdict(c)

def newTitle(title):
    title = TITLES(**title)
    return asdict(title)

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

def newGame(game):
    g = GAMES(**game)
    return asdict(g)

def newMatch(match):
    m = MATCH(**match)
    return asdict(m)

def newGoc(goc):
    godsOfCod = GOC(**goc)
    return asdict(godsOfCod)

def newVault(vault):
    v = VAULT(**vault)
    return asdict(v)

