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
    async def na(self, ctx, tournament: int, price: int, *args):
        if ctx.author.guild_permissions.administrator == True:
            arm = " ".join([*args])
            arm_query = {'ARM': str(arm), 'TOURNAMENT_REQUIREMENTS': int(tournament), 'PRICE': int(price)}
            added = db.createArm(data.newArm(arm_query))
            await ctx.send(added)
        else:
            print(m.ADMIN_ONLY_COMMAND)


    @commands.command()
    async def ba(self, ctx, *args: str):
        arm_name=" ".join([*args])
        vault_query = {'OWNER' : str(ctx.author)}
        vault = db.altQueryVault(vault_query)
        shop = db.queryShopArms()
        arms = []

        currentBalance = vault['BALANCE']
        cost = 0
        mintedArm = ""
        for arm in shop:

            if arm_name == arm['ARM']:
                mintedArm = arm['ARM']
                cost = arm['PRICE']

        if bool(mintedArm):
            if mintedArm in vault['ARMS']:
                await ctx.send(m.USER_ALREADY_HAS_ARM, delete_after=5)
            else:
                newBalance = currentBalance - cost

                if newBalance < 0 :
                    await ctx.send("You have an insufficent Balance")
                else:
                    await main.curse(cost, str(ctx.author))
                    response = db.updateVaultNoFilter(vault_query,{'$addToSet':{'ARMS': str(arm_name)}})
                    await ctx.send(m.PURCHASE_COMPLETE)
        else:
            await ctx.send(m.ARM_DOESNT_EXIST)

    @commands.command()
    async def ua(self, ctx, *args):
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
    async def va(self, ctx, *args):
        arm_name = " ".join([*args])
        arm = db.queryArm({'ARM': str(arm_name)})
        if arm:
            arm_arm = arm['ARM']
            arm_show = arm['SHOW']
            arm_passive = arm['PASS'][0]
                # Arm Passive
            o_arm_passive_type = list(arm_passive.keys())[0]
            o_arm_passive_value = list(arm_passive.values())[0]
            embedVar = discord.Embed(arm=f"{arm_arm}".format(self), description=f"Preview for {arm_arm} from {arm_show}.", colour=000000)

            embedVar.add_field(name="Unique Passive", value=f"`Increases {o_arm_passive_type} by {o_arm_passive_value}`", inline=False)

            await ctx.send(embed=embedVar)

        else:
            await ctx.send(m.CARD_DOESNT_EXIST, delete_after=3)



def setup(bot):
    bot.add_cog(Arm(bot))