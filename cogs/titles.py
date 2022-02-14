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
from discord_slash import cog_ext, SlashContext
from discord_slash import SlashCommand
from discord_slash.utils import manage_components
from discord_slash.model import ButtonStyle
from .crownunlimited import enhancer_mapping, title_enhancer_mapping, enhancer_suffix_mapping, title_enhancer_suffix_mapping

class Titles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print('Titles Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @cog_ext.cog_slash(description="Equip a Title", guild_ids=main.guild_ids)
    async def equiptitle(self, ctx, title: str):
        title_name = title
        user_query = {'DID': str(ctx.author.id)}
        user = db.queryUser(user_query)

        vault_query = {'OWNER' : str(ctx.author)}
        vault = db.altQueryVault(vault_query)

        resp = db.queryTitle({'TITLE': {"$regex": f"^{str(title_name)}$", "$options": "i"}})
        title_name = resp['TITLE']

        if resp:

            if title_name in vault['TITLES']:
                response = db.updateUserNoFilter(user_query, {'$set': {'TITLE': title_name}})
                await ctx.send(response)
            else:
                await ctx.send(m.USER_DOESNT_HAVE_THE_Title, hidden=True)
        else:

            if title_name in vault['TITLES']:
                response = db.updateUserNoFilter(user_query, {'$set': {'TITLE': str(title_name)}})
                await ctx.send(response)
            else:
                await ctx.send(m.USER_DOESNT_HAVE_THE_Title, hidden=True)


    @cog_ext.cog_slash(description="View a Title", guild_ids=main.guild_ids)
    async def viewtitle(self, ctx, title: str):
        title_name = title
        title = db.queryTitle({'TITLE': {"$regex": f"^{str(title)}$", "$options": "i"}})
        if title:
            title_title = title['TITLE']
            title_show = title['UNIVERSE']
            title_price = title['PRICE']
            exclusive = title['EXCLUSIVE']

            if title_show != 'Unbound':
                title_img = db.queryUniverse({'TITLE': title_show})['PATH']
            title_passive = title['ABILITIES'][0]
                # Title Passive
            o_title_passive_type = list(title_passive.keys())[0]
            o_title_passive_value = list(title_passive.values())[0]
            
            message=""

            price_message ="" 
            if exclusive:
                price_message = "_Priceless_"
            else:
                price_message = f"_Shop & Drop_"
            typetext = " "
            type2 = " "
            if o_title_passive_type == 'ATK':
                typetext = "Attack"
                message=f"{title_title} is an ATK title"
            elif o_title_passive_type == 'DEF':
                typetext = "Defense"
                message=f"{title_title} is a DEF title"
            elif o_title_passive_type == 'STAM':
                typetext = "Stamina"
                message=f"{title_title} is a STAM title"
            elif o_title_passive_type == 'HLT':
                typetext = "Health"
                message=f"{title_title} is a HLT title"
            elif o_title_passive_type == 'LIFE':
                typetext = "Health"
                message=f"{title_title} is a LIFE title"
            elif o_title_passive_type == 'DRAIN':
                typetext = "Stamina"
                message=f"{title_title} is a DRAIN title"
            elif o_title_passive_type == 'FLOG':
                typetext = "Attack"
                message=f"{title_title} is a FLOG title"
            elif o_title_passive_type == 'WITHER':
                typetext = "Defense"
                message=f"{title_title} is a WITHER title"
            elif o_title_passive_type == 'RAGE':
                typetext = "Defense gain Attack"
                message=f"{title_title} is a RAGE title"
            elif o_title_passive_type == 'BRACE':    
                typetext = "Attack gain Defense"        
                message=f"{title_title} is a BRACE title"
            elif o_title_passive_type == 'BZRK':    
                typetext = "Health gain Attack"        
                message=f"{title_title} is a BZRK title"
            elif o_title_passive_type == 'CRYSTAL':    
                typetext = "Health gain Defense"        
                message=f"{title_title} is a CRYSTAL title"
            elif o_title_passive_type == 'GROWTH':    
                typetext = "Max Health gain Attack and Defense"        
                message=f"{title_title} is a GROWTH title"
            elif o_title_passive_type == 'STANCE':
                typetext = "Attack and Defense increase"
                message=f"{title_title} is a STANCE title"
            elif o_title_passive_type == 'CONFUSE':
                typetext = "Opponent Attack And Defense decrease Opponent"
                message=f"{title_title} is a CONFUSE title"
            elif o_title_passive_type == 'BLINK':
                typetext = "Decrease Stamina"
                type2 ="Increase Target/Ally Stamina"
                message=f"{title_title} is a BLINK title"
            elif o_title_passive_type == 'SLOW':
                typetext = "Increase Opponent Stamina"
                type2 = "Decrease Stamina"
                message=f"{title_title} is a SLOW title"
            elif o_title_passive_type == 'HASTE':
                typetext = "Increase Stamina by"
                type2 = "Decrease Opponent Stamina"
                message=f"{title_title} is a HASTE title" 
            elif o_title_passive_type == 'SOULCHAIN':
                typetext = "Stamina"
                message=f"{title_title} is a SOULCHAIN title"
            elif o_title_passive_type == 'FEAR':
                typetext = "Max Health reduce Opponent Attack and Defense"
                message=f"{title_title} is a FEAR title"
            elif o_title_passive_type == 'GAMBLE':
                typetext = "Health"
                message=f"{title_title} is a GAMBLE title" 

            embedVar = discord.Embed(title=f"{Crest_dict[title_show]} {title_title}\n{price_message}".format(self), colour=000000)
            if title_show != "Unbound":
                embedVar.set_thumbnail(url=title_img)
            if o_title_passive_type == "ATK" or o_title_passive_type == "DEF" or o_title_passive_type == "HLT" or o_title_passive_type == "STAM":
                embedVar.add_field(name=f"**Unique Passive**", value=f"Increases **{typetext}** by **{o_title_passive_value}{title_enhancer_suffix_mapping[o_title_passive_type]}**", inline=False)
            elif o_title_passive_type == "FLOG" or o_title_passive_type == "WITHER" or o_title_passive_type == "LIFE" or o_title_passive_type == "DRAIN":
                embedVar.add_field(name=f"**Unique Passive**", value=f"Steals **{o_title_passive_value}{title_enhancer_suffix_mapping[o_title_passive_type]} {typetext}**", inline=False)
            elif o_title_passive_type == "RAGE" or o_title_passive_type == "BRACE" or o_title_passive_type == "BZRK" or o_title_passive_type == "CRYSTAL" or o_title_passive_type == "GROWTH" or o_title_passive_type == "FEAR":
                embedVar.add_field(name=f"**Unique Passive**", value=f"Sacrifice **{o_title_passive_value}{title_enhancer_suffix_mapping[o_title_passive_type]} {typetext}**", inline=False)
            elif o_title_passive_type == "STANCE" or o_title_passive_type == "CONFUSE":
                embedVar.add_field(name=f"**Unique Passive**", value=f"Swap {typetext} Defense by **{o_title_passive_value}**", inline=False)
            elif o_title_passive_type == "BLINK":
                embedVar.add_field(name=f"**Unique Passive**", value=f"**{typetext}** by **{o_title_passive_value}**, **{type2}** by **{o_title_passive_value}**", inline=False)
            elif o_title_passive_type == "SLOW" or o_title_passive_type == "HASTE":
                embedVar.add_field(name=f"**Unique Passive**", value=f"**{typetext}** by **{o_title_passive_value}**, **{type2}** by **{o_title_passive_value}** then **Swap Stamina**", inline=False)
            elif o_title_passive_type == "SOULCHAIN" or o_title_passive_type == "GAMBLE":
                embedVar.add_field(name=f"**Unique Passive**", value=f"Set both players **{typetext}** equal to **{o_title_passive_value}**", inline=False)
            embedVar.set_footer(text=f"{o_title_passive_type}: {title_enhancer_mapping[o_title_passive_type]}")

            await ctx.send(embed=embedVar)

        else:
            await ctx.send("That title doesn't exist.", hidden=True)

def setup(bot):
    bot.add_cog(Titles(bot))
    
    
Crest_dict = {'Unbound': ':ideograph_advantage:',
              'My Hero Academia': ':sparkle:',
              'League Of Legends': ':u6307:',
              'Kanto Region': ':chart:',
              'Naruto': ':u7121:',
              'Bleach': ':u6709:',
              'God Of War': ':u7533:',
              'Chainsawman': ':accept:',
              'One Punch Man': ':u55b6:',
              'Johto Region': ':u6708:',
              'Black Clover': ':ophiuchus:',
              'Demon Slayer': ':aries:',
              'Attack On Titan': ':taurus:',
              '7ds': ':capricorn:',
              'Hoenn Region': ':leo:',
              'Digimon': ':cancer:',
              'Fate': ':u6e80:',
              'Solo Leveling': ':u5408:',
              'Souls': ':sos:',
              'Dragon Ball Z': ':u5272:',
              'Sinnoh Region': ':u7981:',
              'Death Note': ':white_flower:',
              'Crown Rift Awakening': ':u7a7a:',
              'Crown Rift Slayers': ':sa:',
              'Crown Rift Madness': ':m:',
              'Persona': ':o:'}
