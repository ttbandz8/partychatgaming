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

class House(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print('House Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @commands.command()
    async def nh(self, ctx, path, *args):
        if ctx.author.guild_permissions.administrator == True:
            house = " ".join([*args])
            house_query = {'HOUSE': str(house), 'PATH':path, 'PRICE': 500}
            added = db.createHouse(data.newHouse(house_query))
            await ctx.send(added)
        else:
            print(m.ADMIN_ONLY_COMMAND)


    @commands.command()
    async def buyhouse(self, ctx, *args: str):
        house_name=" ".join([*args])
        family_query = {'HEAD' : str(ctx.author)}
        family = db.queryFamily(family_query)
        house = db.queryHouse({'HOUSE': house_name})
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

    @commands.command()
    async def viewhouse(self, ctx, *args):
        arm_name = " ".join([*args])
        arm = db.queryArm({'ARM': str(arm_name)})
        if arm:
            arm_arm = arm['ARM']
            arm_show = arm['UNIVERSE']
            arm_price = arm['PRICE']
            exclusive = arm['EXCLUSIVE']

            if arm_show != 'Unbound':
                arm_show_img = db.queryUniverse({'TITLE': arm_show})['PATH']
            arm_passive = arm['ABILITIES'][0]
                # Arm Passive
            o_arm_passive_type = list(arm_passive.keys())[0]
            o_arm_passive_value = list(arm_passive.values())[0]

            message=""
            
            price_message ="" 
            if exclusive:
                price_message = "_Priceless_"
            else:
                price_message = f":coin: {arm_price}"

            if o_arm_passive_type == 'ATK':
                message=f"{arm_arm} is an ATK arm"
            elif o_arm_passive_type == 'DEF':
                message=f"{arm_arm} is a DEF arm"
            elif o_arm_passive_type == 'STAM':
                message=f"{arm_arm} is a STAM arm"
            elif o_arm_passive_type == 'HLT':
                message=f"{arm_arm} is a HLT arm"
            elif o_arm_passive_type == 'LIFE':
                message=f"{arm_arm} is a LIFE arm"
            elif o_arm_passive_type == 'DRAIN':
                message=f"{arm_arm} is an DRAIN arm"
            elif o_arm_passive_type == 'FLOG':
                message=f"{arm_arm} is a FLOG arm"
            elif o_arm_passive_type == 'WITHER':
                message=f"{arm_arm} is a WITHER arm"
            elif o_arm_passive_type == 'RAGE':
                message=f"{arm_arm} is a RAGE arm"
            elif o_arm_passive_type == 'BRACE':            
                message=f"{arm_arm} is a BRACE arm"
            elif o_arm_passive_type == 'BZRK':            
                message=f"{arm_arm} is a BZRK arm"
            elif o_arm_passive_type == 'CRYSTAL':            
                message=f"{arm_arm} is a CRYSTAL arm"
            elif o_arm_passive_type == 'GROWTH':            
                message=f"{arm_arm} is a GROWTH arm"
            elif o_arm_passive_type == 'STANCE':
                message=f"{arm_arm} is a STANCE arm"
            elif o_arm_passive_type == 'CONFUSE':
                message=f"{arm_arm} is a CONFUSE arm"
            elif o_arm_passive_type == 'BLINK':
                message=f"{arm_arm} is a BLINK arm"
            elif o_arm_passive_type == 'SLOW':
                message=f"{arm_arm} is a SLOW arm"
            elif o_arm_passive_type == 'HASTE':
                message=f"{arm_arm} is a HASTE arm" 
            elif o_arm_passive_type == 'SOULCHAIN':
                message=f"{arm_arm} is a SOULCHAIN arm"
            elif o_arm_passive_type == 'FEAR':
                message=f"{arm_arm} is a FEAR arm"
            elif o_arm_passive_type == 'GAMBLE':
                message=f"{arm_arm} is a GAMBLE arm"


            embedVar = discord.Embed(title=f"{arm_arm}\n{price_message}".format(self), colour=000000)
            if arm_show != "Unbound":
                embedVar.set_thumbnail(url=arm_show_img)
            embedVar.add_field(name="Unique Passive", value=f"`Increases {o_arm_passive_type} by {o_arm_passive_value}`", inline=False)
            embedVar.set_footer(text=f".enhance - Enhancement Menu")

            await ctx.send(embed=embedVar)

        else:
            await ctx.send(m.ARM_DOESNT_EXIST, delete_after=3)



def setup(bot):
    bot.add_cog(House(bot))