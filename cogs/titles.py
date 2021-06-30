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
    async def nt(self, ctx, *args):
        if ctx.author.guild_permissions.administrator == True:
            title = " ".join([*args])
            title_query = {'TITLE': str(title), 'TOURNAMENT_REQUIREMENTS': 0, 'PRICE': 500}
            added = db.createTitle(data.newTitle(title_query))
            await ctx.send(added)
        else:
            print(m.ADMIN_ONLY_COMMAND)


    @commands.command()
    async def buytitle(self, ctx, *args: str):
        title_name=" ".join([*args])
        vault_query = {'OWNER' : str(ctx.author)}
        vault = db.altQueryVault(vault_query)
        shop = db.queryShopTitles()
        titles = []

        check_title = db.queryTitle({'TITLE' : str(title_name)})
        if check_title:
            all_universes = db.queryAllUniverse()
            user = db.queryUser({'DISNAME': str(ctx.author)})
            available_universes = []
            for uni in all_universes:
                if uni['PREREQUISITE'] in user['CROWN_TALES']:
                    available_universes.append(uni['TITLE'])
            if check_title['UNIVERSE'] not in available_universes:
                await ctx.send("You cannot purchase titles from Universes you haven't unlocked.")
                return

        currentBalance = vault['BALANCE']
        cost = 0
        mintedTitle = ""
        stock = 0
        newstock = 0
        titleInStock = False
        checkout = True
        for title in shop:

            if title_name == title['TITLE']:
                if stock == title['STOCK']:
                    checkout = titleInStock
                else:
                    titleInStock = True
                    mintedTitle = title['TITLE']
                    cost = title['PRICE']
                    stock = title['STOCK']
                    newstock = stock - 1

        if bool(mintedTitle):
            if mintedTitle in vault['TITLES']:
                await ctx.send(m.USER_ALREADY_HAS_TITLE, delete_after=5)
            else:
                newBalance = currentBalance - cost

                if newBalance < 0 :
                    await ctx.send("You have an insufficent Balance")
                else:
                    await main.curse(cost, str(ctx.author))
                    title_query = {'TITLE' : str(mintedTitle)}
                    titleInventory = db.queryTitle(title_query)
                    update_query = {"$set": {"STOCK": newstock}} 
                    response = db.updateTitle(titleInventory, update_query)
                    response = db.updateVaultNoFilter(vault_query,{'$addToSet':{'TITLES': str(title_name)}})
                    await ctx.send(m.PURCHASE_COMPLETE_1 + f"`{newstock}` `{mintedTitle}` TITLES left in the Shop!")



                    accept = await ctx.send(f"{ctx.author.mention} would you like to equip this Title?")
                    emojis = ['👍', '👎']
                    for emoji in emojis:
                        await accept.add_reaction(emoji)

                    def check(reaction, user):
                        return user == ctx.author and str(reaction.emoji) == '👍'
                    try:
                        user_query = {'DISNAME': str(ctx.author)}
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=25.0, check=check)
                        response = db.updateUserNoFilter(user_query, {'$set': {'TITLE': str(title_name)}})
                        await ctx.send(response)
                    except:
                        return

        elif checkout == True:
            await ctx.send(m.TITLE_DOESNT_EXIST)
        else:
            await ctx.send(m.TITLE_OUT_OF_STOCK)

    @commands.command()
    async def equiptitle(self, ctx, *args):
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
                await ctx.send(m.USER_DOESNT_HAVE_THE_Title)
        else:

            # Check tourney wins
            tournament_wins = user['TOURNAMENT_WINS']
            title_query = {'TOURNAMENT_REQUIREMENTS': tournament_wins}

            if tournament_wins >= resp['TOURNAMENT_REQUIREMENTS']:
                if title_name in vault['TITLES']:
                    response = db.updateUserNoFilter(user_query, {'$set': {'TITLE': str(title_name)}})
                    await ctx.send(response)
                else:
                    await ctx.send(m.USER_DOESNT_HAVE_THE_Title)
            else:
                return "Unable to update Title."

    @commands.command()
    async def viewtitle(self, ctx, *args):
        title_name = " ".join([*args])
        title = db.queryTitle({'TITLE': str(title_name)})
        if title:
            title_title = title['TITLE']
            title_show = title['UNIVERSE']
            title_price = title['PRICE']
            exclusive = title['EXCLUSIVE']

            if title_show != 'Unbound':
                title_img = db.queryUniverse({'TITLE': title_show})['PATH']
            title_passive = title['ABILITIES'][0]
                # Title Passive
            o_title_passive_type = list(title_passive.keys())[0]
            o_title_passive_value = list(title_passive.values())[0]
            
            message=""

            price_message ="" 
            if exclusive:
                price_message = "_Priceless_"
            else:
                price_message = f":coin: {title_price}"

            if o_title_passive_type == 'ATK':
                message=f"{title_title} is an ATK title"
            elif o_title_passive_type == 'DEF':
                message=f"{title_title} is a DEF title"
            elif o_title_passive_type == 'STAM':
                message=f"{title_title} is a STAM title"
            elif o_title_passive_type == 'HLT':
                message=f"{title_title} is a HLT title"
            elif o_title_passive_type == 'LIFE':
                message=f"{title_title} is a LIFE title"
            elif o_title_passive_type == 'DRAIN':
                message=f"{title_title} is a DRAIN title"
            elif o_title_passive_type == 'FLOG':
                message=f"{title_title} is a FLOG title"
            elif o_title_passive_type == 'WITHER':
                message=f"{title_title} is a WITHER title"
            elif o_title_passive_type == 'RAGE':
                message=f"{title_title} is a RAGE title"
            elif o_title_passive_type == 'BRACE':            
                message=f"{title_title} is a BRACE title"
            elif o_title_passive_type == 'BZRK':            
                message=f"{title_title} is a BZRK title"
            elif o_title_passive_type == 'CRYSTAL':            
                message=f"{title_title} is a CRYSTAL title"
            elif o_title_passive_type == 'GROWTH':            
                message=f"{title_title} is a GROWTH title"
            elif o_title_passive_type == 'STANCE':
                message=f"{title_title} is a STANCE title"
            elif o_title_passive_type == 'CONFUSE':
                message=f"{title_title} is a CONFUSE title"
            elif o_title_passive_type == 'BLINK':
                message=f"{title_title} is a BLINK title"
            elif o_title_passive_type == 'SLOW':
                message=f"{title_title} is a SLOW title"
            elif o_title_passive_type == 'HASTE':
                message=f"{title_title} is a HASTE title" 
            elif o_title_passive_type == 'SOULCHAIN':
                message=f"{title_title} is a SOULCHAIN title"
            elif o_title_passive_type == 'FEAR':
                message=f"{title_title} is a FEAR title"
            elif o_title_passive_type == 'GAMBLE':
                message=f"{title_title} is a GAMBLE title" 

            embedVar = discord.Embed(title=f"{title_title}\n{price_message}".format(self), colour=000000)
            if title_show != "Unbound":
                embedVar.set_thumbnail(url=title_img)
            embedVar.add_field(name="Unique Passive", value=f"`Increases {o_title_passive_type} by {o_title_passive_value}`", inline=False)
            embedVar.set_footer(text=f".enhance - Enhancement Menu")

            await ctx.send(embed=embedVar)

        else:
            await ctx.send("That title doesn't exist.", delete_after=3)

    ''' Delete All Titles '''
    # @commands.command()
    # async def dat(self, ctx):
    #     user_query = {"DISNAME": str(ctx.author)}
    #     if ctx.author.guild_permissions.administrator == True:
    #         resp = db.deleteAllTitles(user_query)
    #         await ctx.send(resp)
    #     else:
    #         await ctx.send(m.ADMIN_ONLY_COMMAND)

def setup(bot):
    bot.add_cog(Titles(bot))