import discord
from discord.ext import commands
import bot as main
import db
import classes as data
import messages as m
import numpy as np
import help_commands as h
# Converters
from discord import User
from discord import Member
from PIL import Image, ImageFont, ImageDraw
import requests
from collections import ChainMap
import DiscordUtils

emojis = ['👍', '👎']

class Gods(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Gods Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @commands.command()
    async def gods(self, ctx, args1: str, args2: int, args3: int, args4: str, *args: str ):
        if ctx.author.guild_permissions.administrator == True:
            game_name = " ".join([*args])
            query = {'ALIASES': game_name.lower()}
            game = db.queryGame(query)

            team_flag = False
            if args2 > 1:
                team_flag = True

            gods_query = {'TITLE': args1, 'TYPE': args2, 'TEAM_FLAG': team_flag, 'REWARD': args3, 'IMG_URL': args4, 'GAME': game['GAME'], 'REGISTRATION': True}
            response = db.createGods(data.newGods(gods_query))
            await ctx.send(response)
        else:
            print(m.ADMIN_ONLY_COMMAND)
    
    @commands.command()
    async def startgods(self, ctx):
        if ctx.author.guild_permissions.administrator == True:
            gods_query = {'REGISTRATION': True}
            new_value = {'$set': {'REGISTRATION': False,'AVAILABLE': True}}
            response = db.updateGods(gods_query, new_value)
            await ctx.send("Gods has begun. ")
        else:
            print(m.ADMIN_ONLY_COMMAND)

    @commands.command()
    async def cgods(self, ctx):
        if ctx.author.guild_permissions.administrator == True:
            query = {'AVAILABLE': True}
            g = db.queryGods(query)
            if g:
                session_query = {"OWNER": str(ctx.author), "GAME": g["GAME"], "TYPE": g['TYPE'], "TEAMS": [], "TOURNAMENT": True, "GODS": True, "GODS_TITLE": g['TITLE']}
                resp = db.createSession(data.newSession(session_query))
                await ctx.send(resp)
            else:
                await ctx.send(m.TOURNEY_DOES_NOT_EXIST)
        else:
            await ctx.send(m.ADMIN_ONLY_COMMAND)

    @commands.command()
    async def godsi(self, ctx, *participant: User):
        if ctx.author.guild_permissions.administrator == True:
            gods_query = {'AVAILABLE': True}
            gods = db.queryGods(gods_query)

            session_query = {"OWNER": str(ctx.author), 'GODS': True, 'TOURNAMENT': True, 'GODS_TITLE': gods['TITLE'], "AVAILABLE": True}
            current_session = db.querySession(session_query)
            if current_session:
                team_position = 0

                if not bool(current_session['TEAMS']):
                    team_position = 0
                else:
                    team_position = 1

                if len(participant) < gods['TYPE']:
                    await ctx.send(m.TOO_FEW_PLAYERS_ON_TEAM)

                elif len(participant) > gods['TYPE']:
                    await ctx.send(m.TOO_MANY_PLAYERS_ON_TEAM)

                elif gods['TYPE'] == 1: 

                    if str(participant[0]) in gods['PARTICIPANTS']:
                        await main.DM(ctx, participant[0] ,f"{ctx.author.mention}" + " has invited you to a Gods Tournament Match :eyes:")
                        accept = await ctx.send(f"{participant[0].mention}, Will you join the Gods Match? :fire:")
                    
                        for emoji in emojis:
                            await accept.add_reaction(emoji)

                        def check(reaction, user):
                            return user == participant[0] and str(reaction.emoji) == '👍'
                        try:
                            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)

                            join_query = {"TEAM": [str(participant[0])], "SCORE": 0, "POSITION": team_position}
                            resp = db.joinSession(session_query, join_query)
                            print(resp)
                            await ctx.send(resp)              
                        except:
                            await ctx.send("User did not accept.")
                    else:
                        await ctx.send(m.USER_NOT_REGISTERED_FOR_GODS)

                elif gods['TYPE'] != 1:
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
                    if team_name in gods['PARTICIPANTS']:
                        for member in participant:
                            await main.DM(ctx, member ,f"{ctx.author.mention}" + " has invited you to a Gods Tournament Match :eyes:")
                            accept = await ctx.send(f"{member.mention}, Will you join the Gods Match? :fire:", delete_after=8)
                            
                            for emoji in emojis:
                                await accept.add_reaction(emoji)

                            def check(reaction, user):
                                return user == member and str(reaction.emoji) == '👍'
                            try:
                                reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                                team_members.append(str(member))
                                # await ctx.send(f'{member.mention} accepted the ready check!', delete_after=3)
                            except:
                                await ctx.send("User did not accept.")
                        if len(team_members) == gods['TYPE']:
                            join_query = {"TEAM": team_members, "SCORE": 0, "POSITION": team_position}
                            resp = db.joinSession(session_query, join_query)
                            await ctx.send(resp, delete_after=5)      
                        else:
                            await ctx.send(m.FAILED_TO_ACCEPT)                       
                    else:
                        await ctx.send(m.USER_NOT_REGISTERED_FOR_GODS, delete_after=5)
            else:
                await ctx.send(m.SESSION_DOES_NOT_EXIST)

        else:
            await ctx.send(m.ADMIN_ONLY_COMMAND)

    @commands.command()
    async def endgods(self, ctx):
        if ctx.author.guild_permissions.administrator == True:
            gods_query = {'AVAILABLE': True}
            new_value = {'$set': {'AVAILABLE': False, 'ARCHIVED': True}}
            response = db.updateGods(gods_query, new_value)
            await ctx.send(m.END_GODS)
        else:
            print(m.ADMIN_ONLY_COMMAND)

    @commands.command()
    async def deletegods(self, ctx):
        if ctx.author.guild_permissions.administrator == True:
            gods_query = {'ARCHIVED': False}
            response = db.deleteGods(gods_query)
            await ctx.send("Gods has ended. ")
        else:
            print(m.ADMIN_ONLY_COMMAND)

    @commands.command()
    async def rgods(self, ctx):
        gods_query = {'REGISTRATION': True}
        gods_response = db.queryGods(gods_query)
        if gods_response:
            user = str(ctx.author)
            user_data = db.queryUser({'DISNAME': str(ctx.author)})

            if gods_response['GAME'] in user_data['GAMES']:
                if gods_response['TEAM_FLAG']:
                    if user_data['TEAM'] == 'PCG':
                        await ctx.send("This is a Team Only Tournament. ")
                    else:
                        # Make it so that Team Owner has to be the one to register the team
                        team_data = db.queryTeam({'TNAME': user_data['TEAM']})
                        if gods_response['GAME'] in team_data['GAMES']:

                            if team_data['OWNER'] == str(ctx.author):
                                if len(team_data['MEMBERS']) >= gods_response['TYPE']:
                                    new_value =  {'$addToSet': {'PARTICIPANTS': str(team_data['TNAME'])}}
                                    response = db.updateGods(gods_query, new_value)
                                    await ctx.send(f"{team_data['TNAME']} is now registered for Gods. ")
                                else:
                                    await ctx.send(f"{team_data['TNAME']} does not have enough members to participate in this tournament. ")       
                            else:
                                await ctx.send("Only the owner of the team can register team for Tournaments. ")
                        else:

                            await ctx.send(m.ADD_A_GAME)
                else:
                    if user in gods_response['PARTICIPANTS']:
                        await ctx.send(m.ALREADY_IN_TOURNEY)
                    else:
                        new_value =  {'$addToSet': {'PARTICIPANTS': user}}
                        response = db.updateGods(gods_query, new_value)
                        await ctx.send(f"{ctx.author.mention} is now registered for Gods. ")
            
            else:
                await ctx.send(m.ADD_A_GAME)                
        else:
            await ctx.send(m.UNABLE_TO_REGISTER_FOR_GODS)

    @commands.command()
    async def godslk(self, ctx):
        query = {'ARCHIVED': False}
        g = db.queryGods(query)

        if g:
            title = g['TITLE']
            team_flag = g['TEAM_FLAG']
            game = g['GAME']
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

            

            embedVar = discord.Embed(title=f":checkered_flag: {title}", description=f"{game} Party Chat Gaming Tournament™️", colour=000000)
            embedVar.set_image(url=avatar)
            embedVar.add_field(name=":military_helmet: TEAM TOURNAMENT" , value=str(team_flag))
            embedVar.add_field(name=":skull_crossbones:  TOURNAMENT STYLE", value=game_type)
            embedVar.add_field(name=":video_game: GAME", value=game)
            embedVar.add_field(name=":zap: AVAILABLE", value=str(available))
            embedVar.add_field(name=":sparkler: REGISTRATION", value=str(registration))
            if participants:
                embedVar.add_field(name="Registered Participants", value=participants)
            embedVar.add_field(name=":moneybag: REWARD", value=f"${reward}")
            await ctx.send(embed=embedVar)
        else:
            await ctx.send(m.NO_AVAILABLE_GODS)

    @commands.command()
    async def godsarchive(self, ctx, *args):
        title = " ".join([*args])
        query = {'ARCHIVED': True, 'TITLE': title}
        g = db.queryGods(query)

        if g:
            title = g['TITLE']
            team_flag = g['TEAM_FLAG']
            game = g['GAME']
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

            

            embedVar = discord.Embed(title=f"{title}", description=f"{game} Party Chat Gaming Tournament™™️", colour=000000)
            embedVar.set_thumbnail(url='https://res.cloudinary.com/dkcmq8o15/image/upload/v1620310701/PCG%20LOGOS%20AND%20RESOURCES/Party_Chat_Archives.png')
            embedVar.set_image(url=avatar)
            embedVar.add_field(name="TEAM TOURNAMENT" , value=str(team_flag))
            embedVar.add_field(name="TOURNAMENT STYLE", value=game_type)
            embedVar.add_field(name="GAME", value=game)
            embedVar.add_field(name="TOURNAMENT AVAILABLE", value=str(available))
            embedVar.add_field(name="TOURNAMENT REGISTRATION", value=str(registration))
            if participants:
                embedVar.add_field(name="Registered Participants", value=participants)
            embedVar.add_field(name="REWARD", value=f"${reward}", inline=False)

            if winner:
                embedVar.add_field(name="Winner", value=winner)
            embedVar.set_footer(text="This Gods tournament has been archived. ")
            await ctx.send(embed=embedVar)
        else:
            await ctx.send(m.TOURNEY_DOES_NOT_EXIST, delete_after=5)

    @commands.command()
    async def godsrules(self, ctx):
        query = {'AVAILABLE': True}
        g = db.queryGods(query)
        if g:
            embedVar = discord.Embed(title=f"GODS OF COD: RULES", description="Party Chat Gaming Database™️", colour=000000)
            embedVar.add_field(name="Updated Rules for Gods of Cod" , value=m.GODS_OF_COD_RULES)
            await ctx.send(embed=embedVar)
        else:
            await ctx.send(m.NO_AVAILABLE_GOC, delete_after=5)

def setup(bot):
    bot.add_cog(Gods(bot))

# Leaderboard
# @bot.command()
# @commands.check(validate_user)
# async def godsleaderboard(ctx, args):
#    gods_data = db.queryGods({'TITLE': args})
#    if gods_data:
#       print("yes")