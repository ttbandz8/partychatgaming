import textwrap

# PLAYER_COMMANDS="`/d` - Delete `USER` Account" + "\n\n" + "`/vs` `GAME` @`PLAYER` - How many times you defeated opponent" + "\n\n" + "`/r` - Register `USER` Account\n\n"
# PROFILE_COMMANDS="`/lkg` - Lookup available `GAMES`" + "\n\n" + "`/ag` `GAME` - Add `GAME` to `USER` account" + "\n\n" + "`/uign` `GAME` `IGN` - Update In Game Name for `GAME`"  + "\n\n" + "`/lk` @`player` - Lookup a `PLAYERS` profile" + "\n\n" +  "`/lkt` `TEAM Name` - Lookup `TEAM PROFILE`\n\n"
# SENPAI_COMMANDS="`/senpai` - Learn Basic Of Party Chat Gaming Bot" + "\n\n" + "`/bootcamp` - Learn `LOBBY` commands" + "\n\n" + "`/franchise` - Learn `TEAM` commands" + "\n\n" + "`/legend` - Learn `TOURNAMENT` commands\n\n"
# LOBBY_COMMANDS="`/lobby` - Check if `USER` is hosting a lobby" + "\n\n" + "`/check` - Check if `PLAYER` is in a `LOBBY`" + "\n\n" + "`/createlobby` lobbysize `GAME` - Create `LOBBY` up to size 5" + "\n\n" + "`/end` - End `LOBBY` and Record `SCORE`" + "\n\n" + "`/deletelobby` - Delete `LOBBY`" + "\n\n" + "`/joinlobby`  @`PLAYER`- Join  `PLAYER` `LOBBY`" + "\n\n" + "`/score` @`PLAYER` - Score (`PLAYER` / `TEAM`) in `LOBBY`" + "\n\n" + "`/add` (LOCKED) -  Add `PLAYERS` into `LOBBY`\n\n" 
# SHOP_COMMANDS= "`/shop` - Open Pop Up `SHOP`" + "\n\n" + "`/viewcard` - Preview `CARD` in `SHOP`" + "\n\n" + "`/buycard` - Buy `CARD` from `SHOP`" + "\n\n" + "`/viewtitle` - preview `TITLE` in `SHOP`" + "\n\n" + "`/buytitle` - Buy `TITLE` from `SHOP`" + "\n\n" + "`/viewarm` - preview `ARM` in `SHOP`" + "\n\n" + "`/buyarm` - Buy `ARM` from `SHOP`\n\n" + "\n\n" + "`/viewpet` - preview `PET` in `VAULT`"
# TEAM_COMMANDS="`/createteam` `GAME` `TEAM name` - Create `TEAM`" + "\n\n" +   "`/addteamgame` `GAME` - Add `GAME` to `TEAM`" + "\n\n" + "`/deleteteam` `TEAM` - Delete `TEAM` (`OWNER` Only)" + "\n\n" + "`/addtoteam` @`PLAYER` - Add `PLAYER` to `TEAM` (`OWNER` Only)" + "\n\n" + "`/deletemember` @`PLAYER` - Delete `MEMBER` (`OWNER` Only)" + "\n\n" + "`/apply` @`PLAYER` - Applys for `TEAM` (`PLAYER` must be `OWNER`)" + "\n\n" + "`/leaveteam` `TEAM` - Leave `TEAM`\n\n"
# CROWN_UNLIMITED_PLAYER_COMMANDS="`/vault` - Open `VAULT` *Use :fast_forward:*\n\n`/equipcard` `CARD Name` - Equip new `CARD`\n\n`/equiptitle` - Equip new `TITLE`\n\n`/equiparm` - Equip new `ARM`\n\n`/viewpet` - View `PET` Stats\n\n`/equippet` - Equip new `PET`\n\n`/trade` @`PLAYER` `ITEM` - trade `CARDS`, `TITLES`, `ARMS` or `PETS`\n\n`/sell` @`PLAYER` `ITEM` - sell `CARDS`, `TITLES`, `ARMS` or `PETS`\n\n`/build` - view current Build\n\n`/savedeck` - save current Build\n\n`/viewdeck` - view/load Saved Builds\n\n`/shop` - Open Pop Up `SHOP` *Use :fast_forward:*\n\n"
CROWN_UNLIMITED_GAMES="`/crownhelp` - Crown Unlimited Help Book\n\n`/senpaibattle` - Tutorial Bot\n\n`/legendbattle` -  Advanced Tutorial Bot\n\n`/battle` @`PLAYER` - Challenge another Player\n\n`/start` - To start a battle in your current session\n\n`/wager` `AMOUNT` - Wager amount to battle in current session\n\n`/solo` - Play Crown Unlimited In DMS\n\n`/tales` - Opens Crown Tales Story Mode Menu\n\n`/dungeon` - Opens Crown Tales Dungeon Menu\n\n`/boss` `UNIVERSE` - Opens Crown Universe Boss Fight\n\n`/ctales` @`COMPANION` - Opens Crown Tales CO-OP Story Mode Menu\n\n`/cdungeon` @`COMPANION`- Opens Crown Tales CO-OP Dungeon Menu\n\n`/cboss` @`COMPANION` `UNIVERSE` - Opens Crown Universe CO-OP Boss Fight\n\n`/enhance` - Opens Enhancement Help Menu\n\n"

LEGEND = textwrap.dedent(f"""\
**Card Basics**
🀄 - Card Tier *1-7*
:trident: - Card Level *1-500*
:heart:  - Card Health (HLT)
:cyclone: - Card Stamina (ST)
🗡️ - Attack (ATK) *Blue Crystal* 🟦
🛡️ - Defense (DEF) *Red Crystal* 🟥
:drop_of_blood: - Card Passive *Enhancers applied at the start of battle*
:infinity: - Universe Trait for Card 
*Each Universe has it's own unique Universe Trait*

**Accessories & Summons**
:reminder_ribbon: - Title  *Title enhancers are applied at the start of battle.*
:mechanical_arm: - Arm *Arm enhancers are applied passively throughout the duration of battle.*
🧬 - Summon *Summons use Active Enhancers and are available during battle after you Resolve*

**Moveset**
*Each ability costs Stamina*
:boom: - Basic Attack *costs 10 :cyclone:*
:comet: - Special Attack *costs 30 :cyclone:*
:rosette: - Ultimate Attack *costs 80 :cyclone:*
:microbe: - Active Enhancer Ability *costs 20 :cyclone:*
↘️ - Explains Enhancer Ability

**Battle Explanation**
Select your attack be mindful of stamina cost, 
Once your Stamina reaches 0 you will go into **Focus** mode, where you will recover **90 Stamina**, you will sacrifice 1 turn to increase Attack, Defense and Heal!
After you focus you are able to **Resolve** to boost your Attack and Health but lowering your defense.
You are able to use your  🧬 **Summon** after you Resolve!
First card with 0 health loses!

**Currency**
:coin: - Coins *Buy Items in the /shop and /trinketshop*
:gem: - Gems *Craft Universe Hearts and Souls*

IMPORTANT REMINDER! ⬇️
Use **/daily** to claim your **Daily Reward!** 
**/tutorial** - Tutorial Battle    
**/crown** - Read Game Manual
**/help** - Help Menu
**/enhancers** - Enhancer Help Menu
""")

BOT_COMMANDS = textwrap.dedent(f"""\
**Register, Delete, Lookup**
**/register**: Account Registration
**/deleteaccount**: Delete your account
**/lookup @player**: Profile lookup

**Guild Commands**
**/guild guild name**: Guild lookup
**/createguild guild name**: Create guild 
**/deleteguild**: Delete guild
**/recruit @player**: Add player to guild
**/deletemember @player**: Delete guild member
**/apply @player**: Apply for owners guild 
**/leaveguild guild**: Leave Guild
**/pay @player amount**: Send Guild Members coin (Owner Onlu)
**/donate amount guild name**: Donate coin to Guild Bank

**Association Commands**
**/association association name**: Association lookup
**/oath player association name**: Create Association/Reswear Association
**/disband**: Delete Association (Founder Only)
**/betray**: Leave Association (Sworn Only)
**/knight @player**: Set Association Shield to Player (Association Owners Only)
**/ally @player**: Add Guild To Association (Association Owners Only)
**/exile @player**: Kick Guild from Association (Association Owners Only)
**/renounce**: Leave Association (Guild Owner Only)
**/sponsor guild name amount**: Send Guild coin (Association Owners Onlu)
**/fund amount**: Donate coin to Association Bank
**/bounty amount**: Set Association Bounty (Association Owners Only)
**/viewhall**: View Hall Information
**/buyhall**: Buy and move into a new Association Hall

**Family Commands**
**/family @user**: Family lookup
**/marry @user**:Create Family with a User
**/divorce @user**: Ask for divorce from partner
**/adopt @user**: Adopt kid into family
**/disown @user**: Remove Kid From Family
**/leavefamily**: Leave from family (Kid Only)
**/abandon**: Delete Family
**/allowance @player amount**: Send Family Members coin (Head/Partner Only)
**/invest amount**: Invest coin into family Bank
**/houses**: Show list of available houses
**/viewhouse**: View House Information
**/buyhouse**: Buy and move into a new family house

""")

CROWN_UNLIMITED_COMMANDS = textwrap.dedent(f"""\
**Profile Commands**
**/build**: View your current build
**/preset** View your build presets
**/savepreset**: Save your current build as preset
**/shop**: Open shop
**/balance**: View Balance
**/craft**: Open Crafting
**/gems**: View Gems
**/cards**: Open your list of Cards
**/titles**: Open your list of Titles
**/arms**: Open your list of Arms
**/summons**: Open your list of Summons
**/quest**: Open your list of Quests
**/rebirth**: Rebirth Account with permanent increases

**PvP Commands**
**/battle @player**: Challenge another Player
**/raid association**: Raid another Association
**/arena**: Create PVP Arena

**Tutorial Bot Commands**
**/battle @Senpai**: Tutorial Bot
**/battle @Legend**: Advanced Tutorial Bot
*Must be in Support Server For Tutorial*
**/menu**: View In Game Menu
**/crown**: Crown Unlimited Help Book

**Story Commands**
**/forcequit**: Close Story Mode Private Channel.
**/tales**: Opens Crown Tales Story Mode Menu
**/coop**: Opens Crown Tales CO-OP Story Mode Menu
**/duo**: Opens Crown Tales Duo Story Mode Menu

**Crown Multiverse**
**/universes**: Show List Of Crown Universes
**/viewuniverse universe**: Show Expanded Universe Details


""")
CTAP_COMMANDS = textwrap.dedent(f"""\
**Card Commands**
**/cards**: Open your list of Cards
**/cardlist universe**: View Universe Card List
**/viewcard**: Preview Card 
**/equipcard card**: Equip card
**/analysis card**: View Card Statistics and Optimal Builds
**/destiny**: Open your Destiny List
**/destinies universe**: Show Available Universe Destinies
**/viewboss boss**:Show Boss Description

**Title Commands**
**/titles**: Open your list of Titles
**/titlelist universe**: View Universe Title List
**/viewtitle**: Preview Title
**/equiptitle title**: - Equip title

**Arm Commands**
**/arms**: Open your list of Arms
**/armlist universe**: View Universe Arm List
**/viewarm**: Preview Arm
**/equiparm arm**: Equip arm

**Summon Commands**
**/summons**: Open your list of Summons
**/summonlist universe**: View Universe Pet List
**/viewsummon** Preview Pet
**/equipsummon pet**: Equip pet

**Sell, Trade, Resell, Gift**
**/trade** : Create trade
**/tradecoins**: Add Coins to trade
**/gift @player amount**: Gift player money
""")
