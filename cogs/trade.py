import discord
from discord.ext import commands
import bot as main
import db
import classes as data
import messages as m
import numpy as np
import help_commands as h
import textwrap
import DiscordUtils
# Converters
from discord import User
from discord import Member
from PIL import Image, ImageFont, ImageDraw
import requests
from discord_slash import cog_ext, SlashContext
from discord_slash.utils import manage_components
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_commands import create_option, create_choice
from dinteractions_Paginator import Paginator

class Trade(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print('Trade Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)


    @cog_ext.cog_slash(description="Trade with another Player",
                       options=[
                           create_option(
                               name="mode",
                               description="Trading Options",
                               option_type=3,
                               required=True,
                               choices=[
                                   create_choice(
                                       name="New Trade",
                                       value="New"
                                   ),
                                   create_choice(
                                       name="Check Trade",
                                       value="Open"
                                   ),
                                   create_choice(
                                       name="Accept Trade",
                                       value="Accept"
                                   ),
                                   create_choice(
                                       name="Close Trade",
                                       value="Close"
                                   )
                               ]
                           ),
                           create_option(
                               name="player",
                               description="Buyer",
                               option_type=6,
                               required=True
                           )
                       ]
        , guild_ids=main.guild_ids)
    async def trade(self, ctx: SlashContext,mode : str, player: User):
        try:
            buyer_name = player
            merchant = db.queryUser({'DISNAME': str(ctx.author)})
            buyer = db.queryUser({'DISNAME': str(buyer_name)})
            m_status = merchant['TRADING']
            b_status = buyer['TRADING']
            trade_query={'MERCHANT': str(ctx.author) , 'BUYER' : str(player), 'OPEN' : True}
            if mode == 'New':
                mvault = db.queryVault({'OWNER' : str(ctx.author)})
                bvault = db.queryVault({'OWNER' : str(buyer)})
                m_query = {'MERCHANT': str(ctx.author), 'OPEN': True}
                b_query = {'BUYER': str(buyer), 'OPEN': True}
                m_check = db.queryTrade(m_query)
                b_check = db.queryTrade(b_query)
                if m_check or b_check:
                    if m_check:
                        await ctx.send(f"{ctx.author.mention} check your **Trade Status** close your current trade first!.")
                        return
                    await ctx.send(f"{buyer['NAME']} is currently trading! You can trade once they are done.")
                else:
                    trade = db.createTrade(data.newTrade(trade_query))
                    if trade:
                        embedVar = discord.Embed(title= f"{merchant['NAME']}'s New Trade", description=textwrap.dedent(f"""
                        👨‍🏫 {trade['MERCHANT']} :coin: ~ {'{:,}'.format(trade['MCOIN'])}
                        Cards : {trade['MCARDS']}
                        Titles : {trade['MTITLES']}
                        Arms : {trade['MARMS']}
                        Summons : {trade['MSUMMONS']}
                        🤵{trade['BUYER']} :coin: ~ {'{:,}'.format(trade['BCOIN'])}
                        Cards : {trade['BCARDS']}
                        Titles : {trade['BTITLES']}
                        Arms : {trade['BARMS']}
                        Summons : {trade['BSUMMONS']}
                        """), colour=0x7289da)
                        embedVar.set_footer(text=f"Trade Tax: {trade['TAX']}")
                        await ctx.send(embed=embedVar)
                        mresp = db.updateUserNoFilter({'DISNAME':str(merchant['DISNAME'])},{'$set' : {'TRADING': True}})
                        bresp = db.updateUserNoFilter({'DISNAME':str(buyer['DISNAME'])},{'$set' : {'TRADING': True}})
            elif mode =='Close':
                m_query = {'MERCHANT': str(ctx.author), 'OPEN': True}
                trade_check = db.queryTrade(m_query)
                if trade_check:
                    embedVar = discord.Embed(title= f"{merchant['NAME']}'s Current Trade", description=textwrap.dedent(f"""
                    👨‍🏫 {trade_check['MERCHANT']} :coin: ~ {'{:,}'.format(trade_check['MCOIN'])}
                    Cards : {trade_check['MCARDS']}
                    Titles : {trade_check['MTITLES']}
                    Arms : {trade_check['MARMS']}
                    Summons : {trade_check['MSUMMONS']}
                    🤵{trade_check['BUYER']} :coin: ~ {'{:,}'.format(trade_check['BCOIN'])}
                    Cards : {trade_check['BCARDS']}
                    Titles : {trade_check['BTITLES']}
                    Arms : {trade_check['BARMS']}
                    Summons : {trade_check['BSUMMONS']}
                    """), colour=0x7289da)
                    embedVar.set_footer(text=f"Trade Tax: {trade_check['TAX']}")
                    await ctx.send(embed=embedVar)
                    trade_buttons = [
                                manage_components.create_button(
                                    style=ButtonStyle.green,
                                    label="Yes",
                                    custom_id="yes"
                                ),
                                manage_components.create_button(
                                    style=ButtonStyle.red,
                                    label="No",
                                    custom_id="no"
                                )
                            ]
                    trade_buttons_action_row = manage_components.create_actionrow(*trade_buttons)
                    await ctx.send(f"{ctx.author.mention} do wish to **Cancel This Trade**?", components=[trade_buttons_action_row])
                    def check(button_ctx):
                        return button_ctx.author == ctx.author
                    try:
                        button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[trade_buttons_action_row], timeout=120)

                        if button_ctx.custom_id == "no":
                            await button_ctx.send("No change to **Trade**")
                            self.stop = True
                        if button_ctx.custom_id == "yes":
                            await button_ctx.send("Trade **Cancelled**")
                            
                            mresp = db.updateUserNoFilter({'DISNAME':str(merchant['DISNAME'])},{'$set' : {'TRADING': False}})
                            bresp = db.updateUserNoFilter({'DISNAME':str(buyer['DISNAME'])},{'$set' : {'TRADING': False}})
                            await main.bless(trade_check['MCOIN'], str(ctx.author))
                            await main.bless(trade_check['BCOIN'], str(player))
                            for m in trade_check['MTITLES']:
                                m_title_refund = db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$addToSet':{'TITLES': str(m)}})
                            for b in trade_check['BTITLES']:
                                m_title_refund = db.updateVaultNoFilter({'OWNER': str(player)},{'$addToSet':{'TITLES': str(b)}})
                                
                            resp = db.deleteTrade(trade_check)
                    except Exception as ex:
                        trace = []
                        tb = ex.__traceback__
                        while tb is not None:
                            trace.append({
                                "filename": tb.tb_frame.f_code.co_filename,
                                "name": tb.tb_frame.f_code.co_name,
                                "lineno": tb.tb_lineno
                            })
                            tb = tb.tb_next
                        print(str({
                            'type': type(ex).__name__,
                            'message': str(ex),
                            'trace': trace
                        }))
                        await ctx.send(f"ERROR:\nTYPE: {type(ex).__name__}\nMESSAGE: {str(ex)}\nLINE: {trace} ")
                        return
                else:
                    b_query = {'BUYER': str(ctx.author), 'OPEN': True}
                    trade_check2 = db.queryTrade(b_query)
                    if trade_check2:
                        embedVar = discord.Embed(title= f"{buyer['NAME']}'s Current Trade", description=textwrap.dedent(f"""
                        👨‍🏫 {trade_check2['MERCHANT']} :coin: ~ {'{:,}'.format(trade_check2['MCOIN'])}
                        Cards : {trade_check2['MCARDS']}
                        Titles : {trade_check2['MTITLES']}
                        Arms : {trade_check2['MARMS']}
                        Summons : {trade_check2['MSUMMONS']}
                        🤵{trade_check2['BUYER']} :coin: ~ {'{:,}'.format(trade_check2['BCOIN'])}
                        Cards : {trade_check2['BCARDS']}
                        Titles : {trade_check2['BTITLES']}
                        Arms : {trade_check2['BARMS']}
                        Summons : {trade_check2['BSUMMONS']}
                        """), colour=0x7289da)
                        embedVar.set_footer(text=f"Trade Tax: {trade_check2['TAX']}")
                        await ctx.send(embed=embedVar)
                        trade_buttons = [
                                manage_components.create_button(
                                    style=ButtonStyle.green,
                                    label="Yes",
                                    custom_id="yes"
                                ),
                                manage_components.create_button(
                                    style=ButtonStyle.red,
                                    label="No",
                                    custom_id="no"
                                )
                            ]
                        trade_buttons_action_row = manage_components.create_actionrow(*trade_buttons)
                        await ctx.send(f"{ctx.author.mention} do wish to **Cancel This Trade**?", components=[trade_buttons_action_row])
                        def check(button_ctx):
                            return button_ctx.author == ctx.author
                        try:
                            button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[trade_buttons_action_row], timeout=120)

                            if button_ctx.custom_id == "no":
                                await button_ctx.send("No change to **Trade**")
                                self.stop = True
                            if button_ctx.custom_id == "yes":
                                await button_ctx.send("Trade **Cancelled**")
                                resp = db.deleteTrade(trade_check2)
                                mresp = db.updateUserNoFilter({'DISNAME':str(merchant['DISNAME'])},{'$set' : {'TRADING': False}})
                                bresp = db.updateUserNoFilter({'DISNAME':str(buyer['DISNAME'])},{'$set' : {'TRADING': False}})
                        except Exception as ex:
                            trace = []
                            tb = ex.__traceback__
                            while tb is not None:
                                trace.append({
                                    "filename": tb.tb_frame.f_code.co_filename,
                                    "name": tb.tb_frame.f_code.co_name,
                                    "lineno": tb.tb_lineno
                                })
                                tb = tb.tb_next
                            print(str({
                                'type': type(ex).__name__,
                                'message': str(ex),
                                'trace': trace
                            }))
                            await ctx.send(f"ERROR:\nTYPE: {type(ex).__name__}\nMESSAGE: {str(ex)}\nLINE: {trace} ")
                            return
                    else:
                        await ctx.send(f"{ctx.author.mention} no **Open Trades** found! Happy Trading!")
            elif mode == 'Open':
                m_query = {'MERCHANT': str(ctx.author), 'OPEN': True}
                trade_check = db.queryTrade(m_query)
                if trade_check:
                    embedVar = discord.Embed(title= f"{merchant['NAME']}'s Current Trade", description=textwrap.dedent(f"""
                    👨‍🏫 {trade_check['MERCHANT']} :coin: ~ {'{:,}'.format(trade_check['MCOIN'])}
                    Cards : {trade_check['MCARDS']}
                    Titles : {trade_check['MTITLES']}
                    Arms : {trade_check['MARMS']}
                    Summons : {trade_check['MSUMMONS']}
                    🤵{trade_check['BUYER']} :coin: ~ {'{:,}'.format(trade_check['BCOIN'])}
                    Cards : {trade_check['BCARDS']}
                    Titles : {trade_check['BTITLES']}
                    Arms : {trade_check['BARMS']}
                    Summons : {trade_check['BSUMMONS']}
                    """), colour=0x7289da)
                    embedVar.set_footer(text=f"Trade Tax: {trade_check['TAX']}")
                    await ctx.send(embed=embedVar)
                else:
                    b_query = {'BUYER': str(ctx.author), 'OPEN': True}
                    trade_check2 = db.queryTrade(b_query)
                    if trade_check2:
                        embedVar = discord.Embed(title= f"{buyer['NAME']}'s Current Trade", description=textwrap.dedent(f"""
                        👨‍🏫 {trade_check2['MERCHANT']} :coin: ~ {'{:,}'.format(trade_check2['MCOIN'])}
                        Cards : {trade_check2['MCARDS']}
                        Titles : {trade_check2['MTITLES']}
                        Arms : {trade_check2['MARMS']}
                        Summons : {trade_check2['MSUMMONS']}
                        🤵{trade_check2['BUYER']} :coin: ~ {'{:,}'.format(trade_check2['BCOIN'])}
                        Cards : {trade_check2['BCARDS']}
                        Titles : {trade_check2['BTITLES']}
                        Arms : {trade_check2['BARMS']}
                        Summons : {trade_check2['BSUMMONS']}
                        """), colour=0x7289da)
                        embedVar.set_footer(text=f"Trade Tax: {trade_check2['TAX']}")
                        await ctx.send(embed=embedVar)
                    else:
                        await ctx.send(f"{ctx.author.mention} no **Open Trades** found! Happy Trading!")
            elif mode == "Accept":
                m_query = {'MERCHANT': str(ctx.author), 'OPEN': True}
                trade_check = db.queryTrade(m_query)
                selection=True
                if trade_check:
                    if str(player) != trade_check['BUYER']:
                        await ctx.send(f"{ctx.author.mention} Select the **Buyer** from your **Current Trade**")
                        selection=False
                    embedVar = discord.Embed(title= f"{trade_check['MERCHANT']} Finaliizing Trade", description=textwrap.dedent(f"""
                    👨‍🏫 {trade_check['MERCHANT']} :coin: ~ {'{:,}'.format(trade_check['MCOIN'])}
                    Cards : {trade_check['MCARDS']}
                    Titles : {trade_check['MTITLES']}
                    Arms : {trade_check['MARMS']}
                    Summons : {trade_check['MSUMMONS']}
                    🤵{trade_check['BUYER']} :coin: ~ {'{:,}'.format(trade_check['BCOIN'])}
                    Cards : {trade_check['BCARDS']}
                    Titles : {trade_check['BTITLES']}
                    Arms : {trade_check['BARMS']}
                    Summons : {trade_check['BSUMMONS']}
                    """), colour=0x7289da)
                    embedVar.set_footer(text=f"Trade Tax: {trade_check['TAX']}")                   
                    await ctx.send(embed=embedVar)
                    if selection==False:
                        return
                    trade_buttons = [
                                manage_components.create_button(
                                    style=ButtonStyle.green,
                                    label="Yes",
                                    custom_id="yes"
                                ),
                                manage_components.create_button(
                                    style=ButtonStyle.red,
                                    label="No",
                                    custom_id="no"
                                )
                            ]
                    trade_buttons_action_row = manage_components.create_actionrow(*trade_buttons)
                    await ctx.send(f"{player.mention} do you accept the **Trade**?", components=[trade_buttons_action_row])
                    def check(button_ctx):
                        return button_ctx.author == ctx.author
                    try:
                        button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[trade_buttons_action_row], timeout=120)

                        if button_ctx.custom_id == "no":
                            await button_ctx.send("Trade **Denied**. ")
                            self.stop = True
                        if button_ctx.custom_id == "yes":
                            await button_ctx.send("Trade **Accepted**")
                    except Exception as ex:
                        trace = []
                        tb = ex.__traceback__
                        while tb is not None:
                            trace.append({
                                "filename": tb.tb_frame.f_code.co_filename,
                                "name": tb.tb_frame.f_code.co_name,
                                "lineno": tb.tb_lineno
                            })
                            tb = tb.tb_next
                        print(str({
                            'type': type(ex).__name__,
                            'message': str(ex),
                            'trace': trace
                        }))
                        await ctx.send(f"ERROR:\nTYPE: {type(ex).__name__}\nMESSAGE: {str(ex)}\nLINE: {trace} ")
                        return
            else:
                print("error")
        
        except Exception as ex:
            trace = []
            tb = ex.__traceback__
            while tb is not None:
                trace.append({
                    "filename": tb.tb_frame.f_code.co_filename,
                    "name": tb.tb_frame.f_code.co_name,
                    "lineno": tb.tb_lineno
                })
                tb = tb.tb_next
            print(str({
                'type': type(ex).__name__,
                'message': str(ex),
                'trace': trace
            }))
            await ctx.send(f"ERROR:\nTYPE: {type(ex).__name__}\nMESSAGE: {str(ex)}\nLINE: {trace} ")
            return
        
        
    @cog_ext.cog_slash(description="Add Items to Current Trade",
                       options=[
                           create_option(
                               name="mode",
                               description="Item Type",
                               option_type=3,
                               required=True,
                               choices=[
                                   create_choice(
                                       name="Add",
                                       value="add"
                                   ),
                                   create_choice(
                                       name="Remove",
                                       value="del"
                                   )
                               ]
                           ),
                           create_option(
                               name="item",
                               description="Item Type",
                               option_type=3,
                               required=True,
                               choices=[
                                   create_choice(
                                       name="Cards",
                                       value="C"
                                   ),
                                   create_choice(
                                       name="Titles",
                                       value="T"
                                   ),
                                   create_choice(
                                       name="Arms",
                                       value="A"
                                   ),
                                   create_choice(
                                       name="Summons",
                                       value="S"
                                   ),
                                   create_choice(
                                       name="Coins",
                                       value="P"
                                   )
                               ]
                           ),
                           create_option(
                               name="x",
                               description="Amount: 9999, Items :3, 22, 15",
                               option_type=3,
                               required=True
                           )
                       ]
        , guild_ids=main.guild_ids)
    async def tradeitem(self, ctx: SlashContext, mode : str, item : str, x : str):            
        try:
            trade_mode = mode
            trade_type = item
            list_to_sell = []
            sell_price = 0
            trade_x = str(x)
            mvalidation =False
            bvalidation =False
            user = db.queryUser({'DISNAME': str(ctx.author)})
            if user:
                vault = db.queryVault({'OWNER': str(ctx.author)})
                if vault:
                    mtrade = db.queryTrade({'MERCHANT' : str(ctx.author), 'OPEN' : True})
                    if mtrade:
                        mvalidation=True
                    else:
                        btrade = db.queryTrade({'BUYER' : str(ctx.author), 'OPEN' : True})
                        if btrade:
                            bvalidation=True
                        else:
                            await ctx.send(f"{ctx.author.mention} use **/trade** to open a **trade**")
                            return
                else:
                    await ctx.send("Error with your **Vault** please seek support!")
            else:
                await ctx.send("Not Registered")
            if mvalidation == True or bvalidation ==True:    #If user is valid and has vault
                tax = .10
                cards = vault['CARDS']
                titles = vault['TITLES']
                arms = vault['ARMS']
                arms_names_list = []

                for arm in arms:
                    arms_names_list.append(arm['ARM'])
                pets = vault['PETS']
                balance = vault['BALANCE']
                owned_destinies = []
                for destiny in vault['DESTINY']:
                    owned_destinies.append(destiny['NAME'])

                active_pet = {}
                pet_names = []
                for pet in pets:
                    pet_names.append(pet['NAME'])
                    if pet['NAME'] in str.split(x):
                        pet_ability = list(pet.keys())[3]
                        pet_ability_power = list(pet.values())[3]
                        active_pet = {'NAME': pet['NAME'], 'LVL': pet['LVL'], 'EXP': pet['EXP'], pet_ability: pet_ability_power, 'TYPE': pet['TYPE'], 'BOND': 0, 'BONDEXP': 0, 'PATH': pet['PATH']}
                if item == 'P':
                    coins = abs(int(x))
                    bank = vault['BALANCE']
                    if mode == 'add':
                        if bank >= int(x):
                            await main.curse(coins, ctx.author)
                            if mvalidation ==True:
                                trade_query = {'MERCHANT' : str(ctx.author), 'BUYER' : str(mtrade['BUYER']), 'OPEN' : True}
                                update_query = {"$inc" : {'MCOIN': int(coins)}}
                                resp = db.updateTrade(mtrade, update_query)
                            elif bvalidation==True:
                                trade_query = {'MERCHANT' : str(btrade['MERCHANT']),'BUYER' : str(ctx.author), 'OPEN' : True}
                                update_query = {"$inc" : {'BCOIN': int(coins)}}
                                resp = db.updateTrade(btrade, update_query)
                            else:
                                return
                        else:
                            ctx.send("You Broke. **Go Grind**")
                    elif mode == 'del':
                        trade_coins = 0
                        receipt = abs(int(x))
                        if mvalidation ==True:
                            trade_coins = mtrade['MCOIN']
                        elif bvalidation ==True:
                            trade_coins =btrade['BCOIN']
                        if trade_coins >= receipt:
                            refund = receipt
                            await main.bless(refund, ctx.author)
                            if mvalidation:
                                write_off = 0 - refund
                                trade_query = {'MERCHANT' : str(ctx.author), 'BUYER' : str(mtrade['BUYER']), 'OPEN' : True}
                                update_query = {"$inc" : {'MCOIN': int(write_off)}}
                                resp = db.updateTrade(trade_query, update_query)
                            elif bvalidation:
                                write_off = 0 - refund
                                trade_query = {'MERCHANT' : str(btrade['MERCHANT']),'BUYER' : str(ctx.author), 'OPEN' : True}
                                update_query = {"$inc" : {'BCOIN': int(write_off)}}
                                resp = db.updateTrade(trade_query, update_query)
                            else:
                                return
                        else:
                            await ctx.send("Hmm.. You didn't put that much in did you?")
                    else:
                        await ctx.send("Pick an option!")                     
                        
                elif item == 'T':
                    if mode == 'add':
                        titles = vault['TITLES']
                        tlist = trade_x.split(',')
                        for t in tlist:
                            title = titles[int(t)]
                            if title not in list_to_sell and title != user["TITLE"]:
                                title_data = db.queryTitle({'TITLE':{"$regex": str(title), "$options": "i"}})
                                sell_price = sell_price + (title_data['PRICE'] * tax)
                                list_to_sell.append(f"{str(title)}")
                        for title in list_to_sell:
                            db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$pull':{'TITLES': str(title)}})
                        if mvalidation:
                            trade_query = {'MERCHANT' : str(ctx.author), 'BUYER' : str(mtrade['BUYER']), 'OPEN' : True}
                            for title in list_to_sell:
                                update_query = {"$push" : {'MTITLES': title}, "$inc" : {'TAX' : int(sell_price)}}
                                resp = db.updateTrade(trade_query, update_query)
                        elif bvalidation:
                            trade_query = {'MERCHANT' : str(btrade['MERCHANT']),'BUYER' : str(ctx.author), 'OPEN' : True}
                            for title in list_to_sell:
                                update_query = {"$push" : {'BTITLES': title}, "$inc" : {'TAX' : int(sell_price)}}
                                resp = db.updateTrade(trade_query, update_query)
                    elif mode == 'del':
                        if mvalidation ==True:
                            trade_titles = mtrade['MTITLES']
                        elif bvalidation ==True:
                            trade_titles =btrade['BTITLES']
                        owned_titles = vault['TITLES']
                        refund_titles = trade_titles
                        print(refund_titles)
                        rlist = trade_x.split(',')
                        print(rlist)
                        for r in rlist:
                            refund = refund_titles[int(r)]
                            if refund not in owned_titles:
                                title_data = db.queryTitle({'TITLE':{"$regex": str(title), "$options": "i"}})
                                sell_price = sell_price + (title_data['PRICE'] * tax)
                                list_to_sell.append(f"{str(title)}")
                        
                    else:
                        ctx.send("Please Select a Default Mode!")
                    
                    
                    
                elif item == 'A':
                    print("a")
                elif item == 'C':
                    print("c")
                elif item == 'S':
                    print("s")
                else:
                    print("else")
            else:
                await ctx.send("Not Registered At All")
            if item == "P":
                if mode == 'add':
                    await ctx.send(f"**{x}** coins added to **Trade**")
                else:
                    await ctx.send(f"**{x}** coins removed from **Trade**")
            elif item == "T":
                for titles in list_to_sell:
                    await ctx.send(f"Title: **{titles}** added to **Trade**")
            else:
                await ctx.send("Item Added")
        except Exception as ex:
            trace = []
            tb = ex.__traceback__
            while tb is not None:
                trace.append({
                    "filename": tb.tb_frame.f_code.co_filename,
                    "name": tb.tb_frame.f_code.co_name,
                    "lineno": tb.tb_lineno
                })
                tb = tb.tb_next
            print(str({
                'type': type(ex).__name__,
                'message': str(ex),
                'trace': trace
            }))
            await ctx.send(f"ERROR:\nTYPE: {type(ex).__name__}\nMESSAGE: {str(ex)}\nLINE: {trace} ")
            return

def setup(bot):
    bot.add_cog(Trade(bot))