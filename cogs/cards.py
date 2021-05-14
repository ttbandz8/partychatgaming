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

class Cards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print('Cards Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)


    @commands.command()
    async def nc(self, ctx, args1: str, args2: str, args3: int, args4: int):
        if ctx.author.guild_permissions.administrator == True:
            card_query = {'PATH': str(args1), 'NAME': str(args2), 'TOURNAMENT_REQUIREMENTS': int(args3),'PRICE': int(args4)}
            added = db.createCard(data.newCard(card_query))
            await ctx.send(added, delete_after=3)
        else:
            print(m.ADMIN_ONLY_COMMAND)

    @commands.command()
    async def bc(self, ctx, args: str):
        vault_query = {'OWNER' : str(ctx.author)}
        vault = db.altQueryVault(vault_query)
        shop = db.queryShopCards()
        cards = []

        currentBalance = vault['BALANCE']
        cost = 0
        mintedCard = ""
        for card in shop:
            if args == card['NAME']:
                mintedCard = card['NAME']
                cost = card['PRICE']


        if bool(mintedCard):
            if mintedCard in vault['CARDS']:
                await ctx.send(m.USER_ALREADY_HAS_CARD, delete_after=5)
            else:
                newBalance = currentBalance - cost

                if newBalance < 0 :
                    await ctx.send("You have an insufficent Balance")
                else:
                    await main.curse(cost, str(ctx.author))
                    response = db.updateVaultNoFilter(vault_query,{'$addToSet':{'CARDS': args}})
                    await ctx.send(m.PURCHASE_COMPLETE)
        else:
            await ctx.send(m.CARD_DOESNT_EXIST)

    @commands.command()
    async def uc(self, ctx, args):
        user_query = {'DISNAME': str(ctx.author)}
        user = db.queryUser(user_query)

        vault_query = {'OWNER' : str(ctx.author)}
        vault = db.altQueryVault(vault_query)

        resp = db.queryCard({'NAME': args})

        if resp['TOURNAMENT_REQUIREMENTS'] == 0:

            # Do not Check Tourney wins
            if args in vault['CARDS']:
                response = db.updateUserNoFilter(user_query, {'$set': {'CARD': args}})
                await ctx.send(response)
            else:
                await ctx.send(m.USER_DOESNT_HAVE_THE_CARD, delete_after=5)
        else:

            # Check tourney wins
            tournament_wins = user['TOURNAMENT_WINS']
            card_query = {'TOURNAMENT_REQUIREMENTS': tournament_wins}

            if tournament_wins >= resp['TOURNAMENT_REQUIREMENTS']:
                if args in vault['CARDS']:
                    response = db.updateUserNoFilter(user_query, {'$set': {'CARD': args}})
                    await ctx.send(response)
                else:
                    await ctx.send(m.USER_DOESNT_HAVE_THE_CARD, delete_after=5)
            else:
                return "Unable to update card."

    @commands.command()
    async def vc(self, ctx, args):
        card = db.queryCard({'NAME':args})
        if card:
            img = Image.open(requests.get(card['PATH'], stream=True).raw)
            img.save("text.png")
            await ctx.send(file=discord.File("text.png"))
        else:
            await ctx.send(m.CARD_DOESNT_EXIST, delete_after=3)



def setup(bot):
    bot.add_cog(Cards(bot))

# ''' Delete All Cards '''
# @commands.command()
# async def dac(self, ctx):
#    user_query = {"DISNAME": str(ctx.author)}
#    if ctx.author.guild_permissions.administrator == True:
#       resp = db.deleteAllCards(user_query)
#       await ctx.send(resp)
#    else:
#       await ctx.send(m.ADMIN_ONLY_COMMAND)