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

class Universe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print('Universe Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @cog_ext.cog_slash(description="View a universe", guild_ids=main.guild_ids)
    async def viewUniverse(self, ctx, universe: str):
        universe_name = universe
        universe = db.queryUniverse({'TITLE': {"$regex": universe_name, "$options": "i"}})
        universe_name = universe['TITLE']
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