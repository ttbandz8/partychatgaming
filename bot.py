from dataclasses import field
import wikipedia
from discord import player, team
from discord.ext.commands.errors import CommandOnCooldown
from discord.flags import Intents
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

intents = discord.Intents.all()
client = discord.Client()

if config('ENV') == "production":
   # PRODUCTION
   bot = commands.Bot(command_prefix=".", intents=intents)
else:
   # TEST
   bot = commands.Bot(command_prefix=",", intents=intents)

bot.remove_command("help")

@bot.group(invoke_without_command=True)
async def help(ctx):
   avatar="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Legend.png"

   embedVar1 = discord.Embed(title= f"Bot Commands", description=h.BOT_COMMANDS, colour=0x7289da)
   embedVar1.set_thumbnail(url=avatar)
   embedVar1.add_field(name="Help Navigation", value="*First Page: :track_previous:|Prev Page: :rewind:|\nNext Page: :fast_forward:| Last Page: :track_next:*")
   # embedVar1.set_footer(text=f".senpai - Text Bot Tutorial")

   embedVar2 = discord.Embed(title= f"Crown Unlimited Commands", description=h.CROWN_UNLIMITED_COMMANDS, colour=0x7289da)
   embedVar2.set_thumbnail(url=avatar)
   embedVar2.add_field(name="Help Navigation", value="*First Page: :track_previous:|Prev Page: :rewind:|\nNext Page: :fast_forward:| Last Page: :track_next:*")
   # embedVar2.set_footer(text=f".senpai - Text Bot Tutorial")

   paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
   paginator.add_reaction('⏮️', "first")
   paginator.add_reaction('⏪', "back")
   paginator.add_reaction('🔐', "lock")
   paginator.add_reaction('⏩', "next")
   paginator.add_reaction('⏭️', "last")
   embeds = [embedVar2, embedVar1]
   await paginator.run(embeds)

@bot.group(invoke_without_command=True)
async def enhance(ctx):
   avatar="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Legend.png"


   embedVar1 = discord.Embed(title= f":trident:ENHANCE Sets:",colour=0x7289da)
   embedVar1.set_thumbnail(url=avatar)
   embedVar1.add_field(name="`INCREASES`", value="`ATK` - Increase `ATK`\n\n`DEF` - Increase `DEF`\n\n`HLT` - Increase `HLT`\n\n`STAM` - Increase `STAM`\n\n")
   embedVar1.set_footer(text=f".help - Bot Help")

   embedVar2 = discord.Embed(title= f":trident:ENHANCE Sets:",colour=0x7289da)
   embedVar2.set_thumbnail(url=avatar)
   embedVar2.add_field(name="`STEALS`", value="`FLOG`- `ATK` Steal\n\n`WITHER`- `DEF` Steal\n\n`LIFE` - `LIFE` Steal\n\n`DRAIN` - `STAM` Steal\n\n")
   embedVar2.set_footer(text=f".help - Bot Help")


   embedVar3 = discord.Embed(title= f":trident:ENHANCE Sets:",colour=0x7289da)
   embedVar3.set_thumbnail(url=avatar)
   embedVar3.add_field(name="`SACRIFICE`", value="`RAGE` - Decrease `DEF`, Increase `ATK`\n\n`BRACE` - Decrease `ATK`, Increase `DEF`\n\n`BZRK` - Decrease `HLT`,  Increase `ATK`\n\n`CRYSTAL`- Decrease `HLT`, Increase `DEF`\n\n`GROWTH`- Decrease `MAXHLT`, Increase `STATS`\n\n")
   embedVar3.set_footer(text=f".help - Bot Help")

   embedVar4 = discord.Embed(title= f":trident:ENHANCE Sets:",colour=0x7289da)
   embedVar4.set_thumbnail(url=avatar)
   embedVar4.add_field(name="`TRADE`", value="`STANCE` - Swap `ATK` and `DEF`\n\n`CONFUSE` - Swap `OPP ATK` and  `OPP DEF`\n\n")
   embedVar4.set_footer(text=f".help - Bot Help")

   embedVar5 = discord.Embed(title= f":trident:ENHANCE Sets:",colour=0x7289da)
   embedVar5.set_thumbnail(url=avatar)
   embedVar5.add_field(name="`TIME`", value="`BLINK`  - Decrease  `STAM`, Increase `OPP STAM`\n\n`SLOW` - Decrease `STAM`, Swap `OPP STAM`\n\n`HASTE` - Increase `STAM`, Swap `OPP STAM`\n\n")
   embedVar5.set_footer(text=f".help - Bot Help")

   embedVar6 = discord.Embed(title= f":trident:ENHANCE Sets:",colour=0x7289da)
   embedVar6.set_thumbnail(url=avatar)
   embedVar6.add_field(name="`CONTROL`", value="`SOULCHAIN` - Both `PLAYERS` `STAM` = \n\n`GAMBLE` - Both `PLAYERS` `HEALTH` =\n\n`FEAR` - Decrease `HLT`, Decrease `OPP ATK` & `OPP DEF`")
   embedVar6.set_footer(text=f".help - Bot Help")

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
   **GROWTH:** Lower Max Health, Increase Defense and Attack based on 50% of AP Percentage
   **STANCE:** Swaps your ATK and your DEF, and gives you additional DEF based on AP Value
   **CONFUSE:** Swaps ATK and DEF of opponent and saps additional DEF based on AP Value
   **BLINK:** Decreases Your Stamina by AP Value and gives opponent Stamina by AP Value
   **SLOW:** Increases Your Stamina by AP Value, Decreases your Opponent Stamina by AP Value, then swaps your and your opponents Stamina
   **HASTE:** Decreases your opponent Stamina, Increases your stamina, swap your and your opponent stamina
   **SOUL:** CHAIN - Make you and your opponent Stamina the same based on AP Value
   **GAMBLE:** Make you and your opponent health the same based on AP Value
   **FEAR:** Lower your Health by AP Percentage, Lower your opponent ATK and DEF by AP Percentage
   **WAVE:** Deals AP * Turn Count Damage to Opponent that decreases as the Turn Count increases
   **BLAST:** Deals AP * Turn Count Damage to Opponent that increases as the Turn Count increases
   **CREATION:** Increases AP * Turn Count Max Health & Health that decreases as the Turn Count increases
   **DESTRUCTION:** Decreases AP * Turn Count Max Health that increases as the Turn Count increases
   """) ,colour=0x7289da)
   embedVar7.set_thumbnail(url=avatar)
   embedVar7.set_footer(text=f".help - Bot Help")

   paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
   paginator.add_reaction('⏮️', "first")
   paginator.add_reaction('⏪', "back")
   paginator.add_reaction('🔐', "lock")
   paginator.add_reaction('⏩', "next")
   paginator.add_reaction('⏭️', "last")
   embeds = [embedVar1, embedVar2, embedVar3, embedVar4, embedVar5, embedVar6, embedVar7]
   await paginator.run(embeds)

@bot.group(invoke_without_command=True)
async def crown(ctx):
   avatar="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Legend.png"


   embedVar1 = discord.Embed(title= f":crown: Crown Unlimited",colour=0x7289da)
   embedVar1.set_thumbnail(url=avatar)
   embedVar1.add_field(name="About The Game!", value=textwrap.dedent(f"""\
   Crown Unlimited is a multiplatform card game featuring universes from your favorite series!

   Explore Tales, Dungeons, and Bosses solo, or with your friend!
   """))

   embedVar2 = discord.Embed(title= f":crown: Getting Started", description=textwrap.dedent(f"""\
   Each player starts with 3 cards from the 3 Starter Universes to begin their journey.

   The starting universes are _My Hero Academia_, _Kanto Region_, and _League Of Legends_.

   Compete in Single Player and Multiplayer _Tales_, _Dungeons_, and _Bosses_ to earn :coin: to buy and equip better Items and unlock new worlds!
   """), colour=0x7289da)
   embedVar2.set_thumbnail(url=avatar)

   embedVar3 = discord.Embed(title= f":crown: Card Mechanics", description=textwrap.dedent(f"""\
   **Card Stats** 
   Health (HLT) Stamina (STAM) Attack (ATK) Defense(DEF)

   **Cards have 5 Elements** 
   3 Abilities
   1 Enhancer
   1 Unique Passive

   **Abilities**
   Abilities inflict damage on the opponent.
   Each ability has a corresponding number when selecting from the Movelist
   **1:** Basic Attack _uses 10 stamina_
   **2:** Special Attack _uses 30 stamina_
   **3:** Ultimate Attack _uses 80 stamina_

   **Enhancer**
   Enhancers can either boost your stats or inflict status effects on your opponent. Use .enhance for full list of Enhancers and their effects.
   **4:** Enhancer

   **Unique Passive**
   Unique Passives are Enhancers that take effect at the beginning of the game, no player action needed.

   """), colour=0x7289da)
   embedVar3.set_thumbnail(url=avatar)

   embedVar4 = discord.Embed(title= f":crown: Titles, Arms, and Pets", description=textwrap.dedent(f"""\
   **Titles** & **Arms** 
   Modify your or your opponents stats prior to battle by applying _Enhancers_ at the beginning of the match.

   **Pets**
   Can assist during battle with an Enhancer

   Mix and Match Titles, Arms and Pet passives to gain tactical advantage!

   Match Your Titles and Arms to your Card Universe To gain the **Universe Buff**
   **Universe Buff** + 100 Health , 20 ATK & 20 DEF

   **Destiny Buff** Destiny Cards gain an additional + 50 Health, 5 ATK and 5 DEF
   """) ,colour=0x7289da)
   embedVar4.set_thumbnail(url=avatar)

   embedVar5 = discord.Embed(title= f":crown: Battle Mechanics", description=textwrap.dedent(f"""\
   Players take turns dealing damage using one of their 3 Abilities
   
   Stamina costs are standard across all Cards _check Cards page for details_
   
   **Recovery**
   When Players have used all of their Stamina they enter **Focus State**
   
   **Focus State** sacrifices a turn to Level up stats, increase their Stamina to 90, and recover some health.

   The Match is over when a players Health reaches 0
   """) ,colour=0x7289da)
   embedVar5.set_thumbnail(url=avatar)

   embedVar6 = discord.Embed(title= f":crown: Focus & Resolve", description=textwrap.dedent(f"""\
   Players can take advantage of Focus State to recover, as mentioned on the previous page.
   
   **Resolve**
   Once in Focus State players can enter 5 to Resolve!
   Resolved Characters transform to greatly increase attack and health while sacrificing defense
   Resolved characters can summon Pets to aid them in battle by entering 6

   **Pet Assistance!**
   Pet assistance is a free move and can be used each round in addition to a Card Abiltiy!
   """) ,colour=0x7289da)
   embedVar6.set_thumbnail(url=avatar)

   embedVar7 = discord.Embed(title= f":crown:CROWN Single Player & Multiplayer", description=textwrap.dedent(f"""\
   **Single Player**
   **.tales** Single player adventures where you traverse through your favorite universes as characters from various worlds!
   **.dungeon** Hard version of tales with better loot and better drop rates!
   **.boss** End Game battles featuring Iconic Villians from Crown Universes

   **Multiplayer**
   **.ctales @partner** Take a companion with your through your favorite tales with higher stakes!
   **.cdungeon @partner** Bring a companion through the darkest dungeons to earn awesome loot together
   **.cboss @partner** Epic battles between 2 high level companions and 1 Incredible Boss
   
   Co-Op must be played in Server

   **PVP**
   **.battle @player:** Select your Build and Challenge any Crown Unlimited Player to join your Game Lobby
   **.start:** Starts round against current opponent
   **.wager number:*** In lobby players can wager :coin:
   Builds are locked during lobbies, to change your build end the lobby with **.end** 
   """),colour=0x7289da)
   embedVar7.set_thumbnail(url=avatar)

   embedVar8 = discord.Embed(title= f":crown: Economy",description=textwrap.dedent(f"""\
   Crown Unlimited features an in game shop where you can purchase new Cards, Titles, and Arms

   **Stock**
   Items in the shop have a stock. When they are sold out they become unavailable

   **Sell & Trade**
   **.sell** and **.trade** will allow you to trade Cards, Titles, Arms and Pets with other players

   **Resell**
   **.resell item** to sell Cards, Titles, and Arms back to the market
   """) ,colour=0x7289da)
   embedVar8.set_thumbnail(url=avatar)


   paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
   paginator.add_reaction('⏮️', "first")
   paginator.add_reaction('⏪', "back")
   paginator.add_reaction('🔐', "lock")
   paginator.add_reaction('⏩', "next")
   paginator.add_reaction('⏭️', "last")
   embeds = [embedVar1, embedVar2, embedVar3, embedVar4, embedVar5, embedVar6, embedVar7, embedVar8]
   await paginator.run(embeds)

async def validate_user(ctx):
   query = {'DISNAME': str(ctx.author)}
   valid = db.queryUser(query)

   if valid:
      return True
   else:
      msg = await ctx.send(m.USER_NOT_REGISTERED, delete_after=5)
      return False

@bot.command()
async def load(ctx, extension):
   # Goes into cogs folder and looks for extension
   bot.load_extension(f'cogs.{extension}')

@bot.command()
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

@bot.command()
async def r(ctx):
   disname = str(ctx.author)
   name = disname.split("#",1)[0]
   user = {'DISNAME': disname, 'NAME': name, 'DID' : str(ctx.author.id), 'AVATAR': str(ctx.author.avatar_url)}
   response = db.createUsers(data.newUser(user))
   if response:

      embedVar = discord.Embed(title=f"Welcome to Party Chat Gaming!", description=textwrap.dedent(f"""
      The Party Chat Gaming bot is a multipurpose tool for admins and players alike to run and participate in matches and tournaments in some of your favorite games!
      In addition to the tools for tournaments and more, we offer an incredible gaming experience in Crown Unlimited!_See below for Crown Unlimited Details_
      
      **Welcome to Crown Unlimited**!
      Embark on a journey through Universes filled with characters from your favorite anime and video games! 
      
      **3 Easy Steps for Success**
      1. Collect Cards, Titles, Arms, and Pets
      2. Uniquely Customize your Builds to match your playstyle
      3. Explore Tales, Dungeons, and Bosses solo, or with your friend!

      **.crown**
      Read the Crown Unlimited Manual!

      **.senpaibattle**
      Start Crown Unlimited Battle Tutorial!

      **.build** Check your current build including your equipped Card, Title, Arm, and Pet

      **.shop** Purchase new Cards, Titles, and Arms


      
      Use .solo to play Crown Unlimited undisturbed. Remember to come back and play with your friends!
      _We do not own the rights to the images used in this game. This is a beta of an experimental bot for the purposes of growing our coding talents and skill. We do not make money from this project._
      """), colour=0xe91e63)
      embedVar.set_footer(text=".help to inquire all potential commands and capabilites of the bot")
      await ctx.author.send(embed=embedVar)
      await ctx.send(f"{ctx.author.mention} Welcome! Check your DMs.")

      vault = db.queryVault({'OWNER': disname})
      if vault:
         await ctx.send(m.VAULT_RECOVERED, delete_after=5)
      else:
         vault = db.createVault(data.newVault({'OWNER' : disname}))
         # await ctx.send(m.USER_HAS_REGISTERED, delete_after=5)
   else:
      await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=3) 

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
   await bless(100, ctx.author)

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

   quests = [{'OPPONENT': opponents[q1], 'TYPE': 'Tales', 'GOAL': 3, 'WINS': 0, 'REWARD': 200 },{'OPPONENT': opponents[q2], 'TYPE': 'Tales', 'GOAL': 5, 'WINS': 0, 'REWARD': 350 }, {'OPPONENT': opponents[q3], 'TYPE': 'Dungeon', 'GOAL': 3, 'WINS': 0, 'REWARD': 600 }]
   db.updateVaultNoFilter({'OWNER': str(ctx.author)}, {'$set': {'QUESTS': quests}})

   await ctx.send(f"Daily bonus :coin:100 has been applied for {ctx.author.mention}!\nYour new quests are available on the Quest Board!")
      
@bot.command()
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

@bot.command()
@commands.check(validate_user)
async def trade(ctx, user2: User, *args):
   user = db.queryUser({'DISNAME': str(ctx.author)})
   traded_to = db.queryUser({'DISNAME': str(user2)})
   p1_trade_item = " ".join([*args])
   p1_vault = db.queryVault({'OWNER' : str(ctx.author)})
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
            return user == ctx.author and str(reaction.emoji) == '👍'

         try:
            reaction, user = await bot.wait_for('reaction_add', timeout=8.0, check=check)
            if p2_trade_item in p2_arms:
               db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$pull':{'ARMS': str(p1_trade_item)}})
               response = db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$addToSet':{'ARMS': str(p2_trade_item)}})
               await ctx.send(f"{p2_trade_item} has been added to {ctx.author.mention}'s vault: ARMS")
            elif p2_trade_item in p2_titles:
               db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$pull':{'TITLES': str(p1_trade_item)}})
               response = db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$addToSet':{'TITLES': str(p2_trade_item)}})
               await ctx.send(f"{p2_trade_item} has been added to {ctx.author.mention}'s vault: TITLES")
            elif p2_trade_item in p2_cards:
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

@bot.command()
@commands.check(validate_user)
async def sell(ctx, user2: User, *args):
   user = db.queryUser({'DISNAME': str(ctx.author)})
   p1_trade_item = " ".join([*args])
   p1_vault = db.queryVault({'OWNER' : str(ctx.author)})
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
               return user == ctx.author and str(reaction.emoji) == '👍'

            try:
               reaction, user = await bot.wait_for('reaction_add', timeout=20.0, check=check)

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

@bot.command()
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

@bot.command()
@commands.check(validate_user)
async def teamgift(ctx, user2: User, amount):
   user = db.queryUser({'DISNAME': str(ctx.author)})
   if user['TEAM'] == 'PCG':
      await ctx.send("You must be owner of team to gift from team bank. ")
      return

   team = db.queryTeam({'TNAME': user['TEAM']})

   if str(user2) not in team['MEMBERS']:
      await ctx.send("You can only give from bank to team members. ")
      return

   balance = team['BANK']
   if balance <= int(amount):
      await ctx.send("You do not have that amount to give.")
   else:
      await bless(int(amount), user2)
      await curseteam(int(amount), team['TNAME'])
      await ctx.send(f":coin:{amount} has been gifted to {user2.mention}.")
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


@bot.command()
@commands.check(validate_user)
async def familygift(ctx, user2: User, amount):
   user = db.queryUser({'DISNAME': str(ctx.author)})
   family = db.queryFamily({'HEAD' : user['FAMILY']})
   if user['FAMILY'] == 'PCG' or (user['FAMILY'] != user['DISNAME'] and user['DISNAME'] != family['PARTNER']):
      await ctx.send("You must be the Head of a Household or Partner to give allowance. ")
      return

   family = db.queryFamily({'HEAD': user['FAMILY']})
   kids = family['KIDS']

   if str(user2) not in family['KIDS'] and str(user2) not in family['PARTNER'] and str(user2) not in family['HEAD']:
      await ctx.send("You can only give from savings to family members. ")
      return
   balance = family['BANK']
   if balance <= int(amount):
      await ctx.send("You do not have that amount to give.")
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
   house = family_data['HOUSE']
   multiplier = house['MULT']
   posBlessAmount = posBlessAmount * multiplier
   if family_data:
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

@bot.command()
@commands.check(validate_user)
async def traits(ctx):
   traits = ut.traits
   traitmessages = []
   for trait in traits:
      traitmessages.append(f"_{trait['NAME']}_\n**{trait['EFFECT']}**: {trait['TRAIT']}\n")

   embedVar = discord.Embed(title="Universe Traits", description="\n".join(traitmessages))

   await ctx.send(embed=embedVar)

@bot.command()
@commands.check(validate_user)
async def resell(ctx, *args):
   user = db.queryUser({'DISNAME': str(ctx.author)})
   p1_trade_item = " ".join([*args])

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

@bot.command()
@commands.check(validate_user)
async def addfield(ctx, collection, new_field, field_type):
   if ctx.author.guild_permissions.administrator == True:

      if field_type == 'string':
         field_type = "N/A"
      elif field_type == 'int':
         field_type = 0
      elif field_type == 'list':
         field_type = []
      elif field_type == 'bool':
         field_type = False
      
      if collection == 'cards':
         response = db.updateManyCards({'$set': {new_field: field_type}})
      elif collection == 'titles':
         response = db.updateManyTitles({'$set': {new_field: field_type}})
      elif collection == 'vaults':
         response = db.updateManyVaults({'$set': {new_field: field_type}})
      elif collection == 'users':
         response = db.updateManyUsers({'$set': {new_field: field_type}})
      elif collection == 'universe':
         response = db.updateManyUniverses({'$set': {new_field: field_type}})
      elif collection == 'boss':
         response = db.updateManyBosses({'$set': {new_field: field_type}})
      elif collection == 'arms':
         response = db.updateManyArms({'$set': {new_field: field_type}})
      elif collection == 'pets':
         response = db.updateManyPets({'$set': {new_field: field_type}})
      elif collection == 'teams':
         response = db.updateManyTeams({'$set': {new_field: field_type}})
   else:
      print(m.ADMIN_ONLY_COMMAND)

# @bot.command()
# @commands.check(validate_user)
# async def referred(ctx, user: User):
#    referred = db.queryUser({"DISNAME": str(ctx.author)})
#    if not referred['REFERRED']:
#       resp = db.updateUserNoFilter({'DISNAME': str(ctx.author)}, {'$set': {'REFERRED': True, 'REFERRER': str(user)}})
#       await bless(150, str(ctx.author))
#       await bless(300, str(user))
#       await ctx.send(f"Congrats & Welcome newcomer! You were awarded :coin: 150 and {user.mention} was awarded :coin:300.")
#    else:
#       await ctx.send("You're already referred!")


@bot.command()
async def about(ctx, *args):
   name = " ".join([*args])
   message = wikipedia.summary(str(name), sentences=5)
   if message:
      await ctx.send(message)
   else:
      await ctx.send("Sorry! There's no info for that.")


@bot.command()
@commands.check(validate_user)
async def solo(ctx):
   await ctx.send(f"{ctx.author.mention} check your dms. ")
   await DM(ctx, ctx.author, "Continue your Crown Unlimited journey here, undisturbed. All Crown Unlimited commands are functional here. ")

if config('ENV') == "production":
   DISCORD_TOKEN = config('DISCORD_TOKEN_TEST')
else:
   DISCORD_TOKEN = config('DISCORD_TOKEN_FOR_TESTING')

bot.run(DISCORD_TOKEN)