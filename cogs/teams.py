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

class Teams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Teams Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @commands.command()
    async def cteam(self, ctx, args1, *args):
        game_query = {'ALIASES': args1}
        game = db.queryGame(game_query)['GAME']
        team_name = " ".join([*args])
        team_query = {'OWNER': str(ctx.author), 'TNAME': team_name, 'MEMBERS': [str(ctx.author)], 'GAMES': [game]}
        accept = await ctx.send(f"Do you want to create the {game} team {team_name}?".format(self), delete_after=10)
        for emoji in emojis:
            await accept.add_reaction(emoji)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '👍'

        try:
            confirmed = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
            response = db.createTeam(data.newTeam(team_query), str(ctx.author))
            await ctx.send(response)
        except:
            print("Team not created. ")

    @commands.command()
    async def att(self, ctx, user1: User):
        owner_profile = db.queryUser({'DISNAME': str(ctx.author)})
        team_profile = db.queryTeam({'TNAME': owner_profile['TEAM']})

        if owner_profile['TEAM'] == 'PCG':
            await ctx.send(m.USER_NOT_ON_TEAM, delete_after=5)
        else:

            if owner_profile['DISNAME'] == team_profile['OWNER']:

                member_profile = db.queryUser({'DISNAME': str(user1)})
                # If user is part of a team you cannot add them to your team
                if member_profile['TEAM'] == 'PCG':
                    await main.DM(ctx, user1, f"{ctx.author.mention}" + f" has invited you to join {team_profile['TNAME']} !" + f" React in server to join {team_profile['TNAME']}" )
                    accept = await ctx.send(f"{user1.mention}" +f" do you want to join team {team_profile['TNAME']}?".format(self), delete_after=10)
                    for emoji in emojis:
                        await accept.add_reaction(emoji)

                    def check(reaction, user):
                        return user == user1 and str(reaction.emoji) == '👍'

                    try:
                        confirmed = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                        team_query = {'TNAME': team_profile['TNAME']}
                        new_value_query = {'$push': {'MEMBERS': str(user1)}}
                        response = db.addTeamMember(team_query, new_value_query, str(ctx.author), str(user1))
                        await ctx.send(response)
                    except:
                        await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=3)
                else:
                    await ctx.send(m.USER_ALREADY_ON_TEAM, delete_after=5)

            else:
                await ctx.send(m.OWNER_ONLY_COMMAND, delete_after=5)

    @commands.command()
    async def apply(self, ctx, user1: User):
        owner_profile = db.queryUser({'DISNAME': str(user1)})
        team_profile = db.queryTeam({'TNAME': owner_profile['TEAM']})

        if owner_profile['TEAM'] == 'PCG':
            await ctx.send(m.USER_NOT_ON_TEAM, delete_after=5)
        else:

            if owner_profile['DISNAME'] == team_profile['OWNER']:

                member_profile = db.queryUser({'DISNAME': str(user1)})
                # If user is part of a team you cannot add them to your team
                if member_profile['TEAM'] != 'PCG':
                    await main.DM(ctx, user1, f"{ctx.author.mention}" + f" Applied to join {team_profile['TNAME']} !" + f" You may accept or deny in server." )
                    accept = await ctx.send(f"{ctx.author.mention}" + " applies to join "+f"{user1.mention}" +f" do you accept...?".format(self), delete_after=10)
                    for emoji in emojis:
                        await accept.add_reaction(emoji)

                    def check(reaction, user):
                        return user == user1 and str(reaction.emoji) == '👍'

                    try:
                        confirmed = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                        team_query = {'TNAME': team_profile['TNAME']}
                        new_value_query = {'$push': {'MEMBERS': str(ctx.author)}}
                        response = db.addTeamMember(team_query, new_value_query, str(ctx.author), str(user1))
                        await ctx.send(response)
                    except:
                        await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=3)
                else:
                    await ctx.send(m.USER_ALREADY_ON_TEAM, delete_after=5)

            else:
                await ctx.send(m.OWNER_ONLY_COMMAND, delete_after=5)

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


            embedVar = discord.Embed(title=f":checkered_flag: {team_name}' Team Card".format(self), description=":bank: Party Chat Gaming Database", colour=000000)
            if team['LOGO_FLAG']:
                embedVar.set_image(url=logo)
            embedVar.add_field(name="Owner :man_detective:", value= owner_name.split("#",1)[0])
            embedVar.add_field(name="Games :video_game:", value=f'{games[0]}'.format(self))
            embedVar.add_field(name="Members :military_helmet:", value="\n".join(f'{t}'.format(self) for t in team_list), inline=False)
            embedVar.add_field(name="Scrim Wins :medal:", value=scrim_wins)
            embedVar.add_field(name="Scrim Losses :crossed_swords:", value=scrim_losses)
            embedVar.add_field(name="Tournament Wins :fireworks:", value=tournament_wins, inline=False)

            await ctx.send(embed=embedVar)
        else:
            await ctx.send(m.TEAM_DOESNT_EXIST, delete_after=5)

    @commands.command()
    async def dtm(self, ctx, user1: User):
        owner_profile = db.queryUser({'DISNAME': str(ctx.author)})
        team_profile = db.queryTeam({'TNAME': owner_profile['TEAM']})
        if team_profile:
            if owner_profile['DISNAME'] == team_profile['OWNER']:

                    accept = await ctx.send(f"Do you want to remove {user1.mention} from the {team_profile['TNAME']}?".format(self), delete_after=8)
                    for emoji in emojis:
                        await accept.add_reaction(emoji)

                    def check(reaction, user):
                        return user == ctx.author and str(reaction.emoji) == '👍'

                    try:
                        confirmed = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                        team_query = {'TNAME': team_profile['TNAME']}
                        new_value_query = {'$pull': {'MEMBERS': str(user1)}}
                        response = db.deleteTeamMember(team_query, new_value_query, str(user1))
                        await ctx.send(response)
                    except:
                        print("Team not created. ")
            else:
                await ctx.send(m.OWNER_ONLY_COMMAND, delete_after=5)
        else:
            await ctx.send(m.TEAM_DOESNT_EXIST, delete_after=5)

    @commands.command()
    async def lteam(self, ctx):
        member_profile = db.queryUser({'DISNAME': str(ctx.author)})
        team_profile = db.queryTeam({'TNAME': member_profile['TEAM']})
        if team_profile:

                    accept = await ctx.send(f"Do you want to leave team {member_profile['TEAM']}?".format(self), delete_after=8)
                    for emoji in emojis:
                        await accept.add_reaction(emoji)

                    def check(reaction, user):
                        return user == ctx.author and str(reaction.emoji) == '👍'

                    try:
                        confirmed = await self.bot.wait_for('reaction_add', timeout=5.0, check=check)
                        team_query = {'TNAME': member_profile['TEAM']}
                        new_value_query = {'$pull': {'MEMBERS': str(ctx.author)}}
                        response = db.deleteTeamMember(team_query, new_value_query, str(ctx.author))
                        await ctx.send(response)
                    except:
                        print("Team not created. ")

        else:
            await ctx.send(m.TEAM_DOESNT_EXIST, delete_after=5)


    @commands.command()
    async def dt(self, ctx, *args):
        team_name = " ".join([*args])
        team_query = {'OWNER': str(ctx.author), 'TNAME': team_name}
        team = db.queryTeam(team_query)
        if team:
            if team['OWNER'] == str(ctx.author):
                accept = await ctx.send(f"Do you want to delete the {team['GAMES'][0]} team {team_name}?".format(self), delete_after=10)
                for emoji in emojis:
                    await accept.add_reaction(emoji)

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) == '👍'

                try:
                    confirmed = await self.bot.wait_for('reaction_add', timeout=8.0, check=check)
                    response = db.deleteTeam(team, str(ctx.author))

                    user_query = {'DISNAME': str(ctx.author)}
                    new_value = {'$set': {'TEAM': 'PCG'}}
                    db.updateUserNoFilter(user_query, new_value)

                    await ctx.send(response)
                except:
                    print("Team not created. ")
            else:
                await ctx.send("Only the owner of the team can delete the team. ")
        else:
            await ctx.send(m.TEAM_DOESNT_EXIST, delete_after=5)




def setup(bot):
    bot.add_cog(Teams(bot))