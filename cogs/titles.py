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

class Titles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print('Titles Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @commands.command()
    async def nt(self, ctx, tournament: int, price: int, *args):
        if ctx.author.guild_permissions.administrator == True:
            title = " ".join([*args])
            title_query = {'TITLE': str(title), 'TOURNAMENT_REQUIREMENTS': int(tournament), 'PRICE': int(price)}
            added = db.createTitle(data.newTitle(title_query))
            await ctx.send(added, delete_after=3)
        else:
            print(m.ADMIN_ONLY_COMMAND)


    @commands.command()
    async def bt(self, ctx, *args: str):
        title_name=" ".join([*args])
        vault_query = {'OWNER' : str(ctx.author)}
        vault = db.altQueryVault(vault_query)
        shop = db.queryShopTitles()
        titles = []

        currentBalance = vault['BALANCE']
        cost = 0
        mintedTitle = ""
        for title in shop:

            if title_name == title['TITLE']:
                mintedTitle = title['TITLE']
                cost = title['PRICE']

        if bool(mintedTitle):
            if mintedTitle in vault['TITLES']:
                await ctx.send(m.USER_ALREADY_HAS_TITLE, delete_after=5)
            else:
                newBalance = currentBalance - cost

                if newBalance < 0 :
                    await ctx.send("You have an insufficent Balance")
                else:
                    await main.curse(cost, str(ctx.author))
                    response = db.updateVaultNoFilter(vault_query,{'$addToSet':{'TITLES': str(title_name)}})
                    await ctx.send(m.PURCHASE_COMPLETE)
        else:
            await ctx.send(m.TITLE_DOESNT_EXIST)

    @commands.command()
    async def ut(self, ctx, *args):
        title_name=" ".join([*args])
        user_query = {'DISNAME': str(ctx.author)}
        user = db.queryUser(user_query)

        vault_query = {'OWNER' : str(ctx.author)}
        vault = db.altQueryVault(vault_query)

        resp = db.queryTitle({'TITLE': str(title_name)})

        if resp['TOURNAMENT_REQUIREMENTS'] == 0:

            # Do not Check Tourney wins
            if title_name in vault['TITLES']:
                response = db.updateUserNoFilter(user_query, {'$set': {'TITLE': str(title_name)}})
                await ctx.send(response)
            else:
                await ctx.send(m.USER_DOESNT_HAVE_THE_Title, delete_after=5)
        else:

            # Check tourney wins
            tournament_wins = user['TOURNAMENT_WINS']
            title_query = {'TOURNAMENT_REQUIREMENTS': tournament_wins}

            if tournament_wins >= resp['TOURNAMENT_REQUIREMENTS']:
                if title_name in vault['TITLES']:
                    response = db.updateUserNoFilter(user_query, {'$set': {'TITLE': str(title_name)}})
                    await ctx.send(response)
                else:
                    await ctx.send(m.USER_DOESNT_HAVE_THE_Title, delete_after=5)
            else:
                return "Unable to update Title."


def setup(bot):
    bot.add_cog(Titles(bot))

# @commands.command()
# async def nt(self, ctx, args1: str, args2: int, args3: int):
#    if ctx.author.guild_permissions.administrator == True:
#       title_query = {'TITLE': str(args1), 'TOURNAMENT_REQUIREMENTS': int(args2), 'PRICE': int(args3)}
#       added = db.createTitle(data.newTitle(title_query))
#       await ctx.send(added, delete_after=3)
#    else:
#       print(m.ADMIN_ONLY_COMMAND)