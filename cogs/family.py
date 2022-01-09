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

class Family(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Family Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)


    @cog_ext.cog_slash(description="Marry a player", guild_ids=main.guild_ids)
    async def marry(self, ctx, player: User):
        head_profile = db.queryUser({'DISNAME': str(ctx.author)})
        partner_profile = db.queryUser({'DISNAME': str(player)})
        if head_profile['FAMILY'] != 'PCG' and head_profile['FAMILY'] != 'N/A' and head_profile['FAMILY'] != head_profile['DISNAME'] :
            await ctx.send(m.USER_IN_FAMILY, delete_after=3)
        elif partner_profile['FAMILY'] != 'PCG' and partner_profile['FAMILY'] != 'N/A':
            await ctx.send(m.USER_IN_FAMILY, delete_after=3)
        else:
            family_query = {'HEAD': str(ctx.author)}
            
            trade_buttons = [
                manage_components.create_button(
                    style=ButtonStyle.green,
                    label="Propose!",
                    custom_id="yes"
                ),
                manage_components.create_button(
                    style=ButtonStyle.blue,
                    label="No",
                    custom_id="no"
                )
            ]
            trade_buttons_action_row = manage_components.create_actionrow(*trade_buttons)
            await button_ctx.send(f"Do you want to propose to **{player.mention}**?", components=[trade_buttons_action_row])
            
            def check(button_ctx):
                return button_ctx.author == ctx.author

            
            try:
                button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[trade_buttons_action_row], timeout=120, check=check)
                if button_ctx.custom_id == "no":
                        await button_ctx.send("No **Proposal**")
                        self.stop = True
                if button_ctx.custom_id == "yes":
                    await main.DM(ctx, player, f"{ctx.author.mention}" + f" proposed to you !" + f" React in server to join their family" )
                    await ctx.send(f"{player.mention}" +f" do you accept the proposal?".format(self), delete_after=10)
                    trade_buttons = [
                        manage_components.create_button(
                            style=ButtonStyle.green,
                            label="Lets Get Married!",
                            custom_id="yes"
                        ),
                        manage_components.create_button(
                            style=ButtonStyle.blue,
                            label="No",
                            custom_id="no"
                        )
                    ]
                    trade_buttons_action_row = manage_components.create_actionrow(*trade_buttons)
                    await button_ctx.send(f"**{player.mention}** do you accept the proposal?".format(self), components=[trade_buttons_action_row])
                    
                    def check(button_ctx):
                        return button_ctx.author == player

                    
                    try:
                        button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[trade_buttons_action_row], timeout=120, check=check)
                        if button_ctx.custom_id == "no":
                                await button_ctx.send("**Proposal Denied**")
                                self.stop = True
                        if button_ctx.custom_id == "yes":
                            try:
                                response = db.createFamily(data.newFamily(family_query), str(ctx.author))
                                await ctx.send(response)
                                newvalue = {'$set': {'PARTNER': str(player)}}
                                nextresponse = db.addFamilyMember(family_query, newvalue, str(ctx.author), str(player))
                                await ctx.send(nextresponse)
                            except:
                                await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=3)
                    except Exception as ex:
                        trace = []
                        tb = ex.__traceback__
                        while tb is not None:
                            trace.append({
                                "filename": tb.tb_frame.f_code.co_filename,
                                "name": tb.tb_frame.f_code.co_name,
                                "lineno": tb.tb_lineno
                            })
                            tb = tb.tb_next
                        print(str({
                            'type': type(ex).__name__,
                            'message': str(ex),
                            'trace': trace
                        }))
                        await ctx.send(f"ERROR:\nTYPE: {type(ex).__name__}\nMESSAGE: {str(ex)}\nLINE: {trace} ")
                        return
            except:
                print("No proposal Sent") 

    @cog_ext.cog_slash(description="Divorce your partner", guild_ids=main.guild_ids)
    async def divorce(self, ctx, partner: User):
        head_profile = db.queryUser({'DISNAME': str(ctx.author)})
        family_profile = db.queryFamily({'HEAD': head_profile['FAMILY']})
        family_bank = family_profile['BANK']
        divorce_split = family_bank * .50
        family_query = {'HEAD': str(ctx.author)}
        if family_profile:
            if head_profile['DISNAME'] == family_profile['HEAD'] or head_profile['DISNAME'] == family_profile['PARTNER']:
                accept = await ctx.send(f"Do you want to divorce {partner.mention}?".format(self), delete_after=8)
                for emoji in emojis:
                    await accept.add_reaction(emoji)

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) == '👍'

                try:
                    confirmed = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                    accept1 = await ctx.send(f"{partner.mention} do you accept the divorce?")
                    for emoji in emojis:
                        await accept1.add_reaction(emoji)

                    def check(reaction, partner):
                        return partner == partner and str(reaction.emoji) == '👍'

                    try:
                        confirmed2 = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                        new_value_query = {'$set': {'PARTNER': '' }}
                        response = db.deleteFamilyMember(family_query, new_value_query, str(ctx.author), str(partner))
                        await ctx.send(response)
                        main.cursefamily(divorce_split,family_profile)
                        main.bless(divorce_split, partner)
                    except:
                        print("Divorce Not Accepted ")
                except:
                    print("No Divorce")
            else:
                await ctx.send(m.OWNER_ONLY_COMMAND, delete_after=5)
        else:
            await ctx.send(m.TEAM_DOESNT_EXIST, delete_after=5)

    @cog_ext.cog_slash(description="Adopt a kid", guild_ids=main.guild_ids)
    async def adopt(self, ctx, player: User):
        head_profile = db.queryUser({'DISNAME': str(ctx.author)})
        kid_profile = db.queryUser({'DISNAME': str(player)})
        if head_profile['FAMILY'] == 'PCG':
            await ctx.send(m.USER_NOT_IN_FAMILY, delete_after=3)
        elif kid_profile['FAMILY'] != 'PCG':
            await ctx.send(m.USER_IN_FAMILY, delete_after=3)
        else:
            family_query = {'HEAD': str(ctx.author)}
            family = db.queryFamily(family_query)
            kid_count = 0
            for kids in family['KIDS']:
                kid_count = kid_count + 1
            if kid_count >= 2:
                await ctx.send(m.MAX_CHILDREN, delete_after=3)
                return

            accept = await ctx.send(f"Do you want to adopt {player.mention}?".format(self), delete_after=10)
            for emoji in emojis:
                await accept.add_reaction(emoji)

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) == '👍'

            try:
                confirmed1 = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                await main.DM(ctx, player, f"{ctx.author.mention}" + f" would like to adopt yo!" + f" React in server to join their family" )
                accept = await ctx.send(f"{player.mention}" +f" would you like to be adopted ?".format(self), delete_after=10)
                for emoji in emojis:
                    await accept.add_reaction(emoji)

                def check(reaction, kid):
                    return kid == player and str(reaction.emoji) == '👍'

                try:
                    confirmed2 = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                    newvalue = {'$push': {'KIDS': str(player)}}
                    response = db.addFamilyMember(family_query, newvalue, str(ctx.author), str(player))
                    await ctx.send(response)
                    
                except:
                    await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=3)
            except:
                print("No proposal Sent") 

    @cog_ext.cog_slash(description="Disown your kid", guild_ids=main.guild_ids)
    async def disown(self, ctx, kid: User):
        head_profile = db.queryUser({'DISNAME': str(ctx.author)})
        family_profile = db.queryFamily({'HEAD': head_profile['FAMILY']})
        family_query = {'HEAD': str(ctx.author)}
        if family_profile:
            if head_profile['DISNAME'] == family_profile['HEAD']:
                accept = await ctx.send(f"Do you want to disown {kid.mention}?".format(self), delete_after=8)
                for emoji in emojis:
                    await accept.add_reaction(emoji)

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) == '👍'

                try:
                    confirmed = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                    new_value_query = {'$pull': {'KIDS': str(kid) }}
                    response = db.deleteFamilyMember(family_query, new_value_query, str(ctx.author), str(kid))
                    await ctx.send(response)
                except:
                    print("No Divorce")
            else:
                await ctx.send(m.OWNER_ONLY_COMMAND, delete_after=5)
        else:
            await ctx.send(m.TEAM_DOESNT_EXIST, delete_after=5)

    @cog_ext.cog_slash(description="Runaway from your family", guild_ids=main.guild_ids)
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

    @cog_ext.cog_slash(description="Abandon your family", guild_ids=main.guild_ids)
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