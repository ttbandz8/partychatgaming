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

class Family(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Teams Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)


    @commands.command()
    async def marry(self, ctx, user1: User):
        head_profile = db.queryUser({'DISNAME': str(ctx.author)})
        partner_profile = db.queryUser({'DISNAME': str(user1)})
        if head_profile['FAMILY'] != 'PCG' and head_profile['FAMILY'] != 'N/A' and head_profile['FAMILY'] != head_profile['DISNAME'] :
            await ctx.send(m.USER_IN_FAMILY, delete_after=3)
        elif partner_profile['FAMILY'] != 'PCG' and partner_profile['FAMILY'] != 'N/A':
            await ctx.send(m.USER_IN_FAMILY, delete_after=3)
        else:
            family_query = {'HEAD': str(ctx.author)}
            accept = await ctx.send(f"Do you want to propose to {user1.mention}?".format(self), delete_after=10)
            for emoji in emojis:
                await accept.add_reaction(emoji)

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) == '👍'

            try:
                confirmed1 = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                await main.DM(ctx, user1, f"{ctx.author.mention}" + f" proposed to you !" + f" React in server to join their family" )
                accept = await ctx.send(f"{user1.mention}" +f" do you accept the proposal?".format(self), delete_after=10)
                for emoji in emojis:
                    await accept.add_reaction(emoji)

                def check(reaction, partner):
                    return partner == user1 and str(reaction.emoji) == '👍'

                try:
                    confirmed2 = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                    response = db.createFamily(data.newFamily(family_query), str(ctx.author))
                    await ctx.send(response)
                    newvalue = {'$set': {'PARTNER': str(user1)}}
                    nextresponse = db.addFamilyMember(family_query, newvalue, str(ctx.author), str(user1))
                    await ctx.send(nextresponse)
                except:
                    await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=3)
            except:
                print("No proposal Sent") 

    @commands.command()
    async def divorce(self, ctx, user1: User):
        head_profile = db.queryUser({'DISNAME': str(ctx.author)})
        family_profile = db.queryFamily({'HEAD': head_profile['FAMILY']})
        family_bank = family_profile['BANK']
        divorce_split = family_bank * .50
        family_query = {'HEAD': str(ctx.author)}
        if family_profile:
            if head_profile['DISNAME'] == family_profile['HEAD']:
                accept = await ctx.send(f"Do you want to divorce {user1.mention}?".format(self), delete_after=8)
                for emoji in emojis:
                    await accept.add_reaction(emoji)

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) == '👍'

                try:
                    confirmed = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                    accept1 = await ctx.send(f"{user1.mention} do you accept the divorce?")
                    for emoji in emojis:
                        await accept1.add_reaction(emoji)

                    def check(reaction, partner):
                        return partner == user1 and str(reaction.emoji) == '👍'

                    try:
                        confirmed2 = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                        new_value_query = {'$set': {'PARTNER': '' }}
                        response = db.deleteFamilyMember(family_query, new_value_query, str(ctx.author), str(user1))
                        await ctx.send(response)
                        main.curse(divorce_split)
                    except:
                        print("Divorce Not Accepted ")
                except:
                    print("No Divorce")
            else:
                await ctx.send(m.OWNER_ONLY_COMMAND, delete_after=5)
        else:
            await ctx.send(m.TEAM_DOESNT_EXIST, delete_after=5)

    @commands.command()
    async def adopt(self, ctx, user1: User):
        head_profile = db.queryUser({'DISNAME': str(ctx.author)})
        kid_profile = db.queryUser({'DISNAME': str(user1)})
        if head_profile['FAMILY'] == 'PCG':
            await ctx.send(m.USER_NOT_IN_FAMILY, delete_after=3)
        elif kid_profile['FAMILY'] != 'PCG':
            await ctx.send(m.USER_IN_FAMILY, delete_after=3)
        else:
            family_query = {'HEAD': str(ctx.author)}
            accept = await ctx.send(f"Do you want to adopt {user1.mention}?".format(self), delete_after=10)
            for emoji in emojis:
                await accept.add_reaction(emoji)

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) == '👍'

            try:
                confirmed1 = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                await main.DM(ctx, user1, f"{ctx.author.mention}" + f" would like to adopt yo!" + f" React in server to join their family" )
                accept = await ctx.send(f"{user1.mention}" +f" would you like to be adopted ?".format(self), delete_after=10)
                for emoji in emojis:
                    await accept.add_reaction(emoji)

                def check(reaction, kid):
                    return kid == user1 and str(reaction.emoji) == '👍'

                try:
                    confirmed2 = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                    newvalue = {'$push': {'KIDS': str(user1)}}
                    response = db.addFamilyMember(family_query, newvalue, str(ctx.author), str(user1))
                    await ctx.send(response)
                    
                except:
                    await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=3)
            except:
                print("No proposal Sent") 

    @commands.command()
    async def runaway(self, ctx):
        kid_profile = db.queryUser({'DISNAME': str(ctx.author)})
        family_profile = db.queryFamily({'HEAD': kid_profile['FAMILY']})
        family_query = {'HEAD': kid_profile['FAMILY']}
        if family_profile:

                    accept = await ctx.send(f"Do you want to Runaway from your family?".format(self), delete_after=8)
                    for emoji in emojis:
                        await accept.add_reaction(emoji)

                    def check(reaction, user):
                        return user == ctx.author and str(reaction.emoji) == '👍'

                    try:
                        confirmed = await self.bot.wait_for('reaction_add', timeout=5.0, check=check)
                        new_value_query = {'$pull': {'KIDS': str(ctx.author)}}
                        response = db.deleteFamilyMemberAlt(family_query, new_value_query, str(ctx.author))
                        await ctx.send(response)
                    except:
                        print("Team not created. ")

        else:
            await ctx.send(m.TEAM_DOESNT_EXIST, delete_after=5)

    @commands.command()
    async def abandon(self, ctx):
        family_query = {'HEAD': str(ctx.author)}
        family = db.queryFamily(family_query)
        if family:
            if family['HEAD'] == str(ctx.author):
                accept = await ctx.send(f"Do you want to abandon your family?".format(self), delete_after=10)
                for emoji in emojis:
                    await accept.add_reaction(emoji)

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) == '👍'

                try:
                    confirmed = await self.bot.wait_for('reaction_add', timeout=8.0, check=check)
                    response = db.deleteFamily(family, str(ctx.author))

                    user_query = {'DISNAME': str(ctx.author)}
                    new_value = {'$set': {'FAMILY': 'PCG'}}
                    db.updateUserNoFilter(user_query, new_value)

                    await ctx.send(response)
                except:
                    print("Family Not Deleted. ")
            else:
                await ctx.send("Only the Head Of Household can abandon the family. ")
        else:
            await ctx.send(m.TEAM_DOESNT_EXIST, delete_after=5)




def setup(bot):
    bot.add_cog(Family(bot))