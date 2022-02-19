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
from discord_slash import SlashCommand
from discord_slash.utils import manage_components
from discord_slash.model import ButtonStyle

emojis = ['👍', '👎']

class Teams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Teams Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @cog_ext.cog_slash(description="Create a new guild", guild_ids=main.guild_ids)
    async def createguild(self, ctx, guild: str):
        user = db.queryUser({'DID': str(ctx.author.id)})
        if user['LEVEL'] < 11:
            await ctx.send("🔓 Unlock Guilds by completing Floor 10 of the 🌑 Abyss! Use /abyss to enter the abyss.")
            return
        team_name = guild.lower()
        team_display_name = guild
        transaction_message = f"{user['DISNAME']} has joined the guild."


        team_query = {
            'OWNER': str(ctx.author), 
            'TEAM_NAME': team_name, 
            'TEAM_DISPLAY_NAME': team_display_name, 
            'MEMBERS': [str(ctx.author)],
            'TRANSACTIONS': [transaction_message]
            }

        team_buttons = [
            manage_components.create_button(
                style=ButtonStyle.blue,
                label="Create",
                custom_id="Yes"
            ),
            manage_components.create_button(
                style=ButtonStyle.red,
                label="Cancel",
                custom_id="No"
            )
        ]
        team_buttons_action_row = manage_components.create_actionrow(*team_buttons)
        msg = await ctx.send(f"Create the Guild **{team_display_name}**?".format(self), components=[team_buttons_action_row])


        def check(button_ctx):
            return button_ctx.author == ctx.author

        try:
            button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[team_buttons_action_row], check=check)

            if button_ctx.custom_id == "No":
                await msg.delete()
                return
            
            if button_ctx.custom_id == "Yes":
                
                response = db.createTeam(data.newTeam(team_query), str(ctx.author.id))
                await button_ctx.send(response)
                await msg.delete()
        except:
            await ctx.send("Guild already exists")
    
    @cog_ext.cog_slash(description="Recruit Guild member", guild_ids=main.guild_ids)
    async def recruit(self, ctx, player: User):
        owner_profile = db.queryUser({'DID': str(ctx.author.id)})
        team_profile = db.queryTeam({'TEAM_NAME': owner_profile['TEAM']})
        if owner_profile['LEVEL'] < 11:
            await ctx.send("🔓 Unlock Guilds by completing Floor 10 of the 🌑 Abyss! Use /abyss to enter the abyss.")
            return


        if owner_profile['TEAM'] == 'PCG':
            await ctx.send(m.USER_NOT_ON_TEAM, delete_after=5)
        else:

            if owner_profile['DISNAME'] == team_profile['OWNER']:

                member_profile = db.queryUser({'DID': str(player.id)})
                if member_profile['LEVEL'] < 11:
                    await ctx.send(f"🔓 {player.mention} has not unlocked Guilds!. Complete Floor 10 of the 🌑 Abyss! Use /abyss to enter the abyss.")
                    return

                # If user is part of a team you cannot add them to your team
                if member_profile['TEAM'] == 'PCG':
                    await main.DM(ctx, player, f"{ctx.author.mention}" + f" has invited you to join **{team_profile['TEAM_NAME']}** !" + f" React in server to join **{team_profile['TEAM_NAME']}**" )

                    team_buttons = [
                        manage_components.create_button(
                            style=ButtonStyle.blue,
                            label="✔️",
                            custom_id="Yes"
                        ),
                        manage_components.create_button(
                            style=ButtonStyle.red,
                            label="❌",
                            custom_id="No"
                        )
                    ]
                    team_buttons_action_row = manage_components.create_actionrow(*team_buttons)
                    await ctx.send(f"{player.mention}" +f" do you want to join Guild **{team_profile['TEAM_NAME']}**?".format(self), components=[team_buttons_action_row])

                    def check(button_ctx):
                        return str(button_ctx.author) == str(player)

                    try:
                        button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[team_buttons_action_row], check=check)
                        
                        if button_ctx.custom_id == "No":
                            await button_ctx.send("Member not added.")
                            return

                        if button_ctx.custom_id == "Yes":
                            team_query = {'TEAM_NAME': team_profile['TEAM_NAME']}
                            new_value_query = {
                                '$push': {'MEMBERS': str(player)},
                                '$inc': {'MEMBER_COUNT': 1}
                                }
                            response = db.addTeamMember(team_query, new_value_query, str(ctx.author), str(player))
                            await button_ctx.send(response)
                    except:
                        await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=3)
                else:
                    await ctx.send(m.USER_ALREADY_ON_TEAM, delete_after=5)

            else:
                await ctx.send(m.OWNER_ONLY_COMMAND, delete_after=5)

    @cog_ext.cog_slash(description="Apply for a Guild", guild_ids=main.guild_ids)
    async def apply(self, ctx, owner: User):
        owner_profile = db.queryUser({'DID': str(owner.id)})
        team_profile = db.queryTeam({'TEAM_NAME': owner_profile['TEAM']})

        if owner_profile['TEAM'] == 'PCG':
            await ctx.send(m.USER_NOT_ON_TEAM, delete_after=5)
        else:

            if owner_profile['DISNAME'] == team_profile['OWNER']:
                member_profile = db.queryUser({'DID': str(ctx.author.id)})
                if member_profile['LEVEL'] < 11:
                    await ctx.send(f"🔓 Unlock Guilds by completing Floor 10 of the 🌑 Abyss! Use /abyss to enter the abyss.")
                    return

                # If user is part of a team you cannot add them to your team
                if member_profile['TEAM'] != 'PCG':
                    await main.DM(ctx, owner, f"{ctx.author.mention}" + f" Applied to join **{team_profile['TEAM_NAME']}** !" + f" You may accept or deny in server." )
                    
                    team_buttons = [
                        manage_components.create_button(
                            style=ButtonStyle.blue,
                            label="✔️",
                            custom_id="Yes"
                        ),
                        manage_components.create_button(
                            style=ButtonStyle.red,
                            label="❌",
                            custom_id="No"
                        )
                    ]
                    team_buttons_action_row = manage_components.create_actionrow(*team_buttons)
                    
                    await ctx.send(f"{ctx.author.mention}" + " applies to join "+f"{owner.mention}" +f" do you accept...?".format(self), components=[team_buttons_action_row])

                    def check(button_ctx):
                        return str(button_ctx.author) == str(owner)

                    try:
                        button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[team_buttons_action_row], check=check)
                        
                        if button_ctx.custom_id == "No":
                            await button_ctx.send("Application Denied.")
                            return

                        if button_ctx.custom_id == "Yes":
                            team_query = {'TEAM_NAME': team_profile['TEAM_NAME']}
                            new_value_query = {'$push': {'MEMBERS': str(ctx.author)}}
                            response = db.addTeamMember(team_query, new_value_query, str(owner), str(ctx.author))
                            await button_ctx.send(response)
                    except:
                        await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=3)
                else:
                    await ctx.send(m.USER_ALREADY_ON_TEAM, delete_after=5)
            else:
                await ctx.send(m.OWNER_ONLY_COMMAND, delete_after=5)

    @cog_ext.cog_slash(description="Delete guild member", guild_ids=main.guild_ids)
    async def deletemember(self, ctx, member: User):
        owner_profile = db.queryUser({'DID': str(ctx.author.id)})
        team_profile = db.queryTeam({'TEAM_NAME': owner_profile['TEAM']})
        if team_profile:
            if owner_profile['DISNAME'] == team_profile['OWNER']:  
                team_buttons = [
                    manage_components.create_button(
                        style=ButtonStyle.blue,
                        label="✔️",
                        custom_id="Yes"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red,
                        label="❌",
                        custom_id="No"
                    )
                ]
                team_buttons_action_row = manage_components.create_actionrow(*team_buttons)
                await ctx.send(f"Do you want to remove {member.mention} from the **{team_profile['TEAM_NAME']}**?".format(self), components=[team_buttons_action_row])

                def check(button_ctx):
                    return button_ctx.author == ctx.author

                try:
                    button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[team_buttons_action_row], check=check)
                    
                    if button_ctx.custom_id == "No":
                        await button_ctx.send("Member Not Deleted.")
                        return

                    if button_ctx.custom_id == "Yes":    
                        team_query = {'TEAM_NAME': team_profile['TEAM_NAME']}
                        new_value_query = {
                            '$pull': {'MEMBERS': str(member)},
                            '$inc': {'MEMBER_COUNT': -1}
                            }
                        response = db.deleteTeamMember(team_query, new_value_query, str(member))
                        await button_ctx.send(response)
                except:
                    print("Guild not created. ")
            else:
                await ctx.send(m.OWNER_ONLY_COMMAND, delete_after=5)
        else:
            await ctx.send(m.TEAM_DOESNT_EXIST, delete_after=5)

    @cog_ext.cog_slash(description="Leave a guild", guild_ids=main.guild_ids)
    async def leaveguild(self, ctx):
        member_profile = db.queryUser({'DID': str(ctx.author.id)})
        team_profile = db.queryTeam({'TEAM_NAME': member_profile['TEAM'].lower()})
        
        if team_profile:
            team_display_name = team_profile['TEAM_DISPLAY_NAME']
            team_name = team_profile['TEAM_NAME'].lower()
            transaction_message = f"{member_profile['DISNAME']} has left the guild."

            team_buttons = [
                manage_components.create_button(
                    style=ButtonStyle.blue,
                    label="Leave",
                    custom_id="Yes"
                ),
                manage_components.create_button(
                    style=ButtonStyle.red,
                    label="Stay",
                    custom_id="No"
                )
            ]
            team_buttons_action_row = manage_components.create_actionrow(*team_buttons)
            msg = await ctx.send(f"Leave guild **{team_display_name}**?".format(self), components=[team_buttons_action_row])

            def check(button_ctx):
                return button_ctx.author == ctx.author

            try:
                button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[team_buttons_action_row], check=check)

                if button_ctx.custom_id == "No":
                    await msg.delete()
                    return
                
                if button_ctx.custom_id == "Yes":
                    team_query = {'TEAM_NAME': team_name}
                    new_value_query = {
                        '$pull': {'MEMBERS': member_profile['DISNAME']}, 
                        '$addToSet': {'TRANSACTIONS': transaction_message},
                        '$inc': {'MEMBER_COUNT': -1}
                        }
                    response = db.deleteTeamMember(team_query, new_value_query, str(ctx.author.id))
                    await ctx.send(response)
                    await msg.delete()
            except:
                print("Guild not Left. ")
        else:
            await ctx.send(m.TEAM_DOESNT_EXIST, delete_after=5)

    @cog_ext.cog_slash(description="Delete a guild", guild_ids=main.guild_ids)
    async def deleteguild(self, ctx, guild: str):
        team_query = {'TEAM_NAME': guild.lower()}
        team = db.queryTeam(team_query)
        user = db.queryUser({'DID': str(ctx.author.id)})
        guildteam=False
        if team:
            team_name = team['TEAM_NAME']
            team_display_name = team['TEAM_DISPLAY_NAME']
            
            # ASSOCIATION CHECK
            guildname = team['GUILD']
            if guildname != 'PCG':
                guildteam=True

            if team['OWNER'] == user['DISNAME']:
                team_buttons = [
                    manage_components.create_button(
                        style=ButtonStyle.blue,
                        label="Delete",
                        custom_id="Yes"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red,
                        label="Cancel",
                        custom_id="No"
                    )
                ]
                team_buttons_action_row = manage_components.create_actionrow(*team_buttons)

                msg = await ctx.send(f"Delete Guild **{team_display_name}**?".format(self), components=[team_buttons_action_row])

                def check(button_ctx):
                    return button_ctx.author == ctx.author

                try:
                    button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[team_buttons_action_row], check=check)

                    if button_ctx.custom_id == "No":
                        await msg.delete()
                        return

                    if button_ctx.custom_id == "Yes":
                        response = db.deleteTeam(team, str(ctx.author.id))
                        user_query = {'DID': str(ctx.author.id)}
                        new_value = {'$set': {'TEAM': 'PCG'}}
                        db.updateUserNoFilter(user_query, new_value)
                        await button_ctx.send(response)
                        if guildteam:
                            # ASSOCIATION CHECK
                            guild_query = {'GNAME' : str(guildname)}
                            guild_info = db.queryGuildAlt(guild_query)
                            new_query = {'FOUNDER' : str(guild_info['FOUNDER'])}
                            if guild_info:
                                pull_team = {'$pull' : {'SWORDS' : str(team_name)}}
                                response2 = db.deleteGuildSword(new_query, pull_team, str(guild_info['FOUNDER']), str(team_name))
                                await button_ctx.send(response2)
                except Exception as e:
                    print(e)
            else:
                await ctx.send("Only the owner of the Guild can delete the Guild. ")
        else:
            await ctx.send(m.TEAM_DOESNT_EXIST, delete_after=5)

def setup(bot):
    bot.add_cog(Teams(bot))