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

    @cog_ext.cog_slash(description="Buy an Arm")
    async def buyarm(self, ctx, arm: str):
        arm_name = arm
        vault_query = {'OWNER' : str(ctx.author)}
        vault = db.altQueryVault(vault_query)
        if len(vault['ARMS']) >= 150:
            await ctx.send("You're maxed out on Arms!")
            return
        shop = db.queryShopArms()
        arms = []
        arm_list = []
        for arm in vault['ARMS']:
            arm_list.append(arm['ARM'])
        rift_universes = ['Crown Rift Slayers', 'Crown Rift Awakening', 'Crown Rift Madness']
        riftShopOpen = False
        check_arm = db.queryArm({'ARM' : {"$regex": f"^{str(arm_name)}$", "$options": "i"}})
        arm_name = check_arm['ARM']
        if check_arm:
            if check_arm['UNIVERSE'] in rift_universes:
                await ctx.send("You are not connected to the rift...")
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


        currentBalance = vault['BALANCE']
        cost = 0
        mintedArm = ""
        stock = 0
        newstock = 0
        armInStock = False
        checkout = True
        for arm in shop:

            if arm_name == arm['ARM']:
                if stock == arm['STOCK']:
                    checkout = armInStock
                else:
                    armInStock = True
                    mintedArm = arm['ARM']
                    cost = arm['PRICE']
                    stock = arm['STOCK']
                    newstock = stock - 1

        if bool(mintedArm):
            if mintedArm in arm_list:
                await ctx.send(m.USER_ALREADY_HAS_ARM, delete_after=5)
            else:
                newBalance = currentBalance - cost

                if newBalance < 0 :
                    await ctx.send("You have an insufficent Balance")
                else:
                    await main.curse(cost, str(ctx.author))
                    arm_query = {'ARM' : str(mintedArm)}
                    armInventory = db.queryArm(arm_query)
                    update_query = {"$set": {"STOCK": newstock}} 
                    response = db.updateArm(armInventory, update_query)
                    response = db.updateVaultNoFilter(vault_query,{'$addToSet':{'ARMS': {'ARM': str(arm_name), 'DUR': 25}}})
                    await ctx.send(m.PURCHASE_COMPLETE_1 + f"`{newstock}` `{mintedArm}` ARMS left in the Shop!")

                    arm_buttons = [
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
                    arm_buttons_action_row = manage_components.create_actionrow(*arm_buttons)
                    await ctx.send(f"{ctx.author.mention} would you like to equip this Arm?", components=[arm_buttons_action_row])

                    def check(button_ctx):
                        return button_ctx.author == ctx.author
                    try:
                        button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[arm_buttons_action_row], check=check)

                        if button_ctx.custom_id == "No":
                            await button_ctx.send("Did not equip arm.")
                            return

                        if button_ctx.custom_id == "Yes":
                            user_query = {'DISNAME': str(ctx.author)}
                            response = db.updateUserNoFilter(user_query, {'$set': {'ARM': str(arm_name)}})
                            await button_ctx.send(response)
                    except:
                        return

        elif checkout == True:
            await ctx.send(m.ARM_DOESNT_EXIST)
        else:
            await ctx.send(m.ARM_OUT_OF_STOCK)

    @cog_ext.cog_slash(description="Equip an Arm")
    async def equiparm(self, ctx, arm: str):
        arm_name = arm
        user_query = {'DISNAME': str(ctx.author)}
        user = db.queryUser(user_query)

        vault_query = {'OWNER' : str(ctx.author)}
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
                    await ctx.send(m.USER_DOESNT_HAVE_THE_ARM, delete_after=5)
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
            await ctx.send("That arm doesn't exist.", delete_after=5)
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
                price_message = f":coin: {'{:,}'.format(arm_price)}"

            if o_arm_passive_type == 'ATK':
                message=f"{arm_arm} is an ATK arm"
            elif o_arm_passive_type == 'DEF':
                message=f"{arm_arm} is a DEF arm"
            elif o_arm_passive_type == 'STAM':
                message=f"{arm_arm} is a STAM arm"
            elif o_arm_passive_type == 'HLT':
                message=f"{arm_arm} is a HLT arm"
            elif o_arm_passive_type == 'LIFE':
                message=f"{arm_arm} is a LIFE arm"
            elif o_arm_passive_type == 'DRAIN':
                message=f"{arm_arm} is an DRAIN arm"
            elif o_arm_passive_type == 'FLOG':
                message=f"{arm_arm} is a FLOG arm"
            elif o_arm_passive_type == 'WITHER':
                message=f"{arm_arm} is a WITHER arm"
            elif o_arm_passive_type == 'RAGE':
                message=f"{arm_arm} is a RAGE arm"
            elif o_arm_passive_type == 'BRACE':            
                message=f"{arm_arm} is a BRACE arm"
            elif o_arm_passive_type == 'BZRK':            
                message=f"{arm_arm} is a BZRK arm"
            elif o_arm_passive_type == 'CRYSTAL':            
                message=f"{arm_arm} is a CRYSTAL arm"
            elif o_arm_passive_type == 'GROWTH':            
                message=f"{arm_arm} is a GROWTH arm"
            elif o_arm_passive_type == 'STANCE':
                message=f"{arm_arm} is a STANCE arm"
            elif o_arm_passive_type == 'CONFUSE':
                message=f"{arm_arm} is a CONFUSE arm"
            elif o_arm_passive_type == 'BLINK':
                message=f"{arm_arm} is a BLINK arm"
            elif o_arm_passive_type == 'SLOW':
                message=f"{arm_arm} is a SLOW arm"
            elif o_arm_passive_type == 'HASTE':
                message=f"{arm_arm} is a HASTE arm" 
            elif o_arm_passive_type == 'SOULCHAIN':
                message=f"{arm_arm} is a SOULCHAIN arm"
            elif o_arm_passive_type == 'FEAR':
                message=f"{arm_arm} is a FEAR arm"
            elif o_arm_passive_type == 'GAMBLE':
                message=f"{arm_arm} is a GAMBLE arm"


            embedVar = discord.Embed(title=f"{arm_arm}\n{price_message}".format(self), colour=000000)
            if arm_show != "Unbound":
                embedVar.set_thumbnail(url=arm_show_img)
            embedVar.add_field(name="Unique Passive", value=f"`Increases {o_arm_passive_type} by {o_arm_passive_value}`", inline=False)
            embedVar.set_footer(text=f"/enhancers - Enhancement Menu")

            await ctx.send(embed=embedVar)

        else:
            await ctx.send(m.ARM_DOESNT_EXIST, delete_after=3)

def setup(bot):
    bot.add_cog(Arm(bot))