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

class Guild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Guild Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)


    @cog_ext.cog_slash(description="Swear into Guild!", guild_ids=main.guild_ids)
    async def oath(self, ctx, user1: User, name: str):
        guild_name = name
        cost = 10000
        founder_profile = db.queryUser({'DISNAME': str(ctx.author)})
        guildsearch_name = founder_profile['GUILD']
        if guildsearch_name != "PCG":
            guildsearch_query = {'GNAME' : guildsearch_name}
            guildsearch = db.queryGuildAlt(guildsearch_query)
            if guildsearch:
                if guild_name != guildsearch_name:
                    await ctx.send(m.FOUNDER_LEAVE)
                    return
                await ctx.send(f"{guildsearch_name} NEW OATH!")
                sworn_profile = db.queryUser({'DISNAME': str(user1)})              
                if sworn_profile['GUILD'] != 'PCG' and sworn_profile['GUILD'] != 'N/A':
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
                        accept = await ctx.send(f"Do you wish to swear an oath with {user1.mention}?".format(self), delete_after=10)
                        for emoji in emojis:
                            await accept.add_reaction(emoji)

                        def check(reaction, user):
                            return user == ctx.author and str(reaction.emoji) == '👍'

                        try:
                            confirmed1 = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                            await main.DM(ctx, user1, f"{ctx.author.mention}" + f" would like to join the Guild {guild_name}" + f" React in server to join their Guild" )
                            accept = await ctx.send(f"{user1.mention}" +f" will you swear the oath?".format(self), delete_after=10)
                            for emoji in emojis:
                                await accept.add_reaction(emoji)

                            def check(reaction, partner):
                                return partner == user1 and str(reaction.emoji) == '👍'

                            try:
                                sword_list = []
                                for sword in guildsearch['SWORDS']:
                                    sword_list.append(sword)
                                newvalue = {'$set': {'SWORN': str(user1)}}
                                nextresponse = db.addGuildSworn(guild_query, newvalue, str(ctx.author), str(user1))
                                await ctx.send(nextresponse)
                                shield = db.updateGuild(guild_query, {'$set' : {'SHIELD' : str(user1) }})
                                newvalue = {'$set': {'SHIELD': str(user1)}}
                                response = db.addGuildShield(guild_query, newvalue, str(ctx.author), str(user1))
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
                            print("No Oath Sent")                           
        else:
            sworn_profile = db.queryUser({'DISNAME': str(user1)})
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
                    accept = await ctx.send(f"Do you wish to swear an oath with {user1.mention}?".format(self), delete_after=10)
                    for emoji in emojis:
                        await accept.add_reaction(emoji)

                    def check(reaction, user):
                        return user == ctx.author and str(reaction.emoji) == '👍'

                    try:
                        confirmed1 = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                        await main.DM(ctx, user1, f"{ctx.author.mention}" + f" would like to form the Guild {guild_name}" + f" React in server to join their Guild" )
                        accept = await ctx.send(f"{user1.mention}" +f" will you swear the oath?".format(self), delete_after=10)
                        for emoji in emojis:
                            await accept.add_reaction(emoji)

                        def check(reaction, partner):
                            return partner == user1 and str(reaction.emoji) == '👍'

                        try:
                            confirmed2 = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                            response = db.createGuild(data.newGuild(guild_query), str(ctx.author), str(guild_name))
                            await ctx.send(response)
                            nameguild = db.updateGuild(guild_query,{'$set' : {'GNAME' : str(guild_name)}})
                            newvalue = {'$set': {'SWORN': str(user1)}}
                            nextresponse = db.addGuildSworn(guild_query, newvalue, str(ctx.author), str(user1))
                            await ctx.send(nextresponse)
                            shield = db.updateGuild(guild_query, {'$set' : {'SHIELD' : str(user1) }})
                            newvalue = {'$set': {'SHIELD': str(user1)}}
                            response = db.addGuildShield(guild_query, newvalue, str(ctx.author), str(user1))
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
                        print("No oath Sent") 

    @cog_ext.cog_slash(description="Betray your Guild (Guild Sworn)", guild_ids=main.guild_ids)
    async def betray(self, ctx, user1: User):
        sworn_profile = db.queryUser({'DISNAME': str(ctx.author)})
        founder_profile = db.queryUser({'DISNAME': str(user1)})
        if sworn_profile['GUILD'] != founder_profile['GUILD']:
            await ctx.send(m.GUILD_DOESNT_EXIST, delete_after=5)
            return
        guild_query = {'FOUNDER': str(user1)}
        guild_profile = db.queryGuild(guild_query)
        guild_bank = guild_profile['BANK']
        team_name = sworn_profile['TEAM']
        
        warchest = guild_bank
        
        if guild_profile:
            if sworn_profile['DISNAME'] == guild_profile['SWORN']:
                accept = await ctx.send(f"Will you renounce your Oath?", delete_after=8)
                for emoji in emojis:
                    await accept.add_reaction(emoji)

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) == '👍'

                try:
                    confirmed2 = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                    newvalue = {'$pull': {'SWORDS': str(team_name)}}
                    response2 = db.deleteGuildSword(guild_query, newvalue, str(ctx.author), str(team_name))
                    await ctx.send(response2)
                    new_value_query = {'$set': {'SWORN': 'BETRAYED' }}
                    response = db.deleteGuildSworn(guild_query, new_value_query, str(user1), str(ctx.author))
                    await ctx.send(response)                  
                    
                except:
                    print("No Betrayal")
            else:
                await ctx.send(m.OWNER_ONLY_COMMAND, delete_after=5)
        else:
            await ctx.send(m.GUILD_DOESNT_EXIST, delete_after=5)

    @cog_ext.cog_slash(description="Ask Team Owner to join Guild! (Guild Owner)", guild_ids=main.guild_ids)
    async def ally(self, ctx, user1: User):
        founder_profile = db.queryUser({'DISNAME': str(ctx.author)})
        guildname = founder_profile['GUILD']
        sword_profile = db.queryUser({'DISNAME': str(user1)})
        team_profile = db.queryTeam({'TNAME': sword_profile['TEAM']})
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
            accept = await ctx.send(f"Do you want to ally with {team_name}?", delete_after=10)
            for emoji in emojis:
                await accept.add_reaction(emoji)

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) == '👍'

            try:
                confirmed1 = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                await main.DM(ctx, user1, f"{ctx.author.mention}" + f" would like to ally with your team!" + f" React in server to join their Guild" )
                accept = await ctx.send(f"{user1.mention}" +f" will you join {guild_name}?".format(self), delete_after=10)
                for emoji in emojis:
                    await accept.add_reaction(emoji)

                def check(reaction, kid):
                    return kid == user1 and str(reaction.emoji) == '👍'

                try:
                    confirmed2 = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                    newvalue = {'$push': {'SWORDS': str(team_name)}}
                    response = db.addGuildSword(new_query, newvalue, str(ctx.author), str(team_name))
                    await ctx.send(response)
                    
                except:
                    await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=3)
            except:
                print("No proposal Sent") 
                
    @cog_ext.cog_slash(description="Knight your Guild Shield! (Guild Owner)", guild_ids=main.guild_ids)
    async def knight(self, ctx, user1: User):
        founder_profile = db.queryUser({'DISNAME': str(ctx.author)})
        shield_profile = db.queryUser({'DISNAME' : str(user1)})
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
        accept = await ctx.send(f"Do you wish to knight {user1.mention}?".format(self), delete_after=10)
        for emoji in emojis:
            await accept.add_reaction(emoji)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '👍'

        try:
            confirmed1 = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
            await main.DM(ctx, user1, f"{ctx.author.mention}" + f" would like you to serve as the Guild Shield!" + f" React in server to protect the Guild" )
            accept = await ctx.send(f"{user1.mention}" +f" will you defend {guild_name}?".format(self), delete_after=10)
            for emoji in emojis:
                await accept.add_reaction(emoji)

            def check(reaction, kid):
                return kid == user1 and str(reaction.emoji) == '👍'

            try:
                confirmed2 = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                newvalue = {'$set': {'SHIELD': str(user1), 'STREAK' : 0}}
                response = db.addGuildShield(new_query, newvalue, str(ctx.author), str(user1))
                await ctx.send(response)
                
            except:
                await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=3)
        except:
            print("No proposal Sent")
        
    @cog_ext.cog_slash(description="Exile Team from Guild (Guild Owner)", guild_ids=main.guild_ids)
    async def exile(self, ctx, user1: User):
        leader_profile = db.queryUser({'DISNAME': str(ctx.author)})
        exiled_profile = db.queryUser({'DISNAME': str(user1)})
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
                accept = await ctx.send(f"Do you wish to Exile {user1.mention} and {exiled_profile['TEAM']}?".format(self), delete_after=8)
                for emoji in emojis:
                    await accept.add_reaction(emoji)

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) == '👍'

                try:
                    confirmed = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                    new_value_query = {'$pull': {'SWORDS': str(exiled_profile['TEAM'])}}
                    response2 = db.deleteGuildSword(new_query, new_value_query, str(ctx.author), str(exiled_profile['TEAM']))
                    await ctx.send(response2)
                except:
                    print("No Exile")
            else:
                await ctx.send(m.EXILE_GUILD_FOUNDER, delete_after=5)
        else:
            await ctx.send(m.GUILD_DOESNT_EXIST, delete_after=5)

    @cog_ext.cog_slash(description="Abandon Guild (Team Owner)", guild_ids=main.guild_ids)
    async def renounce(self, ctx):
        sword_profile = db.queryUser({'DISNAME': str(ctx.author)})
        team_profile = db.queryTeam({'TNAME' : sword_profile['TEAM']})
        if sword_profile['DISNAME'] != team_profile['OWNER'] or sword_profile['TEAM'] == 'PCG':
            await ctx.send(m.OWNER_ONLY_COMMAND, delete_after=5)
            return
        team_name = team_profile['TNAME']
        guild_query = {'GNAME': team_profile['GUILD']}
        guild_profile = db.queryGuildAlt(guild_query)
        if sword_profile['DISNAME'] == guild_profile['SWORN']:
            await ctx.send(m.SWORD_LEAVE, delete_after=5)
            return        
        if guild_profile:

                    accept = await ctx.send(f"Do you wish to renounce your allegiance to {guild_profile['GNAME']}?".format(self), delete_after=8)
                    for emoji in emojis:
                        await accept.add_reaction(emoji)

                    def check(reaction, user):
                        return user == ctx.author and str(reaction.emoji) == '👍'

                    try:
                        confirmed = await self.bot.wait_for('reaction_add', timeout=5.0, check=check)
                        new_value_query = {'$pull': {'SWORDS': str(team_name)}}
                        response = db.deleteGuildSwordAlt(guild_query, new_value_query, str(team_name))
                        await ctx.send(response)
                    except:
                        print("Team not created. ")

        else:
            await ctx.send(m.GUILD_DOESNT_EXIST, delete_after=5)

    @cog_ext.cog_slash(description="Disband your Guild (Guild Founder)", guild_ids=main.guild_ids)
    async def disband(self, ctx):
        guild_query = {'FOUNDER': str(ctx.author)}
        guild = db.queryGuild(guild_query)
        if guild:
            if guild['FOUNDER'] == str(ctx.author):
                accept = await ctx.send(f"Do you want to disband the {guild['GNAME']}?".format(self), delete_after=10)
                for emoji in emojis:
                    await accept.add_reaction(emoji)

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) == '👍'

                try:
                    confirmed = await self.bot.wait_for('reaction_add', timeout=8.0, check=check)
                    response = db.deleteGuild(guild, str(ctx.author))

                    user_query = {'DISNAME': str(ctx.author)}
                    new_value = {'$set': {'GUILD': 'PCG'}}
                    db.updateUserNoFilter(user_query, new_value)

                    await ctx.send(response)
                except:
                    print("Guild Not Deleted. ")
            else:
                await ctx.send("Only the Founder can disband the Guild. ")
        else:
            await ctx.send(m.TEAM_DOESNT_EXIST, delete_after=5)




def setup(bot):
    bot.add_cog(Guild(bot))