from dataclasses import field
from discord import player, team
from discord.ext.commands.errors import CommandOnCooldown
from discord.flags import Intents
from pymongo.collation import CollationMaxVariable
import db
import time
import classes as data
import test_data as td
import messages as m
import discord
import DiscordUtils
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import help_commands as h
import destiny as d
# Converters
from discord import User
from discord import Member
from discord_slash import SlashCommand


import os
import logging
import requests
from decouple import config
from collections import ChainMap
import textwrap
import random
import unique_traits as ut
now = time.asctime()

'''User must have predefined roles of the games they play before creating users
   User input for IGN will be available after User is created and goes to join game events
   User input for TEAM will be available after User is created. There will be a command to add Team. '''


# Logging Logic

logging.basicConfig(level=logging.ERROR)

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
emojis = ['👍', '👎']
guild_ids = None

intents = discord.Intents.all()
client = discord.Client()

if config('ENV') == "production":
   # PRODUCTION
   bot = commands.Bot(command_prefix=".", intents=intents)
else:
   # TEST
   bot = commands.Bot(command_prefix=",", intents=intents)
   guild_ids = [839352855000776735]

slash = SlashCommand(bot, sync_commands=True)

bot.remove_command("help")

@bot.group(invoke_without_command=True)
async def help(ctx):
   avatar="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Legend.png"

   embedVar1 = discord.Embed(title= f"Bot Commands", description=h.BOT_COMMANDS, colour=0x7289da)
   embedVar1.set_thumbnail(url=avatar)
   embedVar1.add_field(name="Help Navigation", value="*First Page: :track_previous:|Prev Page: :rewind:|\nNext Page: :fast_forward:| Last Page: :track_next:*")
   embedVar1.set_footer(text=f".senpai - Text Bot Tutorial")

   embedVar2 = discord.Embed(title= f"Crown Unlimited Commands", description=h.CROWN_UNLIMITED_COMMANDS, colour=0x7289da)
   embedVar2.set_thumbnail(url=avatar)
   embedVar2.add_field(name="Help Navigation", value="*First Page: :track_previous:|Prev Page: :rewind:|\nNext Page: :fast_forward:| Last Page: :track_next:*")
   embedVar2.set_footer(text=f".senpai - Text Bot Tutorial")
   
   embedVar3 = discord.Embed(title= f"CTAP Commands", description=h.CTAP_COMMANDS, colour=0x7289da)
   embedVar3.set_thumbnail(url=avatar)
   embedVar3.add_field(name="Help Navigation", value="*First Page: :track_previous:|Prev Page: :rewind:|\nNext Page: :fast_forward:| Last Page: :track_next:*")
   embedVar3.set_footer(text=f".senpai - Text Bot Tutorial")

   paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
   paginator.add_reaction('⏮️', "first")
   paginator.add_reaction('⏪', "back")
   paginator.add_reaction('🔐', "lock")
   paginator.add_reaction('⏩', "next")
   paginator.add_reaction('⏭️', "last")
   embeds = [embedVar2,embedVar3, embedVar1]
   await paginator.run(embeds)

@slash.slash(name="Ping", description="Ping server speed", guild_ids=guild_ids)
async def ping(ctx):
   await ctx.send(f'Local Test Bot speed = {round(bot.latency * 1000)}ms')

async def validate_user(ctx):
   query = {'DISNAME': str(ctx.author)}
   valid = db.queryUser(query)

   if valid:
      return True
   else:
      msg = await ctx.send(m.USER_NOT_REGISTERED, delete_after=5)
      return False

async def load(ctx, extension):
   # Goes into cogs folder and looks for extension
   bot.load_extension(f'cogs.{extension}')

async def unload(ctx, extension):
   # Goes into cogs folder and looks for extension
   bot.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
   if filename.endswith('.py'):
      # :-3 removes .py from filename
      bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
   print('Bot is ready! ')

@slash.slash(name="Enhancers", description="List of Enhancers", guild_ids=guild_ids)
async def enhance(ctx):
   avatar="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Legend.png"


   embedVar1 = discord.Embed(title= f":trident:ENHANCE Sets:",colour=0x7289da)
   embedVar1.set_thumbnail(url=avatar)
   embedVar1.add_field(name="`INCREASES`", value="`ATK` - Increase `ATK`\n\n`DEF` - Increase `DEF`\n\n`HLT` - Increase `HLT`\n\n`STAM` - Increase `STAM`\n\n")
   embedVar1.set_footer(text=f"/help - Bot Help")

   embedVar2 = discord.Embed(title= f":trident:ENHANCE Sets:",colour=0x7289da)
   embedVar2.set_thumbnail(url=avatar)
   embedVar2.add_field(name="`STEALS`", value="`FLOG`- `ATK` Steal\n\n`WITHER`- `DEF` Steal\n\n`LIFE` - `LIFE` Steal\n\n`DRAIN` - `STAM` Steal\n\n")
   embedVar2.set_footer(text=f"/help - Bot Help")

   embedVar3 = discord.Embed(title= f":trident:ENHANCE Sets:",colour=0x7289da)
   embedVar3.set_thumbnail(url=avatar)
   embedVar3.add_field(name="`SACRIFICE`", value="`RAGE` - Decrease `DEF`, Increase `ATK`\n\n`BRACE` - Decrease `ATK`, Increase `DEF`\n\n`BZRK` - Decrease `HLT`,  Increase `ATK`\n\n`CRYSTAL`- Decrease `HLT`, Increase `DEF`\n\n`GROWTH`- Decrease `MAXHLT`, Increase `STATS`\n\n")
   embedVar3.set_footer(text=f"/help - Bot Help")

   embedVar4 = discord.Embed(title= f":trident:ENHANCE Sets:",colour=0x7289da)
   embedVar4.set_thumbnail(url=avatar)
   embedVar4.add_field(name="`TRADE`", value="`STANCE` - Swap `ATK` and `DEF`\n\n`CONFUSE` - Swap `OPP ATK` and  `OPP DEF`\n\n")
   embedVar4.set_footer(text=f"/help - Bot Help")

   embedVar5 = discord.Embed(title= f":trident:ENHANCE Sets:",colour=0x7289da)
   embedVar5.set_thumbnail(url=avatar)
   embedVar5.add_field(name="`TIME`", value="`BLINK`  - Decrease  `STAM`, Increase `OPP STAM`\n\n`SLOW` - Decrease `STAM`, Swap `OPP STAM`\n\n`HASTE` - Increase `STAM`, Swap `OPP STAM`\n\n")
   embedVar5.set_footer(text=f"/help - Bot Help")

   embedVar6 = discord.Embed(title= f":trident:ENHANCE Sets:",colour=0x7289da)
   embedVar6.set_thumbnail(url=avatar)
   embedVar6.add_field(name="`CONTROL`", value="`SOULCHAIN` - Both `PLAYERS` `STAM` = \n\n`GAMBLE` - Both `PLAYERS` `HEALTH` =\n\n`FEAR` - Decrease `MAXHLT`, Decrease `OPP ATK` & `OPP DEF`\n\n")
   embedVar6.set_footer(text=f"/help - Bot Help")

   embedVar8 = discord.Embed(title= f":trident:ENHANCE Sets:",colour=0x7289da)
   embedVar8.set_thumbnail(url=avatar)
   embedVar8.add_field(name="`DAMAGE`", value="`WAVE` - Decreasing Turn Count Based AP DMG \n\n`BLAST` - Increasing Turn Count Based AP DMG\n\n")
   embedVar8.set_footer(text=f"/help - Bot Help")

   embedVar9 = discord.Embed(title= f":trident:ENHANCE Sets:",colour=0x7289da)
   embedVar9.set_thumbnail(url=avatar)
   embedVar9.add_field(name="`DIVINITY`", value="`CREATION` - Increase `MAXHEALTH`\n\n`DESTRUCTION` - Decrease `OPP MAXHEALTH`\n\n")
   embedVar9.set_footer(text=f"/help - Bot Help")

   embedVar7 = discord.Embed(title= f":trident:ENHANCE DETAILS:", description=textwrap.dedent(f"""
   **ATK:** AP Percentage Based Attack Increased
   **DEF:** AP Percentage Based Attack Increased
   **STAM:** Increased Stamina based on AP Value
   **HLT:** Increased Health based on AP Value
   **LIFE:** Lifesteals based on AP Value and 5% of Opponent Health
   **DRAIN:** Steals Opponent Stamina based on AP Value
   **FLOG:** Steals Attack based on 30% of AP Percentage
   **WITHER:** Steals Defense based on 30% of AP Percentage
   **RAGE:** Gain ATK but Lose DEF based on 50% of AP Percentage Of Your DEF
   **BRACE:** GAIN DEF but Lose ATK based on 50% AP Percentage Of Your ATK
   **BZRK:** Gain ATK Based on 50% of your  AP Percentage of Your HLT
   **CRYSTAL:** Gain DEF Based on 50% of your AP Percentage Of Your Health
   **GROWTH:** Lower Max Health, Increase Defense and Attack based on AP Percentage
   **STANCE:** Swaps your ATK and your DEF, and gives you additional DEF based on AP Value
   **CONFUSE:** Swaps ATK and DEF of opponent and saps additional DEF based on AP Value
   **BLINK:** Decreases Your Stamina by AP Value and gives opponent Stamina by AP Value
   **SLOW:** Increases Your Stamina by AP Value, Decreases your Opponent Stamina by AP Value, then swaps your and your opponents Stamina
   **HASTE:** Decreases your opponent Stamina, Increases your stamina, swap your and your opponent stamina
   **SOUL:** CHAIN - Make you and your opponent Stamina the same based on AP Value
   **GAMBLE:** Make you and your opponent health the same based on AP Value
   **FEAR:** Lower your Health by AP Percentage, Lower your opponent ATK and DEF by AP Percentage
   **WAVE:** Deals AP / Turn Count Damage to Opponent that decreases as the Turn Count increases
   **BLAST:** Deals AP * Turn Count Damage to Opponent that increases as the Turn Count increases
   **CREATION:** Increases AP / Turn Count Max Health & Health that decreases as the Turn Count increases
   **DESTRUCTION:** Decreases AP * Turn Count Max Health that increases as the Turn Count increases
   """) ,colour=0x7289da)
   embedVar7.set_thumbnail(url=avatar)
   embedVar7.set_footer(text=f"/help - Bot Help")

   paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
   paginator.add_reaction('⏮️', "first")
   paginator.add_reaction('⏪', "back")
   paginator.add_reaction('🔐', "lock")
   paginator.add_reaction('⏩', "next")
   paginator.add_reaction('⏭️', "last")
   embeds = [embedVar1, embedVar2, embedVar3, embedVar4, embedVar5, embedVar6, embedVar8, embedVar9, embedVar7]
   await paginator.run(embeds)

@slash.slash(name="Crown", description="Crown Unlimited Tutorial", guild_ids=guild_ids)
async def crown(ctx):
   avatar="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Legend.png"


   embedVar1 = discord.Embed(title= f":crown: Crown Unlimited",colour=0x7289da)
   embedVar1.set_thumbnail(url=avatar)
   embedVar1.add_field(name="About The Game!", value=textwrap.dedent(f"""\
   **Crown Unlimited** is a Multiplatform Card Game exploring **Universes** from your favorite Video Game and Anime Series!

   Explore Tales, Dungeons, and Bosses! Play **Solo**, or with **Friends**!
   """))

   embedVar2 = discord.Embed(title= f":crown: Getting Started", description=textwrap.dedent(f"""\
   Players begin with 3 cards from the **Starter Universes**.
   The Title **Starter** and the Arm **Stock** are equipped.
   Your first Pet **Chick** will be joining as well!   

   The **Starter Universes** are _My Hero Academia_, _Kanto Region_, and _League Of Legends_.

   Play **Single Player** and **Multiplayer** Modes to earn :coin:
   Buy and equip better Items and unlock new **Universes**!
   """), colour=0x7289da)
   embedVar2.set_thumbnail(url=avatar)

   embedVar3 = discord.Embed(title= f":crown: Card Mechanics", description=textwrap.dedent(f"""\
   **Card Stats** 
   Health (**HLT**) Stamina (**STAM**) Attack (**ATK**) Defense(**DEF**)

   **Cards Have 6 Elements** 
   3 Abilities
   1 Enhancer
   1 Unique Passive
   1 Universe Trait
   

   **Abilities**
   Abilities inflict damage on the opponent.
   Each ability matches a **Number** and **Stamina Cost** in the Movelist.
   **1:** Basic Attack _uses 10 stamina_
   **2:** Special Attack _uses 30 stamina_
   **3:** Ultimate Attack _uses 80 stamina_
   
   **Block**
   Doubles Defense for 1 turn
   **0:** _uses 20 stamina_ 

   **Enhancer**
   Enhancers either boost your stats or inflict status effects on your opponent. Use .enhance for full list of Enhancers and their effects.
   **4:** Enhancer _uses 20 stamina_

   **Unique Passive**
   Unique Passives are Enhancers that take effect at the beginning of the battle.

   **Universe Traits**
   Universe Traits are universe specific abilities activated during battle. Use .traits for a full list of Universe Traits.

   **Destinies**
   Destinies are card specific achievements that earn you special **Destiny Cards**
 

   """), colour=0x7289da)
   embedVar3.set_thumbnail(url=avatar)

   embedVar4 = discord.Embed(title= f":crown: Titles, Arms, and Pets", description=textwrap.dedent(f"""\
   **Titles** & **Arms** 
   Modify you or the Opponents **Stats** prior to battle by applying **Enhancers** at the start of the match.
   Buy **Titles** and **Arms** with :coin: or Earn them via **Drops**

   **Universe Buff** :Match Your Titles and Arms to your Card **Universe**.
   **Buff**: **Base Stats** + 100 **HLT** , 20 **ATK** & 20 **DEF**.

   **Destiny Universe Buff** Destiny Cards gain an additional **Buff**.
   **Buff**: **Universe Buff** + 50 **HLT**, 5 **ATK** and 5 **DEF**.

   **Pets**
   Can assist during battle with an **Enhancer**.
   Earn **Pets** through Tales, Dungeon and Boss **Drops** or through trade with other Players!
   Battle with your **Pet** to gain **EXP** to increase Pet **Ability Power**. 

   Mix and Match Titles, Arms and Pets to gain the **Tactical Advantage**!
   """) ,colour=0x7289da)
   embedVar4.set_thumbnail(url=avatar)

   embedVar5 = discord.Embed(title= f":crown: Battle Mechanics", description=textwrap.dedent(f"""\
   Players take turns dealing damage using one of their 3 **Abilities**.
   
   **Stamina** costs are standard across all Cards 
   _check Cards page for details_.
   
   **Recovery**
   When Players have used all of their **Stamina** they enter **Focus State**.

   The Match is over when a players **Health** reaches 0.
   """) ,colour=0x7289da)
   embedVar5.set_thumbnail(url=avatar)

   embedVar6 = discord.Embed(title= f":crown: Focus & Resolve", description=textwrap.dedent(f"""\
   **Focus**
   Players can take advantage of **Focus State** to **Recover**.
   **Focus State** sacrifices a turn to Level Up Stats, increase **Stamina** to 90, and **Recover** some **Health**.
   
   **Resolve**
   Once in **Focus State** players can use 5 to **Resolve**!
   **Resolved Characters** transform to greatly increase attack and health while sacrificing defense.
   **Resolved Characters** can summon Pets to aid them in battle.
   **5:** Resolve _uses 1 turn_.

   **Pet Assistance!**
   Pets Enhancers can either boost your stats or inflict status effects on your opponent. Pet moves do not end the player turn!
   **6:** Pet _uses 15 stamina_.

   """) ,colour=0x7289da)
   embedVar6.set_thumbnail(url=avatar)

   embedVar7 = discord.Embed(title= f":crown:CROWN Single Player", description=textwrap.dedent(f"""\
   **Single Player**
   
   **Solo**
   **/tales** Single player adventures where you traverse through your favorite universes as characters from various worlds!
   **/dungeon** Hard version of tales with better loot and better drop rates! (Unlocks after completing **Crown Tale**)
   **/boss** End Game battles featuring Iconic Villians from Crown Universes. (Unlocks after completing **Crown Dungeon**)
   **PATREON ONLY**
   **/atales**:Auto-Battle Tales
   
   **Duo**
   **/dtales 1-3** Battle with your favorite AI preset in this Duo Tale!
   **/ddungeon 1-3** Bring your strongest builds through the Darkest Duo Dungeons.
   **/dboss 1-3** Bring your Dynanmic duo to take on one Incredible Boss.
   
 
   **Crown Rifts**
   Mash-Up Universes featuring heroes and villians connected through common traits and themes!
   Pay attention, Rifts will not stay open for long!
   """),colour=0x7289da)
   embedVar7.set_thumbnail(url=avatar)
   
   embedVar8 = discord.Embed(title= f":crown:CROWN Multiplayer", description=textwrap.dedent(f"""\
   **Multiplayer**
   
   **Co-Op**
   **/ctales @partner** Take a companion with your through your favorite tales with higher stakes!
   **/cdungeon @partner** Bring a companion through the darkest dungeons to earn awesome loot together.
   **/cboss @partner** Epic battles between two high level companions and one Incredible Boss.

   **PVP**
   **/battle @player:** Select your Build and Challenge any Crown Unlimited Player to join your Game Lobby.
   **/start:** Starts round against current opponent.
   **/arena:** Starts round against current opponent and No Pets Allowed.
   **/brawl:** Starts round against current opponent with equal health, attack, and defense.
   **/arenabrawl:** Starts round against current opponent with equal health, attack, and defense and No Pets are allowed.
   **/wager number:*** In lobby players can wager :coin:.
   *Builds are locked during lobbies, to change your build end the lobby with **/end** .*
   
   **Crown Rifts**
   Crown Rifts are Co-Op Compatable and Helping other players in Co-Op **WILL NOT** close your open Rift!
   Grind Those Rifts Together!
   
   """),colour=0x7289da)
   embedVar8.set_thumbnail(url=avatar)
   
   embedVar9 = discord.Embed(title= f":crown: Decks",description=textwrap.dedent(f"""\
   Save your favorite builds in your **Deck**
   **/deck** to open the deck menu and select a preset with **1-3**
   **/savedeck** to save your current build **1-3**
   
   **Deck Builds**
   You can bring your deck builds into Duo Battles!
   **/abuild 1-3** to view the full preset build
   
   Take your **Deck Presets** into Crown Duos!
   """) ,colour=0x7289da)
   embedVar9.set_thumbnail(url=avatar)

   embedVar10 = discord.Embed(title= f":crown: Economy",description=textwrap.dedent(f"""\
   Crown Unlimited features an in game **Shop** where you can purchase new Cards, Titles, and Arms.
   Use /shop to open the **Pop-Up Shop!**

   **Stock**
   Items in the shop have a **Stock**. When they are sold out they become unavailable.

   **Sell & Trade**
   **/sell** and **/trade** will allow you to trade Cards, Titles, Arms and Pets with other players.

   **Resell**
   **/resell item** to sell Cards, Titles, and Arms back to the market.
   """) ,colour=0x7289da)
   embedVar10.set_thumbnail(url=avatar)


   paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
   paginator.add_reaction('⏮️', "first")
   paginator.add_reaction('⏪', "back")
   paginator.add_reaction('🔐', "lock")
   paginator.add_reaction('⏩', "next")
   paginator.add_reaction('⏭️', "last")
   embeds = [embedVar1, embedVar2, embedVar3, embedVar4, embedVar5, embedVar6, embedVar7, embedVar8,embedVar9, embedVar10]
   await paginator.run(embeds)

@slash.slash(name="Register", description="Register for Crown Unlimited", guild_ids=guild_ids)
async def r(ctx):
   disname = str(ctx.author)
   name = disname.split("#",1)[0]
   user = {'DISNAME': disname, 'NAME': name, 'DID' : str(ctx.author.id), 'AVATAR': str(ctx.author.avatar_url)}
   response = db.createUsers(data.newUser(user))
   if response:

      embedVar = discord.Embed(title=f"**Welcome to Crown Unlimited**!", description=textwrap.dedent(f"""
      Embark on a journey through Universes filled with characters from your favorite anime and video games!
      First, run **.daily** to get your daily rewards!

      Type **/menu** for quick overview on what to do next! Checkout the tutorials below if you need additional assistance!

      Start Tutorial!
      **/senpai**

      Start Battle Tutorial!
      **/senpaibattle**
      
      **CHANGING YOUR DISCORD ACCOUNT INFO WILL BREAK YOUR ACCOUNT IN THE GAME. YOU HAVE BEEN WARNED.**
      
      _We do not own the rights to the images used in this game. This is an open beta of an experimental bot for the purposes of growing our coding talents and skill. We do not and will not make money from this project._
      """), colour=0xe91e63)
      embedVar.set_footer(text=".crown to inquire all potential commands and capabilites of the bot")
      await ctx.author.send(embed=embedVar)
      await ctx.send(f"Welcome to Crown Unlimited, {ctx.author.mention}! Use **/daily** to collect your daily reward! Use **/menu** to see what you can do.")

      vault = db.queryVault({'OWNER': disname})
      if vault:
         await ctx.send(m.VAULT_RECOVERED, delete_after=5)
      else:
         vault = db.createVault(data.newVault({'OWNER' : disname}))
         # await ctx.send(m.USER_HAS_REGISTERED, delete_after=5)
   else:
      await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=3) 

@slash.slash(name="Rebirth", description="Rebirth for permanent buffs", guild_ids=guild_ids)
async def rebirth(ctx):
   query = {'DISNAME': str(ctx.author)}
   user_is_validated = db.queryUser(query)
   if user_is_validated:
      rLevel = user_is_validated['REBIRTH']
      if rLevel < 5:
         rebirthCost = round(150000 * (1 + (rLevel)))
         embedVar1 = discord.Embed(title= f":heart_on_fire:{user_is_validated['NAME']}'s Rebirth",colour=0x7289da)
         embedVar1.set_thumbnail(url=user_is_validated['AVATAR'])
         embedVar1.add_field(name=f"Rebirth Level: {user_is_validated['REBIRTH']}\nRebirth Cost: :coin:{'{:,}'.format(rebirthCost)}", value=textwrap.dedent(f"""\
         **Rebirth Effects**
         New Starting Deck
         Starting Pet Bond
         Increase Base ATK
         Increase Base DEF
         Increased :coin: drops
         Increased Item Drop Rates
         
         You will lose all of your equipped and vaulted items.
         
         *Rebirth is permanent and cannot be undone*
         """))
         accept = await ctx.send(embed=embedVar1)
         for emoji in emojis:
            await accept.add_reaction(emoji)

         def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '👍'

         try:
            reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=check)

            vault = db.queryVault({'OWNER': user_is_validated['DISNAME']})
            if vault:
               if vault['BALANCE'] >= rebirthCost:           
                  if rLevel == 0:
                     card_level_list = vault['CARD_LEVELS']
                     owned_cards = []
                     for card in card_level_list:
                        owned_cards.append(card['CARD'])
                     if 'Twice' not in owned_cards:
                        card_level_list.append({'CARD': 'Twice', 'LVL': 0, 'TIER': 1, 'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0})

                     if 'Charmander' not in owned_cards:
                        card_level_list.append({'CARD': 'Charmander', 'LVL': 0, 'TIER': 1, 'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0})

                     if 'Braum' not in owned_cards:
                        card_level_list.append({'CARD': 'Braum', 'LVL': 0, 'TIER': 1, 'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0})

                     delete = db.deleteVault(vault)            
                     vault = db.createVault(data.newVault({'OWNER': user_is_validated['DISNAME'], 'CARDS': ['Twice','Charmander','Braum'], 'TITLES': ['Reborn'], 'ARMS': ['Reborn Stock'],'DECK': [{'CARD': 'Charmander', 'TITLE': 'Reborn', 'ARM': 'Reborn Stock', 'PET': 'Chick'}, {'CARD': 'Twice', 'TITLE': 'Reborn', 'ARM': 'Reborn Stock', 'PET': 'Chick'}, {'CARD': 'Braum', 'TITLE': 'Reborn', 'ARM': 'Reborn Stock', 'PET': 'Chick'}], 'PETS' : [{'NAME': 'Chick', 'LVL': 1, 'EXP': 0, 'Heal': 10, 'TYPE': 'HLT', 'BOND': 2, 'BONDEXP': 0, 'PATH': "https://res.cloudinary.com/dkcmq8o15/image/upload/v1622307902/Pets/chick.jpg"}], 'CARD_LEVELS': card_level_list})) 
                     if vault:  
                        cardList = ['Charmander', 'Twice', 'Braum'] 
                        for card in cardList:
                           for destiny in d.destiny:
                              if card in destiny["USE_CARDS"]:
                                 db.updateVaultNoFilter({'OWNER': user_is_validated['DISNAME']},{'$addToSet':{'DESTINY': destiny}})
                                 message = f"**DESTINY AWAITS!**\n**{destiny['NAME']}** has been added to your vault."     
                                 await ctx.send(message)   
                        db.updateUserNoFilter({'DISNAME': str(ctx.author)}, {'$set': {'CARD': 'Charmander', 'TITLE': 'Reborn', 'ARM':'Reborn Stock'}})  
                        db.updateUserNoFilter({'DISNAME': str(ctx.author)}, {'$set': {'PET': 'Chick'}}) 
                        db.updateUserNoFilter({'DISNAME': str(ctx.author)}, {'$set': {'CROWN_TALES': ['']}}) 
                        db.updateUserNoFilter({'DISNAME': str(ctx.author)}, {'$set': {'DUNGEONS': ['']}}) 
                        db.updateUserNoFilter({'DISNAME': str(ctx.author)}, {'$set': {'BOSS_WINS': ['']}}) 
                        db.updateUserNoFilter(query, {'$inc': {'REBIRTH': 1 }}) 
                        await ctx.send(f"You are now Rebirth Level: {user_is_validated['REBIRTH'] + 1}")           
                  elif rLevel == 1:
                     card_level_list = vault['CARD_LEVELS']
                     owned_cards = []
                     for card in card_level_list:
                        owned_cards.append(card['CARD'])
                     if 'Kirishima' not in owned_cards:
                        card_level_list.append({'CARD': 'Kirishima', 'LVL': 0, 'TIER': 1, 'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0})

                     if 'Squirtle' not in owned_cards:
                        card_level_list.append({'CARD': 'Squirtle', 'LVL': 0, 'TIER': 1, 'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0})

                     if 'Malphite' not in owned_cards:
                        card_level_list.append({'CARD': 'Malphite', 'LVL': 0, 'TIER': 1, 'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0})
                        
                     delete = db.deleteVault(vault)            
                     vault = db.createVault(data.newVault({'OWNER': user_is_validated['DISNAME'], 'CARDS': ['Kirishima','Squirtle','Malphite'], 'TITLES': ['Reborn Soldier'], 'ARMS': ['Deadgun'], 'DECK': [{'CARD': 'Kirishima', 'TITLE': 'Reborn Soldier', 'ARM': 'Deadgun', 'PET': 'Chick'}, {'CARD': 'Squirtle', 'TITLE': 'Reborn Soldier', 'ARM': 'Deadgun', 'PET': 'Chick'}, {'CARD': 'Malphite', 'TITLE': 'Reborn Soldier', 'ARM': 'Deadgun', 'PET': 'Chick'}], 'PETS' : [{'NAME': 'Chick', 'LVL': 3, 'EXP': 0, 'Heal': 10, 'TYPE': 'HLT', 'BOND': 2, 'BONDEXP': 0, 'PATH': "https://res.cloudinary.com/dkcmq8o15/image/upload/v1622307902/Pets/chick.jpg"}], 'CARD_LEVELS': card_level_list}))         
                     if vault:         
                        cardList = ['Squirtle', 'Malphite', 'Kirishima'] 
                        for card in cardList:
                           for destiny in d.destiny:
                              if card in destiny["USE_CARDS"]:
                                 db.updateVaultNoFilter({'OWNER': user_is_validated['DISNAME']},{'$addToSet':{'DESTINY': destiny}})
                                 message = f"**DESTINY AWAITS!**\n**{destiny['NAME']}** has been added to your vault."      
                                 await ctx.send(message)  
                        nCard = db.updateUserNoFilter({'DISNAME': str(ctx.author)}, {'$set': {'CARD': 'Malphite', 'TITLE': 'Reborn Soldier', 'ARM':'Deadgun'}})  
                        db.updateUserNoFilter({'DISNAME': str(ctx.author)}, {'$set': {'PET': 'Chick'}}) 
                        db.updateUserNoFilter({'DISNAME': str(ctx.author)}, {'$set': {'CROWN_TALES': ['']}}) 
                        db.updateUserNoFilter({'DISNAME': str(ctx.author)}, {'$set': {'DUNGEONS': ['']}}) 
                        db.updateUserNoFilter({'DISNAME': str(ctx.author)}, {'$set': {'BOSS_WINS': ['']}}) 
                        nRebirth = db.updateUserNoFilter(query, {'$inc': {'REBIRTH': 1 }}) 
                        await ctx.send(f"You are now Rebirth Level: {user_is_validated['REBIRTH'] + 1}")   
                  elif rLevel == 2:
                     card_level_list = vault['CARD_LEVELS']
                     owned_cards = []
                     for card in card_level_list:
                        owned_cards.append(card['CARD'])
                     if 'Mineta' not in owned_cards:
                        card_level_list.append({'CARD': 'Mineta', 'LVL': 0, 'TIER': 1, 'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0})

                     if 'Bulbasaur' not in owned_cards:
                        card_level_list.append({'CARD': 'Bulbasaur', 'LVL': 0, 'TIER': 1, 'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0})

                     if 'Shen' not in owned_cards:
                        card_level_list.append({'CARD': 'Shen', 'LVL': 0, 'TIER': 1, 'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0})
                        
                     delete = db.deleteVault(vault)            
                     vault = db.createVault(data.newVault({'OWNER' : user_is_validated['DISNAME'], 'CARDS': ['Mineta','Bulbasaur','Shen'], 'TITLES': ['Reborn Legion'], 'ARMS': ['Glaive'], 'DECK': [{'CARD': 'Mineta', 'TITLE': 'Reborn Legion', 'ARM': 'Glaive', 'PET': 'Chick'}, {'CARD': 'Bulbasaur', 'TITLE': 'Reborn Legion', 'ARM': 'Glaive', 'PET': 'Chick'}, {'CARD': 'Shen', 'TITLE': 'Reborn Legion', 'ARM': 'Glaive', 'PET': 'Chick'}], 'PETS' : [{'NAME': 'Chick', 'LVL': 5, 'EXP': 0, 'Heal': 10, 'TYPE': 'HLT', 'BOND': 2, 'BONDEXP': 0, 'PATH': "https://res.cloudinary.com/dkcmq8o15/image/upload/v1622307902/Pets/chick.jpg"}], 'CARD_LEVELS': card_level_list}))         
                     if vault:     
                        cardList = ['Bulbasaur', 'Mineta', 'Shen'] 
                        for card in cardList:
                           for destiny in d.destiny:
                              if card in destiny["USE_CARDS"]:
                                 db.updateVaultNoFilter({'OWNER': user_is_validated['DISNAME']},{'$addToSet':{'DESTINY': destiny}})
                                 message = f"**DESTINY AWAITS!**\n**{destiny['NAME']}** has been added to your vault."    
                                 await ctx.send(message)  
                        nCard = db.updateUserNoFilter({'DISNAME': str(ctx.author)}, {'$set': {'CARD': 'Mineta', 'TITLE': 'Reborn Legion', 'ARM':'Glaive'}})  
                        db.updateUserNoFilter({'DISNAME': str(ctx.author)}, {'$set': {'PET': 'Chick'}}) 
                        db.updateUserNoFilter({'DISNAME': str(ctx.author)}, {'$set': {'CROWN_TALES': ['']}}) 
                        db.updateUserNoFilter({'DISNAME': str(ctx.author)}, {'$set': {'DUNGEONS': ['']}}) 
                        db.updateUserNoFilter({'DISNAME': str(ctx.author)}, {'$set': {'BOSS_WINS': ['']}}) 
                        nRebirth = db.updateUserNoFilter(query, {'$inc': {'REBIRTH': 1 }}) 
                        await ctx.send(f"You are now Rebirth Level: {user_is_validated['REBIRTH'] + 1}")      
                  elif rLevel == 3:
                     card_level_list = vault['CARD_LEVELS']
                     owned_cards = []
                     for card in card_level_list:
                        owned_cards.append(card['CARD'])
                     if 'Hawks' not in owned_cards:
                        card_level_list.append({'CARD': 'Hawks', 'LVL': 0, 'TIER': 1, 'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0})

                     if 'Clefairy' not in owned_cards:
                        card_level_list.append({'CARD': 'Clefairy', 'LVL': 0, 'TIER': 1, 'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0})

                     if 'Yasuo' not in owned_cards:
                        card_level_list.append({'CARD': 'Yasuo', 'LVL': 0, 'TIER': 1, 'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0})
                        
                     delete = db.deleteVault(vault)            
                     vault = db.createVault(data.newVault({'OWNER' : user_is_validated['DISNAME'], 'CARDS': ['Hawks','Clefairy','Yasuo'], 'TITLES': ['Reborn King'], 'ARMS': ['Kings Glaive'], 'DECK': [{'CARD': 'Hawks', 'TITLE': 'Reborn King', 'ARM': 'Kings Glaive', 'PET': 'Chick'}, {'CARD': 'Clefairy', 'TITLE': 'Reborn King', 'ARM': 'Kings Glaive', 'PET': 'Chick'}, {'CARD': 'Yasuo', 'TITLE': 'Reborn King', 'ARM': 'Kings Glaive', 'PET': 'Chick'}], 'PETS' : [{'NAME': 'Chick', 'LVL': 1, 'EXP': 0, 'Heal': 10, 'TYPE': 'HLT', 'BOND': 3, 'BONDEXP': 0, 'PATH': "https://res.cloudinary.com/dkcmq8o15/image/upload/v1622307902/Pets/chick.jpg"}], 'CARD_LEVELS': card_level_list}))         
                     if vault: 
                        cardList = ['Hawks', 'Clefairy', 'Yasuo'] 
                        for card in cardList:
                           for destiny in d.destiny:
                              if card in destiny["USE_CARDS"]:
                                 db.updateVaultNoFilter({'OWNER': user_is_validated['DISNAME']},{'$addToSet':{'DESTINY': destiny}})
                                 message = f"**DESTINY AWAITS!**\n**{destiny['NAME']}** has been added to your vault."    
                                 await ctx.send(message)      
                        nCard = db.updateUserNoFilter({'DISNAME': str(ctx.author)}, {'$set': {'CARD': 'Clefairy', 'TITLE': 'Reborn King', 'ARM':'Kings Glaive'}})  
                        db.updateUserNoFilter({'DISNAME': str(ctx.author)}, {'$set': {'PET': 'Chick'}}) 
                        db.updateUserNoFilter({'DISNAME': str(ctx.author)}, {'$set': {'CROWN_TALES': ['']}}) 
                        db.updateUserNoFilter({'DISNAME': str(ctx.author)}, {'$set': {'DUNGEONS': ['']}}) 
                        db.updateUserNoFilter({'DISNAME': str(ctx.author)}, {'$set': {'BOSS_WINS': ['']}}) 
                        nRebirth = db.updateUserNoFilter(query, {'$inc': {'REBIRTH': 1 }}) 
                        await ctx.send(f"You are now Rebirth Level: {user_is_validated['REBIRTH'] + 1}")     
                  elif rLevel == 4:
                     card_level_list = vault['CARD_LEVELS']
                     owned_cards = []
                     for card in card_level_list:
                        owned_cards.append(card['CARD'])
                     if 'Stain' not in owned_cards:
                        card_level_list.append({'CARD': 'Stain', 'LVL': 0, 'TIER': 1, 'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0})

                     if 'Onix' not in owned_cards:
                        card_level_list.append({'CARD': 'Onix', 'LVL': 0, 'TIER': 1, 'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0})

                     if 'Xayah And Rakan' not in owned_cards:
                        card_level_list.append({'CARD': 'Xayah And Rakan', 'LVL': 0, 'TIER': 1, 'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0})
                        
                     delete = db.deleteVault(vault)            
                     vault = db.createVault(data.newVault({'OWNER' : user_is_validated['DISNAME'], 'CARDS': ['Stain','Onix','Xayah And Rakan'], 'TITLES': ['Reborn Legend'], 'ARMS': ['Legendary Weapon'], 'DECK': [{'CARD': 'Stain', 'TITLE': 'Reborn Legend', 'ARM': 'Legendary Weapon', 'PET': 'Chick'}, {'CARD': 'Onix', 'TITLE': 'Reborn Legend', 'ARM': 'Legendary Weapon', 'PET': 'Chick'}, {'CARD': 'Xayah And Rakan', 'TITLE': 'Reborn Legend', 'ARM': 'Legendary Weapon', 'PET': 'Chick'}], 'PETS' : [{'NAME': 'Chick', 'LVL': 5, 'EXP': 0, 'Heal': 10, 'TYPE': 'HLT', 'BOND': 3, 'BONDEXP': 0, 'PATH': "https://res.cloudinary.com/dkcmq8o15/image/upload/v1622307902/Pets/chick.jpg"}], 'CARD_LEVELS': card_level_list}))         
                     if vault:
                        cardList = ['Stain', 'Onix', 'Xayah And Rakan'] 
                        for card in cardList:
                           for destiny in d.destiny:
                              if card in destiny["USE_CARDS"]:
                                 db.updateVaultNoFilter({'OWNER': user_is_validated['DISNAME']},{'$addToSet':{'DESTINY': destiny}})
                                 message = f"**DESTINY AWAITS!**\n**{destiny['NAME']}** has been added to your vault." 
                                 await ctx.send(message)        
                        nCard = db.updateUserNoFilter({'DISNAME': str(ctx.author)}, {'$set': {'CARD': 'Xayah And Rakan', 'TITLE': 'Reborn Legend', 'ARM':'Legendary Weapon'}})  
                        db.updateUserNoFilter({'DISNAME': str(ctx.author)}, {'$set': {'PET': 'Chick'}}) 
                        db.updateUserNoFilter({'DISNAME': str(ctx.author)}, {'$set': {'CROWN_TALES': ['']}}) 
                        db.updateUserNoFilter({'DISNAME': str(ctx.author)}, {'$set': {'DUNGEONS': ['']}}) 
                        db.updateUserNoFilter({'DISNAME': str(ctx.author)}, {'$set': {'BOSS_WINS': ['']}}) 
                        nRebirth = db.updateUserNoFilter(query, {'$inc': {'REBIRTH': 1 }}) 
                        await ctx.send(f"You are now Rebirth Level: {user_is_validated['REBIRTH'] + 1}")   
               else:
                  await ctx.send(f"Not enough :coin:!\nYou need {rebirthCost} to Rebirth:angel:", delete_after=5)
            else:
               await ctx.send("No Vault:angel:", delete_after=5)
         except:
            await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=3)
      else:
         await ctx.send(f"You are at full Rebirth\n:angel:Level: {user_is_validated['REBIRTH']} ", delete_after=5)
      
@bot.command()
@commands.check(validate_user)
async def purge(ctx, amount = 5):
   if ctx.author.guild_permissions.administrator == True:
      await ctx.channel.purge(limit=amount)
      await ctx.send(f"{amount} messages have been purged.")
   else:
      print(m.ADMIN_ONLY_COMMAND)

@bot.command()
@commands.check(validate_user)
async def fix(ctx, user: User):
   if ctx.author.guild_permissions.administrator == True:
      response = db.updateUserNoFilter({'DISNAME': str(user)}, {'$set': {'AVAILABLE': True}})
      await ctx.send(f"{user.mention} is fixed. ")
   else:
      print(m.ADMIN_ONLY_COMMAND)

@bot.event
async def daily_error_message(ctx,error):
   if isinstance(error, commands.CommandOnCooldown): # Checks Cooldown
      msg = 'You have already claimed your daily. Try again in {:.2f}s'.format(error.retry_after)
      await ctx.author.send(msg)

@bot.command(pass_context=True)
@commands.cooldown(1, 60*60*24, commands.BucketType.user)
async def daily(ctx):
   dailyamount = 550
   await bless(dailyamount, ctx.author)

   user_data = db.queryUser({'DISNAME': str(ctx.author)})
   user_completed_tales = user_data['CROWN_TALES']
   universes = db.queryAllUniverse()
   
   user_available_opponents = []

   for x in universes:
      for y in user_completed_tales:
          if y == x['PREREQUISITE']:
            user_available_opponents.append(x['CROWN_TALES'])

   opponents = [x for x in user_available_opponents for x in x]
   oppponent_len = len(opponents)
   q1 = random.randint(0, oppponent_len)
   q2 = random.randint(0, oppponent_len)
   q3 = random.randint(0, oppponent_len)

   quests = [{'OPPONENT': opponents[q1], 'TYPE': 'Tales', 'GOAL': 3, 'WINS': 0, 'REWARD': 500 },{'OPPONENT': opponents[q2], 'TYPE': 'Tales', 'GOAL': 5, 'WINS': 0, 'REWARD': 1000 }, {'OPPONENT': opponents[q3], 'TYPE': 'Dungeon', 'GOAL': 3, 'WINS': 0, 'REWARD': 1500 }]
   db.updateVaultNoFilter({'OWNER': str(ctx.author)}, {'$set': {'QUESTS': quests}})

   await ctx.send(f"Daily bonus :coin:{dailyamount} has been applied for {ctx.author.mention}!\nYour new quests are available!\n**use /quest to open the Quest Board**!")

@bot.command()
@commands.check(validate_user)
async def updatestock(ctx, args: int):
   if ctx.author.guild_permissions.administrator == True and args == 612232:
      try:
         c_resp = db.updateManyCards({"$set": {"STOCK": 100}})
         t_resp = db.updateManyTitles({"$set": {"STOCK": 100}})
         a_resp = db.updateManyArms({"$set": {"STOCK": 100}})
         await ctx.send("Stock has been updated. ")
      except Exception as e:
         await ctx.send(f"Stock unable to be updated: {e}")
   else:
      print(m.ADMIN_ONLY_COMMAND)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'Your Daily Reward is on cooldown! You can use it in {round(error.retry_after/3600)} hours!')


@slash.slash(name="Vs", description="How many times you defeated opponent", guild_ids=guild_ids)
@commands.check(validate_user)
async def vs(ctx, user: User, args1 ):

   aliases = [x for x in db.query_all_games() for x in x['ALIASES']]
   game = {}
   if args1 in aliases:
      game_query = {'ALIASES': args1}
      game = db.queryGame(game_query)

      win_query = {'GAME': game['GAME'], 'WINNER.TEAM': [str(ctx.author)], 'LOSER.TEAM': [str(user)]}
      win_count = 0
      win_sessions = db.querySessionForUser(win_query)
      for x in win_sessions:
         win_count +=1

      loss_query = {'GAME': game['GAME'], 'WINNER.TEAM': [str(user)], 'LOSER.TEAM': [str(ctx.author)]}
      loss_count = 0
      loss_sessions = db.querySessionForUser(loss_query)
      for x in loss_sessions:
         loss_count +=1

      total_games = win_count + loss_count
      if win_count > 0:
         message = f"{str(ctx.author.mention)} has defeated {str(user.mention)} {win_count} out of {total_games} matches in {game['GAME']}!"
      else:
         message = f"{str(ctx.author.mention)} has never defeated {str(user.mention)} in {game['GAME']}!"

      if total_games == 0:
         message = "You two have not played each other. "
      await ctx.send(message)
   else:
      await ctx.send(m.GAME_NOT_DETECTED, delete_after=5)

async def DM(ctx, user : User, m,  message=None):
    message = message or "This Message is sent via DM"
    await user.send(m)

async def bless(amount, user):
   blessAmount = amount
   posBlessAmount = 0 + abs(int(blessAmount))
   query = {'DISNAME': str(user)}
   vaultOwner = db.queryUser(query)
   if vaultOwner:
      vault = db.queryVault({'OWNER' : vaultOwner['DISNAME']})
      update_query = {"$inc": {'BALANCE': posBlessAmount}}
      db.updateVaultNoFilter(vault, update_query)
   else:
      print("cant find vault")

async def curse(amount, user):
      curseAmount = amount
      negCurseAmount = 0 - abs(int(curseAmount))
      query = {'DISNAME': str(user)}
      vaultOwner = db.queryUser(query)
      if vaultOwner:
         vault = db.queryVault({'OWNER' : vaultOwner['DISNAME']})
         update_query = {"$inc": {'BALANCE': int(negCurseAmount)}}
         db.updateVaultNoFilter(vault, update_query)
      else:
         print("cant find vault")

@slash.slash(name="Trade", description="Trade Cards, Titles, Arms, and Pets", guild_ids=guild_ids)
@commands.check(validate_user)
async def trade(ctx, user2: User, item: str):
   user = db.queryUser({'DISNAME': str(ctx.author)})
   traded_to = db.queryUser({'DISNAME': str(user2)})
   p1_trade_item = item
   p1_vault = db.queryVault({'OWNER' : str(ctx.author)})
   p1_card_levels = p1_vault['CARD_LEVELS']
   p1_cards = p1_vault['CARDS']
   p1_titles = p1_vault['TITLES']
   p1_arms = p1_vault['ARMS']
   p1_pets = p1_vault['PETS']
   p1_balance = p1_vault['BALANCE']
   p1_owned_destinies = []
   for destiny in p1_vault['DESTINY']:
      p1_owned_destinies.append(destiny['NAME'])
   
   p1_active_pet = {}
   p1_pet_names = []
   for pet in p1_pets:
         p1_pet_names.append(pet['NAME'])
         if pet['NAME'] == p1_trade_item:
            pet_ability = list(pet.keys())[3]
            pet_ability_power = list(pet.values())[3]
            p1_active_pet = {'NAME': pet['NAME'], 'LVL': pet['LVL'], 'EXP': pet['EXP'], pet_ability: pet_ability_power, 'TYPE': pet['TYPE'], 'BOND': 0, 'BONDEXP': 0, 'PATH': pet['PATH']}


   p2_vault = db.queryVault({'OWNER' : str(user2)})
   p2_card_levels = p2_vault['CARD_LEVELS']
   p2_cards = p2_vault['CARDS']
   p2_titles = p2_vault['TITLES']
   p2_arms = p2_vault['ARMS']
   p2_pets = p2_vault['PETS']
   p2_balance = p2_vault['BALANCE']
   p2_trade_item = ""
   p2_owned_destinies = []
   for destiny in p2_vault['DESTINY']:
      p2_owned_destinies.append(destiny['NAME'])

   p2_pet_names = []
   for pet in p2_pets:
         p2_pet_names.append(pet['NAME'])


   commence = False

   if p1_trade_item not in p1_cards and p1_trade_item not in p1_titles and p1_trade_item not in p1_arms and p1_trade_item not in p1_pet_names and p1_trade_item not in p2_pet_names:
      await ctx.send("You do not own this item.")
      return
   else:

      if (p1_trade_item == user['CARD']) or (p1_trade_item == user['TITLE']) or (p1_trade_item == user['ARM']) or (p1_trade_item == user['PET']):
            await ctx.send("You cannot trade an equipped item.")
            return

      await ctx.send(f"{user2.mention}, what will you trade for {ctx.author.mention}'s {p1_trade_item}?")

      def check(msg):
         if p1_trade_item in p1_pet_names:
            return msg.author == user2 and msg.content in p2_pet_names and msg.content not in p1_cards and msg.content not in p1_titles and msg.content not in p1_arms and msg.content not in p1_pet_names
         else:
            return msg.author == user2 and msg.content in p2_cards or msg.content in p2_titles or msg.content in p2_arms or msg.content in p2_pet_names and msg.content not in p1_cards and msg.content not in p1_titles and msg.content not in p1_arms and msg.content not in p1_pet_names

      try:
         msg = await bot.wait_for('message', timeout=20.0, check=check)
         p2_trade_item = msg.content

         p2_active_pet = {}
         p2_pet_names = []
         for pet in p2_pets:
               p2_pet_names.append(pet['NAME'])
               if pet['NAME'] == p2_trade_item:
                  pet_ability = list(pet.keys())[3]
                  pet_ability_power = list(pet.values())[3]
                  p2_active_pet = {'NAME': pet['NAME'], 'LVL': pet['LVL'], 'EXP': pet['EXP'], pet_ability: pet_ability_power, 'TYPE': pet['TYPE'], 'BOND': 0, 'BONDEXP': 0, 'PATH': pet['PATH']}

         if (p2_trade_item == user['CARD']) or (p2_trade_item == user['TITLE']) or (p2_trade_item == user['ARM']) or (p2_trade_item == user['PET']):
            await ctx.send("You cannot trade an equipped item.")
            return

         commence = True
      except:
         await ctx.send("Please, triple check your vaults before making a trade. ")
         return

      if commence:
         accept = await ctx.send(f"{ctx.author.mention} do you accept {user2.mention}'s {p2_trade_item}?")
         emojis = ['👍', '👎']
         for emoji in emojis:
            await accept.add_reaction(emoji)

         def check(reaction, user):
            return user == ctx.author and ((str(reaction.emoji) == '👍') or (str(reaction.emoji) == '👎'))

         try:
            reaction, user = await bot.wait_for('reaction_add', timeout=8.0, check=check)
            if str(reaction.emoji) == '👎':
               await ctx.send("Trade ended.")
               return

            if p2_trade_item in p2_arms:
               db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$pull':{'ARMS': str(p1_trade_item)}})
               response = db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$addToSet':{'ARMS': str(p2_trade_item)}})
               await ctx.send(f"{p2_trade_item} has been added to {ctx.author.mention}'s vault: ARMS")
            elif p2_trade_item in p2_titles:
               db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$pull':{'TITLES': str(p1_trade_item)}})
               response = db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$addToSet':{'TITLES': str(p2_trade_item)}})
               await ctx.send(f"{p2_trade_item} has been added to {ctx.author.mention}'s vault: TITLES")
            elif p2_trade_item in p2_cards:
               # CARD_LEVEL Configuration 
               card_2 = db.queryCard({'NAME': str(p2_trade_item)})
               card_2_uni = db.queryUniverse({'TITLE': card_2['UNIVERSE']})
               card_2_tier = card_2_uni['TIER']
               update_query = {'$addToSet': {'CARD_LEVELS': {'CARD': str(p2_trade_item), 'LVL': 0, 'TIER': int(card_2_tier), 'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0}}}
               card_2_level_exist = False
               for card in p1_card_levels:
                  if card['CARD'] == str(p2_trade_item):
                     card_2_level_exist = True
               if card_2_level_exist == False:
                  vault_query = {'OWNER' : str(ctx.author)}
                  response = db.updateVaultNoFilter(vault_query, update_query)

               db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$pull':{'CARDS': str(p1_trade_item)}})
               response = db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$addToSet':{'CARDS': str(p2_trade_item)}})

               for destiny in d.destiny:
                  if p2_trade_item in destiny["USE_CARDS"] and destiny['NAME'] not in p1_owned_destinies:
                     db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$addToSet':{'DESTINY': destiny}})
                     await ctx.send(f"**DESTINY AWAITS!**\n**{destiny['NAME']}** has been added to your vault.")

               db.updateUserNoFilter({'DISNAME': str(ctx.author)}, {'$set': {'CARD': str(p2_trade_item)}})
               await ctx.send(f"{p2_trade_item} has been added to {ctx.author.mention}'s vault: CARDS")
            elif p2_trade_item in p2_pet_names:
               db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$pull':{'PETS':{'NAME': str(p1_trade_item)}}})
               response = db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$addToSet':{'PETS': p2_active_pet}})
               db.updateUserNoFilter({'DISNAME': str(ctx.author)}, {'$set': {'PET': p2_active_pet['NAME']}})
               await ctx.send(f"{p2_trade_item} has been added to {ctx.author.mention}'s vault: PETS")

            if p1_trade_item in p1_arms:
               db.updateVaultNoFilter({'OWNER': str(user2)},{'$pull':{'ARMS': str(p2_trade_item)}})
               response = db.updateVaultNoFilter({'OWNER': str(user2)},{'$addToSet':{'ARMS': str(p1_trade_item)}})
               await ctx.send(f"{p1_trade_item} has been added to {user2.mention}'s vault: ARMS")
            elif p1_trade_item in p1_titles:
               db.updateVaultNoFilter({'OWNER': str(user2)},{'$pull':{'TITLES': str(p2_trade_item)}})
               response = db.updateVaultNoFilter({'OWNER': str(user2)},{'$addToSet':{'TITLES': str(p1_trade_item)}})
               await ctx.send(f"{p1_trade_item} has been added to {user2.mention}'s vault: TITLES")
            elif p1_trade_item in p1_cards:
               # CARD_LEVEL Configuration 
               card_1 = db.queryCard({'NAME': str(p1_trade_item)})
               card_1_uni = db.queryUniverse({'TITLE': card_1['UNIVERSE']})
               card_1_tier = card_1_uni['TIER']
               cupdate_query = {'$addToSet': {'CARD_LEVELS': {'CARD': str(p1_trade_item), 'LVL': 0, 'TIER': int(card_1_tier), 'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0}}}
               card_1_level_exist = False
               for card in p2_card_levels:
                  if card['CARD'] == str(p1_trade_item):
                     card_1_level_exist = True
               if card_1_level_exist == False:
                  cvault_query = {'OWNER' : str(user2)}
                  response = db.updateVaultNoFilter(cvault_query, cupdate_query)

               db.updateVaultNoFilter({'OWNER': str(user2)},{'$pull':{'CARDS': str(p2_trade_item)}})
               response = db.updateVaultNoFilter({'OWNER': str(user2)},{'$addToSet':{'CARDS': str(p1_trade_item)}})

               for destiny in d.destiny:
                  if p1_trade_item in destiny["USE_CARDS"] and destiny['NAME'] not in p2_owned_destinies:
                     db.updateVaultNoFilter({'OWNER': str(user2)},{'$addToSet':{'DESTINY': destiny}})
                     await ctx.send(f"**DESTINY AWAITS!**\n**{destiny['NAME']}** has been added to your vault.")

               db.updateUserNoFilter({'DISNAME': str(user2)}, {'$set': {'CARD': str(p1_trade_item)}})
               await ctx.send(f"{p1_trade_item} has been added to {user2.mention}'s vault: CARDS")
            elif p1_trade_item in p1_pet_names:
               db.updateVaultNoFilter({'OWNER': str(user2)},{'$pull':{'PETS':{'NAME': str(p2_trade_item)}}})
               response = db.updateVaultNoFilter({'OWNER': str(user2)},{'$addToSet':{'PETS': p1_active_pet}})
               db.updateUserNoFilter({'DISNAME': str(user2)}, {'$set': {'PET': p1_active_pet['NAME']}})
               await ctx.send(f"{p1_trade_item} has been added to {user2.mention}'s vault: PETS")

         except:
            await ctx.send("Trade ended. ")

@slash.slash(name="Sell", description="Sell Cards, Titles, Arms, and Pets", guild_ids=guild_ids)
@commands.check(validate_user)
async def sell(ctx, user2: User, item: str):
   user = db.queryUser({'DISNAME': str(ctx.author)})
   p1_trade_item = item
   p1_vault = db.queryVault({'OWNER' : str(ctx.author)})
   p1_card_levels = p1_vault['CARD_LEVELS']
   p1_cards = p1_vault['CARDS']
   p1_titles = p1_vault['TITLES']
   p1_arms = p1_vault['ARMS']
   p1_pets = p1_vault['PETS']
   p1_balance = p1_vault['BALANCE']
   
   
   p1_active_pet = {}
   p1_pet_names = []
   for pet in p1_pets:
         p1_pet_names.append(pet['NAME'])
         if pet['NAME'] == p1_trade_item:
            pet_ability = list(pet.keys())[3]
            pet_ability_power = list(pet.values())[3]
            p1_active_pet = {'NAME': pet['NAME'], 'LVL': pet['LVL'], 'EXP': pet['EXP'], pet_ability: pet_ability_power, 'TYPE': pet['TYPE'], 'BOND': 0, 'BONDEXP': 0, 'PATH': pet['PATH']}

   p2_vault = db.queryVault({'OWNER' : str(user2)})
   p2_card_levels = p2_vault['CARD_LEVELS']
   p2_cards = p2_vault['CARDS']
   p2_titles = p2_vault['TITLES']
   p2_arms = p2_vault['ARMS']
   p2_pets = p2_vault['PETS']
   p2_balance = p2_vault['BALANCE']
   p2_trade_item = ""
   owned_destinies = []
   for destiny in p2_vault['DESTINY']:
      owned_destinies.append(destiny['NAME'])

   p2_pet_names = []
   for pet in p2_pets:
         p2_pet_names.append(pet['NAME'])

   commence = False

   if p1_trade_item in p1_cards and len(p1_cards) == 1:
      await ctx.send("You cannot sell your only card.")
   elif p1_trade_item in p1_arms and len(p1_arms) == 1:
      await ctx.send("You cannot sell your only arm.")
   elif p1_trade_item in p1_titles and len(p1_titles) == 1:
      await ctx.send("You cannot sell your only title.")
   elif p1_trade_item in p1_pet_names and len(p1_pet_names) == 1:
      await ctx.send("You cannot sell your only Pet.")
   elif p1_trade_item in p2_pet_names:
      await ctx.send(f"{user2.mention} already owns a {p1_trade_item}!.")  
   else:

      if (p1_trade_item == user['CARD']) or (p1_trade_item == user['TITLE']) or (p1_trade_item == user['ARM']) or (p1_trade_item == user['PET']):
            await ctx.send("You cannot sell an equipped item.")
            return

      if p1_trade_item not in p1_cards and p1_trade_item not in p1_titles and p1_trade_item not in p1_arms and p1_trade_item not in p1_pet_names:
         await ctx.send("You do not own this item.")
         return
      else:
         await ctx.send(f"{user2.mention} how much are you willing to pay for {ctx.author.mention}'s {p1_trade_item}?")

         def check(msg):
            return msg.author == user2 and (int(msg.content) - int(p2_balance)) <= 0
         try:
            msg = await bot.wait_for('message', timeout=15.0, check=check)
            p2_trade_item = msg.content
            commence = True
         except:
            await ctx.send("Please, triple check your balance before making a trade. ")
            return

         if commence:
            accept = await ctx.send(f"{ctx.author.mention} do you accept {user2.mention}'s offer?")
            emojis = ['👍', '👎']
            for emoji in emojis:
               await accept.add_reaction(emoji)

            def check(reaction, user):
               return user == ctx.author and ((str(reaction.emoji) == '👍') or (str(reaction.emoji) == '👎'))

            try:
               reaction, user = await bot.wait_for('reaction_add', timeout=20.0, check=check)
               
               if str(reaction.emoji) == '👎':
                  await ctx.send("Sell ended.")
                  return

               if p1_trade_item in p1_arms:
                  db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$pull':{'ARMS': str(p1_trade_item)}})
                  await bless(p2_trade_item, ctx.author)
                  await ctx.send(f"{p2_trade_item} has been added to {ctx.author.mention}'s balance.")
               elif p1_trade_item in p1_titles:
                  db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$pull':{'TITLES': str(p1_trade_item)}})
                  await bless(p2_trade_item, ctx.author)
                  await ctx.send(f"{p2_trade_item} has been added to {ctx.author.mention}'s balance.")
               elif p1_trade_item in p1_cards:
               
                  db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$pull':{'CARDS': str(p1_trade_item)}})
                  await bless(p2_trade_item, ctx.author)
                  await ctx.send(f"{p2_trade_item} has been added to {ctx.author.mention}'s balance.")
               elif p1_trade_item in p1_pet_names:
                  db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$pull':{'PETS': {'NAME': str(p1_trade_item)}}})
                  await bless(p2_trade_item, ctx.author)
                  await ctx.send(f"{p2_trade_item} has been added to {ctx.author.mention}'s balance.")


               if p1_trade_item in p1_arms:
                  await curse(p2_trade_item, user2)
                  response = db.updateVaultNoFilter({'OWNER': str(user2)},{'$addToSet':{'ARMS': str(p1_trade_item)}})
                  await ctx.send(f"{p1_trade_item} has been added to {user2.mention}'s vault: ARMS")
               elif p1_trade_item in p1_titles:
                  await curse(p2_trade_item, user2)
                  response = db.updateVaultNoFilter({'OWNER': str(user2)},{'$addToSet':{'TITLES': str(p1_trade_item)}})
                  await ctx.send(f"{p1_trade_item} has been added to {user2.mention}'s vault: TITLES")
               elif p1_trade_item in p1_cards:
                  await curse(p2_trade_item, user2)
                  # CARD_LEVEL Configuration 
                  card_1 = db.queryCard({'NAME': str(p1_trade_item)})
                  card_1_uni = db.queryUniverse({'TITLE': card_1['UNIVERSE']})
                  card_1_tier = card_1_uni['TIER']
                  cupdate_query = {'$addToSet': {'CARD_LEVELS': {'CARD': str(p1_trade_item), 'LVL': 0, 'TIER': int(card_1_tier), 'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0}}}
                  card_1_level_exist = False
                  for card in p2_card_levels:
                     if card['CARD'] == str(p1_trade_item):
                        card_1_level_exist = True
                  if card_1_level_exist == False:
                     cvault_query = {'OWNER' : str(user2)}
                     response = db.updateVaultNoFilter(cvault_query, cupdate_query)

                  response = db.updateVaultNoFilter({'OWNER': str(user2)},{'$addToSet':{'CARDS': str(p1_trade_item)}})

                  for destiny in d.destiny:
                     if p1_trade_item in destiny["USE_CARDS"] and destiny['NAME'] not in owned_destinies:
                        db.updateVaultNoFilter({'OWNER': str(user2)},{'$addToSet':{'DESTINY': destiny}})
                        await ctx.send(f"**DESTINY AWAITS!**\n**{destiny['NAME']}** has been added to your vault.")

                  await ctx.send(f"{p1_trade_item} has been added to {user2.mention}'s vault: CARDS")
               elif p1_trade_item in p1_pet_names:
                  await curse(p2_trade_item, user2)
                  selected_pet = db.queryPet({"PET": p1_trade_item})
                  pet_ability_name = list(selected_pet['ABILITIES'][0].keys())[0]
                  pet_ability_power = list(selected_pet['ABILITIES'][0].values())[0]
                  pet_ability_type = list(selected_pet['ABILITIES'][0].values())[1]

                  response = db.updateVaultNoFilter({'OWNER': str(user2)},{'$addToSet':{'PETS': p1_active_pet}})
                  #response = db.updateVaultNoFilter({'OWNER': str(user2)},{'$addToSet':{'PETS': str(p1_trade_item)}})
                  await ctx.send(f"{p1_trade_item} has been added to {user2.mention}'s vault: PETS")

            except:
               await ctx.send("Trade ended. ")

@slash.slash(name="Gift", description="Give money to friend", guild_ids=guild_ids)
@commands.check(validate_user)
async def gift(ctx, user2: User, amount):
   vault = db.queryVault({'OWNER': str(ctx.author)})
   balance = vault['BALANCE']
   
   if balance <= int(amount):
      await ctx.send("You do not have that amount to gift.")
   else:
      await bless(int(amount), user2)
      await curse(int(amount), ctx.author)
      await ctx.send(f":coin:{amount} has been gifted to {user2.mention}.")
      return
   
@slash.slash(name="Donate", description="Donate money to Guild", guild_ids=guild_ids)
@commands.check(validate_user)
async def donate(ctx, amount, *args):
   vault = db.queryVault({'OWNER': str(ctx.author)})
   balance = vault['BALANCE']
   team = " ".join([*args])
   query = {'TNAME': str(team)}
   team_data = db.queryTeam(query)
   if team_data:
      if balance <= int(amount):
         await ctx.send("You do not have that amount to donate.")
      else:
         await blessteam(int(amount), team)
         await curse(int(amount), ctx.author)
         await ctx.send(f":coin:{amount} has been gifted to {team}.")
         return
   else:
      await ctx.send(f"Team: {team} does not exist")
      
@slash.slash(name="Invest", description="Invest money in your Family", guild_ids=guild_ids)
@commands.check(validate_user)
async def invest(ctx, amount):
   user = db.queryUser({'DISNAME': str(ctx.author)})
   family = db.queryFamily({'HEAD': user['FAMILY']})
   vault = db.queryVault({'OWNER': str(ctx.author)})
   balance = vault['BALANCE']
   if family:
      if balance <= int(amount):
         await ctx.send("You do not have that amount to invest.")
      else:
         await blessfamily_Alt(int(amount), user['FAMILY'])
         await curse(int(amount), ctx.author)
         await ctx.send(f":coin:{amount} invested into {user['NAME']}'s Family'.")
         return
   else:
      await ctx.send(f"Family does not exist")

@slash.slash(name="Pay", description="Pay a Team Member", guild_ids=guild_ids)
@commands.check(validate_user)
async def pay(ctx, user2: User, amount):
   user = db.queryUser({'DISNAME': str(ctx.author)})
   team = db.queryTeam({'TNAME': user['TEAM']})
   
   if user['TEAM'] == 'PCG' or user['DISNAME'] != team['OWNER']:
      await ctx.send("You must be owner of team to pay members. ")
      return

   if str(user2) not in team['MEMBERS']:
      await ctx.send("You can only pay team members. ")
      return
      

   balance = team['BANK']
   if balance <= int(amount):
      await ctx.send("You do not have that amount to pay.")
   else:
      await bless(int(amount), user2)
      await curseteam(int(amount), team['TNAME'])
      await ctx.send(f":coin:{amount} has been paid to {user2.mention}.")
      return

async def blessteam(amount, team):
   blessAmount = amount
   posBlessAmount = 0 + abs(int(blessAmount))
   query = {'TNAME': str(team)}
   team_data = db.queryTeam(query)
   if team_data:
      update_query = {"$inc": {'BANK': posBlessAmount}}
      db.updateTeam(query, update_query)
   else:
      print("Cannot find Team")

async def curseteam(amount, team):
      curseAmount = amount
      negCurseAmount = 0 - abs(int(curseAmount))
      query = {'TNAME': str(team)}
      team_data = db.queryTeam(query)
      if team_data:
         update_query = {"$inc": {'BANK': int(negCurseAmount)}}
         db.updateTeam(query, update_query)
      else:
         print("cant find team")


@slash.slash(name="Allowance", description="Gift Family member an allowance", guild_ids=guild_ids)
@commands.check(validate_user)
async def allowance(ctx, user2: User, amount):
   user = db.queryUser({'DISNAME': str(ctx.author)})
   family = db.queryFamily({'HEAD' : user['FAMILY']})
   if user['FAMILY'] == 'PCG' or (user['FAMILY'] != user['DISNAME'] and user['DISNAME'] != family['PARTNER']):
      await ctx.send("You must be the Head of a Household or Partner to give allowance. ")
      return

   family = db.queryFamily({'HEAD': user['FAMILY']})
   kids = family['KIDS']

   if str(user2) not in family['KIDS'] and str(user2) not in family['PARTNER'] and str(user2) not in family['HEAD']:
      await ctx.send("You can only give allowance family members. ")
      return
   balance = family['BANK']
   if balance <= int(amount):
      await ctx.send("You do not have that amount saved.")
   else:
      await bless(int(amount), user2)
      await cursefamily(int(amount), family['HEAD'])
      await ctx.send(f":coin:{amount} has been gifted to {user2.mention}.")
      return

async def blessfamily(amount, family):
   blessAmount = amount
   posBlessAmount = 0 + abs(int(blessAmount))
   query = {'HEAD': str(family)}
   family_data = db.queryFamily(query)
   if family_data:
      house = family_data['HOUSE']
      house_data = db.queryHouse({'HOUSE': house})
      multiplier = house_data['MULT']
      posBlessAmount = posBlessAmount * multiplier
      update_query = {"$inc": {'BANK': posBlessAmount}}
      db.updateFamily(query, update_query)
   else:
      print("Cannot find family")
      
async def blessfamily_Alt(amount, family):
   blessAmount = amount
   posBlessAmount = 0 + abs(int(blessAmount))
   query = {'HEAD': str(family)}
   family_data = db.queryFamily(query)
   if family_data:
      house = family_data['HOUSE']
      house_data = db.queryHouse({'HOUSE': house})
      posBlessAmount = posBlessAmount
      update_query = {"$inc": {'BANK': posBlessAmount}}
      db.updateFamily(query, update_query)
   else:
      print("Cannot find family")

async def cursefamily(amount, family):
      curseAmount = amount
      negCurseAmount = 0 - abs(int(curseAmount))
      query = {'HEAD': str(family)}
      family_data = db.queryFamily(query)
      if family_data:
         print(family_data)
         update_query = {"$inc": {'BANK': int(negCurseAmount)}}
         db.updateFamily(query, update_query)
      else:
         print("cant find family")

@slash.slash(name="Traits", description="See full list of Universe Traits", guild_ids=guild_ids)
@commands.check(validate_user)
async def traits(ctx):
   traits = ut.traits
   traitmessages = []
   for trait in traits:
      traitmessages.append(f"_{trait['NAME']}_\n**{trait['EFFECT']}**: {trait['TRAIT']}\n")

   embedVar = discord.Embed(title="Universe Traits", description="\n".join(traitmessages))

   await ctx.send(embed=embedVar)

@slash.slash(name="Resell", description="Sell items back to the shop", guild_ids=guild_ids)
@commands.check(validate_user)
async def resell(ctx, item: str):
   user = db.queryUser({'DISNAME': str(ctx.author)})
   p1_trade_item = item
   p1_vault = db.queryVault({'OWNER' : str(ctx.author)})
   p1_cards = p1_vault['CARDS']
   p1_titles = p1_vault['TITLES']
   p1_arms = p1_vault['ARMS']
   p1_balance = p1_vault['BALANCE']

   if p1_trade_item in p1_cards and len(p1_cards) == 1:
      await ctx.send("You cannot sell your only card.")
   elif p1_trade_item in p1_arms and len(p1_arms) == 1:
      await ctx.send("You cannot sell your only arm.")
   elif p1_trade_item in p1_titles and len(p1_titles) == 1:
      await ctx.send("You cannot sell your only title.")
   else:

      if p1_trade_item not in p1_cards and p1_trade_item not in p1_titles and p1_trade_item not in p1_arms:
         await ctx.send("You do not own this item.")
         return
      else:
         if p1_trade_item in p1_cards:
            card = db.queryCard({'NAME':str(p1_trade_item)})
            sell_price = card['PRICE'] * .07
         elif p1_trade_item in p1_titles:
            title = db.queryTitle({'TITLE': str(p1_trade_item)})
            sell_price = title['PRICE'] * .07
         elif p1_trade_item in p1_arms:
            arm = db.queryArm({'ARM': str(p1_trade_item)})
            sell_price = arm['PRICE'] * .07

         if (p1_trade_item == user['CARD']) or (p1_trade_item == user['TITLE']) or (p1_trade_item == user['ARM']):
            await ctx.send("You cannot resell an equipped item.")
            return

         accept = await ctx.send(f"{ctx.author.mention} are you willing to resell {p1_trade_item} for :coin: {round(sell_price)}?")
         emojis = ['👍', '👎']
         for emoji in emojis:
            await accept.add_reaction(emoji)

         def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '👍'

         try:
            reaction, user = await bot.wait_for('reaction_add', timeout=20.0, check=check)

            if p1_trade_item in p1_arms:
               db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$pull':{'ARMS': str(p1_trade_item)}})
               await bless(sell_price, ctx.author)
               await ctx.send(f"{p1_trade_item} has been resold for :coin: {round(sell_price)}.")
            elif p1_trade_item in p1_titles:
               db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$pull':{'TITLES': str(p1_trade_item)}})
               await bless(sell_price, ctx.author)
               await ctx.send(f"{p1_trade_item} has been resold for :coin: {round(sell_price)}.")
            elif p1_trade_item in p1_cards:
               db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$pull':{'CARDS': str(p1_trade_item)}})
               await bless(sell_price, ctx.author)
               await ctx.send(f"{p1_trade_item} has been resold for :coin: {round(sell_price)}.")

         except:
            await ctx.send("Resell ended. ")

# @bot.command()
# @commands.check(validate_user)
# async def addfield(ctx, collection, new_field, field_type):
#    if ctx.author.guild_permissions.administrator == True:

#       if field_type == 'string':
#          field_type = "N/A"
#       elif field_type == 'int':
#          field_type = 0
#       elif field_type == 'list':
#          field_type = []
#       elif field_type == 'bool':
#          field_type = False
      
#       if collection == 'cards':
#          response = db.updateManyCards({'$set': {new_field: field_type}})
#       elif collection == 'titles':
#          response = db.updateManyTitles({'$set': {new_field: field_type}})
#       elif collection == 'vaults':
#          response = db.updateManyVaults({'$set': {new_field: field_type}})
#       elif collection == 'users':
#          response = db.updateManyUsers({'$set': {new_field: field_type}})
#       elif collection == 'universe':
#          response = db.updateManyUniverses({'$set': {new_field: field_type}})
#       elif collection == 'boss':
#          response = db.updateManyBosses({'$set': {new_field: field_type}})
#       elif collection == 'arms':
#          response = db.updateManyArms({'$set': {new_field: field_type}})
#       elif collection == 'pets':
#          response = db.updateManyPets({'$set': {new_field: field_type}})
#       elif collection == 'teams':
#          response = db.updateManyTeams({'$set': {new_field: field_type}})
#    else:
#       print(m.ADMIN_ONLY_COMMAND)

# @bot.command()
# @commands.check(validate_user)
# async def sync(ctx):
#    all_vaults = db.queryAllVault()
#    players = []
#    vaults = []
#    try:
#       for vault in all_vaults:
#          player = vault['OWNER']
#          cards = vault['CARDS']
#          vault_query = {'OWNER' : player}
#          for card in cards:
#             resp = db.queryCard({'NAME': card})
#             universe = db.queryUniverse({'TITLE': resp['UNIVERSE']})
#             tier = universe['TIER']
#             update_query = {'$addToSet': {'CARD_LEVELS': {'CARD': card, 'LVL': 0, 'TIER': int(tier), 'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0}}}
#             db.updateVaultNoFilter(vault_query, update_query)
#    except Exception as e:
#       print(e)
   


   


@bot.command()
@commands.check(validate_user)
async def referred(ctx, user: User):
   referred = db.queryUser({"DISNAME": str(ctx.author)})
   if not referred['REFERRED']:
      resp = db.updateUserNoFilter({'DISNAME': str(ctx.author)}, {'$set': {'REFERRED': True, 'REFERRER': str(user)}})
      await bless(500, str(ctx.author))
      await bless(1000, str(user))
      await ctx.send(f"Congrats & Welcome newcomer! You were awarded :coin: 500 and {user.mention} was awarded :coin:1000.")
   else:
      await ctx.send("You're already referred!")

@slash.slash(name="Menu", description="Menu Options for things to do", guild_ids=guild_ids)
@commands.check(validate_user)
async def menu(ctx):
   try:
      response = db.queryAllMenu()
      profile, story, pvp, objectives = "", "", "", ""
      for menu in response:
         if menu['NAME'] == "Profile":
            profile = menu['PATH']
         if menu['NAME'] == "Story":
            story = menu['PATH']
         if menu['NAME'] == "PVP":
            pvp = menu['PATH']
         if menu['NAME'] == "Objectives":
            objectives = menu['PATH']

      embedVar1 = discord.Embed(title= f"Story Mode", description="Journey through Universes to defeat powerful foes to unlock vast new worlds, tough boss fights, and new possibilities!", colour=0x7289da)
      embedVar1.set_image(url=story)
      embedVar1.set_footer(text=f"use /crown for additional assistance")

      embedVar2 = discord.Embed(title= f"Profile Menu", description="View and Edit your Cards, Titles, Arms, and Pets to craft new builds and strategies.", colour=0x7289da)
      embedVar2.set_image(url=profile)
      # embedVar2.add_field(name="Help Navigation", value="*First Page: :track_previous:|Prev Page: :rewind:|\nNext Page: :fast_forward:| Last Page: :track_next:*")
      embedVar2.set_footer(text=f"use /crown for additional assistance")
      
      embedVar3 = discord.Embed(title= f"PVP Mode", description="Face off against friend or foe!", colour=0x7289da)
      embedVar3.set_image(url=pvp)
      # embedVar3.add_field(name="Help Navigation", value="*First Page: :track_previous:|Prev Page: :rewind:|\nNext Page: :fast_forward:| Last Page: :track_next:*")
      embedVar3.set_footer(text=f"use /crown for additional assistance")

      embedVar4 = discord.Embed(title= f"Crown Unlimited Menu", description="5 Primary Objectives of Crown Unlimited. Click arrow below to go to the next page!", colour=0x7289da)
      embedVar4.set_image(url=objectives)
      # embedVar4.add_field(name="Help Navigation", value="*First Page: :track_previous:|Prev Page: :rewind:|\nNext Page: :fast_forward:| Last Page: :track_next:*")
      embedVar4.set_footer(text=f"use /crown for additional assistance")

      paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
      paginator.add_reaction('⏮️', "first")
      paginator.add_reaction('⏪', "back")
      paginator.add_reaction('🔐', "lock")
      paginator.add_reaction('⏩', "next")
      paginator.add_reaction('⏭️', "last")
      embeds = [embedVar4, embedVar1,embedVar3, embedVar2]
      await paginator.run(embeds)
         
   except Exception as e:
      await ctx.send(f"Error has occurred: {e}")

# @bot.command()
# @commands.check(validate_user)
# async def newmenu(ctx):
#    try:
#       response = db.createMenu({'PATH': 'https://res.cloudinary.com/dkcmq8o15/image/upload/v1627880815/menu/Profile_Mode.jpg', 'NAME': 'Profile'})
#       await ctx.send("New menu added")
#    except Exception as e:
#       print(e)
#       return

if config('ENV') == "production":
   DISCORD_TOKEN = config('DISCORD_TOKEN_TEST')
else:
   DISCORD_TOKEN = config('DISCORD_TOKEN_FOR_TESTING')

bot.run(DISCORD_TOKEN)