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
from discord_slash.utils import manage_components
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_commands import create_option, create_choice
from dinteractions_Paginator import Paginator

emojis = ['👍', '👎']

class Guild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Guild Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)


    @cog_ext.cog_slash(description="Swear into Association!", guild_ids=main.guild_ids)
    async def oath(self, ctx, sworn: User, association: str):
        try:
            owner = sworn
            guild_name = association
            cost = 10000
            founder_profile = db.queryUser({'DID': str(ctx.author.id)})
            guildsearch_name = founder_profile['GUILD']
            
            if founder_profile['LEVEL'] < 31:
                await ctx.send("🔓 Unlock Associations by completing Floor 30 of the 🌑 Abyss! Use /abyss to enter the abyss.")
                return
            if guildsearch_name != "PCG":
                guildsearch_query = {'GNAME' : guildsearch_name}
                guildsearch = db.queryGuildAlt(guildsearch_query)
                if guildsearch:
                    if guild_name != guildsearch_name:
                        await ctx.send(m.FOUNDER_LEAVE)
                        return
                    await ctx.send(f"{guildsearch_name} NEW OATH!")
                    sworn_profile = db.queryUser({'DISNAME': str(owner)}) 
                    if sworn_profile['LEVEL'] < 31:
                        await ctx.send(f"🔓 {sworn.mention} Has not Unlocked Associations! Complete Floor 30 of the 🌑 Abyss! Use /abyss to enter the abyss.")
                        return             
                    if sworn_profile['GUILD'] != 'PCG' and guildsearch['SHIELD'] != sworn_profile['DISNAME']:
                        await ctx.send(m.USER_IN_GUILD, delete_after=3)
                        return
                    else:
                        if founder_profile['TEAM'] == 'PCG' or sworn_profile['TEAM'] == 'PCG':
                            await ctx.send(m.FOUNDER_NO_TEAM, delete_after=3)
                            return
                        else:
                            fteam_query = {'TNAME' : founder_profile['TEAM']}
                            steam_query = {'TNAME' : sworn_profile['TEAM']}
                            founder_team = db.queryTeam(fteam_query)
                            sworn_team = db.queryTeam(steam_query)
                            fbal = founder_team['BANK']
                            sbal = sworn_team['BANK']
                            if founder_team['TNAME'] == sworn_team['TNAME']:
                                await ctx.send(m.SAME_TEAM, delete_after=3)
                                return
                            if sbal < cost:
                                await ctx.send(m.NBROKE_TEAM, delete_after=3)
                                return
                        
                            guild_query = {'FOUNDER': str(ctx.author)}
                            guild_buttons = [
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
                            guild_buttons_action_row = manage_components.create_actionrow(*guild_buttons)
                            await ctx.send(f"Do you wish to swear an oath with {owner.mention}?".format(self), components=[guild_buttons_action_row])


                            def check(button_ctx):
                                return button_ctx.author == ctx.author

                            try:
                                button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[guild_buttons_action_row], check=check)

                                if button_ctx.custom_id == "No":
                                    await button_ctx.send("No Oath Sent")
                                    return
                                
                                if button_ctx.custom_id == "Yes":
                                    await main.DM(ctx, owner, f"{ctx.author.mention}" + f" would like to join the Association {guild_name}" + f" React in server to join their Association" )
                                    await ctx.send(f"{owner.mention}" +f" will you swear the oath?".format(self), components=[guild_buttons_action_row])
                                    def check(button_ctx):
                                        return button_ctx.author == sworn

                                    try:
                                        button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[guild_buttons_action_row], check=check)

                                        if button_ctx.custom_id == "No":
                                            await button_ctx.send("Oath Request Denied")
                                            return
                                        
                                        if button_ctx.custom_id == "Yes":
                                            try:
                                                sword_list = []
                                                for sword in guildsearch['SWORDS']:
                                                    sword_list.append(sword)
                                                newvalue = {'$set': {'SWORN': str(owner)}}
                                                nextresponse = db.addGuildSworn(guild_query, newvalue, str(ctx.author), str(owner))
                                                await ctx.send(nextresponse)
                                                shield = db.updateGuild(guild_query, {'$set' : {'SHIELD' : str(owner) }})
                                                newvalue = {'$set': {'SHIELD': str(owner)}}
                                                response = db.addGuildShield(guild_query, newvalue, str(ctx.author), str(owner))
                                                await ctx.send(response)
                                                if sworn_team['TNAME'] not in sword_list:
                                                    newvalue = {'$push': {'SWORDS': str(sworn_team['TNAME'])}}
                                                    swordaddition2 = db.addGuildSword(guild_query, newvalue, str(ctx.author), str(sworn_team['TNAME']))
                                                    await ctx.send(swordaddition2)
                                                gbank = db.updateGuild(guild_query,{'$inc' : {'BANK' : investment }})
                                                s_new_bal = sbal - cost
                                                new_value = {'$set' : {'BANK' : s_new_bal}}
                                                steambal = db.updateTeam(steam_query, new_value)                      
                                            except:
                                                await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=3)
                                    except:
                                        print("Association creation ended unexpectedly. ")
                            except:
                                print("Association creation ended unexpectedly. ")                    
            else:
                sworn_profile = db.queryUser({'DISNAME': str(owner)})
                investment = cost * 2
                if founder_profile['GUILD'] != 'PCG' and founder_profile['GUILD'] != 'N/A' and founder_profile['GUILD'] != founder_profile['DISNAME'] :
                    await ctx.send(m.USER_IN_GUILD, delete_after=3)
                    return
                elif sworn_profile['GUILD'] != 'PCG' and sworn_profile['GUILD'] != 'N/A':
                    await ctx.send(m.USER_IN_GUILD, delete_after=3)
                    return
                else:
                    if founder_profile['TEAM'] == 'PCG' or sworn_profile['TEAM'] == 'PCG':
                        await ctx.send(m.FOUNDER_NO_TEAM, delete_after=3)
                        return
                    else:
                        fteam_query = {'TNAME' : founder_profile['TEAM']}
                        steam_query = {'TNAME' : sworn_profile['TEAM']}
                        founder_team = db.queryTeam(fteam_query)
                        sworn_team = db.queryTeam(steam_query)
                        fbal = founder_team['BANK']
                        sbal = sworn_team['BANK']
                        if founder_team['TNAME'] == sworn_team['TNAME']:
                            await ctx.send(m.SAME_TEAM, delete_after=3)
                            return
                        if fbal < cost or sbal < cost:
                            await ctx.send(m.BROKE_TEAM, delete_after=3)
                            return
                                        
                        guild_query = {'FOUNDER': str(ctx.author)}
                        guild_buttons = [
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
                        guild_buttons_action_row = manage_components.create_actionrow(*guild_buttons)
                        await ctx.send(f"Do you wish to swear an oath with {owner.mention}?".format(self), components=[guild_buttons_action_row])


                        def check(button_ctx):
                            return button_ctx.author == ctx.author

                        try:
                            button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[guild_buttons_action_row], check=check)

                            if button_ctx.custom_id == "No":
                                await button_ctx.send("No Oath Sent")
                                return
                            
                            if button_ctx.custom_id == "Yes":
                                await main.DM(ctx, owner, f"{ctx.author.mention}" + f" would like to join the Association {guild_name}" + f" React in server to join their Association" )
                                await ctx.send(f"{owner.mention}" +f" will you swear the oath?".format(self), components=[guild_buttons_action_row])
                                def check(button_ctx):
                                    return button_ctx.author == owner

                                try:
                                    button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[guild_buttons_action_row], check=check)

                                    if button_ctx.custom_id == "No":
                                        await button_ctx.send("Oath Request Denied")
                                        return
                                    
                                    if button_ctx.custom_id == "Yes":
                                        try:
                                            response = db.createGuild(data.newGuild(guild_query), str(ctx.author), str(guild_name))
                                            await ctx.send(response)
                                            nameguild = db.updateGuild(guild_query,{'$set' : {'GNAME' : str(guild_name)}})
                                            newvalue = {'$set': {'SWORN': str(owner)}}
                                            nextresponse = db.addGuildSworn(guild_query, newvalue, str(ctx.author), str(owner))
                                            await ctx.send(nextresponse)
                                            shield = db.updateGuild(guild_query, {'$set' : {'SHIELD' : str(owner) }})
                                            newvalue = {'$set': {'SHIELD': str(owner)}}
                                            response = db.addGuildShield(guild_query, newvalue, str(ctx.author), str(owner))
                                            await ctx.send(response)
                                            newvalue = {'$push': {'SWORDS': str(founder_team['TNAME'])}}
                                            swordaddition = db.addGuildSword(guild_query, newvalue, str(ctx.author), str(founder_team['TNAME']))
                                            await ctx.send(swordaddition)
                                            newvalue = {'$push': {'SWORDS': str(sworn_team['TNAME'])}}
                                            swordaddition2 = db.addGuildSword(guild_query, newvalue, str(ctx.author), str(sworn_team['TNAME']))
                                            await ctx.send(swordaddition2)
                                            gbank = db.updateGuild(guild_query,{'$set' : {'BANK' : investment }})
                                            new_bal = fbal - cost
                                            new_value = {'$set' : {'BANK' : new_bal}}
                                            fteambal = db.updateTeam(fteam_query, new_value)
                                            s_new_bal = sbal - cost
                                            new_value = {'$set' : {'BANK' : s_new_bal}}
                                            steambal = db.updateTeam(steam_query, new_value)                    
                                        except:
                                            await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=3)
                                except:
                                    print("Association creation ended unexpectedly. ")
                        except:
                            print("Association creation ended unexpectedly. ")   
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
            await ctx.send(
                "There's an issue with your Oath. Alert support.")
            return
            
                   

    @cog_ext.cog_slash(description="Betray your Association (Association Sworn)", guild_ids=main.guild_ids)
    async def betray(self, sctx, founder: User):
        sworn_profile = db.queryUser({'DID': str(ctx.author.id)})
        founder_profile = db.queryUser({'DISNAME': str(founder)})
        if sworn_profile['GUILD'] != founder_profile['GUILD']:
            await ctx.send(m.GUILD_DOESNT_EXIST, delete_after=5)
            return
        guild_query = {'FOUNDER': str(founder)}
        guild_profile = db.queryGuild(guild_query)
        guild_bank = guild_profile['BANK']
        team_name = sworn_profile['TEAM']
        
        warchest = guild_bank
        
        if guild_profile:
            if sworn_profile['DISNAME'] == guild_profile['SWORN']:
                trade_buttons = [
                    manage_components.create_button(
                        style=ButtonStyle.red,
                        label="Betray Association",
                        custom_id="yes"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.blue,
                        label="No",
                        custom_id="no"
                    )
                ]
                trade_buttons_action_row = manage_components.create_actionrow(*trade_buttons)
                await ctx.send(f"Will you renounce your Oath?".format(self), components=[trade_buttons_action_row])
                
                def check(button_ctx):
                    return button_ctx.author == ctx.author

                
                try:
                    button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[trade_buttons_action_row], timeout=120, check=check)
                    if button_ctx.custom_id == "no":
                        await button_ctx.send("No Change")
                        self.stop = True
                        return
                    if button_ctx.custom_id == "yes":
                        newvalue = {'$pull': {'SWORDS': str(team_name)}}
                        response2 = db.deleteGuildSword(guild_query, newvalue, str(ctx.author), str(team_name))
                        await ctx.send(response2)
                        new_value_query = {'$set': {'SWORN': 'BETRAYED', 'SHIELD' : str(founder)}}
                        response = db.deleteGuildSworn(guild_query, new_value_query, str(founder), str(ctx.author))
                        await ctx.send(response)                  
                    
                except:
                    print("No Betrayal")
            else:
                await ctx.send(m.OWNER_ONLY_COMMAND, delete_after=5)
        else:
            await ctx.send(m.GUILD_DOESNT_EXIST, delete_after=5)

    @cog_ext.cog_slash(description="Ask Guild Owner to join Association! (Association Owner)", guild_ids=main.guild_ids)
    async def ally(self, ctx, owner: User):
        founder_profile = db.queryUser({'DID': str(ctx.author.id)})
        guildname = founder_profile['GUILD']
        sword_profile = db.queryUser({'DISNAME': str(owner)})
        team_profile = db.queryTeam({'TNAME': sword_profile['TEAM']})
        if not team_profile:
            await ctx.send(f"{owner.mention} does not own a Guild")
        team_name = team_profile['TNAME']
        team_owner = team_profile['OWNER']
        if founder_profile['GUILD'] == 'PCG':
            await ctx.send(m.USER_NOT_IN_GUILD, delete_after=3)
        elif team_profile['GUILD'] != 'PCG':
            await ctx.send(m.USER_IN_GUILD, delete_after=3)
        elif sword_profile['DISNAME'] != team_owner:
            await ctx.send(m.SWORD_NO_TEAM, delete_after=3)
        else:
            guild_query = {'GNAME': str(guildname)}
            guild = db.queryGuildAlt(guild_query)
            new_query = {'FOUNDER' : guild['FOUNDER']}
            f_profile = guild['FOUNDER']
            s_profile = guild['SWORN']
            guild_name = guildname
            if founder_profile['DISNAME'] != f_profile and founder_profile['DISNAME'] != s_profile:
                await ctx.send(m.ENLIST_GUILD_FOUNDER, delete_after=3)
                return
            trade_buttons = [
                manage_components.create_button(
                    style=ButtonStyle.green,
                    label="Ally",
                    custom_id="yes"
                ),
                manage_components.create_button(
                    style=ButtonStyle.blue,
                    label="No",
                    custom_id="no"
                )
            ]
            trade_buttons_action_row = manage_components.create_actionrow(*trade_buttons)
            await ctx.send(f"Do you want to ally with {team_name}?".format(self), components=[trade_buttons_action_row])
            
            def check(button_ctx):
                return button_ctx.author == ctx.author

            
            try:
                button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[trade_buttons_action_row], timeout=120, check=check)
                if button_ctx.custom_id == "no":
                    await button_ctx.send("No Change")
                    self.stop = True
                    return
                if button_ctx.custom_id == "yes":
                    await main.DM(ctx, owner, f"{ctx.author.mention}" + f" would like to ally with your team!" + f" React in server to join their Association" )
                    trade_buttons = [
                        manage_components.create_button(
                            style=ButtonStyle.green,
                            label="Form Alliance",
                            custom_id="yes"
                        ),
                        manage_components.create_button(
                            style=ButtonStyle.blue,
                            label="No",
                            custom_id="no"
                        )
                    ]
                    trade_buttons_action_row = manage_components.create_actionrow(*trade_buttons)
                    await ctx.send(f"{owner.mention}" +f" will you join {guild_name}?".format(self), components=[trade_buttons_action_row])
                    
                    def check(button_ctx):
                        return button_ctx.author == owner

                    
                    try:
                        button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[trade_buttons_action_row], timeout=120, check=check)
                        if button_ctx.custom_id == "no":
                            await button_ctx.send("No Change")
                            self.stop = True
                            return
                        if button_ctx.custom_id == "yes":
                            newvalue = {'$push': {'SWORDS': str(team_name)}}
                            response = db.addGuildSword(new_query, newvalue, str(ctx.author), str(team_name))
                            await ctx.send(response)
                    
                    except:
                        await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=3)
            except:
                print("No proposal Sent") 
                
    @cog_ext.cog_slash(description="Knight your Association Shield! (Association Owner)", guild_ids=main.guild_ids)
    async def knight(self, ctx, blade: User):
        founder_profile = db.queryUser({'DID': str(ctx.author.id)})
        shield_profile = db.queryUser({'DISNAME' : str(blade)})
        if not shield_profile:
            await ctx.send(m.USER_NOT_REGISTERED)
        shield_team_name = shield_profile['TEAM']
        if shield_team_name == 'PCG':
            await ctx.send(m.KNIGHT_NOT_TEAM, delete_after=3)
            return
        shield_team = db.queryTeam({'TNAME' : str(shield_team_name)})
        if shield_team['GUILD'] != founder_profile['GUILD']:
            await ctx.send(m.KNIGHT_NOT_TEAM, delete_after=3)
            return
        guildname = founder_profile['GUILD']
        if founder_profile['GUILD'] == 'PCG':
            await ctx.send(m.USER_NOT_IN_GUILD, delete_after=3)
            return
        guild_query = {'GNAME': str(guildname)}
        guild = db.queryGuildAlt(guild_query)
        guild_name = guild['GNAME']
        new_query = {'FOUNDER' : guild['FOUNDER']}
        f_profile = guild['FOUNDER']
        s_profile = guild['SWORN']
        if founder_profile['DISNAME'] != f_profile and founder_profile['DISNAME'] != s_profile:
            await ctx.send(m.KNIGHT_GUILD_FOUNDER, delete_after=3)
            return
        trade_buttons = [
            manage_components.create_button(
                style=ButtonStyle.green,
                label="Knight",
                custom_id="yes"
            ),
            manage_components.create_button(
                style=ButtonStyle.blue,
                label="No",
                custom_id="no"
            )
        ]
        trade_buttons_action_row = manage_components.create_actionrow(*trade_buttons)
        await ctx.send(f"Do you wish to knight {blade.mention}?".format(self), components=[trade_buttons_action_row])
        
        def check(button_ctx):
            return button_ctx.author == ctx.author

        
        try:
            button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[trade_buttons_action_row], timeout=120, check=check)
            if button_ctx.custom_id == "no":
                await button_ctx.send("No Change")
                self.stop = True
                return
            if button_ctx.custom_id == "yes":
                try: 
                    await main.DM(ctx, blade, f"{ctx.author.mention}" + f" would like you to serve as the Association Shield!" + f" React in server to protect the Association" )
                    trade_buttons = [
                        manage_components.create_button(
                            style=ButtonStyle.green,
                            label="Serve",
                            custom_id="yes"
                        ),
                        manage_components.create_button(
                            style=ButtonStyle.blue,
                            label="No",
                            custom_id="no"
                        )
                    ]
                    trade_buttons_action_row = manage_components.create_actionrow(*trade_buttons)
                    await ctx.send(f"{blade.mention}" +f" will you defend {guild_name}?".format(self), components=[trade_buttons_action_row])
                    
                    def check(button_ctx):
                        return button_ctx.author == blade

                    
                    try:
                        button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[trade_buttons_action_row], timeout=120, check=check)
                        if button_ctx.custom_id == "no":
                            await button_ctx.send("Knight Refused")
                            self.stop = True
                            return
                        if button_ctx.custom_id == "yes":
                            newvalue = {'$set': {'SHIELD': str(blade), 'STREAK' : 0}}
                            response = db.addGuildShield(new_query, newvalue, str(ctx.author), str(blade))
                            await ctx.send(response)
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
                    await ctx.send(
                        "There's an issue with your commnads. Alert support.")
                    return
        except:
            print("No proposal Sent")
        
    @cog_ext.cog_slash(description="Exile Guild from Association (Association Owner)", guild_ids=main.guild_ids)
    async def exile(self, ctx, owner: User):
        leader_profile = db.queryUser({'DID': str(ctx.author.id)})
        exiled_profile = db.queryUser({'DISNAME': str(owner)})
        if not exiled_profile:
            await ctx.send(m.USER_DOESNT_EXIST, delete_after=5)
            return
        exiled_team = db.queryTeam({'TNAME' : exiled_profile['TEAM']})
        if leader_profile['GUILD'] != exiled_team['GUILD']:
            await ctx.send(m.GUILD_DOESNT_EXIST, delete_after=5)
            return
        guild_query = {'GNAME': leader_profile['GUILD']}
        guild_profile = db.queryGuildAlt(guild_query)
        new_query = {'FOUNDER' : guild_profile['FOUNDER']}
        
        if guild_profile:
            if leader_profile['DISNAME'] == guild_profile['FOUNDER'] or leader_profile['DISNAME'] == guild_profile['SWORN']:
                accept = await ctx.send(f"".format(self), delete_after=8)
                trade_buttons = [
                    manage_components.create_button(
                        style=ButtonStyle.red,
                        label="Exile Guild",
                        custom_id="yes"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.blue,
                        label="No",
                        custom_id="no"
                    )
                ]
                trade_buttons_action_row = manage_components.create_actionrow(*trade_buttons)
                await ctx.send(f"Do you wish to Exile {owner.mention} and {exiled_profile['TEAM']}?".format(self), components=[trade_buttons_action_row])
                
                def check(button_ctx):
                    return button_ctx.author == ctx.author

                
                try:
                    button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[trade_buttons_action_row], timeout=120, check=check)
                    if button_ctx.custom_id == "no":
                        await button_ctx.send("No Change")
                        self.stop = True
                        return
                    if button_ctx.custom_id == "yes":
                        new_value_query = {'$pull': {'SWORDS': str(exiled_profile['TEAM'])}, '$set': {'SHIELD': guild_profile['SWORN']}}
                        response2 = db.deleteGuildSword(new_query, new_value_query, str(ctx.author), str(exiled_profile['TEAM']))
                        await ctx.send(response2)
                except:
                    print("No Exile")
            else:
                await ctx.send(m.EXILE_GUILD_FOUNDER, delete_after=5)
        else:
            await ctx.send(m.GUILD_DOESNT_EXIST, delete_after=5)

    @cog_ext.cog_slash(description="Abandon Association (Guild Owner)", guild_ids=main.guild_ids)
    async def renounce(self, ctx):
        sword_profile = db.queryUser({'DID': str(ctx.author.id)})
        team_profile = db.queryTeam({'TNAME' : sword_profile['TEAM']})
        if sword_profile['DISNAME'] != team_profile['OWNER'] or sword_profile['TEAM'] == 'PCG':
            await ctx.send(m.OWNER_ONLY_COMMAND, delete_after=5)
            return
        team_name = team_profile['TNAME']
        guild_query = {'GNAME': team_profile['GUILD']}
        guild_profile = db.queryGuildAlt(guild_query)  
        if guild_profile:
            if sword_profile['DISNAME'] == guild_profile['SWORN']:
                await ctx.send(m.SWORD_LEAVE, delete_after=5)
                return      
            trade_buttons = [
                manage_components.create_button(
                    style=ButtonStyle.red,
                    label="Renounce Oath",
                    custom_id="yes"
                ),
                manage_components.create_button(
                    style=ButtonStyle.blue,
                    label="No",
                    custom_id="no"
                )
            ]
            trade_buttons_action_row = manage_components.create_actionrow(*trade_buttons)
            await ctx.send(f"Do you wish to renounce your allegiance to {guild_profile['GNAME']}?".format(self), components=[trade_buttons_action_row])
            
            def check(button_ctx):
                return button_ctx.author == ctx.author

            
            try:
                button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[trade_buttons_action_row], timeout=120, check=check)
                if button_ctx.custom_id == "no":
                    await button_ctx.send("No Change")
                    self.stop = True
                    return
                if button_ctx.custom_id == "yes":
                    try:
                        new_value_query = {'$pull': {'SWORDS': str(team_name)}, '$set': {'SHIELD': guild_profile['SWORN']}}
                        response = db.deleteGuildSwordAlt(guild_query, new_value_query, str(team_name))
                        await ctx.send(response)
                    except:
                        print("Association not created. ")
            except:
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
        else:
            await ctx.send(m.GUILD_DOESNT_EXIST, delete_after=5)

    @cog_ext.cog_slash(description="Disband your Association (Association Founder)", guild_ids=main.guild_ids)
    async def disband(self, ctx):
        guild_query = {'FOUNDER': str(ctx.author)}
        guild = db.queryGuild(guild_query)
        if guild:
            if guild['FOUNDER'] == str(ctx.author):
                trade_buttons = [
                    manage_components.create_button(
                        style=ButtonStyle.red,
                        label="Disband Assosiation",
                        custom_id="yes"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.blue,
                        label="No",
                        custom_id="no"
                    )
                ]
                trade_buttons_action_row = manage_components.create_actionrow(*trade_buttons)
                await ctx.send(f"Do you want to disband the {guild['GNAME']}?".format(self), components=[trade_buttons_action_row])
                
                def check(button_ctx):
                    return button_ctx.author == ctx.author

                
                try:
                    button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[trade_buttons_action_row], timeout=120, check=check)
                    if button_ctx.custom_id == "no":
                        await button_ctx.send("Association not Disbanded")
                        self.stop = True
                        return
                    if button_ctx.custom_id == "yes":
                        try:
                            response = db.deleteGuild(guild, str(ctx.author))

                            user_query = {'DID': str(ctx.author.id)}
                            new_value = {'$set': {'GUILD': 'PCG'}}
                            db.updateUserNoFilter(user_query, new_value)

                            await ctx.send(response)
                        
                        except:
                            print("Association Not Deleted. ")
                except:
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
            else:
                await ctx.send("Only the Founder can disband the Association. ")
        else:
            await ctx.send(m.TEAM_DOESNT_EXIST, delete_after=5)




def setup(bot):
    bot.add_cog(Guild(bot))