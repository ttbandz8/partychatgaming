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

class Kingsgambit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Kings Gambit Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @commands.command()
    async def kg(self, ctx):
        if ctx.author.guild_permissions.administrator == True:
            game = [x for x in db.query_all_games()][0]
            session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 1, "TEAMS": [], "KINGSGAMBIT": True, "RANKED": True, "TOURNAMENT": True}
            resp = db.createSession(data.newSession(session_query))
            await ctx.send(resp)
            await ctx.send(f"{ctx.author.mention}" +" started a *Kings Gambit* :crown:")
        else:
            print(m.ADMIN_ONLY_COMMAND)

    @commands.command()
    async def jkg(self, ctx, user1: User):
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
                accept = await ctx.send(f"{user1.mention}, will you allow {ctx.author.mention} to join the Kings Gambit?", delete_after=10)
                for emoji in emojis:
                    await accept.add_reaction(emoji)

                def check(reaction, user):
                    return user == user1 and str(reaction.emoji) == '👍'

                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                    join_query = {"TEAM": [str(ctx.author)], "SCORE": 0, "POSITION": new_position}
                    session_joined = db.joinKingsGambit(session_query, join_query)
                    await ctx.send(session_joined)
                except:
                    await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=5)
            else:
                await ctx.send(m.ALREADY_IN_SESSION, delete_after=5)
        else:
            accept = await ctx.send(f"{ctx.author.mention}, Will you allow {user1.mention} to join the Kings Gambit?", delete_after=10)
            for emoji in emojis:
                await accept.add_reaction(emoji)

            def check(reaction, user):
                return user == user1 and str(reaction.emoji) == '👍'

            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=check)
                join_query = {"TEAM": [str(ctx.author)], "SCORE": 0, "POSITION": 0}
                session_joined = db.joinKingsGambit(session_query, join_query)
                await ctx.send(session_joined, delete_after=5)
            except:
                await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=5)


    @commands.command()
    async def kghelp(self, ctx):
        embedVar = discord.Embed(title=f"Kings Gambit: How To Register!", description="Party Chat Gaming Database™️", colour=000000)
        embedVar.add_field(name="REGISTRATION!" , value="Type::arrow_right: #r")
        embedVar.add_field(name="ADD CODM IGN!" , value="Type::arrow_right: #ag codm 'IGN'")
        embedVar.add_field(name="JOIN KINGS GAMBIT!" , value="Type::arrow_right: #jkg @streamer")
        embedVar.add_field(name="STREAMER LIST" , value="92Bricks, 𝖆𝖓𝖆𝖙𝖍𝖊𝖇𝖔𝖙シ\nDasinista, Dreamer\nEthwixs, Jah\nKiewiski, Liqxuds\nLust, Newlable\nNoobie, Roc.Bambino")
        embedVar.add_field(name="UPDATE IGN" , value="Type::arrow_right: #uign codm 'IGN'")
        embedVar.add_field(name="STILL LOST????" , value="use #help or ask a PCG Member for assistance")
        await ctx.send(embed=embedVar)

    @commands.command()
    async def skipkg(self, ctx, user: User):
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

    @commands.command()
    async def skg(self, ctx, user: User):
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
            await ctx.send(f"{user.mention}" +f" :heavy_plus_sign::one:")
        else:
            await ctx.send(f"Score not added. Please, try again. ", delete_after=5) 


def setup(bot):
    bot.add_cog(Kingsgambit(bot))