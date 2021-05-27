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
   embedVar1.add_field(name=":woman_teacher:Senpai:tm: Tutorial Commands:", value=h.SENPAI_COMMANDS)
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

# @bot.command()
# async def teamHelp(ctx):
#       embedVar = discord.Embed(title=f"Teams!: How To Register!", description="Party Chat Gaming Database™️", colour=000000)
#       embedVar.add_field(name="REGISTRATION!" , value="Type::arrow_right: .cteam codm 'Team Name'")
#       embedVar.add_field(name="INVITE MEMBERS!" , value="Type::arrow_right: .att 'teamname' @user")
#       embedVar.add_field(name="DELETE MEMBERS!" , value="Type::arrow_right: .dtm @user")
#       embedVar.add_field(name="DELETE TEAM" , value="Type::arrow_right: .dteam 'teamname'")
#       embedVar.add_field(name="STILL LOST????" , value="use .help or ask a PCG Member for assistance")
#       await ctx.send(embed=embedVar)

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
async def addfield(ctx, collection, new_field, field_type):
   if ctx.author.guild_permissions.administrator == True:

      if field_type == 'string':
         field_type = ''
      elif field_type == 'int':
         field_type = 25
      elif field_type == 'list':
         field_type = []
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