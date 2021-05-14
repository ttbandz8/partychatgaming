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

class Godsofcod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Gods Of Cod Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @commands.command()
    async def goc(self, ctx, args1: str, args2: int, args3: bool, args4: int, args5: str ):
        if ctx.author.guild_permissions.administrator == True:
            goc_query = {'TITLE': args1, 'TYPE': args2, 'TEAM_FLAG': args3, 'REWARD': args4, 'IMG_URL': args5, 'REGISTRATION': True}
            response = db.createGoc(data.newGoc(goc_query))
            await ctx.send(response)
        else:
            print(m.ADMIN_ONLY_COMMAND)
    
    @commands.command()
    async def sgoc(self, ctx):
        if ctx.author.guild_permissions.administrator == True:
            goc_query = {'REGISTRATION': True}
            new_value = {'$set': {'REGISTRATION': False,'AVAILABLE': True}}
            response = db.updateGoc(goc_query, new_value)
            await ctx.send("GODS OF COD has begun. ")
        else:
            print(m.ADMIN_ONLY_COMMAND)

    @commands.command()
    async def cgoc(self, ctx):
        if ctx.author.guild_permissions.administrator == True:
            query = {'AVAILABLE': True}
            g = db.queryGoc(query)
            if g:
                game = [x for x in db.query_all_games()][0]
                session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": g['TYPE'], "TEAMS": [], "RANKED": True, "TOURNAMENT": True, "GOC": True, "GOC_TITLE": g['TITLE']}
                resp = db.createSession(data.newSession(session_query))
                await ctx.send(resp, delete_after=5)
            else:
                await ctx.send(m.TOURNEY_DOES_NOT_EXIST, delete_after=5)
        else:
            await ctx.send(m.ADMIN_ONLY_COMMAND)

    @commands.command()
    async def goci(self, ctx, *participant: User):
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
                        await main.DM(ctx, participant[0] ,f"{ctx.author.mention}" + " has invited you to a GOC Tournament Match :eyes:")
                        accept = await ctx.send(f"{participant[0].mention}, Will you join the GOC Match? :fire:", delete_after=15)
                    
                    for emoji in emojis:
                        await accept.add_reaction(emoji)

                    def check(reaction, user):
                        return user == participant[0] and str(reaction.emoji) == '👍'
                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)

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
                            await main.DM(ctx, member ,f"{ctx.author.mention}" + " has invited you to a GOC Tournament Match :eyes:")
                            accept = await ctx.send(f"{member.mention}, Will you join the GOC Match? :fire:", delete_after=8)
                            
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

    @commands.command()
    async def egoc(self, ctx):
        if ctx.author.guild_permissions.administrator == True:
            goc_query = {'AVAILABLE': True}
            new_value = {'$set': {'AVAILABLE': False, 'ARCHIVED': True}}
            response = db.updateGoc(goc_query, new_value)
            await ctx.send(m.END_GOC)
        else:
            print(m.ADMIN_ONLY_COMMAND)

    @commands.command()
    async def dgoc(self, ctx):
        if ctx.author.guild_permissions.administrator == True:
            goc_query = {'ARCHIVED': False}
            response = db.deleteGoc(goc_query)
            await ctx.send("GODS OF COD has ended. ")
        else:
            print(m.ADMIN_ONLY_COMMAND)

    @commands.command()
    async def rgoc(self, ctx):
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

    @commands.command()
    async def goclk(self, ctx):
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

    @commands.command()
    async def gocarchive(self, ctx, args):
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

    @commands.command()
    async def gocrules(self, ctx):
        query = {'AVAILABLE': True}
        g = db.queryGoc(query)
        if g:
            embedVar = discord.Embed(title=f"GODS OF COD: RULES", description="Party Chat Gaming Database™️", colour=000000)
            embedVar.add_field(name="Updated Rules for Gods of Cod" , value=m.GODS_OF_COD_RULES)
            await ctx.send(embed=embedVar)
        else:
            await ctx.send(m.NO_AVAILABLE_GOC, delete_after=5)

def setup(bot):
    bot.add_cog(Godsofcod(bot))

# Leaderboard
# @bot.command()
# @commands.check(validate_user)
# async def gocleaderboard(ctx, args):
#    goc_data = db.queryGoc({'TITLE': args})
#    if goc_data:
#       print("yes")