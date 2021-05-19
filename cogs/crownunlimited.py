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
                o_show = o['SHOW']
                o_title_show = otitle['SHOW']
                o_title_passive = otitle['ABILITIES']
                o_vul = False
                user1 = await self.bot.fetch_user(o_DID)
                o_title_passive_bool = False
                # Team 1 Passive Config
                if (o_show == o_title_show) or (o_title_show == "Unbound"):
                    o_title_passive_bool = True

                # Moves
                o_1 = o_moveset[0]
                o_2 = o_moveset[1]
                o_3 = o_moveset[2]
                o_enhancer = o_moveset[3]

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
                t_show = t['SHOW']
                t_title_show = ttitle['SHOW']
                t_title_passive = ttitle['ABILITIES']
                t_vul = False
                user2 = await self.bot.fetch_user(t_DID)
                t_title_passive_bool = False

                # Team 2 Passive Config
                if (t_show == t_title_show) or (t_title_show == "Unbound"):
                    t_title_passive_bool = True

                # Moves
                t_1 = t_moveset[0]
                t_2 = t_moveset[1]
                t_3 = t_moveset[2]
                t_enhancer = t_moveset[3]

                turn = 0
                start = starting_position(o_speed, t_speed)

                if start == True:
                    turn = 0
                else:
                    turn = 1    
                
                options = [1,2,3,4]
                await ctx.send(f"{user1.mention}: {o_card} VS {user2.mention}: {t_card} has begun!")

                while (o_health >= 0) and (t_health >= 0):
                    if turn == 0:
                        await ctx.send(f"{t_card} has {t_health} health. What move will you use, {user1.mention}?")
                        # Make sure user is responding with move
                        def check(msg):
                            return msg.author == user1 and msg.channel == ctx.channel and int(msg.content) in options
                        try:
                            msg = await self.bot.wait_for("message", check=check)

                            # calculate data based on selected move
                            if int(msg.content) == 1:
                                dmg = damage_cal(o_1, o_attack, o_defense, o_passive, o_title_passive, o_title_passive_bool, o_vul, o_accuracy)
                            elif int(msg.content) == 2:
                                dmg = damage_cal(o_2, o_attack, o_defense, o_passive, o_title_passive, o_title_passive_bool, o_vul, o_accuracy)
                            elif int(msg.content) == 3:
                                dmg = damage_cal(o_3, o_attack, o_defense, o_passive, o_title_passive, o_title_passive_bool, o_vul, o_accuracy)
                            elif int(msg.content) == 4:
                                dmg = damage_cal(o_enhancer, o_attack, o_defense, o_passive, o_title_passive, o_title_passive_bool, o_vul, o_accuracy)

                            t_health = t_health - dmg
                            await ctx.send(f'{int(dmg)} damage dealt!')
                            turn = 1
                        except:
                            await ctx.send('Did not work')

                    elif turn == 1:
                        await ctx.send(f"{o_card} has {o_health} health. What move will you use, {user2.mention}?")
                        # Make sure user is responding with move
                        def check(msg):
                            return msg.author == user2 and msg.channel == ctx.channel and int(msg.content) in options
                        try:
                            msg = await self.bot.wait_for("message", check=check)

                            # calculate data based on selected move
                            if int(msg.content) == 1:
                                dmg = damage_cal(t_1, t_attack, t_defense, t_passive, t_title_passive, t_title_passive_bool, t_vul, t_accuracy)
                            elif int(msg.content) == 2:
                                dmg = damage_cal(t_2, t_attack, t_defense, t_passive, t_title_passive, t_title_passive_bool, t_vul, t_accuracy)
                            elif int(msg.content) == 3:
                                dmg = damage_cal(t_3, t_attack, t_defense, t_passive, t_title_passive, t_title_passive_bool, t_vul, t_accuracy)
                            elif int(msg.content) == 4:
                                dmg = damage_cal(t_enhancer, t_attack, t_defense, t_passive, t_title_passive, t_title_passive_bool, t_vul, t_accuracy)

                            o_health = o_health - int(dmg)
                            await ctx.send(f'{int(dmg)} damage dealt!')
                            turn = 0
                        except:
                            await ctx.send('Did not work')
                # End the match
                if t_health >= 0:
                    await ctx.send(f"{user2.mention} you win the match!")
                elif o_health >=0:
                    await ctx.send(f"{user1.mention} you win the match!")
        else:
            await ctx.send(m.SESSION_DOES_NOT_EXIST)


def starting_position(o,t):
    if o > t:
        return True
    else:
        return False

def damage_cal(ability, attack, defense, card_passive, title_passive, title_passive_bool, vul, accuracy):
    return 100

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