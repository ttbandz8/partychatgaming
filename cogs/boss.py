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

    @commands.command()
    async def nb(self, ctx, image: str, *args):
        if ctx.author.guild_permissions.administrator == True:
            boss = " ".join([*args])
            boss_query = {'NAME': str(boss), 'PATH' : str(image)}
            added = db.createBoss(data.newBoss(boss_query))
            await ctx.send(added)
        else:
            print(m.ADMIN_ONLY_COMMAND)

    @commands.command()
    async def viewboss(self, ctx, *args):
        boss_name = " ".join([*args])
        boss = db.queryBoss({'NAME': str(boss_name)})
        if boss:
            boss_name = boss['NAME']
            boss_show = boss['UNIVERSE']
            boss_title = boss['TITLE']
            boss_arm = boss['ARM']
            boss_desc = boss['DESCRIPTION'][3]
            boss_pic = boss['PATH']
            boss_pet = boss['PET']

            arm = db.queryArm({'ARM': boss_arm})
            arm_passive = arm['ABILITIES'][0]
            arm_passive_type = list(arm_passive.keys())[0]
            arm_passive_value = list(arm_passive.values())[0]

            title = db.queryTitle({'TITLE': boss_title})
            title_passive = title['ABILITIES'][0]
            title_passive_type = list(title_passive.keys())[0]
            title_passive_value = list(title_passive.values())[0]
            
            pet = db.queryPet({'PET': boss_pet})
            pet_ability = pet['ABILITIES'][0]
            pet_ability_name = list(pet_ability.keys())[0]
            pet_ability_type = list(pet_ability.values())[0]
            pet_ability_value = list(pet_ability.values())[0]



            if boss_show != 'Unbound':
                boss_show_img = db.queryUniverse({'TITLE': boss_show})['PATH']
            message= boss_desc

            embedVar = discord.Embed(title=f"{boss_name}".format(self), description=f"{message}", colour=000000)
            if boss_show != "Unbound":
                embedVar.set_thumbnail(url=boss_show_img)
            embedVar.set_image(url=boss_pic)
            embedVar.add_field(name="TITLE", value=f"{boss_title}\nIncreases **{title_passive_type}** by **{title_passive_value}**", inline=True)
            embedVar.add_field(name="ARM", value=f"{boss_arm}\nIncreases **{arm_passive_type}** by **{arm_passive_value}**", inline=True)
            embedVar.add_field(name="PET", value=f"{boss_pet}\nAbilitiy:**{pet_ability_name}**\nIncreases **{pet_ability_type}** by **{pet_ability_value}**", inline=True)

            await ctx.send(embed=embedVar)

        else:
            await ctx.send(m.ARM_DOESNT_EXIST, delete_after=3)










def setup(bot):
    bot.add_cog(Boss(bot))