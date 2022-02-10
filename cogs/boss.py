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
from discord_slash import cog_ext, SlashContext

class Boss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print('Boss Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @cog_ext.cog_slash(description="View a Boss", guild_ids=main.guild_ids)
    async def viewboss(self, ctx, boss : str):
        try:
            uboss_name = boss
            uboss = db.queryBoss({'NAME': {"$regex": str(uboss_name), "$options": "i"}})
            if uboss:
                uboss_name = uboss['NAME']
                uboss_show = uboss['UNIVERSE']
                uboss_title = uboss['TITLE']
                uboss_arm = uboss['ARM']
                uboss_desc = uboss['DESCRIPTION'][3]
                uboss_pic = uboss['PATH']
                uboss_pet = uboss['PET']

                arm = db.queryArm({'ARM': uboss_arm})
                arm_passive = arm['ABILITIES'][0]
                arm_passive_type = list(arm_passive.keys())[0]
                arm_passive_value = list(arm_passive.values())[0]

                title = db.queryTitle({'TITLE': uboss_title})
                title_passive = title['ABILITIES'][0]
                title_passive_type = list(title_passive.keys())[0]
                title_passive_value = list(title_passive.values())[0]
                
                pet = db.queryPet({'PET': uboss_pet})
                pet_ability = pet['ABILITIES'][0]
                pet_ability_name = list(pet_ability.keys())[0]
                pet_ability_type = list(pet_ability.values())[1]
                pet_ability_value = list(pet_ability.values())[0]

                traits = ut.traits

                if uboss_show != 'Unbound':
                    uboss_show_img = db.queryUniverse({'TITLE': uboss_show})['PATH']
                message= uboss_desc
                
                mytrait = {}
                traitmessage = ''
                for trait in traits:
                    if trait['NAME'] == uboss_show:
                        mytrait = trait
                    if uboss_show == 'Kanto Region' or uboss_show == 'Johto Region' or uboss_show == 'Kalos Region' or uboss_show == 'Unova Region' or uboss_show == 'Sinnoh Region' or uboss_show == 'Hoenn Region' or uboss_show == 'Galar Region' or uboss_show == 'Alola Region':
                        if trait['NAME'] == 'Pokemon':
                            mytrait = trait
                if mytrait:
                    traitmessage = f"**{mytrait['EFFECT']}**: {mytrait['TRAIT']}"
                
                embedVar = discord.Embed(title=f":japanese_ogre: | {uboss_name}\n:earth_africa: | {uboss_show} Boss", description=textwrap.dedent(f"""
                **{message}**\n
                
                :flower_playing_cards: | **Card** - {uboss_name}
                :reminder_ribbon: | **Title** - {uboss_title}: **{title_passive_type}** - {title_passive_value}
                :mechanical_arm: | **Arm** - {uboss_arm}: **{arm_passive_type}** - {arm_passive_value}
                :bird: | **Pet** - {uboss_pet}: **{pet_ability_type}**: {pet_ability_value}
                
                :infinity: | **Universe Trait** - {traitmessage}
                """), colour=000000)
                if uboss_show != "Unbound":
                    embedVar.set_thumbnail(url=uboss_show_img)
                embedVar.set_image(url=uboss_pic)

                await ctx.send(embed=embedVar)


            else:
                await ctx.send(m.ARM_DOESNT_EXIST, delete_after=3)
            
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
            await ctx.send(f"Error when viewing boss. Alert support. Thank you!")
            return

    @cog_ext.cog_slash(description="Exchange Boss Souls for Cards", guild_ids=main.guild_ids)
    async def exchange(self, ctx, boss : str, card : str):
        try:
            vault_query = {'OWNER' : str(ctx.author)}
            vault = db.queryVault(vault_query)
            userinfo = db.queryUser({"DISNAME" : str(ctx.author)})
            
            
            if userinfo['LEVEL'] < 100:
                await ctx.send(f"🔓 Unlock **Soul Exchange** by completing **Floor 100** of the 🌑 Abyss! Use /abyss to enter the abyss.")
                return
            
            await ctx.send(f"{ctx.author.mention} :japanese_ogre: **Soul Exchange** will reset your 🌑 Abyss level! ")
            bossname = boss
            cardname = card
            boss_info = db.queryBoss({'NAME': {"$regex": str(bossname), "$options": "i"}})
            mintedBoss = ""
            if userinfo:
                soul_list = userinfo['BOSS_WINS']
                for souls in soul_list:
                    if bossname == souls:
                        mintedBoss = bossname
                if mintedBoss =="":
                    await ctx.send("You do not own this Boss Soul", delete_after=3)
                    return
                elif boss_info:
                    card_info = db.queryCard({'NAME': {"$regex": str(cardname), "$options": "i"}})
                    if card_info:
                        uboss_name = boss_info['NAME']
                        uboss_show = boss_info['UNIVERSE']
                        card_show = card_info['UNIVERSE']
                        if uboss_show == card_show:
                            if card_info['HAS_COLLECTION']:
                                await ctx.send(f"You can not use exchange on Destiny cards.")
                                return
                            card_owned = False
                            for c in vault['CARD_LEVELS']:
                                if c['CARD'] == str(card_info['NAME']):
                                    card_owned = True
                            if not card_owned:
                                uni = db.queryUniverse({'TITLE': card_info['UNIVERSE']})
                                tier = uni['TIER']
                                update_query = {'$addToSet': {'CARD_LEVELS': {'CARD': str(card_info['NAME']), 'LVL': 0, 'TIER': int(tier), 'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0}}}
                                response = db.updateVaultNoFilter(vault_query,{'$addToSet':{'CARDS': str(card_info['NAME'])}})
                                r = db.updateVaultNoFilter(vault_query, update_query)
                            owned_destinies = []
                            for destiny in vault['DESTINY']:
                                owned_destinies.append(destiny['NAME'])
                            for destiny in d.destiny:
                                if card_info['NAME'] in destiny["USE_CARDS"] and destiny['NAME'] not in owned_destinies:
                                    db.updateVaultNoFilter(vault_query,{'$addToSet':{'DESTINY': destiny}})
                                    await ctx.send(f"**DESTINY AWAITS!**\n**{destiny['NAME']}** has been added to your vault.")
                            db.updateUserNoFilter({'DISNAME' : str(ctx.author)}, {'$set' : {'LEVEL' : 0}})
                            db.updateUserNoFilter({'DISNAME': str(ctx.author)},{'$pull':{'BOSS_WINS': str(bossname)}})
                            response = db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$addToSet':{'CARDS': str(cardname)}})
                            await ctx.send(f"SOUL EXCHANGE: {cardname} has been added to {ctx.author.mention}'s vault: CARDS")
                            
                        else:
                            await ctx.send("Card must match Boss Universe", delete_after=3)
                        
                    else:
                        await ctx.send("Card Doesn't Exist", delete_after=3)
                else:
                    await ctx.send("Boss Doesn't Exist", delete_after=3)               
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
            await ctx.send(f"Error when exchanging boss soul. Alert support. Thank you!")
            return








def setup(bot):
    bot.add_cog(Boss(bot))