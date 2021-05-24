from cogs.lobbies import Lobbies
import time
from re import T
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
import random
from collections import ChainMap
now = time.asctime()
import base64
from io import BytesIO

class CrownUnlimited(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print('Crown Unlimited Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)


    @commands.command()
    async def tales(self, ctx):
        sowner = db.queryUser({'DISNAME': str(ctx.author)})
        all_universes = db.queryAllUniverse()
        available_universes = []
        selected_universe = ""
        for uni in all_universes:
            if uni['PREREQUISITE'] in sowner['CROWN_TALES']:
                available_universes.append(uni['TITLE'])
                
        embedVar = discord.Embed(title=f":crown: CROWN TALES!", description="Select a Universe to explore!", colour=0xe91e63)
        embedVar.add_field(name="Available Universes", value="\n".join(available_universes))
        await ctx.send(embed=embedVar)
        accept = await ctx.send(f"{ctx.author.mention} which Universe would you like to explore!")

        def check(msg):
            return msg.author == ctx.author and msg.content in available_universes
        try:
            msg = await self.bot.wait_for('message', timeout=30.0, check=check)
            selected_universe = msg.content
        except:
            embedVar = discord.Embed(title=f"{m.STORY_NOT_SELECTED}", colour=0xe91e63)
            await ctx.send(embed=embedVar)
            return

        starttime = time.asctime()
        h_gametime = starttime[11:13]
        m_gametime = starttime[14:16]
        s_gametime = starttime[17:19]

        universe = db.queryUniverse({'TITLE': str(selected_universe)})
        boss = db.queryBoss({'NAME': str(universe['UNIVERSE_BOSS'])})

        legends = [x for x in universe['CROWN_TALES']]
        total_legends = len(legends)
        currentopponent = 0
        continued = True

        #While Still PLaying Universe
        while continued == True:

            o = db.queryCard({'NAME': sowner['CARD']})
            otitle = db.queryTitle({'TITLE': sowner['TITLE']})
            
            t = db.queryCard({'NAME': legends[currentopponent]})
            ttitle = db.queryTitle({'TITLE': 'Starter'})

            ####################################################################
            # Player Data



            # Player 1 Data
            o_user = sowner
            oarm = db.queryArm({'ARM': o_user['ARM']})
            oarm_passive = oarm['ABILITIES'][0]
            oarm_name=oarm['ARM']
            o_DID = o_user['DID']
            o_card = o['NAME']
            o_card_path=o['PATH']
            o_rcard_path=o['RPATH']
            o_max_health = o['HLT']
            o_health = o['HLT']
            o_stamina = o['STAM']
            o_max_stamina = o['STAM']
            o_moveset = o['MOVESET']
            o_attack = o['ATK'] + (2 * currentopponent)
            o_defense = o['DEF'] + (3 * currentopponent)
            o_type = o['TYPE']
            o_accuracy = o['ACC']
            o_passive = o['PASS'][0]
            o_speed = o['SPD']
            o_universe = o['UNIVERSE']
            o_title_universe = otitle['UNIVERSE']
            o_title_passive = otitle['ABILITIES'][0]
            o_vul = False
            user1 = await self.bot.fetch_user(o_DID)
            o_title_passive_bool = False

            # Player 2 Data
            t_user = boss
            tarm = db.queryArm({'ARM': 'Stock'})
            tarm_passive = tarm['ABILITIES'][0]
            tarm_name=tarm['ARM']
            #t_DID = t_user['DID']
            t_card = t['NAME']
            t_card_path=t['PATH']
            t_rcard_path=t['RPATH']
            t_max_health = t['HLT'] + (10 * currentopponent)
            t_health = t['HLT'] + (10 * currentopponent)
            t_stamina = t['STAM']
            t_max_stamina= t['STAM']
            t_moveset = t['MOVESET']
            t_attack = t['ATK'] + (7 * currentopponent)
            t_defense = t['DEF'] + (5 * currentopponent)
            t_type = t['TYPE']
            t_accuracy = t['ACC']
            t_passive = t['PASS'][0]
            t_speed = t['SPD']
            t_universe = t['UNIVERSE']
            t_title_universe = ttitle['UNIVERSE']
            t_title_passive = ttitle['ABILITIES'][0]
            t_vul = False
            #user2 = await self.bot.fetch_user(t_DID)
            t_title_passive_bool = False
            
            ################################################################################

            # Player 1 Passive Config
            if (o_universe == o_title_universe) or (o_title_universe == "Unbound"):
                o_title_passive_bool = True
            
            # Player 1 Focus & Resolve
            o_focus = 60
            o_used_focus=False
            o_resolve = 50
            o_used_resolve=False

            # Player 1 Moves
            o_1 = o_moveset[0]
            o_2 = o_moveset[1]
            o_3 = o_moveset[2]
            o_enhancer = o_moveset[3]
            o_enhancer_used=False

            # Player 1 Card Passive
            o_card_passive_type = list(o_passive.values())[1]
            o_card_passive = list(o_passive.values())[0]

            if o_card_passive_type == 'ATK':
                o_attack = o_attack + int(o_card_passive)
            elif o_card_passive_type == 'DEF':
                o_defense = o_defense + int(o_card_passive)
            elif o_card_passive_type == 'STAM':
                o_stamina = o_stamina + int(o_card_passive)
            elif o_card_passive_type == 'HLT':
                o_health = o_health + int(o_card_passive)
            elif o_card_passive_type == 'LIFE':
                o_health = o_health + round(int(o_card_passive) + (.10 * t_health))
            elif o_card_passive_type == 'DRAIN':
                o_stamina = o_stamina + int(o_card_passive)

            # Title Passive
            o_title_passive_type = list(o_title_passive.keys())[0]
            o_title_passive_value = list(o_title_passive.values())[0]

            if o_title_passive_bool:
                if o_title_passive_type == 'ATK':
                    o_attack = o_attack + int(o_title_passive_value)
                elif o_title_passive_type == 'DEF':
                    o_defense = o_defense + int(o_title_passive_value)
                elif o_title_passive_type == 'STAM':
                    o_stamina = o_stamina + int(o_title_passive_value)
                elif o_title_passive_type == 'HLT':
                    o_health = o_health + int(o_title_passive_value)

            # Arm Passive Player 1
            oarm_passive_type = list(oarm_passive.keys())[0]
            oarm_passive_value = list(oarm_passive.values())[0]

            if oarm_passive_type == 'ATK':
                o_attack = o_attack + int(oarm_passive_value)
            elif oarm_passive_type == 'DEF':
                o_defense = o_defense + int(oarm_passive_value)
            elif oarm_passive_type == 'STAM':
                o_stamina = o_stamina + int(oarm_passive_value)
            elif oarm_passive_type == 'HLT':
                o_health = o_health + int(oarm_passive_value)

            # Arm Passive Player 2
            tarm_passive_type = list(tarm_passive.keys())[0]
            tarm_passive_value = list(tarm_passive.values())[0]

            if tarm_passive_type == 'ATK':
                t_attack = t_attack + int(tarm_passive_value)
            elif tarm_passive_type == 'DEF':
                t_defense = t_defense + int(tarm_passive_value)
            elif tarm_passive_type == 'STAM':
                t_stamina = t_stamina + int(tarm_passive_value)
            elif tarm_passive_type == 'HLT':
                t_health = t_health + int(tarm_passive_value)

            


            # Player 2 Passive Config
            if (t_universe == t_title_universe) or (t_title_universe == "Unbound"):
                t_title_passive_bool = True
            
            # Player 1 Card Passive
            t_card_passive_type = list(t_passive.values())[1]
            t_card_passive = list(t_passive.values())[0]

            if t_card_passive_type == 'ATK':
                t_attack = t_attack + int(t_card_passive)
            elif t_card_passive_type == 'DEF':
                t_defense = t_defense + int(t_card_passive)
            elif t_card_passive_type == 'STAM':
                t_stamina = t_stamina + int(t_card_passive)
            elif t_card_passive_type == 'HLT':
                t_health = t_health + int(t_card_passive)
            elif t_card_passive_type == 'LIFE':
                t_health = t_health + round(int(t_card_passive) + (.10 * o_health))
            elif t_card_passive_type == 'DRAIN':
                t_stamina = t_stamina + int(t_card_passive)

            # Title Passive
            t_title_passive_type = list(t_title_passive.keys())[0]
            t_title_passive_value = list(t_title_passive.values())[0]

            if t_title_passive_bool:
                if t_title_passive_type == 'ATK':
                    t_attack = t_attack + int(t_title_passive_value)
                elif t_title_passive_type == 'DEF':
                    t_defense = t_defense + int(t_title_passive_value)
                elif t_title_passive_type == 'STAM':
                    t_stamina = t_stamina + int(t_title_passive_value)
                elif t_title_passive_type == 'HLT':
                    t_health = t_health + int(t_title_passive_value)


            # Player 2 Moves
            t_1 = t_moveset[0]
            t_2 = t_moveset[1]
            t_3 = t_moveset[2]
            t_enhancer = t_moveset[3]
            t_enhancer_used=False

            # Player 1 Focus & Resolve
            t_focus = 60
            t_used_focus=False
            t_resolve = 50
            t_used_resolve=False
            
            # Turn iterator
            turn = 0
            # Enhance Turn Iterators
            eo=0
            et=0

            botActive = True
                

            # Vulnerability Check
            if o_type == 0 and t_type == 2:
                o_vul=True
            if t_type == 0 and o_type == 2:
                t_vul=True
            
            options = [1,2,3,4,5,0]
            await ctx.send(f"{user1.mention}: `{o_card}` VS {t_universe} BOSS : `{t_card}` has begun!")

            # Count Turns
            turn_total = 0

            # START TURNS
            while (o_health > 0) and (t_health > 0):
                #Player 1 Turn Start
                if turn == 0:

                    # Tutorial Instructions
                    if turn_total == 0 and botActive:                    
                        embedVar = discord.Embed(title=f"Welcome to `Crown Unlimited`!", description=f"Follow the instructions to learn how to play Crown Unlimited", colour=0xe91e63)
                        embedVar.add_field(name="How do you play this game?", value="The point of the game is to win the game, duh!\nTo do this, you need to select moves in a strategic order to give you the advantage to secure the win!")
                        embedVar.set_footer(text="Select a move to get started. Moves will drain your `Stamina` quickly.\n`When your Stamina depletes to 0 your character will Focus`")
                        await ctx.send(embed=embedVar)

                    

                    if o_health <= (o_max_health * .25):
                        embed_color_o=0xe74c3c
                        
                    elif o_health <= (o_max_health * .50):
                        embed_color_o=0xe67e22
                    elif o_health <= (o_max_health * .75):
                        embed_color_o=0xf1c40f
                        
                    else:
                        embed_color_o = 0x2ecc71

                    if o_stamina <= 0:
                        if botActive and not o_used_focus:                    
                            embedVar = discord.Embed(title=f"You've entered `Focus State`!", description=f"Entering `Focus State` sacrifices a turn to power up and regain `Stamina`!", colour=0xe91e63)
                            embedVar.add_field(name="Strategy", value="Pay attention to your oppononets `STAM` bar. If they are close to entering `Focus State`, you will have the ability to strike twice if you play your cards right!")
                            embedVar.set_footer(text="After you entered focus state once, a transformation is possible by strengthening your `Resolve`!")
                            await ctx.send(embed=embedVar)
                        #fortitude or luck is based on health  
                        fortitude = 0.0
                        low = o_health - (o_health*.90)
                        high = o_health- (o_health*.80)
                        fortitude = random.randint(int(low), int(high))

                        o_stamina = o_focus
                        o_healthcalc = round(((o_focus * .40) + (fortitude * 1))/2)
                        o_attackcalc = round(.20 * ((o_focus * .15) + round(fortitude * 1)))
                        o_defensecalc = round(.20 * ((o_focus * .15) + round(fortitude * 1)))
                        #check if user is at max health and sets messages and focus health value
                        o_newhealth = 0
                        healmessage = ""
                        messagenumber = 0
                        if o_health <= o_max_health:
                            o_newhealth = o_health + o_healthcalc
                            if o_newhealth > o_max_health:
                                healmessage = "the injuries dissapeared"
                                messagenumber = 1
                                o_health = o_max_health
                            else:
                                healmessage = "regained some vitality"
                                messagenumber = 2
                                o_health = o_newhealth
                        else:
                            healmessage = f"`{t_card}`'s blows don't appear to have any effect!"
                            messagenumber = 0
                        o_attack = o_attack + o_attackcalc
                        o_defense =  o_defense + o_defensecalc
                        o_used_focus = True

                        embedVar = discord.Embed(title=f"{o_card} focused and {healmessage}", description="All stats increased", colour=embed_color_o)
                        await ctx.send(embed=embedVar)

                        if messagenumber != 2:
                            if messagenumber == 1:
                                embedVar = discord.Embed(title=f"{o_card} Stamina has recovered!", colour=embed_color_o)
                                await ctx.send(embed=embedVar)
                            else:
                                embedVar = discord.Embed(title=f"{o_card} Stamina has recovered!", colour=embed_color_o)
                                await ctx.send(embed=embedVar)
                        else:
                            embedVar = discord.Embed(title=f"{o_card} Stamina has recovered!", colour=embed_color_o)
                            await ctx.send(embed=embedVar)
                        turn_total= turn_total + 1
                        turn = 1
                    else:

                        # UNIVERSE CARD
                        player_1_card = showcard(o, o_max_health, o_health, o_max_stamina, o_stamina, o_used_resolve, otitle, o_used_focus)
                        await ctx.send(file=player_1_card)
                        embedVar = discord.Embed(title=f"{o_card} What move will you use?", description=f"{t_card} currently has {t_health} health and {t_stamina} stamina.", colour=embed_color_o)
                        if o_used_focus and not o_used_resolve:
                            embedVar.set_author(name="Press 5 to strengthen resolve!")
                        embedVar.set_footer(text="Use 1 for Basic Attack, 2 for Special Attack, 3 for Ultimate Move, and 4 for Enhancer")
                        await ctx.send(embed=embedVar)
                        
                        # Make sure user is responding with move
                        def check(msg):
                            return msg.author == user1 and msg.channel == ctx.channel and int(msg.content) in options
                        try:
                            msg = await self.bot.wait_for("message",timeout=240.0, check=check)

                            # calculate data based on selected move
                            if int(msg.content) == 0:
                                o_health=0
                            if int(msg.content) == 1:
                                dmg = damage_cal(o_card, o_1, o_attack, o_defense, t_defense, o_vul, o_accuracy, o_stamina, o_enhancer_used, o_health, t_health, t_stamina)
                            elif int(msg.content) == 2:
                                dmg = damage_cal(o_card, o_2, o_attack, o_defense, t_defense, o_vul, o_accuracy, o_stamina, o_enhancer_used, o_health, t_health, t_stamina)
                            elif int(msg.content) == 3:
                                dmg = damage_cal(o_card, o_3, o_attack, o_defense, t_defense, o_vul, o_accuracy, o_stamina, o_enhancer_used, o_health, t_health, t_stamina)
                            elif int(msg.content) == 4:
                                o_enhancer_used=True
                                dmg = damage_cal(o_card, o_enhancer, o_attack, o_defense, t_defense, o_vul, o_accuracy, o_stamina, o_enhancer_used, o_health, t_health, t_stamina)
                                o_enhancer_used=False
                            elif int(msg.content) == 5:

                                #Resolve Check and Calculation
                                if not o_used_resolve and o_used_focus:

                                    if botActive:                    
                                        embedVar = discord.Embed(title=f"You are Resolved", description=f"Entering `Resolved State` sacrifices a turn to power up even greater and regain `Stamina`!", colour=0xe91e63)
                                        embedVar.add_field(name="Strategy", value="You sacrifice `Defense` to greatly increase `Attack` in your `Resolved` state. Use it when you need to secure an advantage.")
                                        embedVar.set_footer(text="A poorly planned `Resolve` could cost you the match.")
                                        await ctx.send(embed=embedVar)
                                        

                                    #fortitude or luck is based on health  
                                    fortitude = 0.0
                                    low = o_health - (o_health * .75)
                                    high = o_health- (o_health * .66)
                                    fortitude = random.randint(int(low), int(high))
                                    #Resolve Scaling
                                    o_resolve_health = round(fortitude + (.5*o_resolve))
                                    o_resolve_attack = round(4 * (o_resolve / (.50 * o_attack)))
                                    o_resolve_defense = round(3 * (o_resolve / (.25 * o_defense)))

                                    o_stamina = o_stamina + o_resolve
                                    o_health = o_health + o_resolve_health
                                    o_attack = round(o_attack + o_resolve_attack)
                                    o_defense = round(o_defense - o_resolve_defense)
                                    o_used_resolve = True 

                                    embedVar = discord.Embed(title=f"{o_card} strengthened resolve!", colour=embed_color_o)
                                    await ctx.send(embed=embedVar)
                                    turn_total= turn_total + 1
                                    turn=1
                                else:
                                    emessage = m.CANNOT_USE_RESOLVE
                                    embedVar = discord.Embed(title=emessage, description=f"Entering `Resolved State` sacrifices a turn to power up even greater and regain `Stamina`!", colour=0xe91e63)
                                    await ctx.send(embed=embedVar)
                                    turn=0

                            if int(msg.content) !=5:
                                # If you have enough stamina for move, use it
                                if dmg['CAN_USE_MOVE']:
                                    if dmg['ENHANCE']:
                                        enh_type= dmg['ENHANCED_TYPE']
                                    
                                        if enh_type == 'ATK':
                                            o_attack = round(o_attack + dmg['DMG'])
                                        elif enh_type == 'DEF':
                                            o_defense = round(o_defense + dmg['DMG'])
                                        elif enh_type == 'STAM':
                                            o_stamina = round(o_stamina + dmg['DMG'])
                                        elif enh_type == 'HLT':
                                            o_health = round(o_health + dmg['DMG'])
                                        elif enh_type == 'LIFE':
                                            o_health = round(o_health + dmg['DMG'])
                                            t_health = round(t_health - dmg['DMG'])
                                        elif enh_type == 'DRAIN':
                                            o_stamina = round(o_stamina + dmg['DMG'])
                                            t_stamina = round(t_stamina - dmg['DMG'])
                                        o_stamina = o_stamina - int(dmg['STAMINA_USED'])

                                        embedVar = discord.Embed(title=f"{dmg['MESSAGE']}", colour=embed_color_o)
                                        await ctx.send(embed=embedVar)
                                        turn_total= turn_total + 1
                                        turn=1
                                    elif dmg['DMG'] == 0:
                                        o_stamina = o_stamina - int(dmg['STAMINA_USED'])

                                        embedVar = discord.Embed(title=f"{dmg['MESSAGE']}", colour=embed_color_o)
                                        await ctx.send(embed=embedVar)
                                        turn_total= turn_total + 1
                                        turn=1
                                    else:
                                        t_health = t_health - dmg['DMG']
                                        if t_health < 0:
                                            t_health=0
                                        o_stamina = o_stamina - dmg['STAMINA_USED']

                                        embedVar = discord.Embed(title=f"{dmg['MESSAGE']}", colour=embed_color_o)
                                        await ctx.send(embed=embedVar)
                                        turn_total= turn_total + 1
                                        turn=1
                                else:
                                    emessage = m.NOT_ENOUGH_STAMINA
                                    embedVar = discord.Embed(title=emessage, description=f"Use abilities to Increase `STAM` or enter `FOCUS STATE`!", colour=0xe91e63)
                                    await ctx.send(embed=embedVar)
                                    turn=0
                        except:
                            emessage = m.DID_NOT_WORK
                            embedVar = discord.Embed(title=emessage, description=f"Try Again", colour=0xe91e63)
                            await ctx.send(embed=embedVar)
                #PLayer 2 Turn Start
                elif turn == 1:
                    
                    if t_health <= (t_max_health * .25):
                        embed_color_t=0xe74c3c
                        
                    elif t_health <= (t_max_health * .50):
                        embed_color_t=0xe67e22
                    elif t_health <= (t_max_health * .75):
                        embed_color_t=0xf1c40f
                    else:
                        embed_color_t = 0x2ecc71

                    #Focus
                    if t_stamina <= 0:
                        fortitude = 0.0
                        low = t_health - (t_health*.90)
                        high = t_health- (t_health*.80)
                        fortitude = random.randint(int(low), int(high))

                        t_stamina = t_focus
                        t_healthcalc = round(((t_focus * .40) + (fortitude * 1))/2)
                        t_attackcalc = round(.20 * ((t_focus * .15) + round(fortitude * 1)))
                        t_defensecalc = round(.20 * ((t_focus * .10) + round(fortitude * 1)))
                        t_newhealth = 0
                        healmessage = ""
                        messagenumber = 0

                        if t_health <= t_max_health:
                            t_newhealth = t_health + t_healthcalc
                            if t_newhealth > t_max_health:
                                healmessage = f"recovered!"
                                messagenumber = 1
                                t_health = t_max_health
                            else:
                                healmessage = f"stopped the bleeding..."
                                messagenumber = 2
                                t_health = t_newhealth
                        else:
                            healmessage = f"hasn't been touched..."
                            messagenumber = 0

                        t_attack = t_attack + t_attackcalc
                        t_defense =  t_defense + t_defensecalc
                        t_used_focus=True
                        embedVar = discord.Embed(title=f"{t_card} focused and {healmessage}", description="All stats increased", colour=embed_color_t)
                        await ctx.send(embed=embedVar)

                        if messagenumber != 2:
                            if messagenumber == 1:
                                embedVar = discord.Embed(title=f"{t_card} Stamina has recovered", colour=embed_color_t)
                                await ctx.send(embed=embedVar)
                            else:
                                embedVar = discord.Embed(title=f"{t_card} Stamina has recovered", colour=embed_color_t)
                                await ctx.send(embed=embedVar)
                        else:
                            embedVar = discord.Embed(title=f"{t_card} Stamina has recovered", colour=embed_color_t)
                            await ctx.send(embed=embedVar)
                        turn_total= turn_total + 1
                        turn=0
                    else:
                        # UNIVERSE CARD
                        player_2_card = showcard(t, t_max_health, t_health, t_max_stamina, t_stamina, t_used_resolve, ttitle, t_used_focus)
                        await ctx.send(file=player_2_card)

                        embedVar = discord.Embed(title=f"{t_card} What move will you use?", description=f"{o_card} currently has {o_health} health and {o_stamina} stamina.", colour=embed_color_t)
                        if t_used_focus and not t_used_resolve:
                            embedVar.set_author(name="Press 5 to strengthen resolve!")
                        embedVar.set_footer(text="Use 1 for Basic Attack, 2 for Special Attack, 3 for Ultimate Move, and 4 for Enhancer")
                        await ctx.send(embed=embedVar)
                        aiMove = 0
                        

                        if o_stamina == 0:
                            aiMove = 1
                        elif t_stamina >= 160 and (t_health >= o_health):
                            aiMove = 3
                        elif t_stamina >= 160:
                            aiMove = 3                                   
                        elif t_stamina >= 150 and (t_health >= o_health):
                            aiMove = 1
                        elif t_stamina >= 150:
                            aiMove = 1                                     
                        elif t_stamina >= 140 and (t_health >= o_health):
                            aiMove = 1
                        elif t_stamina >= 140:
                            aiMove = 3                                      
                        elif t_stamina >= 130 and (t_health >= o_health):
                            aiMove = 1
                        elif t_stamina >= 130:
                            aiMove = 3                                     
                        elif t_stamina >= 120 and (t_health >= o_health):
                            aiMove = 2
                        elif t_stamina >= 120:
                            aiMove = 3                                 
                        elif t_stamina >= 110 and (t_health >= o_health):
                            aiMove = 1
                        elif t_stamina >= 110:
                            aiMove = 2                                   
                        elif t_stamina >= 100 and (t_health >= o_health):
                            aiMove = 4
                        elif t_stamina >= 100:
                            aiMove = 1
                        elif t_stamina >= 90 and (t_health >= o_health):
                            aiMove = 3
                        elif t_stamina >= 90:
                            aiMove = 4
                        elif t_stamina >= 80 and (t_health >= o_health):
                            aiMove = 1
                        elif t_stamina >= 80:
                            aiMove = 3
                        elif t_stamina >= 70 and (t_health >= o_health):
                            aiMove = 4
                        elif t_stamina >= 70:
                            aiMove = 1
                        elif t_stamina >= 60 and (t_health >= o_health):
                            if t_used_resolve == False and t_used_focus:
                                aiMove = 5
                            elif t_used_focus == False:
                                aiMove = 2
                            else:
                                aiMove = 1 
                        elif t_stamina >= 60:
                            if t_used_resolve == False and t_used_focus:
                                aiMove = 5
                            elif t_used_focus == False:
                                aiMove = 2
                            else:
                                aiMove = 1 
                        elif t_stamina >= 50 and (t_health >= o_health):
                            if t_stamina >= o_stamina:
                                aiMove = 4
                            else:
                                aiMove = 1
                        elif t_stamina >= 50:
                            aiMove = 2
                        elif t_stamina >= 40 and (t_health >= o_health):
                            aiMove = 1
                        elif t_stamina >= 40:
                            aiMove = 2
                        elif t_stamina >= 30 and (t_health >= o_health):
                            aiMove = 4
                        elif t_stamina >= 30:
                            aiMove = 2
                        elif t_stamina >= 20 and (t_health >= o_health):
                            aiMove = 1
                        elif t_stamina >= 20:
                            aiMove = 4
                        elif t_stamina >= 10:
                            aiMove = 1
                        else:
                            aiMove = 0
                        

                        if int(aiMove) == 0:
                            t_health=0
                        if int(aiMove) == 1:
                            dmg = damage_cal(t_card, t_1, t_attack, t_defense, o_defense, t_vul, t_accuracy, t_stamina, t_enhancer_used, t_health, o_health, o_stamina)
                        elif int(aiMove) == 2:
                            dmg = damage_cal(t_card, t_2, t_attack, t_defense, o_defense, t_vul, t_accuracy, t_stamina, t_enhancer_used, t_health, o_health, o_stamina)
                        elif int(aiMove) == 3:
                            dmg = damage_cal(t_card, t_3, t_attack, t_defense, o_defense, t_vul, t_accuracy, t_stamina, t_enhancer_used, t_health, o_health, o_stamina)
                        elif int(aiMove) == 4:
                            t_enhancer_used=True
                            dmg = damage_cal(t_card, t_enhancer, t_attack, t_defense, o_defense, t_vul, t_accuracy, t_stamina, t_enhancer_used, t_health,o_health, o_stamina)
                            t_enhancer_used=False
                        elif int(aiMove) == 5:
                            if not t_used_resolve and t_used_focus:
                                #fortitude or luck is based on health  
                                fortitude = 0.0
                                low = t_health - (t_health * .75)
                                high = t_health- (t_health * .66)
                                fortitude = random.randint(int(low), int(high))
                                #Resolve Scaling
                                t_resolve_health = round(fortitude + (.5*t_resolve))
                                t_resolve_attack = round(4 * (t_resolve / (.25 * t_attack)))
                                t_resolve_defense = round(3 * (t_resolve / (.25 * t_defense)))

                                t_stamina = t_stamina + t_resolve
                                t_health = t_health + t_resolve_health
                                t_attack = round(t_attack + t_resolve_attack)
                                t_defense = round(t_defense - t_resolve_defense)
                                t_used_resolve=True
                                embedVar = discord.Embed(title=f"{t_card} strengthened resolve!", colour=embed_color_t)
                                await ctx.send(embed=embedVar)
                                turn_total= turn_total + 1
                                turn=0
                            else:
                                await ctx.send(m.CANNOT_USE_RESOLVE)
                                turn=1

                        if int(aiMove) !=5:
                            # If you have enough stamina for move, use it
                            if dmg['CAN_USE_MOVE']:

                                if dmg['ENHANCE']:
                                    enh_type= dmg['ENHANCED_TYPE']
                                    if enh_type == 'ATK':
                                        t_attack = round(t_attack + dmg['DMG'])
                                    elif enh_type == 'DEF':
                                        t_defense = round(t_defense + dmg['DMG'])
                                    elif enh_type == 'STAM':
                                        t_stamina = round(t_stamina + dmg['DMG'])
                                    elif enh_type == 'HLT':
                                        t_health = round(t_health + dmg['DMG'])
                                    elif enh_type == 'LIFE':
                                        t_health = round(t_health + dmg['DMG'])
                                        o_health = round(o_health - dmg['DMG'])
                                    elif enh_type == 'DRAIN':
                                        t_stamina = round(t_stamina + dmg['DMG'])
                                        o_stamina = round(o_stamina - dmg['DMG'])
                                    t_stamina = t_stamina - int(dmg['STAMINA_USED'])
                                    embedVar = discord.Embed(title=f"{dmg['MESSAGE']}", colour=embed_color_t)
                                    await ctx.send(embed=embedVar)
                                    turn_total= turn_total + 1
                                    turn = 0
                                elif dmg['DMG'] == 0:
                                    t_stamina = t_stamina - int(dmg['STAMINA_USED'])
                                    embedVar = discord.Embed(title=f"{dmg['MESSAGE']}", colour=embed_color_t)
                                    await ctx.send(embed=embedVar)
                                    turn_total= turn_total + 1
                                    turn=0
                                else:
                                    o_health = o_health - int(dmg['DMG'])
                                    if o_health < 0:
                                        o_health=0
                                    t_stamina = t_stamina - int(dmg['STAMINA_USED'])

                                    embedVar = discord.Embed(title=f"{dmg['MESSAGE']}", colour=embed_color_t)
                                    await ctx.send(embed=embedVar)
                                    turn_total= turn_total + 1
                                    turn=0

                            else:
                                await ctx.send(m.NOT_ENOUGH_STAMINA)
                                turn = 1
            if botActive:
                end_message="Use the #end command to end the tutorial lobby"
            else:
                end_message="Try Again"
            # End the match
            if o_health <= 0:
                # await ctx.send(f":zap: {user2.mention} you win the match!")
                wintime = time.asctime()
                h_playtime = int(wintime[11:13])
                m_playtime = int(wintime[14:16])
                s_playtime = int(wintime[17:19])
                gameClock = getTime(int(h_gametime),int(m_gametime),int(s_gametime),h_playtime,m_playtime,s_playtime)

                embedVar = discord.Embed(title=f":zap: `{t_card}` scores and wins the match!", description=f"Match concluded in {turn_total} turns!", colour=0x1abc9c)
                embedVar.set_author(name=f"{o_card} lost!\n{end_message}", icon_url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620236432/PCG%20LOGOS%20AND%20RESOURCES/PCGBot_1.png")
                if int(gameClock[0]) == 0 and int(gameClock[1]) == 0:
                    embedVar.set_footer(text=f"Play again?\nBattle Time: {gameClock[2]} Seconds.")
                elif int(gameClock[0]) == 0:
                    embedVar.set_footer(text=f"Play again?\nBattle Time: {gameClock[1]} Minutes and {gameClock[2]} Seconds.")
                else: 
                    embedVar.set_footer(text=f"Play again?\nBattle Time: {gameClock[0]} Hours {gameClock[1]} Minutes and {gameClock[2]} Seconds.")
                await ctx.send(embed=embedVar)

                if botActive:                    
                    await curse(5, str(ctx.author))
                    embedVar = discord.Embed(title=f"PLAY AGAIN", description=f"Don't Worry! Losing is apart of the game. Use the #end command to `END` the tutorial lobby OR use #start to `PLAY AGAIN`", colour=0xe74c3c)
                    embedVar.set_author(name=f"You Lost...")
                    embedVar.add_field(name="Tips!", value="Equiping stronger `TITLES` and `ARMS` will make you character tougher in a fight!")
                    embedVar.set_footer(text="The #shop is full of strong CARDS, TITLES and ARMS try different combinations! ")
                    await ctx.send(embed=embedVar)

                continued = False

            elif t_health <=0:
                uid = o_DID
                ouser = await self.bot.fetch_user(uid)
                wintime = time.asctime()
                h_playtime = int(wintime[11:13])
                m_playtime = int(wintime[14:16])
                s_playtime = int(wintime[17:19])
                gameClock = getTime(int(h_gametime),int(m_gametime),int(s_gametime),h_playtime,m_playtime,s_playtime)
                if currentopponent != (total_legends - 1):
                    if botActive:                    
                        embedVar = discord.Embed(title=f"VICTORY", description=f"{t_card} has been defeated!", colour=0xe91e63)
                        embedVar.add_field(name="Continue...", value="Continue down the path to beat the Universe!")
                        embedVar.set_footer(text="The #shop is full of strong CARDS, TITLES and ARMS try different combinations! ")
                        await ctx.send(embed=embedVar)
                    
                    await bless(5, ctx.author)

                    emojis = ['👍', '👎']
                    accept = await ctx.send(f"{ctx.author.mention} would you like to continue?")
                    for emoji in emojis:
                        await accept.add_reaction(emoji)

                    def check(reaction, user):
                        return user == user1 and str(reaction.emoji) == '👍'
                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                        currentopponent = currentopponent + 1

                        continued = True
                    except:
                        embedVar = discord.Embed(title=f"{m.STORY_ENDED}", colour=0xe91e63)
                        embedVar.set_footer(text="Use .tales to play again")
                        await ctx.send(embed=embedVar)
                        return
                if t_card == legends[(total_legends - 1)]:
                    embedVar = discord.Embed(title=f"UNIVERSE CONQUERED", description=f"Universe {selected_universe} has been conquered", colour=0xe91e63)
                    embedVar.set_author(name=f"New Universes have been unlocked to explore!")
                    embedVar.set_footer(text="The #shop has been updated with new CARDS, TITLES and ARMS! ")
                    upload_query={'DISNAME': str(ctx.author)}
                    new_upload_query={'$addToSet': {'CROWN_TALES': selected_universe}}
                    r=db.updateUserNoFilter(upload_query, new_upload_query)
                    if selected_universe in available_universes:
                        await bless(25, ctx.author)
                    else:
                        await bless(500, ctx.author)
                    await ctx.send(embed=embedVar)
                    continued=False




        print("Quit")
  
    @commands.command()
    async def boss(self, ctx, *args):
        t_available = False
        universeName = " ".join([*args])
        universe = db.queryUniverse({'TITLE': str(universeName)})
        bossname = ''
        starttime = time.asctime()
        h_gametime = starttime[11:13]
        m_gametime = starttime[14:16]
        s_gametime = starttime[17:19]

        sowner = db.queryUser({'DISNAME': str(ctx.author)})


        bossname = universe['UNIVERSE_BOSS']
        boss = db.queryBoss({'NAME': str(bossname)})


        o = db.queryCard({'NAME': sowner['CARD']})
        otitle = db.queryTitle({'TITLE': sowner['TITLE']})
        
        t = db.queryCard({'NAME': boss['CARD']})
        ttitle = db.queryTitle({'TITLE': boss['TITLE']})

        ####################################################################
        #PLayer Data



        # Player 1 Data
        o_user = sowner
        oarm = db.queryArm({'ARM': o_user['ARM']})
        oarm_passive = oarm['ABILITIES'][0]
        oarm_name=oarm['ARM']
        o_DID = o_user['DID']
        o_card = o['NAME']
        o_card_path=o['PATH']
        o_rcard_path=o['RPATH']
        o_max_health = o['HLT']
        o_health = o['HLT']
        o_stamina = o['STAM']
        o_max_stamina = o['STAM']
        o_moveset = o['MOVESET']
        o_attack = o['ATK']
        o_defense = o['DEF']
        o_type = o['TYPE']
        o_accuracy = o['ACC']
        o_passive = o['PASS'][0]
        o_speed = o['SPD']
        o_universe = o['UNIVERSE']
        o_title_universe = otitle['UNIVERSE']
        o_title_passive = otitle['ABILITIES'][0]
        o_vul = False
        user1 = await self.bot.fetch_user(o_DID)
        o_title_passive_bool = False

        # Player 2 Data
        t_user = boss
        t_available = boss['AVAILABLE']
        if not t_available:
            embedVar = discord.Embed(title=f"Boss fight unavailable. ", colour=0xe91e63)
            await ctx.send(embed=embedVar)
            return
        tarm = db.queryArm({'ARM': t_user['ARM']})
        tarm_passive = tarm['ABILITIES'][0]
        tarm_name=tarm['ARM']
        #t_DID = t_user['DID']
        t_card = t['NAME']
        t_card_path=t['PATH']
        t_rcard_path=t['RPATH']
        t_max_health = t['HLT'] * 3
        t_health = t['HLT'] *3
        t_stamina = t['STAM']
        t_max_stamina= t['STAM']
        t_moveset = t['MOVESET']
        t_attack = t['ATK'] * 1.5
        t_defense = t['DEF'] * 1.5
        t_type = t['TYPE']
        t_accuracy = t['ACC']
        t_passive = t['PASS'][0]
        t_speed = t['SPD']
        t_universe = t['UNIVERSE']
        t_title_universe = ttitle['UNIVERSE']
        t_title_passive = ttitle['ABILITIES'][0]
        t_vul = False
        #user2 = await self.bot.fetch_user(t_DID)
        t_title_passive_bool = False

        ################################################################################
        ##world Building
        t_arena = t_user['DESCRIPTION'][0]
        t_arenades = t_user['DESCRIPTION'][1]
        t_entrance = t_user['DESCRIPTION'][2]
        t_description = t_user['DESCRIPTION'][3]
        t_welcome = t_user['DESCRIPTION'][4]
        t_feeling = t_user['DESCRIPTION'][5]
        t_powerup = t_user['DESCRIPTION'][6]
        t_aura = t_user['DESCRIPTION'][7]
        t_assault = t_user['DESCRIPTION'][8]
        t_world = t_user['DESCRIPTION'][9]
        t_punish = t_user['DESCRIPTION'][10]
        t_rmessage = t_user['DESCRIPTION'][11]
        t_rebuke = t_user['DESCRIPTION'][12]
        t_concede = t_user['DESCRIPTION'][13]
        t_wins = t_user['DESCRIPTION'][14]
        
        
        ################################################################################

        # Player 1 Passive Config
        if (o_universe == o_title_universe) or (o_title_universe == "Unbound"):
            o_title_passive_bool = True
        
        # Player 1 Focus & Resolve
        o_focus = 60
        o_used_focus=False
        o_resolve = 50
        o_used_resolve=False

        # Player 1 Moves
        o_1 = o_moveset[0]
        o_2 = o_moveset[1]
        o_3 = o_moveset[2]
        o_enhancer = o_moveset[3]
        o_enhancer_used=False

        # Player 1 Card Passive
        o_card_passive_type = list(o_passive.values())[1]
        o_card_passive = list(o_passive.values())[0] * 2

        if o_card_passive_type == 'ATK':
            o_attack = o_attack + int(o_card_passive)
        elif o_card_passive_type == 'DEF':
            o_defense = o_defense + int(o_card_passive)
        elif o_card_passive_type == 'STAM':
            o_stamina = o_stamina + int(o_card_passive)
        elif o_card_passive_type == 'HLT':
            o_health = o_health + int(o_card_passive)
        elif o_card_passive_type == 'LIFE':
            o_health = o_health + round(int(o_card_passive) + (.10 * t_health))
        elif o_card_passive_type == 'DRAIN':
            o_stamina = o_stamina + int(o_card_passive)

        # Title Passive
        o_title_passive_type = list(o_title_passive.keys())[0]
        o_title_passive_value = list(o_title_passive.values())[0]

        if o_title_passive_bool:
            if o_title_passive_type == 'ATK':
                o_attack = o_attack + int(o_title_passive_value)
            elif o_title_passive_type == 'DEF':
                o_defense = o_defense + int(o_title_passive_value)
            elif o_title_passive_type == 'STAM':
                o_stamina = o_stamina + int(o_title_passive_value)
            elif o_title_passive_type == 'HLT':
                o_health = o_health + int(o_title_passive_value)

        # Arm Passive Player 1
        oarm_passive_type = list(oarm_passive.keys())[0]
        oarm_passive_value = list(oarm_passive.values())[0]

        if oarm_passive_type == 'ATK':
            o_attack = o_attack + int(oarm_passive_value)
        elif oarm_passive_type == 'DEF':
            o_defense = o_defense + int(oarm_passive_value)
        elif oarm_passive_type == 'STAM':
            o_stamina = o_stamina + int(oarm_passive_value)
        elif oarm_passive_type == 'HLT':
            o_health = o_health + int(oarm_passive_value)

        # Arm Passive Player 2
        tarm_passive_type = list(tarm_passive.keys())[0]
        tarm_passive_value = list(tarm_passive.values())[0]

        if tarm_passive_type == 'ATK':
            t_attack = t_attack + int(tarm_passive_value)
        elif tarm_passive_type == 'DEF':
            t_defense = t_defense + int(tarm_passive_value)
        elif tarm_passive_type == 'STAM':
            t_stamina = t_stamina + int(tarm_passive_value)
        elif tarm_passive_type == 'HLT':
            t_health = t_health + int(tarm_passive_value)

        


        # Player 2 Passive Config
        if (t_universe == t_title_universe) or (t_title_universe == "Unbound"):
            t_title_passive_bool = True
        
        # Player 1 Card Passive
        t_card_passive_type = list(t_passive.values())[1]
        t_card_passive = list(t_passive.values())[0]

        if t_card_passive_type == 'ATK':
            t_attack = t_attack + int(t_card_passive)
        elif t_card_passive_type == 'DEF':
            t_defense = t_defense + int(t_card_passive)
        elif t_card_passive_type == 'STAM':
            t_stamina = t_stamina + int(t_card_passive)
        elif t_card_passive_type == 'HLT':
            t_health = t_health + int(t_card_passive)
        elif t_card_passive_type == 'LIFE':
            t_health = t_health + round(int(t_card_passive) + (.10 * o_health))
        elif t_card_passive_type == 'DRAIN':
            t_stamina = t_stamina + int(t_card_passive)

        # Title Passive
        t_title_passive_type = list(t_title_passive.keys())[0]
        t_title_passive_value = list(t_title_passive.values())[0]

        if t_title_passive_bool:
            if t_title_passive_type == 'ATK':
                t_attack = t_attack + int(t_title_passive_value)
            elif t_title_passive_type == 'DEF':
                t_defense = t_defense + int(t_title_passive_value)
            elif t_title_passive_type == 'STAM':
                t_stamina = t_stamina + int(t_title_passive_value)
            elif t_title_passive_type == 'HLT':
                t_health = t_health + int(t_title_passive_value)


        # Player 2 Moves
        t_1 = t_moveset[0]
        t_2 = t_moveset[1]
        t_3 = t_moveset[2]
        t_enhancer = t_moveset[3]
        t_enhancer_used=False

        # Player 1 Focus & Resolve
        t_focus = 60
        t_used_focus=False
        t_resolve = 50
        t_used_resolve=False
        
        # Turn iterator
        turn = 0
        # Enhance Turn Iterators
        eo=0
        et=0

        botActive = True
            

        # Vulnerability Check
        if o_type == 0 and t_type == 2:
            o_vul=True
        if t_type == 0 and o_type == 2:
            t_vul=True
        
        options = [1,2,3,4,5,0]
        

        # Count Turns
        turn_total = 0

        await ctx.send(f"{user1.mention}: `{o_card}` VS {t_universe} BOSS : `{t_card}` has begun!")
        # START TURNS
        while (o_health > 0) and (t_health > 0) and t_available:
            
            #Player 1 Turn Start
            if turn == 0:

                # Tutorial Instructions
                if turn_total == 0 and botActive:                    
                    embedVar = discord.Embed(title=f"`{t_card}` Boss of `{t_universe}`", description=f"*{t_description}*", colour=0xe91e63)
                    embedVar.add_field(name=f"{t_arena}", value=f"{t_arenades}")
                    embedVar.add_field(name=f"Entering the {t_arena}",value= f"{t_entrance}", inline=False)
                    embedVar.set_footer(text=f"{t_card} waits for you to strike....")
                    await ctx.send(embed=embedVar)
                

                if o_health <= (o_max_health * .25):
                    embed_color_o=0xe74c3c
                    
                elif o_health <= (o_max_health * .50):
                    embed_color_o=0xe67e22
                elif o_health <= (o_max_health * .75):
                    embed_color_o=0xf1c40f
                    
                else:
                    embed_color_o = 0x2ecc71

                if o_stamina <= 0:
                    if botActive and not o_used_focus:                    
                        embedVar = discord.Embed(title=f"{t_punish}")
                        embedVar.add_field(name=f"{t_arena}",value= f"{t_world}", inline=False)
                        embedVar.set_footer(text=f"{t_assault}")
                        await ctx.send(embed=embedVar)
                    #fortitude or luck is based on health  
                    fortitude = 0.0
                    low = o_health - (o_health*.90)
                    high = o_health- (o_health*.80)
                    fortitude = random.randint(int(low), int(high))

                    o_stamina = o_focus
                    o_healthcalc = round(((o_focus * .40) + (fortitude * 1))/2)
                    o_attackcalc = round(.20 * ((o_focus * .15) + round(fortitude * 1)))
                    o_defensecalc = round(.20 * ((o_focus * .15) + round(fortitude * 1)))
                    #check if user is at max health and sets messages and focus health value
                    o_newhealth = 0
                    healmessage = ""
                    messagenumber = 0
                    if o_health <= o_max_health:
                        o_newhealth = o_health + o_healthcalc
                        if o_newhealth > o_max_health:
                            healmessage = "the injuries dissapeared"
                            messagenumber = 1
                            o_health = o_max_health
                        else:
                            healmessage = "regained some vitality"
                            messagenumber = 2
                            o_health = o_newhealth
                    else:
                        healmessage = f"`{t_card}`'s blows don't appear to have any effect!"
                        messagenumber = 0
                    o_attack = o_attack + o_attackcalc
                    o_defense =  o_defense + o_defensecalc
                    o_used_focus = True

                    embedVar = discord.Embed(title=f"{o_card} focused and {healmessage}", description="All stats increased", colour=embed_color_o)
                    await ctx.send(embed=embedVar)

                    if messagenumber != 2:
                        if messagenumber == 1:
                            embedVar = discord.Embed(title=f"{o_card} Stamina has recovered!", colour=embed_color_o)
                            await ctx.send(embed=embedVar)
                        else:
                            embedVar = discord.Embed(title=f"{o_card} Stamina has recovered!", colour=embed_color_o)
                            await ctx.send(embed=embedVar)
                    else:
                        embedVar = discord.Embed(title=f"{o_card} Stamina has recovered!", colour=embed_color_o)
                        await ctx.send(embed=embedVar)
                    turn_total= turn_total + 1
                    turn = 1
                else:

                    # UNIVERSE CARD
                    player_1_card = showcard(o, o_max_health, o_health, o_max_stamina, o_stamina, o_used_resolve, otitle, o_used_focus)
                    await ctx.send(file=player_1_card)
                    embedVar = discord.Embed(title=f"{o_card} What move will you use?", description=f"{t_card} currently has {t_health} health and {t_stamina} stamina.", colour=embed_color_o)
                    if o_used_focus and not o_used_resolve:
                        embedVar.set_author(name="Press 5 to strengthen resolve!")
                    embedVar.set_footer(text="Use 1 for Basic Attack, 2 for Special Attack, 3 for Ultimate Move, and 4 for Enhancer")
                    await ctx.send(embed=embedVar)
                    
                    # Make sure user is responding with move
                    def check(msg):
                        return msg.author == user1 and msg.channel == ctx.channel and int(msg.content) in options
                    try:
                        msg = await self.bot.wait_for("message",timeout=240.0, check=check)

                        # calculate data based on selected move
                        if int(msg.content) == 0:
                            o_health=0
                        if int(msg.content) == 1:
                            dmg = damage_cal(o_card, o_1, o_attack, o_defense, t_defense, o_vul, o_accuracy, o_stamina, o_enhancer_used, o_health, t_health, t_stamina)
                        elif int(msg.content) == 2:
                            dmg = damage_cal(o_card, o_2, o_attack, o_defense, t_defense, o_vul, o_accuracy, o_stamina, o_enhancer_used, o_health, t_health, t_stamina)
                        elif int(msg.content) == 3:
                            dmg = damage_cal(o_card, o_3, o_attack, o_defense, t_defense, o_vul, o_accuracy, o_stamina, o_enhancer_used, o_health, t_health, t_stamina)
                        elif int(msg.content) == 4:
                            o_enhancer_used=True
                            dmg = damage_cal(o_card, o_enhancer, o_attack, o_defense, t_defense, o_vul, o_accuracy, o_stamina, o_enhancer_used, o_health, t_health, t_stamina)
                            o_enhancer_used=False
                        elif int(msg.content) == 5:

                            #Resolve Check and Calculation
                            if not o_used_resolve and o_used_focus:

                                if botActive:                    
                                    embedVar = discord.Embed(title=f"`{t_card}` Snarls", description=f"{t_rebuke}", colour=0xe91e63)
                                    embedVar.add_field(name=f"`{o_card}` Says", value="You have not faced me.")
                                    embedVar.set_footer(text=f"{t_card} enrages in anticipation of your next attack!")
                                    await ctx.send(embed=embedVar)
                                    

                                #fortitude or luck is based on health  
                                fortitude = 0.0
                                low = o_health - (o_health * .75)
                                high = o_health- (o_health * .66)
                                fortitude = random.randint(int(low), int(high))
                                #Resolve Scaling
                                o_resolve_health = round(fortitude + (.5*o_resolve))
                                o_resolve_attack = round(4 * (o_resolve / (.50 * o_attack)))
                                o_resolve_defense = round(3 * (o_resolve / (.25 * o_defense)))

                                o_stamina = o_stamina + o_resolve
                                o_health = o_health + o_resolve_health
                                o_attack = round(o_attack + o_resolve_attack)
                                o_defense = round(o_defense - o_resolve_defense)
                                o_used_resolve = True 

                                embedVar = discord.Embed(title=f"{o_card} strengthened resolve!", colour=embed_color_o)
                                await ctx.send(embed=embedVar)
                                turn_total= turn_total + 1
                                turn=1
                            else:
                                emessage = m.CANNOT_USE_RESOLVE
                                embedVar = discord.Embed(title=emessage, description=f"Entering `Resolved State` sacrifices a turn to power up even greater and regain `Stamina`!", colour=0xe91e63)
                                await ctx.send(embed=embedVar)
                                turn=0

                        if int(msg.content) !=5:
                            # If you have enough stamina for move, use it
                            if dmg['CAN_USE_MOVE']:
                                if dmg['ENHANCE']:
                                    enh_type= dmg['ENHANCED_TYPE']
                                
                                    if enh_type == 'ATK':
                                        o_attack = round(o_attack + dmg['DMG'])
                                    elif enh_type == 'DEF':
                                        o_defense = round(o_defense + dmg['DMG'])
                                    elif enh_type == 'STAM':
                                        o_stamina = round(o_stamina + dmg['DMG'])
                                    elif enh_type == 'HLT':
                                        o_health = round(o_health + dmg['DMG'])
                                    elif enh_type == 'LIFE':
                                        o_health = round(o_health + dmg['DMG'])
                                        t_health = round(t_health - dmg['DMG'])
                                    elif enh_type == 'DRAIN':
                                        o_stamina = round(o_stamina + dmg['DMG'])
                                        t_stamina = round(t_stamina - dmg['DMG'])
                                    o_stamina = o_stamina - int(dmg['STAMINA_USED'])

                                    embedVar = discord.Embed(title=f"{dmg['MESSAGE']}", colour=embed_color_o)
                                    await ctx.send(embed=embedVar)
                                    turn_total= turn_total + 1
                                    turn=1
                                elif dmg['DMG'] == 0:
                                    o_stamina = o_stamina - int(dmg['STAMINA_USED'])

                                    embedVar = discord.Embed(title=f"{dmg['MESSAGE']}", colour=embed_color_o)
                                    await ctx.send(embed=embedVar)
                                    turn_total= turn_total + 1
                                    turn=1
                                else:
                                    t_health = t_health - dmg['DMG']
                                    if t_health < 0:
                                        t_health=0
                                    o_stamina = o_stamina - dmg['STAMINA_USED']

                                    embedVar = discord.Embed(title=f"{dmg['MESSAGE']}", colour=embed_color_o)
                                    await ctx.send(embed=embedVar)
                                    turn_total= turn_total + 1
                                    turn=1
                            else:
                                emessage = m.NOT_ENOUGH_STAMINA
                                embedVar = discord.Embed(title=emessage, description=f"Use abilities to Increase `STAM` or enter `FOCUS STATE`!", colour=0xe91e63)
                                await ctx.send(embed=embedVar)
                                turn=0
                    except:
                        emessage = m.DID_NOT_WORK
                        embedVar = discord.Embed(title=emessage, description=f"Try Again", colour=0xe91e63)
                        await ctx.send(embed=embedVar)
            #PLayer 2 Turn Start
            elif turn == 1:

                # Boss Conversation Instructions
                if turn_total == 1 and botActive:                    
                    embedVar = discord.Embed(title=f"`{t_card}` Says : ", description=f"{t_welcome}", colour=0xe91e63)
                    embedVar.add_field(name=f"`{o_card}` Braces: ",value=f"{t_feeling}")
                    embedVar.set_footer(text=f" The {t_card} begins his assault")
                    await ctx.send(embed=embedVar)
                
                if t_health <= (t_max_health * .25):
                    embed_color_t=0xe74c3c
                    
                elif t_health <= (t_max_health * .50):
                    embed_color_t=0xe67e22
                elif t_health <= (t_max_health * .75):
                    embed_color_t=0xf1c40f
                else:
                    embed_color_t = 0x2ecc71

                #Focus
                if t_stamina <= 0:
                    if botActive and not o_used_focus:                    
                        embedVar = discord.Embed(title=f"`{t_card}` Says ", description=f"{t_powerup}", colour=0xe91e63)
                        embedVar.add_field(name=f"A great aura starts to envelop `{t_card}` ",value= f"{t_aura}")
                        embedVar.set_footer(text=f"{t_card} Says: 'Now, are you ready for a real fight?'")
                        await ctx.send(embed=embedVar)

                    fortitude = 0.0
                    low = t_health - (t_health*.90)
                    high = t_health- (t_health*.80)
                    fortitude = random.randint(int(low), int(high))

                    t_stamina = t_focus
                    t_healthcalc = round(((t_focus * .40) + (fortitude * 1))/2)
                    t_attackcalc = round(.20 * ((t_focus * .15) + round(fortitude * 1)))
                    t_defensecalc = round(.20 * ((t_focus * .10) + round(fortitude * 1)))
                    t_newhealth = 0
                    healmessage = ""
                    messagenumber = 0

                    if t_health <= t_max_health:
                        t_newhealth = t_health + t_healthcalc
                        if t_newhealth > t_max_health:
                            healmessage = f"recovered!"
                            messagenumber = 1
                            t_health = t_max_health
                        else:
                            healmessage = f"stopped the bleeding..."
                            messagenumber = 2
                            t_health = t_newhealth
                    else:
                        healmessage = f"hasn't been touched..."
                        messagenumber = 0

                    t_attack = t_attack + t_attackcalc
                    t_defense =  t_defense + t_defensecalc
                    t_used_focus=True
                    embedVar = discord.Embed(title=f"{t_card} focused and {healmessage}", description="All stats increased", colour=embed_color_t)
                    await ctx.send(embed=embedVar)

                    if messagenumber != 2:
                        if messagenumber == 1:
                            embedVar = discord.Embed(title=f"{t_card} Stamina has recovered", colour=embed_color_t)
                            await ctx.send(embed=embedVar)
                        else:
                            embedVar = discord.Embed(title=f"{t_card} Stamina has recovered", colour=embed_color_t)
                            await ctx.send(embed=embedVar)
                    else:
                        embedVar = discord.Embed(title=f"{t_card} Stamina has recovered", colour=embed_color_t)
                        await ctx.send(embed=embedVar)
                    turn_total= turn_total + 1
                    turn=0
                else:
                    # UNIVERSE CARD
                    player_2_card = showcard(t, t_max_health, t_health, t_max_stamina, t_stamina, t_used_resolve, ttitle, t_used_focus)
                    await ctx.send(file=player_2_card)

                    embedVar = discord.Embed(title=f"{t_card} What move will you use?", description=f"{o_card} currently has {o_health} health and {o_stamina} stamina.", colour=embed_color_t)
                    if t_used_focus and not t_used_resolve:
                        embedVar.set_author(name="Press 5 to strengthen resolve!")
                    embedVar.set_footer(text="Use 1 for Basic Attack, 2 for Special Attack, 3 for Ultimate Move, and 4 for Enhancer")
                    await ctx.send(embed=embedVar)
                    aiMove = 0
                    

                    if o_stamina == 0:
                        aiMove = 1
                    elif t_stamina >= 160 and (t_health >= o_health):
                        aiMove = 3
                    elif t_stamina >= 160:
                        aiMove = 3                                   
                    elif t_stamina >= 150 and (t_health >= o_health):
                        aiMove = 1
                    elif t_stamina >= 150:
                        aiMove = 1                                     
                    elif t_stamina >= 140 and (t_health >= o_health):
                        aiMove = 1
                    elif t_stamina >= 140:
                        aiMove = 3                                      
                    elif t_stamina >= 130 and (t_health >= o_health):
                        aiMove = 1
                    elif t_stamina >= 130:
                        aiMove = 3                                     
                    elif t_stamina >= 120 and (t_health >= o_health):
                        aiMove = 2
                    elif t_stamina >= 120:
                        aiMove = 3                                 
                    elif t_stamina >= 110 and (t_health >= o_health):
                        aiMove = 1
                    elif t_stamina >= 110:
                        aiMove = 2                                   
                    elif t_stamina >= 100 and (t_health >= o_health):
                        aiMove = 4
                    elif t_stamina >= 100:
                        aiMove = 1
                    elif t_stamina >= 90 and (t_health >= o_health):
                        aiMove = 3
                    elif t_stamina >= 90:
                        aiMove = 4
                    elif t_stamina >= 80 and (t_health >= o_health):
                        aiMove = 1
                    elif t_stamina >= 80:
                        aiMove = 3
                    elif t_stamina >= 70 and (t_health >= o_health):
                        aiMove = 4
                    elif t_stamina >= 70:
                        aiMove = 1
                    elif t_stamina >= 60 and (t_health >= o_health):
                        if t_used_resolve == False and t_used_focus:
                            aiMove = 5
                        elif t_used_focus == False:
                            aiMove = 2
                        else:
                            aiMove = 1 
                    elif t_stamina >= 60:
                        if t_used_resolve == False and t_used_focus:
                            aiMove = 5
                        elif t_used_focus == False:
                            aiMove = 2
                        else:
                            aiMove = 1 
                    elif t_stamina >= 50 and (t_health >= o_health):
                        if t_stamina >= o_stamina:
                            aiMove = 4
                        else:
                            aiMove = 1
                    elif t_stamina >= 50:
                        aiMove = 2
                    elif t_stamina >= 40 and (t_health >= o_health):
                        aiMove = 1
                    elif t_stamina >= 40:
                        aiMove = 2
                    elif t_stamina >= 30 and (t_health >= o_health):
                        aiMove = 4
                    elif t_stamina >= 30:
                        aiMove = 2
                    elif t_stamina >= 20 and (t_health >= o_health):
                        aiMove = 1
                    elif t_stamina >= 20:
                        aiMove = 4
                    elif t_stamina >= 10:
                        aiMove = 1
                    else:
                        aiMove = 0
                    

                    if int(aiMove) == 0:
                        t_health=0
                    if int(aiMove) == 1:
                        dmg = damage_cal(t_card, t_1, t_attack, t_defense, o_defense, t_vul, t_accuracy, t_stamina, t_enhancer_used, t_health, o_health, o_stamina)
                    elif int(aiMove) == 2:
                        dmg = damage_cal(t_card, t_2, t_attack, t_defense, o_defense, t_vul, t_accuracy, t_stamina, t_enhancer_used, t_health, o_health, o_stamina)
                    elif int(aiMove) == 3:
                        dmg = damage_cal(t_card, t_3, t_attack, t_defense, o_defense, t_vul, t_accuracy, t_stamina, t_enhancer_used, t_health, o_health, o_stamina)
                    elif int(aiMove) == 4:
                        t_enhancer_used=True
                        dmg = damage_cal(t_card, t_enhancer, t_attack, t_defense, o_defense, t_vul, t_accuracy, t_stamina, t_enhancer_used, t_health,o_health, o_stamina)
                        t_enhancer_used=False
                    elif int(aiMove) == 5:
                        if not t_used_resolve and t_used_focus:

                            if botActive:                    
                                embedVar = discord.Embed(title=f"{t_card} is Resolved", description=f"{t_rmessage}", colour=0xe91e63)
                                embedVar.add_field(name=f"{o_card} are you ready?", value="This will not be easy.")
                                embedVar.set_footer(text=f"{o_card} take advantage of its current state and end this !")
                                await ctx.send(embed=embedVar)
                            #fortitude or luck is based on health  
                            fortitude = 0.0
                            low = t_health - (t_health * .75)
                            high = t_health- (t_health * .66)
                            fortitude = random.randint(int(low), int(high))
                            #Resolve Scaling
                            t_resolve_health = round(fortitude + (.5*t_resolve))
                            t_resolve_attack = round(4 * (t_resolve / (.25 * t_attack)))
                            t_resolve_defense = round(3 * (t_resolve / (.25 * t_defense)))

                            t_stamina = t_stamina + t_resolve
                            t_health = t_health + t_resolve_health
                            t_attack = round(t_attack + t_resolve_attack)
                            t_defense = round(t_defense - t_resolve_defense)
                            t_used_resolve=True
                            embedVar = discord.Embed(title=f"{t_card} strengthened resolve!", colour=embed_color_t)
                            await ctx.send(embed=embedVar)
                            turn_total= turn_total + 1
                            turn=0
                        else:
                            await ctx.send(m.CANNOT_USE_RESOLVE)
                            turn=1

                    if int(aiMove) !=5:
                        # If you have enough stamina for move, use it
                        if dmg['CAN_USE_MOVE']:

                            if dmg['ENHANCE']:
                                enh_type= dmg['ENHANCED_TYPE']
                                if enh_type == 'ATK':
                                    t_attack = round(t_attack + dmg['DMG'])
                                elif enh_type == 'DEF':
                                    t_defense = round(t_defense + dmg['DMG'])
                                elif enh_type == 'STAM':
                                    t_stamina = round(t_stamina + dmg['DMG'])
                                elif enh_type == 'HLT':
                                    t_health = round(t_health + dmg['DMG'])
                                elif enh_type == 'LIFE':
                                    t_health = round(t_health + dmg['DMG'])
                                    o_health = round(o_health - dmg['DMG'])
                                elif enh_type == 'DRAIN':
                                    t_stamina = round(t_stamina + dmg['DMG'])
                                    o_stamina = round(o_stamina - dmg['DMG'])
                                t_stamina = t_stamina - int(dmg['STAMINA_USED'])
                                embedVar = discord.Embed(title=f"{dmg['MESSAGE']}", colour=embed_color_t)
                                await ctx.send(embed=embedVar)
                                turn_total= turn_total + 1
                                turn = 0
                            elif dmg['DMG'] == 0:
                                t_stamina = t_stamina - int(dmg['STAMINA_USED'])
                                embedVar = discord.Embed(title=f"{dmg['MESSAGE']}", colour=embed_color_t)
                                await ctx.send(embed=embedVar)
                                turn_total= turn_total + 1
                                turn=0
                            else:
                                o_health = o_health - int(dmg['DMG'])
                                if o_health < 0:
                                    o_health=0
                                t_stamina = t_stamina - int(dmg['STAMINA_USED'])

                                embedVar = discord.Embed(title=f"{dmg['MESSAGE']}", colour=embed_color_t)
                                await ctx.send(embed=embedVar)
                                turn_total= turn_total + 1
                                turn=0

                        else:
                            await ctx.send(m.NOT_ENOUGH_STAMINA)
                            turn = 1
        if botActive:
            end_message="Use the #end command to end the tutorial lobby"
        else:
            end_message="Try Again"
        # End the match
        if o_health <= 0:
            # await ctx.send(f":zap: {user2.mention} you win the match!")
            wintime = time.asctime()
            h_playtime = int(wintime[11:13])
            m_playtime = int(wintime[14:16])
            s_playtime = int(wintime[17:19])
            gameClock = getTime(int(h_gametime),int(m_gametime),int(s_gametime),h_playtime,m_playtime,s_playtime)

            embedVar = discord.Embed(title=f":zap: `{t_card}` {t_wins}", description=f"Match concluded in {turn_total} turns!", colour=0x1abc9c)
            embedVar.set_author(name=f"{o_card} lost!\n{end_message}", icon_url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620236432/PCG%20LOGOS%20AND%20RESOURCES/PCGBot_1.png")
            if int(gameClock[0]) == 0 and int(gameClock[1]) == 0:
                embedVar.set_footer(text=f"Play again?\nBattle Time: {gameClock[2]} Seconds.")
            elif int(gameClock[0]) == 0:
                embedVar.set_footer(text=f"Play again?\nBattle Time: {gameClock[1]} Minutes and {gameClock[2]} Seconds.")
            else: 
                embedVar.set_footer(text=f"Play again?\nBattle Time: {gameClock[0]} Hours {gameClock[1]} Minutes and {gameClock[2]} Seconds.")
            await ctx.send(embed=embedVar)
            if botActive:                    
                embedVar = discord.Embed(title=f"PLAY AGAIN", description=f"{t_card} was too powerful level up your character and try again...", colour=0xe74c3c)
                embedVar.set_author(name=f"You Lost...")
                embedVar.add_field(name="Tips!", value="Equiping stronger `TITLES` and `ARMS` will make you character tougher in a fight!")
                embedVar.set_footer(text="The #shop is full of strong CARDS, TITLES and ARMS try different combinations! ")
                await ctx.send(embed=embedVar)

        elif t_health <=0:
            uid = o_DID
            ouser = await self.bot.fetch_user(uid)
            wintime = time.asctime()
            h_playtime = int(wintime[11:13])
            m_playtime = int(wintime[14:16])
            s_playtime = int(wintime[17:19])
            gameClock = getTime(int(h_gametime),int(m_gametime),int(s_gametime),h_playtime,m_playtime,s_playtime)
            await bless(50, str(ctx.author))
            embedVar = discord.Embed(title=f":zap: `{o_card}`defeated the {t_universe} Boss {t_card}!\n{t_concede}", description=f"Match concluded in {turn_total} turns!", colour=0xe91e63)
            embedVar.set_author(name=f"{t_card} lost!\n{end_message}", icon_url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620236432/PCG%20LOGOS%20AND%20RESOURCES/PCGBot_1.png")
            if int(gameClock[0]) == 0 and int(gameClock[1]) == 0:
                embedVar.set_footer(text=f"Play again?\nBattle Time: {gameClock[2]} Seconds.")
            elif int(gameClock[0]) == 0:
                embedVar.set_footer(text=f"Play again?\nBattle Time: {gameClock[1]} Minutes and {gameClock[2]} Seconds.")
            else: 
                embedVar.set_footer(text=f"Play again?\nBattle Time: {gameClock[0]} Hours {gameClock[1]} Minutes and {gameClock[2]} Seconds.")
            await ctx.send(embed=embedVar)
            if botActive:                    
                embedVar = discord.Embed(title=f"BOSS DEFEATED", description=f"Boss Victories are added to your player profile! Defeat {t_card} again to earn exotic loot!", colour=0xe91e63)
                embedVar.set_author(name=f"Congratulations You Defeated {t_card}!")
                embedVar.add_field(name="Tips!", value=f"Run #lookup {o_user} to view your Boss Souls")
                embedVar.set_footer(text="Bosses have a chance to drop :coin:, ARMS, TITLES, and even BOSS CARDS:eyes:")
                await ctx.send(embed=embedVar)
            
            if t_card not in sowner['BOSS_WINS']:
                await bless(1000, str(ctx.author))
                query = {'DISNAME': sowner['DISNAME']}
                new_query = {'$addToSet': {'BOSS_WINS': t_card}}
                resp = db.updateUserNoFilter(query, new_query)


    #senpai ai Template
    async def AiBot(self, ctx):
        session_query = {"OWNER": str(ctx.author), "AVAILABLE": True}
        session = db.querySession(session_query)
        if session:
            if session['GAME'] == 'Crown Unlimited':
                # Get Session Owner Disname for scoring
                sowner = db.queryUser({'DISNAME': str(session['OWNER'])})

                teams = [x for x in session['TEAMS']]
                team_1 = [x for x in teams if x['POSITION'] == 0][0] # position 0
                team_2 = [x for x in teams if x['POSITION'] == 1][0] # position 1

                o = db.queryCard({'NAME': team_1['CARD']})
                otitle = db.queryTitle({'TITLE': team_1['TITLE']})

                t = db.queryCard({'NAME': team_2['CARD']})
                ttitle = db.queryTitle({'TITLE': team_1['TITLE']})

                ####################################################################
                #PLayer Data



                # Player 1 Data
                o_user = db.queryUser({'DISNAME': team_1['TEAM'][0]})
                oarm = db.queryArm({'ARM': o_user['ARM']})
                oarm_passive = oarm['ABILITIES'][0]
                oarm_name=oarm['ARM']
                o_DID = o_user['DID']
                o_card = o['NAME']
                o_card_path=o['PATH']
                o_rcard_path=o['RPATH']
                o_max_health = o['HLT']
                o_health = o['HLT']
                o_stamina = o['STAM']
                o_max_stamina = o['STAM']
                o_moveset = o['MOVESET']
                o_attack = o['ATK']
                o_defense = o['DEF']
                o_type = o['TYPE']
                o_accuracy = o['ACC']
                o_passive = o['PASS'][0]
                o_speed = o['SPD']
                o_universe = o['UNIVERSE']
                o_title_universe = otitle['UNIVERSE']
                o_title_passive = otitle['ABILITIES'][0]
                o_vul = False
                user1 = await self.bot.fetch_user(o_DID)
                o_title_passive_bool = False

                # Player 2 Data
                t_user = db.queryUser({'DISNAME': team_2['TEAM'][0]})
                tarm = db.queryArm({'ARM': t_user['ARM']})
                tarm_passive = tarm['ABILITIES'][0]
                tarm_name=tarm['ARM']
                t_DID = t_user['DID']
                t_card = t['NAME']
                t_card_path=t['PATH']
                t_rcard_path=t['RPATH']
                t_max_health = t['HLT']
                t_health = t['HLT']
                t_stamina = t['STAM']
                t_max_stamina= t['STAM']
                t_moveset = t['MOVESET']
                t_attack = t['ATK']
                t_defense = t['DEF']
                t_type = t['TYPE']
                t_accuracy = t['ACC']
                t_passive = t['PASS'][0]
                t_speed = t['SPD']
                t_universe = t['UNIVERSE']
                t_title_universe = ttitle['UNIVERSE']
                t_title_passive = ttitle['ABILITIES'][0]
                t_vul = False
                user2 = await self.bot.fetch_user(t_DID)
                t_title_passive_bool = False
                
                ################################################################################

                # Player 1 Passive Config
                if (o_universe == o_title_universe) or (o_title_universe == "Unbound"):
                    o_title_passive_bool = True
                
                # Player 1 Focus & Resolve
                o_focus = 60
                o_used_focus=False
                o_resolve = 50
                o_used_resolve=False

                # Player 1 Moves
                o_1 = o_moveset[0]
                o_2 = o_moveset[1]
                o_3 = o_moveset[2]
                o_enhancer = o_moveset[3]
                o_enhancer_used=False

                # Player 1 Card Passive
                o_card_passive_type = list(o_passive.values())[1]
                o_card_passive = list(o_passive.values())[0]

                if o_card_passive_type == 'ATK':
                    o_attack = o_attack + int(o_card_passive)
                elif o_card_passive_type == 'DEF':
                    o_defense = o_defense + int(o_card_passive)
                elif o_card_passive_type == 'STAM':
                    o_stamina = o_stamina + int(o_card_passive)
                elif o_card_passive_type == 'HLT':
                    o_health = o_health + int(o_card_passive)
                elif o_card_passive_type == 'LIFE':
                    o_health = o_health + round(int(o_card_passive) + (.10 * t_health))
                elif o_card_passive_type == 'DRAIN':
                    o_stamina = o_stamina + int(o_card_passive)

                # Title Passive
                o_title_passive_type = list(o_title_passive.keys())[0]
                o_title_passive_value = list(o_title_passive.values())[0]

                if o_title_passive_bool:
                    if o_title_passive_type == 'ATK':
                        o_attack = o_attack + int(o_title_passive_value)
                    elif o_title_passive_type == 'DEF':
                        o_defense = o_defense + int(o_title_passive_value)
                    elif o_title_passive_type == 'STAM':
                        o_stamina = o_stamina + int(o_title_passive_value)
                    elif o_title_passive_type == 'HLT':
                        o_health = o_health + int(o_title_passive_value)

                # Arm Passive Player 1
                oarm_passive_type = list(oarm_passive.keys())[0]
                oarm_passive_value = list(oarm_passive.values())[0]

                if oarm_passive_type == 'ATK':
                    o_attack = o_attack + int(oarm_passive_value)
                elif oarm_passive_type == 'DEF':
                    o_defense = o_defense + int(oarm_passive_value)
                elif oarm_passive_type == 'STAM':
                    o_stamina = o_stamina + int(oarm_passive_value)
                elif oarm_passive_type == 'HLT':
                    o_health = o_health + int(oarm_passive_value)

                # Arm Passive Player 2
                tarm_passive_type = list(tarm_passive.keys())[0]
                tarm_passive_value = list(tarm_passive.values())[0]

                if tarm_passive_type == 'ATK':
                    t_attack = t_attack + int(tarm_passive_value)
                elif tarm_passive_type == 'DEF':
                    t_defense = t_defense + int(tarm_passive_value)
                elif tarm_passive_type == 'STAM':
                    t_stamina = t_stamina + int(tarm_passive_value)
                elif tarm_passive_type == 'HLT':
                    t_health = t_health + int(tarm_passive_value)

                


                # Player 2 Passive Config
                if (t_universe == t_title_universe) or (t_title_universe == "Unbound"):
                    t_title_passive_bool = True
                
                # Player 1 Card Passive
                t_card_passive_type = list(t_passive.values())[1]
                t_card_passive = list(t_passive.values())[0]

                if t_card_passive_type == 'ATK':
                    t_attack = t_attack + int(t_card_passive)
                elif t_card_passive_type == 'DEF':
                    t_defense = t_defense + int(t_card_passive)
                elif t_card_passive_type == 'STAM':
                    t_stamina = t_stamina + int(t_card_passive)
                elif t_card_passive_type == 'HLT':
                    t_health = t_health + int(t_card_passive)
                elif t_card_passive_type == 'LIFE':
                    t_health = t_health + round(int(t_card_passive) + (.10 * o_health))
                elif t_card_passive_type == 'DRAIN':
                    t_stamina = t_stamina + int(t_card_passive)

                # Title Passive
                t_title_passive_type = list(t_title_passive.keys())[0]
                t_title_passive_value = list(t_title_passive.values())[0]

                if t_title_passive_bool:
                    if t_title_passive_type == 'ATK':
                        t_attack = t_attack + int(t_title_passive_value)
                    elif t_title_passive_type == 'DEF':
                        t_defense = t_defense + int(t_title_passive_value)
                    elif t_title_passive_type == 'STAM':
                        t_stamina = t_stamina + int(t_title_passive_value)
                    elif t_title_passive_type == 'HLT':
                        t_health = t_health + int(t_title_passive_value)


                # Player 2 Moves
                t_1 = t_moveset[0]
                t_2 = t_moveset[1]
                t_3 = t_moveset[2]
                t_enhancer = t_moveset[3]
                t_enhancer_used=False

                # Player 1 Focus & Resolve
                t_focus = 60
                t_used_focus=False
                t_resolve = 50
                t_used_resolve=False
                
                # Turn iterator
                turn = 0
                # Enhance Turn Iterators
                eo=0
                et=0

                start = starting_position(o_speed, t_speed)
                if start == True:
                    turn = 0
                else:
                    turn = 1    

                # Vulnerability Check
                if o_type == 0 and t_type == 2:
                    o_vul=True
                if t_type == 0 and o_type == 2:
                    t_vul=True
                
                options = [1,2,3,4,5,0]
                await ctx.send(f"{user1.mention}: `{o_card}` VS {user2.mention}: `{t_card}` has begun!")

                # Count Turns
                turn_total = 0

            

                # START TURNS
                while (o_health > 0) and (t_health > 0):

                    if turn == 0:
                        

                        if o_health <= (o_max_health * .25):
                            embed_color_o=0xe74c3c
                            
                        elif o_health <= (o_max_health * .50):
                            embed_color_o=0xe67e22
                        elif o_health <= (o_max_health * .75):
                            embed_color_o=0xf1c40f
                            
                        else:
                            embed_color_o = 0x2ecc71

                        if o_stamina <= 0:
                            #fortitude or luck is based on health  
                            fortitude = 0.0
                            low = o_health - (o_health*.90)
                            high = o_health- (o_health*.80)
                            fortitude = random.randint(int(low), int(high))

                            o_stamina = o_focus
                            o_healthcalc = round(((o_focus * .40) + (fortitude * 1))/2)
                            o_attackcalc = round(.20 * ((o_focus * .15) + round(fortitude * 1)))
                            o_defensecalc = round(.20 * ((o_focus * .15) + round(fortitude * 1)))
                            #check if user is at max health and sets messages and focus health value
                            o_newhealth = 0
                            healmessage = ""
                            messagenumber = 0
                            if o_health <= o_max_health:
                                o_newhealth = o_health + o_healthcalc
                                if o_newhealth > o_max_health:
                                    healmessage = "the injuries dissapeared"
                                    messagenumber = 1
                                    o_health = o_max_health
                                else:
                                    healmessage = "regained some vitality"
                                    messagenumber = 2
                                    o_health = o_newhealth
                            else:
                                healmessage = f"`{t_card}`'s blows don't appear to have any effect!"
                                messagenumber = 0
                            o_attack = o_attack + o_attackcalc
                            o_defense =  o_defense + o_defensecalc
                            o_used_focus = True

                            embedVar = discord.Embed(title=f"{o_card} focused and {healmessage}", description="All stats increased", colour=embed_color_o)
                            await ctx.send(embed=embedVar)

                            if messagenumber != 2:
                                if messagenumber == 1:
                                    embedVar = discord.Embed(title=f"{o_card} Stamina has recovered!", colour=embed_color_o)
                                    await ctx.send(embed=embedVar)
                                else:
                                    embedVar = discord.Embed(title=f"{o_card} Stamina has recovered!", colour=embed_color_o)
                                    await ctx.send(embed=embedVar)
                            else:
                                embedVar = discord.Embed(title=f"{o_card} Stamina has recovered!", colour=embed_color_o)
                                await ctx.send(embed=embedVar)
                            turn_total= turn_total + 1
                            turn = 1
                        else:

                            # UNIVERSE CARD
                            player_1_card = showcard(o, o_max_health, o_health, o_max_stamina, o_stamina, o_used_resolve, otitle, o_used_focus)
                            await ctx.send(file=player_1_card)
                            embedVar = discord.Embed(title=f"{o_card} What move will you use?", description=f"{t_card} currently has {t_health} health and {t_stamina} stamina.", colour=embed_color_o)
                            if o_used_focus and not o_used_resolve:
                                embedVar.set_author(name="Press 5 to strengthen resolve!")
                            embedVar.set_footer(text="Use 1 for Basic Attack, 2 for Special Attack, 3 for Ultimate Move, and 4 for Enhancer")
                            await ctx.send(embed=embedVar)

                            # Make sure user is responding with move
                            def check(msg):
                                return msg.author == user1 and msg.channel == ctx.channel and int(msg.content) in options
                            try:
                                msg = await self.bot.wait_for("message",timeout=240.0, check=check)

                                # calculate data based on selected move
                                if int(msg.content) == 0:
                                    o_health=0
                                if int(msg.content) == 1:
                                    dmg = damage_cal(o_card, o_1, o_attack, o_defense, t_defense, o_vul, o_accuracy, o_stamina, o_enhancer_used, o_health, t_health, t_stamina)
                                elif int(msg.content) == 2:
                                    dmg = damage_cal(o_card, o_2, o_attack, o_defense, t_defense, o_vul, o_accuracy, o_stamina, o_enhancer_used, o_health, t_health, t_stamina)
                                elif int(msg.content) == 3:
                                    dmg = damage_cal(o_card, o_3, o_attack, o_defense, t_defense, o_vul, o_accuracy, o_stamina, o_enhancer_used, o_health, t_health, t_stamina)
                                elif int(msg.content) == 4:
                                    o_enhancer_used=True
                                    dmg = damage_cal(o_card, o_enhancer, o_attack, o_defense, t_defense, o_vul, o_accuracy, o_stamina, o_enhancer_used, o_health, t_health, t_stamina)
                                    o_enhancer_used=False
                                elif int(msg.content) == 5:

                                    #Resolve Check and Calculation
                                    if not o_used_resolve and o_used_focus:
                                        #fortitude or luck is based on health  
                                        fortitude = 0.0
                                        low = o_health - (o_health * .75)
                                        high = o_health- (o_health * .66)
                                        fortitude = random.randint(int(low), int(high))
                                        #Resolve Scaling
                                        o_resolve_health = round(fortitude + (.5*o_resolve))
                                        o_resolve_attack = round(4 * (o_resolve / (.50 * o_attack)))
                                        o_resolve_defense = round(3 * (o_resolve / (.25 * o_defense)))

                                        o_stamina = o_stamina + o_resolve
                                        o_health = o_health + o_resolve_health
                                        o_attack = round(o_attack + o_resolve_attack)
                                        o_defense = round(o_defense - o_resolve_defense)
                                        o_used_resolve = True 

                                        embedVar = discord.Embed(title=f"{o_card} strengthened his resolve!", colour=embed_color_o)
                                        await ctx.send(embed=embedVar)
                                        turn_total= turn_total + 1
                                        turn=1
                                    else:
                                        await ctx.send(m.CANNOT_USE_RESOLVE)
                                        turn=0

                                if int(msg.content) !=5:
                                    # If you have enough stamina for move, use it
                                    if dmg['CAN_USE_MOVE']:
                                        if dmg['ENHANCE']:
                                            enh_type= dmg['ENHANCED_TYPE']
                                        
                                            if enh_type == 'ATK':
                                                o_attack = round(o_attack + dmg['DMG'])
                                            elif enh_type == 'DEF':
                                                o_defense = round(o_defense + dmg['DMG'])
                                            elif enh_type == 'STAM':
                                                o_stamina = round(o_stamina + dmg['DMG'])
                                            elif enh_type == 'HLT':
                                                o_health = round(o_health + dmg['DMG'])
                                            elif enh_type == 'LIFE':
                                                o_health = round(o_health + dmg['DMG'])
                                                t_health = round(t_health - dmg['DMG'])
                                            elif enh_type == 'DRAIN':
                                                o_stamina = round(o_stamina + dmg['DMG'])
                                                t_stamina = round(t_stamina - dmg['DMG'])
                                            o_stamina = o_stamina - int(dmg['STAMINA_USED'])

                                            embedVar = discord.Embed(title=f"{dmg['MESSAGE']}", colour=embed_color_o)
                                            await ctx.send(embed=embedVar)
                                            turn_total= turn_total + 1
                                            turn=1
                                        elif dmg['DMG'] == 0:
                                            o_stamina = o_stamina - int(dmg['STAMINA_USED'])

                                            embedVar = discord.Embed(title=f"{dmg['MESSAGE']}", colour=embed_color_o)
                                            await ctx.send(embed=embedVar)
                                            turn_total= turn_total + 1
                                            turn=1
                                        else:
                                            t_health = t_health - dmg['DMG']
                                            if t_health < 0:
                                                t_health=0
                                            o_stamina = o_stamina - dmg['STAMINA_USED']

                                            embedVar = discord.Embed(title=f"{dmg['MESSAGE']}", colour=embed_color_o)
                                            await ctx.send(embed=embedVar)
                                            turn_total= turn_total + 1
                                            turn=1
                                    else:
                                        await ctx.send(m.NOT_ENOUGH_STAMINA)
                                        turn=0
                            except:
                                await ctx.send('Did not work')

                    elif turn == 1:
                        
                        if t_health <= (t_max_health * .25):
                            embed_color_t=0xe74c3c
                            
                        elif t_health <= (t_max_health * .50):
                            embed_color_t=0xe67e22
                        elif t_health <= (t_max_health * .75):
                            embed_color_t=0xf1c40f
                        else:
                            embed_color_t = 0x2ecc71

                        if t_stamina <= 0:
                            fortitude = 0.0
                            low = t_health - (t_health*.90)
                            high = t_health- (t_health*.80)
                            fortitude = random.randint(int(low), int(high))

                            t_stamina = t_focus
                            t_healthcalc = round(((t_focus * .40) + (fortitude * 1))/2)
                            t_attackcalc = round(.20 * ((t_focus * .15) + round(fortitude * 1)))
                            t_defensecalc = round(.20 * ((t_focus * .10) + round(fortitude * 1)))
                            t_newhealth = 0
                            healmessage = ""
                            messagenumber = 0

                            if t_health <= t_max_health:
                                t_newhealth = t_health + t_healthcalc
                                if t_newhealth > t_max_health:
                                    healmessage = f"recovered!"
                                    messagenumber = 1
                                    t_health = t_max_health
                                else:
                                    healmessage = f"stopped the bleeding..."
                                    messagenumber = 2
                                    t_health = t_newhealth
                            else:
                                healmessage = f"hasn't been touched..."
                                messagenumber = 0

                            t_attack = t_attack + t_attackcalc
                            t_defense =  t_defense + t_defensecalc
                            t_used_focus=True
                            embedVar = discord.Embed(title=f"{t_card} focused and {healmessage}", description="All stats increased", colour=embed_color_t)
                            await ctx.send(embed=embedVar)

                            if messagenumber != 2:
                                if messagenumber == 1:
                                    embedVar = discord.Embed(title=f"{t_card} Stamina has recovered", colour=embed_color_t)
                                    await ctx.send(embed=embedVar)
                                else:
                                    embedVar = discord.Embed(title=f"{t_card} Stamina has recovered", colour=embed_color_t)
                                    await ctx.send(embed=embedVar)
                            else:
                                embedVar = discord.Embed(title=f"{t_card} Stamina has recovered", colour=embed_color_t)
                                await ctx.send(embed=embedVar)
                            turn_total= turn_total + 1
                            turn=0
                        else:

                            # UNIVERSE CARD
                            player_2_card = showcard(t, t_max_health, t_health, t_max_stamina, t_stamina, t_used_resolve, ttitle, t_used_focus)
                            await ctx.send(file=player_2_card)

                            embedVar = discord.Embed(title=f"{t_card} What move will you use?", description=f"{o_card} currently has {o_health} health and {o_stamina} stamina.", colour=embed_color_t)
                            if t_used_focus and not t_used_resolve:
                                embedVar.set_author(name="Press 5 to strengthen resolve!")
                            embedVar.set_footer(text="Use 1 for Basic Attack, 2 for Special Attack, 3 for Ultimate Move, and 4 for Enhancer")
                            await ctx.send(embed=embedVar)
                            aiMove = 0
                            
                            if o_stamina == 0:
                                aiMove = 1
                            elif t_stamina >= 90 and (t_health >= o_health):
                                aiMove = 3
                            elif t_stamina >= 90:
                                aiMove = 4
                            elif t_stamina >= 80 and (t_health >= o_health):
                                aiMove = 4
                            elif t_stamina >= 80:
                                aiMove = 2
                            elif t_stamina >= 70 and (t_health >= o_health):
                                aiMove = 4
                            elif t_stamina >= 70:
                                aiMove = 1
                            elif t_stamina >= 60 and (t_health >= o_health):
                                aiMove = 1
                            elif t_stamina >= 60:
                                if t_used_resolve == False:
                                    aiMove = 5
                                else:
                                    aiMove = 2
                            elif t_stamina >= 50 and (t_health >= o_health):
                                if t_stamina >= o_stamina:
                                    aiMove = 4
                                else:
                                    aiMove = 1
                            elif t_stamina >= 50:
                                aiMove = 2
                            elif t_stamina >= 40 and (t_health >= o_health):
                                aiMove = 1
                            elif t_stamina >= 40:
                                aiMove = 2
                            elif t_stamina >= 30 and (t_health >= o_health):
                                aiMove = 4
                            elif t_stamina >= 30:
                                aiMove = 2
                            elif t_stamina >= 20 and (t_health >= o_health):
                                aiMove = 1
                            elif t_stamina >= 20:
                                aiMove = 4
                            elif t_stamina >= 10:
                                aiMove = 1
                            else:
                                aiMove = 1

                            if int(aiMove) == 0:
                                t_health=0
                            if int(aiMove) == 1:
                                dmg = damage_cal(t_card, t_1, t_attack, t_defense, o_defense, t_vul, t_accuracy, t_stamina, t_enhancer_used, t_health, o_health, o_stamina)
                            elif int(aiMove) == 2:
                                dmg = damage_cal(t_card, t_2, t_attack, t_defense, o_defense, t_vul, t_accuracy, t_stamina, t_enhancer_used, t_health, o_health, o_stamina)
                            elif int(aiMove) == 3:
                                dmg = damage_cal(t_card, t_3, t_attack, t_defense, o_defense, t_vul, t_accuracy, t_stamina, t_enhancer_used, t_health, o_health, o_stamina)
                            elif int(aiMove) == 4:
                                t_enhancer_used=True
                                dmg = damage_cal(t_card, t_enhancer, t_attack, t_defense, o_defense, t_vul, t_accuracy, t_stamina, t_enhancer_used, t_health,o_health, o_stamina)
                                t_enhancer_used=False
                            elif int(aiMove) == 5:
                                if not t_used_resolve and t_used_focus:
                                    #fortitude or luck is based on health  
                                    fortitude = 0.0
                                    low = t_health - (t_health * .75)
                                    high = t_health- (t_health * .66)
                                    fortitude = random.randint(int(low), int(high))
                                    #Resolve Scaling
                                    t_resolve_health = round(fortitude + (.5*t_resolve))
                                    t_resolve_attack = round(4 * (t_resolve / (.25 * t_attack)))
                                    t_resolve_defense = round(3 * (t_resolve / (.25 * t_defense)))

                                    t_stamina = t_stamina + t_resolve
                                    t_health = t_health + t_resolve_health
                                    t_attack = round(t_attack + t_resolve_attack)
                                    t_defense = round(t_defense - t_resolve_defense)
                                    t_used_resolve=True
                                    embedVar = discord.Embed(title=f"{t_card} strengthened resolve!", colour=embed_color_t)
                                    await ctx.send(embed=embedVar)
                                    turn_total= turn_total + 1
                                    turn=0
                                else:
                                    await ctx.send(m.CANNOT_USE_RESOLVE)
                                    turn=1

                            if int(msg.content) !=5:
                                # If you have enough stamina for move, use it
                                if dmg['CAN_USE_MOVE']:

                                    if dmg['ENHANCE']:
                                        enh_type= dmg['ENHANCED_TYPE']
                                        if enh_type == 'ATK':
                                            t_attack = round(t_attack + dmg['DMG'])
                                        elif enh_type == 'DEF':
                                            t_defense = round(t_defense + dmg['DMG'])
                                        elif enh_type == 'STAM':
                                            t_stamina = round(t_stamina + dmg['DMG'])
                                        elif enh_type == 'HLT':
                                            t_health = round(t_health + dmg['DMG'])
                                        elif enh_type == 'LIFE':
                                            t_health = round(t_health + dmg['DMG'])
                                            o_health = round(o_health - dmg['DMG'])
                                        elif enh_type == 'DRAIN':
                                            t_stamina = round(t_stamina + dmg['DMG'])
                                            o_stamina = round(o_stamina - dmg['DMG'])
                                        t_stamina = t_stamina - int(dmg['STAMINA_USED'])
                                        embedVar = discord.Embed(title=f"{dmg['MESSAGE']}", colour=embed_color_t)
                                        await ctx.send(embed=embedVar)
                                        turn_total= turn_total + 1
                                        turn = 0
                                    elif dmg['DMG'] == 0:
                                        t_stamina = t_stamina - int(dmg['STAMINA_USED'])
                                        embedVar = discord.Embed(title=f"{dmg['MESSAGE']}", colour=embed_color_t)
                                        await ctx.send(embed=embedVar)
                                        turn_total= turn_total + 1
                                        turn=0
                                    else:
                                        o_health = o_health - int(dmg['DMG'])
                                        if o_health < 0:
                                            o_health=0
                                        t_stamina = t_stamina - int(dmg['STAMINA_USED'])

                                        embedVar = discord.Embed(title=f"{dmg['MESSAGE']}", colour=embed_color_t)
                                        await ctx.send(embed=embedVar)
                                        turn_total= turn_total + 1
                                        turn=0

                                else:
                                    await ctx.send(m.NOT_ENOUGH_STAMINA)
                                    turn = 1
                            
                            # except:
                            #     await ctx.send('Did not work')
                # End the match
                if o_health <= 0:
                    # await ctx.send(f":zap: {user2.mention} you win the match!")
                    uid = t_DID
                    tuser = await self.bot.fetch_user(uid)

                    ouid = sowner['DID']
                    sownerctx = await self.bot.fetch_user(ouid)
                    response = await score(sownerctx, tuser)

                    embedVar = discord.Embed(title=f":zap: `{t_card}` scores {response} and wins the match!", description=f"Match concluded in {turn_total} turns!", colour=0x1abc9c)
                    embedVar.set_author(name=f"{o_card} lost! ", icon_url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620236432/PCG%20LOGOS%20AND%20RESOURCES/PCGBot_1.png")
                    embedVar.set_footer(text=f"Play again? {now}")
                    await ctx.send(embed=embedVar)

                elif t_health <=0:
                    uid = o_DID
                    ouser = await self.bot.fetch_user(uid)

                    ouid = sowner['DID']
                    sownerctx = await self.bot.fetch_user(ouid)
                    response = await score(sownerctx, ouser)

                    embedVar = discord.Embed(title=f":zap: `{o_card}` {response} and wins the match!", description=f"Match concluded in {turn_total} turns!", colour=0xe91e63)
                    embedVar.set_author(name=f"{t_card} lost! ", icon_url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620236432/PCG%20LOGOS%20AND%20RESOURCES/PCGBot_1.png")
                    embedVar.set_footer(text=f"Play again? {now}")
                    await ctx.send(embed=embedVar)
        else:
            await ctx.send(m.SESSION_DOES_NOT_EXIST)

    @commands.command()
    async def start(self, ctx):
        starttime = time.asctime()
        h_gametime = starttime[11:13]
        m_gametime = starttime[14:16]
        s_gametime = starttime[17:19]
        session_query = {"OWNER": str(ctx.author), "AVAILABLE": True}
        session = db.querySession(session_query)
        if session:
            if session['GAME'] == 'Crown Unlimited':
                # Get Session Owner Disname for scoring
                sowner = db.queryUser({'DISNAME': str(session['OWNER'])})

                teams = [x for x in session['TEAMS']]
                team_1 = [x for x in teams if x['POSITION'] == 0][0] # position 0
                team_2 = [x for x in teams if x['POSITION'] == 1][0] # position 1
                o = db.queryCard({'NAME': team_1['CARD']})
                otitle = db.queryTitle({'TITLE': team_1['TITLE']})
                
                t = db.queryCard({'NAME': team_2['CARD']})
                ttitle = db.queryTitle({'TITLE': team_2['TITLE']})

                ####################################################################
                #PLayer Data



                # Player 1 Data
                o_user = db.queryUser({'DISNAME': team_1['TEAM'][0]})
                oarm = db.queryArm({'ARM': o_user['ARM']})
                oarm_passive = oarm['ABILITIES'][0]
                oarm_name=oarm['ARM']
                o_DID = o_user['DID']
                o_card = o['NAME']
                o_card_path=o['PATH']
                o_rcard_path=o['RPATH']
                o_max_health = o['HLT']
                o_health = o['HLT']
                o_stamina = o['STAM']
                o_max_stamina = o['STAM']
                o_moveset = o['MOVESET']
                o_attack = o['ATK']
                o_defense = o['DEF']
                o_type = o['TYPE']
                o_accuracy = o['ACC']
                o_passive = o['PASS'][0]
                o_speed = o['SPD']
                o_universe = o['UNIVERSE']
                o_title_universe = otitle['UNIVERSE']
                o_title_passive = otitle['ABILITIES'][0]
                o_vul = False
                user1 = await self.bot.fetch_user(o_DID)
                o_title_passive_bool = False

                # Player 2 Data
                t_user = db.queryUser({'DISNAME': team_2['TEAM'][0]})
                tarm = db.queryArm({'ARM': t_user['ARM']})
                tarm_passive = tarm['ABILITIES'][0]
                tarm_name=tarm['ARM']
                t_DID = t_user['DID']
                t_card = t['NAME']
                t_card_path=t['PATH']
                t_rcard_path=t['RPATH']
                t_max_health = t['HLT']
                t_health = t['HLT']
                t_stamina = t['STAM']
                t_max_stamina= t['STAM']
                t_moveset = t['MOVESET']
                t_attack = t['ATK']
                t_defense = t['DEF']
                t_type = t['TYPE']
                t_accuracy = t['ACC']
                t_passive = t['PASS'][0]
                t_speed = t['SPD']
                t_universe = t['UNIVERSE']
                t_title_universe = ttitle['UNIVERSE']
                t_title_passive = ttitle['ABILITIES'][0]
                t_vul = False
                user2 = await self.bot.fetch_user(t_DID)
                t_title_passive_bool = False
                
                ################################################################################

                # Player 1 Passive Config
                if (o_universe == o_title_universe) or (o_title_universe == "Unbound"):
                    o_title_passive_bool = True
                
                # Player 1 Focus & Resolve
                o_focus = 60
                o_used_focus=False
                o_resolve = 50
                o_used_resolve=False

                # Player 1 Moves
                o_1 = o_moveset[0]
                o_2 = o_moveset[1]
                o_3 = o_moveset[2]
                o_enhancer = o_moveset[3]
                o_enhancer_used=False

                # Player 1 Card Passive
                o_card_passive_type = list(o_passive.values())[1]
                o_card_passive = list(o_passive.values())[0]

                if o_card_passive_type == 'ATK':
                    o_attack = o_attack + int(o_card_passive)
                elif o_card_passive_type == 'DEF':
                    o_defense = o_defense + int(o_card_passive)
                elif o_card_passive_type == 'STAM':
                    o_stamina = o_stamina + int(o_card_passive)
                elif o_card_passive_type == 'HLT':
                    o_health = o_health + int(o_card_passive)
                elif o_card_passive_type == 'LIFE':
                    o_health = o_health + round(int(o_card_passive) + (.10 * t_health))
                elif o_card_passive_type == 'DRAIN':
                    o_stamina = o_stamina + int(o_card_passive)

                # Title Passive
                o_title_passive_type = list(o_title_passive.keys())[0]
                o_title_passive_value = list(o_title_passive.values())[0]

                if o_title_passive_bool:
                    if o_title_passive_type == 'ATK':
                        o_attack = o_attack + int(o_title_passive_value)
                    elif o_title_passive_type == 'DEF':
                        o_defense = o_defense + int(o_title_passive_value)
                    elif o_title_passive_type == 'STAM':
                        o_stamina = o_stamina + int(o_title_passive_value)
                    elif o_title_passive_type == 'HLT':
                        o_health = o_health + int(o_title_passive_value)

                # Arm Passive Player 1
                oarm_passive_type = list(oarm_passive.keys())[0]
                oarm_passive_value = list(oarm_passive.values())[0]

                if oarm_passive_type == 'ATK':
                    o_attack = o_attack + int(oarm_passive_value)
                elif oarm_passive_type == 'DEF':
                    o_defense = o_defense + int(oarm_passive_value)
                elif oarm_passive_type == 'STAM':
                    o_stamina = o_stamina + int(oarm_passive_value)
                elif oarm_passive_type == 'HLT':
                    o_health = o_health + int(oarm_passive_value)

                # Arm Passive Player 2
                tarm_passive_type = list(tarm_passive.keys())[0]
                tarm_passive_value = list(tarm_passive.values())[0]

                if tarm_passive_type == 'ATK':
                    t_attack = t_attack + int(tarm_passive_value)
                elif tarm_passive_type == 'DEF':
                    t_defense = t_defense + int(tarm_passive_value)
                elif tarm_passive_type == 'STAM':
                    t_stamina = t_stamina + int(tarm_passive_value)
                elif tarm_passive_type == 'HLT':
                    t_health = t_health + int(tarm_passive_value)

                


                # Player 2 Passive Config
                if (t_universe == t_title_universe) or (t_title_universe == "Unbound"):
                    t_title_passive_bool = True
                
                # Player 1 Card Passive
                t_card_passive_type = list(t_passive.values())[1]
                t_card_passive = list(t_passive.values())[0]

                if t_card_passive_type == 'ATK':
                    t_attack = t_attack + int(t_card_passive)
                elif t_card_passive_type == 'DEF':
                    t_defense = t_defense + int(t_card_passive)
                elif t_card_passive_type == 'STAM':
                    t_stamina = t_stamina + int(t_card_passive)
                elif t_card_passive_type == 'HLT':
                    t_health = t_health + int(t_card_passive)
                elif t_card_passive_type == 'LIFE':
                    t_health = t_health + round(int(t_card_passive) + (.10 * o_health))
                elif t_card_passive_type == 'DRAIN':
                    t_stamina = t_stamina + int(t_card_passive)

                # Title Passive
                t_title_passive_type = list(t_title_passive.keys())[0]
                t_title_passive_value = list(t_title_passive.values())[0]

                if t_title_passive_bool:
                    if t_title_passive_type == 'ATK':
                        t_attack = t_attack + int(t_title_passive_value)
                    elif t_title_passive_type == 'DEF':
                        t_defense = t_defense + int(t_title_passive_value)
                    elif t_title_passive_type == 'STAM':
                        t_stamina = t_stamina + int(t_title_passive_value)
                    elif t_title_passive_type == 'HLT':
                        t_health = t_health + int(t_title_passive_value)


                # Player 2 Moves
                t_1 = t_moveset[0]
                t_2 = t_moveset[1]
                t_3 = t_moveset[2]
                t_enhancer = t_moveset[3]
                t_enhancer_used=False

                # Player 1 Focus & Resolve
                t_focus = 60
                t_used_focus=False
                t_resolve = 50
                t_used_resolve=False
                
                # Turn iterator
                turn = 0
                # Enhance Turn Iterators
                eo=0
                et=0

                botActive = False
                tutorialbot = '837538366509154407'
                legendbot = '845672426113466395'
                userID = t_user['DID']
                if tutorialbot == userID:
                    botActive = True
                    await ctx.send(f"Welcome to Bootcamp!")
                    turn = 0
                elif legendbot == userID:
                    botActive = True
                    await ctx.send(f"Welcome to Legends!")
                    turn = 0
                else:
                    botActive = False
                    start = starting_position(o_speed, t_speed)
                    if start == True:
                        turn = 0
                    else:
                        turn = 1
                    

                # Vulnerability Check
                if o_type == 0 and t_type == 2:
                    o_vul=True
                if t_type == 0 and o_type == 2:
                    t_vul=True
                
                options = [1,2,3,4,5,0]
                await ctx.send(f"{user1.mention}: `{o_card}` VS {user2.mention}: `{t_card}` has begun!")

                # Count Turns
                turn_total = 0

                
                # START TURNS
                while (o_health > 0) and (t_health > 0):
                    #Player 1 Turn Start
                    if turn == 0:

                        # Tutorial Instructions
                        if turn_total == 0 and botActive:                    
                            embedVar = discord.Embed(title=f"Welcome to `Crown Unlimited`!", description=f"Follow the instructions to learn how to play Crown Unlimited", colour=0xe91e63)
                            embedVar.add_field(name="How do you play this game?", value="The point of the game is to win the game, duh!\nTo do this, you need to select moves in a strategic order to give you the advantage to secure the win!")
                            embedVar.set_footer(text="Select a move to get started. Moves will drain your `Stamina` quickly.\n`When your Stamina depletes to 0 your character will Focus`")
                            await ctx.send(embed=embedVar)

                        

                        if o_health <= (o_max_health * .25):
                            embed_color_o=0xe74c3c
                            
                        elif o_health <= (o_max_health * .50):
                            embed_color_o=0xe67e22
                        elif o_health <= (o_max_health * .75):
                            embed_color_o=0xf1c40f
                            
                        else:
                            embed_color_o = 0x2ecc71

                        if o_stamina <= 0:
                            if botActive and not o_used_focus:                    
                                embedVar = discord.Embed(title=f"You've entered `Focus State`!", description=f"Entering `Focus State` sacrifices a turn to power up and regain `Stamina`!", colour=0xe91e63)
                                embedVar.add_field(name="Strategy", value="Pay attention to your oppononets `STAM` bar. If they are close to entering `Focus State`, you will have the ability to strike twice if you play your cards right!")
                                embedVar.set_footer(text="After you entered focus state once, a transformation is possible by strengthening your `Resolve`!")
                                await ctx.send(embed=embedVar)
                            #fortitude or luck is based on health  
                            fortitude = 0.0
                            low = o_health - (o_health*.90)
                            high = o_health- (o_health*.80)
                            fortitude = random.randint(int(low), int(high))

                            o_stamina = o_focus
                            o_healthcalc = round(((o_focus * .40) + (fortitude * 1))/2)
                            o_attackcalc = round(.20 * ((o_focus * .15) + round(fortitude * 1)))
                            o_defensecalc = round(.20 * ((o_focus * .15) + round(fortitude * 1)))
                            #check if user is at max health and sets messages and focus health value
                            o_newhealth = 0
                            healmessage = ""
                            messagenumber = 0
                            if o_health <= o_max_health:
                                o_newhealth = o_health + o_healthcalc
                                if o_newhealth > o_max_health:
                                    healmessage = "the injuries dissapeared"
                                    messagenumber = 1
                                    o_health = o_max_health
                                else:
                                    healmessage = "regained some vitality"
                                    messagenumber = 2
                                    o_health = o_newhealth
                            else:
                                healmessage = f"`{t_card}`'s blows don't appear to have any effect!"
                                messagenumber = 0
                            o_attack = o_attack + o_attackcalc
                            o_defense =  o_defense + o_defensecalc
                            o_used_focus = True

                            embedVar = discord.Embed(title=f"{o_card} focused and {healmessage}", description="All stats increased", colour=embed_color_o)
                            await ctx.send(embed=embedVar)

                            if messagenumber != 2:
                                if messagenumber == 1:
                                    embedVar = discord.Embed(title=f"{o_card} Stamina has recovered!", colour=embed_color_o)
                                    await ctx.send(embed=embedVar)
                                else:
                                    embedVar = discord.Embed(title=f"{o_card} Stamina has recovered!", colour=embed_color_o)
                                    await ctx.send(embed=embedVar)
                            else:
                                embedVar = discord.Embed(title=f"{o_card} Stamina has recovered!", colour=embed_color_o)
                                await ctx.send(embed=embedVar)
                            turn_total= turn_total + 1
                            turn = 1
                        else:

                            # UNIVERSE CARD
                            player_1_card = showcard(o, o_max_health, o_health, o_max_stamina, o_stamina, o_used_resolve, otitle, o_used_focus)
                            await ctx.send(file=player_1_card)
                            embedVar = discord.Embed(title=f"{o_card} What move will you use?", description=f"{t_card} currently has {t_health} health and {t_stamina} stamina.", colour=embed_color_o)
                            if o_used_focus and not o_used_resolve:
                                embedVar.set_author(name="Press 5 to strengthen resolve!")
                            embedVar.set_footer(text="Use 1 for Basic Attack, 2 for Special Attack, 3 for Ultimate Move, and 4 for Enhancer. Use 0 to Quit")
                            await ctx.send(embed=embedVar)
                            
                            # Make sure user is responding with move
                            def check(msg):
                                return msg.author == user1 and msg.channel == ctx.channel and int(msg.content) in options
                            try:
                                msg = await self.bot.wait_for("message",timeout=240.0, check=check)

                                # calculate data based on selected move
                                if int(msg.content) == 0:
                                    o_health = 0
                                if int(msg.content) == 1:
                                    dmg = damage_cal(o_card, o_1, o_attack, o_defense, t_defense, o_vul, o_accuracy, o_stamina, o_enhancer_used, o_health, t_health, t_stamina)
                                elif int(msg.content) == 2:
                                    dmg = damage_cal(o_card, o_2, o_attack, o_defense, t_defense, o_vul, o_accuracy, o_stamina, o_enhancer_used, o_health, t_health, t_stamina)
                                elif int(msg.content) == 3:
                                    dmg = damage_cal(o_card, o_3, o_attack, o_defense, t_defense, o_vul, o_accuracy, o_stamina, o_enhancer_used, o_health, t_health, t_stamina)
                                elif int(msg.content) == 4:
                                    o_enhancer_used=True
                                    dmg = damage_cal(o_card, o_enhancer, o_attack, o_defense, t_defense, o_vul, o_accuracy, o_stamina, o_enhancer_used, o_health, t_health, t_stamina)
                                    o_enhancer_used=False
                                elif int(msg.content) == 5:

                                    #Resolve Check and Calculation
                                    if not o_used_resolve and o_used_focus:

                                        if botActive:                    
                                            embedVar = discord.Embed(title=f"You are Resolved", description=f"Entering `Resolved State` sacrifices a turn to power up even greater and regain `Stamina`!", colour=0xe91e63)
                                            embedVar.add_field(name="Strategy", value="You sacrifice `Defense` to greatly increase `Attack` in your `Resolved` state. Use it when you need to secure an advantage.")
                                            embedVar.set_footer(text="A poorly planned `Resolve` could cost you the match.")
                                            await ctx.send(embed=embedVar)
                                            

                                        #fortitude or luck is based on health  
                                        fortitude = 0.0
                                        low = o_health - (o_health * .75)
                                        high = o_health- (o_health * .66)
                                        fortitude = random.randint(int(low), int(high))
                                        #Resolve Scaling
                                        o_resolve_health = round(fortitude + (.5*o_resolve))
                                        o_resolve_attack = round(4 * (o_resolve / (.50 * o_attack)))
                                        o_resolve_defense = round(3 * (o_resolve / (.25 * o_defense)))

                                        o_stamina = o_stamina + o_resolve
                                        o_health = o_health + o_resolve_health
                                        o_attack = round(o_attack + o_resolve_attack)
                                        o_defense = round(o_defense - o_resolve_defense)
                                        o_used_resolve = True 

                                        embedVar = discord.Embed(title=f"{o_card} strengthened resolve!", colour=embed_color_o)
                                        await ctx.send(embed=embedVar)
                                        turn_total= turn_total + 1
                                        turn=1
                                    else:
                                        emessage = m.CANNOT_USE_RESOLVE
                                        embedVar = discord.Embed(title=emessage, description=f"Entering `Resolved State` sacrifices a turn to power up even greater and regain `Stamina`!", colour=0xe91e63)
                                        await ctx.send(embed=embedVar)
                                        turn=0

                                if int(msg.content) !=5:
                                    # If you have enough stamina for move, use it
                                    if dmg['CAN_USE_MOVE']:
                                        if dmg['ENHANCE']:
                                            enh_type= dmg['ENHANCED_TYPE']
                                        
                                            if enh_type == 'ATK':
                                                o_attack = round(o_attack + dmg['DMG'])
                                            elif enh_type == 'DEF':
                                                o_defense = round(o_defense + dmg['DMG'])
                                            elif enh_type == 'STAM':
                                                o_stamina = round(o_stamina + dmg['DMG'])
                                            elif enh_type == 'HLT':
                                                o_health = round(o_health + dmg['DMG'])
                                            elif enh_type == 'LIFE':
                                                o_health = round(o_health + dmg['DMG'])
                                                t_health = round(t_health - dmg['DMG'])
                                            elif enh_type == 'DRAIN':
                                                o_stamina = round(o_stamina + dmg['DMG'])
                                                t_stamina = round(t_stamina - dmg['DMG'])
                                            o_stamina = o_stamina - int(dmg['STAMINA_USED'])

                                            embedVar = discord.Embed(title=f"{dmg['MESSAGE']}", colour=embed_color_o)
                                            await ctx.send(embed=embedVar)
                                            turn_total= turn_total + 1
                                            turn=1
                                        elif dmg['DMG'] == 0:
                                            o_stamina = o_stamina - int(dmg['STAMINA_USED'])

                                            embedVar = discord.Embed(title=f"{dmg['MESSAGE']}", colour=embed_color_o)
                                            await ctx.send(embed=embedVar)
                                            turn_total= turn_total + 1
                                            turn=1
                                        else:
                                            t_health = t_health - dmg['DMG']
                                            if t_health < 0:
                                                t_health=0
                                            o_stamina = o_stamina - dmg['STAMINA_USED']

                                            embedVar = discord.Embed(title=f"{dmg['MESSAGE']}", colour=embed_color_o)
                                            await ctx.send(embed=embedVar)
                                            turn_total= turn_total + 1
                                            turn=1
                                    else:
                                        emessage = m.NOT_ENOUGH_STAMINA
                                        embedVar = discord.Embed(title=emessage, description=f"Use abilities to Increase `STAM` or enter `FOCUS STATE`!", colour=0xe91e63)
                                        await ctx.send(embed=embedVar)
                                        turn=0
                            except:
                                emessage = m.DID_NOT_WORK
                                embedVar = discord.Embed(title=emessage, description=f"Try Again", colour=0xe91e63)
                                await ctx.send(embed=embedVar)
                    #PLayer 2 Turn Start
                    elif turn == 1:
                        
                        if t_health <= (t_max_health * .25):
                            embed_color_t=0xe74c3c
                            
                        elif t_health <= (t_max_health * .50):
                            embed_color_t=0xe67e22
                        elif t_health <= (t_max_health * .75):
                            embed_color_t=0xf1c40f
                        else:
                            embed_color_t = 0x2ecc71

                        #Focus
                        if t_stamina <= 0:
                            fortitude = 0.0
                            low = t_health - (t_health*.90)
                            high = t_health- (t_health*.80)
                            fortitude = random.randint(int(low), int(high))

                            t_stamina = t_focus
                            t_healthcalc = round(((t_focus * .40) + (fortitude * 1))/2)
                            t_attackcalc = round(.20 * ((t_focus * .15) + round(fortitude * 1)))
                            t_defensecalc = round(.20 * ((t_focus * .10) + round(fortitude * 1)))
                            t_newhealth = 0
                            healmessage = ""
                            messagenumber = 0

                            if t_health <= t_max_health:
                                t_newhealth = t_health + t_healthcalc
                                if t_newhealth > t_max_health:
                                    healmessage = f"recovered!"
                                    messagenumber = 1
                                    t_health = t_max_health
                                else:
                                    healmessage = f"stopped the bleeding..."
                                    messagenumber = 2
                                    t_health = t_newhealth
                            else:
                                healmessage = f"hasn't been touched..."
                                messagenumber = 0

                            t_attack = t_attack + t_attackcalc
                            t_defense =  t_defense + t_defensecalc
                            t_used_focus=True
                            embedVar = discord.Embed(title=f"{t_card} focused and {healmessage}", description="All stats increased", colour=embed_color_t)
                            await ctx.send(embed=embedVar)

                            if messagenumber != 2:
                                if messagenumber == 1:
                                    embedVar = discord.Embed(title=f"{t_card} Stamina has recovered", colour=embed_color_t)
                                    await ctx.send(embed=embedVar)
                                else:
                                    embedVar = discord.Embed(title=f"{t_card} Stamina has recovered", colour=embed_color_t)
                                    await ctx.send(embed=embedVar)
                            else:
                                embedVar = discord.Embed(title=f"{t_card} Stamina has recovered", colour=embed_color_t)
                                await ctx.send(embed=embedVar)
                            turn_total= turn_total + 1
                            turn=0
                        else:
                            #Check If Playing Bot
                            if botActive != True:
                                #PlayUser
                                # UNIVERSE CARD
                                player_2_card = showcard(t, t_max_health, t_health, t_max_stamina, t_stamina, t_used_resolve, ttitle, t_used_focus)
                                await ctx.send(file=player_2_card)

                                embedVar = discord.Embed(title=f"{t_card} What move will you use?", description=f"{o_card} currently has {o_health} health and {o_stamina} stamina.", colour=embed_color_t)
                                if t_used_focus and not t_used_resolve:
                                    embedVar.set_author(name="Press 5 to strengthen resolve!")
                                embedVar.set_footer(text="Use 1 for Basic Attack, 2 for Special Attack, 3 for Ultimate Move, and 4 for Enhancer. Use 0 to Quit")
                                await ctx.send(embed=embedVar)
                                # Make sure user is responding with move
                                def check(msg):
                                    return msg.author == user2 and msg.channel == ctx.channel and int(msg.content) in options
                                try:
                                    msg = await self.bot.wait_for("message",timeout=240.0, check=check)

                                    # calculate data based on selected move
                                    if int(msg.content) == 0:
                                        t_health = 0
                                    if int(msg.content) == 1:
                                        dmg = damage_cal(t_card, t_1, t_attack, t_defense, o_defense, t_vul, t_accuracy, t_stamina, t_enhancer_used, t_health, o_health, o_stamina)
                                    elif int(msg.content) == 2:
                                        dmg = damage_cal(t_card, t_2, t_attack, t_defense, o_defense, t_vul, t_accuracy, t_stamina, t_enhancer_used, t_health, o_health, o_stamina)
                                    elif int(msg.content) == 3:
                                        dmg = damage_cal(t_card, t_3, t_attack, t_defense, o_defense, t_vul, t_accuracy, t_stamina, t_enhancer_used, t_health, o_health, o_stamina)
                                    elif int(msg.content) == 4:
                                        t_enhancer_used=True
                                        dmg = damage_cal(t_card, t_enhancer, t_attack, t_defense, o_defense, t_vul, t_accuracy, t_stamina, t_enhancer_used, t_health,o_health, o_stamina)
                                        t_enhancer_used=False
                                    elif int(msg.content) == 5:
                                        if not t_used_resolve and t_used_focus:
                                            #fortitude or luck is based on health  
                                            fortitude = 0.0
                                            low = t_health - (t_health * .75)
                                            high = t_health- (t_health * .66)
                                            fortitude = random.randint(int(low), int(high))
                                            #Resolve Scaling
                                            t_resolve_health = round(fortitude + (.5*t_resolve))
                                            t_resolve_attack = round(4 * (t_resolve / (.25 * t_attack)))
                                            t_resolve_defense = round(3 * (t_resolve / (.25 * t_defense)))

                                            t_stamina = t_stamina + t_resolve
                                            t_health = t_health + t_resolve_health
                                            t_attack = round(t_attack + t_resolve_attack)
                                            t_defense = round(t_defense - t_resolve_defense)
                                            t_used_resolve=True
                                            embedVar = discord.Embed(title=f"{t_card} strengthened resolve!", colour=embed_color_t)
                                            await ctx.send(embed=embedVar)
                                            turn_total= turn_total + 1
                                            turn=0
                                        else:
                                            emessage = m.CANNOT_USE_RESOLVE
                                            embedVar = discord.Embed(title=emessage, description=f"Entering `Resolved State` sacrifices a turn to power up even greater and regain `Stamina`!", colour=0xe91e63)
                                            await ctx.send(embed=embedVar)
                                            await ctx.send(m.CANNOT_USE_RESOLVE)
                                            turn=1

                                    if int(msg.content) !=5:
                                        # If you have enough stamina for move, use it
                                        if dmg['CAN_USE_MOVE']:

                                            if dmg['ENHANCE']:
                                                enh_type= dmg['ENHANCED_TYPE']
                                                if enh_type == 'ATK':
                                                    t_attack = round(t_attack + dmg['DMG'])
                                                elif enh_type == 'DEF':
                                                    t_defense = round(t_defense + dmg['DMG'])
                                                elif enh_type == 'STAM':
                                                    t_stamina = round(t_stamina + dmg['DMG'])
                                                elif enh_type == 'HLT':
                                                    t_health = round(t_health + dmg['DMG'])
                                                elif enh_type == 'LIFE':
                                                    t_health = round(t_health + dmg['DMG'])
                                                    o_health = round(o_health - dmg['DMG'])
                                                elif enh_type == 'DRAIN':
                                                    t_stamina = round(t_stamina + dmg['DMG'])
                                                    o_stamina = round(o_stamina - dmg['DMG'])
                                                t_stamina = t_stamina - int(dmg['STAMINA_USED'])
                                                embedVar = discord.Embed(title=f"{dmg['MESSAGE']}", colour=embed_color_t)
                                                await ctx.send(embed=embedVar)
                                                turn_total= turn_total + 1
                                                turn = 0
                                            elif dmg['DMG'] == 0:
                                                t_stamina = t_stamina - int(dmg['STAMINA_USED'])
                                                embedVar = discord.Embed(title=f"{dmg['MESSAGE']}", colour=embed_color_t)
                                                await ctx.send(embed=embedVar)
                                                turn_total= turn_total + 1
                                                turn=0
                                            else:
                                                o_health = o_health - int(dmg['DMG'])
                                                if o_health < 0:
                                                    o_health=0
                                                t_stamina = t_stamina - int(dmg['STAMINA_USED'])

                                                embedVar = discord.Embed(title=f"{dmg['MESSAGE']}", colour=embed_color_t)
                                                await ctx.send(embed=embedVar)
                                                turn_total= turn_total + 1
                                                turn=0

                                        else:
                                            emessage = m.NOT_ENOUGH_STAMINA
                                            embedVar = discord.Embed(title=emessage, description=f"Use abilities to Increase `STAM` or enter `FOCUS STATE`!", colour=0xe91e63)
                                            await ctx.send(embed=embedVar)
                                            turn = 1
                                except:
                                    emessage = m.DID_NOT_WORK
                                    embedVar = discord.Embed(title=emessage, description=f"Try Again", colour=0xe91e63)
                                    await ctx.send(embed=embedVar)
                                    await ctx.send('Did not work')
                            #Play Bot
                            else:
                                # UNIVERSE CARD
                                player_2_card = showcard(t, t_max_health, t_health, t_max_stamina, t_stamina, t_used_resolve, ttitle, t_used_focus)
                                await ctx.send(file=player_2_card)

                                embedVar = discord.Embed(title=f"{t_card} What move will you use?", description=f"{o_card} currently has {o_health} health and {o_stamina} stamina.", colour=embed_color_t)
                                if t_used_focus and not t_used_resolve:
                                    embedVar.set_author(name="Press 5 to strengthen resolve!")
                                embedVar.set_footer(text="Use 1 for Basic Attack, 2 for Special Attack, 3 for Ultimate Move, and 4 for Enhancer")
                                await ctx.send(embed=embedVar)
                                aiMove = 0
                                

                                if o_stamina == 0:
                                    aiMove = 1
                                elif t_stamina >= 160 and (t_health >= o_health):
                                    aiMove = 3
                                elif t_stamina >= 160:
                                    aiMove = 3                                   
                                elif t_stamina >= 150 and (t_health >= o_health):
                                    aiMove = 1
                                elif t_stamina >= 150:
                                    aiMove = 1                                     
                                elif t_stamina >= 140 and (t_health >= o_health):
                                    aiMove = 1
                                elif t_stamina >= 140:
                                    aiMove = 3                                      
                                elif t_stamina >= 130 and (t_health >= o_health):
                                    aiMove = 1
                                elif t_stamina >= 130:
                                    aiMove = 3                                     
                                elif t_stamina >= 120 and (t_health >= o_health):
                                    aiMove = 2
                                elif t_stamina >= 120:
                                    aiMove = 3                                 
                                elif t_stamina >= 110 and (t_health >= o_health):
                                    aiMove = 1
                                elif t_stamina >= 110:
                                    aiMove = 2                                   
                                elif t_stamina >= 100 and (t_health >= o_health):
                                    aiMove = 4
                                elif t_stamina >= 100:
                                    aiMove = 1
                                elif t_stamina >= 90 and (t_health >= o_health):
                                    aiMove = 3
                                elif t_stamina >= 90:
                                    aiMove = 4
                                elif t_stamina >= 80 and (t_health >= o_health):
                                    aiMove = 1
                                elif t_stamina >= 80:
                                    aiMove = 3
                                elif t_stamina >= 70 and (t_health >= o_health):
                                    aiMove = 4
                                elif t_stamina >= 70:
                                    aiMove = 1
                                elif t_stamina >= 60 and (t_health >= o_health):
                                    aiMove = 1
                                elif t_stamina >= 60:
                                    if t_used_resolve == False and t_used_focus:
                                        aiMove = 5
                                    elif t_used_focus == False:
                                        aiMove = 2
                                    else:
                                        aiMove = 1 
                                elif t_stamina >= 50 and (t_health >= o_health):
                                    if t_stamina >= o_stamina:
                                        aiMove = 4
                                    else:
                                        aiMove = 1
                                elif t_stamina >= 50:
                                    aiMove = 2
                                elif t_stamina >= 40 and (t_health >= o_health):
                                    aiMove = 1
                                elif t_stamina >= 40:
                                    aiMove = 2
                                elif t_stamina >= 30 and (t_health >= o_health):
                                    aiMove = 4
                                elif t_stamina >= 30:
                                    aiMove = 2
                                elif t_stamina >= 20 and (t_health >= o_health):
                                    aiMove = 1
                                elif t_stamina >= 20:
                                    aiMove = 4
                                elif t_stamina >= 10:
                                    aiMove = 1
                                else:
                                    aiMove = 0
                                

                                if int(aiMove) == 0:
                                    t_health=0
                                if int(aiMove) == 1:
                                    dmg = damage_cal(t_card, t_1, t_attack, t_defense, o_defense, t_vul, t_accuracy, t_stamina, t_enhancer_used, t_health, o_health, o_stamina)
                                elif int(aiMove) == 2:
                                    dmg = damage_cal(t_card, t_2, t_attack, t_defense, o_defense, t_vul, t_accuracy, t_stamina, t_enhancer_used, t_health, o_health, o_stamina)
                                elif int(aiMove) == 3:
                                    dmg = damage_cal(t_card, t_3, t_attack, t_defense, o_defense, t_vul, t_accuracy, t_stamina, t_enhancer_used, t_health, o_health, o_stamina)
                                elif int(aiMove) == 4:
                                    t_enhancer_used=True
                                    dmg = damage_cal(t_card, t_enhancer, t_attack, t_defense, o_defense, t_vul, t_accuracy, t_stamina, t_enhancer_used, t_health,o_health, o_stamina)
                                    t_enhancer_used=False
                                elif int(aiMove) == 5:
                                    if not t_used_resolve and t_used_focus:
                                        #fortitude or luck is based on health  
                                        fortitude = 0.0
                                        low = t_health - (t_health * .75)
                                        high = t_health- (t_health * .66)
                                        fortitude = random.randint(int(low), int(high))
                                        #Resolve Scaling
                                        t_resolve_health = round(fortitude + (.5*t_resolve))
                                        t_resolve_attack = round(4 * (t_resolve / (.25 * t_attack)))
                                        t_resolve_defense = round(3 * (t_resolve / (.25 * t_defense)))

                                        t_stamina = t_stamina + t_resolve
                                        t_health = t_health + t_resolve_health
                                        t_attack = round(t_attack + t_resolve_attack)
                                        t_defense = round(t_defense - t_resolve_defense)
                                        t_used_resolve=True
                                        embedVar = discord.Embed(title=f"{t_card} strengthened resolve!", colour=embed_color_t)
                                        await ctx.send(embed=embedVar)
                                        turn_total= turn_total + 1
                                        turn=0
                                    else:
                                        await ctx.send(m.CANNOT_USE_RESOLVE)
                                        turn=1

                                if int(aiMove) !=5:
                                    # If you have enough stamina for move, use it
                                    if dmg['CAN_USE_MOVE']:

                                        if dmg['ENHANCE']:
                                            enh_type= dmg['ENHANCED_TYPE']
                                            if enh_type == 'ATK':
                                                t_attack = round(t_attack + dmg['DMG'])
                                            elif enh_type == 'DEF':
                                                t_defense = round(t_defense + dmg['DMG'])
                                            elif enh_type == 'STAM':
                                                t_stamina = round(t_stamina + dmg['DMG'])
                                            elif enh_type == 'HLT':
                                                t_health = round(t_health + dmg['DMG'])
                                            elif enh_type == 'LIFE':
                                                t_health = round(t_health + dmg['DMG'])
                                                o_health = round(o_health - dmg['DMG'])
                                            elif enh_type == 'DRAIN':
                                                t_stamina = round(t_stamina + dmg['DMG'])
                                                o_stamina = round(o_stamina - dmg['DMG'])
                                            t_stamina = t_stamina - int(dmg['STAMINA_USED'])
                                            embedVar = discord.Embed(title=f"{dmg['MESSAGE']}", colour=embed_color_t)
                                            await ctx.send(embed=embedVar)
                                            turn_total= turn_total + 1
                                            turn = 0
                                        elif dmg['DMG'] == 0:
                                            t_stamina = t_stamina - int(dmg['STAMINA_USED'])
                                            embedVar = discord.Embed(title=f"{dmg['MESSAGE']}", colour=embed_color_t)
                                            await ctx.send(embed=embedVar)
                                            turn_total= turn_total + 1
                                            turn=0
                                        else:
                                            o_health = o_health - int(dmg['DMG'])
                                            if o_health < 0:
                                                o_health=0
                                            t_stamina = t_stamina - int(dmg['STAMINA_USED'])

                                            embedVar = discord.Embed(title=f"{dmg['MESSAGE']}", colour=embed_color_t)
                                            await ctx.send(embed=embedVar)
                                            turn_total= turn_total + 1
                                            turn=0

                                    else:
                                        await ctx.send(m.NOT_ENOUGH_STAMINA)
                                        turn = 1
                if botActive:
                    end_message="Use the #end command to end the tutorial lobby"
                else:
                    end_message = "Try Again!"
                # End the match
                if o_health <= 0:
                    # await ctx.send(f":zap: {user2.mention} you win the match!")
                    uid = t_DID
                    tuser = await self.bot.fetch_user(uid)
                    wintime = time.asctime()
                    h_playtime = int(wintime[11:13])
                    m_playtime = int(wintime[14:16])
                    s_playtime = int(wintime[17:19])
                    gameClock = getTime(int(h_gametime),int(m_gametime),int(s_gametime),h_playtime,m_playtime,s_playtime)

                    ouid = sowner['DID']
                    sownerctx = await self.bot.fetch_user(ouid)
                    response = await score(sownerctx, tuser)
                    await curse(3, str(ctx.author))
                    embedVar = discord.Embed(title=f":zap: `{t_card}` scores {response} and wins the match!", description=f"Match concluded in {turn_total} turns!", colour=0x1abc9c)
                    embedVar.set_author(name=f"{o_card} lost!\n{end_message}", icon_url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620236432/PCG%20LOGOS%20AND%20RESOURCES/PCGBot_1.png")
                    if int(gameClock[0]) == 0 and int(gameClock[1]) == 0:
                        embedVar.set_footer(text=f"Play again?\nBattle Time: {gameClock[2]} Seconds.")
                    elif int(gameClock[0]) == 0:
                        embedVar.set_footer(text=f"Play again?\nBattle Time: {gameClock[1]} Minutes and {gameClock[2]} Seconds.")
                    else: 
                        embedVar.set_footer(text=f"Play again?\nBattle Time: {gameClock[0]} Hours {gameClock[1]} Minutes and {gameClock[2]} Seconds.")
                    await ctx.send(embed=embedVar)
                    if botActive:                    
                        embedVar = discord.Embed(title=f"PLAY AGAIN", description=f"Don't Worry! Losing is apart of the game. Use the #end command to `END` the tutorial lobby OR use #start to `PLAY AGAIN`", colour=0xe74c3c)
                        embedVar.set_author(name=f"You Lost...")
                        embedVar.add_field(name="Tips!", value="Equiping stronger `TITLES` and `ARMS` will make you character tougher in a fight!")
                        embedVar.set_footer(text="The #shop is full of strong CARDS, TITLES and ARMS try different combinations! ")
                        await ctx.send(embed=embedVar)

                elif t_health <=0:
                    uid = o_DID
                    ouser = await self.bot.fetch_user(uid)
                    wintime = time.asctime()
                    h_playtime = int(wintime[11:13])
                    m_playtime = int(wintime[14:16])
                    s_playtime = int(wintime[17:19])
                    gameClock = getTime(int(h_gametime),int(m_gametime),int(s_gametime),h_playtime,m_playtime,s_playtime)
                    ouid = sowner['DID']
                    sownerctx = await self.bot.fetch_user(ouid)
                    response = await score(sownerctx, ouser)
                    await bless(5, str(ctx.author))
                    embedVar = discord.Embed(title=f":zap: `{o_card}` {response} and wins the match!", description=f"Match concluded in {turn_total} turns!", colour=0xe91e63)
                    embedVar.set_author(name=f"{t_card} lost!\n{end_message}", icon_url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620236432/PCG%20LOGOS%20AND%20RESOURCES/PCGBot_1.png")
                    if int(gameClock[0]) == 0 and int(gameClock[1]) == 0:
                        embedVar.set_footer(text=f"Play again?\nBattle Time: {gameClock[2]} Seconds.")
                    elif int(gameClock[0]) == 0:
                        embedVar.set_footer(text=f"Play again?\nBattle Time: {gameClock[1]} Minutes and {gameClock[2]} Seconds.")
                    else: 
                        embedVar.set_footer(text=f"Play again?\nBattle Time: {gameClock[0]} Hours {gameClock[1]} Minutes and {gameClock[2]} Seconds.")
                    await ctx.send(embed=embedVar)
                    if botActive:                    
                        embedVar = discord.Embed(title=f"VICTORY", description=f"Victories earn `ITEMS` ! Use the #end command to `END` the tutorial lobby\nOR use #start to `PLAY AGAIN`", colour=0xe91e63)
                        embedVar.set_author(name=f"Congratulations You Beat Senpai!")
                        embedVar.add_field(name="Tips!", value="Equiping stronger `TITLES` and `ARMS` will make you character tougher in a fight!")
                        embedVar.set_footer(text="The #shop is full of strong CARDS, TITLES and ARMS try different combinations! ")
                        await ctx.send(embed=embedVar)

        else:
            await ctx.send(m.SESSION_DOES_NOT_EXIST)


async def score(owner, user: User):
        session_query = {"OWNER": str(owner), "AVAILABLE": True, "KINGSGAMBIT": False}
        session_data = db.querySession(session_query)
        teams = [x for x in session_data['TEAMS']]
        winning_team = {}
        for x in teams:
            if str(user) in x['TEAM']: 
                winning_team = x
        new_score = winning_team['SCORE'] + 1
        update_query = {'$set': {'TEAMS.$.SCORE': new_score}}
        query = {"_id": session_data["_id"], "TEAMS.TEAM": str(user)}
        response = db.updateSession(session_query, query, update_query)
        reciever = db.queryUser({'DISNAME': str(user)})
        name = reciever['DISNAME']
        message = ":one: You Scored, Don't Let Up :one:"

        if response:
            message = ":one:"
        else:
            message = "Score not added. Please, try again. "

        return message

def starting_position(o,t):
    if o > t:
        return True
    else:
        return False

def damage_cal(card, ability, attack, defense, op_defense, vul, accuracy, stamina, enhancer, health, op_health, op_stamina): 
    move = list(ability.keys())[0]
    ap = list(ability.values())[0]
    move_stamina = list(ability.values())[1]
    can_use_move_flag = True

    enh = ""
    if enhancer:
        enh = list(ability.values())[2]
    
    # Do I have enough stamina to use this move?
    if stamina >= move_stamina:
        can_use_move_flag = True
    else:
        can_use_move_flag = False
    

    atk = attack
    defense = defense
    stam = stamina
    hlt = health
    lifesteal = op_health
    drain = op_stamina

    enh_type=""
    if enhancer:
        if enh == 'ATK':
            enh_type="ATK"
            atk = ap
        elif enh == 'DEF':
            enh_type="DEF"
            defense = ap
        elif enh == 'STAM':
            enh_type="STAM"
            stam = ap
        elif enh == 'HLT':
            enh_type='HLT'
            hlt = ap + (.10 * health)
        elif enh == 'LIFE':
            enh_type='LIFE'
            lifesteal = ap + (.10 * op_health)
        elif enh == 'DRAIN':
            enh_type='DRAIN'
            drain = ap 

    #handle different staments for lifesteal and drain
    if enhancer:
        if enh_type == 'DRAIN' or enh_type == 'LIFE':
            if enh_type == 'DRAIN':
                message = f'`{card}` used `{move}`! absorbing some STAMINA...'
            else:
                message = f'`{card}` used `{move}`! absorbing some {enh_type}...'
        else:
            message = f'`{card}` used `{move}`! enhanced {enh_type}...'
        enhanced=0
        if enh_type == "ATK":
            enhanced=atk
        elif enh_type == "DEF":
            enhanced=defense
        elif enh_type == "STAM":
            enhanced=stam
        elif enh_type == "HLT":
            enhanced=hlt
        elif enh_type == 'LIFE':
            enhanced =lifesteal
        elif enh_type == 'DRAIN':
            enhanced = drain
        
        response = {"DMG": enhanced, "MESSAGE": message, "STAMINA_USED": move_stamina, "CAN_USE_MOVE": can_use_move_flag, "ENHANCED_TYPE": enh_type, "ENHANCE": True}
        return response

    else:
        # Calculate Damage
        dmg = (int(ap) * int(atk)) / op_defense
        # dmg = (int(ap)*(100/(100+int(op_defense)))) + int(atk)
        low = dmg - (dmg * .3)
        high = dmg + (dmg * .1)

        true_dmg = random.randint(int(low), int(high))
        message = ""

        miss_hit = 3 # Miss
        low_hit = 7 # Lower Damage
        med_hit = 11 # Medium Damage
        standard_hit = 19 # Standard Damage
        high_hit = 20 # Crit Hit
        hit_roll = random.randint(0,20)

        if hit_roll <= miss_hit:
            true_dmg=0
            message=f'`{move}` used! It misses!'
        elif hit_roll <=low_hit and hit_roll > miss_hit:
            true_dmg = round(true_dmg * .75)
            message=f'`{move}` used! It chips for {true_dmg}! :anger:'
        elif hit_roll <=med_hit and hit_roll > low_hit:
            true_dmg = round(true_dmg * .85)
            message=f'`{move}` used! It connects for {true_dmg}! :bangbang:'
        elif hit_roll <=standard_hit and hit_roll > med_hit:
            true_dmg = round(true_dmg)
            message=f'`{move}` used! It hits for {true_dmg}! :anger_right:'
        elif hit_roll == 20:
            true_dmg = round(true_dmg * 2)
            message=f"`{card}` used `{move}`! :boom:   IT CRITICALLY HITS FOR {true_dmg}!! :boom: "

        response = {"DMG": true_dmg, "MESSAGE": message, "STAMINA_USED": move_stamina, "CAN_USE_MOVE": can_use_move_flag, "ENHANCE": False}
        return response

def health_bar(size, radius, alpha=255):
    factor = 5  # Factor to increase the image size that I can later antialiaze the corners
    radius = radius * factor
    image = Image.new('RGBA', (size[0] * factor, size[1] * factor), (0, 0, 0, 0))

    # create corner
    corner = Image.new('RGBA', (radius, radius), (0, 0, 0, 0))
    draw = ImageDraw.Draw(corner)
    # added the fill = .. you only drew a line, no fill
    draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=(50, 50, 50, alpha + 55))

    # max_x, max_y
    mx, my = (size[0] * factor, size[1] * factor)

    # paste corner rotated as needed
    # use corners alpha channel as mask
    image.paste(corner, (0, 0), corner)
    image.paste(corner.rotate(90), (0, my - radius), corner.rotate(90))
    image.paste(corner.rotate(180), (mx - radius, my - radius), corner.rotate(180))
    image.paste(corner.rotate(270), (mx - radius, 0), corner.rotate(270))

    # draw both inner rects
    draw = ImageDraw.Draw(image)
    draw.rectangle([(radius, 0), (mx - radius, my)], fill=(50, 50, 50, alpha))
    draw.rectangle([(0, radius), (mx, my - radius)], fill=(255,0,0,alpha))
    image = image.resize(size, Image.ANTIALIAS)  # Smooth the corners

    return image

def stamina_bar(size, radius, alpha=255):
    factor = 5  # Factor to increase the image size that I can later antialiaze the corners
    radius = radius * factor
    image = Image.new('RGBA', (size[0] * factor, size[1] * factor), (0, 0, 0, 0))

    # create corner
    corner = Image.new('RGBA', (radius, radius), (0, 0, 0, 0))
    draw = ImageDraw.Draw(corner)
    # added the fill = .. you only drew a line, no fill
    draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=(50, 50, 50, alpha + 55))

    # max_x, max_y
    mx, my = (size[0] * factor, size[1] * factor)

    # paste corner rotated as needed
    # use corners alpha channel as mask
    image.paste(corner, (0, 0), corner)
    image.paste(corner.rotate(90), (0, my - radius), corner.rotate(90))
    image.paste(corner.rotate(180), (mx - radius, my - radius), corner.rotate(180))
    image.paste(corner.rotate(270), (mx - radius, 0), corner.rotate(270))

    # draw both inner rects
    draw = ImageDraw.Draw(image)
    draw.rectangle([(radius, 0), (mx - radius, my)], fill=(50, 50, 50, alpha))
    draw.rectangle([(0, radius), (mx, my - radius)], fill=(30,144,255,alpha))
    image = image.resize(size, Image.ANTIALIAS)  # Smooth the corners

    return image

#default bar
def round_rectangle(size, radius, alpha=55):
    factor = 5  # Factor to increase the image size that I can later antialiaze the corners
    radius = radius * factor
    image = Image.new('RGBA', (size[0] * factor, size[1] * factor), (0, 0, 0, 0))

    # create corner
    corner = Image.new('RGBA', (radius, radius), (0, 0, 0, 0))
    draw = ImageDraw.Draw(corner)
    # added the fill = .. you only drew a line, no fill
    draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=(50, 50, 50, alpha + 55))

    # max_x, max_y
    mx, my = (size[0] * factor, size[1] * factor)

    # paste corner rotated as needed
    # use corners alpha channel as mask
    image.paste(corner, (0, 0), corner)
    image.paste(corner.rotate(90), (0, my - radius), corner.rotate(90))
    image.paste(corner.rotate(180), (mx - radius, my - radius), corner.rotate(180))
    image.paste(corner.rotate(270), (mx - radius, 0), corner.rotate(270))

    # draw both inner rects
    draw = ImageDraw.Draw(image)
    draw.rectangle([(radius, 0), (mx - radius, my)], fill=(0, 0, 0, alpha))
    draw.rectangle([(0, radius), (mx, my - radius)], fill=(0, 0, 0, alpha))
    image = image.resize(size, Image.ANTIALIAS)  # Smooth the corners

    return image

def showcard(d, max_health, health, max_stamina, stamina, resolved, title, focused):
    if health <= 0:
        im = Image.open(requests.get(d['PATH'], stream=True).raw)
        im.save("text.png")
        return discord.File("text.png")
    else:
        if resolved:
            im = Image.open(requests.get(d['RPATH'], stream=True).raw)
        else:
            im = Image.open(requests.get(d['PATH'], stream=True).raw)

        # Max Health
        hlt_base = round_rectangle((int(max_health), 30), 0)
        im.paste(hlt_base, (80, 160), hlt_base)
        # Health Meter
        hlt = health_bar((health, 30), 0)
        im.paste(hlt, (80, 160), hlt)


        # Max Stamina
        stam_base = round_rectangle((int(max_stamina), 30), 0)
        im.paste(stam_base, (80, 195), stam_base)
        # Stamina Meter
        stam = stamina_bar((stamina, 30), 0)
        im.paste(stam, (80, 195), stam)

        draw = ImageDraw.Draw(im)
        header = ImageFont.truetype("KomikaTitle-Paint.ttf", 55)
        tournament_wins_font = ImageFont.truetype("RobotoCondensed-Bold.ttf", 35)
        s = ImageFont.truetype("Roboto-Bold.ttf", 22)
        h = ImageFont.truetype("Roboto-Bold.ttf", 35)
        m = ImageFont.truetype("Roboto-Bold.ttf", 25)
        r = ImageFont.truetype("Freedom-10eM.ttf", 40)


        # Health & Stamina
        header = ImageFont.truetype("KomikaTitle-Paint.ttf", 60)
        health_text = f'{health}/{max_health}'
        stamina_text = f'{stamina}/{max_stamina}'
        draw.text((185,155), health_text, (255, 255, 255), font=h, align="left")
        draw.text((82,197), stamina_text, (255, 255, 255), font=s, align="left")

        # Character Name
        draw.text((82,50), d['NAME'], (255, 255, 255), font=header, align="left")
        # Title Name
        draw.text((85,20), title['TITLE'], (255, 255, 255), font=h, align="left")

        if focused:
                        # side    # vert
            draw.line(((0, 0), (0, 800)), fill=(30,144,255), width=15)
            draw.line(((1195, 0), (1195, 800)), fill=(30,144,255), width=10)
            draw.line(((1195, 0), (0, 0)), fill=(30,144,255), width=15)
            draw.line(((0, 600), (1195, 600)), fill=(30,144,255), width=15)
            draw.text((82,130), "FOCUSED", (30,144,255), font=r, align="left")

        if resolved:
                        # side    # vert
            draw.line(((0, 0), (0, 800)), fill=(255,215,0), width=15)
            draw.line(((1195, 0), (1195, 800)), fill=(255,215,0), width=10)
            draw.line(((1195, 0), (0, 0)), fill=(255,215,0), width=15)
            draw.line(((0, 600), (1195, 600)), fill=(255,215,0), width=15)
            draw.text((280,130), "RESOLVED", (255,215,0), font=r, align="left")

        moveset = d['MOVESET']
        # Player Moves
        move1 = moveset[0]
        move1_text = list(move1.keys())[0]

        move2 = moveset[1]
        move2_text = list(move2.keys())[0]

        move3 = moveset[2]
        move3_text = list(move3.keys())[0]

        move_enhanced = moveset[3]
        move_enhanced_text = list(move_enhanced.keys())[0]

        if resolved:
            draw.text((82,240), f"1. R {move1_text}: 10 STAM",  (255, 255, 255), font=m, align="left")
            draw.text((82,270), f"2. R {move2_text}: 30 STAM",  (255, 255, 255), font=m, align="left")
            draw.text((82,300), f"3. R {move3_text}: 80 STAM",  (255, 255, 255), font=m, align="left")
            draw.text((82,330), f"4. R {move_enhanced_text}: 20 STAM",  (255, 255, 255), font=m, align="left")
            draw.text((82,550), f"0. Quit.",  (255, 255, 255), font=m, align="left")
        else:
            if focused:
                draw.text((82,240), f"1. {move1_text}: 10 STAM",  (255, 255, 255), font=m, align="left")
                draw.text((82,270), f"2. {move2_text}: 30 STAM",  (255, 255, 255), font=m, align="left")
                draw.text((82,300), f"3. {move3_text}: 80 STAM",  (255, 255, 255), font=m, align="left")
                draw.text((82,330), f"4. {move_enhanced_text}: 20 STAM",  (255, 255, 255), font=m, align="left")
                draw.text((82,360), f"5. Resolve",  (255, 255, 255), font=m, align="left")
                draw.text((82,550), f"0. Quit.",  (255, 255, 255), font=m, align="left")
            else:
                draw.text((82,240), f"1. {move1_text}: 10 STAM",  (255, 255, 255), font=m, align="left")
                draw.text((82,270), f"2. {move2_text}: 30 STAM",  (255, 255, 255), font=m, align="left")
                draw.text((82,300), f"3. {move3_text}: 80 STAM",  (255, 255, 255), font=m, align="left")
                draw.text((82,330), f"4. {move_enhanced_text}: 20 STAM",  (255, 255, 255), font=m, align="left")
                draw.text((82,550), f"0. Quit.",  (255, 255, 255), font=m, align="left")
        

        # data = io.BytesIO

        # im.save(data, "PNG")

        # encoded_img_data = base64.b64encode(data.getvalue())

        with BytesIO() as image_binary:
            im.save(image_binary, "PNG")
            image_binary.seek(0)
            # await ctx.send(file=discord.File(fp=image_binary,filename="image.png"))
            return discord.File(fp=image_binary,filename="image.png")



def setup(bot):
    bot.add_cog(CrownUnlimited(bot))

def getTime(hgame, mgame, sgame, hnow, mnow, snow):
    hoursPassed = hnow - hgame
    minutesPassed = mnow - mgame
    secondsPassed = snow - sgame
    if hoursPassed > 0:
        minutesPassed = mnow     
        if minutesPassed > 0:
            secondsPassed = snow
        else:
            secondsPassed = snow - sgame
    else:
        minutesPassed = mnow - mgame
        if minutesPassed > 0:
            secondsPassed = snow
        else:
            secondsPassed = snow - sgame
    gameTime = str(hoursPassed) + str(minutesPassed) + str(secondsPassed)
    return gameTime

async def bless(amount, user):
   blessAmount = amount
   posBlessAmount = 0 + abs(int(blessAmount))
   query = {'DISNAME': str(user)}
   vaultOwner = db.queryUser(query)
   if vaultOwner:
      vault = db.queryVault({'OWNER' : vaultOwner['DISNAME']})
      update_query = {"$inc": {'BALANCE': posBlessAmount}}
      db.updateVaultNoFilter(vault, update_query)
   else:
      print("cant find vault")

async def curse(amount, user):
      curseAmount = amount
      negCurseAmount = 0 - abs(int(curseAmount))
      query = {'DISNAME': str(user)}
      vaultOwner = db.queryUser(query)
      if vaultOwner:
         vault = db.queryVault({'OWNER' : vaultOwner['DISNAME']})
         update_query = {"$inc": {'BALANCE': int(negCurseAmount)}}
         db.updateVaultNoFilter(vault, update_query)
      else:
         print("cant find vault")