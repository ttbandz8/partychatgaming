import db
import time
import classes as data
import test_data as td
import discord
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw

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
emojis = ['👍', '👎']

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
      ranked = d['RANKED']
      normal = d['NORMAL']
      tournament_wins = d['TOURNAMENT_WINS']


      ranked_to_string = dict(ChainMap(*ranked))
      normal_to_string = dict(ChainMap(*normal))
      ign_to_string = dict(ChainMap(*ign))


      

      embedVar = discord.Embed(title=f"{name}'s Profile Card".format(client), description="Party Chat Gaming Database", colour=000000)
      embedVar.set_thumbnail(url=avatar)
      embedVar.add_field(name="Game", value=' '.join(str(x) for x in games))
      embedVar.add_field(name="In-Game Name", value="\n".join(f'{v}' for k,v in ign_to_string.items()))
      embedVar.add_field(name="Teams", value=' '.join(str(x) for x in teams))
      embedVar.add_field(name="Titles", value=' '.join(str(x) for x in titles))
      embedVar.add_field(name="Ranked", value="\n".join(f'{k}: {"/".join([str(int) for int in v])}' for k,v in ranked_to_string.items()))
      embedVar.add_field(name="Normals", value="\n".join(f'{k}: {"/".join([str(int) for int in v])}' for k,v in normal_to_string.items()))
      embedVar.add_field(name="Tournament Wins", value=tournament_wins)
      await ctx.send(embed=embedVar, delete_after=15)
   else:
      await ctx.send("User does not exist in the system. ", delete_after=3)

'''TITLES'''
@bot.command()
@commands.check(validate_user)
async def nt(ctx, args1: str, args2: int, args3: int, args4: int):
   if ctx.author.guild_permissions.administrator == True:
      title_query = {'TITLE': str(args1), 'WINS_REQUIREMENTS': int(args2), 'TOURNAMENT_REQUIREMENTS': int(args3), 'TIER': int(args4)}
      added = db.createTitle(data.newTitle(title_query))
      await ctx.send(added, delete_after=3)
   else:
      print("Nah Nigga this ain't going down like you think pussy boy")

@bot.command()
@commands.check(validate_user)
async def at(ctx):
   user_query = {'DISNAME': str(ctx.author)}
   user = db.queryUser(user_query)
   tournament_wins = user['TOURNAMENT_WINS']
   # card_query = {'TOURNAMENT_REQUIREMENTS': tournament_wins}
   resp = db.queryAllTitles()
   titles = []
   unavailable_titles = []
   for title in resp:
      if tournament_wins >= title['TOURNAMENT_REQUIREMENTS']:
         titles.append(title['TITLE'])
   
   embedVar = discord.Embed(title=f"Your Available Titles", description="Titles are earned through valor and tournament achievements.", colour=000000)
   embedVar.add_field(name="Unlocked Titles", value="\n".join(titles))
   await ctx.send(embed=embedVar, delete_after=15)

@bot.command()
@commands.check(validate_user)
async def ut(ctx, args):
   user_query = {'DISNAME': str(ctx.author)}
   user = db.queryUser(user_query)
   tournament_wins = user['TOURNAMENT_WINS']
   title_query = {'TOURNAMENT_REQUIREMENTS': tournament_wins}
   resp = db.queryAllTitles()
   titles = []
   for title in resp:
      if tournament_wins >= title['TOURNAMENT_REQUIREMENTS']:
         titles.append(title['TITLE'])
   if args in titles:
      response = db.updateUserNoFilter(user_query, {'$set': {'TITLE': args}})
      await ctx.send(response)
   else:
      return "Unable to update title."

'''CARDS'''
@bot.command()
@commands.check(validate_user)
async def nc(ctx, args1: str, args2: str, args3: int, args4: int, args5: int):
   if ctx.author.guild_permissions.administrator == True:
      card_query = {'PATH': str(args1), 'NAME': str(args2), 'WINS_REQUIREMENTS': int(args3), 'TOURNAMENT_REQUIREMENTS': int(args4), 'TIER': int(args5)}
      added = db.createCard(data.newCard(card_query))
      await ctx.send(added, delete_after=3)
   else:
      print("Nah Nigga this ain't going down like you think pussy boy")


@bot.command()
@commands.check(validate_user)
async def ac(ctx):
   user_query = {'DISNAME': str(ctx.author)}
   user = db.queryUser(user_query)
   tournament_wins = user['TOURNAMENT_WINS']
   # card_query = {'TOURNAMENT_REQUIREMENTS': tournament_wins}
   resp = db.queryAllCards()
   cards = []
   unavailable_cards = []
   for card in resp:
      if tournament_wins >= card['TOURNAMENT_REQUIREMENTS']:
         cards.append(card['NAME'])
   
   embedVar = discord.Embed(title=f"Your Available Cards", description="Cards are earned through valor and tournament achievements.", colour=000000)
   embedVar.add_field(name="Unlocked Cards", value="\n".join(cards))
   await ctx.send(embed=embedVar, delete_after=15)


@bot.command()
@commands.check(validate_user)
async def uc(ctx, args):
   user_query = {'DISNAME': str(ctx.author)}
   user = db.queryUser(user_query)
   tournament_wins = user['TOURNAMENT_WINS']
   card_query = {'TOURNAMENT_REQUIREMENTS': tournament_wins}
   resp = db.queryAllCards()
   cards = []
   for card in resp:
      if tournament_wins >= card['TOURNAMENT_REQUIREMENTS']:
         cards.append(card['NAME'])
   if args in cards:
      response = db.updateUserNoFilter(user_query, {'$set': {'CARD': args}})
      await ctx.send(response)
   else:
      return "Unable to update card."
 

@bot.command()
async def flex(ctx):
   query = {'DISNAME': str(ctx.author)}
   d = db.queryUser(query)

   card = db.queryCard({'NAME': d['CARD']})

   if d:
      name = d['DISNAME'].split("#",1)[0]
      games = d['GAMES']
      ign = d['IGN']
      teams = d['TEAMS']
      title = d['TITLE']
      avatar = d['AVATAR']
      ranked = d['RANKED']
      normal = d['NORMAL']
      tournament_wins = d['TOURNAMENT_WINS']


      ranked_to_string = dict(ChainMap(*ranked))
      normal_to_string = dict(ChainMap(*normal))
      ign_to_string = dict(ChainMap(*ign))

      game_text = ' '.join(str(x) for x in games)
      titles_text = ' '.join(str(x) for x in title)
      teams_text = ' '.join(str(x) for x in teams)
      normals_text = "\n".join(f'{k}: {"/".join([str(int) for int in v])}' for k,v in normal_to_string.items())
      ranked_text = "\n".join(f'{k}: {"/".join([str(int) for int in v])}' for k,v in ranked_to_string.items())

      
      img = Image.open(requests.get(card['PATH'], stream=True).raw)

      draw = ImageDraw.Draw(img)
      header = ImageFont.truetype("KomikaTitle-Paint.ttf", 60)
      tournament_wins_font = ImageFont.truetype("RobotoCondensed-Bold.ttf", 35)
      p = ImageFont.truetype("Roboto-Bold.ttf", 25)

      profile_pic = Image.open(requests.get(d['AVATAR'], stream=True).raw)
      profile_pic_resized = profile_pic.resize((120, 120), resample=0)
      img.paste(profile_pic_resized, (1045, 30))
      draw.text((95,45), name, (255, 255, 255), font=header, align="left")
      draw.text((5,65), str(tournament_wins), (255, 255, 255), font=tournament_wins_font, align="center")
      draw.text((60, 320), game_text, (255, 255, 255), font=p, align="center")
      draw.text((368, 320), teams_text, (255, 255, 255), font=p, align="center")
      draw.text((650, 320), titles_text, (255, 255, 255), font=p, align="center")
      draw.text((865, 320), normals_text, (255, 255, 255), font=p, align="center")
      draw.text((1040, 320), ranked_text, (255, 255, 255), font=p, align="center")

      img.save("text.png")

      await ctx.send(file=discord.File("text.png"))



      

      # embedVar = discord.Embed(title=f"My Profile Card", description="Party Chat Gaming Database", colour=000000)
      # embedVar.set_thumbnail(url=avatar)
      # embedVar.add_field(name="Game", value=' '.join(str(x) for x in games))
      # embedVar.add_field(name="In-Game Name", value="\n".join(f'{v}' for k,v in ign_to_string.items()))
      # embedVar.add_field(name="Teams", value=' '.join(str(x) for x in teams))
      # embedVar.add_field(name="Titles", value=' '.join(str(x) for x in titles))
      # embedVar.add_field(name="Ranked", value="\n".join(f'{k}: {"/".join([str(int) for int in v])}' for k,v in ranked_to_string.items()))
      # embedVar.add_field(name="Normals", value="\n".join(f'{k}: {"/".join([str(int) for int in v])}' for k,v in normal_to_string.items()))
      # embedVar.add_field(name="Tournament Wins", value=tournament_wins)
      # await ctx.send(embed=embedVar, delete_after=15)
   else:
      await ctx.send("User does not exist in the system. ", delete_after=3)



@bot.command()
async def r(ctx):
   user = {'DISNAME': str(ctx.author), 'AVATAR': str(ctx.author.avatar_url)}
   response = db.createUsers(data.newUser(user))
   await ctx.send(response, delete_after=5)


'''delete user'''
@bot.command()
@commands.check(validate_user)
async def d(ctx, user: User, args):
   if args == 'IWANTTODELETEMYACCOUNT':
      if str(ctx.author) == str(user):
         query = {'DISNAME': str(ctx.author)}
         user_is_validated = db.queryUser(query)
         if user_is_validated:
            delete_user_resp = db.deleteUser(query)
            await ctx.send(delete_user_resp, delete_after=5)
   else:
      await ctx.send("Invalid command", delete_after=5)


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
            resp = db.updateUserNoFilter(user, query_to_update_game)
            ctx.send(resp, delete_after=5)
         else:
            query_to_update_game = {"$addToSet": {"GAMES": title}}
            resp = db.updateUserNoFilter(user, query_to_update_game)
            ctx.send(resp, delete_after=5)
      elif title not in user_data['GAMES'] and ign == True:
         if "PCG" in user_data['GAMES']:
            query_to_update_game = {"$set": {"GAMES": [title], "IGN": [{title : args[1]}]}}
            resp = db.updateUserNoFilter(user, query_to_update_game)
            await ctx.send(resp, delete_after=5)
         else:

            query_to_update_game = {"$addToSet": {"GAMES": title, "IGN": {title : args[1]}}}
            resp = db.updateUserNoFilter(user, query_to_update_game)
            await ctx.send(resp, delete_after=5)

@bot.command()
@commands.check(validate_user)
async def uign(ctx, args1, args2):
   user = {'DISNAME': str(ctx.author)}
   aliases = [x for x in db.query_all_games() for x in x['ALIASES']]
   new_ign = args2
   if args1 in aliases:
      game_query = {'ALIASES': args1}
      game = db.queryGame(game_query)
      title = game['GAME']
      ign = game['IGN']
      if ign:
         update_query = {"$set": {"IGN": [{title : new_ign}]}}
         updated = db.updateUserNoFilter(user, update_query)
         await ctx.send(updated)
      else:
         await ctx.send("In Game Names unavailable for this game. ", delete_after=3)
   else:
      await ctx.send("Game is unavailable. ", delete_after=3)
   

@bot.command()
@commands.check(validate_user)
async def c1v1(ctx, args):
   game = [x for x in db.query_all_games()][0]
   session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 1, "TEAMS": [{"TEAM": [str(ctx.author)], "SCORE": 0, "POSITION": 0}]}
   if args == "n":
      resp = db.createSession(data.newSession(session_query))
      await ctx.send(resp, delete_after=5)
   elif args == "r":
      session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 1, "TEAMS": [{"TEAM": [str(ctx.author)], "SCORE": 0, "POSITION": 0}], "RANKED": True}
      resp = db.createSession(data.newSession(session_query))
      await ctx.send(resp, delete_after=5)


@bot.command()
@commands.check(validate_user)
async def c2v2(ctx, args, user1: User):
   game = [x for x in db.query_all_games()][0]
   
   validate_teammate = db.queryUser({'DISNAME': str(user1)})

   if validate_teammate:
      accept = await ctx.send("Will you join the session?", delete_after=10)
      for emoji in emojis:
         await accept.add_reaction(emoji)

      def check(reaction, user):
         return user == user1 and str(reaction.emoji) == '👍'

      try:
         reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=check)


         session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 2, "TEAMS": [{"TEAM": [str(ctx.author), str(user1)], "SCORE": 0, "POSITION": 0}]}
         if args == "n":
            resp = db.createSession(data.newSession(session_query))
            await ctx.send(resp, delete_after=5)
         elif args == "r":
            session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 2, "TEAMS": [{"TEAM": [str(ctx.author), str(user1)], "SCORE": 0, "POSITION": 0}], "RANKED": True}
            resp = db.createSession(data.newSession(session_query))
            await ctx.send(resp, delete_after=5)
      except:
         await ctx.send("Did not work")
   else:
      await ctx.send("Users must register.", delete_after=5)

@bot.command()
@commands.check(validate_user)
async def c3v3(ctx, args, user1: User, user2: User):
   game = [x for x in db.query_all_games()][0]
   
   teammates = [str(user1), str(user2)]
   valid_teammates = []
   for x in teammates:
      valid = db.queryUser(x)
      if valid:
         valid_teammates.append(valid["DISNAME"])
      else:
         await ctx.send(f"{valid['DISNAME']} needs to register.".format(bot), delete_after=5)

   if valid_teammates:
      accept = await ctx.send("Will you join the session?", delete_after=10)
      for emoji in emojis:
         await accept.add_reaction(emoji)

      def check(reaction, user):
         return user in valid_teammates and str(reaction.emoji) == '👍'

      try:
         reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=check)


         session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 2, "TEAMS": [{"TEAM": [str(ctx.author), str(user1), str(user2)], "SCORE": 0, "POSITION": 0}]}
         if args == "n":
            resp = db.createSession(data.newSession(session_query))
            await ctx.send(resp, delete_after=5)
         elif args == "r":
            session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 2, "TEAMS": [{"TEAM": [str(ctx.author), str(user1), str(user2)], "SCORE": 0, "POSITION": 0}], "RANKED": True}
            resp = db.createSession(data.newSession(session_query))
            await ctx.send(resp, delete_after=5)
      except:
         await ctx.send("Did not work")
   else:
      await ctx.send("Users must register.", delete_after=5)


@bot.command()
@commands.check(validate_user)
async def c4v4(ctx, args, user1: User, user2: User, user3: User):
   game = [x for x in db.query_all_games()][0]
   
   teammates = [str(user1), str(user2), str(user3)]
   valid_teammates = []
   for x in teammates:
      valid = db.queryUser(x)
      if valid:
         valid_teammates.append(valid["DISNAME"])
      else:
         await ctx.send(f"{valid['DISNAME']} needs to register.".format(bot), delete_after=5)

   if valid_teammates:
      accept = await ctx.send("Will you join the session?", delete_after=10)
      for emoji in emojis:
         await accept.add_reaction(emoji)

      def check(reaction, user):
         return user in valid_teammates and str(reaction.emoji) == '👍'

      try:
         reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=check)


         session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 2, "TEAMS": [{"TEAM": [str(ctx.author), str(user1), str(user2), str(user3)], "SCORE": 0, "POSITION": 0}]}
         if args == "n":
            resp = db.createSession(data.newSession(session_query))
            await ctx.send(resp, delete_after=5)
         elif args == "r":
            session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 2, "TEAMS": [{"TEAM": [str(ctx.author), str(user1), str(user2), str(user3)], "SCORE": 0, "POSITION": 0}], "RANKED": True}
            resp = db.createSession(data.newSession(session_query))
            await ctx.send(resp, delete_after=5)
      except:
         await ctx.send("Did not work")
   else:
      await ctx.send("Users must register.", delete_after=5)


@bot.command()
@commands.check(validate_user)
async def c5v5(ctx, args, user1: User, user2: User, user3: User, user4: User):
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
      accept = await ctx.send("Will you join the session?", delete_after=10)
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
         await ctx.send("Did not work")
   else:
      await ctx.send("Users must register.", delete_after=5)


@bot.command()
@commands.check(validate_user)
async def score(ctx, user: User):
   session_query = {"OWNER": str(ctx.author), "AVAILABLE": True}
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
   name = reciever['DISNAME']#.split("#",1)[0]
   message = "You Scored, Don't Let Up"
   await DM(ctx, user, message)
  # DM(reciever,"You Scored, Keep it Up")
   if response:
      await ctx.send(f"+1", delete_after=2)
   else:
      await ctx.send(f"Score not added. Please, try again. ", delete_after=5)


@bot.command()
@commands.check(validate_user)
async def es(ctx):
   session_query = {"OWNER": str(ctx.author), "AVAILABLE": True}
   await sw(ctx)
   await sl(ctx)
   end = db.endSession(session_query)
   await ctx.send(end, delete_after=5)

@bot.command()
@commands.check(validate_user)
async def js(ctx, *user: User):
   session_query = {"OWNER": str(user[0]), "AVAILABLE": True}
   session = db.querySession(session_query)
   match_type = session['TYPE']
   if match_type == 1:
      join_query = {"TEAM": [str(ctx.author)], "SCORE": 0, "POSITION": 1}
      session_joined = db.joinSession(session_query, join_query)
      await ctx.send(session_joined, delete_after=5)
   if match_type ==2:
      join_query = {"TEAM": [str(ctx.author), (str(user[1]))], "SCORE": 0, "POSITION": 1}
      session_joined = db.joinSession(session_query, join_query)
      await ctx.send(session_joined, delete_after=5)


@bot.command()
@commands.check(validate_user)
async def s(ctx, user: User):
   session_owner = {'OWNER': str(user), "AVAILABLE": True}
   session = db.querySession(session_owner)
   if session:
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
         ranked = "Normal"

      teams = [x for x in session['TEAMS']]
      team_list = []
      for x in teams:
         print(x)
         for members in x['TEAM']:
            print(members)
            mem_query = db.queryUser({'DISNAME': members})
            ign_list = [x for x in mem_query['IGN']]
            ign_list_keys = [k for k in ign_list[0].keys()]
            if ign_list_keys == [games]:
               team_list.append(f"{ign_list[0][games]}: {x['SCORE']}")
            else:
               team_list.append(f"{members}: {x['SCORE']}")


      embedVar = discord.Embed(title=f"{name}'s {games} Session ".format(bot), description="Party Chat Gaming Database", colour=000000)
      embedVar.set_thumbnail(url=avatar)
      embedVar.add_field(name="Match Type", value=f'{game_type}'.format(bot))
      embedVar.add_field(name="Ranked", value=f'{ranked}'.format(bot))
      embedVar.add_field(name="Competitors", value="\n".join(f'{t}'.format(bot) for t in team_list), inline=False)
      await ctx.send(embed=embedVar, delete_after=15)
   else:
      await ctx.send("Session does not exist. ", delete_after=5)


@bot.command()
@commands.check(validate_user)
async def ms(ctx):
   session_owner = {'OWNER': str(ctx.author), "AVAILABLE": True}
   session = db.querySession(session_owner)
   if session:
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
         ranked = "Normal"

      teams = [x for x in session['TEAMS']]
      team_list = []
      for x in teams:
         print(x)
         for members in x['TEAM']:
            print(members)
            mem_query = db.queryUser({'DISNAME': members})
            ign_list = [x for x in mem_query['IGN']]
            ign_list_keys = [k for k in ign_list[0].keys()]
            if ign_list_keys == [games]:
               team_list.append(f"{ign_list[0][games]}: {x['SCORE']}")
            else:
               team_list.append(f"{members}: {x['SCORE']}")


      embedVar = discord.Embed(title=f"{name}'s {games} Session ".format(bot), description="Party Chat Gaming Database", colour=000000)
      embedVar.set_thumbnail(url=avatar)
      embedVar.add_field(name="Match Type", value=f'{game_type}'.format(bot))
      embedVar.add_field(name="Ranked", value=f'{ranked}'.format(bot))
      embedVar.add_field(name="Competitors", value="\n".join(f'{t}'.format(bot) for t in team_list), inline=False)
      await ctx.send(embed=embedVar, delete_after=15)
   else:
      await ctx.send("Session does not exist. ", delete_after=5)


@bot.command()
@commands.check(validate_user)
async def ct(ctx, args1, *args):
   game_query = {'ALIASES': args1}
   game = db.queryGame(game_query)['GAME']
   team_name = " ".join([*args])
   team_query = {'OWNER': str(ctx.author), 'TNAME': team_name, 'MEMBERS': [str(ctx.author)], 'GAMES': [game]}
   accept = await ctx.send(f"Do you want to create the {game} team {team_name}?".format(bot), delete_after=10)
   for emoji in emojis:
      await accept.add_reaction(emoji)

   def check(reaction, user):
      return user == ctx.author and str(reaction.emoji) == '👍'

   try:
      confirmed = await bot.wait_for('reaction_add', timeout=5.0, check=check)
      response = db.createTeam(data.newTeam(team_query), str(ctx.author))
      await ctx.send(response, delete_after=5)
   except:
      print("Team not created. ")

@bot.command()
@commands.check(validate_user)
async def att(ctx, user1: User, *args):
   team_name = " ".join([*args])
   team_query = {'OWNER': str(ctx.author), 'TNAME': team_name}
   team = db.queryTeam(team_query)
   accept = await ctx.send(f"Do you want to join team {team_name}?".format(bot), delete_after=8)
   for emoji in emojis:
      await accept.add_reaction(emoji)

   def check(reaction, user):
      return user == user1 and str(reaction.emoji) == '👍'

   try:
      confirmed = await bot.wait_for('reaction_add', timeout=5.0, check=check)
      new_value_query = {'$push': {'MEMBERS': str(user1)}}
      response = db.addTeamMember(team_query, new_value_query, str(ctx.author), str(user1))
      await ctx.send(response, delete_after=5)
   except:
      print("Team not created. ")

@bot.command()
@commands.check(validate_user)
async def lkt(ctx, *args):
   team_name = " ".join([*args])
   team_query = {'TNAME': team_name}
   team = db.queryTeam(team_query)
   if team:
      team_name = team['TNAME']
      games = team['GAMES']
      # avatar = game['IMAGE_URL']
      badges = team['BADGES']
      ranked = team['RANKED']
      normal = team['NORMAL']
      tournament_wins = team['TOURNAMENT_WINS']


      ranked_to_string = dict(ChainMap(*ranked))
      normal_to_string = dict(ChainMap(*normal))

      team_list = []
      for members in team['MEMBERS']:
         mem_query = db.queryUser({'DISNAME': members})
         ign_list = [x for x in mem_query['IGN']]
         ign_list_keys = [k for k in ign_list[0].keys()]
         if ign_list_keys == games:
            team_list.append(f"{ign_list[0][games[0]]}") 
         else:
            team_list.append(f"{members}")


      embedVar = discord.Embed(title=f"{team_name}' Team Card".format(bot), description="Party Chat Gaming Database", colour=000000)
      # embedVar.set_thumbnail(url=avatar)
      embedVar.add_field(name="Games", value=f'{games[0]}'.format(bot))
      embedVar.add_field(name="Members", value="\n".join(f'{t}'.format(bot) for t in team_list), inline=False)
      embedVar.add_field(name="Ranked", value="\n".join(f'{k}: {"/".join([str(int) for int in v])}' for k,v in ranked_to_string.items()))
      embedVar.add_field(name="Normals", value="\n".join(f'{k}: {"/".join([str(int) for int in v])}' for k,v in normal_to_string.items()))
      embedVar.add_field(name="Tournament Wins", value=tournament_wins)

      await ctx.send(embed=embedVar, delete_after=20)
   else:
      await ctx.send("Team does not exist. ", delete_after=5)


@bot.command()
@commands.check(validate_user)
async def dtm(ctx, user1: User, *args):
   team_name = " ".join([*args])
   team_query = {'OWNER': str(ctx.author), 'TNAME': team_name}
   team = db.queryTeam(team_query)

   if str(ctx.author) == team['OWNER']:
      accept = await ctx.send(f"Do you want to remove {str(user1)} from the team?".format(bot), delete_after=8)
      for emoji in emojis:
         await accept.add_reaction(emoji)

      def check(reaction, user):
         return user == ctx.author and str(reaction.emoji) == '👍'

      try:
         confirmed = await bot.wait_for('reaction_add', timeout=5.0, check=check)
         new_value_query = {'$pull': {'MEMBERS': str(user1)}}
         response = db.deleteTeamMember(team_query, new_value_query, str(user1))
         await ctx.send(response, delete_after=5)
      except:
         print("Team not created. ")
   else:
      return "Only the owner remove team members. "


@bot.command()
@commands.check(validate_user)
async def dt(ctx, *args):
   team_name = " ".join([*args])
   team_query = {'OWNER': str(ctx.author), 'TNAME': team_name}
   team = db.queryTeam(team_query)
   if team['OWNER'] == str(ctx.author):
      accept = await ctx.send(f"Do you want to delete the {team['GAMES'][0]} team {team_name}?".format(bot), delete_after=10)
      for emoji in emojis:
         await accept.add_reaction(emoji)

      def check(reaction, user):
         return user == ctx.author and str(reaction.emoji) == '👍'

      try:
         confirmed = await bot.wait_for('reaction_add', timeout=8.0, check=check)
         response = db.deleteTeam(team, str(ctx.author))
         print(response)
         await ctx.send(response, delete_after=5)
      except:
         print("Team not created. ")
   else:
      await ctx.send("Only the owner of the team can delete the team. ")


@bot.command()
@commands.check(validate_user)
async def cs(ctx, user: User):
   current_session = {'TEAMS.TEAM': str(user), "AVAILABLE": True}
   session = db.querySessionMembers(current_session)
   if session:
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
         ranked = "Normal"

      teams = [x for x in session['TEAMS']]
      team_list = []
      for x in teams:
         for members in x['TEAM']:
            mem_query = db.queryUser({'DISNAME': members})
            ign_list = [x for x in mem_query['IGN']]
            ign_list_keys = [k for k in ign_list[0].keys()]
            if ign_list_keys == [games]:
               team_list.append(f"{ign_list[0][games]}: {x['SCORE']}")
            else:
               team_list.append(f"{members}: {x['SCORE']}")

      embedVar = discord.Embed(title=f"{name}'s {games} Session ".format(bot), description="Party Chat Gaming Database", colour=000000)
      embedVar.set_thumbnail(url=avatar)
      embedVar.add_field(name="Match Type", value=f'{game_type}'.format(bot))
      embedVar.add_field(name="Ranked", value=f'{ranked}'.format(bot))
      embedVar.add_field(name="Competitors", value="\n".join(f'{t}'.format(bot) for t in team_list), inline=False)
      await ctx.send(embed=embedVar, delete_after=15)
   else:
      await ctx.send("Session does not exist. ", delete_after=5)


async def sw(ctx):
   session_query = {"OWNER": str(ctx.author), "AVAILABLE": True}
   session_data = db.querySession(session_query)
   teams = [x for x in session_data['TEAMS']]
   winning_team = {}
   high_score = teams[0]['SCORE']
   for x in teams:
      if x['SCORE'] >= high_score:
         high_score = x['SCORE']
         winning_team = x
   session_data['WINNER'] = winning_team
   winner = session_data['WINNER']
   session = session_data
   update_query = {'$set': {'WINNER': winner}}
   query = {"_id": session_data["_id"], "TEAMS.TEAM": str(ctx.author)}
   db.updateSession(session, query, update_query)
   game_type = ""
   if session_data['RANKED'] == False:
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

      for x in winning_team['TEAM']:
         player = db.queryUser({'DISNAME': x})
         types_of_matches_list = [x for x in player['NORMAL']]
         types_of_matches = dict(ChainMap(*types_of_matches_list))
         current_score = types_of_matches[game_type.upper()]
         # print(current_score)
         query = {'DISNAME': player['DISNAME']}
         new_value = {"$inc": {'NORMAL.$[type].' + game_type.upper() + '.0': 1}}
         filter_query = [{'type.' + game_type.upper(): current_score}]
         db.updateUser(query, new_value, filter_query)
   else :
      print("hello world")


async def sl(ctx):
   session_query = {"OWNER": str(ctx.author), "AVAILABLE": True}
   session_data = db.querySession(session_query)
   teams = [x for x in session_data['TEAMS']]
   losing_team = {}
   low_score = teams[0]['SCORE']
   for x in teams:
      if x['SCORE'] <= low_score:
         low_score = x['SCORE']
         losing_team = x
   session_data['LOSER'] = losing_team
   loser = session_data['LOSER']
   session = session_data
   update_query = {'$set': {'LOSER': loser}}
   query = {"_id": session_data["_id"], "TEAMS.TEAM": str(ctx.author)}
   db.updateSession(session, query, update_query)
   game_type = ""
   if session_data['RANKED'] == False:
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
         types_of_matches_list = [x for x in player['NORMAL']]
         types_of_matches = dict(ChainMap(*types_of_matches_list))
         current_score = types_of_matches[game_type.upper()]
         # print(current_score)
         query = {'DISNAME': player['DISNAME']}
         new_value = {"$inc": {'NORMAL.$[type].' + game_type.upper() + '.1': 1}}
         filter_query = [{'type.' + game_type.upper(): current_score}]
         db.updateUser(query, new_value, filter_query)
         print("hi")
   else :
      print("hello world")
   # await ctx.send(loser['TEAM'], delete_after=5)


async def DM(ctx, user, m,  message=None):
    message = message or "This Message is sent via DM"
    await user.send(m)


DISCORD_TOKEN = config('DISCORD_TOKEN')

bot.run(DISCORD_TOKEN)