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
async def lk(ctx, user: User):
   query = {'DISNAME': str(user)}
   d = db.queryUser(query)

   if d:
      name = d['DISNAME'].split("#",1)[0]
      games = d['GAMES']
      ign = d['IGN']
      team = d['TEAM']
      titles = d['TITLE']
      avatar = d['AVATAR']
      ranked = d['RANKED']
      normal = d['NORMAL']
      tournament_wins = d['TOURNAMENT_WINS']


      ranked_to_string = dict(ChainMap(*ranked))
      normal_to_string = dict(ChainMap(*normal))
      ign_to_string = dict(ChainMap(*ign))

      embedVar = discord.Embed(title= f":triangular_flag_on_post: " + f"{name}".format(client), description=":bank: Party Chat Gaming Database™️", colour=000000)
      embedVar.set_thumbnail(url=avatar)
      embedVar.add_field(name="Game" + " :video_game:" , value=' '.join(str(x) for x in games))
      embedVar.add_field(name="In-Game Name" + " :selfie:", value="\n".join(f'{v}' for k,v in ign_to_string.items()))
      embedVar.add_field(name="Team" + " :military_helmet:", value=team)
      embedVar.add_field(name="Titles" + " :crown:", value=' '.join(str(x) for x in titles))
      embedVar.add_field(name="Ranked" + " :medal:", value="\n".join(f'{k}: {"/".join([str(int) for int in v])}' for k,v in ranked_to_string.items()))
      embedVar.add_field(name="Normals" + " :crossed_swords:", value="\n".join(f'{k}: {"/".join([str(int) for int in v])}' for k,v in normal_to_string.items()))
      embedVar.add_field(name="Tournament Wins" + " :fireworks:", value=tournament_wins)
      await ctx.send(embed=embedVar, delete_after=15)
   else:
      await ctx.send(m.USER_NOT_REGISTERED, delete_after=3)

# Leaderboard
# @bot.command()
# @commands.check(validate_user)
# async def gocleaderboard(ctx, args):
#    goc_data = db.queryGoc({'TITLE': args})
#    if goc_data:
#       print("yes")

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

# Create 1v1 - 5v5 Lobbies

#testing reactions 
@bot.command()
@commands.check(validate_user)
async def cversus(ctx, args, *participant: User):
   if ctx.author.guild_permissions.administrator == True:
      game = [x for x in db.query_all_games()][0]
      teammates = []
      #load up teammate array 
      for users in participant:
         teammates.append(str(users))
      valid_teammates = []
      #Check if same team members
      list_of_teams = set()
      for x in teammates:
         valid = db.queryUser({'DISNAME' : str(x)})
         if valid:
            valid_teammates.append(valid["DISNAME"])
            list_of_teams.add(valid['TEAM'])
         else:
            await ctx.send(f"{valid['DISNAME']} needs to register.".format(bot), delete_after=5)
      if len(valid_teammates) == 2:
         if len(list_of_teams) > 1:
            await ctx.send(m.DIFFERENT_TEAMS, delete_after=5)
         else:
            team_name ="".join(list_of_teams)
            team_members=[]
            for player in participant:
               await DM(ctx, player, f"{ctx.author.mention}has invited you to a Team Scrimm:military_helmet:")
               accept = await ctx.send(f"{player.mention} are you ready to Scrimm?", delete_after=10)

               for emoji in emojis:
                  await accept.add_reaction(emoji)

               def check(reaction,user):
                  return user == player and str(reaction.emoji)== '👍'
               try:
                  reaction,user = await bot.wait_for('reaction_add',timeout=15.0,check=check)
                  team_members.append(str(player))
               except:
                  await ctx.send(f"{player.mention} did not accept:eyes:")
            if args == "n":
               session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 3, "SCRIM": True, "TEAMS": [{"TEAM": [str(ctx.author), team_members], "SCORE": 0, "POSITION": 0}]}
               resp = db.createSession(data.newSession(session_query))
               await ctx.send(resp, delete_after=5)
            elif args == "r":
               session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 3, "SCRIM": True, "TEAMS": [{"TEAM": [str(ctx.author), team_members], "SCORE": 0, "POSITION": 0}], "RANKED": True}
               resp = db.createSession(data.newSession(session_query))
               await ctx.send(resp, delete_after=5)
      else:
         await ctx.send(m.USER_NOT_REGISTERED)
   else:
      await ctx.send(m.USER_NOT_REGISTERED, delete_after=5)

#Legacy v5v5 code
async def cmps(ctx, args, user1: User, user2: User, user3: User, user4: User):
   game = [x for x in db.query_all_games()][0]
   
   teammates = [str(user1), str(user2), str(user3), str(user4)]
   valid_teammates = []
   for x in teammates:
      valid = db.queryUser(x)
      if valid:
         valid_teammates.append(valid["DISNAME"])
      else:
         await ctx.send(f"{valid['DISNAME']} needs to register.".format(bot), delete_after=5)

   if valid_teammates:
      accept = await ctx.send("Will you join the lobby?", delete_after=10)
      for emoji in emojis:
         await accept.add_reaction(emoji)

      def check(reaction, user):
         return user in valid_teammates and str(reaction.emoji) == '👍'

      try:
         reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=check)


         session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 2, "TEAMS": [{"TEAM": [str(ctx.author), str(user1), str(user2), str(user3), str(user4)], "SCORE": 0, "POSITION": 0}]}
         if args == "n":
            resp = db.createSession(data.newSession(session_query))
            await ctx.send(resp, delete_after=5)
         elif args == "r":
            session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 2, "TEAMS": [{"TEAM": [str(ctx.author), str(user1), str(user2), str(user3), str(user4 )], "SCORE": 0, "POSITION": 0}], "RANKED": True}
            resp = db.createSession(data.newSession(session_query))
            await ctx.send(resp, delete_after=5)
      except:
         await ctx.send(m.INVITE_NOT_ACCEPTED, delete_after=3)
   else:
      await ctx.send(m.USER_NOT_REGISTERED, delete_after=5)


''' Score '''
@bot.command()
@commands.check(validate_user)
async def score(ctx, user: User):
   session_query = {"OWNER": str(ctx.author), "AVAILABLE": True, "KINGSGAMBIT": False}
   session_data = db.querySession(session_query)
   teams = [x for x in session_data['TEAMS']]
   winning_team = {}
   for x in teams:
      if str(user) in x['TEAM']: 
         winning_team = x
   new_score = winning_team['SCORE'] + 1
   update_query = {'$set': {'TEAMS.$.SCORE': new_score}}
   query = {"_id": session_data["_id"], "TEAMS.TEAM": str(user)}
   response = db.updateSession(session_query, query, update_query)
   reciever = db.queryUser({'DISNAME': str(user)})
   name = reciever['DISNAME']
   message = ":one: You Scored, Don't Let Up :one:"
   await DM(ctx, user, message)
   if response:
      await ctx.send(f"{user.mention}" +f" + :one:", delete_after=2)
   else:
      await ctx.send(f"Score not added. Please, try again. ", delete_after=5)


#end lobby and push data to database
@bot.command()
@commands.check(validate_user)
async def el(ctx):
   session_query = {"OWNER": str(ctx.author), "AVAILABLE": True}
   session = db.querySession(session_query)
   teams = [x for x in session['TEAMS']]
   if len(teams) != 1:
      await sw(ctx)
      await altsl(ctx)
      end = db.endSession(session_query)
      await ctx.send(end, delete_after=5)
   else:
      end = db.endSession(session_query)
      await ctx.send(m.SESSION_HAS_ENDED)


#delete session from database
@bot.command()
@commands.check(validate_user)
async def dl(ctx):
   session_query = {"OWNER": str(ctx.author), "AVAILABLE": True}
   response = db.deleteSession(session_query)
   await ctx.send(response, delete_after=5)


# ''' Delete All Sessions '''
# @bot.command()
# @commands.check(validate_user)
# async def dal(ctx):
#    user_query = {"DISNAME": str(ctx.author)}
#    if ctx.author.guild_permissions.administrator == True:
#       resp = db.deleteAllSessions(user_query)
#       await ctx.send(resp)
#    else:
#       await ctx.send(m.ADMIN_ONLY_COMMAND)




''' Invite to 1v1 '''
@bot.command()
@commands.check(validate_user)
async def challenge(ctx, args, user1: User):
   game = [x for x in db.query_all_games()][0]
   
   validate_opponent = db.queryUser({'DISNAME': str(user1)})

   if validate_opponent:
      await DM(ctx, user1, f"{ctx.author.mention}" + " has challeneged you... :eyes:")
      accept = await ctx.send(f"{user1.mention}, Will you join the lobby? :fire:", delete_after=15)
      for emoji in emojis:
         await accept.add_reaction(emoji)

      def check(reaction, user):
         return user == user1 and str(reaction.emoji) == '👍'
      try:
         reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=check)

         session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 1, "TEAMS": [{"TEAM": [str(ctx.author)], "SCORE": 0, "POSITION": 0}], "AVAILABLE": True}
         join_query = {"TEAM": [str(user1)], "SCORE": 0, "POSITION": 1}
         if args == "n":
            session = db.createSession(data.newSession(session_query))
            resp = db.joinSession(session_query, join_query)
            await ctx.send(resp, delete_after=5)
         elif args == "r":
            session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 1, "TEAMS": [{"TEAM": [str(ctx.author)], "SCORE": 0, "POSITION": 0}], "RANKED": True, "AVAILABLE": True}
            session = db.createSession(data.newSession(session_query))
            resp = db.joinSession(session_query, join_query)
            await ctx.send(resp, delete_after=5)
      except:
         await ctx.send(m.INVITE_NOT_ACCEPTED, delete_after=3)
   else:
      await ctx.send("Users must register.", delete_after=5)


#Join Session with up to 4 mates
@bot.command()
@commands.check(validate_user)
async def jl(ctx, *user: User):
   session_query = {"OWNER": str(user[0]), "AVAILABLE": True}
   session = db.querySession(session_query)
   if session:
      match_type = session['TYPE']
      invalid_user = False
      for u in user:
         user_query = ({'DISNAME': str(u)})
         resp = db.queryUser(user_query)
         if not resp:
            invalid_user = True
      
      if invalid_user:
         await ctx.send(m.USER_NOT_REGISTERED, delete_after=5)
      else:
         if match_type == 1:
            join_query = {"TEAM": [str(ctx.author)], "SCORE": 0, "POSITION": 1}
            session_joined = db.joinSession(session_query, join_query)
            await ctx.send(session_joined, delete_after=5)
         if match_type ==2:
            join_query = {"TEAM": [str(ctx.author), (str(user[1]))], "SCORE": 0, "POSITION": 1}
            session_joined = db.joinSession(session_query, join_query)
            await ctx.send(session_joined, delete_after=5)
         if match_type ==3:
            join_query = {"TEAM": [str(ctx.author), (str(user[1])), str(user[2])], "SCORE": 0, "POSITION": 1}
            session_joined = db.joinSession(session_query, join_query)
            await ctx.send(session_joined, delete_after=5)
         if match_type ==4:
            join_query = {"TEAM": [str(ctx.author), (str(user[1])), str(user[2]), str(user[3])], "SCORE": 0, "POSITION": 1}
            session_joined = db.joinSession(session_query, join_query)
            await ctx.send(session_joined, delete_after=5)
         if match_type ==5:
            join_query = {"TEAM": [str(ctx.author), (str(user[1])), str(user[2]), str(user[3]), str(user[4])], "SCORE": 0, "POSITION": 1}
            session_joined = db.joinSession(session_query, join_query)
            await ctx.send(session_joined, delete_after=5)
   else:
      await ctx.send(m.SESSION_DOES_NOT_EXIST)

#Session Generator Admin's can pull users in sessions up to 5's
@bot.command()
@commands.check(validate_user)
async def lg(ctx, *user: User):
   if ctx.author.guild_permissions.administrator == True:  
      session_query = {"OWNER": str(ctx.author), "AVAILABLE": True}
      session = db.querySession(session_query)
      match_type = session['TYPE']
      invalid_user = False
      for u in user:
         user_query = ({'DISNAME': str(u)})
         resp = db.queryUser(user_query)
         if not resp:
            invalid_user = True
      
      if invalid_user:
         await ctx.send("You must first register before joining lobbies. ", delete_after=5)
      else:
         if match_type == 1:
            join_query = {"TEAM": [str(user[0])], "SCORE": 0, "POSITION": 1}
            session_joined = db.joinSession(session_query, join_query)
            await ctx.send(session_joined, delete_after=5)
         if match_type ==2:
            join_query = {"TEAM": [str(user[0]), (str(user[1]))], "SCORE": 0, "POSITION": 1}
            session_joined = db.joinSession(session_query, join_query)
            await ctx.send(session_joined, delete_after=5)
         if match_type ==3:
            join_query = {"TEAM": [str(user[0]), (str(user[1])), str(user[2])], "SCORE": 0, "POSITION": 1}
            session_joined = db.joinSession(session_query, join_query)
            await ctx.send(session_joined, delete_after=5)
         if match_type ==4:
            join_query = {"TEAM": [str(user[0]), (str(user[1])), str(user[2]), str(user[3])], "SCORE": 0, "POSITION": 1}
            session_joined = db.joinSession(session_query, join_query)
            await ctx.send(session_joined, delete_after=5)
         if match_type ==5:
            join_query = {"TEAM": [str(user[0]), (str(user[1])), str(user[2]), str(user[3]), str(user[4])], "SCORE": 0, "POSITION": 1}
            session_joined = db.joinSession(session_query, join_query)
            await ctx.send(session_joined, delete_after=5)
   else:
      await ctx.send("Admin Only", delete_after=5)

      
''' How many times have I beaten someone '''
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

      message = f"{str(ctx.author.mention)} has defeated {str(user.mention)} {win_count} out of {total_games} matches!"
      if total_games == 0:
         message = "You two have not played each other. "
      await ctx.send(message)
   else:
      await ctx.send(m.GAME_NOT_DETECTED, delete_after=5)

# Check if User is hosting a session
@bot.command()
@commands.check(validate_user)
async def lo(ctx, user: User):
   session_owner = {'OWNER': str(user), "AVAILABLE": True}
   session = db.querySession(session_owner)
   if session:
      game_query = {'ALIASES': session['GAME']}
      game = db.queryGame(game_query)

      name = session['OWNER'].split("#",1)[0]
      games = game['GAME']
      avatar = game['IMAGE_URL']
      tournament = session['TOURNAMENT']
      scrim = session['SCRIM']
      kingsgambit = session['KINGSGAMBIT']
      goc = session['GOC']
      gocname = session['GOC_TITLE']
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
         stype = ":medal:"
      elif session['RANKED'] == False:
         ranked = "Normal"
         stype = ":crossed_swords:"

      teams = [x for x in session['TEAMS']]
    
      team_list = []
      team_1 = [x for x in teams if x['POSITION'] == 0] # position 0
      team_2 = [x for x in teams if x['POSITION'] == 1] # position 1
      other_teams = [x for x in teams if x['POSITION'] > 1] # position 1

      team_1_comp_with_ign = []
      team_2_comp_with_ign = []

      team_1_score = ""
      team_2_score = ""

      king_score = 0

      other_teams_comp = []

      for x in team_1:
         # n = x['TEAM'].split("#",1)[1]
         team_1_score = f" Score: {x['SCORE']}"
         king_score = x['SCORE']
         for y in x['TEAM']:
            data = db.queryUser({'DISNAME': y})
            ign = ""
            for z in data['IGN']:
               if games in z:
                  ign = z[games]
                  team_1_comp_with_ign.append(f"{data['DISNAME']} : 🎮 {ign}".format(bot))
               else:
                  team_1_comp_with_ign.append(f"{data['DISNAME']}")
         team_1_comp = "\n".join(x['TEAM'])



      
      for x in team_2:
         team_2_score = f" Score: {x['SCORE']}"

         for y in x['TEAM']:
            data = db.queryUser({'DISNAME': y})
            ign = ""
            for z in data['IGN']:
               if games in z:
                  ign = z[games]
                  team_2_comp_with_ign.append(f"{data['DISNAME']} : 🎮 {ign}".format(bot))
               else:
                  team_2_comp_with_ign.append(f"{data['DISNAME']}")


      if kingsgambit:
         for x in other_teams:
            p = x['POSITION']
            for a in x['TEAM']:
               other_teams_comp.append({a:p})

      other_teams_comp_to_str = dict(ChainMap(*other_teams_comp))
      n = dict(sorted(other_teams_comp_to_str.items(), key=lambda item: item[1]))
      other_teams_sorted_list = "\n".join(f'{k}' for k,v in n.items())

      embedVar = discord.Embed(title=f"{name}'s {games} Session ".format(bot), description="Party Chat Gaming Database", colour=000000)
      embedVar.set_thumbnail(url=avatar)
      embedVar.add_field(name="Match ", value=f'{game_type}'.format(bot))
      embedVar.add_field(name="Type: " + stype , value=f'{ranked}'.format(bot))
      if tournament:
         embedVar.add_field(name="Tournament", value="Yes")
      
      if kingsgambit:
         embedVar.add_field(name="Kings Gambit", value="Yes")

      if scrim:
         embedVar.add_field(name="Scrim", value="Yes")
      
      if goc:
         embedVar.add_field(name="GODS OF COD : " + f"{gocname}", value="Yes")
      
      if kingsgambit and king_score > 0:
         embedVar.add_field(name=f":crown:King - {team_1_score}", value="\n".join(team_1_comp_with_ign), inline=False)
      elif not team_1_score:
         embedVar.add_field(name=f":military_helmet:Team 1", value="Vacant", inline=False)
      else:
         embedVar.add_field(name=f":military_helmet:Team 1 - {team_1_score}", value="\n".join(team_1_comp_with_ign), inline=False)
      
      if team_2_comp_with_ign:
         embedVar.add_field(name=f":military_helmet:Team 2 - {team_2_score}", value="\n".join(team_2_comp_with_ign), inline=False)
      else:
         embedVar.add_field(name=f":military_helmet:Team 2", value="Vacant", inline=False)

      if kingsgambit and other_teams:
         embedVar.add_field(name=f"Up Next...", value=other_teams_sorted_list, inline=False)

      await ctx.send(embed=embedVar, delete_after=15)
   else:
      await ctx.send(m.SESSION_DOES_NOT_EXIST, delete_after=5)

# Check your current session
@bot.command()
@commands.check(validate_user)
async def ml(ctx):  
   session_owner = {'OWNER': str(ctx.author), "AVAILABLE": True}
   session = db.querySession(session_owner)

   if session:
      game_query = {'ALIASES': session['GAME']}
      game = db.queryGame(game_query)
      tournament = session['TOURNAMENT']
      kingsgambit = session['KINGSGAMBIT']
      scrim = session['SCRIM']
      name = session['OWNER'].split("#",1)[0]
      games = game['GAME']
      avatar = game['IMAGE_URL']
      goc = session['GOC']
      gocname = session['GOC_TITLE']
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
         stype = ":medal:"
      elif session['RANKED'] == False:
         ranked = "Normal"
         stype = ":crossed_swords:"

      teams = [x for x in session['TEAMS']]
    
      team_list = []
      team_1 = [x for x in teams if x['POSITION'] == 0] # position 0
      team_2 = [x for x in teams if x['POSITION'] == 1] # position 1
      other_teams = [x for x in teams if x['POSITION'] > 1]



      team_1_comp_with_ign = []
      team_2_comp_with_ign = []

      team_1_score = ""
      team_2_score = ""

      king_score = 0

      other_teams_comp = []

      for x in team_1:
         # n = x['TEAM'].split("#",1)[1]
         team_1_score = f" Score: {x['SCORE']}"
         king_score = x['SCORE']
         for y in x['TEAM']:
            data = db.queryUser({'DISNAME': y})
            ign = ""
            for z in data['IGN']:
               if games in z:
                  ign = z[games]
                  team_1_comp_with_ign.append(f"{data['DISNAME']} : 🎮 {ign}".format(bot))
               else:
                  team_1_comp_with_ign.append(f"{data['DISNAME']}")
         team_1_comp = "\n".join(x['TEAM'])



      
      for x in team_2:
         team_2_score = f" Score: {x['SCORE']}"

         for y in x['TEAM']:
            data = db.queryUser({'DISNAME': y})
            ign = ""
            for z in data['IGN']:
               if games in z:
                  ign = z[games]
                  team_2_comp_with_ign.append(f"{data['DISNAME']} : 🎮 {ign}".format(bot))
               else:
                  team_2_comp_with_ign.append(f"{data['DISNAME']}")


      if kingsgambit:
         for x in other_teams:
            p = x['POSITION']
            for a in x['TEAM']:
               other_teams_comp.append({a:p})

      other_teams_comp_to_str = dict(ChainMap(*other_teams_comp))
      n = dict(sorted(other_teams_comp_to_str.items(), key=lambda item: item[1]))
      other_teams_sorted_list = "\n".join(f'{k}' for k,v in n.items())

      embedVar = discord.Embed(title=f"{name}'s {games} Session ".format(bot), description="Party Chat Gaming Database", colour=000000)
      embedVar.set_thumbnail(url=avatar)
      embedVar.add_field(name="Match ", value=f'{game_type}'.format(bot))
      embedVar.add_field(name="Type: " + stype , value=f'{ranked}'.format(bot))
      if tournament:
         embedVar.add_field(name="Tournament", value="Yes")
      
      if kingsgambit:
         embedVar.add_field(name="Kings Gambit", value="Yes")

      if scrim:
         embedVar.add_field(name="Scrim", value="Yes")

      if goc:
         embedVar.add_field(name="GODS OF COD : " + f"{gocname}", value="Yes")
      
      if kingsgambit and king_score > 0:
         embedVar.add_field(name=f":crown:King - {team_1_score}", value="\n".join(team_1_comp_with_ign), inline=False)
      elif not team_1_score:
         embedVar.add_field(name=f":military_helmet:Team 1", value="Vacant", inline=False)
      else:
         embedVar.add_field(name=f":military_helmet:Team 1 - {team_1_score}", value="\n".join(team_1_comp_with_ign), inline=False)
      
      if team_2_comp_with_ign:
         embedVar.add_field(name=f":military_helmet:Team 2 - {team_2_score}", value="\n".join(team_2_comp_with_ign), inline=False)
      else:
         embedVar.add_field(name=f":military_helmet:Team 2", value="Vacant", inline=False)

      if kingsgambit and other_teams:
         embedVar.add_field(name=f"Up Next...", value=other_teams_sorted_list, inline=False)

      await ctx.send(embed=embedVar, delete_after=120)
   else:
      await ctx.send(m.SESSION_DOES_NOT_EXIST, delete_after=5)


# Check What Session A Player Is In
@bot.command()
@commands.check(validate_user)
async def cl(ctx, user: User):
   current_session = {'TEAMS.TEAM': str(user), "AVAILABLE": True}
   session = db.querySessionMembers(current_session)
   if session:
      game_query = {'ALIASES': session['GAME']}
      game = db.queryGame(game_query)

      name = session['OWNER'].split("#",1)[0]
      games = game['GAME']
      avatar = game['IMAGE_URL']
      tournament = session['TOURNAMENT']
      
      scrim = session['SCRIM']
      kingsgambit = session['KINGSGAMBIT']
      goc = session['GOC']
      gocname = session['GOC_TITLE']
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
         stype = ":medal:"
      elif session['RANKED'] == False:
         ranked = "Normal"
         stype = ":crossed_swords:"

      teams = [x for x in session['TEAMS']]
    
      team_list = []
      team_1 = [x for x in teams if x['POSITION'] == 0] # position 0
      team_2 = [x for x in teams if x['POSITION'] == 1] # position 1
      other_teams = [x for x in teams if x['POSITION'] > 1] # position 1




      team_1_comp_with_ign = []
      team_2_comp_with_ign = []

      team_1_score = ""
      team_2_score = ""

      king_score = 0

      other_teams_comp = []

      for x in team_1:
         # n = x['TEAM'].split("#",1)[1]
         team_1_score = f" Score: {x['SCORE']}"
         king_score = x['SCORE']
         for y in x['TEAM']:
            data = db.queryUser({'DISNAME': y})
            ign = ""
            for z in data['IGN']:
               if games in z:
                  ign = z[games]
                  team_1_comp_with_ign.append(f"{data['DISNAME']} : 🎮 {ign}".format(bot))
               else:
                  team_1_comp_with_ign.append(f"{data['DISNAME']}")
         team_1_comp = "\n".join(x['TEAM'])



      
      for x in team_2:
         team_2_score = f" Score: {x['SCORE']}"

         for y in x['TEAM']:
            data = db.queryUser({'DISNAME': y})
            ign = ""
            for z in data['IGN']:
               if games in z:
                  ign = z[games]
                  team_2_comp_with_ign.append(f"{data['DISNAME']} : 🎮 {ign}".format(bot))
               else:
                  team_2_comp_with_ign.append(f"{data['DISNAME']}")


      if kingsgambit:
         for x in other_teams:
            p = x['POSITION']
            for a in x['TEAM']:
               other_teams_comp.append({a:p})

      other_teams_comp_to_str = dict(ChainMap(*other_teams_comp))
      n = dict(sorted(other_teams_comp_to_str.items(), key=lambda item: item[1]))
      other_teams_sorted_list = "\n".join(f'{k}' for k,v in n.items())

      embedVar = discord.Embed(title=f"{name}'s {games} Lobby ".format(bot), description="Party Chat Gaming Database", colour=000000)
      embedVar.set_thumbnail(url=avatar)
      embedVar.add_field(name="Match ", value=f'{game_type}'.format(bot))
      embedVar.add_field(name="Type: " + stype , value=f'{ranked}'.format(bot))
      if tournament:
         embedVar.add_field(name="Tournament", value="Yes")
      
      if kingsgambit:
         embedVar.add_field(name="Kings Gambit", value="Yes")

      if scrim:
         embedVar.add_field(name="Scrim", value="Yes")
      if goc:
         embedVar.add_field(name="GODS OF COD : " + f"{gocname}", value="Yes")
      
      if kingsgambit and king_score > 0:
         embedVar.add_field(name=f":crown:King - {team_1_score}", value="\n".join(team_1_comp_with_ign), inline=False)
      elif not team_1_score:
         embedVar.add_field(name=f":military_helmet:Team 1", value="Vacant", inline=False)
      else:
         embedVar.add_field(name=f":military_helmet:Team 1 - {team_1_score}", value="\n".join(team_1_comp_with_ign), inline=False)
      
      if team_2_comp_with_ign:
         embedVar.add_field(name=f":military_helmet:Team 2 - {team_2_score}", value="\n".join(team_2_comp_with_ign), inline=False)
      else:
         embedVar.add_field(name=f":military_helmet:Team 2", value="Vacant", inline=False)

      if kingsgambit and other_teams:
         embedVar.add_field(name=f"Up Next...", value=other_teams_sorted_list, inline=False)

      await ctx.send(embed=embedVar, delete_after=15)
   else:
      await ctx.send(m.SESSION_DOES_NOT_EXIST, delete_after=5)

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

async def sw(ctx):
   session_query = {"OWNER": str(ctx.author), "AVAILABLE": True}
   session_data = db.querySession(session_query)
   teams = [x for x in session_data['TEAMS']]
   winning_team = {}
   blessings = 0
   high_score = teams[0]['SCORE']
   for x in teams:
      if x['SCORE'] >= high_score:
         high_score = x['SCORE']
         winning_team = x
   session_data['WINNER'] = winning_team
   winner = session_data['WINNER']
   session = session_data
   
   players_team_name = ""
   update_query = {}
   add_score_to_team={}
   if session_data['GOC']:
      blessings = blessings + 10000
      for x in winning_team['TEAM']:
         player = db.queryUser({'DISNAME': x})
         players_team_name = player['TEAM']
         update_query = {'$set': {'WINNER': winner, 'WINNING_TEAM': players_team_name}}
         add_score_to_team = {'$inc': {'TOURNAMENT_WINS': 1}}       
   elif session_data['SCRIM']:
      for x in winning_team['TEAM']:
         player = db.queryUser({'DISNAME': x})
         players_team_name = player['TEAM']
         update_query = {'$set': {'WINNER': winner, 'WINNING_TEAM': players_team_name}}
         add_score_to_team = {'$inc': {'SCRIM_WINS': 1}}
   else:
      update_query = {'$set': {'WINNER': winner}}

   query = {"_id": session_data["_id"]}
   db.updateSession(session, query, update_query)
   db.updateTeam({'TNAME': players_team_name}, add_score_to_team)
   game_type = ""

   if session['TYPE'] == 1:
      game_type = "1v1"
      blessings = blessings + 10
   elif session['TYPE'] == 2:
      game_type = "2v2"
      blessings = blessings + 15
   elif session['TYPE'] == 3:
      game_type = "3v3"
      blessings = blessings + 30
   elif session['TYPE'] == 4:
      game_type = "4v4"
      blessings = blessings + 40
   elif session['TYPE'] == 5:
      game_type = "5v5"
      blessings = blessings + 50
   for x in winning_team['TEAM']:
      player = db.queryUser({'DISNAME': x})
      winner_earned_tourney_cards = False
      winner_earned_tourney_titles = False
      goc_player_team = player['TEAM']

      tourney_cards = db.queryTournamentCards()
      tourney_titles = db.queryTournamentTitles()

      types_of_matches_list = [x for x in player['NORMAL']]
      types_of_matches = dict(ChainMap(*types_of_matches_list))
      current_score = types_of_matches[game_type.upper()]
      query = {'DISNAME': player['DISNAME']}
      #uid = {'DID' : player['DID']}
      
      new_value = {}
      if session_data['TOURNAMENT']:
         new_value = {"$inc": {'TOURNAMENT_WINS': 1}}
         blessings = blessings + 100

      elif session_data['RANKED']:
         new_value = {"$inc": {'RANKED.$[type].' + game_type.upper() + '.0': 1}}
         blessings = blessings + (.30*blessings)

      elif not session_data['RANKED']:
         new_value = {"$inc": {'NORMAL.$[type].' + game_type.upper() + '.0': 1}}

      filter_query = [{'type.' + game_type.upper(): current_score}]

      if session_data['TOURNAMENT']:
         db.updateUserNoFilter(query, new_value)

         # Add new tourney cards to winner vault if applicable

         vault_query = {'OWNER' : x}
         vault = db.altQueryVault(vault_query)
         cards = []
         titles = []
         for card in tourney_cards:
            if player['TOURNAMENT_WINS'] == (card['TOURNAMENT_REQUIREMENTS'] - 1):
               cards.append(card['NAME'])

         for title in tourney_titles:
            if player['TOURNAMENT_WINS'] == (title['TOURNAMENT_REQUIREMENTS'] - 1):
               titles.append(title['TITLE']) 

         if bool(cards):
            winner_earned_tourney_cards=True
            for card in cards:
               db.updateVaultNoFilter(vault_query, {'$addToSet':{'CARDS': card}})

         if bool(titles):
            winner_earned_tourney_titles=True
            for title in titles:
               db.updateVaultNoFilter(vault_query, {'$addToSet':{'TITLES': title}})
         else:
            print("No update")
      else:
         db.updateUser(query, new_value, filter_query)
      
      uid = player['DID']
      user = await bot.fetch_user(uid)
      await bless(blessings, player['DISNAME'])

      await DM(ctx, user, "You Won. Doesnt Prove Much Tho :yawning_face:")

      if winner_earned_tourney_cards or winner_earned_tourney_titles:
         await ctx.send(f"Competitor " + f"{user.mention}" + " earns a victory ! :100:", delete_after=5)
         await ctx.send( f"{user.mention}" + "You have Unlocked New Items in your Vault! :eyes:", delete_after=5)
      else:
         await ctx.send(f"Competitor " + f"{user.mention}" + " earns a victory ! :100:", delete_after=5)

async def altsl(ctx):
   session_query = {"OWNER": str(ctx.author), "AVAILABLE": True}
   session_data = db.querySession(session_query)
   if session_data['KINGSGAMBIT']:
      return await ctx.send("Lobby has ended. See you for the next Kings Gambit!")
   else:
      teams = [x for x in session_data['TEAMS']]
      losing_team = {}
      losing_kingsgambit_teams = []
      low_score = teams[0]['SCORE']

      for x in teams:
         if x['SCORE'] <= low_score:
            low_score = x['SCORE']
            losing_team = x
      session_data['LOSER'] = losing_team
      loser = session_data['LOSER']
      session = session_data
      
      players_team_name = ""
      update_query = {}
      add_score_to_team={}
      if session_data['GOC']:
         for x in losing_team['TEAM']:
            player = db.queryUser({'DISNAME': x})
            players_team_name = player['TEAM']
            update_query = {'$set': {'LOSER': loser, 'LOSING_TEAM': players_team_name}}       
      elif session_data['SCRIM']:
         for x in losing_team['TEAM']:
            player = db.queryUser({'DISNAME': x})
            players_team_name = player['TEAM']
            update_query = {'$set': {'LOSER': loser, 'LOSING_TEAM': players_team_name}}
            add_score_to_team = {'$inc': {'SCRIM_LOSSES': 1}}
      else:
         update_query = {'$set': {'LOSER': loser}}

      query = {"_id": session_data["_id"], "TEAMS.TEAM": str(ctx.author)}
      db.updateSession(session, query, update_query)
      blah = db.updateTeam({'TNAME': players_team_name}, add_score_to_team)
      game_type = ""

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

      for x in losing_team['TEAM']:
         player = db.queryUser({'DISNAME': x})
         winner_earned_tourney_cards = False
         winner_earned_tourney_titles = False
         goc_player_team = player['TEAM']

         tourney_cards = db.queryTournamentCards()
         tourney_titles = db.queryTournamentTitles()

         types_of_matches_list = [x for x in player['NORMAL']]
         types_of_matches = dict(ChainMap(*types_of_matches_list))
         current_score = types_of_matches[game_type.upper()]
         query = {'DISNAME': player['DISNAME']}
         #uid = {'DID' : player['DID']}
         
         new_value = {}
         if session_data['TOURNAMENT']:
            new_value = {"$inc": {'TOURNAMENT_WINS': 0}}

         elif session_data['RANKED']:
            new_value = {"$inc": {'RANKED.$[type].' + game_type.upper() + '.1': 1}}

         elif not session_data['RANKED']:
            new_value = {"$inc": {'NORMAL.$[type].' + game_type.upper() + '.1': 1}}

         filter_query = [{'type.' + game_type.upper(): current_score}]

         if session_data['TOURNAMENT']:
            db.updateUserNoFilter(query, new_value)
         else:
            db.updateUser(query, new_value, filter_query)

         uid = player['DID']
         user = await bot.fetch_user(uid)
         await curse(5, user)
         await DM(ctx, user, "You Lost. Get back in there :poop:")
         await ctx.send(f"Competitor " + f"{user.mention}" + " took another L! :eyes:", delete_after=5)

async def DM(ctx, user : User, m,  message=None):
    message = message or "This Message is sent via DM"
    await user.send(m)

'''
1V1 ADMIN TOURNAMENTS
Admin will create the session, users will join session via invite, users will submit screenshot (or admin will watch) and score based on winner
'''
@bot.command()
@commands.check(validate_user)
async def e(ctx):
   if ctx.author.guild_permissions.administrator == True:
      game = [x for x in db.query_all_games()][0]
      session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 1, "TEAMS": [], "RANKED": True, "TOURNAMENT": True, }
      resp = db.createSession(data.newSession(session_query))
      await ctx.send(resp, delete_after=5)
   else:
      await ctx.send(m.ADMIN_ONLY_COMMAND)



@bot.command()
@commands.check(validate_user)
async def einvite(ctx, user1: User):
   if ctx.author.guild_permissions.administrator == True:
      game = [x for x in db.query_all_games()][0]
      
      validate_opponent = db.queryUser({'DISNAME': str(user1)})

      if validate_opponent:
         await DM(ctx, user1, f"{ctx.author.mention}" + " has invited you to a Tournament Match :eyes:")
         accept = await ctx.send(f"{user1.mention}, Will you join the Exhibition? :fire:", delete_after=15)
         for emoji in emojis:
            await accept.add_reaction(emoji)

         def check(reaction, user):
            return user == user1 and str(reaction.emoji) == '👍'
         try:
            reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=check)

            session_query = {"OWNER": str(ctx.author),"TOURNAMENT": True , "AVAILABLE": True}
            session_data = db.querySession(session_query)
            teams_list = [x for x in session_data['TEAMS']]
            positions = []
            new_position = 0
            if bool(teams_list):
               for x in teams_list:
                  positions.append(x['POSITION'])
               new_position = max(positions) + 1

            join_query = {"TEAM": [str(user1)], "SCORE": 0, "POSITION": new_position}
            resp = db.joinExhibition(session_query, join_query)
            await ctx.send(resp, delete_after=5)
         except:
            await ctx.send("User did not accept.")
      else:
         await ctx.send(m.USER_NOT_REGISTERED, delete_after=5)
   else:
      await ctx.send(m.ADMIN_ONLY_COMMAND)

if config('ENV') == "production":
   DISCORD_TOKEN = config('DISCORD_TOKEN_TEST')
else:
   DISCORD_TOKEN = config('DISCORD_TOKEN_FOR_TESTING')

bot.run(DISCORD_TOKEN)