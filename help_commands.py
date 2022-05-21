import textwrap

# PLAYER_COMMANDS="`/d` - Delete `USER` Account" + "\n\n" + "`/vs` `GAME` @`PLAYER` - How many times you defeated opponent" + "\n\n" + "`/r` - Register `USER` Account\n\n"
# PROFILE_COMMANDS="`/lkg` - Lookup available `GAMES`" + "\n\n" + "`/ag` `GAME` - Add `GAME` to `USER` account" + "\n\n" + "`/uign` `GAME` `IGN` - Update In Game Name for `GAME`"  + "\n\n" + "`/lk` @`player` - Lookup a `PLAYERS` profile" + "\n\n" +  "`/lkt` `TEAM Name` - Lookup `TEAM PROFILE`\n\n"
# SENPAI_COMMANDS="`/senpai` - Learn Basic Of Party Chat Gaming Bot" + "\n\n" + "`/bootcamp` - Learn `LOBBY` commands" + "\n\n" + "`/franchise` - Learn `TEAM` commands" + "\n\n" + "`/legend` - Learn `TOURNAMENT` commands\n\n"
# LOBBY_COMMANDS="`/lobby` - Check if `USER` is hosting a lobby" + "\n\n" + "`/check` - Check if `PLAYER` is in a `LOBBY`" + "\n\n" + "`/createlobby` lobbysize `GAME` - Create `LOBBY` up to size 5" + "\n\n" + "`/end` - End `LOBBY` and Record `SCORE`" + "\n\n" + "`/deletelobby` - Delete `LOBBY`" + "\n\n" + "`/joinlobby`  @`PLAYER`- Join  `PLAYER` `LOBBY`" + "\n\n" + "`/score` @`PLAYER` - Score (`PLAYER` / `TEAM`) in `LOBBY`" + "\n\n" + "`/add` (LOCKED) -  Add `PLAYERS` into `LOBBY`\n\n" 
# SHOP_COMMANDS= "`/shop` - Open Pop Up `SHOP`" + "\n\n" + "`/viewcard` - Preview `CARD` in `SHOP`" + "\n\n" + "`/buycard` - Buy `CARD` from `SHOP`" + "\n\n" + "`/viewtitle` - preview `TITLE` in `SHOP`" + "\n\n" + "`/buytitle` - Buy `TITLE` from `SHOP`" + "\n\n" + "`/viewarm` - preview `ARM` in `SHOP`" + "\n\n" + "`/buyarm` - Buy `ARM` from `SHOP`\n\n" + "\n\n" + "`/viewpet` - preview `PET` in `VAULT`"
# TEAM_COMMANDS="`/createteam` `GAME` `TEAM name` - Create `TEAM`" + "\n\n" +   "`/addteamgame` `GAME` - Add `GAME` to `TEAM`" + "\n\n" + "`/deleteteam` `TEAM` - Delete `TEAM` (`OWNER` Only)" + "\n\n" + "`/addtoteam` @`PLAYER` - Add `PLAYER` to `TEAM` (`OWNER` Only)" + "\n\n" + "`/deletemember` @`PLAYER` - Delete `MEMBER` (`OWNER` Only)" + "\n\n" + "`/apply` @`PLAYER` - Applys for `TEAM` (`PLAYER` must be `OWNER`)" + "\n\n" + "`/leaveteam` `TEAM` - Leave `TEAM`\n\n"
# CROWN_UNLIMITED_PLAYER_COMMANDS="`/vault` - Open `VAULT` *Use :fast_forward:*\n\n`/equipcard` `CARD Name` - Equip new `CARD`\n\n`/equiptitle` - Equip new `TITLE`\n\n`/equiparm` - Equip new `ARM`\n\n`/viewpet` - View `PET` Stats\n\n`/equippet` - Equip new `PET`\n\n`/trade` @`PLAYER` `ITEM` - trade `CARDS`, `TITLES`, `ARMS` or `PETS`\n\n`/sell` @`PLAYER` `ITEM` - sell `CARDS`, `TITLES`, `ARMS` or `PETS`\n\n`/build` - view current Build\n\n`/savedeck` - save current Build\n\n`/viewdeck` - view/load Saved Builds\n\n`/shop` - Open Pop Up `SHOP` *Use :fast_forward:*\n\n"

CROWN_UNLIMITED_GAMES = textwrap.dedent(f"""\
**🆕How to Register, Delete, Lookup your account**
**/register**: 🆕 Register your account
**/deleteaccount**: Delete your account
**/player**: Lookup your account, or a friends


**PVE Game Modes**
**🆘 The Tutorial** - Learn Anime VS+ battle system
**🌑 The Abyss** - Climb the ladder for rewards and unlockables
**⚔️ Tales** - Normal battle mode to earn cards, accessories and more
**🔥 Dungeon** - Hard battle mode to earn dungeon cards, dungeon accessories, and more
**👹 Boss Encounter** - Extreme Boss battles to earn Boss cards, boss accessories and more

**Solo Player!**
**/solo** - Play through all pve game modes solo to earn solo rewards

**Co-op Players!**
**/coop** - Play through all pve game modes with a friend to earn co-op rewards

**Duo with AI**
**/duo** - Play through all pve game modes with one of your build presets as an AI companion

**PVP**
**/pvp** - Battle a rival in PVP mode

[Join the Anime VS+ Support Server](https://discord.gg/2JkCqcN3hB)
""")


UNIVERSE_STUFF = textwrap.dedent(f"""\
**View Universes!**
**/universes** - View all available universe info including all available cards, accessories, and destinies

[Join the Anime VS+ Support Server](https://discord.gg/2JkCqcN3hB)
""")


LEGEND = textwrap.dedent(f"""\
**Card Basics**
🀄 - **Card Tier** *1-7*
🔱 - **Card Level** *1-999*
❤️ - **Card Health** (HLT)
🌀 / ⚡ - **Card Stamina** (ST)
🗡️ - **Attack (ATK)** Blue Crystal 🟦
🛡️ - **Defense (DEF)** Red Crystal 🟥
🩸 - Card Passive *Enhancers applied at the start of the battle*

**Accessories & Summons**
🎗️ - **Title accessory**  *Title enhancers are applied each turn, passively.*
🦾 - **Arm accessory** *Arm enhancers are applied passively throughout the duration of battle.*
🧬 - **Summon!** *Summons use Active Enhancers that are available during battle after you Resolve*

**Currency**
💰 - **Coins** *Buy items in the shop and blacksmith*
💎 - **Gems** *Craft universe hearts, souls, cards, and destiny lines!*

[Join the Anime VS+ Support Server](https://discord.gg/2JkCqcN3hB)
""")

ELEMENTS = textwrap.dedent(f"""\
👊 Physical - Normal Damage

<a:Fire:777975890172837898> Fire - Does 30% damage of previous attack on next opponent turn 

❄️ Ice - After 3 uses opponent freezes and loses 1 turn 

💧 Water - increases all water attack dmg by 25 Flat 

🌱 Earth - Cannot be Parried. Increases Def by 20% AP

⚡️ Electric- Add 5% to Shock damage, added to each attack

🌪️ Wind - Cannot Miss 

🔮 Psychic - Penetrates Barriers. Reduce opponent ATK & DEF by 8% AP 

☠️ Death - Adds 5% opponent max health as damage

❤️‍🔥 Life - Heal for 15% AP 

🔅 Light - Regain 50% Stamina Cost

♠️ Dark- Penetrates shields & drains 5 stamina 

🧪 Poison - opponent takes additional 8 damage each turn stacking up to 100

🏹 Ranged - If ST > 80 deals 1.3x Damage

💙 Spirit - Has higher chance of crit attack

⛓️ Recoil - Deals 25% damage back to you

⌛ Time - You Focus after attacking

🩸 Bleed - After 10 Attacks deal 10x turn count damage to opponent

[Join the Anime VS+ Support Server](https://discord.gg/2JkCqcN3hB)
""")


BOT_COMMANDS = textwrap.dedent(f"""\
**Guild Commands**
**/guild** - Guild lookup, configurations, and apply for
**/guildoperations** - Guild operations
**/createguild** - Create guild 
**/disbandguild** - Delete guild
**/recruit** - Recruit player to your guild
**/leaveguild guild** - Leave Guild
**/pay** - Send Guild Members coin
**/donate** - Donate coin to Guild Bank


**Association Commands**
**/association** - Association lookup
**/oath** - Create Association/Reswear Association
**/disband** - Delete Association (Founder Only)
**/betray** - Leave Association (Sworn Only)
**/knight** - Set Association Shield to Player (Association Owners Only)
**/ally** - Add Guild To Association (Association Owners Only)
**/exile** - Kick Guild from Association (Association Owners Only)
**/renounce** - Leave Association (Guild Owner Only)
**/sponsor** - Send Guild coin (Association Owners Onlu)
**/fund** - Donate coin to Association Bank
**/bounty** - Set Association Bounty (Association Owners Only)
**/viewhall** - View Hall Information
**/buyhall** - Buy and move into a new Association Hall


**Family Commands**
**/family** - Family lookup
**/marry** - Create Family with a User
**/divorce** - Ask for divorce from partner
**/adopt** - Adopt kid into family
**/disown** - Remove Kid From Family
**/leavefamily** - Leave from family (Kid Only)
**/abandon** - Delete Family
**/allowance** - Send Family Members coin (Head/Partner Only)
**/invest** - Invest coin into family Bank
**/houses** - Show list of available houses
**/viewhouse** - View House Information
**/buyhouse** - Buy and move into a new family house

[Join the Anime VS+ Support Server](https://discord.gg/2JkCqcN3hB)
""")


CTAP_COMMANDS = textwrap.dedent(f"""\
**Main Menu!⚒️**
**/menu** - Access your current build, cards, titles, arms, quests, and destinies. You can also open the shop and visit the blacksmith here!

**Reward Codes! ⌨️**
**/code** - Enter in codes to earn in-game rewards!

**Trade! 🎴 🎗️ 🦾**
**/trade** - Start a trade with a friend!
**/tradecoins** - Add 🪙 to your trade!

**Gift! 🪙**
**/gift** - Gift a friend some 🪙!

**Card Analysis! 🎴**
**/analysis** - View specific card statistics and optimal builds for that card

**Do you already know the card or accessories name?**
*If you already know what you want to equip / view, use the fast equip commands below to equip your item...*
*/equipcard*
*/equiparm*
*/equiptitle*
*/equipsummon*
------------------
*/view*

[Join the Anime VS+ Support Server](https://discord.gg/2JkCqcN3hB)
""")
