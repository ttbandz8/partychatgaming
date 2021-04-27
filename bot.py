import db
import time
import classes as data
import test_data as td
import discord
from discord.ext import commands

# Converters
from discord import User
from discord import Member

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

client = discord.Client()

bot = commands.Bot(command_prefix=">")

def validate_user(ctx):
   query = {'DISNAME': str(ctx.author)}
   validate = db.queryUser(query)
   if validate:
      return True
   else:
      return False

@bot.event
async def on_ready():
   print('Bot is ready. ')

@bot.command()
@commands.check(validate_user)
async def lookup(ctx, user: User):
   query = {'DISNAME': str(user)}
   d = db.queryUser(query)

   if d:
      name = d['DISNAME'].split("#",1)[0]
      games = d['GAMES']
      ign = d['IGN']
      teams = d['TEAMS']
      titles = d['TITLES']
      avatar = d['AVATAR']
      rwins = d['RWINS']
      rlosses = d['RLOSSES']
      urwins = d['URWINS']
      urlosses = d['URLOSSES']
      tournament_wins = d['TOURNAMENT_WINS']

      rwins_to_string = dict(ChainMap(*rwins))
      rlosses_to_string = dict(ChainMap(*rlosses))
      urwins_to_string = dict(ChainMap(*urwins))
      urlosses_to_string = dict(ChainMap(*urlosses))
      ign_to_string = dict(ChainMap(*ign))

      embedVar = discord.Embed(title=f"{name}'s profile".format(client), description="Party Chat Gaming Database", colour=000000)
      embedVar.set_thumbnail(url=avatar)
      embedVar.add_field(name="Games", value=' '.join(str(x) for x in games))
      embedVar.add_field(name="In-Game Names", value="\n".join(f'{k}: {v}' for k,v in ign_to_string.items()))
      embedVar.add_field(name="Teams", value=' '.join(str(x) for x in teams))
      embedVar.add_field(name="Titles", value=' '.join(str(x) for x in titles))
      embedVar.add_field(name="Ranked Wins", value="\n".join(f'{k}: {v}' for k,v in rwins_to_string.items()))
      embedVar.add_field(name="Ranked Losses", value="\n".join(f'{k}: {v}' for k,v in rlosses_to_string.items()))
      embedVar.add_field(name="Normal Wins", value="\n".join(f'{k}: {v}' for k,v in urwins_to_string.items()))
      embedVar.add_field(name="Normal Losses", value="\n".join(f'{k}: {v}' for k,v in urlosses_to_string.items()))
      embedVar.add_field(name="Tournament Wins", value=tournament_wins)
      await ctx.send(embed=embedVar)
   else:
      await ctx.send("User does not exist in the system. ")

   
@bot.command()
async def register(ctx):
   user = {'DISNAME': str(ctx.author), 'AVATAR': str(ctx.author.avatar_url)}
   response = db.createUsers(data.newUser(user))
   await ctx.send(response)

@bot.command()
async def delete(ctx, user: User, args):
   if args == 'IWANTTODELETEMYACCOUNT':
      if str(ctx.author) == str(user):
         query = {'DISNAME': str(ctx.author)}
         user_is_validated = db.queryUser(query)
         if user_is_validated:
            delete_user_resp = db.deleteUser(query)
            await ctx.send(delete_user_resp)
   else:
      await ctx.send("Invalid command")

@bot.command()
async def addGame(ctx, args):
   user = {'DISNAME': str(ctx.author)}
   await ctx.send(response)
            



DISCORD_TOKEN = config('DISCORD_TOKEN')

bot.run('ODM1OTY4MjE1MjU0NDMzNzkz.YIXKEg.Rkpq-J1uFNYwLlDR8x6KpDVqqP4')

# Add game to database (done)
# Add game to user profile
# 


