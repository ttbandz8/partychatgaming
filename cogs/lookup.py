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

class Lookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print('Lookup Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @commands.command()
    async def owner(self, ctx, user: User):
        session_owner = {'OWNER': str(user), "AVAILABLE": True}
        session = db.querySession(session_owner)
        if session:
            game_query = {'ALIASES': session['GAME'].lower()}
            game = db.queryGame(game_query)

            name = session['OWNER'].split("#",1)[0]
            games = game['GAME']
            avatar = game['IMAGE_URL']
            owner = session['OWNER']
            tournament = session['TOURNAMENT']
            scrim = session['SCRIM']
            kingsgambit = session['KINGSGAMBIT']
            gods = session['GODS']
            godsname = session['GODS_TITLE']
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

            teams = [x for x in session['TEAMS']]
            
            team_list = []
            team_1 = [x for x in teams if x['POSITION'] == 0] # position 0
            team_2 = [x for x in teams if x['POSITION'] == 1] # position 1
            other_teams = [x for x in teams if x['POSITION'] > 1] # position 1

            team_1_comp_with_ign = []
            team_2_comp_with_ign = []

            team_1_score = ""
            team_2_score = ""

            king_score = 0

            other_teams_comp = []

            for x in team_1:
                # n = x['TEAM'].split("#",1)[1]
                team_1_score = f" Score: {x['SCORE']}"
                king_score = x['SCORE']
                for y in x['TEAM']:
                    data = db.queryUser({'DISNAME': y})
                    ign = ""
                    for z in data['IGN']:
                        if games in z:
                            ign = z[games]
                            team_1_comp_with_ign.append(f"{data['DISNAME']} : 🎮 {ign}".format(self))
                if not team_1_comp_with_ign:
                    team_1_comp_with_ign.append(f"{data['DISNAME']}")



            
            for x in team_2:
                team_2_score = f" Score: {x['SCORE']}"

                for y in x['TEAM']:
                    data = db.queryUser({'DISNAME': y})
                    ign = ""
                    for z in data['IGN']:
                        if games in z:
                            ign = z[games]
                            team_2_comp_with_ign.append(f"{data['DISNAME']} : 🎮 {ign}".format(self))
                if not team_2_comp_with_ign:
                    team_2_comp_with_ign.append(f"{data['DISNAME']}")

            if kingsgambit:
                for x in other_teams:
                    p = x['POSITION']
                    for a in x['TEAM']:
                        other_teams_comp.append({a:p})

            other_teams_comp_to_str = dict(ChainMap(*other_teams_comp))
            n = dict(sorted(other_teams_comp_to_str.items(), key=lambda item: item[1]))
            other_teams_sorted_list = "\n".join(f'{k}' for k,v in n.items())

            team1="Team 1"
            team2="Team 2"

            if games == "Crown Unlimited":
                if team_1:
                    team1=team_1[0]['CARD']
                if team_2:
                    team2=team_2[0]['CARD']

            if gods:
                embedVar = discord.Embed(title=f":trophy: {godsname} Lobby: {game_type} ".format(self), description=f"{user.mention} owns this lobby.\n" + "Compete in PCGs Grand Tournament to determine the one true God of the game!", colour=000000)
            elif kingsgambit:
                embedVar = discord.Embed(title=f":crown: [Kings Gambit]\n{games} Lobby: {game_type} ".format(self), description=f"{user.mention} owns this lobby.\n" + "Compete in 1v1 matches where the winner stays on to determine the king of the game!", colour=000000)            
            else:
                embedVar = discord.Embed(title=f"{games} Lobby: {game_type} ".format(self), description=f"{user.mention} owns this lobby", colour=000000)            
            embedVar.set_image(url=avatar)
            
            if scrim:
                embedVar.add_field(name="Scrim", value="Yes")
            
            if kingsgambit and king_score > 0:
                embedVar.add_field(name=f":crown:King - {team_1_score}", value="\n".join(team_1_comp_with_ign))
            elif not team_1_score:
                embedVar.add_field(name=f":military_helmet:{team1}", value="Vacant")
            else:
                embedVar.add_field(name=f":military_helmet:{team1} - {team_1_score}", value="\n".join(team_1_comp_with_ign))
            
            if team_2_comp_with_ign:
                embedVar.add_field(name=f":military_helmet:{team2} - {team_2_score}", value="\n".join(team_2_comp_with_ign))
            else:
                embedVar.add_field(name=f":military_helmet:{team2}", value="Vacant")

            if kingsgambit and other_teams:
                embedVar.add_field(name=f"Up Next...", value=other_teams_sorted_list)

            await ctx.send(embed=embedVar)
        else:
            await ctx.send(m.SESSION_DOES_NOT_EXIST, delete_after=5)

    @commands.command()
    async def ml(self, ctx):  
        session_owner = {'OWNER': str(ctx.author), "AVAILABLE": True}
        session = db.querySession(session_owner)

        if session:
            game_query = {'ALIASES': session['GAME'].lower()}
            game = db.queryGame(game_query)
            tournament = session['TOURNAMENT']
            kingsgambit = session['KINGSGAMBIT']
            scrim = session['SCRIM']
            name = session['OWNER'].split("#",1)[0]
            games = game['GAME']
            avatar = game['IMAGE_URL']
            gods = session['GODS']
            godsname = session['GODS_TITLE']
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

            teams = [x for x in session['TEAMS']]
            
            team_list = []
            team_1 = [x for x in teams if x['POSITION'] == 0] # position 0
            team_2 = [x for x in teams if x['POSITION'] == 1] # position 1
            other_teams = [x for x in teams if x['POSITION'] > 1]



            team_1_comp_with_ign = []
            team_2_comp_with_ign = []

            team_1_score = ""
            team_2_score = ""

            king_score = 0

            other_teams_comp = []
            king_in_the_lead = []
            for x in team_1:
                team_1_score = f" Score: {x['SCORE']}"
                king_score = x['SCORE']
                for y in x['TEAM']:
                    data = db.queryUser({'DISNAME': y})
                    ign = ""
                    for z in data['IGN']:
                        if games in z:
                            ign = z[games]
                            team_1_comp_with_ign.append(f"{data['DISNAME']} : 🎮 {ign}".format(self))
                if not team_1_comp_with_ign:
                    team_1_comp_with_ign.append(f"{data['DISNAME']}")



            
            for x in team_2:
                team_2_score = f" Score: {x['SCORE']}"

                for y in x['TEAM']:
                    data = db.queryUser({'DISNAME': y})
                    ign = ""
                    for z in data['IGN']:
                        if games in z:
                            ign = z[games]
                            team_2_comp_with_ign.append(f"{data['DISNAME']} : 🎮 {ign}".format(self))
                if not team_2_comp_with_ign:
                    team_2_comp_with_ign.append(f"{data['DISNAME']}")

            if kingsgambit:
                for x in other_teams:
                    p = x['POSITION']
                    for a in x['TEAM']:
                        other_teams_comp.append({a:p})
            
            in_the_lead = {}
            if kingsgambit:
                scores = []
                lead_scores = [x for x in teams if x['SCORE'] > 0]
                for x in teams:
                    scores.append(x['SCORE'])
                
                for x in lead_scores:
                    if x['SCORE'] == max(scores):
                        in_the_lead = {x['TEAM'][0]:x['SCORE']}
            lead_player = "".join([*in_the_lead])
            lead_score = "".join([str(*in_the_lead.values())])

            other_teams_comp_to_str = dict(ChainMap(*other_teams_comp))
            n = dict(sorted(other_teams_comp_to_str.items(), key=lambda item: item[1]))
            other_teams_sorted_list = "\n".join(f'{k}' for k,v in n.items())

            team1="Team 1"
            team2="Team 2"

            if games == "Crown Unlimited":

                if team_1:
                    team1=team_1[0]['CARD']
                if team_2:
                    team2=team_2[0]['CARD']

            if gods:
                embedVar = discord.Embed(title=f":trophy: {godsname} Lobby: {game_type} ".format(self), description=f"{ctx.author.mention} owns this lobby.\n" + "Compete in PCGs Grand Tournament to determine the one true God of the game!", colour=000000)
            if kingsgambit:
                embedVar = discord.Embed(title=f":crown: [Kings Gambit]\n{games} Lobby: {game_type} ".format(self), description=f"{ctx.author.mention} owns this lobby.\n" + "Compete in 1v1 matches where the winner stays on to determine the king of the game!", colour=000000)
            if king_score > 0:
                embedVar = discord.Embed(title=f":crown: [Kings Gambit]\n:100: {lead_player} Is in the lead with {lead_score} points!".format(self), description=f"{ctx.author.mention} owns this lobby.\n" + "Compete in 1v1 matches where the winner stays on to determine the king of the game!", colour=000000)
            if not gods and not kingsgambit:
                embedVar = discord.Embed(title=f"{games} Lobby: {game_type} ".format(self), description=f"{ctx.author.mention} owns this lobby", colour=000000)
            embedVar.set_image(url=avatar)

            if scrim:
                embedVar.add_field(name="Scrim", value="Yes")
            
            if kingsgambit and king_score > 0:
                embedVar.add_field(name=f":crown: King - {team_1_score}", value="\n".join(team_1_comp_with_ign))
            elif not team_1_score:
                embedVar.add_field(name=f":military_helmet:{team1}", value="Vacant")
            else:
                embedVar.add_field(name=f":military_helmet:{team1} - {team_1_score}", value="\n".join(team_1_comp_with_ign))

            if team_2_comp_with_ign:
                embedVar.add_field(name=f":military_helmet:{team2} - {team_2_score}", value="\n".join(team_2_comp_with_ign))
            else:
                embedVar.add_field(name=f":military_helmet:{team2}", value="Vacant")

            if kingsgambit and other_teams:
                embedVar.add_field(name=f"Up Next...", value=other_teams_sorted_list, inline=False)

            await ctx.send(embed=embedVar)
        else:
            await ctx.send(m.SESSION_DOES_NOT_EXIST, delete_after=5)

    @commands.command()
    async def check(self, ctx, user: User):
        current_session = {'TEAMS.TEAM': str(user), "AVAILABLE": True}
        session = db.querySessionMembers(current_session)
        if session:
            game_query = {'ALIASES': session['GAME'].lower()}
            game = db.queryGame(game_query)

            name = session['OWNER'].split("#",1)[0]
            games = game['GAME']
            avatar = game['IMAGE_URL']
            tournament = session['TOURNAMENT']
            owner = session['OWNER']
            scrim = session['SCRIM']
            kingsgambit = session['KINGSGAMBIT']
            gods = session['GODS']
            godsname = session['GODS_TITLE']
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

            owner_query = db.queryUser({'DISNAME': owner})
            lobby_owner = await self.bot.fetch_user(owner_query['DID'])

            teams = [x for x in session['TEAMS']]
            
            team_list = []
            team_1 = [x for x in teams if x['POSITION'] == 0] # position 0
            team_2 = [x for x in teams if x['POSITION'] == 1] # position 1
            other_teams = [x for x in teams if x['POSITION'] > 1] # position 1




            team_1_comp_with_ign = []
            team_2_comp_with_ign = []

            team_1_score = ""
            team_2_score = ""

            king_score = 0

            other_teams_comp = []

            for x in team_1:
                # n = x['TEAM'].split("#",1)[1]
                team_1_score = f" Score: {x['SCORE']}"
                king_score = x['SCORE']
                for y in x['TEAM']:
                    data = db.queryUser({'DISNAME': y})
                    ign = ""
                    for z in data['IGN']:
                        if games in z:
                            ign = z[games]
                            team_1_comp_with_ign.append(f"{data['DISNAME']} : 🎮 {ign}".format(self))
                if not team_1_comp_with_ign:
                    team_1_comp_with_ign.append(f"{data['DISNAME']}")



            
            for x in team_2:
                team_2_score = f" Score: {x['SCORE']}"

                for y in x['TEAM']:
                    data = db.queryUser({'DISNAME': y})
                    ign = ""
                    for z in data['IGN']:
                        if games in z:
                            ign = z[games]
                            team_2_comp_with_ign.append(f"{data['DISNAME']} : 🎮 {ign}".format(self))
                if not team_2_comp_with_ign:
                    team_2_comp_with_ign.append(f"{data['DISNAME']}")   


            if kingsgambit:
                for x in other_teams:
                    p = x['POSITION']
                    for a in x['TEAM']:
                     other_teams_comp.append({a:p})

            other_teams_comp_to_str = dict(ChainMap(*other_teams_comp))
            n = dict(sorted(other_teams_comp_to_str.items(), key=lambda item: item[1]))
            other_teams_sorted_list = "\n".join(f'{k}' for k,v in n.items())

            team1="Team 1"
            team2="Team 2"

            if games == "Crown Unlimited":
                if team_1:
                    team1=team_1[0]['CARD']
                if team_2:
                    team2=team_2[0]['CARD']

            if gods:
                embedVar = discord.Embed(title=f":trophy: {godsname} Lobby: {game_type} ".format(self), description=f"{lobby_owner.mention} owns this lobby.\n" + "Compete in PCGs Grand Tournament to determine the one true God of the game!", colour=000000)
            elif kingsgambit:
                embedVar = discord.Embed(title=f":crown: [Kings Gambit]\n{games} Lobby: {game_type} ".format(self), description=f"{lobby_owner.mention} owns this lobby.\n" + "Compete in 1v1 matches where the winner stays on to determine the king of the game!", colour=000000)
            else:
                embedVar = discord.Embed(title=f"{games} Lobby: {game_type} ".format(self), description=f"{lobby_owner.mention} owns this lobby", colour=000000)            
            embedVar.set_image(url=avatar)

            if scrim:
                embedVar.add_field(name="Scrim", value="Yes")
            
            if kingsgambit and king_score > 0:
                embedVar.add_field(name=f":crown:King - {team_1_score}", value="\n".join(team_1_comp_with_ign))
            elif not team_1_score:
                embedVar.add_field(name=f":military_helmet:{team1}", value="Vacant", inline=False)
            else:
                embedVar.add_field(name=f":military_helmet:{team1} - {team_1_score}", value="\n".join(team_1_comp_with_ign))
            
            if team_2_comp_with_ign:
                embedVar.add_field(name=f":military_helmet:{team2} - {team_2_score}", value="\n".join(team_2_comp_with_ign))
            else:
                embedVar.add_field(name=f":military_helmet:{team2}", value="Vacant")

            if kingsgambit and other_teams:
                embedVar.add_field(name=f"Up Next...", value=other_teams_sorted_list)

            await ctx.send(embed=embedVar)
        else:
            await ctx.send(m.SESSION_DOES_NOT_EXIST, delete_after=5)

    @commands.command()
    async def lk(self, ctx, user: User):
        query = {'DISNAME': str(user)}
        d = db.queryUser(query)

        if d:
            name = d['DISNAME'].split("#",1)[0]
            games = d['GAMES']
            ign = d['IGN']
            team = d['TEAM']
            titles = d['TITLE']
            avatar = d['AVATAR']
            matches = d['MATCHES']
            tournament_wins = d['TOURNAMENT_WINS']


            matches_to_string = dict(ChainMap(*matches))
            ign_to_string = dict(ChainMap(*ign))
            embed1 = discord.Embed(title= f":triangular_flag_on_post: " + f"{name}".format(self), description=":bank: Party Chat Gaming Database™️", colour=000000)
            embed1.set_thumbnail(url=avatar)
            embed1.add_field(name="Team" + " :military_helmet:", value=team)
            embed1.add_field(name="Title" + " :crown:", value=' '.join(str(x) for x in titles))
            embed1.add_field(name="Tournament Wins" + " :fireworks:", value=tournament_wins)

            embed2 = discord.Embed(title= f":triangular_flag_on_post: " + f"{name}".format(self), description=":bank: Party Chat Gaming Database™️", colour=000000)
            embed2.set_thumbnail(url=avatar)
            embed2.add_field(name="Game" + " :video_game:" , value='\n'.join(games))
            embed2.add_field(name="In-Game Name" + " :selfie:", value="\n".join(f'{k}: :video_game: {v}' for k,v in ign_to_string.items()), inline=False)

            embed3 = discord.Embed(title= f":triangular_flag_on_post: " + f"{name}".format(self), description=":bank: Party Chat Gaming Database™️", colour=000000)
            embed3.set_thumbnail(url=avatar)
            embed3.add_field(name="Stats" + " :medal:", value="\n".join(f'{k}: {"/".join([str(int) for int in v])}' for k,v in matches_to_string.items()))

            paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
            paginator.add_reaction('⏮️', "first")
            paginator.add_reaction('⏪', "back")
            paginator.add_reaction('🔐', "lock")
            paginator.add_reaction('⏩', "next")
            paginator.add_reaction('⏭️', "last")
            embeds = [embed1, embed2, embed3]
            await paginator.run(embeds)
        else:
            await ctx.send(m.USER_NOT_REGISTERED)

    @commands.command()
    async def lkt(self, ctx, *args):
        team_name = " ".join([*args])
        team_query = {'TNAME': team_name}
        team = db.queryTeam(team_query)
        owner_name = ""
        if team:
            team_name = team['TNAME']
            owner_name = team['OWNER']
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


            embed1 = discord.Embed(title=f":checkered_flag: {team_name} Team Card".format(self), description=":bank: Party Chat Gaming Database", colour=000000)
            if team['LOGO_FLAG']:
                embed1.set_image(url=logo)
            embed1.add_field(name="Owner :man_detective:", value= owner_name.split("#",1)[0], inline=False)
            embed1.add_field(name="Scrim Wins :medal:", value=scrim_wins)
            embed1.add_field(name="Scrim Losses :crossed_swords:", value=scrim_losses)
            embed1.add_field(name="Tournament Wins :fireworks:", value=tournament_wins, inline=False)
            
            embed2 = discord.Embed(title=f":checkered_flag: {team_name} Team Members".format(self), description=":bank: Party Chat Gaming Database", colour=000000)
            if team['LOGO_FLAG']:
                embed2.set_image(url=logo)
            embed2.add_field(name="Members :military_helmet:", value="\n".join(f'{t}'.format(self) for t in team_list), inline=False)

            embed3 = discord.Embed(title=f":checkered_flag: {team_name} Team Members".format(self), description=":bank: Party Chat Gaming Database", colour=000000)
            if team['LOGO_FLAG']:
                embed3.set_image(url=logo)
            embed3.add_field(name="Games :video_game:", value="\n".join(games), inline=False)
            paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
            paginator.add_reaction('⏮️', "first")
            paginator.add_reaction('⏪', "back")
            paginator.add_reaction('🔐', "lock")
            paginator.add_reaction('⏩', "next")
            paginator.add_reaction('⏭️', "last")
            embeds = [embed1, embed2, embed3]
            await paginator.run(embeds)
        else:
            await ctx.send(m.TEAM_DOESNT_EXIST)


def setup(bot):
    bot.add_cog(Lookup(bot))