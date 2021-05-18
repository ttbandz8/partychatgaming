from discord import player, team
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

client = discord.Client()

if config('ENV') == "production":
   # PRODUCTION
   bot = commands.Bot(command_prefix="#")
else:
   # TEST
   bot = commands.Bot(command_prefix=">")

bot.remove_command("help")

@bot.group(invoke_without_command=True)
async def help(ctx):
   em = discord.Embed(title = "Party Chat Gaming Bot Help Page", description = "use #help <command> for extended information on that command.", color = ctx.author.color)

   em.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Legend.png")
   em.add_field(name = "Player Commands", value =h.PLAYER_COMMANDS , inline=False)
   em.add_field(name = "Profile Commands", value =h.PROFILE_COMMANDS, inline=False)
   em.add_field(name = "Senpai:tm: Tutorial Commands", value =h.SENPAI_COMMANDS,inline=False)
   em.add_field(name = "Lobbies", value =h.LOBBY_COMMANDS,inline=False)
   em.add_field(name = "Shop", value =h.SHOP_COMMANDS, inline=False)
   em.add_field(name = "Team", value =h.TEAM_COMMANDS,inline=True)
   em.add_field(name = "Tournament Types:", value = "\nExhibitions\nKingsGambit\nGodsOfCod",inline=True)
   em.set_footer(text="Many more cards and titles are available via tournament win only. ")
   await ctx.send(embed = em)

@bot.command()
async def teamHelp(ctx):
      embedVar = discord.Embed(title=f"Teams!: How To Register!", description="Party Chat Gaming Database™️", colour=000000)
      embedVar.add_field(name="REGISTRATION!" , value="Type::arrow_right: #cteam codm 'Team Name'")
      embedVar.add_field(name="INVITE MEMBERS!" , value="Type::arrow_right: #att 'teamname' @user")
      embedVar.add_field(name="DELETE MEMBERS!" , value="Type::arrow_right: #dtm @user")
      embedVar.add_field(name="DELETE TEAM" , value="Type::arrow_right: #dteam 'teamname'")
      embedVar.add_field(name="STILL LOST????" , value="use #help or ask a PCG Member for assistance")
      await ctx.send(embed=embedVar)

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
      vault = db.queryVault({'OWNER': disname})
      if vault:
         await ctx.send(m.VAULT_RECOVERED, delete_after=5)
      else:
         vault = db.createVault(data.newVault({'OWNER' : disname}))
         await ctx.send(m.USER_HAS_REGISTERED, delete_after=5)
   else:
      await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=3)  

@bot.command()
@commands.check(validate_user)
async def iby(ctx, args1, user: User):

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
async def test(ctx):
   number = 10
   while number >= 0:
      await ctx.send(f"Number is {number}. Still not 0!")

      def check(msg):
         return msg.author == ctx.author and msg.channel == ctx.channel
      try:
         msg = await bot.wait_for("message", check=check)
         number = number - int(msg.content)
      except:
         await ctx.send('Did not work')
   await ctx.send("Number is 0!")

if config('ENV') == "production":
   DISCORD_TOKEN = config('DISCORD_TOKEN_TEST')
else:
   DISCORD_TOKEN = config('DISCORD_TOKEN_FOR_TESTING')

bot.run(DISCORD_TOKEN)