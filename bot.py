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
async def lk(ctx, user: User):
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
      embedVar.add_field(name="Game", value=' '.join(str(x) for x in games))
      embedVar.add_field(name="In-Game Name", value="\n".join(f'{v}' for k,v in ign_to_string.items()))
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
async def r(ctx):
   user = {'DISNAME': str(ctx.author), 'AVATAR': str(ctx.author.avatar_url)}
   response = db.createUsers(data.newUser(user))
   await ctx.send(response)

@bot.command()
@commands.check(validate_user)
async def d(ctx, user: User, args):
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
@commands.check(validate_user)
async def ag(ctx, *args):
   user = {'DISNAME': str(ctx.author)}
   user_data = db.queryUser(user)
   aliases = [x for x in db.query_all_games() for x in x['ALIASES']]
   if args[0] in aliases:
      game_query = {'ALIASES': args[0]}
      game = db.queryGame(game_query)
      title = game['GAME']
      ign = game['IGN']
      if title not in user_data['GAMES'] and ign != True:
         if "PCG" in user_data['GAMES']:
            query_to_update_game = {"$set": {"GAMES": [title]}}
            resp = db.updateUser(user, query_to_update_game)
            ctx.send(resp)
         else:
            query_to_update_game = {"$addToSet": {"GAMES": title}}
            resp = db.updateUser(user, query_to_update_game)
            ctx.send(resp)
      elif title not in user_data['GAMES'] and ign == True:
         if "PCG" in user_data['GAMES']:
            query_to_update_game = {"$set": {"GAMES": [title], "IGN": [{title : args[1]}]}}
            resp = db.updateUser(user, query_to_update_game)
            await ctx.send(resp)
         else:

            query_to_update_game = {"$addToSet": {"GAMES": title, "IGN": {title : args[1]}}}
            resp = db.updateUser(user, query_to_update_game)
            await ctx.send(resp)

@bot.command()
@commands.check(validate_user)
async def c1v1(ctx, args):
   game = [x for x in db.query_all_games()][0]
   session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 1, "TEAMS": [{"TEAM": [str(ctx.author)], "SCORE": 0, "POSITION": 0}]}
   if args == "ur":
      resp = db.createSession(data.newSession(session_query))
      await ctx.send(resp)
   elif args == "r":
      session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 1, "TEAMS": [{"TEAM": [str(ctx.author)], "SCORE": 0, "POSITION": 0}], "RANKED": True}
      resp = db.createSession(data.newSession(session_query))
      await ctx.send(resp)
# @bot.command()
# @commands.check(validate_user)
# async def c2v2(ctx, *user: User):
#    user_query = {'DISNAME': str(ctx.author)}
#    session_type = args
#    users = [str(x) for x in user]
#    if session_type > 1:
#       print("Not a 1v1. ")
#    else:
#       print("1v1")

# @bot.command()
# @commands.check(validate_user)
# async def c3v3(ctx, *user: User):
#    user_query = {'DISNAME': str(ctx.author)}
#    session_type = args
#    users = [str(x) for x in user]
#    if session_type > 1:
#       print("Not a 1v1. ")
#    else:
#       print("1v1")

# @bot.command()
# @commands.check(validate_user)
# async def c4v4(ctx, *user: User):
#    user_query = {'DISNAME': str(ctx.author)}
#    session_type = args
#    users = [str(x) for x in user]
#    if session_type > 1:
#       print("Not a 1v1. ")
#    else:
#       print("1v1")

# @bot.command()
# @commands.check(validate_user)
# async def c5v5(ctx, *user: User):
#    user_query = {'DISNAME': str(ctx.author)}
#    session_type = args
#    users = [str(x) for x in user]
#    if session_type > 1:
#       print("Not a 1v1. ")
#    else:
#       print("1v1")

@bot.command()
@commands.check(validate_user)
async def js(ctx, *user: User):
   print("join session")

@bot.command()
@commands.check(validate_user)
async def session(ctx, user: User):
   session_owner = {'OWNER': str(user)}
   session = db.querySession(session_owner)

   game_query = {'ALIASES': session['GAME']}
   game = db.queryGame(game_query)

   name = session['OWNER'].split("#",1)[0]
   games = game['GAME']
   avatar = game['IMAGE_URL']
   game_type = " "
   if session['TYPE'] == 1:
      game_type = "1v1"
   elif session['TYPE'] == 2:
      game_type = "2v2"
   elif session['TYPE'] == 3:
      game_type = "3v3"
   elif session['TYPE'] == 4:
      game_type = "4v4"
   elif session['TYPE'] == 5:
      game_type = "5v5"

   ranked = " "
   if session['RANKED'] == True:
      ranked = "Ranked"
   elif session['RANKED'] == False:
      ranked = "Unranked"

   print(session['TEAMS'])
   # titles = d['TITLES']

   # rwins = d['RWINS']
   # rlosses = d['RLOSSES']
   # urwins = d['URWINS']
   # urlosses = d['URLOSSES']
   # tournament_wins = d['TOURNAMENT_WINS']

   # rwins_to_string = dict(ChainMap(*rwins))
   # rlosses_to_string = dict(ChainMap(*rlosses))
   # urwins_to_string = dict(ChainMap(*urwins))
   # urlosses_to_string = dict(ChainMap(*urlosses))
   # ign_to_string = dict(ChainMap(*ign))

   embedVar = discord.Embed(title=f"{name}'s {games} Session ".format(bot), description="Party Chat Gaming Database", colour=000000)
   embedVar.set_thumbnail(url=avatar)
   embedVar.add_field(name="MATCH TYPE", value=f'{game_type}'.format(bot))
   embedVar.add_field(name="RANKED", value=f'{ranked}'.format(bot))
   await ctx.send(embed=embedVar)




DISCORD_TOKEN = config('DISCORD_TOKEN')

bot.run(DISCORD_TOKEN)