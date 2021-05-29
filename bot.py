from dataclasses import field
from discord import player, team
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

# Converters
from discord import User
from discord import Member

import os
import logging
import requests
from decouple import config
from collections import ChainMap

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


   embedVar1 = discord.Embed(title= f":video_game:Player Commands:", description=h.PLAYER_COMMANDS, colour=0x7289da)
   embedVar1.set_thumbnail(url=avatar)
   embedVar1.add_field(name="Help Navigation", value="*First Page: :track_previous:|Prev Page: :rewind:|\nNext Page: :fast_forward:| Last Page: :track_next:*")

   embedVar2 = discord.Embed(title= f":triangular_flag_on_post:Profile Commands:", description=h.PROFILE_COMMANDS, colour=0x7289da)
   embedVar2.set_thumbnail(url=avatar)
   embedVar2.add_field(name="Help Navigation", value="*First Page: :track_previous:|Prev Page: :rewind:|\nNext Page: :fast_forward:| Last Page: :track_next:*")

   embedVar3 = discord.Embed(title= f":crossed_swords:Lobbies:", description=h.LOBBY_COMMANDS, colour=0x7289da)
   embedVar3.set_thumbnail(url=avatar)
   embedVar3.add_field(name="Help Navigation", value="*First Page: :track_previous:|Prev Page: :rewind:|\nNext Page: :fast_forward:| Last Page: :track_next:*")

   embedVar4 = discord.Embed(title= f":crown:Crown Unlimited Player Commands:", description=h.CROWN_UNLIMITED_PLAYER_COMMANDS, colour=0x7289da)
   embedVar4.set_thumbnail(url=avatar)
   embedVar4.add_field(name="Help Navigation", value="*First Page: :track_previous:|Prev Page: :rewind:|\nNext Page: :fast_forward:| Last Page: :track_next:*")

   embedVar5 = discord.Embed(title= f":military_helmet:Teams:", description=h.TEAM_COMMANDS, colour=0x7289da)
   embedVar5.set_thumbnail(url=avatar)
   embedVar5.add_field(name=":fireworks:Tournament Types:", value="\n`Exhibitions`\n`KingsGambit`\n`GodsOfCod`")
   embedVar5.add_field(name="Help Navigation", value="*First Page: :track_previous:|Prev Page: :rewind:|\nNext Page: :fast_forward:| Last Page: :track_next:*")

   embedVar6 = discord.Embed(title= f":shopping_cart:Pop Up Shop:", description=h.SHOP_COMMANDS, colour=0x7289da)
   embedVar6.set_thumbnail(url=avatar)
   embedVar6.add_field(name="Help Navigation", value="*First Page: :track_previous:|Prev Page: :rewind:|\nNext Page: :fast_forward:| Last Page: :track_next:*")

   embedVar7 = discord.Embed(title= f":crown:Crown Unlimited Game Commands:", description=h.CROWN_UNLIMITED_GAMES, colour=0x7289da)
   embedVar7.set_thumbnail(url=avatar)
   embedVar7.add_field(name="Help Navigation", value="*First Page: :track_previous:|Prev Page: :rewind:|\nNext Page: :fast_forward:| Last Page: :track_next:*")

   paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
   paginator.add_reaction('⏮️', "first")
   paginator.add_reaction('⏪', "back")
   paginator.add_reaction('🔐', "lock")
   paginator.add_reaction('⏩', "next")
   paginator.add_reaction('⏭️', "last")
   embeds = [embedVar1, embedVar4, embedVar6, embedVar7, embedVar2, embedVar3, embedVar5]
   await paginator.run(embeds)

@bot.group(invoke_without_command=True)
async def status(ctx):
   avatar="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Legend.png"


   embedVar1 = discord.Embed(title= f":trident:ENHANCE Sets:",colour=0x7289da)
   embedVar1.set_thumbnail(url=avatar)
   embedVar1.add_field(name="`INCREASES`", value="`ATK` - Increase `ATK`\n\n`DEF` - Increase `DEF`\n\n`HLT` - Increase `HLT`\n\n`STAM` - Increase `STAM`\n\n")

   embedVar2 = discord.Embed(title= f":trident:ENHANCE Sets:",colour=0x7289da)
   embedVar2.set_thumbnail(url=avatar)
   embedVar2.add_field(name="`STEALS`", value="`FLOG`- `ATK` Steal\n\n`WITHER`- `DEF` Steal\n\n`LIFE` - `LIFE` Steal\n\n`DRAIN` - `STAM` Steal\n\n")


   embedVar3 = discord.Embed(title= f":trident:ENHANCE Sets:",colour=0x7289da)
   embedVar3.set_thumbnail(url=avatar)
   embedVar3.add_field(name="`SACRIFICE`", value="`RAGE` - Decrease `DEF`, Increase `ATK`\n\n`BRACE` - Decrease `ATK`, Increase `DEF`\n\n`BZRK` - Decrease `HLT`,  Increase `ATK`\n\n`CRYSTAL`- Decrease `HLT`, Increase `DEF`\n\n`GROWTH`- Decrease `MAXHLT`, Increase `STATS`\n\n")

   embedVar4 = discord.Embed(title= f":trident:ENHANCE Sets:",colour=0x7289da)
   embedVar4.set_thumbnail(url=avatar)
   embedVar4.add_field(name="`TRADE`", value="`STANCE` - Swap `ATK` and `DEF`\n\n`CONFUSE` - Swap `OPP ATK` and  `OPP DEF`\n\n")

   embedVar5 = discord.Embed(title= f":trident:ENHANCE Sets:",colour=0x7289da)
   embedVar5.set_thumbnail(url=avatar)
   embedVar5.add_field(name="`TIME`", value="`BLINK`  - Decrease  `STAM`, Increase `OPP STAM`\n\n`SLOW` - Decrease `STAM`, Swap `OPP STAM`\n\n`HASTE` - Increase `STAM`, Swap `OPP STAM`\n\n")

   embedVar6 = discord.Embed(title= f":trident:ENHANCE Sets:",colour=0x7289da)
   embedVar6.set_thumbnail(url=avatar)
   embedVar6.add_field(name="`CONTROL`", value="`SOULCHAIN` - Both `PLAYERS` `STAM` = \n\n`GAMBLE` - Both `PLAYERS` `HEALTH` =\n\n`FEAR` - Decrease `HLT`, Decrease `OPP ATK` & `OPP DEF`")

   paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
   paginator.add_reaction('⏮️', "first")
   paginator.add_reaction('⏪', "back")
   paginator.add_reaction('🔐', "lock")
   paginator.add_reaction('⏩', "next")
   paginator.add_reaction('⏭️', "last")
   embeds = [embedVar1, embedVar2, embedVar3, embedVar4, embedVar5, embedVar6]
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

      embedVar = discord.Embed(title=f"Welcome to Party Chat Gaming!", colour=0xe91e63)
      embedVar.set_author(name="Use .solo to play Crown Unlimited undisturbed. Remember to come back and play with your friends!")
      embedVar.add_field(name=".vault", value="Check your equipped `card`, `title` and `arm`")
      embedVar.add_field(name=".shop", value="Purchase your starting `card`, `title` and `arm`")
      embedVar.add_field(name=".senpaibattle", value="Start tutorial on Crown Unlimited")
      embedVar.add_field(name=".help", value="Inquire all potential commands and capabilites of the bot")
      embedVar.set_footer(text=".senpai will start tutorial on overall bot capabilities")
      await ctx.send(embed=embedVar)

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
            p1_active_pet = pet


   p2_vault = db.queryVault({'OWNER' : str(user2)})
   p2_cards = p2_vault['CARDS']
   p2_titles = p2_vault['TITLES']
   p2_arms = p2_vault['ARMS']
   p2_pets = p2_vault['PETS']
   p2_balance = p2_vault['BALANCE']
   p2_trade_item = ""

   p2_pet_names = []
   for pet in p2_pets:
         p2_pet_names.append(pet['NAME'])


   commence = False

   if p1_trade_item not in p1_cards and p1_trade_item not in p1_titles and p1_trade_item not in p1_arms and p1_trade_item not in p1_pet_names and p1_trade_item not in p2_pet_names:
      await ctx.send("You do not own this item.")
      return
   else:
      await ctx.send(f"{user2.mention}, what will you trade for {ctx.author.mention}'s {p1_trade_item}?")

      def check(msg):
         if p1_trade_item in p1_pet_names:
            return msg.author == user2 and msg.content in p2_pet_names and msg.content not in p1_cards and msg.content not in p1_titles and msg.content not in p1_arms and msg.content not in p1_pet_names
         else:
            return msg.author == user2 and msg.content in p2_cards or msg.content in p2_titles or msg.content in p2_arms or msg.content in p2_pet_names and msg.content not in p1_cards and msg.content not in p1_titles and msg.content not in p1_arms and msg.content not in p1_pet_names

      try:
         msg = await bot.wait_for('message', timeout=25.0, check=check)
         p2_trade_item = msg.content

         p2_active_pet = {}
         p2_pet_names = []
         for pet in p2_pets:
               p2_pet_names.append(pet['NAME'])
               if pet['NAME'] == p2_trade_item:
                  p2_active_pet = pet

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
            print(p2_active_pet)
            print(p1_active_pet)

            reaction, user = await bot.wait_for('reaction_add', timeout=25.0, check=check)
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
   p1_trade_item = " ".join([*args])
   p1_vault = db.queryVault({'OWNER' : str(ctx.author)})
   p1_cards = p1_vault['CARDS']
   p1_titles = p1_vault['TITLES']
   p1_arms = p1_vault['ARMS']
   p1_balance = p1_vault['BALANCE']

   p2_vault = db.queryVault({'OWNER' : str(user2)})
   p2_cards = p2_vault['CARDS']
   p2_titles = p2_vault['TITLES']
   p2_arms = p2_vault['ARMS']
   p2_balance = p2_vault['BALANCE']
   p2_trade_item = ""

   commence = False

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
         await ctx.send(f"{user2.mention} how much are you willing to pay for {ctx.author.mention}'s {p1_trade_item}?")

         def check(msg):
            return msg.author == user2 and (int(msg.content) - int(p2_balance)) <= 0
         try:
            msg = await bot.wait_for('message', timeout=25.0, check=check)
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
               reaction, user = await bot.wait_for('reaction_add', timeout=25.0, check=check)

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
                  await ctx.send(f"{p1_trade_item} has been added to {user2.mention}'s vault: CARDS")

            except:
               await ctx.send("Trade ended. ")

@bot.command()
@commands.check(validate_user)
async def addfield(ctx, collection, new_field, field_type):
   if ctx.author.guild_permissions.administrator == True:

      if field_type == 'string':
         field_type = ''
      elif field_type == 'int':
         field_type = 25
      elif field_type == 'list':
         field_type = [{'NAME': 'Doge', 'LVL': 1, 'EXP': 0, 'Hodl': 20, 'TYPE': 'HLT', 'BOND': 0, 'PATH': "https://res.cloudinary.com/dkcmq8o15/image/upload/v1622221287/Pets/Doge.jpg"}]
      elif field_type == 'bool':
         field_type = True
      
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
   else:
      print(m.ADMIN_ONLY_COMMAND)

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