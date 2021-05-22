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
    async def buycard(self, ctx, *args: str):
        card_name = " ".join([*args])
        vault_query = {'OWNER' : str(ctx.author)}
        vault = db.altQueryVault(vault_query)
        shop = db.queryShopCards()
        cards = []

        currentBalance = vault['BALANCE']
        cost = 0
        mintedCard = ""
        stock = 0
        newstock = 0
        cardInStock = False
        checkout = True
        for card in shop:
            if card_name == card['NAME']:
                if stock == card['STOCK']:
                    checkout = cardInStock
                else:        
                    cardInStock == True           
                    mintedCard = card['NAME']
                    cost = card['PRICE']
                    stock = card['STOCK']
                    newstock = stock - 1
                    

        if bool(mintedCard):
            if mintedCard in vault['CARDS']:
                await ctx.send(m.USER_ALREADY_HAS_CARD, delete_after=5)
            else:
                newBalance = currentBalance - cost

                if newBalance < 0 :
                    await ctx.send("You have an insufficent Balance")
                else:
                    await main.curse(cost, str(ctx.author))
                    card_query = {'NAME' : str(mintedCard)}
                    cardInventory = db.queryCard(card_query)
                    update_query = {"$set": {"STOCK": newstock}} 
                    response = db.updateCard(cardInventory, update_query)
                    response = db.updateVaultNoFilter(vault_query,{'$addToSet':{'CARDS': str(card_name)}})
                    await ctx.send(m.PURCHASE_COMPLETE_1 + f"`{newstock}` `{mintedCard}` CARDS left in the Shop!")
        elif checkout == True:
            await ctx.send(m.CARD_DOESNT_EXIST)
        else:
            await ctx.send(m.CARD_OUT_OF_STOCK)

    @commands.command()
    async def updatecard(self, ctx, *args):
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
    async def viewcard(self, ctx, *args):
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
            o_show = card['UNIVERSE']
            show_img = db.queryUniverse({'TITLE': o_show})['PATH']
            o_collection = card['COLLECTION']
            resolved = False
            focused = False
            title = {'TITLE': 'CARD PREVIEW'}
            card_file = showcard(card, o_max_health, o_health, o_max_stamina, o_stamina, resolved, title, focused)

            passive_name = list(o_passive.keys())[0]
            passive_num = list(o_passive.values())[0]
            passive_type = list(o_passive.values())[1]

            o_1 = o_moveset[0]
            o_2 = o_moveset[1]
            o_3 = o_moveset[2]
            o_enhancer = o_moveset[3]
            
            # Move 1
            move1 = list(o_1.keys())[0]
            move1ap = list(o_1.values())[0]
            move1_stamina = list(o_1.values())[1]
            
            # Move 2
            move2 = list(o_2.keys())[0]
            move2ap = list(o_2.values())[0]
            move2_stamina = list(o_2.values())[1]

            # Move 3
            move3 = list(o_3.keys())[0]
            move3ap = list(o_3.values())[0]
            move3_stamina = list(o_3.values())[1]

            # Move Enhancer
            move4 = list(o_enhancer.keys())[0]
            move4ap = list(o_enhancer.values())[0]
            move4_stamina = list(o_enhancer.values())[1]
            move4enh = list(o_enhancer.values())[2]

            message = ""
            tip = ""
            if o_attack > o_defense:
                message = f"{o_card} is an offensive card. "
                tip="Equipping defensive titles and arms would help boost survivability"
            elif o_defense > o_attack:
                message = f"{o_card} is a defensive card. "
                tip="Equipping offensive titles and arms would help boost killability"              

            embedVar = discord.Embed(title=f"{o_card}".format(self), description=f"`{message}`", colour=000000)
            if o_show != "Unbound":
                embedVar.set_thumbnail(url=show_img)
            embedVar.add_field(name="Health", value=f"`{o_max_health}`")
            embedVar.add_field(name="Stamina", value=f"`{o_max_stamina}`")
            embedVar.add_field(name="Attack", value=f"`{o_attack}`")
            embedVar.add_field(name="Defense", value=f"`{o_defense}`")
            embedVar.add_field(name="Speed", value=f"`{o_speed}`")

            embedVar.add_field(name=f"{move1}", value=f"Power: `{move1ap}`", inline=False)
            embedVar.add_field(name=f"{move2}", value=f"Power: `{move2ap}`", inline=False)
            embedVar.add_field(name=f"{move3}", value=f"Power: `{move3ap}`", inline=False)

            embedVar.add_field(name="Unique Passive", value=f"`{passive_name}: Increases {passive_type} by {passive_num}`", inline=False)
            embedVar.set_footer(text=f"{tip}")
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