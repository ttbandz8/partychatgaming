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

class Universe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print('Universe Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @commands.command()
    async def newuniverse(self, ctx, path, *args):
        if ctx.author.guild_permissions.administrator == True:
            universe = " ".join([*args])
            universe_query = {'TITLE': str(universe), 'PATH': str(path)}
            added = db.createUniverse(data.newUniverse(universe_query))
            await ctx.send(added)
        else:
            print(m.ADMIN_ONLY_COMMAND)

    @commands.command()
    async def viewUniverse(self, ctx, *args):
        universe_name = " ".join([*args])
        universe = db.queryUniverse({'TITLE': str(universe_name)})
        if universe:
            universe_title= universe['TITLE']
            universe_image = universe['PATH']

            embedVar = discord.Embed(universe=f"{universe}".format(self), description=f"Crown Unlimited Universe", colour=000000)
            embedVar.set_image(url=universe_image)

            await ctx.send(embed=embedVar)

        else:
            await ctx.send(m.UNIVERSE_DOES_NOT_EXIST)

def setup(bot):
    bot.add_cog(Universe(bot))