from os import name
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

class Pet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print('Pet Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @cog_ext.cog_slash(description="Equip Summon", guild_ids=main.guild_ids)
    async def equipsummon(self, ctx, summon: str):
        pet_name = summon
        user_query = {'DISNAME': str(ctx.author)}
        user = db.queryUser(user_query)

        vault_query = {'OWNER' : str(ctx.author)}
        vault = db.altQueryVault(vault_query)

        selected_pet = ""

        for pet in vault['PETS']:
            if pet_name.upper() == pet['NAME'].upper():
                selected_pet = pet

        # Do not Check Tourney wins
        if selected_pet:
            response = db.updateUserNoFilter(user_query, {'$set': {'PET': str(selected_pet['NAME'])}})
            await ctx.send(f"{selected_pet['NAME']} is ready for battle!", hidden=True)
        else:
            await ctx.send(m.USER_DOESNT_HAVE_THE_PET, hidden=True)
            return

    @cog_ext.cog_slash(description="View a Summon", guild_ids=main.guild_ids)
    async def viewsummon(self, ctx, summon: str):
        pet = db.queryPet({'PET': {"$regex": f"^{str(summon)}$", "$options": "i"}})
        if pet:
            pet_pet = pet['PET']
            pet_show = pet['UNIVERSE']
            pet_image = pet['PATH']

            if pet_show != 'Unbound':
                pet_show_img = db.queryUniverse({'TITLE': pet_show})['PATH']
            pet_passive = pet['ABILITIES'][0]
                # Summon Passive
            o_pet_passive_name = list(pet_passive.keys())[0]
            o_pet_passive_value = list(pet_passive.values())[0]
            o_pet_passive_type = list(pet_passive.values())[1]

            message=""
            
            if o_pet_passive_type == 'ATK':
                typetext = "Attack"
                message=f"{pet_pet} is a ATK Summon"
            elif o_pet_passive_type == 'DEF':
                typetext = "Defense"
                mmessage=f"{pet_pet} is a DEF Summon"
            elif o_pet_passive_type == 'STAM':
                typetext = "Stamina"
                message=f"{pet_pet} is a STAM Summon"
            elif o_pet_passive_type == 'HLT':
                typetext = "Health"
                message=f"{pet_pet} is a HLT Summon"
            elif o_pet_passive_type == 'LIFE':
                typetext = "Health"
                message=f"{pet_pet} is a LIFE Summon"
            elif o_pet_passive_type == 'DRAIN':
                typetext = "Stamina"
                message=f"{pet_pet} is a DRAIN Summon"
            elif o_pet_passive_type == 'FLOG':
                typetext = "Attack"
                message=f"{pet_pet} is a FLOG Summon"
            elif o_pet_passive_type == 'WITHER':
                typetext = "Defense"
                message=f"{pet_pet} is a WITHER Summon"
            elif o_pet_passive_type == 'RAGE':
                typetext = "Defense gain Attack"
                message=f"{pet_pet} is a RAGE Summon"
            elif o_pet_passive_type == 'BRACE':    
                typetext = "Attack gain Defense"        
                message=f"{pet_pet} is a BRACE Summon"
            elif o_pet_passive_type == 'BZRK':    
                typetext = "Health gain Attack"        
                message=f"{pet_pet} is a BZRK Summon"
            elif o_pet_passive_type == 'CRYSTAL':    
                typetext = "Health gain Defense"        
                message=f"{pet_pet} is a CRYSTAL Summon"
            elif o_pet_passive_type == 'GROWTH':    
                typetext = "Max Health gain Attack and Defense"        
                message=f"{pet_pet} is a GRWOTH Summon"
            elif o_pet_passive_type == 'STANCE':
                typetext = "Attack and Defense increase"
                message=f"{pet_pet} is a STANCE Summon"
            elif o_pet_passive_type == 'CONFUSE':
                typetext = "Opponent Attack And Defense decrease Opponent"
                message=f"{pet_pet} is a CONFUSE Summon"
            elif o_pet_passive_type == 'BLINK':
                typetext = "Decrease Stamina, Increase Opponent Stamina"
                message=f"{pet_pet} is a BLINK Summon"
            elif o_pet_passive_type == 'SLOW':
                typetext = "Decrease Stamina by"
                message=f"{pet_pet} is a SLOW Summon"
            elif o_pet_passive_type == 'HASTE':
                typetext = "Increase Stamina by"
                message=f"{pet_pet} is a HASTE Summon"
            elif o_pet_passive_type == 'SOULCHAIN':
                typetext = "Stamina"
                message=f"{pet_pet} is a SOULCHAIN Summon"
            elif o_pet_passive_type == 'FEAR':
                typetext = "Max Health reduce Opponent Attack and Defense"
                message=f"{pet_pet} is a FEAR Summon"
            elif o_pet_passive_type == 'GAMBLE':
                typetext = "Health"
                message=f"{pet_pet} is a GAMBLE Summon"   
            elif o_pet_passive_type == 'BLAST':
                typetext = "Deals Increasing AP * Turn Count Damage "
                message=f"{pet_pet} is a BLAST Summon"
            elif o_pet_passive_type == 'WAVE':
                typetext = "Deals Decreasing AP / Turn Count Damage"
                message=f"{pet_pet} is a SOULCHAIN Summon"
            elif o_pet_passive_type == 'DESTRUCTION':
                typetext = "Destroys Increasing AP * Turn Count Max Health"
                message=f"{pet_pet} is a FEAR Summon"
            elif o_pet_passive_type == 'CREATION':
                typetext = "Grants Decreasing AP / Turn Count Max Health"
                message=f"{pet_pet} is a GAMBLE Summon"   


            # embedVar = discord.Embed(pet=f"{Crest_dict[pet_show]} {pet_pet}".format(self), description=f"{message}", colour=000000)
            # if pet_show != "Unbound":
            #     embedVar.set_thumbnail(url=pet_show_img)
            # embedVar.set_author(name=pet_pet)
            # embedVar.set_image(url=pet_image)
            # embedVar.add_field(name=f"{o_pet_passive_type}", value=f"`Move {o_pet_passive_name} increases {o_pet_passive_type} by {o_pet_passive_value}`", inline=False)
            # embedVar.set_footer(text=f"/enhancers - Enhancement Menu")
            
            embedVar = discord.Embed(title=f"{Crest_dict[pet_show]} {pet_pet}".format(self), colour=000000)
            if pet_show != "Unbound":
                embedVar.set_thumbnail(url=pet_show_img)
            embedVar.set_image(url=pet_image)
            if o_pet_passive_type == "ATK" or o_pet_passive_type == "DEF" or o_pet_passive_type == "HLT" or o_pet_passive_type == "STAM":
                embedVar.add_field(name=f"**Unique Passive**", value=f"Increases **{typetext}** by **{o_pet_passive_value}{enhancer_suffix_mapping[o_pet_passive_type]}**", inline=False)
            elif o_pet_passive_type == "FLOG" or o_pet_passive_type == "WITHER" or o_pet_passive_type == "LIFE" or o_pet_passive_type == "DRAIN":
                embedVar.add_field(name=f"**Unique Passive**", value=f"Steals **{o_pet_passive_value}{enhancer_suffix_mapping[o_pet_passive_type]} {typetext}**", inline=False)
            elif o_pet_passive_type == "RAGE" or o_pet_passive_type == "BRACE" or o_pet_passive_type == "BZRK" or o_pet_passive_type == "CRYSTAL" or o_pet_passive_type == "GROWTH" or o_pet_passive_type == "FEAR":
                embedVar.add_field(name=f"**Unique Passive**", value=f"Sacrifice **{o_pet_passive_value}{enhancer_suffix_mapping[o_pet_passive_type]} {typetext}**", inline=False)
            elif o_pet_passive_type == "STANCE" or o_pet_passive_type == "CONFUSE":
                embedVar.add_field(name=f"**Unique Passive**", value=f"Swap {typetext} Defense by **{o_pet_passive_value}**", inline=False)
            elif o_pet_passive_type == "BLINK":
                embedVar.add_field(name=f"**Unique Passive**", value=f"**{typetext}** by **{o_pet_passive_value}**", inline=False)
            elif o_pet_passive_type == "SLOW" or o_pet_passive_type == "HASTE":
                embedVar.add_field(name=f"**Unique Passive**", value=f"**{typetext}** by **{o_pet_passive_value}**", inline=False)
            elif o_pet_passive_type == "SOULCHAIN" or o_pet_passive_type == "GAMBLE":
                embedVar.add_field(name=f"**Unique Passive**", value=f"Set both players **{typetext}** equal to **{o_pet_passive_value}**", inline=False)
            elif o_pet_passive_type == "BLAST" or o_pet_passive_type == "DESTRUCTION":
                embedVar.add_field(name=f"**Unique Passive**", value=f"**{typetext}** starting at **{o_pet_passive_value}**", inline=False)
            elif o_pet_passive_type == "WAVE" or o_pet_passive_type == "CREATION":
                embedVar.add_field(name=f"**Unique Passive**", value=f"**{typetext}** starting at **{o_pet_passive_value}**", inline=False)
            embedVar.set_footer(text=f"{o_pet_passive_type}: {enhancer_mapping[o_pet_passive_type]}")

            await ctx.send(embed=embedVar, hidden=True)

        else:
            await ctx.send(m.PET_DOESNT_EXIST, hidden=True)

def setup(bot):
    bot.add_cog(Pet(bot))
    
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
enhancer_mapping = {'ATK': 'Increase Attack %',
'DEF': 'Increase Defense %',
'STAM': 'Increase Stamina',
'HLT': 'Heal yourself or companion',
'LIFE': 'Steal Health from Opponent',
'DRAIN': 'Drain Stamina from Opponent',
'FLOG': 'Steal Attack from Opponent',
'WITHER': 'Steal Defense from Opponent',
'RAGE': 'Lose Defense, Increase Attack',
'BRACE': 'Lose Attack, Increase Defense',
'BZRK': 'Lose Health, Increase Attack',
'CRYSTAL': 'Lose Health, Increase Defense',
'GROWTH': 'Lose Health, Increase Attack & Defense',
'STANCE': 'Swap your Attack & Defense, Increase Attack',
'CONFUSE': 'Swap Opponent Attack & Defense, Decrease Opponent Defense',
'BLINK': 'Decrease your  Stamina, Increase Target Stamina',
'SLOW': 'Decrease Opponent Stamina, Swap Stamina with Opponent',
'HASTE': ' Increase your Stamina, Swap Stamina with Opponent',
'FEAR': 'Decrease your Health, Decrease Opponent Attack and Defense',
'SOULCHAIN': 'You and Your Opponent Stamina Link',
'GAMBLE': 'You and Your Opponent Health Link',
'WAVE': 'Deal Damage, Decreases over time',
'CREATION': 'Heals you, Decreases over time',
'BLAST': 'Deals Damage, Increases over time',
'DESTRUCTION': 'Decreases Opponent Max Health, Increases over time',
'BASIC': 'Increase Basic Attack AP',
'SPECIAL': 'Increase Special Attack AP',
'ULTIMATE': 'Increase Ultimate Attack AP',
'ULTIMAX': 'Increase All AP Values',
'MANA': 'Increase Enchancer AP',
'SHIELD': 'Blocks Incoming DMG, until broken',
'BARRIER': 'Nullifies Incoming Attacks, until broken',
'PARRY': 'Returns Half Damage, until broken'
}
enhancer_suffix_mapping = {'ATK': '%',
'DEF': '%',
'STAM': ' Flat',
'HLT': '%',
'LIFE': '%',
'DRAIN': ' Flat',
'FLOG': '%',
'WITHER': '%',
'RAGE': '%',
'BRACE': '%',
'BZRK': '%',
'CRYSTAL': '%',
'GROWTH': '%',
'STANCE': ' Flat',
'CONFUSE': ' Flat',
'BLINK': ' Flat',
'SLOW': ' Flat',
'HASTE': ' Flat',
'FEAR': '%',
'SOULCHAIN': ' Flat',
'GAMBLE': ' Flat',
'WAVE': ' Flat',
'CREATION': ' Flat',
'BLAST': ' Flat',
'DESTRUCTION': ' Flat',
'BASIC': ' Flat',
'SPECIAL': ' Flat',
'ULTIMATE': ' Flat',
'ULTIMAX': ' Flat',
'MANA': ' %',
'SHIELD': ' DMG 🌐',
'BARRIER': ' Blocks 💠',
'PARRY': ' Counters 🔄'
}