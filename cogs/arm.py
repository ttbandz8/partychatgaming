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

class Arm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print('Arm Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @commands.command()
    async def na(self, ctx, *args):
        if ctx.author.guild_permissions.administrator == True:
            arm = " ".join([*args])
            arm_query = {'ARM': str(arm), 'TOURNAMENT_REQUIREMENTS': 0, 'PRICE': 500}
            added = db.createArm(data.newArm(arm_query))
            await ctx.send(added)
        else:
            print(m.ADMIN_ONLY_COMMAND)


    @commands.command()
    async def buyarm(self, ctx, *args: str):
        arm_name=" ".join([*args])
        vault_query = {'OWNER' : str(ctx.author)}
        vault = db.altQueryVault(vault_query)
        shop = db.queryShopArms()
        arms = []

        currentBalance = vault['BALANCE']
        cost = 0
        mintedArm = ""
        stock = 0
        newstock = 0
        armInStock = False
        checkout = True
        for arm in shop:

            if arm_name == arm['ARM']:
                if stock == arm['STOCK']:
                    checkout = armInStock
                else:
                    armInStock = True
                    mintedArm = arm['ARM']
                    cost = arm['PRICE']
                    stock = arm['STOCK']
                    newstock = stock - 1

        if bool(mintedArm):
            if mintedArm in vault['ARMS']:
                await ctx.send(m.USER_ALREADY_HAS_ARM, delete_after=5)
            else:
                newBalance = currentBalance - cost

                if newBalance < 0 :
                    await ctx.send("You have an insufficent Balance")
                else:
                    await main.curse(cost, str(ctx.author))
                    arm_query = {'ARM' : str(mintedArm)}
                    armInventory = db.queryArm(arm_query)
                    update_query = {"$set": {"STOCK": newstock}} 
                    response = db.updateArm(armInventory, update_query)
                    response = db.updateVaultNoFilter(vault_query,{'$addToSet':{'ARMS': str(arm_name)}})
                    await ctx.send(m.PURCHASE_COMPLETE_1 + f"`{newstock}` `{mintedArm}` ARMS left in the Shop!")

                    accept = await ctx.send(f"{ctx.author.mention} would you like to equip this Arm?")
                    emojis = ['👍', '👎']
                    for emoji in emojis:
                        await accept.add_reaction(emoji)

                    def check(reaction, user):
                        return user == ctx.author and str(reaction.emoji) == '👍'
                    try:
                        user_query = {'DISNAME': str(ctx.author)}
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=25.0, check=check)
                        response = db.updateUserNoFilter(user_query, {'$set': {'ARM': str(arm_name)}})
                        await ctx.send(response)
                    except:
                        return

        elif checkout == True:
            await ctx.send(m.ARM_DOESNT_EXIST)
        else:
            await ctx.send(m.ARM_OUT_OF_STOCK)

    @commands.command()
    async def equiparm(self, ctx, *args):
        arm_name=" ".join([*args])
        user_query = {'DISNAME': str(ctx.author)}
        user = db.queryUser(user_query)

        vault_query = {'OWNER' : str(ctx.author)}
        vault = db.altQueryVault(vault_query)

        resp = db.queryArm({'ARM': str(arm_name)})

        if resp['TOURNAMENT_REQUIREMENTS'] == 0:

            # Do not Check Tourney wins
            if arm_name in vault['ARMS']:
                response = db.updateUserNoFilter(user_query, {'$set': {'ARM': str(arm_name)}})
                await ctx.send(response)
            else:
                await ctx.send(m.USER_DOESNT_HAVE_THE_ARM, delete_after=5)
        else:

            # Check tourney wins
            tournament_wins = user['TOURNAMENT_WINS']
            arm_query = {'TOURNAMENT_REQUIREMENTS': tournament_wins}

            if tournament_wins >= resp['TOURNAMENT_REQUIREMENTS']:
                if arm_name in vault['ARMS']:
                    response = db.updateUserNoFilter(user_query, {'$set': {'ARM': str(arm_name)}})
                    await ctx.send(response)
                else:
                    await ctx.send(m.USER_DOESNT_HAVE_THE_ARM, delete_after=5)
            else:
                return "Unable to update Arm."

    @commands.command()
    async def viewarm(self, ctx, *args):
        arm_name = " ".join([*args])
        arm = db.queryArm({'ARM': str(arm_name)})
        if arm:
            arm_arm = arm['ARM']
            arm_show = arm['UNIVERSE']
            if arm_show != 'Unbound':
                arm_show_img = db.queryUniverse({'TITLE': arm_show})['PATH']
            arm_passive = arm['ABILITIES'][0]
                # Arm Passive
            o_arm_passive_type = list(arm_passive.keys())[0]
            o_arm_passive_value = list(arm_passive.values())[0]

            message=""

            if o_arm_passive_type == 'ATK':
                message=f"{arm_arm} is an offensive arm"
            elif o_arm_passive_type == 'DEF':
                message=f"{arm_arm} is a defensive arm"
            elif o_arm_passive_type == 'STAM':
                message=f"{arm_arm} is an offensive arm"
            elif o_arm_passive_type == 'HLT':
                message=f"{arm_arm} is a defensive arm"
            elif o_arm_passive_type == 'LIFE':
                message=f"{arm_arm} is a defensive arm"
            elif o_arm_passive_type == 'DRAIN':
                message=f"{arm_arm} is an offensive arm"


            embedVar = discord.Embed(arm=f"{arm_arm}".format(self), description=f"{message}", colour=000000)
            if arm_show != "Unbound":
                embedVar.set_thumbnail(url=arm_show_img)
            embedVar.add_field(name="Unique Passive", value=f"`Increases {o_arm_passive_type} by {o_arm_passive_value}`", inline=False)

            await ctx.send(embed=embedVar)

        else:
            await ctx.send(m.ARM_DOESNT_EXIST, delete_after=3)



def setup(bot):
    bot.add_cog(Arm(bot))