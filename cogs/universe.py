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
        try:
            universe_name = universe
            universe = db.queryUniverse({'TITLE': {"$regex": f"^{universe_name}$", "$options": "i"}})
            universe_name = universe['TITLE']
            if universe:
                universe_title= universe['TITLE']
                universe_image = universe['PATH']

                embedVar = discord.Embed(title=f"{universe_name}".format(self), description=f"Crown Unlimited Universe")
                embedVar.set_image(url=universe_image)

                await ctx.send(embed=embedVar)

            else:
                await ctx.send(m.UNIVERSE_DOES_NOT_EXIST)
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
            await ctx.send(f"Error when viewing universe. Alert support. Thank you!")
            return

def setup(bot):
    bot.add_cog(Universe(bot))