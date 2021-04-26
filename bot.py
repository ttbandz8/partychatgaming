import db
import time
import classes as data
import test_data as td
import discord
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

@client.event
async def on_ready():
   print('Plugged in as {0.user}'.format(client))


@client.event
async def on_message(message):
   #### VARIABLES ####
   server = message.guild
   author = message.author
   channel = message.channel
   name = author.name
   mentions = message.mentions
   # mentioned = f'{mentions[0].name}#{mentions[0].discriminator}'.format(client)
   msg = message.content

   if message.author == client.user:
        return
   
   if msg.startswith("$pcg"):
      command = msg.split()
      more_than_two_args = len(command) == 3

      if len(command) == 1:
         await channel.send("Invalid command. ")
      else:
         
         # REGISTER USER
         if command[1] == 'register' and not more_than_two_args:
            user = {'DISNAME': str(author), 'AVATAR': str(author.avatar_url)}
            response = db.createUsers(data.newUser(user))
            await channel.send(response)
         
         # QUERY USER
         elif mentions and not more_than_two_args:
            mentioned = f'{mentions[0].name}#{mentions[0].discriminator}'.format(client)
            query = {'DISNAME': mentioned}
            d = db.queryUser(query)
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
            embedVar.add_field(name="Titles", value=' '.join(str(x) for x in titles), inline=False)
            embedVar.add_field(name="Ranked Wins", value="\n".join(f'{k}: {v}' for k,v in rwins_to_string.items()))
            embedVar.add_field(name="Ranked Losses", value="\n".join(f'{k}: {v}' for k,v in rlosses_to_string.items()))
            embedVar.add_field(name="Normal Wins", value="\n".join(f'{k}: {v}' for k,v in urwins_to_string.items()))
            embedVar.add_field(name="Normal Losses", value="\n".join(f'{k}: {v}' for k,v in urlosses_to_string.items()))
            embedVar.add_field(name="Tournament Wins", value=tournament_wins)
            await channel.send(embed=embedVar)
         else:
            await channel.send("Invalid command. ")
      

DISCORD_TOKEN = config('DISCORD_TOKEN')

client.run(DISCORD_TOKEN)
