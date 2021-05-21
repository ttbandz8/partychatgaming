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
from .crownunlimited import showcard

class Cards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print('Cards Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)


    @commands.command()
    async def nc(self, ctx, path: str, tournament: int, price: int, *args):
        if ctx.author.guild_permissions.administrator == True:
            name = " ".join([*args])
            card_query = {'PATH': str(path), 'NAME': str(name), 'TOURNAMENT_REQUIREMENTS': int(tournament),'PRICE': int(price)}
            added = db.createCard(data.newCard(card_query))
            await ctx.send(added, delete_after=3)
        else:
            print(m.ADMIN_ONLY_COMMAND)

    @commands.command()
    async def bc(self, ctx, *args: str):
        card_name = " ".join([*args])
        vault_query = {'OWNER' : str(ctx.author)}
        vault = db.altQueryVault(vault_query)
        shop = db.queryShopCards()
        cards = []

        currentBalance = vault['BALANCE']
        cost = 0
        mintedCard = ""
        for card in shop:
            if card_name == card['NAME']:
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
                    response = db.updateVaultNoFilter(vault_query,{'$addToSet':{'CARDS': str(card_name)}})
                    await ctx.send(m.PURCHASE_COMPLETE)
        else:
            await ctx.send(m.CARD_DOESNT_EXIST)

    @commands.command()
    async def uc(self, ctx, *args):
        card_name = " ".join([*args])
        user_query = {'DISNAME': str(ctx.author)}
        user = db.queryUser(user_query)

        vault_query = {'OWNER' : str(ctx.author)}
        vault = db.altQueryVault(vault_query)

        resp = db.queryCard({'NAME': card_name})

        if resp['TOURNAMENT_REQUIREMENTS'] == 0:

            # Do not Check Tourney wins
            if card_name in vault['CARDS']:
                response = db.updateUserNoFilter(user_query, {'$set': {'CARD': str(card_name)}})
                await ctx.send(response)
            else:
                await ctx.send(m.USER_DOESNT_HAVE_THE_CARD, delete_after=5)
        else:

            # Check tourney wins
            tournament_wins = user['TOURNAMENT_WINS']
            card_query = {'TOURNAMENT_REQUIREMENTS': tournament_wins}

            if tournament_wins >= resp['TOURNAMENT_REQUIREMENTS']:
                if card_name in vault['CARDS']:
                    response = db.updateUserNoFilter(user_query, {'$set': {'CARD': str(card_name)}})
                    await ctx.send(response)
                else:
                    await ctx.send(m.USER_DOESNT_HAVE_THE_CARD, delete_after=5)
            else:
                return "Unable to update card."

    @commands.command()
    async def vc(self, ctx, *args):
        card_name = " ".join([*args])
        card = db.queryCard({'NAME':str(card_name)})
        if card:
            o_card = card['NAME']
            o_card_path=card['PATH']
            o_max_health = card['HLT']
            o_health = card['HLT']
            o_stamina = card['STAM']
            o_max_stamina = card['STAM']
            o_moveset = card['MOVESET']
            o_attack = card['ATK']
            o_defense = card['DEF']
            o_type = card['TYPE']
            o_accuracy = card['ACC']
            o_passive = card['PASS'][0]
            o_speed = card['SPD']
            o_show = card['SHOW']
            o_collection = card['COLLECTION']
            resolved = False
            focused = False
            title = {'TITLE': 'CARD PREVIEW'}
            card_file = showcard(card, o_max_health, o_health, o_max_stamina, o_stamina, resolved, title, focused)

            passive_name = list(o_passive.keys())[0]
            passive_num = list(o_passive.values())[0]
            passive_type = list(o_passive.values())[1]

            embedVar = discord.Embed(title=f"{o_card} Preview".format(self), description=f"Preview for {o_card} from {o_show}.", colour=000000)
            # embedVar.set_image(url=card_file)
            embedVar.add_field(name="Health", value=f"{o_max_health}")
            embedVar.add_field(name="Stamina", value=f"{o_max_stamina}")
            embedVar.add_field(name="Attack", value=f"{o_attack}")
            embedVar.add_field(name="Defense", value=f"{o_defense}")
            embedVar.add_field(name="Speed", value=f"{o_speed}")
            embedVar.add_field(name="Unique Passive", value=f"`{passive_name}: Increases {passive_type} by {passive_num}`", inline=False)

            await ctx.send(embed=embedVar)

            await ctx.send(file=card_file)
        else:
            await ctx.send(m.CARD_DOESNT_EXIST, delete_after=3)

    ''' Delete All Cards '''
    @commands.command()
    async def dac(self, ctx):
        user_query = {"DISNAME": str(ctx.author)}
        if ctx.author.guild_permissions.administrator == True:
            resp = db.deleteAllCards(user_query)
            await ctx.send(resp)
        else:
            await ctx.send(m.ADMIN_ONLY_COMMAND)

def setup(bot):
    bot.add_cog(Cards(bot))