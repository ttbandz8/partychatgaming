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

class CrownUnlimited(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print('Crown Unlimited Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @commands.command()
    async def begin(self, ctx):
        session_query = {"OWNER": str(ctx.author), "AVAILABLE": True}
        session = db.querySession(session_query)
        if session:
            if session['GAME'] == 'Crown Unlimited':
                teams = [x for x in session['TEAMS']]
                team_1 = [x for x in teams if x['POSITION'] == 0][0] # position 0
                team_2 = [x for x in teams if x['POSITION'] == 1][0] # position 1
                o = db.queryCard({'NAME': team_1['CARD']})
                otitle = db.queryTitle({'TITLE': team_1['TITLE']})

                t = db.queryCard({'NAME': team_2['CARD']})
                ttitle = db.queryTitle({'TITLE': team_1['TITLE']})

                
                # GLOBAL FUNCTION
                focus = 90
                resolve = 50

                # TEAM 1 Data
                o_user = db.queryUser({'DISNAME': team_1['TEAM'][0]})
                o_DID = o_user['DID']
                o_card = o['NAME']
                o_health = o['HLT']
                o_stamina = o['STAM']
                o_moveset = o['MOVESET']
                o_attack = o['ATK']
                o_defense = o['DEF']
                o_type = o['TYPE']
                o_accuracy = o['ACC']
                o_passive = o['PASS']
                o_speed = o['SPD']
                o_vulerable = o['VUL']
                o_show = o['SHOW']
                o_title_show = otitle['SHOW']
                o_title_passive = otitle['ABILITIES']
                o_vul = False
                user1 = await self.bot.fetch_user(o_DID)

                print(o_moveset)

                # TEAM 2 Data
                t_user = db.queryUser({'DISNAME': team_2['TEAM'][0]})
                t_DID = t_user['DID']
                t_card = t['NAME']
                t_health = t['HLT']
                t_stamina = t['STAM']
                t_moveset = t['MOVESET']
                t_attack = t['ATK']
                t_defense = t['DEF']
                t_type = t['TYPE']
                t_accuracy = t['ACC']
                t_passive = t['PASS']
                t_speed = t['SPD']
                t_vulerable = t['VUL']
                t_show = t['SHOW']
                t_title_show = ttitle['SHOW']
                t_title_passive = ttitle['ABILITIES']
                o_vul = True
                user2 = await self.bot.fetch_user(t_DID)

                turn = 0
                start = starting_position(o_speed, t_speed)

                if start == True:
                    turn = 0
                else:
                    turn = 1    
                
                # test = 10
                # while test >= 0:
                #     await ctx.send(f"Number is {test}. Still not 0!")
                #     if turn == 0:

                #         await ctx.send(f'{user1.mention} pick a number!')
                #         def check(msg):
                #             return msg.author == user1 and msg.channel == ctx.channel
                #         try:
                #             msg = await self.bot.wait_for("message", check=check)
                #             test = test - int(msg.content)
                #             turn = 1
                #         except:
                #             await ctx.send('Did not work')

                #     elif turn == 1:

                #         await ctx.send(f'{user2.mention} pick a number!')
                #         def check(msg):
                #             return msg.author == user2 and msg.channel == ctx.channel
                #         try:
                #             msg = await self.bot.wait_for("message", check=check)
                #             test = test - int(msg.content)
                #             turn = 0
                #         except:
                #             await ctx.send('Did not work')

                # await ctx.send("Number is 0!")
        else:
            await ctx.send(m.SESSION_DOES_NOT_EXIST)


def starting_position(o,t):
    if o > t:
        return True
    else:
        return False

def damage_cal(attack, ap, defense, passive, vul):
    bonus = 1.00
    if vul:
        bonus = .75
    else:
        bonus = 1.25
    if passive
    damage = (ap/defense)* attack*bonus

def setup(bot):
    bot.add_cog(CrownUnlimited(bot))

# ''' Delete All Cards '''
# @commands.command()
# async def dac(self, ctx):
#    user_query = {"DISNAME": str(ctx.author)}
#    if ctx.author.guild_permissions.administrator == True:
#       resp = db.deleteAllCards(user_query)
#       await ctx.send(resp)
#    else:
#       await ctx.send(m.ADMIN_ONLY_COMMAND)