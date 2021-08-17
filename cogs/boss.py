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

class Boss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print('Boss Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @cog_ext.cog_slash(description="View a Boss", guild_ids=main.guild_ids)
    async def viewboss(self, ctx, boss : str):
        uboss_name = boss
        uboss = db.queryBoss({'NAME': {"$regex": str(uboss_name), "$options": "i"}})
        if uboss:
            uboss_name = uboss['NAME']
            uboss_show = uboss['UNIVERSE']
            uboss_title = uboss['TITLE']
            uboss_arm = uboss['ARM']
            uboss_desc = uboss['DESCRIPTION'][3]
            uboss_pic = uboss['PATH']
            uboss_pet = uboss['PET']

            arm = db.queryArm({'ARM': uboss_arm})
            arm_passive = arm['ABILITIES'][0]
            arm_passive_type = list(arm_passive.keys())[0]
            arm_passive_value = list(arm_passive.values())[0]

            title = db.queryTitle({'TITLE': uboss_title})
            title_passive = title['ABILITIES'][0]
            title_passive_type = list(title_passive.keys())[0]
            title_passive_value = list(title_passive.values())[0]
            
            pet = db.queryPet({'PET': uboss_pet})
            pet_ability = pet['ABILITIES'][0]
            pet_ability_name = list(pet_ability.keys())[0]
            pet_ability_type = list(pet_ability.values())[1]
            pet_ability_value = list(pet_ability.values())[0]



            if uboss_show != 'Unbound':
                uboss_show_img = db.queryUniverse({'TITLE': uboss_show})['PATH']
            message= uboss_desc

            embedVar = discord.Embed(title=f"{uboss_name}".format(self), description=f"{message}", colour=000000)
            if uboss_show != "Unbound":
                embedVar.set_thumbnail(url=uboss_show_img)
            embedVar.set_image(url=uboss_pic)
            embedVar.add_field(name="TITLE", value=f"{uboss_title}\nIncreases **{title_passive_type}** by **{title_passive_value}**", inline=True)
            embedVar.add_field(name="ARM", value=f"{uboss_arm}\nIncreases **{arm_passive_type}** by **{arm_passive_value}**", inline=True)
            embedVar.add_field(name="PET", value=f"{uboss_pet}\nAbilitiy:**{pet_ability_name}**\nIncreases **{pet_ability_type}** by **{pet_ability_value}**", inline=True)

            await ctx.send(embed=embedVar)

        else:
            await ctx.send(m.ARM_DOESNT_EXIST, delete_after=3)










def setup(bot):
    bot.add_cog(Boss(bot))