from itertools import filterfalse
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
import destiny as d
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
    async def trade(self, ctx: SlashContext, mode: str, player: User):
        try:
            buyer_name = player
            merchant = db.queryUser({'DISNAME': str(ctx.author)})
            buyer = db.queryUser({'DISNAME': str(buyer_name)})
            mvault = db.queryVault({'OWNER' : str(ctx.author)})
            trade_query={'MERCHANT': str(ctx.author) , 'BUYER' : str(player), 'OPEN' : True}
            if mode == 'New':
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
                    trade_buttons = [
                                manage_components.create_button(
                                    style=ButtonStyle.green,
                                    label="Accept",
                                    custom_id="yes"
                                ),
                                manage_components.create_button(
                                    style=ButtonStyle.red,
                                    label="Decline",
                                    custom_id="no"
                                )
                            ]
                    trade_buttons_action_row = manage_components.create_actionrow(*trade_buttons)
                    await ctx.send(f"{player.mention} Do you accept the **Trade Invite**?", components=[trade_buttons_action_row])
                    def check(button_ctx):
                        return button_ctx.author == player
                    try:
                        button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[trade_buttons_action_row], timeout=120, check=check)

                        if button_ctx.custom_id == "no":
                            await button_ctx.send("Trade **Declined**")
                            self.stop = True
                        if button_ctx.custom_id == "yes":
                            await button_ctx.send("Trade **Started**")
                            trade = db.createTrade(data.newTrade(trade_query))
                            mcards = ", ".join(trade['MCARDS'])
                            mtitles = ", ".join(trade['MTITLES'])
                            marms = ", ".join(trade['MARMS'])
                            msummons = ", ".join(trade['MSUMMONS'])

                            bcards = ", ".join(trade['BCARDS'])
                            btitles = ", ".join(trade['BTITLES'])
                            barms = ", ".join(trade['BARMS'])
                            bsummons = ", ".join(trade['BSUMMONS'])

                            if trade:
                                embedVar = discord.Embed(title= f"{merchant['NAME']}'s New Trade", description=textwrap.dedent(f"""
                                👨‍🏫 {trade['MERCHANT']} :coin: ~ {'{:,}'.format(trade['MCOIN'])}
                                🎴 {mcards}
                                🎗️ {mtitles}
                                🦾 {marms}
                                🧬 {msummons}
                                🤵{trade['BUYER']} :coin: ~ {'{:,}'.format(trade['BCOIN'])}
                                🎴 {bcards}
                                🎗️ {btitles}
                                🦾 {barms}
                                🧬 {bsummons}
                                """), colour=0x7289da)
                                embedVar.set_footer(text=f"Trade Tax: {trade['TAX']}")
                                await ctx.send(embed=embedVar)
                                mresp = db.updateUserNoFilter({'DISNAME':str(merchant['DISNAME'])},{'$set' : {'TRADING': True}})
                                bresp = db.updateUserNoFilter({'DISNAME':str(buyer['DISNAME'])},{'$set' : {'TRADING': True}})
                            else:
                                await ctx.send(f"{ctx.author.mention} Error Reach Out To Support")
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
            elif mode == 'Open':
                m_query = {'MERCHANT': str(ctx.author), 'OPEN': True}
                trade_check = db.queryTrade(m_query)
                mcards = ", ".join(trade_check['MCARDS'])
                mtitles = ", ".join(trade_check['MTITLES'])
                marms = ", ".join(trade_check['MARMS'])
                msummons = ", ".join(trade_check['MSUMMONS'])

                bcards = ", ".join(trade_check['BCARDS'])
                btitles = ", ".join(trade_check['BTITLES'])
                barms = ", ".join(trade_check['BARMS'])
                bsummons = ", ".join(trade_check['BSUMMONS'])

                if trade_check:
                    buyer = trade_check['BUYER']
                    buyer_info = db.queryUser({'DISNAME': str(buyer)})
                    embedVar = discord.Embed(title= f"{merchant['NAME']}'s Current Trade", description=textwrap.dedent(f"""
                    👨‍🏫 {trade_check['MERCHANT']} :coin: ~ {'{:,}'.format(trade_check['MCOIN'])}
                    🎴 {mcards}
                    🎗️ {mtitles}
                    🦾 {marms}
                    🧬 {msummons}
                    🤵{trade_check['BUYER']} :coin: ~ {'{:,}'.format(trade_check['BCOIN'])}
                    🎴 {bcards}
                    🎗️ {btitles}
                    🦾 {barms}
                    🧬 {bsummons}
                    """), colour=0x7289da)
                    embedVar.set_footer(text=f"Trade Tax: {trade_check['TAX']}")
                    trade_buttons = [
                                manage_components.create_button(
                                    style=ButtonStyle.green,
                                    label="Accept",
                                    custom_id="yes"
                                ),
                                manage_components.create_button(
                                    style=ButtonStyle.red,
                                    label="Decline",
                                    custom_id="no"
                                ),
                                manage_components.create_button(
                                    style=ButtonStyle.grey,
                                    label="Exit",
                                    custom_id="exit"
                                )
                            ]
                    trade_buttons_action_row = manage_components.create_actionrow(*trade_buttons)
                    await ctx.send(embed=embedVar, components=[trade_buttons_action_row])
                    #await ctx.send(f"{ctx.author.mention} do wish to **Cancel This Trade**?", components=[trade_buttons_action_row])
                    def check(button_ctx):
                        return button_ctx.author == ctx.author
                    try:
                        button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[trade_buttons_action_row], timeout=120, check=check)

                        if button_ctx.custom_id == "exit":
                            await button_ctx.send("No change to **Trade**")
                            self.stop = True
                        if button_ctx.custom_id == "no":
                            await button_ctx.send("Trade **Cancelled**")
                            
                            mresp = db.updateUserNoFilter({'DISNAME':str(merchant['DISNAME'])},{'$set' : {'TRADING': False}})
                            bresp = db.updateUserNoFilter({'DISNAME':str(buyer_info['DISNAME'])},{'$set' : {'TRADING': False}})                              
                            await main.bless(trade_check['MCOIN'], str(ctx.author))
                            await main.bless(trade_check['BCOIN'], str(trade_check['BUYER']))
                            resp = db.deleteTrade(trade_check)
                        if button_ctx.custom_id == "yes":
                            try:
                                await button_ctx.send("Processing Trade...")
                                m_cards = trade_check['MCARDS']
                                m_titles = trade_check['MTITLES']
                                m_arms = trade_check['MARMS']
                                m_summons = trade_check['MSUMMONS']
                                m_coins = trade_check['MCOIN']
                                b_cards = trade_check['BCARDS']
                                b_titles = trade_check['BTITLES']
                                b_arms = trade_check['BARMS']
                                b_summons = trade_check['BSUMMONS']
                                b_coins = trade_check['BCOIN']
                                tax = trade_check['TAX']
                                tax_split = tax/2
                                
                                m_destinies = mvault['DESTINY']
                                m_owned_destinies = []
                                for mdestiny in m_destinies:
                                    m_owned_destinies.append(mdestiny['NAME'])
                                b_destinies = bvault['DESTINY']
                                b_owned_destinies = []
                                for bdestiny in b_destinies:
                                    b_owned_destinies.append(bdestiny['NAME'])
                                    
                                m_card_levels = mvault['CARD_LEVELS']
                                b_card_levels = bvault['CARD_LEVELS']
                                card_level_exist =False
                                
                                m_fees = m_coins + tax_split
                                b_fees = b_coins + tax_split
                                
                                durability = 0
                                
                                m_cardlist = "\n".join(m_cards)
                                m_titlelist = "\n".join(m_titles)
                                m_armlist = "\n".join(m_arms)
                                m_summonlist = "\n".join(m_summons)
                                m_coin_diff = int(mvault['BALANCE']) - (int(mvault['BALANCE']) - m_fees + b_fees)
                                b_cardlist = "\n".join(b_cards)
                                b_titlelist = "\n".join(b_titles)
                                b_armlist = "\n".join(b_arms)
                                b_summonlist = "\n".join(b_summons)
                                b_coin_diff = int(bvault['BALANCE']) - (int(bvault['BALANCE']) - b_fees + m_fees)
                                
                                
                                
                                if m_fees > mvault['BALANCE']:
                                    await ctx.send(f"{ctx.author.mention} you need at least {'{:,}'.format(m_fees)} to cover your **Taxes** and **Trade**")
                                    return
                                if b_fees > mvault['BALANCE']:
                                    await ctx.send(f"{player.mention} you need at least {'{:,}'.format(b_fees)} to cover your **Taxes** and **Trade**")
                                    return
                                
                                for c in m_cards:
                                    for card_lvl in b_card_levels:
                                        if c == card_lvl['CARD']:
                                            card_level_exist=True
                                    if card_level_exist==False:
                                        update_query = {'$addToSet': {'CARD_LEVELS': {'CARD': str(c), 'LVL': 0, 'TIER': 0, 'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0}}}
                                        db.updateVaultNoFilter({'OWNER': str(buyer)}, update_query)
                                    db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$pull':{'CARDS': str(c)}})
                                    db.updateVaultNoFilter({'OWNER': str(buyer)},{'$addToSet':{'CARDS': str(c)}})
                                    
                                    for dest in d.destiny:
                                        if c in dest["USE_CARDS"] and dest['NAME'] not in b_owned_destinies:
                                            db.updateVaultNoFilter({'OWNER': str(buyer)},{'$addToSet':{'DESTINY': dest}})
                                            await ctx.send(f"**DESTINY AWAITS!**\n**{dest['NAME']}** has been added to your vault.")
                                
                                for t in m_titles:
                                    db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$pull':{'TITLES': str(t)}})
                                    db.updateVaultNoFilter({'OWNER': str(buyer)},{'$addToSet':{'TITLES': str(t)}})
                                    
                                for a in m_arms:
                                    dur = mvault['ARMS']
                                    for b in dur:
                                        if a == b['ARM']:
                                            print(a)
                                            durability = b['DUR']
                                            print(durability)
                                    db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$pull':{'ARMS': {'ARM': str(a)}}})
                                    db.updateVaultNoFilter({'OWNER': str(buyer)},{'$addToSet':{'ARMS': {'ARM': str(a), 'DUR': durability}}})
                                    
                                for s in m_summons:
                                    summons = mvault['PETS']
                                    for l in summons:
                                        if s == l['NAME']:
                                            level = l['LVL']
                                            xp = l['EXP']
                                            pet_ability = list(l.keys())[3]
                                            pet_ability_power = list(l.values())[3]
                                            pet_info = {'NAME': l['NAME'], 'LVL': l['LVL'], 'EXP': l['EXP'], pet_ability: pet_ability_power, 'TYPE': l['TYPE'], 'BOND': 0, 'BONDEXP': 0, 'PATH': l['PATH']}
                                    db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$pull':{'PETS': {'NAME': str(s)}}})
                                    db.updateVaultNoFilter({'OWNER': str(buyer)},{'$addToSet':{'PETS': pet_info }})
                                
                                #buyer  
                                card_level_exist=False
                                for c in b_cards:
                                    for card_lvl in m_card_levels:
                                        if c == card_lvl['CARD']:
                                            card_level_exist=True
                                    if card_level_exist==False:
                                        update_query = {'$addToSet': {'CARD_LEVELS': {'CARD': str(c), 'LVL': 0, 'TIER': 0, 'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0}}}
                                        db.updateVaultNoFilter({'OWNER': str(ctx.author)}, update_query)
                                    db.updateVaultNoFilter({'OWNER': str(buyer)},{'$pull':{'CARDS': str(c)}})
                                    db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$addToSet':{'CARDS': str(c)}})
                                    
                                    for dest in d.destiny:
                                        if c in dest["USE_CARDS"] and dest['NAME'] not in m_owned_destinies:
                                            db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$addToSet':{'DESTINY': dest}})
                                            await ctx.send(f"**DESTINY AWAITS!**\n**{dest['NAME']}** has been added to your vault.")
                                
                                for t in b_titles:
                                    db.updateVaultNoFilter({'OWNER': str(buyer)},{'$pull':{'TITLES': str(t)}})
                                    db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$addToSet':{'TITLES': str(t)}})
                                    
                                for a in b_arms:
                                    dur = bvault['ARMS']
                                    for b in dur:
                                        if a == b['ARM']:
                                            durability = b['DUR']
                                    db.updateVaultNoFilter({'OWNER': str(buyer)},{'$pull':{'ARMS': {'ARM': str(a)}}})
                                    db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$addToSet':{'ARMS': {'ARM': str(a), 'DUR': durability}}})
                                    
                                for s in b_summons:
                                    summons = bvault['PETS']
                                    for l in summons:
                                        if s == l['NAME']:
                                            level = l['LVL']
                                            xp = l['EXP']
                                            pet_ability = list(l.keys())[3]
                                            pet_ability_power = list(l.values())[3]
                                            pet_info = {'NAME': l['NAME'], 'LVL': l['LVL'], 'EXP': l['EXP'], pet_ability: pet_ability_power, 'TYPE': l['TYPE'], 'BOND': 0, 'BONDEXP': 0, 'PATH': l['PATH']}
                                    db.updateVaultNoFilter({'OWNER': str(buyer)},{'$pull':{'PETS': {'NAME': str(s)}}})
                                    db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$addToSet':{'PETS': pet_info }})
                                    
                                await main.curse(m_fees, str(ctx.author))
                                await main.curse(b_fees, str(buyer_info['DISNAME']))
                                await main.bless(b_coins, str(ctx.author))
                                await main.bless(m_coins, str(buyer_info['DISNAME']))
                                
                                await ctx.author.send(f"**SOLD**\n\n**CARDS SOLD**\n {m_cardlist}\n**TITLES SOLD**\n {m_titlelist}!\n**ARMS SOLD**\n {m_armlist}!\n**SUMMONS SOLD**\n {m_summonlist}!\n**TAX**\n {int(tax_split)}!\n**COIN DIFF**\n {m_coin_diff}!\n\n")
                                await ctx.author.send(f"\n\n**PURCHASED**\n\n**CARDS**\n {b_cardlist}\n**TITLES**\n {b_titlelist}!\n**ARMS**\n {b_armlist}!\n**SUMMONS**\n {b_summonlist}!")
                                await ctx.send(f"Trade Finished, {ctx.author.mention} Check your DMS for Receipt")
                                
                                
                                
                                    
                                resp = db.deleteTrade(trade_check)
                                self.stop = True
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
                        buyer = trade_check2['BUYER']
                        buyer_info = db.queryUser({'DISNAME': str(buyer)})
                        embedVar = discord.Embed(title= f"{buyer_info['NAME']}'s Current Trade", description=textwrap.dedent(f"""
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
                        
                        trade_buttons = [
                                manage_components.create_button(
                                    style=ButtonStyle.red,
                                    label="Decline",
                                    custom_id="no"
                                ),
                                manage_components.create_button(
                                    style=ButtonStyle.grey,
                                    label="Exit",
                                    custom_id="exit"
                                )
                            ]
                        trade_buttons_action_row = manage_components.create_actionrow(*trade_buttons)
                        await ctx.send(embed=embedVar, components=[trade_buttons_action_row])
                        #await ctx.send(f"{ctx.author.mention} do wish to **Cancel This Trade**?", components=[trade_buttons_action_row])
                        def check(button_ctx):
                            return button_ctx.author == ctx.author
                        try:
                            button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[trade_buttons_action_row], timeout=120)

                            if button_ctx.custom_id == "exit":
                                await button_ctx.send("No change to **Trade**")
                                self.stop = True
                            if button_ctx.custom_id == "no":
                                await button_ctx.send("Trade **Cancelled**")
                                mresp = db.updateUserNoFilter({'DISNAME':str(trade_check2['MERCHANT'])},{'$set' : {'TRADING': False}})
                                bresp = db.updateUserNoFilter({'DISNAME':str(trade_check2['BUYER'])},{'$set' : {'TRADING': False}})
                                await main.bless(trade_check2['MCOIN'], str(trade_check2['MERCHANT']))
                                await main.bless(trade_check2['BCOIN'], str(trade_check2['BUYER']))
                                resp = db.deleteTrade(trade_check2)
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
                                       name="Add Coins",
                                       value="add"
                                   ),
                                   create_choice(
                                       name="Remove Coins",
                                       value="del"
                                   )
                               ]
                           ),
                           create_option(
                               name="amount",
                               description="Total Coins",
                               option_type=3,
                               required=True
                           )
                       ]
        , guild_ids=main.guild_ids)
    async def tradecoins(self, ctx: SlashContext, mode : str, amount : int):            
        try:
            x = amount
            trade_mode = mode
            list_to_sell = []
            sell_price = 0
            trade_x = str(x)
            mvalidation =False
            bvalidation =False
            item = 'P'
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
            else:
                await ctx.send("Not Registered At All")
            if item == "P":
                if mode == 'add':
                    await ctx.send(f"**{x}** coins added to **Trade**")
                else:
                    await ctx.send(f"**{x}** coins removed from **Trade**")
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