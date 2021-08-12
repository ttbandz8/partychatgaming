from os import times
from time import time
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
from discord_slash import cog_ext, SlashContext

emojis = ['👍', '👎']

class Lobbies(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print('Lobbies Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @cog_ext.cog_slash(description="End your Crown PVP Match", guild_ids=main.guild_ids)
    async def end(self, ctx):
        session_query = {"OWNER": str(ctx.author), "AVAILABLE": True}
        session = db.querySession(session_query)

        if not session:
            await ctx.send(m.SESSION_DOES_NOT_EXIST)
            return

        teams = [x for x in session['TEAMS']]
        team_1 = teams[0]
        team_2 = teams[1]
        
        team_1_score = team_1['SCORE']
        team_2_score = team_2['SCORE']


        overall = team_1_score + team_2_score

        if len(teams) != 1:
            if overall == 0:
                end = db.endSession(session_query)
                await ctx.send(m.SESSION_NO_SCORE)
            else:
                if team_1_score == team_2_score:
                    end = db.endSession(session_query)
                    await ctx.send(m.SESSION_DRAW)
                else:
                    await self.sw(ctx)
                    await self.sl(ctx)
                    end = db.endSession(session_query)
                    await ctx.send(end)
        else:
            end = db.endSession(session_query)
            await ctx.send(m.SESSION_HAS_ENDED)

    async def sw(self, ctx):
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
        if session_data['GODS']:
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
            gods_player_team = player['TEAM']

            tourney_cards = db.queryTournamentCards()
            tourney_titles = db.queryTournamentTitles()

            types_of_matches_list = [x for x in player['MATCHES']]
            types_of_matches = dict(ChainMap(*types_of_matches_list))
            current_score = types_of_matches[game_type.upper()]
            query = {'DISNAME': player['DISNAME']}
            #uid = {'DID' : player['DID']}
            
            new_value = {}
            if session_data['TOURNAMENT']:
                new_value = {"$inc": {'TOURNAMENT_WINS': 1}}
                blessings = blessings + 100

            else:
                new_value = {"$inc": {'MATCHES.$[type].' + game_type.upper() + '.0': 1}}
                blessings = blessings + (.30*blessings)

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
            user = await self.bot.fetch_user(uid)
            await main.bless(blessings, player['DISNAME'])

            await main.DM(ctx, user, "You Won. Doesnt Prove Much Tho :yawning_face:")

            if winner_earned_tourney_cards or winner_earned_tourney_titles:
                await ctx.send(f"Competitor " + f"{user.mention}" + " earns a victory ! :100:")
                await ctx.send( f"{user.mention}" + "You have Unlocked New Items in your Vault! :eyes:")
            else:
                await ctx.send(f"Competitor " + f"{user.mention}" + " earns a victory ! :100:")

    async def sl(self, ctx):
        session_query = {"OWNER": str(ctx.author), "AVAILABLE": True}
        session_data = db.querySession(session_query)
        if session_data['KINGSGAMBIT']:
            return await ctx.send("Lobby has ended. See you for the next Kings Gambit!")
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
            
            players_team_name = ""
            update_query = {}
            add_score_to_team={}
            if session_data['GODS']:
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
                types_of_matches_list = [x for x in player['MATCHES']]
                types_of_matches = dict(ChainMap(*types_of_matches_list))
                current_score = types_of_matches[game_type.upper()]
                query = {'DISNAME': player['DISNAME']}
                
                new_value = {}
                if session_data['TOURNAMENT']:
                    new_value = {"$inc": {'TOURNAMENT_WINS': 0}}
                else:
                    new_value = {"$inc": {'MATCHES.$[type].' + game_type.upper() + '.1': 1}}

                filter_query = [{'type.' + game_type.upper(): current_score}]

                if session_data['TOURNAMENT']:
                    db.updateUserNoFilter(query, new_value)
                else:
                    db.updateUser(query, new_value, filter_query)

                uid = player['DID']
                user = await self.bot.fetch_user(uid)
                await main.curse(8, user)
                await main.DM(ctx, user, "You Lost. Get back in there!")
                await ctx.send(f"Competitor " + f"{user.mention}" + " took an L! :eyes:")

    @cog_ext.cog_slash(description="Setup PVP against player", guild_ids=main.guild_ids)
    async def battle(self, ctx, user1: User):
        game_name = "Crown Unlimited"
        query = {'ALIASES': game_name.lower()}
        game = db.queryGame(query)

        if game:
            name = game['GAME']
            user_query = {'DISNAME': str(ctx.author)}
            player2_query = {'DISNAME': str(user1)}
            player2=db.queryUser(player2_query)

            card1=player2['CARD']
            title1=player2['TITLE']
            arm1=player2['ARM']

            user = db.queryUser(user_query)
            card = user['CARD']
            title = user['TITLE']
            arm = user['ARM']
            if name in user['GAMES']:
                await main.DM(ctx, user1, f"{ctx.author.mention}" + f" has challenged you to {name}")
                accept = await ctx.send(f"{user1.mention} are you ready to battle {ctx.author.mention}? !!!:fire:")
                for emoji in emojis:
                    await accept.add_reaction(emoji)

                def check(reaction, user):
                    return user == user1 and str(reaction.emoji) == '👍'
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check)


                    join_query = {"TEAM": [str(user1)], "SCORE": 0, "CARD": card1, "TITLE": title1, "ARM": arm, "POSITION": 1}

                    session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 1, "TEAMS": [{"TEAM": [str(ctx.author)], "SCORE": 0, "CARD": card, "TITLE": title, "ARM": arm, "POSITION": 0}], "AVAILABLE": True}


                    session = db.createSession(data.newSession(session_query))
                    resp = db.joinSession(session_query, join_query)
                    await ctx.send(resp)
                    message = await ctx.send(f"{ctx.author.mention} use /start to start Ranked Match or Use /menu to view other PVP Modes!!!:fire:")

                except:
                    await ctx.send(m.ALREADY_IN_SESSION)  

            else:
                await ctx.send(m.ADD_A_GAME)
        else:
            await ctx.send(m.GAME_UNAVAILABLE)

    @cog_ext.cog_slash(description="Tutorial Battle: Normal Difficulty", guild_ids=main.guild_ids)
    async def senpaibattle(self, ctx):
        #game_name = " ".join([*args])
        query = {'ALIASES': 'crown'}
        game = db.queryGame(query)
        user1 = "SenpaiSays#3224"
        if game:
            name = game['GAME']
            user_query = {'DISNAME': str(ctx.author)}
            player2_query = {'DISNAME': user1}
            player2=db.queryUser(player2_query)

            card1=player2['CARD']
            title1=player2['TITLE']

            user = db.queryUser(user_query)
            card = user['CARD']
            title = user['TITLE']
            if name in user['GAMES']:
                #await main.DM(ctx, user1, f"{ctx.author.mention}" + f" has challenged you to {name}")
                await ctx.send(f"{ctx.author.mention} are you ready to battle? !!!:fire:")
                # for emoji in emojis:
                #     await accept.add_reaction(emoji)

                # def check(reaction, user):
                #     return user == user1 and str(reaction.emoji) == '👍'
                # try:
                #     reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)

                if name == 'Crown Unlimited':
                    join_query = {"TEAM": [str(user1)], "SCORE": 0, "CARD": card1, "TITLE": title1, "POSITION": 1}
                else:
                    join_query = {"TEAM": [str(user1)], "SCORE": 0, "POSITION": 1}

                if name == 'Crown Unlimited':
                    session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 1, "TEAMS": [{"TEAM": [str(ctx.author)], "SCORE": 0, "CARD": card, "TITLE": title, "POSITION": 0}], "AVAILABLE": True}
                else:
                    session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 1, "TEAMS": [{"TEAM": [str(ctx.author)], "SCORE": 0, "POSITION": 0}], "AVAILABLE": True}
                
                try:

                    session = db.createSession(data.newSession(session_query))
                    resp = db.joinSession(session_query, join_query)
                    await ctx.send(resp)
                    embedVar = discord.Embed(title=f"Use the .start command to start the tutorial match", colour=0xe91e63)
                    await ctx.send(embed=embedVar)

                except:
                    await ctx.send(m.ALREADY_IN_SESSION)   
                    return
            else:
                await ctx.send(m.ADD_A_GAME)
        else:
            await ctx.send(m.GAME_UNAVAILABLE)

    @cog_ext.cog_slash(description="Tutorial Battle: Hard Difficulty", guild_ids=main.guild_ids)
    async def legendbattle(self, ctx):
        #game_name = " ".join([*args])
        query = {'ALIASES': 'crown'}
        game = db.queryGame(query)
        user1 = "SenpaiLegend#9179"
        if game:
            name = game['GAME']
            user_query = {'DISNAME': str(ctx.author)}
            player2_query = {'DISNAME': user1}
            player2=db.queryUser(player2_query)

            card1=player2['CARD']
            title1=player2['TITLE']

            user = db.queryUser(user_query)
            card = user['CARD']
            title = user['TITLE']
            if name in user['GAMES']:
                #await main.DM(ctx, user1, f"{ctx.author.mention}" + f" has challenged you to {name}")
                await ctx.send(f"{ctx.author.mention} are you ready to battle? !!!:fire:")

                if name == 'Crown Unlimited':
                    join_query = {"TEAM": [str(user1)], "SCORE": 0, "CARD": card1, "TITLE": title1, "POSITION": 1}
                else:
                    join_query = {"TEAM": [str(user1)], "SCORE": 0, "POSITION": 1}

                if name == 'Crown Unlimited':
                    session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 1, "TEAMS": [{"TEAM": [str(ctx.author)], "SCORE": 0, "CARD": card, "TITLE": title, "POSITION": 0}], "AVAILABLE": True}
                else:
                    session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 1, "TEAMS": [{"TEAM": [str(ctx.author)], "SCORE": 0, "POSITION": 0}], "AVAILABLE": True}
                try:
                    session = db.createSession(data.newSession(session_query))
                    resp = db.joinSession(session_query, join_query)
                    await ctx.send(resp)
                    embedVar = discord.Embed(title=f"Use the .start command to start the tutorial match", colour=0xe91e63)
                    await ctx.send(embed=embedVar)

                except:
                    await ctx.send(m.ALREADY_IN_SESSION)   
                    return
            else:
                await ctx.send(m.ADD_A_GAME)
        else:
            await ctx.send(m.GAME_UNAVAILABLE)

def setup(bot):
    bot.add_cog(Lobbies(bot))


