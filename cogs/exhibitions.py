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

class Exhibitions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print('Exhibitions Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @commands.command()
    async def e(self, ctx):
        if ctx.author.guild_permissions.administrator == True:
            game = [x for x in db.query_all_games()][0]
            session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 1, "TEAMS": [], "RANKED": True, "TOURNAMENT": True, }
            resp = db.createSession(data.newSession(session_query))
            await ctx.send(resp)
        else:
            await ctx.send(m.ADMIN_ONLY_COMMAND)

    @commands.command()
    async def einvite(self, ctx, user1: User):
        if ctx.author.guild_permissions.administrator == True:
            game = [x for x in db.query_all_games()][0]
            
            validate_opponent = db.queryUser({'DISNAME': str(user1)})

            if validate_opponent:
                await main.DM(ctx, user1, f"{ctx.author.mention}" + " has invited you to a Tournament Match :eyes:")
                accept = await ctx.send(f"{user1.mention}, Will you join the Exhibition? :fire:", delete_after=15)
                for emoji in emojis:
                    await accept.add_reaction(emoji)

                def check(reaction, user):
                    return user == user1 and str(reaction.emoji) == '👍'
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)

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


def setup(bot):
    bot.add_cog(Exhibitions(bot))