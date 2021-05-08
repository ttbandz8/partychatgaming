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

# PRODUCTION
bot = commands.Bot(command_prefix="#")

# TEST
# bot = commands.Bot(command_prefix=">")

async def validate_user(ctx):
   query = {'DISNAME': str(ctx.author)}
   valid = db.queryUser(query)

   if valid:
      return True
   else:
      msg = await ctx.send(m.USER_NOT_REGISTERED, delete_after=5)
      return False

@bot.event
async def on_ready():
   print('Bot is ready. ')

@bot.command()
@commands.check(validate_user)
async def legend(ctx):
   embed1 = discord.Embed(title= f":crown: " + "Senpai™️ Legend:", description="Use the Reactions to learn with Senpai™️\n:brain: Learn about Exhibitions, Kings Gambit and Gods of COD!\nWrite your name is history...\n*Make sure to say thank you*:heart_exclamation:", colour=000000, value="Page 1")
   embed2 = discord.Embed(color=ctx.author.color).add_field(name=":crown: " + "Senpai™️ Legend:\n" + "#legend = Tournaments!", value="Welcome to Senpai:tm: Legend!\n(Commands are described using a #command 'argument' 'argument' ... etc format.)\n:warning:Do not go on before completing Senpai:tm: Franchise! *#franchise*")
   embed3 = discord.Embed(color=ctx.author.color).add_field(name=":crown: " + "Senpai™️ Legend:\n" + "*Exhibitions* :medal:", value="An Exhibition or Bounty Match is a 1v1 duel between 2 players!\n*Winner Gets 1 Tournament Win*\nHow can you join an exhibition you may ask?\nWell you can't, you must be summoned by one of the Gods\nWhen your time comes, make sure you accept the *invitation*")
   embed4 = discord.Embed(color=ctx.author.color).add_field(name=":crown: " + "Senpai™️ Legend:\n" + "#jkg to Join a *Kings Gambit* :crown:", value="Kings Gambits are King of the Hill style Lobbies where the KING picks the rules\nParty Chat Admins can start Kings Gambits matches open for all players\nPlayers can join using the #jkg 'AdminName' command\nBe the King at the end of the session to win extra :coin: and a Tournament Win!")
   embed5 = discord.Embed(color=ctx.author.color).add_field(name=":crown: " + "Senpai™️ Legend:\n" + "Gods of COD", value="Gods of Cod are the largest CODM tournaments Party Chat Gaming has to offer\nEach Tournament length, prize and rules are different and are announced before Registrations\nAs long as Registrations are open teams can use #rgoc to register their team for GOC\n*NOTE as long as 1 player in your team registers, your entire team will be registed!*")
   embed6 = discord.Embed(color=ctx.author.color).add_field(name=":crown: " + "Senpai™️ Legend:\n" + "Gauntlet Week", value="When the tournamnet starts, registration is closed and the games begin with Gauntlet Week(s)!\nGauntlet week(s) are prolonged periods of fierce competition where teams battle it out to earn the most WINS!\nBrackets will be determined based on the number of wins each team earns during Gauntlet Week!")
   embed7 = discord.Embed(color=ctx.author.color).add_field(name=":crown: " + "Senpai™️ Legend:\n" + "Brackets", value="Brackets take place at the end of Gauntlet Week!\nTeams are places according to the number of wins and compete in single elimination matches\nThe Winner of the brackets earns Tournament exclusive loot !\n*And Bragging rights for life*")
   embed8 = discord.Embed(color=ctx.author.color).add_field(name=":crown: " + "Senpai™️ Legend:\n" + "CONGRATULATIONS !", value="You completed Legend!!\nNow you can start competing in Exhibitions, Kings Gambits, and Gods of Cod Tournaments!!!\nEarn Tournament Wins to gain access to exclusive Cards and Titles and bounties of :coin:!!!\nDon't forget to check out Flex Shop:tm: with that big bag you got now:eyes:\n*Make sure to say thank you*:heart_exclamation:")
   embed9 = discord.Embed(color=ctx.author.color).add_field(name=":crown: " + "Senpai™️:\n" + "GOOD-BYE!", value="*Thank You*:heart_exclamation:")
   paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
   paginator.add_reaction('⏮️', "first")
   paginator.add_reaction('⏪', "back")
   paginator.add_reaction('🔐', "lock")
   paginator.add_reaction('⏩', "next")
   paginator.add_reaction('⏭️', "last")
   embeds = [embed1, embed2, embed3, embed4, embed5, embed6, embed7, embed8,embed9]
   await paginator.run(embeds)


@bot.command()
@commands.check(validate_user)
async def franchise(ctx):
   embed1 = discord.Embed(title= f":checkered_flag: " + "Senpai™️ Franchise:", description="Use the Reactions to learn with Senpai™️\n:brain: Learn how to create and manage your own league team!\nStart Scrimming with other League teams today!\n*Make sure to say thank you*:heart_exclamation:", colour=000000, value="Page 1")
   embed2 = discord.Embed(color=ctx.author.color).add_field(name=":checkered_flag: " + "Senpai™️ Franchise:\n" + "#franchise = Team Play!", value="Welcome to Senpai:tm: Franchise!\n(Commands are described using a #command 'argument' 'argument' ... etc format.)\n:warning:Do not go on before passing Senpai:tm: Bootcamp! *#bootcamp*")
   embed3 = discord.Embed(color=ctx.author.color).add_field(name=":checkered_flag: " + "Senpai™️ Franchise:\n" + "#cteam = Create Team! :military_helmet:", value="Now its time to raise the competition!\nThink you got what it takes to compete with the best teams in the League?\nEverybody starts on Team PCG but you seem ready to go out on your own.\nLet's start by creating our very own CODM team!\nUse #cteam 'game' 'teamname' to create your first team!\nOnce the team is created run a #flex to see your new team added to the card!\n*HINT: use #cteam codm teamname")
   embed4 = discord.Embed(color=ctx.author.color).add_field(name=":checkered_flag: " + "Senpai™️ Franchise:\n" + "#lkt then #dt", value="Now lets dive into your TEAM Page\nThis is where we can see all your stats, team members and even your Team Logo\nRun the #lk command on a user and check if they are apart of a league team\nNow run #lkt 'teamname' to find that users teams\nThis should bring up a new Team Card with the users team information!\nMake sure you scout out the competition!\nTeam owners can use the #dt 'teamname' command to remove a team from the database\n'")
   embed5 = discord.Embed(color=ctx.author.color).add_field(name=":checkered_flag: " + "Senpai™️ Franchise:\n" + "#att = Add To Team ", value="Time to start recruiting TEAMMATES!\nStep 1. Now lets run another #cteam to create a new CODM team\nIf you still OWN a team dont worry skip the first step\nOnce the Team is created make sure you have a teammate ready to REACTION RESPOND!\nUse #att 'DiscordUserName' 'teamname' to invite\nIf your friend accepts your invite they will be added to your team members list!\n*Players can only be apart of 1 team per game choose your alliances wisely!*")
   embed6 = discord.Embed(color=ctx.author.color).add_field(name=":checkered_flag: " + "Senpai™️ Franchise:\n" + "#dtm and #lteam", value="Use #dtm to delete teammates from your League TEAM\nrun #lkt try #dtm 'DiscordName' to remove them\n*Do not delete yourself you will lose your team*\nTo Leave a team that you have already joined use the #lteam 'teamname' command")
   embed7 = discord.Embed(color=ctx.author.color).add_field(name=":checkered_flag: " + "Senpai™️ Franchise:\n" + "SCRIMS! : 3v3 - 5v5", value="Now that you have joined/created a team, its time to compete!\nTeams can compete in NORMAL SCRIMS!\n'SCRIMS' are team based lobbies that can hold up to 10 players!\nThats Right, you can run #c3v3 #c4v4 and #c5v5!\nJust use #c3v3 'type' 'playername' 'playername' to Create a private SCRIM lobby!\n*HINT: #c4v4 and #c5v5 work the same way just add more players !*")
   embed8 = discord.Embed(color=ctx.author.color).add_field(name=":checkered_flag: " + "Senpai™️ Franchise:\n" + "SCRIMS! : #js = Join Session/Join Scrim", value="Remember the #js command from #bootcamp?\nTeam members can join Scrims and via Party using the #js 'Session Owner Name' 'teammate 1' 'teammate 2'\nThis will pull all members into Scrim!\n*Like always this works for 4v4's and 5v5s just add more teammates*")
   embed9 = discord.Embed(color=ctx.author.color).add_field(name=":checkered_flag: " + "Senpai™️ Franchise:\n" + "SCRIMS! : Scorin and Recordin'", value="Now its time to play IRL!\nPlayers get +1 score per round like usually\nTHE SESSION OWNER can score any teammate on the SCORING team to add a point for the team!\nOnce you are done playing IRL the OWNER may use #es to close the session\nThis will record the scores update the user AND TEAM PROFILES! with a W or L\nRemember we are operating off the HONOR system so use *Screenshots* to dispute any *cheating*")
   embed10 = discord.Embed(color=ctx.author.color).add_field(name=":checkered_flag: " + "Senpai™️ Franchise:\n" + "CONGRATULATIONS !", value="You completed franchise!\nNow you can start creating and joining teams!\nWin SCRIMS and earn :coin: to buy new items from the Flex Shop:tm:\nBe vigilant, new teams are created everyday and the GODs have gotten restless...\nToo much cooperation makes little entertainment.. they want a show so we shall set the stage!\nWhen your ready to compete for True Glory use #legend!\n*The First Gods of Cod Tournament took place on October 25th, 2020*")
   paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
   paginator.add_reaction('⏮️', "first")
   paginator.add_reaction('⏪', "back")
   paginator.add_reaction('🔐', "lock")
   paginator.add_reaction('⏩', "next")
   paginator.add_reaction('⏭️', "last")
   embeds = [embed1, embed2, embed3, embed4, embed5, embed6, embed7, embed8, embed9, embed10]
   await paginator.run(embeds)


@bot.command()
@commands.check(validate_user)
async def bootcamp(ctx):
   embed1 = discord.Embed(title= f":military_helmet: " + "Senpai™️ Bootcamp:", description="Use the Reactions to learn with Senpai™️\n:brain: Learn how to Create, Lookup and Record SESSIONS\n*Make sure to say thank you*:heart_exclamation:", colour=000000, value="Page 1")
   embed2 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + "#bootcamp = training!", value="Welcome to Senpai:tm: Bootcamp!\n(Commands are described using a #command 'argument' 'argument' ... etc format.)\n:warning:Do not go on before playing Senpai:tm: Says! *#senpai*")
   embed3 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + "SESSIONS!", value="Now that you're registerd you can create custom sessions!\nThink of sessions like a game lobby!\nYou can open up public sessions, challenge specific players\nYou can even bring along a buddy for 2v2s!\nFirst let's learn to lookup sessions!")
   embed4 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + "#ms , #cs, and #s", value="Now try the #ms command\nIf this is your first time using #ms you should get the following message\n*Session does not exist.*\nThis is because you currently do not *OWN* a SESSION!\nWe will go over how to Create sessions soon but for now...\nUse the #cs 'username' to check if anyone else in the server is playing in a SESSION\nCheck if one of your friends is running their own public session using #s 'username'")
   embed5 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + "#c1v1 = Create 1v1 ", value="Lets create a 1v1 SESSION\nSESSIONS are scored by 'TYPE' either NORMAL or RANKED\nLets create a public NORMAL SESSION\nUse #c1v1 'type'\n*HINT : #c1v1 n*")
   embed6 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + "check.. oops. #ds", value="Great you created a public Normal 1v1 lobby!\nNow lets put that #ms command to good use!\nType *#ms*\nNow you can see the current status of your very own Party Chat Gaming Session!\nPlayers can see that you have opened this session and can check by using the #cs and #s command\nAnd you can too ! go ahead and try #cs 'your user name' and #s 'your user name'\nGreat now we know how to check on open sessions!\nLets go ahead and delete this session use #ds")
   embed7 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + "#Js = Join Session!", value="Players can join each others sessions with #js\n#js allows you to join any public session that is not full\nJust use #js 'playername' to join any open 1v1\n#js works for all match types but well get into those a little bit later!\nFor now lets practice joining sessions and creating lobbies!\nor we can...")
   embed8 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + "#challenge a friend!", value="For those of you who prefer a more *subtle* approach\nUse #challenge 'type' 'username' to directly call out ANY player\nIf your oppenent accepts via *reaction*\nyou will both be pulled into your OWN public 1v1 lobby\nNext we'll learn how to score points and record Wins and Losses.")
   embed9 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + "#score and Win or...", value="Now its time to play IRL!\nPlayers get +1 score per round\nTHE SESSION OWNER must use the #score 'round winner username' to tally score\nOnce you are done playing IRL the OWNER may use #es to close the session\nThis will record the scores update the user profiles with a W or L\nRemember we are operating off the HONOR system so use *Screenshots* to dispute any *cheating*")
   embed10 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + "Team up with #c2v2", value="Grab your friend and battle for double glory!\nCreating 2v2 lobbies is similar to using #challenge !\nInstead of calling your friend out, your Calling them to ACTION!\nLike 1v1, 2v2's are scored by type, either NORMAL or RANKED\nLets create a public NORMAL 2v2 lobby\nUse *#c2v2 'type' 'teamate name'*\nIf your teammate accepts you will be pulled into an open Public 2v2 of the specified type!\nNow other duos can join your 2v2 using #js\n#js 'session owner name' 'teammate name'")
   embed11 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + "CONGRATULATIONS !", value="You completed bootcamp!\nNow you can start creating and joining sessions!\nWin Sessions and earn :coin: to buy new items from the Flex Shop:tm:\nDon't Compete alone... Start a TEAM and win BIG!\nWhen your ready to take your game to the next level use #Franchise!\n*HINT use #iby 'playername' to see how many times you beat another player:eyes:")
   paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
   paginator.add_reaction('⏮️', "first")
   paginator.add_reaction('⏪', "back")
   paginator.add_reaction('🔐', "lock")
   paginator.add_reaction('⏩', "next")
   paginator.add_reaction('⏭️', "last")
   embeds = [embed1, embed2, embed3, embed4, embed5, embed6, embed7, embed8, embed9, embed10, embed11]
   await paginator.run(embeds)


@bot.command()
async def senpai(ctx):
   embed1 = discord.Embed(title= f":man_teacher: " + "Senpai™️", description=" Use the Reactions to learn with Senpai™️\n:brain: Learn how to register!\n*Make sure to say thank you*:heart_exclamation:", colour=000000, value="Page 1")
   #embeds.set_thumbnail(url=avatar)
   embed2 = discord.Embed(color=ctx.author.color).add_field(name=":man_teacher: " + "Senpai™️\n" + "#senpai = Teacher!", value="Good job you did your first command\n(Commands are described using a #command 'argument' 'argument' ... etc format.)\n Let's play Senpai:tm: Says!")
   embed3 = discord.Embed(color=ctx.author.color).add_field(name=":man_teacher: " + "Senpai™️ Says:\n" + "#r = REGISTER !", value="Before you can start competing you first need to register your account!\nDon't Worry we only sweep your internet history once... jk :eyes: ")
   embed4 = discord.Embed(color=ctx.author.color).add_field(name=":man_teacher: " + "Senpai™️ Says:\n" + "#flex = :muscle:", value="Now try the #flex command!\nFlex is where you show off your 'CARDS' and 'TITLES' !\nPersonalize your #flex to standout against the rest of the competition !")
   embed5 = discord.Embed(color=ctx.author.color).add_field(name=":man_teacher: " + "Senpai™️ Says:\n" + "#lk = Lookup:eyes:", value="Lets learn how to use lookup\n#lk 'DiscordUserName' will pull a users data from The Party Chat Gaming Database\n#lk is a great way to check on the stats of any registered player!\nTry #lk 'YourUserName'\nGreat you should see your stats, games, titles and teams !\n *Try #lk on another user for practice*")
   embed6 = discord.Embed(color=ctx.author.color).add_field(name=":man_teacher: " + "Senpai™️ Says:\n" + ":coin: in the #vault", value="Make it Rain or Stack em up!\nYour purchases are stored in YOUR vault!\nEarn coins by competing against other players!\nEarn Titles and Cards by winning Tournaments or Purchasing them in the....")
   embed7 = discord.Embed(color=ctx.author.color).add_field(name=":man_teacher: " + "Senpai™️ Says :\n" + "#shop till you drop!", value="Welcome to the Flex Shop!\nAll the Cards and Titles available for you are here to purchase\nWe can tell if you broke\nDont expect to see the expensive stuff until you got the :coin: for it !")
   embed8 = discord.Embed(color=ctx.author.color).add_field(name=":man_teacher: " + "Senpai™️ Says :\n" + "#vc = View Card", value="You got some coin so why not spend it?\nUse #vc 'cardname' to View Card\n*Type card name exactly as seen*\nYou can use #vc at anytime\nMaybe even to find unknown cards...:eyes:\n *hint try #vc ErenDawn*")
   embed9 = discord.Embed(color=ctx.author.color).add_field(name=":man_teacher: " + "Senpai™️ Says :\n" + "Buy with #bc and #bt", value="Now open up the shop lets buy!\n*hint use #shop\nUse #bc 'cardname' or #bt 'title' to make a purchase !\nRemember you can use #vc to view cards in the shop\nAnd no you can't get those shiny cards in the back just yet...:laugh:")
   embed10 = discord.Embed(color=ctx.author.color).add_field(name=":man_teacher: " + "Senpai™️ Says :\n" + "Update with #uc, #ut", value="Now time to get fresh and go #flex but first\n#vault and lets look at our options\nUse #uc 'cardname' to switch to that brand new card\nNow use #ut 'title' put some respeck on it\nOnce you decided on your new swag hit that #flex")
   embed11 = discord.Embed(color=ctx.author.color).add_field(name=":man_teacher: " + "Senpai™️ Says :\n" + "#ag and start competing!", value="Now You know how to show off your stats\nTime to build your reputation\nAdd the games you want to track using the #ag command\n #ag 'gamename' 'In Game Name'\nYou can update your In Game Name or 'IGN'\nWith the #uign command\n#uign works similar to #ag !\n Just type #uign 'gamename' 'IGN' ")
   embed12 = discord.Embed(color=ctx.author.color).add_field(name=":man_teacher: " + "Senpai™️ Says :\n" + "CONGRATULATIONS !", value="Now you can be take part in all the great features of The Party Chat Gaming:tm: Bot!\nwhen your ready to start making your own custom teams & sessions use #bootcamp!")
   paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
   paginator.add_reaction('⏮️', "first")
   paginator.add_reaction('⏪', "back")
   paginator.add_reaction('🔐', "lock")
   paginator.add_reaction('⏩', "next")
   paginator.add_reaction('⏭️', "last")
   embeds = [embed1, embed2, embed3, embed4, embed5, embed6, embed7, embed8,embed9,embed10,embed11, embed12]
   await paginator.run(embeds)

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
      new_value = {'$set': {'REGISTRATION': False,'AVAILABLE': True}}
      response = db.updateGoc(goc_query, new_value)
      await ctx.send("GODS OF COD has begun. ")
   else:
      print(m.ADMIN_ONLY_COMMAND)

# Create a Goc Session
@bot.command()
@commands.check(validate_user)
async def cgoc(ctx):
   if ctx.author.guild_permissions.administrator == True:
      query = {'AVAILABLE': True}
      g = db.queryGoc(query)
      if g:
         game = [x for x in db.query_all_games()][0]
         session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": g['TYPE'], "TEAMS": [], "RANKED": True, "TOURNAMENT": True, "GOC": True, "GOC_TITLE": g['TITLE']}
         print("Created Session")
         resp = db.createSession(data.newSession(session_query))
         await ctx.send(resp, delete_after=5)
      else:
         await ctx.send(m.TOURNEY_DOES_NOT_EXIST, delete_after=5)
   else:
      await ctx.send(m.ADMIN_ONLY_COMMAND)

# Invite to Gods of Cod
@bot.command()
@commands.check(validate_user)
async def goci(ctx, *participant: User):
   if ctx.author.guild_permissions.administrator == True:
      game = [x for x in db.query_all_games()][0]
      goc_query = {'AVAILABLE': True}
      goc = db.queryGoc(goc_query)

      session_query = {"OWNER": str(ctx.author),'RANKED' : True, 'GOC': True, 'TOURNAMENT': True, 'GOC_TITLE': goc['TITLE'], "AVAILABLE": True}
      current_session = db.querySession(session_query)
      if current_session:
         team_position = 0

         if not bool(current_session['TEAMS']):
            team_position = 0
         else:
            team_position = 1

         if len(participant) < goc['TYPE']:
            await ctx.send(m.TOO_FEW_PLAYERS_ON_TEAM)

         elif len(participant) > goc['TYPE']:
            await ctx.send(m.TOO_MANY_PLAYERS_ON_TEAM)

         elif goc['TYPE'] == 1: 

            if str(participant[0]) in goc['PARTICIPANTS']:
               await DM(ctx, participant[0] ,f"{ctx.author.mention}" + " has invited you to a GOC Tournament Match :eyes:")
               accept = await ctx.send(f"{participant[0].mention}, Will you join the GOC Match? :fire:", delete_after=15)
               
               for emoji in emojis:
                  await accept.add_reaction(emoji)

               def check(reaction, user):
                  return user == participant[0] and str(reaction.emoji) == '👍'
               try:
                  reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=check)

                  join_query = {"TEAM": [str(participant[0])], "SCORE": 0, "POSITION": team_position}
                  resp = db.joinSession(session_query, join_query)
                  print(resp)
                  await ctx.send(resp, delete_after=5)              
               except:
                  await ctx.send("User did not accept.")
            else:
               await ctx.send(m.USER_NOT_REGISTERED_FOR_GOC, delete_after=5)

         elif goc['TYPE'] != 1:
            # Check if same team members
            list_of_teams = set()
            for member in participant:
               member_data = db.queryUser({'DISNAME': str(member)})
               list_of_teams.add(member_data['TEAM'])
            
            if len(list_of_teams) > 1:
               await ctx.send(m.DIFFERENT_TEAMS, delete_after=5)
            else:
               team_name="".join(list_of_teams)
               team_members=[]
               if team_name in goc['PARTICIPANTS']:
                  for member in participant:
                     await DM(ctx, member ,f"{ctx.author.mention}" + " has invited you to a GOC Tournament Match :eyes:")
                     accept = await ctx.send(f"{member.mention}, Will you join the GOC Match? :fire:", delete_after=8)
                     
                     for emoji in emojis:
                        await accept.add_reaction(emoji)

                     def check(reaction, user):
                        return user == member and str(reaction.emoji) == '👍'
                     try:
                        reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=check)
                        team_members.append(str(member))
                        # await ctx.send(f'{member.mention} accepted the ready check!', delete_after=3)
                     except:
                        await ctx.send("User did not accept.")
                  if len(team_members) == goc['TYPE']:
                     join_query = {"TEAM": team_members, "SCORE": 0, "POSITION": team_position}
                     resp = db.joinSession(session_query, join_query)
                     await ctx.send(resp, delete_after=5)      
                  else:
                     await ctx.send(m.FAILED_TO_ACCEPT)                       
               else:
                  await ctx.send(m.USER_NOT_REGISTERED_FOR_GOC, delete_after=5)
      else:
         await ctx.send(m.SESSION_DOES_NOT_EXIST)


   else:
      await ctx.send(m.ADMIN_ONLY_COMMAND)

# Leaderboard
# @bot.command()
# @commands.check(validate_user)
# async def gocleaderboard(ctx, args):
#    goc_data = db.queryGoc({'TITLE': args})
#    if goc_data:
#       print("yes")

# End (complete) Gods of Cod
@bot.command()
@commands.check(validate_user)
async def egoc(ctx):
   if ctx.author.guild_permissions.administrator == True:
      goc_query = {'AVAILABLE': True}
      new_value = {'$set': {'AVAILABLE': False, 'ARCHIVED': True}}
      response = db.updateGoc(goc_query, new_value)
      await ctx.send(m.END_GOC)
   else:
      print(m.ADMIN_ONLY_COMMAND)

# Delete Gods of Cod
@bot.command()
@commands.check(validate_user)
async def dgoc(ctx):
   if ctx.author.guild_permissions.administrator == True:
      goc_query = {'ARCHIVED': False}
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
   if goc_response:
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
   else:
      await ctx.send(m.UNABLE_TO_REGISTER_FOR_GOC)

# Lookup current Gods of Cod
@bot.command()
async def goclk(ctx):
   query = {'ARCHIVED': False}
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
      await ctx.send(m.NO_AVAILABLE_GOC, delete_after=5)

# Lookup archived Gods of Cod
@bot.command()
async def gocarchive(ctx, args):
   query = {'ARCHIVED': True, 'TITLE': args}
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
      winner = g['WINNER']

      

      embedVar = discord.Embed(title=f"GODS OF COD: {title}", description="Party Chat Gaming Database™️", colour=000000)
      embedVar.set_thumbnail(url='https://res.cloudinary.com/dkcmq8o15/image/upload/v1620310701/PCG%20LOGOS%20AND%20RESOURCES/Party_Chat_Archives.png')
      embedVar.set_image(url=avatar)
      embedVar.add_field(name="TEAM TOURNAMENT" , value=str(team_flag))
      embedVar.add_field(name="TOURNAMENT STYLE", value=game_type)
      embedVar.add_field(name="TOURNAMENT AVAILABLE", value=str(available))
      embedVar.add_field(name="TOURNAMENT REGISTRATION", value=str(registration))
      if participants:
         embedVar.add_field(name="Registered Participants", value=participants)
      embedVar.add_field(name="REWARD", value=f"${reward}", inline=False)

      if winner:
         embedVar.add_field(name="Winner", value=winner)
      embedVar.set_footer(text="This GODS OF COD tournament has been archived. ")
      await ctx.send(embed=embedVar)
   else:
      await ctx.send(m.TOURNEY_DOES_NOT_EXIST, delete_after=5)

@bot.command()
async def gocrules(ctx):
   query = {'AVAILABLE': True}
   g = db.queryGoc(query)

   if g:

      embedVar = discord.Embed(title=f"GODS OF COD: RULES", description="Party Chat Gaming Database™️", colour=000000)
      embedVar.add_field(name="Updated Rules for Gods of Cod" , value=m.GODS_OF_COD_RULES)
      await ctx.send(embed=embedVar)
   else:
      await ctx.send(m.NO_AVAILABLE_GOC, delete_after=5)


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

# @bot.command()
# @commands.check(validate_user)
# async def nt(ctx, args1: str, args2: int, args3: int):
#    if ctx.author.guild_permissions.administrator == True:
#       title_query = {'TITLE': str(args1), 'TOURNAMENT_REQUIREMENTS': int(args2), 'PRICE': int(args3)}
#       added = db.createTitle(data.newTitle(title_query))
#       await ctx.send(added, delete_after=3)
#    else:
#       print(m.ADMIN_ONLY_COMMAND)

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
         if card['NAME'] not in vault['CARDS']:
            cards.append({card['NAME']: card['PRICE']})

   title_resp = db.queryShopTitles()
   titles = []
   unavailable_titles = []
   for title in title_resp:
      if title['PRICE'] != 0 and title['PRICE'] < (vault['BALANCE'] + 1000):
         if title['TITLE'] not in vault['TITLES']:
            titles.append({title['TITLE']: title['PRICE']})

 
   cards_to_str = dict(ChainMap(*cards))
   n = dict(sorted(cards_to_str.items(), key=lambda item: item[1]))
   cards_sorted_list = "\n".join(f'{k} : ' +  f" :coin:{'{:,}'.format(v)}"  for k,v in n.items())
   cards_list_array = cards_sorted_list.split("\n")
   
   # Upon adding more cards, be sure it increate the number below
   cards_broken_up = np.array_split(cards_list_array, 7)

   # Upon adding more cards, be sure it increate the number below
   titles_to_str = dict(ChainMap(*titles))
   n = dict(sorted(titles_to_str.items(), key=lambda item: item[1]))
   titles_sorted_list = "\n".join(f'{k} : ' +  f" :coin:{'{:,}'.format(v)}"  for k,v in n.items())
   titles_list_array = titles_sorted_list.split("\n")
   titles_broken_up = np.array_split(titles_list_array, 7)
  
   embed_list = []
   for i in range(0, len(titles_broken_up)):
      globals()['embedVar%s' % i] = discord.Embed(title=f":shopping_cart: Flex Shop", description="To preview cards, use the #vc card command. " + "\n" + "You will unlock more purchasable items as you save and earn more gold. ", colour=000000, value='Page 1')
      globals()['embedVar%s' % i].set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620236723/PCG%20LOGOS%20AND%20RESOURCES/Party_Chat_Shop.png")
      globals()['embedVar%s' % i].add_field(name=":shopping_bags: Available Cards", value="\n".join(cards_broken_up[i]))
      globals()['embedVar%s' % i].add_field(name=":shopping_bags: Available Titles", value="\n".join(titles_broken_up[i]))
      embed_list.append(globals()['embedVar%s' % i])

   paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
   paginator.add_reaction('⏮️', "first")
   paginator.add_reaction('⏪', "back")
   paginator.add_reaction('🔐', "lock")
   paginator.add_reaction('⏩', "next")
   paginator.add_reaction('⏭️', "last")
   embeds = embed_list
   await paginator.run(embeds)


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



# ''' Delete All Cards '''
# @bot.command()
# @commands.check(validate_user)
# async def dac(ctx):
#    user_query = {"DISNAME": str(ctx.author)}
#    if ctx.author.guild_permissions.administrator == True:
#       resp = db.deleteAllCards(user_query)
#       await ctx.send(resp)
#    else:
#       await ctx.send(m.ADMIN_ONLY_COMMAND)


@bot.command()
@commands.check(validate_user)
async def flex(ctx):
   query = {'DISNAME': str(ctx.author)}
   d = db.queryUser(query)

   if d:
      card = db.queryCard({'NAME': d['CARD']})
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
      draw.text((635, 320), titles_text, (255, 255, 255), font=p, align="center")
      draw.text((865, 320), normals_text, (255, 255, 255), font=p, align="center")
      draw.text((1040, 320), ranked_text, (255, 255, 255), font=p, align="center")

      img.save("text.png")

      await ctx.send(file=discord.File("text.png"))

   else:
      await ctx.send(m.USER_NOT_REGISTERED, delete_after=3)


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

      cards_broken_up = np.array_split(cards, 6)
      titles_broken_up = np.array_split(titles, 6)

      if len(cards) < 25:
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
         embed_list = []
         for i in range(0, len(titles_broken_up)):
            globals()['embedVar%s' % i] = discord.Embed(title= f":triangular_flag_on_post: " + f"{name}".format(client) +"\n" + f" :coin:{'{:,}'.format(balance)}", description=":bank: Your Party Chat Gaming Vault™️", colour=000000)
            globals()['embedVar%s' % i].set_thumbnail(url=avatar)
            # embedVar.add_field(name="Balance" + " :fireworks:", value=f":coin:{balance}")
            if bool(cards):
               globals()['embedVar%s' % i].add_field(name="Cards" + " :fireworks:", value="\n".join(cards_broken_up[i]))
            else:
               globals()['embedVar%s' % i].set_footer(text="No Cards available")
            
            if bool(titles):
               globals()['embedVar%s' % i].add_field(name="Titles" + " :fireworks:", value="\n".join(titles_broken_up[i]))
            embed_list.append(globals()['embedVar%s' % i])

         paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
         paginator.add_reaction('⏮️', "first")
         paginator.add_reaction('⏪', "back")
         paginator.add_reaction('🔐', "lock")
         paginator.add_reaction('⏩', "next")
         paginator.add_reaction('⏭️', "last")
         embeds = embed_list
         await paginator.run(embeds)
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

# @bot.command()
# @commands.check(validate_user)
# async def blessall(ctx, args):
#    if ctx.author.guild_permissions.administrator == True:
#       blessAmount = args
#       posBlessAmount = 0 + abs(int(blessAmount))
#       data = db.queryAllVault()
#       for vault in data:
#          vault = db.queryVault({'OWNER' : vault['OWNER']})
#          update_query = {"$inc": {'BALANCE': posBlessAmount}}
#          db.updateVaultNoFilter(vault, update_query)
#       await ctx.send("All have been blessed. ")
#    else:
#       await ctx.send(m.ADMIN_ONLY_COMMAND)



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
   if response:
      vault = db.queryVault({'OWNER': disname})
      if vault:
         await ctx.send(m.VAULT_RECOVERED, delete_after=5)
      else:
         vault = db.createVault(data.newVault({'OWNER' : disname}))
         await ctx.send(m.USER_HAS_REGISTERED, delete_after=5)
   else:
      await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=3)  


'''delete user'''
@bot.command()
@commands.check(validate_user)
async def d(ctx, user: User, args):
   if args == 'IWANTTODELETEMYACCOUNT':
      if str(ctx.author) == str(user):
         query = {'DISNAME': str(ctx.author)}
         user_is_validated = db.queryUser(query)
         if user_is_validated:

            accept = await ctx.send(f"{ctx.author.mention}, are you sure you want to delete your account? " + "\n" + "All of your wins, tournament wins, shop purchases and other earnings will be removed from the system can can not be recovered. ", delete_after=10)
            for emoji in emojis:
               await accept.add_reaction(emoji)

            def check(reaction, user):
               return user == ctx.author and str(reaction.emoji) == '👍'

            try:
               reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=check)

               delete_user_resp = db.deleteUser(query)
               vault = db.queryVault({'OWNER': user_is_validated['DISNAME']})
               if vault:
                  db.deleteVault(vault)
                  print("vault gone")
               else:
                  await ctx.send(delete_user_resp, delete_after=5)
            except:
               await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=3)


            
   else:
      await ctx.send("Invalid command", delete_after=5)


@bot.command()
async def ag(ctx, *args):
   user = {'DISNAME': str(ctx.author)}
   user_data = db.queryUser(user)
 
   if user_data:
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
               await ctx.send(resp, delete_after=5)
         elif title not in user_data['GAMES'] and ign == True:

            if "PCG" in user_data['GAMES']:
               query_to_update_game = {"$set": {"GAMES": [title], "IGN": [{title : args[1]}]}}
               resp = db.updateUserNoFilter(user, query_to_update_game)
               await ctx.send(resp, delete_after=5)
            else:

               query_to_update_game = {"$addToSet": {"GAMES": title, "IGN": {title : args[1]}}}
               resp = db.updateUserNoFilter(user, query_to_update_game)
               await ctx.send(resp, delete_after=5)
   else:
      await ctx.send(m.USER_NOT_REGISTERED, delete_after=5)

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
      await ctx.send(f"{ctx.author.mention}" +" started a *Kings Gambit* :crown:")
   else:
      print(m.ADMIN_ONLY_COMMAND)


@bot.command()
@commands.check(validate_user)
async def jkg(ctx, user1: User):
   session_query = {"OWNER": str(user1), "AVAILABLE": True, "KINGSGAMBIT": True}
   session = db.querySession(session_query)

   if bool(session['TEAMS']):
      teams_list = [x for x in session['TEAMS']]
      current_member = []
      positions = []
      new_position = 0

      if bool(teams_list):
         for x in teams_list:

            if str(ctx.author) in x['TEAM']:

               current_member.append(str(ctx.author))
            positions.append(x['POSITION'])
         new_position = max(positions) + 1

      if not bool(current_member):
         accept = await ctx.send(f"{user1.mention}, Will you allow {ctx.author.mention} to join the Kings Gambit?", delete_after=10)
         for emoji in emojis:
            await accept.add_reaction(emoji)

         def check(reaction, user):
            return user == user1 and str(reaction.emoji) == '👍'

         try:
            reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=check)

            join_query = {"TEAM": [str(ctx.author)], "SCORE": 0, "POSITION": new_position}
            session_joined = db.joinKingsGambit(session_query, join_query)
            await ctx.send(session_joined, delete_after=5)
         except:
            await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=5)
      else:
         await ctx.send(m.ALREADY_IN_SESSION, delete_after=5)
   else:
      accept = await ctx.send(f"{ctx.author.mention}, Will you allow {user1.mention} to join the Kings Gambit?", delete_after=10)
      for emoji in emojis:
         await accept.add_reaction(emoji)

      def check(reaction, user):
         return user == ctx.author and str(reaction.emoji) == '👍'

      try:
         reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=check)
         join_query = {"TEAM": [str(ctx.author)], "SCORE": 0, "POSITION": 0}
         session_joined = db.joinKingsGambit(session_query, join_query)
         await ctx.send(session_joined, delete_after=5)
      except:
         await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=5)

# Skips the player
@bot.command()
@commands.check(validate_user)
async def skipkg(ctx, user: User):
   session_query = {"OWNER": str(ctx.author), "AVAILABLE": True, "KINGSGAMBIT": True}
   session_data = db.querySession(session_query)
   teams = [x for x in session_data['TEAMS']]
   winning_team = {}
   for x in teams:
      if str(user) in x['TEAM'] and x['POSITION'] < 2: 
         winning_team = x

   new_score = winning_team['SCORE'] + 0
   update_query = {'$set': {'TEAMS.$.SCORE': new_score}}
   query = {"_id": session_data["_id"], "TEAMS.TEAM": str(user)}
   response = db.updateSession(session_query, query, update_query)


   positions = []
   loser = {}

   ''' IF POSITIN 0 SKIPS '''
   if winning_team['POSITION'] == 0:

      for x in teams:
         positions.append(x['POSITION'])
         if x['POSITION'] == 0:
            loser = x

      query = {"OWNER": str(ctx.author), "AVAILABLE": True, "KINGSGAMBIT": True}
      update_query = {'$set': {'TEAMS.$[type].POSITION': max(positions) + 1}}
      arrayFilter = [{'type.' + 'TEAM': loser['TEAM']}]
      response = db.updatekg(session_query, query, update_query, arrayFilter)
      
      for x in teams:
         if x['POSITION'] >= 1:
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
         if x['POSITION'] == 1:
            loser = x

      query = {"OWNER": str(ctx.author), "AVAILABLE": True, "KINGSGAMBIT": True}
      update_query = {'$set': {'TEAMS.$[type].POSITION': max(positions) + 1}}
      arrayFilter = [{'type.' + 'TEAM': loser['TEAM']}]
      response = db.updatekg(session_query, query, update_query, arrayFilter)

      # query = {"OWNER": str(ctx.author), "AVAILABLE": True, "KINGSGAMBIT": True}
      # update_query = {'$set': {'TEAMS.$[type].POSITION': 0}}
      # arrayFilter = [{'type.' + 'TEAM': winning_team['TEAM']}]
      # response = db.updatekg(session_query, query, update_query, arrayFilter)

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
      await ctx.send(f"{user.mention}" +f" was skipped this round. ", delete_after=2)
   else:
      await ctx.send(f"Skip not completed. Please, try again. ", delete_after=5) 


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


         session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 2, "TEAMS": [{"TEAM": [str(ctx.author), str(user1)], "SCORE": 0, "POSITION": 0}]}
         if args == "n":
            resp = db.createSession(data.newSession(session_query))
            await ctx.send(resp, delete_after=5)
         elif args == "r":
            session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 2, "TEAMS": [{"TEAM": [str(ctx.author), str(user1)], "SCORE": 0, "POSITION": 0}], "RANKED": True}
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

      # Check if same team members
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
         await ctx.send(m.USER_NOT_REGISTERED)
   else:
      await ctx.send(m.USER_NOT_REGISTERED, delete_after=5)


@bot.command()
@commands.check(validate_user)
async def c4v4(ctx, args, user1: User, user2: User, user3: User):
   if ctx.author.guild_permissions.administrator == True:
      game = [x for x in db.query_all_games()][0]
      
      teammates = [str(user1), str(user2), str(user3)]
      valid_teammates = []

      # Check if same team members
      list_of_teams = set()

      for x in teammates:
         valid = db.queryUser({'DISNAME' : str(x)})
         if valid:
            valid_teammates.append(valid["DISNAME"])
            list_of_teams.add(valid['TEAM'])
         else:
            await ctx.send(f"{valid['DISNAME']} needs to register.".format(bot), delete_after=5)

      if len(valid_teammates) == 3:
         if len(list_of_teams) > 1:
            await ctx.send(m.DIFFERENT_TEAMS, delete_after=5)
         else:
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
         await ctx.send(m.USER_NOT_REGISTERED)
   else:
      await ctx.send(m.USER_NOT_REGISTERED, delete_after=5)


@bot.command()
@commands.check(validate_user)
async def c5v5(ctx, args, user1: User, user2: User, user3: User, user4: User):
   if ctx.author.guild_permissions.administrator == True:
      game = [x for x in db.query_all_games()][0]
      
      teammates = [str(user1), str(user2), str(user3), str(user4)]
      valid_teammates = []

      # Check if same team members
      list_of_teams = set()


      for x in teammates:
         valid = db.queryUser({'DISNAME' : str(x)})
         if valid:
            valid_teammates.append(valid["DISNAME"])
            list_of_teams.add(valid['TEAM'])
         else:
            await ctx.send(f"{valid['DISNAME']} needs to register.".format(bot), delete_after=5)

      if len(valid_teammates) == 4:
         if len(list_of_teams) > 1:
            await ctx.send(m.DIFFERENT_TEAMS, delete_after=5)
         else:
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
         await ctx.send(m.USER_NOT_REGISTERED)
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
   session = db.querySession(session_query)
   teams = [x for x in session['TEAMS']]
   if len(teams) != 1:
      await sw(ctx)
      await sl(ctx)
      end = db.endSession(session_query)
      await ctx.send(end, delete_after=5)
   else:
      end = db.endSession(session_query)
      await ctx.send(m.SESSION_HAS_ENDED)


#delete session from database
@bot.command()
@commands.check(validate_user)
async def ds(ctx):
   session_query = {"OWNER": str(ctx.author), "AVAILABLE": True}
   response = db.deleteSession(session_query)
   await ctx.send(response, delete_after=5)


# ''' Delete All Sessions '''
# @bot.command()
# @commands.check(validate_user)
# async def das(ctx):
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

#Check if User is hosting a session
@bot.command()
@commands.check(validate_user)
async def so(ctx, user: User):
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
      embedVar.add_field(name="Match", value=f'{game_type}'.format(bot))
      embedVar.add_field(name="Type: " + stype, value=f'{ranked}'.format(bot))
      if tournament:
         embedVar.add_field(name="Tournament", value="Yes")
      
      if kingsgambit:
         embedVar.add_field(name="Kings Gambit", value="Yes")
      
      if goc:
         embedVar.add_field(name="GODS OF COD", value="Yes")
      
      if kingsgambit and king_score > 0:
         embedVar.add_field(name=f":crown:King - {team_1_score}", value=team_1_comp, inline=False)
      else:
         embedVar.add_field(name=f":military_helmet:Team 1 - {team_1_score}", value=team_1_comp, inline=False)
      
      if team_2_comp:
         embedVar.add_field(name=f":military_helmet:Team 2 - {team_2_score}", value=team_2_comp, inline=False)
      else:
         embedVar.add_field(name=f":military_helmet:Team 2", value="Vacant", inline=False)
      
      if kingsgambit and other_teams:
         embedVar.add_field(name=f"Up Next...", value=other_teams_sorted_list, inline=False)

      await ctx.send(embed=embedVar, delete_after=15)
   else:
      await ctx.send(m.SESSION_DOES_NOT_EXIST, delete_after=5)

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
      embedVar.add_field(name="Match ", value=f'{game_type}'.format(bot))
      embedVar.add_field(name="Type: " + stype , value=f'{ranked}'.format(bot))
      if tournament:
         embedVar.add_field(name="Tournament", value="Yes")
      
      if kingsgambit:
         embedVar.add_field(name="Kings Gambit", value="Yes")

      if goc:
         embedVar.add_field(name="GODS OF COD : " + f"{gocname}", value="Yes")
      
      if kingsgambit and king_score > 0:
         embedVar.add_field(name=f":crown:King - {team_1_score}", value=team_1_comp, inline=False)
      elif not team_1_score:
         embedVar.add_field(name=f":military_helmet:Team 1", value="Vacant", inline=False)
      else:
         embedVar.add_field(name=f":military_helmet:Team 1 - {team_1_score}", value=team_1_comp, inline=False)
      
      if team_2_comp:
         embedVar.add_field(name=f":military_helmet:Team 2 - {team_2_score}", value=team_2_comp, inline=False)
      else:
         embedVar.add_field(name=f":military_helmet:Team 2", value="Vacant", inline=False)

      if kingsgambit and other_teams:
         embedVar.add_field(name=f"Up Next...", value=other_teams_sorted_list, inline=False)

      await ctx.send(embed=embedVar, delete_after=15)
   else:
      await ctx.send(m.SESSION_DOES_NOT_EXIST, delete_after=5)


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
      print(tournament)
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
      embedVar.add_field(name="Match", value=f'{game_type}'.format(bot))
      embedVar.add_field(name="Type: "+ stype, value=f'{ranked}'.format(bot))
      if tournament:
         embedVar.add_field(name="Tournament", value="Yes")
      
      if kingsgambit:
         embedVar.add_field(name="Kings Gambit", value="Yes")
      
      if goc:
         embedVar.add_field(name="GODS OF COD", value="Yes")
      
      if kingsgambit and king_score > 0:
         embedVar.add_field(name=f":crown:King - {team_1_score}", value=team_1_comp, inline=False)
      elif not team_1_score:
         embedVar.add_field(name=f":military_helmet:Team 1", value="Vacant", inline=False)
      else:
         embedVar.add_field(name=f":military_helmet:Team 1 - {team_1_score}", value=team_1_comp, inline=False)
      
      if team_2_comp:
         embedVar.add_field(name=f":military_helmet:Team 2 - {team_2_score}", value=team_2_comp, inline=False)
      else:
         embedVar.add_field(name=f":military_helmet:Team 2", value="Vacant", inline=False)
      
      if kingsgambit and other_teams:
         embedVar.add_field(name=f"Up Next...", value=other_teams_sorted_list, inline=False)

      await ctx.send(embed=embedVar, delete_after=15)
   else:
      await ctx.send(m.SESSION_DOES_NOT_EXIST, delete_after=5)


''' Team Functions '''
@bot.command()
@commands.check(validate_user)
async def cteam(ctx, args1, *args):
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
async def att(ctx, user1: User):
   owner_profile = db.queryUser({'DISNAME': str(ctx.author)})
   team_profile = db.queryTeam({'TNAME': owner_profile['TEAM']})

   if owner_profile['TEAM'] == 'PCG':
      await ctx.send(m.USER_NOT_ON_TEAM, delete_after=5)
   else:

      if owner_profile['DISNAME'] == team_profile['OWNER']:

         member_profile = db.queryUser({'DISNAME': str(user1)})
         # If user is part of a team you cannot add them to your team
         if member_profile['TEAM'] == 'PCG':
            await DM(ctx, user1, f"{ctx.author.mention}" + f" has invited you to join {team_profile['TNAME']} !" + f" React in server to join {team_profile['TNAME']}" )
            accept = await ctx.send(f"{user1.mention}" +f" do you want to join team {team_profile['TNAME']}?".format(bot), delete_after=10)
            for emoji in emojis:
               await accept.add_reaction(emoji)

            def check(reaction, user):
               return user == user1 and str(reaction.emoji) == '👍'

            try:
               confirmed = await bot.wait_for('reaction_add', timeout=5.0, check=check)
               team_query = {'TNAME': team_profile['TNAME']}
               new_value_query = {'$push': {'MEMBERS': str(user1)}}
               response = db.addTeamMember(team_query, new_value_query, str(ctx.author), str(user1))
               await ctx.send(response, delete_after=5)
            except:
               await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=3)
         else:
            await ctx.send(m.USER_ALREADY_ON_TEAM, delete_after=5)

      else:
         await ctx.send(m.OWNER_ONLY_COMMAND, delete_after=5)

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
      scrim_wins = team['SCRIM_WINS']
      scrim_losses = team['SCRIM_LOSSES']
      tournament_wins = team['TOURNAMENT_WINS']
      logo = team['LOGO_URL']

      team_list = []
      for members in team['MEMBERS']:
         mem_query = db.queryUser({'DISNAME': members})
         ign_list = [x for x in mem_query['IGN']]
         ign_list_keys = [k for k in ign_list[0].keys()]
         if ign_list_keys == games:
            team_list.append(f"{ign_list[0][games[0]]}") 
         else:
            team_list.append(f"{members}")


      embedVar = discord.Embed(title=f":checkered_flag: {team_name}' Team Card".format(bot), description=":bank: Party Chat Gaming Database", colour=000000)
      if team['LOGO_FLAG']:
         embedVar.set_image(url=logo)
      embedVar.add_field(name="Games :video_game:", value=f'{games[0]}'.format(bot))
      embedVar.add_field(name="Members :military_helmet:", value="\n".join(f'{t}'.format(bot) for t in team_list), inline=False)
      embedVar.add_field(name="Scrim Wins :medal:", value=scrim_wins)
      embedVar.add_field(name="Scrim Losses :crossed_swords:", value=scrim_losses)
      embedVar.add_field(name="Tournament Wins :fireworks:", value=tournament_wins, inline=False)

      await ctx.send(embed=embedVar, delete_after=20)
   else:
      await ctx.send(m.TEAM_DOESNT_EXIST, delete_after=5)


@bot.command()
@commands.check(validate_user)
async def dtm(ctx, user1: User):
   owner_profile = db.queryUser({'DISNAME': str(ctx.author)})
   team_profile = db.queryTeam({'TNAME': owner_profile['TEAM']})
   if team_profile:
      if owner_profile['DISNAME'] == team_profile['OWNER']:

            accept = await ctx.send(f"Do you want to remove {user1.mention} from the {team_profile['TNAME']}?".format(bot), delete_after=8)
            for emoji in emojis:
               await accept.add_reaction(emoji)

            def check(reaction, user):
               return user == ctx.author and str(reaction.emoji) == '👍'

            try:
               confirmed = await bot.wait_for('reaction_add', timeout=5.0, check=check)
               team_query = {'TNAME': team_profile['TNAME']}
               new_value_query = {'$pull': {'MEMBERS': str(user1)}}
               response = db.deleteTeamMember(team_query, new_value_query, str(user1))
               await ctx.send(response, delete_after=5)
            except:
               print("Team not created. ")
      else:
         await ctx.send(m.OWNER_ONLY_COMMAND, delete_after=5)
   else:
      await ctx.send(m.TEAM_DOESNT_EXIST, delete_after=5)

@bot.command()
@commands.check(validate_user)
async def lteam(ctx):
   member_profile = db.queryUser({'DISNAME': str(ctx.author)})
   team_profile = db.queryTeam({'TNAME': member_profile['TEAM']})
   if team_profile:

            accept = await ctx.send(f"Do you want to leave team {member_profile['TEAM']}?".format(bot), delete_after=8)
            for emoji in emojis:
               await accept.add_reaction(emoji)

            def check(reaction, user):
               return user == ctx.author and str(reaction.emoji) == '👍'

            try:
               confirmed = await bot.wait_for('reaction_add', timeout=5.0, check=check)
               team_query = {'TNAME': member_profile['TEAM']}
               new_value_query = {'$pull': {'MEMBERS': str(ctx.author)}}
               response = db.deleteTeamMember(team_query, new_value_query, str(ctx.author))
               await ctx.send(response, delete_after=5)
            except:
               print("Team not created. ")

   else:
      await ctx.send(m.TEAM_DOESNT_EXIST, delete_after=5)

@bot.command()
@commands.check(validate_user)
async def dt(ctx, *args):
   team_name = " ".join([*args])
   team_query = {'OWNER': str(ctx.author), 'TNAME': team_name}
   team = db.queryTeam(team_query)
   if team:
      if team['OWNER'] == str(ctx.author):
         accept = await ctx.send(f"Do you want to delete the {team['GAMES'][0]} team {team_name}?".format(bot), delete_after=10)
         for emoji in emojis:
            await accept.add_reaction(emoji)

         def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '👍'

         try:
            confirmed = await bot.wait_for('reaction_add', timeout=8.0, check=check)
            response = db.deleteTeam(team, str(ctx.author))

            user_query = {'DISNAME': str(ctx.author)}
            new_value = {'$set': {'TEAM': 'PCG'}}
            db.updateUserNoFilter(user_query, new_value)

            await ctx.send(response, delete_after=5)
         except:
            print("Team not created. ")
      else:
         await ctx.send("Only the owner of the team can delete the team. ")
   else:
      await ctx.send(m.TEAM_DOESNT_EXIST, delete_after=5)


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

   query = {"_id": session_data["_id"], "TEAMS.TEAM": str(ctx.author)}
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
      await bless(ctx, blessings, user)

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

# if NODE_ENV == 'Production':
#    DISCORD_TOKEN = config('DISCORD_TOKEN_PROD')   
# else:
#    DISCORD_TOKEN = config('DISCORD_TOKEN_TEST')

@bot.command()
async def newgame(ctx, *args):
   if ctx.author.guild_permissions.administrator == True:
      game_name = " ".join([*args])
      # games = [x for x in db.query_all_games()][0]
      
      response = db.addGame(data.newGame({'GAME': game_name}))
      await ctx.send(response, delete_after=5)
   else:
      await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=5)


@bot.command()
async def addgamealiases(ctx, *args):
   if ctx.author.guild_permissions.administrator == True:
      admin = db.queryUser({'DISNAME': str(ctx.author)})
      if not args:
         await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=5)
      else:
         # game = admin['GAMES'][0]
         test_game = "Call Of Duty Mobile"

         aliases = []

         for title in args:
            aliases.append(title)

         query = {'GAME': test_game}
         new_value = {'$set': {'ALIASES': aliases}}

         response = db.updateGame(query, new_value)
         await ctx.send(m.UPDATE_COMPLETE, delete_after=5)

@bot.command()
async def addgamealias(ctx, *args):
   if ctx.author.guild_permissions.administrator == True:
      alias = " ".join([*args])
      admin = db.queryUser({'DISNAME': str(ctx.author)})
      if not args:
         await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=5)
      else:
         # game = admin['GAMES'][0]
         test_game = "Call Of Duty Mobile"

         query = {'GAME': test_game}
         new_value = {'$addToSet': {'ALIASES': alias}}

         response = db.updateGame(query, new_value)
         await ctx.send(m.UPDATE_COMPLETE, delete_after=5)

@bot.command()
async def addgametypes(ctx, *args):
   if ctx.author.guild_permissions.administrator == True:
      admin = db.queryUser({'DISNAME': str(ctx.author)})
      if not args:
         await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=5)
      else:
         # game = admin['GAMES'][0]
         test_game = "Call Of Duty Mobile"

         types = []

         for gametype in args:
            types.append(gametype)

         query = {'GAME': test_game}
         new_value = {'$set': {'TYPE': types}}

         response = db.updateGame(query, new_value)
         await ctx.send(m.UPDATE_COMPLETE, delete_after=5)

@bot.command()
async def addgameimage(ctx, args):
   if ctx.author.guild_permissions.administrator == True:
      admin = db.queryUser({'DISNAME': str(ctx.author)})
      if not args:
         await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=5)
      else:

         test_game = "Call Of Duty Mobile"

         query = {'GAME': test_game}
         new_value = {'$set': {'IMAGE_URL': args}}

         response = db.updateGame(query, new_value)
         await ctx.send(m.UPDATE_COMPLETE, delete_after=5)


@bot.command()
async def deletegame(ctx, *args):
   if ctx.author.guild_permissions.administrator == True:
      game_name = " ".join([*args])
      admin = db.queryUser({'DISNAME': str(ctx.author)})
      if not args:
         await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=5)
      else:
         query = {'GAME': game_name}
         response = db.deleteGame(query)
         await ctx.send(m.DELETE_COMPLETE, delete_after=5)

@bot.command()
# @commands.check(validate_user)
async def lkg(ctx):
   data = db.query_all_games()

   if data:

      game_list = []
      for game in data:
         game_list.append(game)

      game_title_list = []

      for title in game_list:
         game_title_list.append(title['GAME'])

      embedVar = discord.Embed(title=f"Games Lookup", description=":bank: Party Chat Gaming Database", colour=000000)
      embedVar.add_field(name="Games", value="\n".join(game_title_list))
      embedVar.set_footer(text="More games will be added soon. ")

      await ctx.send(embed=embedVar, delete_after=20)
   else:
      await ctx.send(m.NO_GAMES_AVAILABLE, delete_after=5)

# REVERSE THIS UPON DEPLOYMENT
# DISCORD_TOKEN = config('DISCORD_TOKEN_TEST')
DISCORD_TOKEN = config('DISCORD_TOKEN_PROD')
bot.run(DISCORD_TOKEN)