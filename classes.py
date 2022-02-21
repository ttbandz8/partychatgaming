from dataclasses import dataclass, asdict, field
from logging import captureWarnings
import time

now = time.asctime()


@dataclass(frozen=True, order=True)
class USER():
    DISNAME: str
    NAME: str
    DID: str
    AVATAR: list[str] = field(default_factory=lambda: [''])
    IGN: list[str] = field(default_factory=lambda: [{'DEFAULT': 'PCG'}])
    GAMES: list[str] = field(default_factory=lambda: ['Crown Unlimited'])
    GUILD: str = field(default_factory=lambda: 'PCG')
    TEAM: str = field(default_factory=lambda: 'PCG')
    FAMILY: str = field(default_factory=lambda: 'PCG')
    TITLE: str = field(default_factory=lambda: 'Starter')
    CARD: str = field(default_factory=lambda: "Ochaco Uraraka")
    DECK: list[str] = field(default_factory=lambda: [''])
    ARM: str = field(default_factory=lambda: "Stock")
    PET: str = field(default_factory=lambda: "Chick")
    MATCHES: list = field(default_factory=lambda: [{'1V1': [0, 0]}, {'2V2': [0, 0]}, {'3V3': [0, 0]}, {'4V4': [0, 0]}, {'5V5': [0, 0]}])
    TOURNAMENT_WINS: int = field(default_factory=lambda: 0)
    AVAILABLE: bool = field(default_factory=lambda: True)
    CROWN_TALES: list[str] = field(default_factory=lambda: [""])
    DUNGEONS: list[str] = field(default_factory=lambda: [""])
    BOSS_WINS: list[str] = field(default_factory=lambda: [""])
    REFERRED: bool = field(default_factory=lambda: False)
    REFERRER: str = field(default_factory=lambda: "N/A")
    TIMESTAMP: str = now
    IS_ADMIN: bool = field(default_factory=lambda: False)
    RIFT: int = field(default_factory=lambda: 0)
    REBIRTH: int = field(default_factory=lambda: 0)
    PATRON: bool = field(default_factory=lambda: False)
    LEVEL: int = field(default_factory=lambda: 0)
    EXPLORE: bool = field(default_factory=lambda: True)
    SAVE_SPOT: list[str] = field(default_factory=lambda: [])
    PERFORMANCE: bool = field(default_factory=lambda: False)
    TRADING: bool = field(default_factory=lambda: False)
    BOSS_FOUGHT: bool = field(default_factory=lambda: False)
    SERVER: str = field(default_factory=lambda: "N/A")

@dataclass(frozen=True, order=True)
class TRADE():
    MERCHANT: str = field(default_factory=lambda: '')
    MCOIN: int = field(default_factory=lambda: 0)
    MCARDS: list[str] = field(default_factory=lambda: [])
    MTITLES: list[str] = field(default_factory=lambda: [])
    MARMS: list[str] = field(default_factory=lambda: [])
    MSUMMONS: list[str] = field(default_factory=lambda: [])
    BUYER: str = field(default_factory=lambda: '')
    BCOIN: int = field(default_factory=lambda: 0)
    BCARDS: list[str] = field(default_factory=lambda: [])
    BTITLES: list[str] = field(default_factory=lambda: [])
    BARMS: list[str] = field(default_factory=lambda: [])
    BSUMMONS: list[str] = field(default_factory=lambda: [])
    TAX: int = field(default_factory=lambda: 0)
    OPEN: bool = field(default_factory=lambda:True)
    TIMESTAMP: str = now


@dataclass(frozen=True, order=True)
class SERVER():
    GNAME: str = field(default_factory=lambda: '')
    EXP_CHANNEL: str = field(default_factory=lambda: '')
    SERVER_BUFF_BOOL: bool = field(default_factory=lambda:False)
    SERVER_BUFF: list[str] = field(default_factory=lambda: [])
    SERVER_VIRUS_BOOL: bool = field(default_factory=lambda:False)
    SERVER_VIRUS: list[str] = field(default_factory=lambda: [])
    SERVER_PLAYERS: list[str] = field(default_factory=lambda: [])
    SERVER_TEAMS: list[str] = field(default_factory=lambda: [])
    SPECIAL_SERVER_CARDS: list[str] = field(default_factory=lambda: [])
    SPECIAL_SERVER_SUMMONS: list[str] = field(default_factory=lambda: [])
    SERVER_BALANCE: int = field(default_factory=lambda: 0)
    TIMESTAMP: str = now
        

@dataclass(frozen=True, order=True)
class GUILD():
    GNAME: str = field(default_factory=lambda: '')
    FOUNDER: str = field(default_factory=lambda: '')
    SWORN: str = field(default_factory=lambda: '')
    SHIELD: str = field(default_factory=lambda: '')
    SWORDS: list[str] = field(default_factory=lambda: [])
    STREAK: int = field(default_factory=lambda: 0)
    BANK: int = field(default_factory=lambda: 0)
    BOUNTY: int = field(default_factory=lambda: 500000)
    CREST: list[str] = field(default_factory=lambda: ['Unbound'])
    HALL: str = field(default_factory=lambda: 'Mine')
    TIMESTAMP: str = now


@dataclass(frozen=True, order=True)
class TEAMS():
    OWNER: str
    MEMBERS: list
    TEAM_NAME: str
    TEAM_DISPLAY_NAME:  str = field(default_factory=lambda: '')
    OFFICERS: list[str] = field(default_factory=lambda: []) 
    CAPTAINS: list[str] = field(default_factory=lambda: [])
    TRANSACTIONS: list[str] = field(default_factory=lambda: [])
    STORAGE: list[str] = field(default_factory=lambda: [])
    GUILD_BUFF_AVAILABLE: bool = field(default_factory=lambda: False)
    GUILD_BUFF_ON: bool = field(default_factory=lambda: False)
    GUILD_BUFF: list[str] = field(default_factory=lambda: []) 
    GUILD: str = field(default_factory=lambda: 'PCG')
    TOURNAMENT_WINS: int = field(default_factory=lambda: 0)
    BANK: int = field(default_factory=lambda: 0)
    WINS: int = field(default_factory=lambda: 0)
    LOSSES: int = field(default_factory=lambda: 0)
    LOGO_URL: str = field(default_factory=lambda: '')
    LOGO_FLAG: bool = field(default_factory=lambda: False)
    BADGES: list[str] = field(default_factory=lambda: ['New Team'])
    GUILD_MISSION: list[str] = field(default_factory=lambda: [])
    COMPLETED_MISSIONS: int = field(default_factory=lambda: 0)
    MEMBER_COUNT: int = field(default_factory=lambda: 1)
    TIMESTAMP: str = now


@dataclass(frozen=True, order=True)
class ARENA():
    OWNER: str = field(default_factory=lambda: '')
    ACTIVE: bool = field(default_factory=lambda: False)
    READY: bool = field(default_factory=lambda: False)
    SUBBED_PLAYER: bool = field(default_factory=lambda: False)
    GUILD_WAR: bool = field(default_factory=lambda: False)
    SINGLES: bool = field(default_factory=lambda: False)
    IS_FULL: bool = field(default_factory=lambda: False)
    WINNER: str = field(default_factory=lambda: '')
    LOSER: str = field(default_factory=lambda: '')
    GUILD1: str = field(default_factory=lambda: '')
    GUILD2: str = field(default_factory=lambda: '')
    GUILD1_MEMBERS: list[str] = field(default_factory=lambda: [])
    GUILD2_MEMBERS: list[str] = field(default_factory=lambda: [])
    TIMESTAMP: str = now


@dataclass(frozen=True, order=True)
class FAMILY():
    HEAD: str = field(default_factory=lambda: '')
    PARTNER: str = field(default_factory=lambda: '')
    KIDS: list[str] = field(default_factory=lambda: [])
    BANK: int = field(default_factory=lambda: 0)
    HOUSE: str = field(default_factory=lambda: 'Cave')
    TIMESTAMP: str = now


@dataclass(frozen=True, order=True)
class HOUSE():
    PATH: str
    HOUSE: str
    PRICE: int = field(default_factory=lambda: 0)
    TIMESTAMP: str = now
    MULT: float = field(default_factory=lambda: 1.0)
    AVAILABLE: bool = field(default_factory=lambda: False)


@dataclass(frozen=True, order=True)
class HALL():
    PATH: str
    HALL: str
    PRICE: int = field(default_factory=lambda: 0)
    MULT: float = field(default_factory=lambda: 1.0)
    SPLIT: float = field(default_factory=lambda: 1.0)
    DEFENSE: float = field(default_factory=lambda: 1.0)
    FEE: int = field(default_factory=lambda: 100000)
    AVAILABLE: bool = field(default_factory=lambda: False)
    TIMESTAMP: str = now


@dataclass(frozen=True, order=True)
class SESSIONS():
    OWNER: str
    GAME: str
    TYPE: int
    TEAMS: list[str] = field(default_factory=lambda: [])
    GODS: bool = field(default_factory=lambda: False)
    GODS_TITLE: str = field(default_factory=lambda: 'N/A')
    TOURNAMENT: str = field(default_factory=lambda: False)
    SCRIM: bool = field(default_factory=lambda: False)
    KINGSGAMBIT: str = field(default_factory=lambda: False)
    AVAILABLE: bool = field(default_factory=lambda: True)
    IS_FULL: bool = field(default_factory=lambda: False)
    WINNING_TEAM: str = field(default_factory=lambda: 'N/A')
    LOSING_TEAM: str = field(default_factory=lambda: 'N/A')
    WINNER: str = field(default_factory=lambda: 'N/A')
    LOSER: str = field(default_factory=lambda: 'N/A')
    CROWN_UNLIMITED: bool = field(default_factory=lambda: False)
    TIMESTAMP: str = now


@dataclass(frozen=True, order=True)
class MATCHES():
    PLAYER: str
    CARD: str = field(default_factory=lambda: 'N/A')
    PATH: str = field(default_factory=lambda: 'N/A')
    TITLE: str = field(default_factory=lambda: 'N/A')
    ARM: str = field(default_factory=lambda: 'N/A')
    UNIVERSE: str = field(default_factory=lambda: "Unbound")
    UNIVERSE_TYPE: str = field(default_factory=lambda: "Unbound")
    EXCLUSIVE: bool = field(default_factory=lambda: False)
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
    FPATH: str = field(default_factory=lambda: "N/A")
    PRICE: int = field(default_factory=lambda: 0)
    TOURNAMENT_REQUIREMENTS: int = field(default_factory=lambda: 0)
    TIMESTAMP: str = now
    MOVESET: list[str] = field(
        default_factory=lambda: [{'MOVE1': 20, "STAM": 10}, {'MOVE2': 50, "STAM": 30}, {'ULTIMATE': 100, "STAM": 80},
                                 {'ENHANCER': 0, "STAM": 20, "TYPE": "TYPE"}])
    RPATH: str = field(default_factory=lambda: "N/A")
    RNAME: str = field(default_factory=lambda: "N/A")
    GIF: str = field(default_factory=lambda: "N/A")
    HLT: int = field(default_factory=lambda: 500)
    STAM: int = field(default_factory=lambda: 100)
    ATK: int = field(default_factory=lambda: 25)
    DEF: int = field(default_factory=lambda: 25)
    TYPE: int = field(default_factory=lambda: 0)
    TIER: float = field(default_factory=lambda: 1)
    PASS: list[str] = field(default_factory=lambda: [{'NAME': 0, 'TYPE': 'TYPE'}])
    SPD: float = field(default_factory=lambda: 1)
    VUL: bool = field(default_factory=lambda: False)
    UNIVERSE: str = field(default_factory=lambda: "Unbound")
    COLLECTION: str = field(default_factory=lambda: "N/A")
    HAS_COLLECTION: bool = field(default_factory=lambda: False)
    STOCK: int = field(default_factory=lambda: 5)
    AVAILABLE: bool = field(default_factory=lambda: False)
    BASEATK: int = field(default_factory=lambda: 25)
    BASEDEF: int = field(default_factory=lambda: 25)
    DESCRIPTIONS: list[str] = field(default_factory=lambda: [])
    EXCLUSIVE: bool = field(default_factory=lambda: False)
    IS_SKIN: bool = field(default_factory=lambda: False)
    SKIN_FOR: str = field(default_factory=lambda: "N/A")
    

@dataclass(frozen=True, order=True)
class TITLES():
    TITLE: str
    PRICE: int = field(default_factory=lambda: 0)
    TOURNAMENT_REQUIREMENTS: int = field(default_factory=lambda: 0)
    ABILITIES: list[str] = field(default_factory=lambda: [{'TYPE': 0}])
    UNIVERSE: str = field(default_factory=lambda: "Unbound")
    COLLECTION: str = field(default_factory=lambda: "N/A")
    TIMESTAMP: str = now
    STOCK: int = field(default_factory=lambda: 5)
    AVAILABLE: bool = field(default_factory=lambda: False)
    EXCLUSIVE: bool = field(default_factory=lambda: False)


@dataclass(frozen=True, order=True)
class ARM():
    ARM: str
    PRICE: int = field(default_factory=lambda: 0)
    TOURNAMENT_REQUIREMENTS: int = field(default_factory=lambda: 0)
    ABILITIES: list[str] = field(default_factory=lambda: [{'TYPE': 0}])
    UNIVERSE: str = field(default_factory=lambda: "Unbound")
    COLLECTION: str = field(default_factory=lambda: "N/A")
    TIMESTAMP: str = now
    STOCK: int = field(default_factory=lambda: 5)
    AVAILABLE: bool = field(default_factory=lambda: False)
    EXCLUSIVE: bool = field(default_factory=lambda: False)


@dataclass(frozen=True, order=True)
class PET():
    PET: str
    PATH: str = field(default_factory=lambda: '')
    UNIVERSE: str = field(default_factory=lambda: "Unbound")
    LVL: int = field(default_factory=lambda: 0)
    EXP: float = field(default_factory=lambda: 0)
    ABILITIES: list[str] = field(default_factory=lambda: [{'MOVE': 0, 'TYPE': 'Enhancer'}])
    COLLECTION: str = field(default_factory=lambda: "N/A")
    TIMESTAMP: str = now
    AVAILABLE: bool = field(default_factory=lambda: True)
    EXCLUSIVE: bool = field(default_factory=lambda: False)


@dataclass(frozen=True, order=True)
class UNIVERSE():
    TITLE: str
    PATH: str = field(default_factory=lambda: '')
    CROWN_TALES: list[str] = field(default_factory=lambda: [''])
    DUNGEONS: list[str] = field(default_factory=lambda: [''])
    HAS_DUNGEON: bool = field(default_factory=lambda: False)
    PREREQUISITE: str = field(default_factory=lambda: "Deathnote")
    UNIVERSE_BOSS: str = field(default_factory=lambda: "")
    HAS_CROWN_TALES: bool = field(default_factory=lambda: False)
    TIMESTAMP: str = now
    AVAILABLE: bool = field(default_factory=lambda: True)
    UTITLE: str = field(default_factory=lambda: "Starter")
    UARM: str = field(default_factory=lambda: "Stock")
    DTITLE: str = field(default_factory=lambda: "Starter")
    DARM: str = field(default_factory=lambda: "Stock")
    UPET: str = field(default_factory=lambda: "")
    DPET: str = field(default_factory=lambda: "")
    TIER: int = field(default_factory=lambda: 0)
    GUILD: str = field(default_factory=lambda: "PCG")


@dataclass(frozen=True, order=True)
class BOSS():
    NAME: str = field(default_factory=lambda: '')
    PATH: str = field(default_factory=lambda: '')
    TITLE: str = field(default_factory=lambda: '')
    ARM: str = field(default_factory=lambda: '')
    PET: str = field(default_factory=lambda: '')
    UNIVERSE: str = field(default_factory=lambda: "Unbound")
    CARD: str = field(default_factory=lambda: '')
    TIMESTAMP: str = now
    DESCRIPTION: list[str] = field(default_factory=lambda: '')
    AVAILABLE: bool = field(default_factory=lambda: True)
    PET: list[str] = field(default_factory=lambda: [
        {'NAME': 'Chick', 'LVL': 1, 'EXP': 0, 'Glare': 5, 'TYPE': 'HLT', 'BOND': 0,
         'PATH': "https://res.cloudinary.com/dkcmq8o15/image/upload/v1622307902/Pets/chick.jpg"}])


@dataclass(frozen=True, order=True)
class SCORES():
    TOTAL: int
    MATCHES: list
    TIMESTAMP: str = now


@dataclass(frozen=True, order=True)
class GAMES():
    GAME: str
    IMAGE_URL: str = field(default_factory=lambda: "")
    TYPE: list[int] = field(default_factory=lambda: [])
    IGN: bool = field(default_factory=lambda: False)
    ALIASES: list[str] = field(default_factory=lambda: [])
    TIMESTAMP: str = now


@dataclass(frozen=True, order=True)
class GODS():
    PLAYER: str
    DID: str
    CARD: str
    TITLE: int
    ARM: str
    TIMESTAMP: str = now


@dataclass(frozen=True, order=True)
class VAULT():
    OWNER: str
    DID: str
    BALANCE: int = field(default_factory=lambda: 500000)
    CARDS: list[str] = field(default_factory=lambda: ['Ochaco Uraraka', 'Eevee', 'Garen'])
    TITLES: list[str] = field(default_factory=lambda: ['Starter', 'Iron 4', 'UA 1st Year', 'Pokemon Trainer'])
    ARMS: list[str] = field(default_factory=lambda: [{'ARM':'Stock', 'DUR': 999999}, {'ARM': 'Poke Ball', 'DUR': 50}, {'ARM': 'Hyper-Density Seals', 'DUR': 50}, {'ARM': 'Dorans Shield', 'DUR': 50}])
    PETS: list[str] = field(default_factory=lambda: [
        {'NAME': 'Chick', 'LVL': 1, 'EXP': 0, 'Heal': 5, 'TYPE': 'HLT', 'BOND': 0, 'BONDEXP': 0,
         'PATH': "https://res.cloudinary.com/dkcmq8o15/image/upload/v1638814575/Pets/CHICK.png"}])
    DECK: list[str] = field(
        default_factory=lambda: [{'CARD': 'Eevee', 'TITLE': 'Pokemon Trainer', 'ARM': 'Poke Ball', 'PET': 'Chick'},
                                 {'CARD': 'Ochaco Uraraka', 'TITLE': 'UA 1st Year', 'ARM': 'Hyper-Density Seals',
                                  'PET': 'Chick'},
                                 {'CARD': 'Garen', 'TITLE': 'Iron 4', 'ARM': 'Dorans Shield', 'PET': 'Chick'}])
    CARD_LEVELS: list[str] = field(default_factory=lambda: [
        {'CARD': 'Eevee', 'LVL': 0, 'TIER': 1, 'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0},
        {'CARD': 'Ochaco Uraraka', 'LVL': 0, 'TIER': 1, 'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0},
        {'CARD': 'Garen', 'LVL': 0, 'TIER': 1, 'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0}])
    QUESTS: list[str] = field(default_factory=lambda: [])
    DESTINY: list[str] = field(default_factory=lambda: [])
    GEMS: list[str] = field(default_factory=lambda: [])
    STORAGE: list[str] = field(default_factory=lambda: [])


@dataclass(frozen=True, order=True)
class MENU():
    PATH: str
    NAME: str
    TIMESTAMP: str = now


''' Data Functions'''
def newServer(server):
    ser = SERVER(**server)
    return asdict(ser)


def newArena(arena):
    are = ARENA(**arena)
    return asdict(are)


def newCard(card):
    c = CARDS(**card)
    return asdict(c)


def newTitle(title):
    title = TITLES(**title)
    return asdict(title)


def newArm(arm):
    arm = ARM(**arm)
    return asdict(arm)


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


def newFamily(family):
    f = FAMILY(**family)
    return asdict(f)


def newUniverse(universe):
    nu = UNIVERSE(**universe)
    return asdict(nu)


def newBoss(boss):
    nb = BOSS(**boss)
    return asdict(nb)


def newSession(session):
    s = SESSIONS(**session)
    return asdict(s)


def newGame(game):
    g = GAMES(**game)
    return asdict(g)


def newGods(gods):
    god = GODS(**gods)
    return asdict(god)


def newVault(vault):
    v = VAULT(**vault)
    return asdict(v)


def newPet(pet):
    p = PET(**pet)
    return asdict(p)


def newMatch(match):
    m = MATCHES(**match)
    return asdict(m)


def newHouse(house):
    h = HOUSE(**house)
    return asdict(h)


def newGuild(guild):
    gu = GUILD(**guild)
    return asdict(gu)


def newHall(hall):
    ha = HALL(**hall)
    return asdict(ha)

def newTrade(trade):
    tr = TRADE(**trade)
    return asdict(tr)
