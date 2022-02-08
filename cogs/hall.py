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

class Hall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print('Hall Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @cog_ext.cog_slash(description="Buy a Hall for your guild", guild_ids=main.guild_ids)
    async def buyhall(self, ctx, hall: str):
        hall_name = hall
        leadername = str(ctx.author)
        user_query = {'DISNAME' : leadername}
        leader_info = db.queryUser(user_query)
        guildname = leader_info['GUILD']
        if guildname == 'PCG':
            await ctx.send(m.NOT_LEADER, delete_after=5)
            return
        guild_query = {'GNAME' : guildname}
        guild = db.queryGuildAlt(guild_query)
        hall = db.queryHall({'HALL': {"$regex": f"^{str(hall)}$", "$options": "i"}})
        currentBalance = guild['BANK']
        cost = hall['PRICE']
        hall_name = hall['HALL']
        if hall:
            if hall_name in guild['HALL']:
                await ctx.send(m.USERS_ALREADY_HAS_HALL, delete_after=5)
            else:
                newBalance = currentBalance - cost
                if newBalance < 0 :
                    await ctx.send("You have an insufficent Balance")
                else:
                    await main.curseguild(cost, str(guildname))
                    response = db.updateGuildAlt(guild_query,{'$set':{'HALL': str(hall_name)}})
                    await ctx.send(m.PURCHASE_COMPLETE_H + "Enjoy your new Hall!")
                    return
        else:
            await ctx.send(m.HALL_DOESNT_EXIST)

    @cog_ext.cog_slash(description="View a Hall", guild_ids=main.guild_ids)
    async def viewhall(self, ctx, hall: str):
        hall = db.queryHall({'HALL':{"$regex": f"^{str(hall)}$", "$options": "i"}})
        if hall:
            hall_hall = hall['HALL']
            hall_price = hall['PRICE']
            hall_img = hall['PATH']
            hall_multiplier = hall['MULT']
            hall_fee = hall['FEE']
            hall_split = hall['SPLIT']
            hall_def = hall['DEFENSE']

            message=""
            
            price_message ="" 
            price_message = f":coin: {'{:,}'.format(hall_price)}"


            embedVar = discord.Embed(title=f"{hall_hall}\n{price_message}", colour=000000)
            embedVar.set_thumbnail(url=hall_img)
            embedVar.add_field(name="Bounty Fee", value=f"**{'{:,}'.format(hall_fee)}** :yen: per **Raid**!", inline=False)
            embedVar.add_field(name="Multiplier", value=f"Association earns **{hall_multiplier}x** :coin: per match!", inline=False)
            embedVar.add_field(name="Split", value=f"**Guilds** earn **{hall_split}x** :coin: per match!", inline=False)
            embedVar.add_field(name="Defenses", value=f"**Shield** Defense Boost: **{hall_def}x**", inline=False)
            embedVar.set_footer(text=f"/halls - Hall Menu")

            await ctx.send(embed=embedVar)

        else:
            await ctx.send(m.ARM_DOESNT_EXIST, delete_after=3)


def setup(bot):
    bot.add_cog(Hall(bot))