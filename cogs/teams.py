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

class Teams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Teams Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @cog_ext.cog_slash(description="Create a new team", guild_ids=main.guild_ids)
    async def createteam(self, ctx, team: str):
        team_name = team
        if team_name == "":
            return
        team_query = {'OWNER': str(ctx.author), 'TNAME': team_name, 'MEMBERS': [str(ctx.author)], 'GAMES': ["Crown Unlimited"]}
        accept = await ctx.send(f"Do you want to create the team {team_name}?".format(self), delete_after=10)
        for emoji in emojis:
            await accept.add_reaction(emoji)

        def check(reaction, user):
            return (user == ctx.author and (str(reaction.emoji) == '👍')) or (user == ctx.author and (str(reaction.emoji) == '👎'))

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)

            if str(reaction.emoji) == '👎':
                await ctx.send("Team not created.")
                return

            response = db.createTeam(data.newTeam(team_query), str(ctx.author))
            await ctx.send(response)
        except:
            print("Team not created. ")

    @cog_ext.cog_slash(description="Recruit team member", guild_ids=main.guild_ids)
    async def recruit(self, ctx, player: User):
        owner_profile = db.queryUser({'DISNAME': str(ctx.author)})
        team_profile = db.queryTeam({'TNAME': owner_profile['TEAM']})

        if owner_profile['TEAM'] == 'PCG':
            await ctx.send(m.USER_NOT_ON_TEAM, delete_after=5)
        else:

            if owner_profile['DISNAME'] == team_profile['OWNER']:

                member_profile = db.queryUser({'DISNAME': str(player)})
                # If user is part of a team you cannot add them to your team
                if member_profile['TEAM'] == 'PCG':
                    await main.DM(ctx, player, f"{ctx.author.mention}" + f" has invited you to join {team_profile['TNAME']} !" + f" React in server to join {team_profile['TNAME']}" )
                    accept = await ctx.send(f"{player.mention}" +f" do you want to join team {team_profile['TNAME']}?".format(self), delete_after=10)
                    for emoji in emojis:
                        await accept.add_reaction(emoji)

                    def check(reaction, user):
                        return user == player and str(reaction.emoji) == '👍'

                    try:
                        confirmed = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                        team_query = {'TNAME': team_profile['TNAME']}
                        new_value_query = {'$push': {'MEMBERS': str(player)}}
                        response = db.addTeamMember(team_query, new_value_query, str(ctx.author), str(player))
                        await ctx.send(response)
                    except:
                        await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=3)
                else:
                    await ctx.send(m.USER_ALREADY_ON_TEAM, delete_after=5)

            else:
                await ctx.send(m.OWNER_ONLY_COMMAND, delete_after=5)

    @cog_ext.cog_slash(description="Apply for a team", guild_ids=main.guild_ids)
    async def apply(self, ctx, owner: User):
        owner_profile = db.queryUser({'DISNAME': str(owner)})
        team_profile = db.queryTeam({'TNAME': owner_profile['TEAM']})

        if owner_profile['TEAM'] == 'PCG':
            await ctx.send(m.USER_NOT_ON_TEAM, delete_after=5)
        else:

            if owner_profile['DISNAME'] == team_profile['OWNER']:
                member_profile = db.queryUser({'DISNAME': str(owner)})
                # If user is part of a team you cannot add them to your team
                if member_profile['TEAM'] != 'PCG':
                    await main.DM(ctx, owner, f"{ctx.author.mention}" + f" Applied to join {team_profile['TNAME']} !" + f" You may accept or deny in server." )
                    accept = await ctx.send(f"{ctx.author.mention}" + " applies to join "+f"{owner.mention}" +f" do you accept...?".format(self), delete_after=10)
                    for emoji in emojis:
                        await accept.add_reaction(emoji)

                    def check(reaction, user):
                        return user == owner and str(reaction.emoji) == '👍'

                    try:
                        confirmed = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                        team_query = {'TNAME': team_profile['TNAME']}
                        new_value_query = {'$push': {'MEMBERS': str(ctx.author)}}
                        response = db.addTeamMember(team_query, new_value_query, str(owner), str(ctx.author))
                        await ctx.send(response)
                    except:
                        await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=3)
                else:
                    await ctx.send(m.USER_ALREADY_ON_TEAM, delete_after=5)
            else:
                await ctx.send(m.OWNER_ONLY_COMMAND, delete_after=5)

    @cog_ext.cog_slash(description="Delete team member", guild_ids=main.guild_ids)
    async def deletemember(self, ctx, member: User):
        owner_profile = db.queryUser({'DISNAME': str(ctx.author)})
        team_profile = db.queryTeam({'TNAME': owner_profile['TEAM']})
        if team_profile:
            if owner_profile['DISNAME'] == team_profile['OWNER']:

                    accept = await ctx.send(f"Do you want to remove {member.mention} from the {team_profile['TNAME']}?".format(self), delete_after=8)
                    for emoji in emojis:
                        await accept.add_reaction(emoji)

                    def check(reaction, user):
                        return (user == ctx.author and (str(reaction.emoji) == '👍')) or (user == ctx.author and (str(reaction.emoji) == '👎'))

                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                        if str(reaction.emoji) == '👎':
                            await ctx.send("Member not deleted. ")
                            return
                        team_query = {'TNAME': team_profile['TNAME']}
                        new_value_query = {'$pull': {'MEMBERS': str(member)}}
                        response = db.deleteTeamMember(team_query, new_value_query, str(member))
                        await ctx.send(response)
                    except:
                        print("Team not created. ")
            else:
                await ctx.send(m.OWNER_ONLY_COMMAND, delete_after=5)
        else:
            await ctx.send(m.TEAM_DOESNT_EXIST, delete_after=5)

    @cog_ext.cog_slash(description="Leave a team", guild_ids=main.guild_ids)
    async def leaveteam(self, ctx):
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

    @cog_ext.cog_slash(description="Delete a team", guild_ids=main.guild_ids)
    async def deleteteam(self, ctx, team: str):
        team_name = team
        team_query = {'OWNER': str(ctx.author), 'TNAME': team_name}
        team = db.queryTeam(team_query)
        guildteam=False
        if team:
            guildname = team['GUILD']
            if guildname != 'PCG':
                guildteam=True
            if team['OWNER'] == str(ctx.author):
                accept = await ctx.send(f"Do you want to delete the {team['GAMES'][0]} team {team_name}?".format(self), delete_after=10)
                for emoji in emojis:
                    await accept.add_reaction(emoji)

                def check(reaction, user):
                    return (user == ctx.author and (str(reaction.emoji) == '👍')) or (user == ctx.author and (str(reaction.emoji) == '👎'))

                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=8.0, check=check)
                    if str(reaction.emoji) == '👎':
                        await ctx.send("Team not deleted.")
                        return
                    response = db.deleteTeam(team, str(ctx.author))

                    user_query = {'DISNAME': str(ctx.author)}
                    new_value = {'$set': {'TEAM': 'PCG'}}
                    db.updateUserNoFilter(user_query, new_value)
                    await ctx.send(response)
                    if guildteam:
                        guild_query = {'GNAME' : str(guildname)}
                        guild_info = db.queryGuildAlt(guild_query)
                        new_query = {'FOUNDER' : str(guild_info['FOUNDER'])}
                        if guild_info:
                            pull_team = {'$pull' : {'SWORDS' : str(team_name)}}
                            response2 = db.deleteGuildSword(new_query, pull_team, str(guild_info['FOUNDER']), str(team_name))
                            await ctx.send(response2)
                except Exception as e:
                    print(e)
            else:
                await ctx.send("Only the owner of the team can delete the team. ")
        else:
            await ctx.send(m.TEAM_DOESNT_EXIST, delete_after=5)

def setup(bot):
    bot.add_cog(Teams(bot))