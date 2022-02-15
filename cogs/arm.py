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

class Arm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Arm Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    # @cog_ext.cog_slash(description="Buy an Arm")
    # async def buyarm(self, ctx, arm: str):
    #     arm_name = arm
    #     vault_query = {'OWNER' : str(ctx.author)}
    #     vault = db.altQueryVault(vault_query)
    #     if len(vault['ARMS']) >= 25:
    #         await ctx.send("You're maxed out on Arms!", hidden=True)
    #         return
    #     shop = db.queryShopArms()
    #     arms = []
    #     arm_list = []
    #     for arm in vault['ARMS']:
    #         arm_list.append(arm['ARM'])
    #     rift_universes = ['Crown Rift Slayers', 'Crown Rift Awakening', 'Crown Rift Madness']
    #     riftShopOpen = False
    #     check_arm = db.queryArm({'ARM' : {"$regex": f"^{str(arm_name)}$", "$options": "i"}})
    #     arm_name = check_arm['ARM']
    #     if check_arm:
    #         if check_arm['UNIVERSE'] in rift_universes:
    #             await ctx.send("You are not connected to the rift...", hidden=True)
    #             return
    #         all_universes = db.queryAllUniverse()
    #         user = db.queryUser({'DID': str(ctx.author.id)})
    #         available_universes = []
    #         if user['RIFT'] == 1:
    #             riftShopOpen = True
    #         if riftShopOpen:    
    #             for uni in all_universes:
    #                 if uni['PREREQUISITE'] in user['CROWN_TALES']:
    #                     if uni['TIER'] != 9:
    #                         available_universes.append(uni['TITLE'])
    #                     elif uni['TITLE'] in user['CROWN_TALES']:
    #                         available_universes.append(uni['TITLE'])
    #         else:
    #             for uni in all_universes:
    #                 if uni['PREREQUISITE'] in user['CROWN_TALES'] and not uni['TIER'] == 9:
    #                     available_universes.append(uni['TITLE'])


    #     currentBalance = vault['BALANCE']
    #     cost = 0
    #     mintedArm = ""
    #     stock = 0
    #     newstock = 0
    #     armInStock = False
    #     checkout = True
    #     for arm in shop:

    #         if arm_name == arm['ARM']:
    #             if stock == arm['STOCK']:
    #                 checkout = armInStock
    #             else:
    #                 armInStock = True
    #                 mintedArm = arm['ARM']
    #                 cost = arm['PRICE']
    #                 stock = arm['STOCK']
    #                 newstock = stock - 1

    #     if bool(mintedArm):
    #         if mintedArm in arm_list:
    #             await ctx.send(m.USER_ALREADY_HAS_ARM, hidden=True)
    #         else:
    #             newBalance = currentBalance - cost

    #             if newBalance < 0 :
    #                 await ctx.send("You have an insufficent Balance", hidden=True)
    #             else:
    #                 await main.curse(cost, str(ctx.author))
    #                 arm_query = {'ARM' : str(mintedArm)}
    #                 armInventory = db.queryArm(arm_query)
    #                 update_query = {"$set": {"STOCK": newstock}} 
    #                 response = db.updateArm(armInventory, update_query)
    #                 response = db.updateVaultNoFilter(vault_query,{'$addToSet':{'ARMS': {'ARM': str(arm_name), 'DUR': 25}}})
    #                 await ctx.send(m.PURCHASE_COMPLETE_1 + f"`{newstock}` `{mintedArm}` ARMS left in the Shop!")

    #                 arm_buttons = [
    #                         manage_components.create_button(
    #                             style=ButtonStyle.blue,
    #                             label="Yes",
    #                             custom_id="Yes"
    #                         ),
    #                         manage_components.create_button(
    #                             style=ButtonStyle.red,
    #                             label="No",
    #                             custom_id="No"
    #                         )
    #                     ]
    #                 arm_buttons_action_row = manage_components.create_actionrow(*arm_buttons)
    #                 await ctx.send(f"{ctx.author.mention} would you like to equip this Arm?", components=[arm_buttons_action_row])

    #                 def check(button_ctx):
    #                     return button_ctx.author == ctx.author
    #                 try:
    #                     button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[arm_buttons_action_row], check=check)

    #                     if button_ctx.custom_id == "No":
    #                         await button_ctx.send("Did not equip arm.")
    #                         return

    #                     if button_ctx.custom_id == "Yes":
    #                         user_query = {'DID': str(ctx.author.id)}
    #                         response = db.updateUserNoFilter(user_query, {'$set': {'ARM': str(arm_name)}})
    #                         await button_ctx.send(response)
    #                 except:
    #                     return

    #     elif checkout == True:
    #         await ctx.send(m.ARM_DOESNT_EXIST, hidden=True)
    #     else:
    #         await ctx.send(m.ARM_OUT_OF_STOCK, hidden=True)

    @cog_ext.cog_slash(description="Equip an Arm")
    async def equiparm(self, ctx, arm: str):
        arm_name = arm
        user_query = {'DID': str(ctx.author.id)}
        user = db.queryUser(user_query)

        vault_query = {'DID' : str(ctx.author.id)}
        vault = db.altQueryVault(vault_query)

        resp = db.queryArm({'ARM': {"$regex": f"^{str(arm_name)}$", "$options": "i"}})
        
        if resp :
            try:
                arm_name = resp['ARM']
                owned = False
                for arm in vault['ARMS']:
                    if arm_name in arm['ARM']:
                        response = db.updateUserNoFilter(user_query, {'$set': {'ARM': str(arm_name)}})
                        owned = True
                        await ctx.send(response)
                if not owned:
                    await ctx.send(m.USER_DOESNT_HAVE_THE_ARM, hidden=True)
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
        else:
            await ctx.send("That arm doesn't exist.", hidden=True)
            return
           

    @cog_ext.cog_slash(description="View an Arm")
    async def viewarm(self, ctx, arm: str):
        arm_name = arm
        arm = db.queryArm({'ARM': {"$regex": f"^{str(arm_name)}$", "$options": "i"}})
        if arm:
            arm_arm = arm['ARM']
            arm_show = arm['UNIVERSE']
            arm_price = arm['PRICE']
            exclusive = arm['EXCLUSIVE']

            if arm_show != 'Unbound':
                arm_show_img = db.queryUniverse({'TITLE': arm_show})['PATH']
            arm_passive = arm['ABILITIES'][0]
                # Arm Passive
            o_arm_passive_type = list(arm_passive.keys())[0]
            o_arm_passive_value = list(arm_passive.values())[0]

            message=""
            
            price_message ="" 
            if exclusive:
                price_message = "_Priceless_"
            else:
                price_message = f"_Shop & Drop_"

            if o_arm_passive_type == 'BASIC':
                typetext = 'Basic'
                message=f"{arm_arm} is an BASIC arm"
            elif o_arm_passive_type == 'SPECIAL':
                typetext = 'Special'
                message=f"{arm_arm} is a SPECIAL arm"
            elif o_arm_passive_type == 'ULTIMATE':
                typetext = 'Ultimate'
                message=f"{arm_arm} is a ULTIMATE arm"
            elif o_arm_passive_type == 'ULTIMAX':
                typetext = 'Ultimax'
                message=f"{arm_arm} is a ULTIMAX arm"
            elif o_arm_passive_type == 'SHIELD':
                typetext = 'Shield'
                message=f"{arm_arm} is a SHIELD arm"
            elif o_arm_passive_type == 'BARRIER':
                typetext = 'Barrier'
                message=f"{arm_arm} is an BARRIER arm"
            elif o_arm_passive_type == 'PARRY':
                typetext = 'Parry'
                message=f"{arm_arm} is a PARRY arm"
            elif o_arm_passive_type == 'MANA':
                typetext = 'Mana'
                message=f"{arm_arm} is a MANA arm"



            embedVar = discord.Embed(title=f"{Crest_dict[arm_show]} {arm_arm}\n{price_message}".format(self), colour=000000)
            if arm_show != "Unbound":
                embedVar.set_thumbnail(url=arm_show_img)
            embedVar.add_field(name=f"Unique Passive", value=f"Increases {typetext} by **{o_arm_passive_value}**", inline=False)
            embedVar.set_footer(text=f"{o_arm_passive_type}: {enhancer_mapping[o_arm_passive_type]}")

            await ctx.send(embed=embedVar)

        else:
            await ctx.send(m.ARM_DOESNT_EXIST, hidden=True)

def setup(bot):
    bot.add_cog(Arm(bot))
    
Crest_dict = {'Unbound': ':ideograph_advantage:',
              'My Hero Academia': ':sparkle:',
              'League Of Legends': ':u6307:',
              'Kanto Region': ':chart:',
              'Naruto': ':u7121:',
              'Bleach': ':u6709:',
              'God Of War': ':u7533:',
              'Chainsawman': ':accept:',
              'One Punch Man': ':u55b6:',
              'Johto Region': ':u6708:',
              'Black Clover': ':ophiuchus:',
              'Demon Slayer': ':aries:',
              'Attack On Titan': ':taurus:',
              '7ds': ':capricorn:',
              'Hoenn Region': ':leo:',
              'Digimon': ':cancer:',
              'Fate': ':u6e80:',
              'Solo Leveling': ':u5408:',
              'Souls': ':sos:',
              'Dragon Ball Z': ':u5272:',
              'Sinnoh Region': ':u7981:',
              'Death Note': ':white_flower:',
              'Crown Rift Awakening': ':u7a7a:',
              'Crown Rift Slayers': ':sa:',
              'Crown Rift Madness': ':m:',
              'Persona': ':o:'}
enhancer_mapping = {'ATK': 'Increase Attack %',
'DEF': 'Increase Defense %',
'STAM': 'Increase Stamina',
'HLT': 'Heal yourself or companion',
'LIFE': 'Steal Health from Opponent',
'DRAIN': 'Drain Stamina from Opponent',
'FLOG': 'Steal Attack from Opponent',
'WITHER': 'Steal Defense from Opponent',
'RAGE': 'Lose Defense, Increase Attack',
'BRACE': 'Lose Attack, Increase Defense',
'BZRK': 'Lose Health, Increase Attack',
'CRYSTAL': 'Lose Health, Increase Defense',
'GROWTH': 'Lose Health, Increase Attack & Defense',
'STANCE': 'Swap your Attack & Defense, Increase Attack',
'CONFUSE': 'Swap Opponent Attack & Defense, Decrease Opponent Defense',
'BLINK': 'Decrease your  Stamina, Increase Target Stamina',
'SLOW': 'Decrease Opponent Stamina, Swap Stamina with Opponent',
'HASTE': ' Increase your Stamina, Swap Stamina with Opponent',
'FEAR': 'Decrease your Health, Decrease Opponent Attack and Defense',
'SOULCHAIN': 'You and Your Opponent Stamina Link',
'GAMBLE': 'You and Your Opponent Health Link',
'WAVE': 'Deal Damage, Decreases over time',
'CREATION': 'Heals you, Decreases over time',
'BLAST': 'Deals Damage, Increases over time',
'DESTRUCTION': 'Decreases Opponent Max Health, Increases over time',
'BASIC': 'Increase Basic Attack AP',
'SPECIAL': 'Increase Special Attack AP',
'ULTIMATE': 'Increase Ultimate Attack AP',
'ULTIMAX': 'Increase All AP Values',
'MANA': 'Increase Enchancer AP',
'SHIELD': 'Blocks Incoming DMG, until broken',
'BARRIER': 'Nullifies Incoming Attacks, until broken',
'PARRY': 'Returns 25% Damage, until broken',
'SIPHON': 'Heal for 10% DMG inflicted + AP'
}
enhancer_suffix_mapping = {'ATK': '%',
'DEF': '%',
'STAM': ' Flat',
'HLT': '%',
'LIFE': '%',
'DRAIN': ' Flat',
'FLOG': '%',
'WITHER': '%',
'RAGE': '%',
'BRACE': '%',
'BZRK': '%',
'CRYSTAL': '%',
'GROWTH': '%',
'STANCE': ' Flat',
'CONFUSE': ' Flat',
'BLINK': ' Flat',
'SLOW': ' Flat',
'HASTE': ' Flat',
'FEAR': '%',
'SOULCHAIN': ' Flat',
'GAMBLE': ' Flat',
'WAVE': ' Flat',
'CREATION': ' Flat',
'BLAST': ' Flat',
'DESTRUCTION': ' Flat',
'BASIC': ' Flat',
'SPECIAL': ' Flat',
'ULTIMATE': ' Flat',
'ULTIMAX': ' Flat',
'MANA': ' %',
'SHIELD': ' DMG 🌐',
'BARRIER': ' Blocks 💠',
'PARRY': ' Counters 🔄',
'SIPHON': ' Healing 💉'
}