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
    async def cl(self, ctx, matchtype, *args):
        game_name = " ".join([*args])
        query = {'ALIASES': game_name.lower()}
        game = db.queryGame(query)
      
        if game:
            name = game['GAME']
            allowed_types = game['TYPE']

            user_query = {'DISNAME': str(ctx.author)}
            user = db.queryUser(user_query)
            if name in user['GAMES']:
                if int(matchtype) in allowed_types:
  
                    session_query = {"OWNER": str(ctx.author), "GAME": name, "TYPE": int(matchtype), "TEAMS": [], 'AVAILABLE': True}
                    resp = db.createSession(data.newSession(session_query))
                    await ctx.send(resp)
                else:
                    await ctx.send(m.GAME_TYPE_UNSUPPORTED)                    
            else:
                await ctx.send(m.ADD_A_GAME)
        else:
            await ctx.send(m.GAME_UNAVAILABLE)

    @commands.command()
    async def deletelobby(self, ctx):
        session_query = {"OWNER": str(ctx.author), "AVAILABLE": True}
        response = db.deleteSession(session_query)
        await ctx.send(response)

    @commands.command()
    async def el(self, ctx):
        session_query = {"OWNER": str(ctx.author), "AVAILABLE": True}
        session = db.querySession(session_query)
        teams = [x for x in session['TEAMS']]
        if len(teams) != 1:
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

    @commands.command()
    async def add(self, ctx, *user: User):
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
                if session['GAME'] not in resp['GAMES']:
                    await ctx.send(m.ADD_A_GAME)
                    return False
            
            if invalid_user:
                await ctx.send("You must first register before joining lobbies. ", delete_after=5)
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

    @commands.command()
    async def jl(self, ctx, *user: User):
        session_query = {"OWNER": str(user[0]), "AVAILABLE": True}
        session = db.querySession(session_query)
        if session:
            match_type = session['TYPE']
            game = session['GAME']
            user_query = ({'DISNAME': str(ctx.author)})
            response = db.queryUser(user_query)
            card = response['CARD']
            title = response['TITLE']
            if game not in response['GAMES']:
                await ctx.send(m.ADD_A_GAME)
            else:
                invalid_user = False
                for u in user:
                    user_query = ({'DISNAME': str(u)})
                    resp = db.queryUser(user_query)
                    if not resp:
                        invalid_user = True
                        await ctx.send(m.USER_NOT_REGISTERED)
                    if game not in resp['GAMES']:
                        invalid_user = True
                        await ctx.send(m.ADD_A_GAME)
            
                if invalid_user:
                    await ctx.send(m.USER_NOT_REGISTERED, delete_after=5)
                else:
                    position=0
                    if bool(session['TEAMS']):
                        position=1
                    if match_type == 1 and game == 'Crown Unlimited':
                        join_query = {"TEAM": [str(ctx.author)], "SCORE": 0, "CARD": card, "TITLE": title, "POSITION": position}
                        session_joined = db.joinSession(session_query, join_query)
                        await ctx.send(session_joined)
                    if match_type == 1 and game != 'Crown Unlimited':
                        join_query = {"TEAM": [str(ctx.author)], "SCORE": 0, "POSITION": position}
                        session_joined = db.joinSession(session_query, join_query)
                        await ctx.send(session_joined)
                    if match_type == 2:
                        join_query = {"TEAM": [str(ctx.author), (str(user[1]))], "SCORE": 0, "POSITION": position}
                        session_joined = db.joinSession(session_query, join_query)
                        await ctx.send(session_joined)
                    if match_type == 3:
                        join_query = {"TEAM": [str(ctx.author), (str(user[1])), str(user[2])], "SCORE": 0, "POSITION": position}
                        session_joined = db.joinSession(session_query, join_query)
                        await ctx.send(session_joined)
                    if match_type ==4:
                        join_query = {"TEAM": [str(ctx.author), (str(user[1])), str(user[2]), str(user[3])], "SCORE": 0, "POSITION": position}
                        session_joined = db.joinSession(session_query, join_query)
                        await ctx.send(session_joined)
                    if match_type ==5:
                        join_query = {"TEAM": [str(ctx.author), (str(user[1])), str(user[2]), str(user[3]), str(user[4])], "SCORE": 0, "POSITION": position}
                        session_joined = db.joinSession(session_query, join_query)
                        await ctx.send(session_joined)
                    if match_type >5:
                        await ctx.send(m.TOO_MANY_PLAYERS_ON_TEAM)                     

        else:
            await ctx.send(m.SESSION_DOES_NOT_EXIST)

    @commands.command()
    async def score(self,ctx, user: User):
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
        await main.DM(ctx, user, message)
        if response:
            await ctx.send(f"{user.mention}" +f" + :one:", delete_after=2)
        else:
            await ctx.send(f"Score not added. Please, try again. ", delete_after=5)

    # @commands.command()
    # async def cards(self,ctx, user: User):
    #     print(ctx.author[])
    #     await self.cl(self,ctx,1,"Flex")
    #     await self.jl(self,ctx,ctx.author)
    #     await self.add(self,ctx,user)





def setup(bot):
    bot.add_cog(Lobbies(bot))

    # @commands.command()
    # async def challenge(self, ctx, user1: User):
    #     game = [x for x in db.query_all_games()][0]
        
    #     validate_opponent = db.queryUser({'DISNAME': str(user1)})

    #     if validate_opponent:
    #         await main.DM(ctx, user1, f"{ctx.author.mention}" + " has challeneged you... :eyes:")
    #         accept = await ctx.send(f"{user1.mention}, Will you join the lobby? :fire:", delete_after=15)
    #         for emoji in emojis:
    #             await accept.add_reaction(emoji)

    #         def check(reaction, user):
    #             return user == user1 and str(reaction.emoji) == '👍'
    #         try:
    #             reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
    #             join_query = {"TEAM": [str(user1)], "SCORE": 0, "POSITION": 1}

    #             session_query = {"OWNER": str(ctx.author), "GAME": game["GAME"], "TYPE": 1, "TEAMS": [{"TEAM": [str(ctx.author)], "SCORE": 0, "POSITION": 0}], "AVAILABLE": True}
    #             session = db.createSession(data.newSession(session_query))
    #             resp = db.joinSession(session_query, join_query)
    #             await ctx.send(resp)
    #         except:
    #             await ctx.send(m.INVITE_NOT_ACCEPTED, delete_after=3)
    #     else:
    #         await ctx.send(m.USER_NOT_REGISTERED, delete_after=5)


# ''' Delete All Sessions '''
# @bot.command()
# @commands.check(validate_user)
# async def dal(ctx):
#    user_query = {"DISNAME": str(ctx.author)}
#    if ctx.author.guild_permissions.administrator == True:
#       resp = db.deleteAllSessions(user_query)
#       await ctx.send(resp)
#    else:
#       await ctx.send(m.ADMIN_ONLY_COMMAND)