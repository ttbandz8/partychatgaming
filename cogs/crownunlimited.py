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

class CrownUnlimited(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print('Crown Unlimited Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)
    
    # o is Player 1
    # t is Player 2
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

                # Player 1 Data
                o_user = db.queryUser({'DISNAME': team_1['TEAM'][0]})
                o_DID = o_user['DID']
                o_card = o['NAME']
                o_card_path=o['PATH']
                o_max_health = o['HLT']
                o_health = o['HLT']
                o_stamina = o['STAM']
                o_moveset = o['MOVESET']
                o_attack = o['ATK']
                o_defense = o['DEF']
                o_type = o['TYPE']
                o_accuracy = o['ACC']
                o_passive = o['PASS'][0]
                o_speed = o['SPD']
                o_show = o['SHOW']
                o_title_show = otitle['SHOW']
                o_title_passive = otitle['PASS'][0]
                o_vul = False
                user1 = await self.bot.fetch_user(o_DID)
                o_title_passive_bool = False
                
                # Player 1 Passive Config
                if (o_show == o_title_show) or (o_title_show == "Unbound"):
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

                # Player 2 Data
                t_user = db.queryUser({'DISNAME': team_2['TEAM'][0]})
                t_DID = t_user['DID']
                t_card = t['NAME']
                t_card_path=t['PATH']
                t_max_health = t['HLT']
                t_health = t['HLT']
                t_stamina = t['STAM']
                t_moveset = t['MOVESET']
                t_attack = t['ATK']
                t_defense = t['DEF']
                t_type = t['TYPE']
                t_accuracy = t['ACC']
                t_passive = t['PASS'][0]
                t_speed = t['SPD']
                t_show = t['SHOW']
                t_title_show = ttitle['SHOW']
                t_title_passive = ttitle['PASS'][0]
                t_vul = False
                user2 = await self.bot.fetch_user(t_DID)
                t_title_passive_bool = False


                # Player 2 Passive Config
                if (t_show == t_title_show) or (t_title_show == "Unbound"):
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
                
                options = [1,2,3,4,5]
                await ctx.send(f"{user1.mention}: {o_card} VS {user2.mention}: {t_card} has begun!")

                while (o_health >= 0) and (t_health >= 0):
                    if turn == 0:
                        if o_stamina <= 0:
                            o_stamina = o_focus
                            o_health = round(o_health + (o_focus * (.4 + (1/o_health))))
                            o_attack = round(o_attack + (o_focus * (.15 + (1/o_attack))))
                            o_defense = round(o_defense + (o_focus * (.10 + (1/o_defense))))
                            o_used_focus=True
                            await ctx.send(f'{o_card} has entered focus state!\nStamina has recovered! Health has increased by {round(o_focus * (.4 + (1/o_health)))}!\nAttack has increased by {round(o_focus * (.15 + (1/o_attack)))}!\nDefense has increased by {round(o_focus * (.10 + (1/o_defense)))}!')
                            turn = 1
                        else:

                            player_1_card = showcard(o, o_max_health, o_health)
                            await ctx.send(file=player_1_card)
                            await ctx.send(f"{t_card} has {round(t_health)} health. What move will you use, {user1.mention}\nYour health is {round(o_health)}\n Your Stamina is {round(o_stamina)}")

                            # Make sure user is responding with move
                            def check(msg):
                                return msg.author == user1 and msg.channel == ctx.channel and int(msg.content) in options
                            try:
                                msg = await self.bot.wait_for("message",timeout=240.0, check=check)

                                # calculate data based on selected move
                                if int(msg.content) == 1:
                                    dmg = damage_cal(o_card, o_1, o_attack, o_defense, t_defense, o_vul, o_accuracy, o_stamina, o_enhancer_used)
                                elif int(msg.content) == 2:
                                    dmg = damage_cal(o_card, o_2, o_attack, o_defense, t_defense, o_vul, o_accuracy, o_stamina, o_enhancer_used)
                                elif int(msg.content) == 3:
                                    dmg = damage_cal(o_card, o_3, o_attack, o_defense, t_defense, o_vul, o_accuracy, o_stamina, o_enhancer_used)
                                elif int(msg.content) == 4:
                                    o_enhancer_used=True
                                    dmg = damage_cal(o_card, o_enhancer, o_attack, o_defense, t_defense, o_vul, o_accuracy, o_stamina, o_enhancer_used)
                                    o_enhancer_used=False
                                elif int(msg.content) == 5:
                                    if not o_used_resolve and o_used_focus:
                                        o_stamina = o_stamina + o_resolve
                                        o_health = o_health + o_resolve
                                        o_attack = round(o_attack + (o_resolve / o_attack))
                                        o_defense = round(o_defense - (o_resolve / o_defense))
                                        o_used_resolve=True
                                        await ctx.send(f'{o_card} strengthened resolve!!\nStamina has recovered! Health has increased by {o_resolve}!\nAttack has increased by {round(o_attack + (o_resolve / o_attack))}!\nDefenses at risk, dropping by {round(o_defense - (o_resolve / o_defense))} points!!')
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
                                                o_attack = o_attack + dmg['DMG']
                                            elif enh_type == 'DEF':
                                                o_defense = o_defense + dmg['DMG']
                                            elif enh_type == 'STAM':
                                                o_stamina = o_stamina + dmg['DMG']
                                            o_stamina = o_stamina - int(dmg['STAMINA_USED'])
                                            await ctx.send(dmg['MESSAGE'])
                                            turn=1
                                        elif dmg['DMG'] == 0:
                                            o_stamina = o_stamina - int(dmg['STAMINA_USED'])
                                            await ctx.send(dmg['MESSAGE'])
                                            turn=1
                                        else:
                                            t_health = t_health - dmg['DMG']
                                            o_stamina = o_stamina - dmg['STAMINA_USED']
                                            await ctx.send(dmg['MESSAGE'])
                                            turn=1
                                    else:
                                        await ctx.send(m.NOT_ENOUGH_STAMINA)
                                        turn=0
                            except:
                                await ctx.send('Did not work')

                    elif turn == 1:

                        if t_stamina <= 0:
                            t_stamina = t_focus
                            t_health = t_health + (t_focus * (.4 + (1/t_health)))
                            t_attack = t_attack + (t_focus * (.15 + (1/t_attack)))
                            t_defense = t_defense = (t_focus * (.1 + (1/t_defense)))
                            t_used_focus=True
                            await ctx.send(f'{t_card} has entered focus state!\nStamina has recovered! Health has increased by {round(.4 + (1/t_health))}!\nAttack has increased by {round(t_focus * (.15 + (1/t_attack)))}!\nDefense has increased by {round(t_focus * (.1 + (1/t_defense)))}!')
                            turn=0
                        else:
                            player_2_card = showcard(t, t_max_health, t_health)
                            await ctx.send(file=player_2_card)
                            await ctx.send(f"{o_card} has {round(o_health)} health. What move will you use, {user2.mention}?\nYour health is {round(t_health)}\n Your Stamina is {round(t_stamina)}")

                            # Make sure user is responding with move
                            def check(msg):
                                return msg.author == user2 and msg.channel == ctx.channel and int(msg.content) in options
                            try:
                                msg = await self.bot.wait_for("message",timeout=240.0, check=check)

                                # calculate data based on selected move
                                if int(msg.content) == 1:
                                    dmg = damage_cal(t_card, t_1, t_attack, t_defense, o_defense, t_vul, t_accuracy, t_stamina, t_enhancer_used)
                                elif int(msg.content) == 2:
                                    dmg = damage_cal(t_card, t_2, t_attack, t_defense, o_defense, t_vul, t_accuracy, t_stamina, t_enhancer_used)
                                elif int(msg.content) == 3:
                                    dmg = damage_cal(t_card, t_3, t_attack, t_defense, o_defense, t_vul, t_accuracy, t_stamina, t_enhancer_used)
                                elif int(msg.content) == 4:
                                    t_enhancer_used=True
                                    dmg = damage_cal(t_card, t_enhancer, t_attack, t_defense, o_defense, t_vul, t_accuracy, t_stamina, t_enhancer_used)
                                    t_enhancer_used=False
                                elif int(msg.content) == 5:
                                    if not t_used_resolve and t_used_focus:
                                        t_stamina = t_stamina + t_resolve
                                        t_health = t_health + t_resolve
                                        t_attack = round(t_attack + (t_resolve / t_attack))
                                        t_defense = round(t_defense - (t_resolve / t_defense))
                                        t_used_resolve=True
                                        await ctx.send(f'{t_card} strengthened resolve!!\nStamina has recovered! Health has increased by {t_resolve}!\nAttack has increased by {round(t_attack + (t_resolve / t_attack))}!\nDefenses at risk, dropping by {round(t_defense - (t_resolve / t_defense))} points!!')
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
                                                t_attack = t_attack + dmg['DMG']
                                            elif enh_type == 'DEF':
                                                t_defense = t_defense + dmg['DMG']
                                            elif enh_type == 'STAM':
                                                t_stamina = t_stamina + dmg['DMG']
                                            t_stamina = t_stamina - int(dmg['STAMINA_USED'])
                                            await ctx.send(dmg['MESSAGE'])
                                            turn = 0
                                        elif dmg['DMG'] == 0:
                                            t_stamina = t_stamina - int(dmg['STAMINA_USED'])
                                            await ctx.send(dmg['MESSAGE'])
                                            turn=0
                                        else:
                                            o_health = o_health - int(dmg['DMG'])
                                            t_stamina = t_stamina - int(dmg['STAMINA_USED'])
                                            await ctx.send(dmg['MESSAGE'])
                                            turn=0

                                    else:
                                        await ctx.send(m.NOT_ENOUGH_STAMINA)
                                        turn = 1
                            except:
                                await ctx.send('Did not work')
                # End the match
                if t_health >= 0:
                    await ctx.send(f":zap: {user2.mention} you win the match!")
                elif o_health >=0:
                    await ctx.send(f":zap: {user1.mention} you win the match!")
        else:
            await ctx.send(m.SESSION_DOES_NOT_EXIST)


def starting_position(o,t):
    if o > t:
        return True
    else:
        return False

def damage_cal(card, ability, attack, defense, op_defense, vul, accuracy, stamina, enhancer): 
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

    enh_type=""
    if enhancer:
        if enh == 'ATK':
            enh_type="ATK"
            atk = atk * (ap / 100)
        elif enh == 'DEF':
            enh_type="DEF"
            defense = defense * (ap / 100)
        elif enh == 'STAM':
            enh_type="STAM"
            stam = stam * (ap / 100)

    if enhancer:
        message = f'{card} used {move}! enhanced his {enh_type}...'
        enhanced=0
        if enh_type == "ATK":
            enhanced=atk
        elif enh_type == "DEF":
            enhanced=defense
        elif enh_type == "STAM":
            enhanced=stam
        
        response = {"DMG": enhanced, "MESSAGE": message, "STAMINA_USED": move_stamina, "CAN_USE_MOVE": can_use_move_flag, "ENHANCED_TYPE": enh_type, "ENHANCE": True}
        return response

    else:
        # Calculate Damage
        dmg = (int(ap)*(100/(100+int(op_defense)))) + int(atk)
        low = dmg - (dmg * .3)
        high = dmg + (dmg * .1)

        true_dmg = random.randint(int(low), int(high))
        message = ""

        miss_hit = 5 # Miss
        low_hit = 10 # Lower Damage
        med_hit = 16 # Medium Damage
        standard_hit = 19 # Standard Damage
        high_hit = 20 # Crit Hit
        hit_roll = random.randint(0,20)

        if hit_roll <= miss_hit:
            true_dmg=0
            message=f'{move} used! It misses! :eyes:'
        elif hit_roll <=10 and hit_roll > 5:
            true_dmg = round(true_dmg * .25)
            message=f'{move} used! It chips for {true_dmg}! :anger:'
        elif hit_roll <=16 and hit_roll > 10:
            true_dmg = round(true_dmg * .60)
            message=f'{move} used! It connects for {true_dmg}! :bangbang:'
        elif hit_roll <=19 and hit_roll > 16:
            true_dmg = round(true_dmg)
            message=f'{move} used! It hits for {true_dmg}! :anger_right:'
        elif hit_roll == 20:
            true_dmg = round(true_dmg * 2)
            message=f"{card} used {move}! :boom:   IT CRITICALLY HITS FOR {true_dmg}!! :boom: "

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

def round_rectangle(size, radius, alpha=255):
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
    draw.rectangle([(0, radius), (mx, my - radius)], fill=(50, 50, 50, alpha))
    image = image.resize(size, Image.ANTIALIAS)  # Smooth the corners

    return image

def showcard(d, max_health, health):
    # matches_to_string = dict(ChainMap(*matches))
    # ign_to_string = dict(ChainMap(*ign))

    # game_text = '\n'.join(str(x) for x in games)
    # titles_text = ' '.join(str(x) for x in title)
    # matches_text = "\n".join(f'{k}: {"/".join([str(int) for int in v])}' for k,v in matches_to_string.items())
    
    progress=50
    
    # Meter
    im = Image.open(requests.get(d['PATH'], stream=True).raw)
    img = health_bar((health, 20), 0)
    im.paste(img, (80, 70), img)
    # Max
    img2 = round_rectangle((int(max_health), 20), 0)
    im.paste(img2, (80, 70), img2)

    draw = ImageDraw.Draw(im)
    header = ImageFont.truetype("KomikaTitle-Paint.ttf", 60)
    tournament_wins_font = ImageFont.truetype("RobotoCondensed-Bold.ttf", 35)
    p = ImageFont.truetype("Roboto-Bold.ttf", 25)

    # profile_pic = Image.open(requests.get(d['AVATAR'], stream=True).raw)
    # profile_pic_resized = profile_pic.resize((120, 120), resample=0)
    # img.paste(profile_pic_resized, (1045, 30))
    # draw.text((95,45), name, (255, 255, 255), font=header, align="left")
    # draw.text((5,65), str(tournament_wins), (255, 255, 255), font=tournament_wins_font, align="center")
    # draw.text((60, 320), game_text, (255, 255, 255), font=p, align="left")
    # draw.text((368, 320), team, (255, 255, 255), font=p, align="center")
    # draw.text((635, 320), titles_text, (255, 255, 255), font=p, align="center")
    # draw.text((1040, 320), matches_text, (255, 255, 255), font=p, align="center")

    im.save("text.png")

    return discord.File("text.png")


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