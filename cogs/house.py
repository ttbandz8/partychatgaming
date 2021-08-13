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

class House(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print('House Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    # @commands.command()
    # async def nh(self, ctx, path, *args):
    #     if ctx.author.guild_permissions.administrator == True:
    #         house = " ".join([*args])
    #         house_query = {'HOUSE': str(house), 'PATH':path, 'PRICE': 500}
    #         added = db.createHouse(data.newHouse(house_query))
    #         await ctx.send(added)
    #     else:
    #         print(m.ADMIN_ONLY_COMMAND)


    @cog_ext.cog_slash(description="Buy a House for your family", guild_ids=main.guild_ids)
    async def buyhouse(self, ctx, house: str):
        house_name = house
        family_query = {'HEAD' : str(ctx.author)}
        family = db.queryFamily(family_query)
        house = db.queryHouse({'HOUSE': house})
        currentBalance = family['BANK']
        cost = house['PRICE']

        if house:
            if house_name in family['HOUSE']:
                await ctx.send(m.USERS_ALREADY_HAS_HOUSE, delete_after=5)
            else:
                newBalance = currentBalance - cost
                if newBalance < 0 :
                    await ctx.send("You have an insufficent Balance")
                else:
                    await main.cursefamily(cost, str(ctx.author))
                    response = db.updateFamily(family_query,{'$set':{'HOUSE': str(house_name)}})
                    await ctx.send(m.PURCHASE_COMPLETE_H + "Enjoy your new Home!")
                    return
        else:
            await ctx.send(m.HOUSE_DOESNT_EXIST)

    @cog_ext.cog_slash(description="View a House", guild_ids=main.guild_ids)
    async def viewhouse(self, ctx, house: str):
        house = db.queryHouse({'HOUSE': str(house)})
        if house:
            house_house = house['HOUSE']
            house_price = house['PRICE']
            house_img = house['PATH']
            house_multiplier = house['MULT']

            message=""
            
            price_message ="" 
            price_message = f":coin: {house_price}"


            embedVar = discord.Embed(title=f"{house_house}\n{price_message}".format(self), colour=000000)
            embedVar.set_thumbnail(url=house_img)
            embedVar.add_field(name="Multiplier", value=f"Family earns {house_multiplier}x :coin: per match!", inline=False)
            embedVar.set_footer(text=f".houses - House Menu")

            await ctx.send(embed=embedVar)

        else:
            await ctx.send(m.ARM_DOESNT_EXIST, delete_after=3)



def setup(bot):
    bot.add_cog(House(bot))