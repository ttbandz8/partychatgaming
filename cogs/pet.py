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

    @cog_ext.cog_slash(description="Equip Pet", guild_ids=main.guild_ids)
    async def equippet(self, ctx, pet: str):
        pet_name = pet
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
            await ctx.send(f"{selected_pet['NAME']} is ready for battle!")
        else:
            await ctx.send(m.USER_DOESNT_HAVE_THE_PET, delete_after=5)
            return

    @cog_ext.cog_slash(description="View a Pet", guild_ids=main.guild_ids)
    async def viewpet(self, ctx, pet: str):
        pet = db.queryPet({'PET': {"$regex": f"^{str(pet)}$", "$options": "i"}})
        if pet:
            pet_pet = pet['PET']
            pet_show = pet['UNIVERSE']
            pet_image = pet['PATH']

            if pet_show != 'Unbound':
                pet_show_img = db.queryUniverse({'TITLE': pet_show})['PATH']
            pet_passive = pet['ABILITIES'][0]
                # Pet Passive
            o_pet_passive_name = list(pet_passive.keys())[0]
            o_pet_passive_value = list(pet_passive.values())[0]
            o_pet_passive_type = list(pet_passive.values())[1]

            message=""

            if o_pet_passive_type == 'ATK':
                message=f"{pet_pet} is an offensive Pet"
            elif o_pet_passive_type == 'DEF':
                message=f"{pet_pet} is a defensive Pet"
            elif o_pet_passive_type == 'STAM':
                message=f"{pet_pet} is an offensive Pet"
            elif o_pet_passive_type == 'HLT':
                message=f"{pet_pet} is a defensive Pet"
            elif o_pet_passive_type == 'LIFE':
                message=f"{pet_pet} is a defensive Pet"
            elif o_pet_passive_type == 'DRAIN':
                message=f"{pet_pet} is a DRAIN Pet"
            elif o_pet_passive_type == 'FLOG':
                message=f"{pet_pet} is a FLOG Pet"
            elif o_pet_passive_type == 'WITHER':
                message=f"{pet_pet} is a WITHER Pet"
            elif o_pet_passive_type == 'RAGE':
                message=f"{pet_pet} is a RAGE Pet"
            elif o_pet_passive_type == 'BRACE':            
                message=f"{pet_pet} is a BRACE Pet"
            elif o_pet_passive_type == 'BZRK':            
                message=f"{pet_pet} is a BZRK Pet"
            elif o_pet_passive_type == 'CRYSTAL':            
                message=f"{pet_pet} is a CRYSTAL Pet"
            elif o_pet_passive_type == 'GROWTH':            
                message=f"{pet_pet} is a GROWTH Pet"
            elif o_pet_passive_type == 'STANCE':
                message=f"{pet_pet} is a STANCE Pet"
            elif o_pet_passive_type == 'CONFUSE':
                message=f"{pet_pet} is a CONFUSE Pet"
            elif o_pet_passive_type == 'BLINK':
                message=f"{pet_pet} is a BLINK Pet"
            elif o_pet_passive_type == 'SLOW':
                message=f"{pet_pet} is a SLOW Pet"
            elif o_pet_passive_type == 'HASTE':
                message=f"{pet_pet} is a HASTE Pet" 
            elif o_pet_passive_type == 'SOULCHAIN':
                message=f"{pet_pet} is a SOULCHAIN Pet"
            elif o_pet_passive_type == 'FEAR':
                message=f"{pet_pet} is a FEAR Pet"
            elif o_pet_passive_type == 'GAMBLE':
                message=f"{pet_pet} is a GAMBLE Pet"             


            embedVar = discord.Embed(pet=f"{pet_pet}".format(self), description=f"{message}", colour=000000)
            if pet_show != "Unbound":
                embedVar.set_thumbnail(url=pet_show_img)
            embedVar.set_author(name=pet_pet)
            embedVar.set_image(url=pet_image)
            embedVar.add_field(name="Unique Passive", value=f"`Move {o_pet_passive_name} increases {o_pet_passive_type} by {o_pet_passive_value}`", inline=False)
            embedVar.set_footer(text=f"/enhancers - Enhancement Menu")

            await ctx.send(embed=embedVar)

        else:
            await ctx.send(m.PET_DOESNT_EXIST, delete_after=3)

def setup(bot):
    bot.add_cog(Pet(bot))