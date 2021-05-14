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

class Lobbies(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print('Lobbies Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @commands.command()
    async def c1v1(self, ctx, args):
        game = [x for x in db.query_all_games()][0]
        session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 1, "TEAMS": [{"TEAM": [str(ctx.author)], "SCORE": 0, "POSITION": 0}]}
        if args == "n":
            resp = db.createSession(data.newSession(session_query))
            await ctx.send(resp, delete_after=5)
        elif args == "r":
            session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 1, "TEAMS": [{"TEAM": [str(ctx.author)], "SCORE": 0, "POSITION": 0}], "RANKED": True}
            resp = db.createSession(data.newSession(session_query))
            await ctx.send(resp, delete_after=5)

    @commands.command()
    async def c2v2(self, ctx, args, user1: User):
        game = [x for x in db.query_all_games()][0]
        
        validate_teammate = db.queryUser({'DISNAME': str(user1)})

        if validate_teammate:
            accept = await ctx.send(f"{user1.mention}, Will you join the lobby?", delete_after=10)
            for emoji in emojis:
                await accept.add_reaction(emoji)

            def check(reaction, user):
                return user == user1 and str(reaction.emoji) == '👍'

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)


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

    @commands.command()
    async def c3v3(self, ctx, args, user1: User, user2: User):
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
                    await ctx.send(f"{valid['DISNAME']} needs to register.".format(self), delete_after=5)


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
 
    @commands.command()
    async def c4v4(self, ctx, args, user1: User, user2: User, user3: User):
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
                    await ctx.send(f"{valid['DISNAME']} needs to register.".format(self), delete_after=5)

            if len(valid_teammates) == 3:
                if len(list_of_teams) > 1:
                    await ctx.send(m.DIFFERENT_TEAMS, delete_after=5)
                else:
                    accept = await ctx.send("SCRIM STARTING : 4v4 ", delete_after=10)
                    session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 4, "SCRIM": True, "TEAMS": [{"TEAM": [str(ctx.author), str(user1), str(user2), str(user3)], "SCORE": 0, "POSITION": 0}]}
                    if args == "n":
                        resp = db.createSession(data.newSession(session_query))
                        await ctx.send(resp)
                    elif args == "r":
                        session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 4, "SCRIM": True, "TEAMS": [{"TEAM": [str(ctx.author), str(user1), str(user2), str(user3)], "SCORE": 0, "POSITION": 0}], "RANKED": True}
                        resp = db.createSession(data.newSession(session_query))
                        await ctx.send(resp)
            else:
                await ctx.send(m.USER_NOT_REGISTERED)
        else:
            await ctx.send(m.USER_NOT_REGISTERED, delete_after=5)
 
    @commands.command()
    async def c5v5(self, ctx, args, user1: User, user2: User, user3: User, user4: User):
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
                    await ctx.send(f"{valid['DISNAME']} needs to register.".format(self), delete_after=5)

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


def setup(bot):
    bot.add_cog(Lobbies(bot))