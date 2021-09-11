import textwrap
import discord
from discord.ext import commands
import bot as main
import db
import classes as data
import messages as m
import numpy as np
import unique_traits as ut
import help_commands as h
# Converters
from discord import User
from discord import Member
from PIL import Image, ImageFont, ImageDraw
import requests
from discord_slash import cog_ext, SlashContext

class Universe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print('Universe Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @cog_ext.cog_slash(description="View a universe", guild_ids=main.guild_ids)
    async def viewuniverse(self, ctx, universe: str):
        try:
            universe_name = universe
            universe = db.queryUniverse({'TITLE': {"$regex": f"^{universe_name}$", "$options": "i"}})
            universe_name = universe['TITLE']
            ttitle = "Starter"
            tarm = "Stock"
            dtitle = "Reborn"
            darm = "Reborn Stock"
            dpet = "Chick"
            boss = "Bossless"
            crest = Crest_dict['Unbound']
            prerec = ""
            owner = "PCG"
            traits = ut.traits
            if universe:
                universe_title= universe['TITLE']
                fights = len(universe['CROWN_TALES'])
                crest = Crest_dict[universe_title]
                universe_image = universe['PATH']
                ttitle = universe['UTITLE']
                tarm = universe['UARM']
                dtitle = universe['DTITLE']
                darm = universe['DARM']
                dpet = universe['DPET']
                boss = universe['UNIVERSE_BOSS']
                tier = universe['TIER']
                bossmessage = f"*Use /viewboss {boss}*"
                if boss == "":
                    bossmessage = f"No {universe_title} Boss available yet!"
                prerec = universe['PREREQUISITE']
                
                prerecmessage = f"Compelete the {prerec} Tale to unlock this Universe!"
                if prerec == "":
                    if tier == 9:
                        prerec = "Crown Rift"
                        prerecmessage = "Complete Battles To Open Crown Rifts!"
                    else:
                        prerec = "Starter Universe"
                        prerecmessage = "Complete this Starter Tale to unlock additional Universes!"
                owner = universe['GUILD']
                ownermessage = f"{universe_title} is owned by the {owner} Guild!"
                if owner == "PCG":
                    owner = "Crest Unclaimed"
                    ownermessage = "*Complete the /dungeon and Claim this Universe for your Guild!*"
                   
                
                mytrait = {}
                traitmessage = ''
                for trait in traits:
                    if trait['NAME'] == universe_title:
                        mytrait = trait
                    if universe_title == 'Kanto Region' or universe_title == 'Johto Region' or universe_title == 'Kalos Region' or universe_title == 'Unova Region' or universe_title == 'Sinnoh Region' or universe_title == 'Hoenn Region' or universe_title == 'Galar Region' or universe_title == 'Alola Region':
                        if trait['NAME'] == 'Pokemon':
                            mytrait = trait
                if mytrait:
                    traitmessage = f"**{mytrait['EFFECT']}**: {mytrait['TRAIT']}"
                    

                embedVar = discord.Embed(title=f":earth_africa: | {universe_title} :crossed_swords: {fights}", description=textwrap.dedent(f"""
                {crest} | **{ownermessage}**\n
                
                :crown: | **Tales Build**\n                                                                               
                :reminder_ribbon: | **Title** - {ttitle}
                :mechanical_arm: | **Arm** - {tarm}\n

                :fire: | **Dungeon Build**\n
                :reminder_ribbon: | **Title** - {dtitle}
                :mechanical_arm: | **Arm** - {darm}
                :bird: | **Pet** {dpet}\n
                
                :japanese_ogre: | **Universe Boss**
                :flower_playing_cards: | **Card** - {boss}
                {bossmessage}\n

                :infinity: | **Universe Trait** - {traitmessage}
                :lock: | **Prerequisites:** {prerecmessage}
                """), colour=000000)
                embedVar.set_image(url=universe_image)

                await ctx.send(embed=embedVar)

            else:
                await ctx.send(m.UNIVERSE_DOES_NOT_EXIST)
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
            await ctx.send(f"Error when viewing universe. Alert support. Thank you!")
            return

def setup(bot):
    bot.add_cog(Universe(bot))
    
Crest_dict = {'Unbound': ':ideograph_advantage:',
              'My Hero Academia': ':sparkle:',
              'League Of Legends': ':u6307:',
              'Kanto Region': ':chart:',
              'Naruto': ':u7121:',
              'Bleach': ':u6709:',
              'God Of War': ':u7533:',
              'Chainsawman' : ':accept:',
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
              'Crown Rift Madness': ':loop:'}