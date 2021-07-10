import textwrap

# PLAYER_COMMANDS="`.d` - Delete `USER` Account" + "\n\n" + "`.vs` `GAME` @`PLAYER` - How many times you defeated opponent" + "\n\n" + "`.r` - Register `USER` Account\n\n"
# PROFILE_COMMANDS="`.lkg` - Lookup available `GAMES`" + "\n\n" + "`.ag` `GAME` - Add `GAME` to `USER` account" + "\n\n" + "`.uign` `GAME` `IGN` - Update In Game Name for `GAME`"  + "\n\n" + "`.lk` @`player` - Lookup a `PLAYERS` profile" + "\n\n" +  "`.lkt` `TEAM Name` - Lookup `TEAM PROFILE`\n\n"
# SENPAI_COMMANDS="`.senpai` - Learn Basic Of Party Chat Gaming Bot" + "\n\n" + "`.bootcamp` - Learn `LOBBY` commands" + "\n\n" + "`.franchise` - Learn `TEAM` commands" + "\n\n" + "`.legend` - Learn `TOURNAMENT` commands\n\n"
# LOBBY_COMMANDS="`.lobby` - Check if `USER` is hosting a lobby" + "\n\n" + "`.check` - Check if `PLAYER` is in a `LOBBY`" + "\n\n" + "`.createlobby` lobbysize `GAME` - Create `LOBBY` up to size 5" + "\n\n" + "`.end` - End `LOBBY` and Record `SCORE`" + "\n\n" + "`.deletelobby` - Delete `LOBBY`" + "\n\n" + "`.joinlobby`  @`PLAYER`- Join  `PLAYER` `LOBBY`" + "\n\n" + "`.score` @`PLAYER` - Score (`PLAYER` / `TEAM`) in `LOBBY`" + "\n\n" + "`.add` (LOCKED) -  Add `PLAYERS` into `LOBBY`\n\n" 
# SHOP_COMMANDS= "`.shop` - Open Pop Up `SHOP`" + "\n\n" + "`.viewcard` - Preview `CARD` in `SHOP`" + "\n\n" + "`.buycard` - Buy `CARD` from `SHOP`" + "\n\n" + "`.viewtitle` - preview `TITLE` in `SHOP`" + "\n\n" + "`.buytitle` - Buy `TITLE` from `SHOP`" + "\n\n" + "`.viewarm` - preview `ARM` in `SHOP`" + "\n\n" + "`.buyarm` - Buy `ARM` from `SHOP`\n\n" + "\n\n" + "`.viewpet` - preview `PET` in `VAULT`"
# TEAM_COMMANDS="`.createteam` `GAME` `TEAM name` - Create `TEAM`" + "\n\n" +   "`.addteamgame` `GAME` - Add `GAME` to `TEAM`" + "\n\n" + "`.deleteteam` `TEAM` - Delete `TEAM` (`OWNER` Only)" + "\n\n" + "`.addtoteam` @`PLAYER` - Add `PLAYER` to `TEAM` (`OWNER` Only)" + "\n\n" + "`.deletemember` @`PLAYER` - Delete `MEMBER` (`OWNER` Only)" + "\n\n" + "`.apply` @`PLAYER` - Applys for `TEAM` (`PLAYER` must be `OWNER`)" + "\n\n" + "`.leaveteam` `TEAM` - Leave `TEAM`\n\n"
# CROWN_UNLIMITED_PLAYER_COMMANDS="`.vault` - Open `VAULT` *Use :fast_forward:*\n\n`.equipcard` `CARD Name` - Equip new `CARD`\n\n`.equiptitle` - Equip new `TITLE`\n\n`.equiparm` - Equip new `ARM`\n\n`.viewpet` - View `PET` Stats\n\n`.equippet` - Equip new `PET`\n\n`.trade` @`PLAYER` `ITEM` - trade `CARDS`, `TITLES`, `ARMS` or `PETS`\n\n`.sell` @`PLAYER` `ITEM` - sell `CARDS`, `TITLES`, `ARMS` or `PETS`\n\n`.build` - view current Build\n\n`.savedeck` - save current Build\n\n`.viewdeck` - view/load Saved Builds\n\n`.shop` - Open Pop Up `SHOP` *Use :fast_forward:*\n\n"
CROWN_UNLIMITED_GAMES="`.crownhelp` - Crown Unlimited Help Book\n\n`.senpaibattle` - Tutorial Bot\n\n`.legendbattle` -  Advanced Tutorial Bot\n\n`.battle` @`PLAYER` - Challenge another Player\n\n`.start` - To start a battle in your current session\n\n`.wager` `AMOUNT` - Wager amount to battle in current session\n\n`.solo` - Play Crown Unlimited In DMS\n\n`.tales` - Opens Crown Tales Story Mode Menu\n\n`.dungeon` - Opens Crown Tales Dungeon Menu\n\n`.boss` `UNIVERSE` - Opens Crown Universe Boss Fight\n\n`.ctales` @`COMPANION` - Opens Crown Tales CO-OP Story Mode Menu\n\n`.cdungeon` @`COMPANION`- Opens Crown Tales CO-OP Dungeon Menu\n\n`.cboss` @`COMPANION` `UNIVERSE` - Opens Crown Universe CO-OP Boss Fight\n\n`.enhance` - Opens Enhancement Help Menu\n\n"

BOT_COMMANDS = textwrap.dedent(f"""\
**PROFILE COMMANDS**
**.r**: Account Registration
**.d @player**IWANTTODELETEMYACCOUNT: Delete your account
**.lk @player**: Profile lookup

**GAME COMMANDS**
**.vs game @player**: Matchup lookup
**.lkg**: Lookup available Games to add to Profile
**.ag game name**: Add Game to your account
**.uign game ign**: Update In Game Name for a game

**TEAM COMMANDS**
**.lookupteam team name**: Team lookup
**.createteam game team name**: Create team 
**.addteamgame game**: Add game to your team
**.deleteteam**: Delete team
**.addtoteam @player**: Add player to team
**.deletemember @player**: Delete team member
**.apply @player**: Apply for owners team 
**.leaveteam team**: Leave Team

**FAMILY COMMANDS**
**.lookupfamily @user**: Family lookup
**.marry @user**:Create Family with a User
**.divorce @user**: Ask for divorce from user
**.adopt @user**: Adopt user into family
**.runaway**: Runaway from family as child
**.abandon**: Delete Family


**LOBBY COMMANDS**
**.lobby**: Check if you're in a lobby
**.check @player**: Check if player is in a lobby
**.createlobby lobbysize game**: - Create lobby up 5 players
**.deletelobby**: Delete your lobby
**.joinlobby @player**: Join players lobby
**.score @player**: Score player/team in lobby
**.add @player**:  Add player into your lobby
**.end**: End lobby and save score
""")

CROWN_UNLIMITED_COMMANDS = textwrap.dedent(f"""\
**PROFILE COMMANDS**
**.solo**: Play Crown Unlimited In DM
**.crownhelp**: Crown Unlimited Help Book
**.build**: View your current build
**.viewdeck** View your build presets
**.savedeck**: Save your current build as preset
**.shop**: Open shop
**.bal**: View Balance
**.cvault**: Open your list of Cards
**.tvault**: Open your list of Titles
**.avault**: Open your list of Arms
**.pvault**: Open your list of Pets
**.destiny**: Open your list of Destiny Lines
**.quest**: Open your list of Quests
**.deck**: View your Presets
**.savedeck**: Save your Build as Preset

**Card Commands**
**.viewcard**: Preview Card 
**.buycard**: Buy Card
**.equipcard card**: Equip card

**Title Commands**
**.viewtitle**: Preview Title
**.buytitle**: Buy Title
**.equiptitle title**: - Equip title

**Arm Commands**
**.viewarm**: Preview Arm
**.buyarm**: Buy Arm
**.equiparm arm**: Equip arm

**Pet Commands**
**.viewpet** Preview Pet
**.equippet pet**: Equip pet

**Economy Commands**
**.trade @player item**: Trade Cards, Titles, Arms, Pets
**.sell @player item**: Sell Cards, Titles, and Arms
**.resell item**: Sell Card, Title, Arm back to shop
**.gift @player amount**: Gift player money

**Crown Unlimited PVP Mode**
**.senpaibattle**: Tutorial Bot
**.legendbattle**:  Advanced Tutorial Bot
**.battle @player**: Challenge another Player
**.start** Start a battle in your current session
**.wager amount**: Wager amount to battle in current session

**Crown Unlimited Story Mode**
**.tales**: Opens Crown Tales Story Mode Menu
**.dungeon**: Opens Crown Tales Dungeon Menu
**.boss Universe**: Opens Crown Universe Boss Fight
**.ctales @companion**: Opens Crown Tales CO-OP Story Mode Menu
**.cdungeon @companion**: Opens Crown Tales CO-OP Dungeon Menu
**.cboss @companion universe**: Opens Crown Universe CO-OP Boss Fight
""")