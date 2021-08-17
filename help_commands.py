import textwrap

# PLAYER_COMMANDS="`/d` - Delete `USER` Account" + "\n\n" + "`/vs` `GAME` @`PLAYER` - How many times you defeated opponent" + "\n\n" + "`/r` - Register `USER` Account\n\n"
# PROFILE_COMMANDS="`/lkg` - Lookup available `GAMES`" + "\n\n" + "`/ag` `GAME` - Add `GAME` to `USER` account" + "\n\n" + "`/uign` `GAME` `IGN` - Update In Game Name for `GAME`"  + "\n\n" + "`/lk` @`player` - Lookup a `PLAYERS` profile" + "\n\n" +  "`/lkt` `TEAM Name` - Lookup `TEAM PROFILE`\n\n"
# SENPAI_COMMANDS="`/senpai` - Learn Basic Of Party Chat Gaming Bot" + "\n\n" + "`/bootcamp` - Learn `LOBBY` commands" + "\n\n" + "`/franchise` - Learn `TEAM` commands" + "\n\n" + "`/legend` - Learn `TOURNAMENT` commands\n\n"
# LOBBY_COMMANDS="`/lobby` - Check if `USER` is hosting a lobby" + "\n\n" + "`/check` - Check if `PLAYER` is in a `LOBBY`" + "\n\n" + "`/createlobby` lobbysize `GAME` - Create `LOBBY` up to size 5" + "\n\n" + "`/end` - End `LOBBY` and Record `SCORE`" + "\n\n" + "`/deletelobby` - Delete `LOBBY`" + "\n\n" + "`/joinlobby`  @`PLAYER`- Join  `PLAYER` `LOBBY`" + "\n\n" + "`/score` @`PLAYER` - Score (`PLAYER` / `TEAM`) in `LOBBY`" + "\n\n" + "`/add` (LOCKED) -  Add `PLAYERS` into `LOBBY`\n\n" 
# SHOP_COMMANDS= "`/shop` - Open Pop Up `SHOP`" + "\n\n" + "`/viewcard` - Preview `CARD` in `SHOP`" + "\n\n" + "`/buycard` - Buy `CARD` from `SHOP`" + "\n\n" + "`/viewtitle` - preview `TITLE` in `SHOP`" + "\n\n" + "`/buytitle` - Buy `TITLE` from `SHOP`" + "\n\n" + "`/viewarm` - preview `ARM` in `SHOP`" + "\n\n" + "`/buyarm` - Buy `ARM` from `SHOP`\n\n" + "\n\n" + "`/viewpet` - preview `PET` in `VAULT`"
# TEAM_COMMANDS="`/createteam` `GAME` `TEAM name` - Create `TEAM`" + "\n\n" +   "`/addteamgame` `GAME` - Add `GAME` to `TEAM`" + "\n\n" + "`/deleteteam` `TEAM` - Delete `TEAM` (`OWNER` Only)" + "\n\n" + "`/addtoteam` @`PLAYER` - Add `PLAYER` to `TEAM` (`OWNER` Only)" + "\n\n" + "`/deletemember` @`PLAYER` - Delete `MEMBER` (`OWNER` Only)" + "\n\n" + "`/apply` @`PLAYER` - Applys for `TEAM` (`PLAYER` must be `OWNER`)" + "\n\n" + "`/leaveteam` `TEAM` - Leave `TEAM`\n\n"
# CROWN_UNLIMITED_PLAYER_COMMANDS="`/vault` - Open `VAULT` *Use :fast_forward:*\n\n`/equipcard` `CARD Name` - Equip new `CARD`\n\n`/equiptitle` - Equip new `TITLE`\n\n`/equiparm` - Equip new `ARM`\n\n`/viewpet` - View `PET` Stats\n\n`/equippet` - Equip new `PET`\n\n`/trade` @`PLAYER` `ITEM` - trade `CARDS`, `TITLES`, `ARMS` or `PETS`\n\n`/sell` @`PLAYER` `ITEM` - sell `CARDS`, `TITLES`, `ARMS` or `PETS`\n\n`/build` - view current Build\n\n`/savedeck` - save current Build\n\n`/viewdeck` - view/load Saved Builds\n\n`/shop` - Open Pop Up `SHOP` *Use :fast_forward:*\n\n"
CROWN_UNLIMITED_GAMES="`/crownhelp` - Crown Unlimited Help Book\n\n`/senpaibattle` - Tutorial Bot\n\n`/legendbattle` -  Advanced Tutorial Bot\n\n`/battle` @`PLAYER` - Challenge another Player\n\n`/start` - To start a battle in your current session\n\n`/wager` `AMOUNT` - Wager amount to battle in current session\n\n`/solo` - Play Crown Unlimited In DMS\n\n`/tales` - Opens Crown Tales Story Mode Menu\n\n`/dungeon` - Opens Crown Tales Dungeon Menu\n\n`/boss` `UNIVERSE` - Opens Crown Universe Boss Fight\n\n`/ctales` @`COMPANION` - Opens Crown Tales CO-OP Story Mode Menu\n\n`/cdungeon` @`COMPANION`- Opens Crown Tales CO-OP Dungeon Menu\n\n`/cboss` @`COMPANION` `UNIVERSE` - Opens Crown Universe CO-OP Boss Fight\n\n`/enhance` - Opens Enhancement Help Menu\n\n"

BOT_COMMANDS = textwrap.dedent(f"""\
**ACCOUNT COMMANDS**
**/r**: Account Registration
**/deleteaccount @player**IWANTTODELETEMYACCOUNT: Delete your account
**/lookup @player**: Profile lookup

**GAME COMMANDS**
**/vs @player**: Matchup lookup

**TEAM COMMANDS**
**/team team name**: Team lookup
**/createteam game team name**: Create team 
**/deleteteam**: Delete team
**/recruit @player**: Add player to team
**/deletemember @player**: Delete team member
**/apply @player**: Apply for owners team 
**/leaveteam team**: Leave Team
**/pay @player amount**: Send Team Members coin (Owner Onlu)
**/donate amount team name**: Donate coin to Team Bank

**GUILD COMMANDS**
**/guild guild name**: Guild lookup
**/oath player guild name**: Create Guild/Reswear Guild
**/disband**: Delete Guild (Founder Only)
**/betray**: Leave Guild (Sworn Only)
**/knight @player**: Set Guild Shield to Player (Guild Owners Only)
**/ally @player**: Add Team To Guild (Guild Owners Only)
**/exile @player**: Kick Team from Guild (Guild Owners Only)
**/renounce**: Leave Guild (Team Owner Only)
**/sponsor team name amount**: Send Team Guild coin (Guild Owners Onlu)
**/donate amount team name**: Donate coin to Team Bank
**/bounty amount**: Set Guild Bounty (Guild Owners Only)
**/viewhall**: View Hall Information
**/buyhall**: Buy and move into a new Guild Hall

**FAMILY COMMANDS**
**/family @user**: Family lookup
**/marry @user**:Create Family with a User
**/divorce @user**: Ask for divorce from partner
**/adopt @user**: Adopt user into family as Child
**/disown @user**: Remove Child From Family
**/runaway**: Runaway from family as child
**/abandon**: Delete Family
**/allowance @player amount**: Send Family Members coin (Head/Partner Only)
**/invest amount**: Invest coin into family Bank
**/houses**: Show list of available houses
**/viewhouse**: View House Information
**/buyhouse**: Buy and move into a new family house


**LOBBY COMMANDS**
**/check @player**: Check if player is in a lobby
**/end**: End lobby and save score
""")

CROWN_UNLIMITED_COMMANDS = textwrap.dedent(f"""\
**CROWN UNLIMITED PROFILE COMMANDS**
**/menu**: View Balance

**/crown**: Crown Unlimited Help Book
**/build**: View your current build
**/preset** View your build presets
**/savepreset**: Save your current build as preset
**/shop**: Open shop
**/bal**: View Balance
**/cards**: Open your list of Cards
**/titles**: Open your list of Titles
**/arms**: Open your list of Arms
**/pets**: Open your list of Pets
**/quest**: Open your list of Quests
**/rebirth**: Rebirth Account with permanent increases

**CROWN UNLIMITED PVP COMMANDS**
**/senpaibattle**: Tutorial Bot
**/legendbattle**:  Advanced Tutorial Bot
**/battle @player**: Challenge another Player
**/start** Start a battle in your current session
**/arena:** Starts round against current opponent and No Pets Allowed/
**/brawl:** Starts round against current opponent with equal health, attack, and defense/
**/arenabrawl:** Starts round against current opponent with equal health, attack, and defense and No Pets are allowed/
**/wager amount**: Wager amount to battle in current session
**/raid guild**: Start Guild Raid Battle

**CROWN UNLIMITED STORY MODE COMMANDS**
**/ff**: Leave current tale, dungeon, or boss fight
**/universes**: Show List Of Crown Universes
**/tales**: Opens Crown Tales Story Mode Menu
**/dungeon**: Opens Crown Tales Dungeon Menu
**/boss**: Opens Crown Universe Boss Menu
**/ctales @companion**: Opens Crown Tales CO-OP Story Mode Menu
**/cdungeon @companion**: Opens Crown Tales CO-OP Dungeon Menu
**/cboss @companion**: Opens Crown Universe CO-OP Boss Menu
**/dtales 1-3**: Opens Crown Tales Duo Story Mode Menu
**/ddungeon 1-3**: Opens Crown Tales Duo Dungeon Menu
**/dboss 1-3**: Opens Crown Universe Duo Boss Menu
**PATREON ONLY**
**/atales**:Auto-Battle Tales
""")
CTAP_COMMANDS = textwrap.dedent(f"""\
**CARD COMMANDS**
**/cards universe**: View Universe Card List
**/viewcard**: Preview Card 
**/buycard**: Buy Card
**/equipcard card**: Equip card
**/analysis card**: View Card Statistics and Optimal Builds
**/destiny**: Open your Destiny List
**/destinies universe**: Show Available Universe Destinies
**/viewboss boss**:Show Boss Description

**TITLE COMMANDS**
**/titlelist universe**: View Universe Title List
**/viewtitle**: Preview Title
**/buytitle**: Buy Title
**/equiptitle title**: - Equip title

**ARM COMMANDS**
**/armlist universe**: View Universe Arm List
**/viewarm**: Preview Arm
**/buyarm**: Buy Arm
**/equiparm arm**: Equip arm

**PET COMMANDS**
**/petlist universe**: View Universe Pet List
**/viewpet** Preview Pet
**/equippet pet**: Equip pet

**ECONOMY COMMANDS**
**/trade @player item**: Trade Cards, Titles, Arms, Pets
**/sell @player item**: Sell Cards, Titles, and Arms
**/resell item**: Sell Card, Title, Arm back to shop
**/gift @player amount**: Gift player money
""")
