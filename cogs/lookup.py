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
    async def lo(self, ctx, user: User):
        session_owner = {'OWNER': str(user), "AVAILABLE": True}
        session = db.querySession(session_owner)
        if session:
            game_query = {'ALIASES': session['GAME']}
            game = db.queryGame(game_query)

            name = session['OWNER'].split("#",1)[0]
            games = game['GAME']
            avatar = game['IMAGE_URL']
            tournament = session['TOURNAMENT']
            scrim = session['SCRIM']
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
                        else:
                            team_1_comp_with_ign.append(f"{data['DISNAME']}")
                team_1_comp = "\n".join(x['TEAM'])



            
            for x in team_2:
                team_2_score = f" Score: {x['SCORE']}"

                for y in x['TEAM']:
                    data = db.queryUser({'DISNAME': y})
                    ign = ""
                    for z in data['IGN']:
                        if games in z:
                            ign = z[games]
                            team_2_comp_with_ign.append(f"{data['DISNAME']} : 🎮 {ign}".format(self))
                        else:
                            team_2_comp_with_ign.append(f"{data['DISNAME']}")


            if kingsgambit:
                for x in other_teams:
                    p = x['POSITION']
                    for a in x['TEAM']:
                        other_teams_comp.append({a:p})

            other_teams_comp_to_str = dict(ChainMap(*other_teams_comp))
            n = dict(sorted(other_teams_comp_to_str.items(), key=lambda item: item[1]))
            other_teams_sorted_list = "\n".join(f'{k}' for k,v in n.items())

            embedVar = discord.Embed(title=f"{name}'s {games} Session ".format(self), description="Party Chat Gaming Database", colour=000000)
            embedVar.set_thumbnail(url=avatar)
            embedVar.add_field(name="Match ", value=f'{game_type}'.format(self))
            embedVar.add_field(name="Type: " + stype , value=f'{ranked}'.format(self))
            if tournament:
                embedVar.add_field(name="Tournament", value="Yes")
            
            if kingsgambit:
                embedVar.add_field(name="Kings Gambit", value="Yes")

            if scrim:
                embedVar.add_field(name="Scrim", value="Yes")
            
            if goc:
                embedVar.add_field(name="GODS OF COD : " + f"{gocname}", value="Yes")
            
            if kingsgambit and king_score > 0:
                embedVar.add_field(name=f":crown:King - {team_1_score}", value="\n".join(team_1_comp_with_ign), inline=False)
            elif not team_1_score:
                embedVar.add_field(name=f":military_helmet:Team 1", value="Vacant", inline=False)
            else:
                embedVar.add_field(name=f":military_helmet:Team 1 - {team_1_score}", value="\n".join(team_1_comp_with_ign), inline=False)
            
            if team_2_comp_with_ign:
                embedVar.add_field(name=f":military_helmet:Team 2 - {team_2_score}", value="\n".join(team_2_comp_with_ign), inline=False)
            else:
                embedVar.add_field(name=f":military_helmet:Team 2", value="Vacant", inline=False)

            if kingsgambit and other_teams:
                embedVar.add_field(name=f"Up Next...", value=other_teams_sorted_list, inline=False)

            await ctx.send(embed=embedVar)
        else:
            await ctx.send(m.SESSION_DOES_NOT_EXIST, delete_after=5)

    @commands.command()
    async def ml(self, ctx):  
        session_owner = {'OWNER': str(ctx.author), "AVAILABLE": True}
        session = db.querySession(session_owner)

        if session:
            game_query = {'ALIASES': session['GAME']}
            game = db.queryGame(game_query)
            tournament = session['TOURNAMENT']
            kingsgambit = session['KINGSGAMBIT']
            scrim = session['SCRIM']
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
                    else:
                        team_1_comp_with_ign.append(f"{data['DISNAME']}")
                team_1_comp = "\n".join(x['TEAM'])



            
            for x in team_2:
                team_2_score = f" Score: {x['SCORE']}"

                for y in x['TEAM']:
                    data = db.queryUser({'DISNAME': y})
                    ign = ""
                    for z in data['IGN']:
                        if games in z:
                            ign = z[games]
                            team_2_comp_with_ign.append(f"{data['DISNAME']} : 🎮 {ign}".format(self))
                    else:
                        team_2_comp_with_ign.append(f"{data['DISNAME']}")


            if kingsgambit:
                for x in other_teams:
                    p = x['POSITION']
                    for a in x['TEAM']:
                        other_teams_comp.append({a:p})

            other_teams_comp_to_str = dict(ChainMap(*other_teams_comp))
            n = dict(sorted(other_teams_comp_to_str.items(), key=lambda item: item[1]))
            other_teams_sorted_list = "\n".join(f'{k}' for k,v in n.items())

            embedVar = discord.Embed(title=f"{name}'s {games} Session ".format(self), description="Party Chat Gaming Database", colour=000000)
            embedVar.set_thumbnail(url=avatar)
            embedVar.add_field(name="Match ", value=f'{game_type}'.format(self))
            embedVar.add_field(name="Type: " + stype , value=f'{ranked}'.format(self))
            if tournament:
                embedVar.add_field(name="Tournament", value="Yes")
            
            if kingsgambit:
                embedVar.add_field(name="Kings Gambit", value="Yes")

            if scrim:
                embedVar.add_field(name="Scrim", value="Yes")

            if goc:
                embedVar.add_field(name="GODS OF COD : " + f"{gocname}", value="Yes")
            
            if kingsgambit and king_score > 0:
                embedVar.add_field(name=f":crown:King - {team_1_score}", value="\n".join(team_1_comp_with_ign), inline=False)
            elif not team_1_score:
                embedVar.add_field(name=f":military_helmet:Team 1", value="Vacant", inline=False)
            else:
                embedVar.add_field(name=f":military_helmet:Team 1 - {team_1_score}", value="\n".join(team_1_comp_with_ign), inline=False)
            
            if team_2_comp_with_ign:
                embedVar.add_field(name=f":military_helmet:Team 2 - {team_2_score}", value="\n".join(team_2_comp_with_ign), inline=False)
            else:
                embedVar.add_field(name=f":military_helmet:Team 2", value="Vacant", inline=False)

            if kingsgambit and other_teams:
                embedVar.add_field(name=f"Up Next...", value=other_teams_sorted_list, inline=False)

            await ctx.send(embed=embedVar)
        else:
            await ctx.send(m.SESSION_DOES_NOT_EXIST, delete_after=5)

    @commands.command()
    async def cl(self, ctx, user: User):
        current_session = {'TEAMS.TEAM': str(user), "AVAILABLE": True}
        session = db.querySessionMembers(current_session)
        if session:
            game_query = {'ALIASES': session['GAME']}
            game = db.queryGame(game_query)

            name = session['OWNER'].split("#",1)[0]
            games = game['GAME']
            avatar = game['IMAGE_URL']
            tournament = session['TOURNAMENT']
            
            scrim = session['SCRIM']
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
                    else:
                        team_1_comp_with_ign.append(f"{data['DISNAME']}")
                team_1_comp = "\n".join(x['TEAM'])



            
            for x in team_2:
                team_2_score = f" Score: {x['SCORE']}"

                for y in x['TEAM']:
                    data = db.queryUser({'DISNAME': y})
                    ign = ""
                    for z in data['IGN']:
                        if games in z:
                            ign = z[games]
                            team_2_comp_with_ign.append(f"{data['DISNAME']} : 🎮 {ign}".format(self))
                    else:
                        team_2_comp_with_ign.append(f"{data['DISNAME']}")


            if kingsgambit:
                for x in other_teams:
                    p = x['POSITION']
                    for a in x['TEAM']:
                     other_teams_comp.append({a:p})

            other_teams_comp_to_str = dict(ChainMap(*other_teams_comp))
            n = dict(sorted(other_teams_comp_to_str.items(), key=lambda item: item[1]))
            other_teams_sorted_list = "\n".join(f'{k}' for k,v in n.items())

            embedVar = discord.Embed(title=f"{name}'s {games} Lobby ".format(self), description="Party Chat Gaming Database", colour=000000)
            embedVar.set_thumbnail(url=avatar)
            embedVar.add_field(name="Match ", value=f'{game_type}'.format(self))
            embedVar.add_field(name="Type: " + stype , value=f'{ranked}'.format(self))
            if tournament:
                embedVar.add_field(name="Tournament", value="Yes")
            
            if kingsgambit:
                embedVar.add_field(name="Kings Gambit", value="Yes")

            if scrim:
                embedVar.add_field(name="Scrim", value="Yes")
            if goc:
                embedVar.add_field(name="GODS OF COD : " + f"{gocname}", value="Yes")
            
            if kingsgambit and king_score > 0:
                embedVar.add_field(name=f":crown:King - {team_1_score}", value="\n".join(team_1_comp_with_ign), inline=False)
            elif not team_1_score:
                embedVar.add_field(name=f":military_helmet:Team 1", value="Vacant", inline=False)
            else:
                embedVar.add_field(name=f":military_helmet:Team 1 - {team_1_score}", value="\n".join(team_1_comp_with_ign), inline=False)
            
            if team_2_comp_with_ign:
                embedVar.add_field(name=f":military_helmet:Team 2 - {team_2_score}", value="\n".join(team_2_comp_with_ign), inline=False)
            else:
                embedVar.add_field(name=f":military_helmet:Team 2", value="Vacant", inline=False)

            if kingsgambit and other_teams:
                embedVar.add_field(name=f"Up Next...", value=other_teams_sorted_list, inline=False)

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
            ranked = d['RANKED']
            normal = d['NORMAL']
            tournament_wins = d['TOURNAMENT_WINS']


            ranked_to_string = dict(ChainMap(*ranked))
            normal_to_string = dict(ChainMap(*normal))
            ign_to_string = dict(ChainMap(*ign))

            embedVar = discord.Embed(title= f":triangular_flag_on_post: " + f"{name}".format(self), description=":bank: Party Chat Gaming Database™️", colour=000000)
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

def setup(bot):
    bot.add_cog(Lookup(bot))