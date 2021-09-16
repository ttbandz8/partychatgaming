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
from discord_slash import SlashCommand
from discord_slash.utils import manage_components
from discord_slash.model import ButtonStyle

class Titles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print('Titles Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @cog_ext.cog_slash(description="Buy a Title", guild_ids=main.guild_ids)
    async def buytitle(self, ctx, title: str):
        title_name = title
        vault_query = {'OWNER' : str(ctx.author)}
        vault = db.altQueryVault(vault_query)
        if len(vault['TITLES']) >= 150:
            await ctx.send("You're maxed out on Titles!")
            return

        shop = db.queryShopTitles()
        titles = []
        rift_universes = ['Crown Rift Slayers', 'Crown Rift Awakening', 'Crown Rift Madness']
        riftShopOpen = False
        check_title = db.queryTitle({'TITLE' : {"$regex": f"^{str(title)}$", "$options": "i"}})
        title_name = check_title['TITLE']
        if check_title:
            all_universes = db.queryAllUniverse()
            user = db.queryUser({'DISNAME': str(ctx.author)})
            available_universes = []
            if user['RIFT'] == 1:
                riftShopOpen = True
            if riftShopOpen:    
                for uni in all_universes:
                    if uni['PREREQUISITE'] in user['CROWN_TALES']:
                        if uni['TIER'] != 9:
                            available_universes.append(uni['TITLE'])
                        elif uni['TITLE'] in user['CROWN_TALES']:
                            available_universes.append(uni['TITLE'])
            else:
                for uni in all_universes:
                    if uni['PREREQUISITE'] in user['CROWN_TALES'] and not uni['TIER'] == 9:
                        available_universes.append(uni['TITLE'])
            if check_title['UNIVERSE'] not in available_universes:
                if check_title['UNIVERSE'] in rift_universes:
                    await ctx.send("You are not connected to the rift...")
                else:
                    await ctx.send("You cannot purchase titles from Universes you haven't unlocked or Rifts yet completed.")
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


                    title_buttons = [
                            manage_components.create_button(
                                style=ButtonStyle.blue,
                                label="Yes",
                                custom_id="Yes"
                            ),
                            manage_components.create_button(
                                style=ButtonStyle.red,
                                label="No",
                                custom_id="No"
                            )
                        ]
                    title_buttons_action_row = manage_components.create_actionrow(*title_buttons)
                    await ctx.send(f"{ctx.author.mention} would you like to equip this Title?", components=[title_buttons_action_row])

                    def check(button_ctx):
                        return button_ctx.author == ctx.author

                    try:
                        button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[title_buttons_action_row], check=check)
                        
                        if button_ctx.custom_id == "No":
                            await button_ctx.send("Did not equip title.")
                            return
                        
                        if button_ctx.custom_id == "Yes":
                            user_query = {'DISNAME': str(ctx.author)}
                            response = db.updateUserNoFilter(user_query, {'$set': {'TITLE': str(title_name)}})
                            await button_ctx.send(response)
                    except:
                        return

        elif checkout == True:
            await ctx.send(m.TITLE_DOESNT_EXIST)
        else:
            await ctx.send(m.TITLE_OUT_OF_STOCK)


    @cog_ext.cog_slash(description="Equip a Title", guild_ids=main.guild_ids)
    async def equiptitle(self, ctx, title: str):
        title_name = title
        user_query = {'DISNAME': str(ctx.author)}
        user = db.queryUser(user_query)

        vault_query = {'OWNER' : str(ctx.author)}
        vault = db.altQueryVault(vault_query)

        resp = db.queryTitle({'TITLE': {"$regex": f"^{str(title_name)}$", "$options": "i"}})
        title_name = resp['TITLE']

        if resp:

            if title_name in vault['TITLES']:
                response = db.updateUserNoFilter(user_query, {'$set': {'TITLE': title_name}})
                await ctx.send(response)
            else:
                await ctx.send(m.USER_DOESNT_HAVE_THE_Title)
        else:

            if title_name in vault['TITLES']:
                response = db.updateUserNoFilter(user_query, {'$set': {'TITLE': str(title_name)}})
                await ctx.send(response)
            else:
                await ctx.send(m.USER_DOESNT_HAVE_THE_Title)


    @cog_ext.cog_slash(description="View a Title", guild_ids=main.guild_ids)
    async def viewtitle(self, ctx, title: str):
        title_name = title
        title = db.queryTitle({'TITLE': {"$regex": f"^{str(title)}$", "$options": "i"}})
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
                price_message = f":coin: {'{:,}'.format(title_price)}"

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

def setup(bot):
    bot.add_cog(Titles(bot))