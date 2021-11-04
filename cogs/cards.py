import textwrap
import discord
from discord.ext import commands
import bot as main
import db
import classes as data
import messages as m
import numpy as np
import help_commands as h
import unique_traits as ut
import destiny as d
# Converters
from discord import User
from discord import Member
from PIL import Image, ImageFont, ImageDraw
import requests
import random
from .crownunlimited import showcard, enhancer_mapping, enhancer_suffix_mapping
from discord_slash import cog_ext, SlashContext
from discord_slash import SlashCommand
from discord_slash.utils import manage_components
from discord_slash.model import ButtonStyle

class Cards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print('Cards Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @cog_ext.cog_slash(description="Buy a Card", guild_ids=main.guild_ids)
    async def buycard(self, ctx, card: str):
        try:
            card_name = card
            vault_query = {'OWNER' : str(ctx.author)}
            vault = db.altQueryVault(vault_query)
            owned_card_levels_list = []
            if len(vault['CARDS']) >= 150:
                await ctx.send("You're maxed out on Cards!")
                return
                
            for c in vault['CARD_LEVELS']:
                owned_card_levels_list.append(c['CARD'])

            owned_destinies = []
            rift_universes = ['Crown Rift Slayers', 'Crown Rift Awakening', 'Crown Rift Madness']
            riftShopOpen = False
            for destiny in vault['DESTINY']:
                owned_destinies.append(destiny['NAME'])

            shop = db.queryShopCards()
            cards = []
            tier = 0

            check_card = db.queryCard({'NAME' : {"$regex": f"^{str(card)}$", "$options": "i"}})
            card_name = check_card['NAME']
            if check_card:
                if check_card['UNIVERSE'] == 'Unbound':
                    await ctx.send("You cannot purchase this card.")
                    return
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
                            # Add Tier
                        if uni['TITLE'] == check_card['UNIVERSE']:
                            tier = uni['TIER']
                if check_card['UNIVERSE'] not in available_universes:
                    if check_card['UNIVERSE'] in rift_universes:
                        await ctx.send("You are not connected to the rift...")
                    else:                   
                        await ctx.send("You cannot purchase Cards from Universes you haven't unlocked or Rifts yet completed.")
                    return
                if check_card['HAS_COLLECTION']:
                    await ctx.send("This card can not be purchased.")
                    return

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
                        
                        # Add Card Level config
                        if card_name not in owned_card_levels_list:
                            update_query = {'$addToSet': {'CARD_LEVELS': {'CARD': str(card_name), 'LVL': 0, 'TIER': int(tier), 'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0}}}        
                            r = db.updateVaultNoFilter(vault_query, update_query)
                        
                        await ctx.send(f"You Purchased **{mintedCard}**\n**{newstock}** {mintedCard} cards left in the Shop!")
                        # Add Destiny
                        for destiny in d.destiny:
                            if card_name in destiny["USE_CARDS"] and destiny['NAME'] not in owned_destinies:
                                db.updateVaultNoFilter(vault_query,{'$addToSet':{'DESTINY': destiny}})
                                await ctx.send(f"**DESTINY AWAITS!**\n**{destiny['NAME']}** has been added to your vault.")

                        card_buttons = [
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
                        card_buttons_action_row = manage_components.create_actionrow(*card_buttons)
                        await ctx.send(f"{ctx.author.mention} would you like to equip this Card?", components=[card_buttons_action_row])

                        def check(button_ctx):
                            return button_ctx.author == ctx.author

                        try:
                            button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[card_buttons_action_row], check=check)

                            if button_ctx.custom_id == "No":
                                await button_ctx.send("Did not equip card.")
                                return

                            if button_ctx.custom_id == "Yes":
                                user_query = {'DISNAME': str(ctx.author)}
                                response = db.updateUserNoFilter(user_query, {'$set': {'CARD': str(card_name)}})
                                await button_ctx.send(response)
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

            elif checkout == True:
                await ctx.send(m.CARD_DOESNT_EXIST)
            else:
                await ctx.send(m.CARD_OUT_OF_STOCK)
        except Exception as e:
            await ctx.send(f"Failure to purchase card: {e}")
            return

    @cog_ext.cog_slash(description="Equip a Card", guild_ids=main.guild_ids)
    async def equipcard(self, ctx, card: str):
        card_name = card
        user_query = {'DISNAME': str(ctx.author)}
        user = db.queryUser(user_query)

        vault_query = {'OWNER' : str(ctx.author)}
        vault = db.altQueryVault(vault_query)

        resp = db.queryCard({'NAME': {"$regex": f"^{str(card)}$", "$options": "i"}})

        card_name = resp["NAME"]
        # Do not Check Tourney wins
        if card_name in vault['CARDS']:
            response = db.updateUserNoFilter(user_query, {'$set': {'CARD': str(card_name)}})
            await ctx.send(response)
        else:
            await ctx.send(m.USER_DOESNT_HAVE_THE_CARD, delete_after=5)
        
    @cog_ext.cog_slash(description="View a Card", guild_ids=main.guild_ids)
    async def viewcard(self, ctx, card: str):
        card_name = card
        card = db.queryCard({'NAME': {"$regex": f"^{str(card_name)}$", "$options": "i"}})
        if card:
            o_card = card['NAME']
            o_card_path=card['PATH']
            o_price=card['PRICE']
            o_exclusive = card['EXCLUSIVE']
            o_available = card['AVAILABLE']
            o_max_health = card['HLT']
            o_health = card['HLT']
            o_stamina = card['STAM']
            o_max_stamina = card['STAM']
            o_moveset = card['MOVESET']
            o_attack = card['ATK']
            o_defense = card['DEF']
            o_type = card['TYPE']
            o_passive = card['PASS'][0]
            o_speed = card['SPD']
            o_show = card['UNIVERSE']
            o_has_collection = card['HAS_COLLECTION']
            traits = ut.traits
            show_img = db.queryUniverse({'TITLE': o_show})['PATH']
            o_collection = card['COLLECTION']
            resolved = False
            focused = False
            dungeon = False
            title = {'TITLE': 'CARD PREVIEW'}

            if o_show == "Unbound":
                await ctx.send("You cannot view this card at this time. ")
                return 
            
            price_message ="" 
            card_icon =""
            if o_exclusive or o_has_collection:
                if o_has_collection ==True:
                    price_message = "_Priceless_"
                    card_icon= f":sparkles:"
                else:
                    price_message = "_Priceless_"
                    card_icon= f":fire:"
                    dungeon = True
            elif o_exclusive ==False and o_available == False and o_has_collection == False:
                price_message = "_Priceless_"
                card_icon= f":japanese_ogre:"
            else:
                price_message = f":coin: {'{:,}'.format(o_price)}"
                card_icon= f":flower_playing_cards:"
            att = 0
            defe = 0
            turn = 0
            mytrait = {}
            traitmessage = ''
            for trait in traits:
                if trait['NAME'] == o_show:
                    mytrait = trait
                if o_show == 'Kanto Region' or o_show == 'Johto Region' or o_show == 'Kalos Region' or o_show == 'Unova Region' or o_show == 'Sinnoh Region' or o_show == 'Hoenn Region' or o_show == 'Galar Region' or o_show == 'Alola Region':
                    if trait['NAME'] == 'Pokemon':
                        mytrait = trait
            if mytrait:
                traitmessage = f"**{mytrait['EFFECT']}**: {mytrait['TRAIT']}"
            
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
            if o_has_collection==True or dungeon== True:
                if o_has_collection:
                    message = f"{o_card} is a Destiny card. "
                    tip=f"Complete {o_show} Destiny: {o_collection} to unlock this card"
                else:
                    message = f"{o_card} is a Dungeon card. "
                    tip=f"Find this card in the {o_show} /dungeon"
            elif o_has_collection == False and o_available == False and o_exclusive == False:
                message = f"{o_card} is a Boss card. "
                tip=f"Defeat the {o_show} /boss to earn this card"
            elif o_attack > o_defense:
                message = f"{o_card} is an offensive card. "
                tip="Equipping defensive /titles and /arms would help boost survivability"
            elif o_defense > o_attack:
                message = f"{o_card} is a defensive card. "
                tip="Equipping offensive /titles and /arms would help boost killability"              
            
            card_file = showcard(card, o_max_health, o_health, o_max_stamina, o_stamina, resolved, title, focused, o_attack, o_defense, turn, move1ap, move2ap, move3ap, move4ap, move4enh, 0)
            embedVar = discord.Embed(title=f"{card_icon} {price_message}".format(self), description=textwrap.dedent(f"""
            :drop_of_blood: _Passive:_ **{passive_name}:** {passive_type} by {passive_num}
            :infinity: {traitmessage}
            """), colour=000000)
            if o_show != "Unbound":
                embedVar.set_thumbnail(url=show_img)
            embedVar.set_footer(text=f"{tip}")
            await ctx.send(embed=embedVar, file=card_file)
            # await ctx.send(file=card_file)

        else:
            await ctx.send(m.CARD_DOESNT_EXIST, delete_after=3)

def setup(bot):
    bot.add_cog(Cards(bot))