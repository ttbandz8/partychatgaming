import db
import time
import classes as data
import test_data as td
import messages as m
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

bot = commands.Bot(command_prefix="#")

async def validate_user(ctx):
   query = {'DISNAME': str(ctx.author)}
   valid = db.queryUser(query)
   if valid:
      return True
   else:
      msg = await ctx.send(m.USER_NOT_REGISTERED)
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


# Create Gods of Cod
@bot.command()
@commands.check(validate_user)
async def goc(ctx, args1: str, args2: int, args3: bool, args4: int, args5: str ):
   if ctx.author.guild_permissions.administrator == True:
      goc_query = {'TITLE': args1, 'TYPE': args2, 'TEAM_FLAG': args3, 'REWARD': args4, 'IMG_URL': args5, 'REGISTRATION': True}
      response = db.createGoc(data.newGoc(goc_query))
      await ctx.send(response, delete_after=3)
   else:
      print(m.ADMIN_ONLY_COMMAND)

# Start Gods of Cod
@bot.command()
@commands.check(validate_user)
async def sgoc(ctx):
   if ctx.author.guild_permissions.administrator == True:
      goc_query = {'REGISTRATION': True}
      new_value = {'$set': {'REGISTRATION': False}, '$set': {'AVAILABLE': True}}
      response = db.updateGoc(goc_query, new_value)
      await ctx.send("GODS OF COD has begun. ")
   else:
      print(m.ADMIN_ONLY_COMMAND)

# Create a Goc Session
@bot.command()
@commands.check(validate_user)
async def cgoc(ctx):
   if ctx.author.guild_permissions.administrator == True:
      query = {'REGISTRATION': True}
      g = db.queryGoc(query)
      if g:
         game = [x for x in db.query_all_games()][0]
         session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 1, "TEAMS": [], "RANKED": True, "TOURNAMENT": True, "GOC": True, "GOC_TITLE": g['TITLE']}
         resp = db.createSession(data.newSession(session_query))
         await ctx.send(resp, delete_after=5)

      else:
         await ctx.send(m.TOURNEY_DOES_NOT_EXIST, delete_after=5)
   else:
      await ctx.send(m.ADMIN_ONLY_COMMAND)

# Invite to Gods of Cod
@bot.command()
@commands.check(validate_user)
async def goci(ctx, user1: User):
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

# Delete Gods of Cod
@bot.command()
@commands.check(validate_user)
async def dgoc(ctx):
   if ctx.author.guild_permissions.administrator == True:
      goc_query = {'AVAILABLE': True}
      response = db.deleteGoc(goc_query)
      await ctx.send("GODS OF COD has ended. ")
   else:
      print(m.ADMIN_ONLY_COMMAND)

# Gods of Cod SignUp
@bot.command()
@commands.check(validate_user)
async def rgoc(ctx):
   goc_query = {'REGISTRATION': True}
   goc_response = db.queryGoc(goc_query)
   user = str(ctx.author)
   user_data = db.queryUser({'DISNAME': str(ctx.author)})

   if goc_response['TEAM_FLAG']:
      if user_data['TEAM'] == 'PCG':
         await ctx.send("This is a Team Only Tournament. ")
      else:
         # Make it so that Team Owner has to be the one to register the team
         team_data = db.queryTeam({'TNAME': user_data['TEAM']})
         if team_data['OWNER'] == str(ctx.author):
            if len(team_data['MEMBERS']) >= goc_response['TYPE']:
               new_value =  {'$addToSet': {'PARTICIPANTS': str(team_data['TNAME'])}}
               response = db.updateGoc(goc_query, new_value)
               await ctx.send(f"{team_data['TNAME']} is now registered for GODS OF COD. ")           
         else:
            await ctx.send("Only the owner of the team can register team for Tournaments. ")
   else:
      if user in goc_response['PARTICIPANTS']:
         await ctx.send(m.ALREADY_IN_TOURNEY, delete_after=4)
      else:
         new_value =  {'$addToSet': {'PARTICIPANTS': user}}
         response = db.updateGoc(goc_query, new_value)
         await ctx.send(f"{ctx.author.mention} is now registered for GODS OF COD. ")

# Lookup Gods of Cod
@bot.command()
async def goclk(ctx):
   query = {'REGISTRATION': True}
   g = db.queryGoc(query)

   if g:
      title = g['TITLE']
      team_flag = g['TEAM_FLAG']
      game_type = " "
      if g['TYPE'] == 1:
         game_type = "1v1"
      elif g['TYPE'] == 2:
         game_type = "2v2"
      elif g['TYPE'] == 3:
         game_type = "3v3"
      elif g['TYPE'] == 4:
         game_type = "4v4"
      elif g['TYPE'] == 5:
         game_type = "5v5"

      available = g['AVAILABLE']
      registration = g['REGISTRATION']
      avatar = g['IMG_URL']
      reward = g['REWARD']
      participants = "\n".join(g['PARTICIPANTS'])

      

      embedVar = discord.Embed(title=f"GODS OF COD: {title}", description="Party Chat Gaming Database™️", colour=000000)
      embedVar.set_image(url=avatar)
      embedVar.add_field(name="TEAM TOURNAMENT" , value=str(team_flag))
      embedVar.add_field(name="TOURNAMENT STYLE", value=game_type)
      embedVar.add_field(name="TOURNAMENT AVAILABLE", value=str(available))
      embedVar.add_field(name="TOURNAMENT REGISTRATION", value=str(registration))
      if participants:
         embedVar.add_field(name="Registered Participants", value=participants)
      embedVar.add_field(name="REWARD", value=f"${reward}", inline=False)
      await ctx.send(embed=embedVar)
   else:
      await ctx.send("No GODS OF COD at this time. ", delete_after=5)


# New Titles
@bot.command()
@commands.check(validate_user)
async def nt(ctx, args1: str, args2: int, args3: int):
   if ctx.author.guild_permissions.administrator == True:
      title_query = {'TITLE': str(args1), 'TOURNAMENT_REQUIREMENTS': int(args2), 'PRICE': int(args3)}
      added = db.createTitle(data.newTitle(title_query))
      await ctx.send(added, delete_after=3)
   else:
      print(m.ADMIN_ONLY_COMMAND)

@bot.command()
@commands.check(validate_user)
async def bt(ctx, args: str):
   vault_query = {'OWNER' : str(ctx.author)}
   vault = db.altQueryVault(vault_query)
   shop = db.queryShopTitles()
   titles = []

   currentBalance = vault['BALANCE']
   cost = 0
   mintedTitle = ""
   for title in shop:

      if args == title['TITLE']:
         mintedTitle = title['TITLE']
         cost = title['PRICE']

   if bool(mintedTitle):
      if mintedTitle in vault['TITLES']:
         await ctx.send(m.USER_ALREADY_HAS_TITLE, delete_after=5)
      else:
         newBalance = currentBalance - cost

         if newBalance < 0 :
            await ctx.send("You have an insufficent Balance")
         else:
            await curse(ctx, cost, ctx.author)
            response = db.updateVaultNoFilter(vault_query,{'$addToSet':{'TITLES': args}})
            await ctx.send(m.PURCHASE_COMPLETE)
   else:
      await ctx.send(m.TITLE_DOESNT_EXIST)

@bot.command()
@commands.check(validate_user)
async def ut(ctx, args):
   user_query = {'DISNAME': str(ctx.author)}
   user = db.queryUser(user_query)

   vault_query = {'OWNER' : str(ctx.author)}
   vault = db.altQueryVault(vault_query)

   resp = db.queryTitle({'TITLE': args})

   if resp['TOURNAMENT_REQUIREMENTS'] == 0:

      # Do not Check Tourney wins
      if args in vault['TITLES']:
         response = db.updateUserNoFilter(user_query, {'$set': {'TITLE': args}})
         await ctx.send(response)
      else:
         await ctx.send(m.USER_DOESNT_HAVE_THE_Title, delete_after=5)
   else:

      # Check tourney wins
      tournament_wins = user['TOURNAMENT_WINS']
      title_query = {'TOURNAMENT_REQUIREMENTS': tournament_wins}

      if tournament_wins >= resp['TOURNAMENT_REQUIREMENTS']:
         if args in vault['TITLES']:
            response = db.updateUserNoFilter(user_query, {'$set': {'TITLE': args}})
            await ctx.send(response)
         else:
            await ctx.send(m.USER_DOESNT_HAVE_THE_Title, delete_after=5)
      else:
         return "Unable to update Title."

'''CARDS'''
@bot.command()
@commands.check(validate_user)
async def nc(ctx, args1: str, args2: str, args3: int, args4: int):
   if ctx.author.guild_permissions.administrator == True:
      card_query = {'PATH': str(args1), 'NAME': str(args2), 'TOURNAMENT_REQUIREMENTS': int(args3),'PRICE': int(args4)}
      added = db.createCard(data.newCard(card_query))
      await ctx.send(added, delete_after=3)
   else:
      print(m.ADMIN_ONLY_COMMAND)


@bot.command()
@commands.check(validate_user)
async def shop(ctx):
   resp = db.queryShopCards()
   vault_query = {'OWNER' : str(ctx.author)}
   vault = db.altQueryVault(vault_query)
   cards = []
   unavailable_cards = []
   for card in resp:
      if card['PRICE'] != 0 and card['PRICE'] < (vault['BALANCE'] + 1000):
         cards.append({card['NAME']: card['PRICE']})

   title_resp = db.queryShopTitles()
   titles = []
   unavailable_titles = []
   for title in title_resp:
      if title['PRICE'] != 0 and title['PRICE'] < (vault['BALANCE'] + 1000):
         titles.append({title['TITLE']: title['PRICE']})

   cards_to_str = dict(ChainMap(*cards))
   n = dict(sorted(cards_to_str.items(), key=lambda item: item[1]))
   cards_sorted_list = "\n".join(f'{k} : ' +  f" :coin:{'{:,}'.format(v)}"  for k,v in n.items())

   titles_to_str = dict(ChainMap(*titles))
   n = dict(sorted(titles_to_str.items(), key=lambda item: item[1]))
   titles_sorted_list = "\n".join(f'{k} : ' +  f" :coin:{'{:,}'.format(v)}"  for k,v in n.items())
   
   embedVar = discord.Embed(title=f":shopping_cart: Flex Shop", description="To preview cards, use the #vc card command. " + "\n" + "You will unlock more purchasable cards as you save and earn more gold. ", colour=000000)
   embedVar.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620236723/PCG%20LOGOS%20AND%20RESOURCES/Party_Chat_Shop.png")
   embedVar.add_field(name=":shopping_bags: Available Cards", value=cards_sorted_list)
   embedVar.add_field(name=":shopping_bags: Available Titles", value=titles_sorted_list)
   await ctx.send(embed=embedVar, delete_after=30)

@bot.command()
@commands.check(validate_user)
async def bc(ctx, args: str):
   vault_query = {'OWNER' : str(ctx.author)}
   vault = db.altQueryVault(vault_query)
   shop = db.queryShopCards()
   cards = []

   currentBalance = vault['BALANCE']
   cost = 0
   mintedCard = ""
   for card in shop:
      if args == card['NAME']:
         mintedCard = card['NAME']
         cost = card['PRICE']


   if bool(mintedCard):
      if mintedCard in vault['CARDS']:
         await ctx.send(m.USER_ALREADY_HAS_CARD, delete_after=5)
      else:
         newBalance = currentBalance - cost

         if newBalance < 0 :
            await ctx.send("You have an insufficent Balance")
         else:
            await curse(ctx, cost, ctx.author)
            response = db.updateVaultNoFilter(vault_query,{'$addToSet':{'CARDS': args}})
            await ctx.send(m.PURCHASE_COMPLETE)
   else:
      await ctx.send(m.CARD_DOESNT_EXIST)

### Update card
@bot.command()
@commands.check(validate_user)
async def uc(ctx, args):
   user_query = {'DISNAME': str(ctx.author)}
   user = db.queryUser(user_query)

   vault_query = {'OWNER' : str(ctx.author)}
   vault = db.altQueryVault(vault_query)

   resp = db.queryCard({'NAME': args})

   if resp['TOURNAMENT_REQUIREMENTS'] == 0:

      # Do not Check Tourney wins
      if args in vault['CARDS']:
         response = db.updateUserNoFilter(user_query, {'$set': {'CARD': args}})
         await ctx.send(response)
      else:
         await ctx.send(m.USER_DOESNT_HAVE_THE_CARD, delete_after=5)
   else:

      # Check tourney wins
      tournament_wins = user['TOURNAMENT_WINS']
      card_query = {'TOURNAMENT_REQUIREMENTS': tournament_wins}

      if tournament_wins >= resp['TOURNAMENT_REQUIREMENTS']:
         if args in vault['CARDS']:
            response = db.updateUserNoFilter(user_query, {'$set': {'CARD': args}})
            await ctx.send(response)
         else:
            await ctx.send(m.USER_DOESNT_HAVE_THE_CARD, delete_after=5)
      else:
         return "Unable to update card."

 
### View preview of Card
@bot.command()
@commands.check(validate_user)
async def vc(ctx, args):
   card = db.queryCard({'NAME':args})
   if card:
      img = Image.open(requests.get(card['PATH'], stream=True).raw)
      img.save("text.png")
      await ctx.send(file=discord.File("text.png"))
   else:
      await ctx.send(m.CARD_DOESNT_EXIST, delete_after=3)



''' Delete All Sessions '''
@bot.command()
@commands.check(validate_user)
async def dac(ctx):
   user_query = {"DISNAME": str(ctx.author)}
   if ctx.author.guild_permissions.administrator == True:
      resp = db.deleteAllCards(user_query)
      await ctx.send(resp)
   else:
      await ctx.send(m.ADMIN_ONLY_COMMAND)


@bot.command()
@commands.check(validate_user)
async def flex(ctx):
   query = {'DISNAME': str(ctx.author)}
   d = db.queryUser(query)

   card = db.queryCard({'NAME': d['CARD']})

   if d:
      name = d['DISNAME'].split("#",1)[0]
      games = d['GAMES']
      ign = d['IGN']
      team = d['TEAM']
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
      draw.text((368, 320), team, (255, 255, 255), font=p, align="center")
      draw.text((650, 320), titles_text, (255, 255, 255), font=p, align="center")
      draw.text((865, 320), normals_text, (255, 255, 255), font=p, align="center")
      draw.text((1040, 320), ranked_text, (255, 255, 255), font=p, align="center")

      img.save("text.png")

      await ctx.send(file=discord.File("text.png"))

   else:
      await ctx.send("User does not exist in the system. ", delete_after=3)


@bot.command()
@commands.check(validate_user)
async def vault(ctx):
   query = {'DISNAME': str(ctx.author)}
   d = db.queryUser(query)

   vault = db.queryVault({'OWNER': d['DISNAME']})
   if vault:
      name = d['DISNAME'].split("#",1)[0]
      avatar = d['AVATAR']
      balance = vault['BALANCE']
      cards = vault['CARDS']
      titles = vault['TITLES']



      embedVar = discord.Embed(title= f":triangular_flag_on_post: " + f"{name}".format(client) +"\n" + f" :coin:{'{:,}'.format(balance)}", description=":bank: Your Party Chat Gaming Vault™️", colour=000000)
      embedVar.set_thumbnail(url=avatar)
      # embedVar.add_field(name="Balance" + " :fireworks:", value=f":coin:{balance}")
      if bool(cards):
         embedVar.add_field(name="Cards" + " :fireworks:", value="\n".join(cards))
      else:
         embedVar.set_footer(text="No Cards available")
      
      if bool(titles):
         embedVar.add_field(name="Titles" + " :fireworks:", value="\n".join(titles))
      await ctx.send(embed=embedVar, delete_after=15)

   else:
      newVault = db.createVault({'OWNER': d['DISNAME']})
      print(newVault)


@bot.command()
@commands.check(validate_user)
async def bless(ctx, args, user1: User):
   if ctx.author.guild_permissions.administrator == True:
      blessAmount = args
      posBlessAmount = 0 + abs(int(blessAmount))
      query = {'DISNAME': str(user1)}
      vaultOwner = db.queryUser(query)
      if vaultOwner:
         vault = db.queryVault({'OWNER' : vaultOwner['DISNAME']})
         update_query = {"$inc": {'BALANCE': posBlessAmount}}
         db.updateVaultNoFilter(vault, update_query)
      else:
         print("cant find vault")


@bot.command()
@commands.check(validate_user)
async def curse(ctx,args, user1: User):
   if ctx.author.guild_permissions.administrator == True:
      curseAmount = args
      negCurseAmount = 0 - abs(int(curseAmount))
      query = {'DISNAME': str(user1)}
      vaultOwner = db.queryUser(query)
      if vaultOwner:
         vault = db.queryVault({'OWNER' : vaultOwner['DISNAME']})
         update_query = {"$inc": {'BALANCE': int(negCurseAmount)}}
         db.updateVaultNoFilter(vault, update_query)
      else:
         print("cant find vault")

@bot.command()
async def r(ctx):
   disname = str(ctx.author)
   name = disname.split("#",1)[0]
   user = {'DISNAME': disname, 'NAME': name, 'DID' : str(ctx.author.id), 'AVATAR': str(ctx.author.avatar_url)}
   response = db.createUsers(data.newUser(user))
   userQuery = db.queryUser({'DISNAME': str(ctx.author)})
   vault = db.queryVault({'OWNER': userQuery['DISNAME']})
   if vault:
      await ctx.send(response, delete_after=5)
   else:
      vault = db.createVault(data.newVault({'OWNER' : userQuery['DISNAME']}))
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
            vault = db.queryVault({'OWNER': user_is_validated['DISNAME']})
            if vault:
               db.deleteVault(vault)
               print("vault gone")
            else:
               print("coudlnt delete")
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



''' Kings Gambit '''
@bot.command()
@commands.check(validate_user)
async def kg(ctx):
   if ctx.author.guild_permissions.administrator == True:
      game = [x for x in db.query_all_games()][0]
      session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 1, "TEAMS": [], "KINGSGAMBIT": True, "RANKED": True, "TOURNAMENT": True}
      resp = db.createSession(data.newSession(session_query))
      await ctx.send(resp, delete_after=5)
   else:
      print(m.ADMIN_ONLY_COMMAND)


@bot.command()
@commands.check(validate_user)
async def jkg(ctx, user1: User):
   session_query = {"OWNER": str(user1), "AVAILABLE": True, "KINGSGAMBIT": True}
   session = db.querySession(session_query)


   teams_list = [x for x in session['TEAMS']]
   current_member = []
   positions = []
   new_position = 0

   if bool(teams_list):
      for x in teams_list:
         
         if str(user1) in x['TEAM']:
            current_member.append(str(user1))
         positions.append(x['POSITION'])
      new_position = max(positions) + 1

   if bool(current_member):
      join_query = {"TEAM": [str(ctx.author)], "SCORE": 0, "POSITION": new_position}
      session_joined = db.joinKingsGambit(session_query, join_query)
      await ctx.send(session_joined, delete_after=5)
   else:
      await ctx.send(m.ALREADY_IN_SESSION, delete_after=5)
   

@bot.command()
@commands.check(validate_user)
async def skg(ctx, user: User):
   session_query = {"OWNER": str(ctx.author), "AVAILABLE": True, "KINGSGAMBIT": True}
   session_data = db.querySession(session_query)
   teams = [x for x in session_data['TEAMS']]
   winning_team = {}
   for x in teams:
      if str(user) in x['TEAM'] and x['POSITION'] < 2: 
         winning_team = x

   new_score = winning_team['SCORE'] + 1
   update_query = {'$set': {'TEAMS.$.SCORE': new_score}}
   query = {"_id": session_data["_id"], "TEAMS.TEAM": str(user)}
   response = db.updateSession(session_query, query, update_query)


   positions = []
   loser = {}

   ''' IF POSITIN 0 WINS '''
   if winning_team['POSITION'] == 0:

      for x in teams:
         positions.append(x['POSITION'])
         if x['POSITION'] == 1:
            loser = x

      query = {"OWNER": str(ctx.author), "AVAILABLE": True, "KINGSGAMBIT": True}
      update_query = {'$set': {'TEAMS.$[type].POSITION': max(positions) + 1}}
      arrayFilter = [{'type.' + 'TEAM': loser['TEAM']}]
      response = db.updatekg(session_query, query, update_query, arrayFilter)
      
      for x in teams:
         if x['POSITION'] > 1:
            query = {"OWNER": str(ctx.author), "AVAILABLE": True, "KINGSGAMBIT": True}
            update_query = {'$inc': {'TEAMS.$[type].POSITION': -1}}
            arrayFilter = [{'type.' + 'TEAM': x['TEAM']}]
            response = db.updatekg(session_query, query, update_query, arrayFilter)

      query = {"OWNER": str(ctx.author), "AVAILABLE": True, "KINGSGAMBIT": True}
      update_query = {'$inc': {'TEAMS.$[type].POSITION': - 1}}
      arrayFilter = [{'type.' + 'TEAM': loser['TEAM']}]
      response = db.updatekg(session_query, query, update_query, arrayFilter)


   ''' IF POSITIN 1 WINS '''
   if winning_team['POSITION'] == 1:

      for x in teams:
         positions.append(x['POSITION'])
         if x['POSITION'] == 0:
            loser = x

      query = {"OWNER": str(ctx.author), "AVAILABLE": True, "KINGSGAMBIT": True}
      update_query = {'$set': {'TEAMS.$[type].POSITION': max(positions) + 1}}
      arrayFilter = [{'type.' + 'TEAM': loser['TEAM']}]
      response = db.updatekg(session_query, query, update_query, arrayFilter)

      query = {"OWNER": str(ctx.author), "AVAILABLE": True, "KINGSGAMBIT": True}
      update_query = {'$set': {'TEAMS.$[type].POSITION': 0}}
      arrayFilter = [{'type.' + 'TEAM': winning_team['TEAM']}]
      response = db.updatekg(session_query, query, update_query, arrayFilter)

      for x in teams:
         if x['POSITION'] > 1:
            query = {"OWNER": str(ctx.author), "AVAILABLE": True, "KINGSGAMBIT": True}
            update_query = {'$inc': {'TEAMS.$[type].POSITION': -1}}
            arrayFilter = [{'type.' + 'TEAM': x['TEAM']}]
            response = db.updatekg(session_query, query, update_query, arrayFilter)

      query = {"OWNER": str(ctx.author), "AVAILABLE": True, "KINGSGAMBIT": True}
      update_query = {'$inc': {'TEAMS.$[type].POSITION': - 1}}
      arrayFilter = [{'type.' + 'TEAM': loser['TEAM']}]
      response = db.updatekg(session_query, query, update_query, arrayFilter)

   if response:
      await ctx.send(f"{user.mention}" +f" :heavy_plus_sign::one:", delete_after=2)
   else:
      await ctx.send(f"Score not added. Please, try again. ", delete_after=5) 



''' Create 1v1 - 5v5 Sessions '''
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
      accept = await ctx.send(f"{user1.mention}, Will you join the session?", delete_after=10)
      for emoji in emojis:
         await accept.add_reaction(emoji)

      def check(reaction, user):
         return user == user1 and str(reaction.emoji) == '👍'

      try:
         reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=check)


         session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 3, "TEAMS": [{"TEAM": [str(ctx.author), str(user1)], "SCORE": 0, "POSITION": 0}]}
         if args == "n":
            resp = db.createSession(data.newSession(session_query))
            await ctx.send(resp, delete_after=5)
         elif args == "r":
            session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 3, "TEAMS": [{"TEAM": [str(ctx.author), str(user1)], "SCORE": 0, "POSITION": 0}], "RANKED": True}
            resp = db.createSession(data.newSession(session_query))
            await ctx.send(resp, delete_after=5)
      except:
         await ctx.send(m.INVITE_NOT_ACCEPTED, delete_after=3)
   else:
      await ctx.send(m.USER_NOT_REGISTERED, delete_after=5)

@bot.command()
@commands.check(validate_user)
async def c3v3(ctx, args, user1: User, user2: User):
   if ctx.author.guild_permissions.administrator == True:
      game = [x for x in db.query_all_games()][0]
      
      teammates = [str(user1), str(user2)]
      valid_teammates = []
      for x in teammates:
         valid = db.queryUser({'DISNAME' : str(x)})
         if valid:
            valid_teammates.append(valid["DISNAME"])
         else:
            await ctx.send(f"{valid['DISNAME']} needs to register.".format(bot), delete_after=5)

      if valid_teammates:
         accept = await ctx.send("SCRIM STARTING : 3v3 ", delete_after=10)
         session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 3, "SCRIM": True, "TEAMS": [{"TEAM": [str(ctx.author), str(user1), str(user2)], "SCORE": 0, "POSITION": 0}]}
         if args == "n":
            resp = db.createSession(data.newSession(session_query))
            await ctx.send(resp, delete_after=5)
         elif args == "r":
            session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 3, "SCRIM": True, "TEAMS": [{"TEAM": [str(ctx.author), str(user1), str(user2)], "SCORE": 0, "POSITION": 0}], "RANKED": True}
            resp = db.createSession(data.newSession(session_query))
            await ctx.send(resp, delete_after=5)
   else:
      await ctx.send(m.USER_NOT_REGISTERED, delete_after=5)


@bot.command()
@commands.check(validate_user)
async def c4v4(ctx, args, user1: User, user2: User, user3: User):
   if ctx.author.guild_permissions.administrator == True:
      game = [x for x in db.query_all_games()][0]
      
      teammates = [str(user1), str(user2), str(user3)]
      valid_teammates = []
      for x in teammates:
         valid = db.queryUser({'DISNAME' : str(x)})
         if valid:
            valid_teammates.append(valid["DISNAME"])
         else:
            await ctx.send(f"{valid['DISNAME']} needs to register.".format(bot), delete_after=5)

      if valid_teammates:
         accept = await ctx.send("SCRIM STARTING : 4v4 ", delete_after=10)
         session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 4, "SCRIM": True, "TEAMS": [{"TEAM": [str(ctx.author), str(user1), str(user2), str(user3)], "SCORE": 0, "POSITION": 0}]}
         if args == "n":
            resp = db.createSession(data.newSession(session_query))
            await ctx.send(resp, delete_after=5)
         elif args == "r":
            session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 4, "SCRIM": True, "TEAMS": [{"TEAM": [str(ctx.author), str(user1), str(user2), str(user3)], "SCORE": 0, "POSITION": 0}], "RANKED": True}
            resp = db.createSession(data.newSession(session_query))
            await ctx.send(resp, delete_after=5)

   else:
      await ctx.send(m.USER_NOT_REGISTERED, delete_after=5)


@bot.command()
@commands.check(validate_user)
async def c5v5(ctx, args, user1: User, user2: User, user3: User, user4: User):
   if ctx.author.guild_permissions.administrator == True:
      game = [x for x in db.query_all_games()][0]
      
      teammates = [str(user1), str(user2), str(user3), str(user4)]
      valid_teammates = []
      for x in teammates:
         valid = db.queryUser({'DISNAME' : str(x)})
         if valid:
            valid_teammates.append(valid["DISNAME"])
         else:
            await ctx.send(f"{valid['DISNAME']} needs to register.".format(bot), delete_after=5)

      if valid_teammates:
         accept = await ctx.send("SCRIM STARTING : 5v5 ", delete_after=10)
         session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 5, "SCRIM": True, "TEAMS": [{"TEAM": [str(ctx.author), str(user1), str(user2), str(user3), str(user4)], "SCORE": 0, "POSITION": 0}]}
         if args == "n":
            resp = db.createSession(data.newSession(session_query))
            await ctx.send(resp, delete_after=5)
         elif args == "r":
            session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 5, "SCRIM": True, "TEAMS": [{"TEAM": [str(ctx.author), str(user1), str(user2), str(user3), str(user4)], "SCORE": 0, "POSITION": 0}], "RANKED": True}
            resp = db.createSession(data.newSession(session_query))
            await ctx.send(resp, delete_after=5)
      else:
         await ctx.send("Users must register.", delete_after=5)
   else:
      await ctx.send("Public SCRIMS coming soon! Join a League Team to Participate ! :military_helmet:", delete_after=5)

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


#end session and push data to database
@bot.command()
@commands.check(validate_user)
async def es(ctx):
   session_query = {"OWNER": str(ctx.author), "AVAILABLE": True}
   await sw(ctx)
   await sl(ctx)
   end = db.endSession(session_query)
   await ctx.send(end, delete_after=5)


#delete session from database
@bot.command()
@commands.check(validate_user)
async def ds(ctx):
   session_query = {"OWNER": str(ctx.author), "AVAILABLE": True}
   response = db.deleteSession(session_query)
   await ctx.send(response, delete_after=5)


''' Delete All Sessions '''
@bot.command()
@commands.check(validate_user)
async def das(ctx):
   user_query = {"DISNAME": str(ctx.author)}
   if ctx.author.guild_permissions.administrator == True:
      resp = db.deleteAllSessions(user_query)
      await ctx.send(resp)
   else:
      await ctx.send(m.ADMIN_ONLY_COMMAND)



''' Invite to 1v1 '''
@bot.command()
@commands.check(validate_user)
async def invite(ctx, args, user1: User):
   game = [x for x in db.query_all_games()][0]
   
   validate_opponent = db.queryUser({'DISNAME': str(user1)})

   if validate_opponent:
      await DM(ctx, user1, f"{ctx.author.mention}" + " has challeneged you... :eyes:")
      accept = await ctx.send(f"{user1.mention}, Will you join the session? :fire:", delete_after=15)
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
async def js(ctx, *user: User):
   session_query = {"OWNER": str(user[0]), "AVAILABLE": True}
   session = db.querySession(session_query)
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

#Session Generator Admin's can pull users in sessions up to 5's
@bot.command()
@commands.check(validate_user)
async def sg(ctx, *user: User):
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
         await ctx.send("You must first register before joining sessions. ", delete_after=5)
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
async def iby(ctx, user: User):
   win_query = {'WINNER.TEAM': [str(ctx.author)], 'LOSER.TEAM': [str(user)]}
   win_count = 0
   win_sessions = db.querySessionForUser(win_query)
   for x in win_sessions:
      win_count +=1

   loss_query = {'WINNER.TEAM': [str(user)], 'LOSER.TEAM': [str(ctx.author)]}
   loss_count = 0
   loss_sessions = db.querySessionForUser(loss_query)
   for x in loss_sessions:
      loss_count +=1

   total_games = win_count + loss_count

   message = f"{str(ctx.author.mention)} has defeated {str(user.mention)} {win_count} out of {total_games} matches!"
   if total_games == 0:
      message = "You two have not played each other. "
   await ctx.send(message)


#Check if User is hosting a session
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
      tournament = session['TOURNAMENT']
      kingsgambit = session['KINGSGAMBIT']
      goc = session['GOC']
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
      team_1 = [x for x in teams if x['POSITION'] == 0] # position 0
      team_2 = [x for x in teams if x['POSITION'] == 1] # position 1
      other_teams = [x for x in teams if x['POSITION'] > 1] # position 1


      team_1_comp = ""
      team_2_comp = ""

      team_1_score = ""
      team_2_score = ""

      king_score = 0

      other_teams_comp = []

      for x in team_1:
         # n = x['TEAM'].split("#",1)[1]
         team_1_comp = "\n".join(x['TEAM'])
         team_1_score = f" Score: {x['SCORE']}"
         king_score = x['SCORE']


      
      for x in team_2:
         team_2_comp = "\n".join(x['TEAM'])
         team_2_score = f" Score: {x['SCORE']}"

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
      embedVar.add_field(name="Match Type", value=f'{game_type}'.format(bot))
      embedVar.add_field(name="Ranked", value=f'{ranked}'.format(bot))
      if tournament:
         embedVar.add_field(name="Tournament", value="Yes")
      
      if kingsgambit:
         embedVar.add_field(name="Kings Gambit", value="Yes")
      
      if goc:
         embedVar.add_field(name="GODS OF COD", value="Yes")
      
      if kingsgambit and king_score > 0:
         embedVar.add_field(name=f"King - {team_1_score}", value=team_1_comp, inline=False)
      else:
         embedVar.add_field(name=f"Team 1 - {team_1_score}", value=team_1_comp, inline=False)
      
      if team_2_comp:
         embedVar.add_field(name=f"Team 2 - {team_2_score}", value=team_2_comp, inline=False)
      else:
         await ctx.send("No one has joined to compete. ", delete_after=5)
      
      if kingsgambit:
         embedVar.add_field(name=f"Up Next...", value=other_teams_sorted_list, inline=False)

      await ctx.send(embed=embedVar, delete_after=15)
   else:
      await ctx.send("Session does not exist. ", delete_after=5)

#Check your current session
@bot.command()
@commands.check(validate_user)
async def ms(ctx):  
   session_owner = {'OWNER': str(ctx.author), "AVAILABLE": True}
   session = db.querySession(session_owner)
   if session:
      game_query = {'ALIASES': session['GAME']}
      game = db.queryGame(game_query)
      tournament = session['TOURNAMENT']
      kingsgambit = session['KINGSGAMBIT']
      name = session['OWNER'].split("#",1)[0]
      games = game['GAME']
      avatar = game['IMAGE_URL']
      goc = session['GOC']
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
      team_1 = [x for x in teams if x['POSITION'] == 0] # position 0
      team_2 = [x for x in teams if x['POSITION'] == 1] # position 1
      other_teams = [x for x in teams if x['POSITION'] > 1] # position 1


      team_1_comp = ""
      team_2_comp = ""

      team_1_score = ""
      team_2_score = ""

      king_score = 0

      other_teams_comp = []

      for x in team_1:
         # n = x['TEAM'].split("#",1)[1]
         team_1_comp = "\n".join(x['TEAM'])
         team_1_score = f" Score: {x['SCORE']}"
         king_score = x['SCORE']


      
      for x in team_2:
         team_2_comp = "\n".join(x['TEAM'])
         team_2_score = f" Score: {x['SCORE']}"

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
      embedVar.add_field(name="Match Type", value=f'{game_type}'.format(bot))
      embedVar.add_field(name="Ranked", value=f'{ranked}'.format(bot))
      if tournament:
         embedVar.add_field(name="Tournament", value="Yes")
      
      if kingsgambit:
         embedVar.add_field(name="Kings Gambit", value="Yes")

      if goc:
         embedVar.add_field(name="GODS OF COD", value="Yes")
      
      if kingsgambit and king_score > 0:
         embedVar.add_field(name=f"King - {team_1_score}", value=team_1_comp, inline=False)
      else:
         embedVar.add_field(name=f"Team 1 - {team_1_score}", value=team_1_comp, inline=False)
      
      if team_2_comp:
         embedVar.add_field(name=f"Team 2 - {team_2_score}", value=team_2_comp, inline=False)
      else:
         await ctx.send("No one has joined to compete. ", delete_after=5)

      if kingsgambit:
         embedVar.add_field(name=f"Up Next...", value=other_teams_sorted_list, inline=False)

      await ctx.send(embed=embedVar, delete_after=15)
   else:
      await ctx.send("Session does not exist. ", delete_after=5)

''' Team Functions '''
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
   await DM(ctx, user1, f"{ctx.author.mention}" + f" has invited you to join {team_name} !" + f" React in server to join {team_name}" )
   accept = await ctx.send(f"{user1.mention}" +f" do you want to join team {team_name}?".format(bot), delete_after=8)
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

         await ctx.send(response, delete_after=5)
      except:
         print("Team not created. ")
   else:
      await ctx.send("Only the owner of the team can delete the team. ")

''' Check What Session A Player Is In '''
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
      tournament = session['TOURNAMENT']
      kingsgambit = session['KINGSGAMBIT']
      goc = session['GOC']
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
      team_1 = [x for x in teams if x['POSITION'] == 0] # position 0
      team_2 = [x for x in teams if x['POSITION'] == 1] # position 1
      other_teams = [x for x in teams if x['POSITION'] > 1] # position 1


      team_1_comp = ""
      team_2_comp = ""

      team_1_score = ""
      team_2_score = ""

      king_score = 0

      other_teams_comp = []

      for x in team_1:
         # n = x['TEAM'].split("#",1)[1]
         team_1_comp = "\n".join(x['TEAM'])
         team_1_score = f" Score: {x['SCORE']}"
         king_score = x['SCORE']


      
      for x in team_2:
         team_2_comp = "\n".join(x['TEAM'])
         team_2_score = f" Score: {x['SCORE']}"

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
      embedVar.add_field(name="Match Type", value=f'{game_type}'.format(bot))
      embedVar.add_field(name="Ranked", value=f'{ranked}'.format(bot))
      if tournament:
         embedVar.add_field(name="Tournament", value="Yes")
      
      if kingsgambit:
         embedVar.add_field(name="Kings Gambit", value="Yes")
      
      if goc:
         embedVar.add_field(name="GODS OF COD", value="Yes")
      
      if kingsgambit and king_score > 0:
         embedVar.add_field(name=f"King - {team_1_score}", value=team_1_comp, inline=False)
      else:
         embedVar.add_field(name=f"Team 1 - {team_1_score}", value=team_1_comp, inline=False)
      
      if team_2_comp:
         embedVar.add_field(name=f"Team 2 - {team_2_score}", value=team_2_comp, inline=False)
      else:
         await ctx.send("No one has joined to compete. ", delete_after=5)
      
      if kingsgambit:
         embedVar.add_field(name=f"Up Next...", value=other_teams_sorted_list, inline=False)

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
      winner_earned_tourney_cards = False
      winner_earned_tourney_titles = False

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


      elif session_data['RANKED']:
         new_value = {"$inc": {'RANKED.$[type].' + game_type.upper() + '.0': 1}}

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
      await bless(ctx, 10, user)

      await DM(ctx, user, "You Won. Doesnt Prove Much Tho :yawning_face:")

      if winner_earned_tourney_cards or winner_earned_tourney_titles:
         await ctx.send(f"Competitor " + f"{user.mention}" + " earns a victory ! :100:", delete_after=5)
         await ctx.send( f"{user.mention}" + "You have Unlocked New Items in your Vault! :eyes:", delete_after=5)
      else:
         await ctx.send(f"Competitor " + f"{user.mention}" + " earns a victory ! :100:", delete_after=5)



async def sl(ctx):
   session_query = {"OWNER": str(ctx.author), "AVAILABLE": True}
   session_data = db.querySession(session_query)
   if session_data['KINGSGAMBIT']:
      return await ctx.send("Session has ended. See you for the next Kings Gambit!")
   else:
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
         query = {'DISNAME': player['DISNAME']}

         new_value = {}
         if session_data['TOURNAMENT']:
            new_value = {"$set": {'TOURNAMENT_LOSSES': 1}}
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
         await curse(ctx, 5, user)
         await DM(ctx, user, "You Lost. Get back in there :poop:")
         await ctx.send(f"Competitor " + f"{user.mention}" + " took another L! :eyes:", delete_after=5)

      # await ctx.send(loser['TEAM'], delete_after=5)


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


DISCORD_TOKEN = config('DISCORD_TOKEN')

bot.run(DISCORD_TOKEN)