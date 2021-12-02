import discord
from discord.ext import commands
import bot as main
import db
import classes as data
import messages as m
import numpy as np
import help_commands as h
import unique_traits as ut
from discord_slash import SlashCommand
from discord_slash.utils import manage_components
from discord_slash.model import ButtonStyle
# Converters
from discord import User
from discord import Member
from PIL import Image, ImageFont, ImageDraw
import requests
from collections import ChainMap
import DiscordUtils
from .crownunlimited import showcard, cardback, enhancer_mapping, enhancer_suffix_mapping
import random
import textwrap
from discord_slash import cog_ext, SlashContext
from dinteractions_Paginator import Paginator

emojis = ['👍', '👎']

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Profile Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @cog_ext.cog_slash(description="Delete your account (password - IWANTTODELETEMYACCOUNT)", guild_ids=main.guild_ids)
    async def deleteaccount(self, ctx, account: User, password: str):
        user = account
        if password == 'IWANTTODELETEMYACCOUNT':
            if str(ctx.author) == str(account):
                query = {'DISNAME': str(ctx.author)}
                user_is_validated = db.queryUser(query)
                if user_is_validated:

                    accept = await ctx.send(f"{ctx.author.mention}, are you sure you want to delete your account? " + "\n" + "All of your wins, tournament wins, shop purchases and other earnings will be removed from the system can can not be recovered. ", delete_after=10)
                    for emoji in emojis:
                        await accept.add_reaction(emoji)

                    def check(reaction, user):
                        return (user == ctx.author and (str(reaction.emoji) == '👍')) or (user == ctx.author and (str(reaction.emoji) == '👎'))

                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                        if str(reaction.emoji) == '👎':
                            await ctx.send("You're still here!")
                            return

                        delete_user_resp = db.deleteUser(query)
                        vault = db.queryVault({'OWNER': user_is_validated['DISNAME']})
                        if vault:
                            db.deleteVault(vault)
                        else:
                            await ctx.send(delete_user_resp, delete_after=5)
                        team = db.queryTeam()
                    except:
                        await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=3)
                
            else:
                await ctx.send("Invalid command", delete_after=5)


    @cog_ext.cog_slash(description="View your current build", guild_ids=main.guild_ids)
    async def build(self, ctx):
        query = {'DISNAME': str(ctx.author)}
        d = db.queryUser(query)
        card = db.queryCard({'NAME':str(d['CARD'])})
        title = db.queryTitle({'TITLE': str(d['TITLE'])})
        arm = db.queryArm({'ARM': str(d['ARM'])})
        vault = db.queryVault({'OWNER': d['DISNAME']})
        if card:
            try:
                durability = ""
                base_arm_names = ['Reborn Stock', 'Stock', 'Deadgun', 'Glaive', 'Kings Glaive', 'Legendary Weapon']
                for a in vault['ARMS']:
                    if a['ARM'] == str(d['ARM']) and a['ARM'] in base_arm_names:
                        durability = f""
                    elif a['ARM'] == str(d['ARM']) and a['ARM'] not in base_arm_names:
                        durability = f"| ⚒️ {a['DUR']}"
                   
                # Acquire Card Levels data
                card_lvl = 0
                card_tier = 0
                card_exp = 0
                card_lvl_attack_buff = 0
                card_lvl_defense_buff = 0
                card_lvl_ap_buff = 0
                card_lvl_hlt_buff = 0


                for x in vault['CARD_LEVELS']:
                    if x['CARD'] == card['NAME']:
                        card_lvl = x['LVL']
                        card_tier = x['TIER']
                        card_exp = x['EXP']
                        card_lvl_ap_buff = x['AP']
                        card_lvl_attack_buff = x['ATK']
                        card_lvl_defense_buff = x['DEF']
                        card_lvl_hlt_buff = x['HLT']

                oarm_universe = arm['UNIVERSE']
                o_title_universe = title['UNIVERSE']
                o_card = card['NAME']
                o_card_path=card['PATH']
                o_max_health = card['HLT'] + card_lvl_hlt_buff
                o_health = card['HLT'] + card_lvl_hlt_buff
                o_stamina = card['STAM']
                o_max_stamina = card['STAM']
                o_moveset = card['MOVESET']
                o_attack = card['ATK'] + card_lvl_attack_buff
                o_defense = card['DEF'] + card_lvl_defense_buff
                o_type = card['TYPE']
                o_passive = card['PASS'][0]
                o_speed = card['SPD']
                o_show = card['UNIVERSE']
                o_collection = card['COLLECTION']
                o_destiny = card['HAS_COLLECTION']
                o_rebirth = d['REBIRTH']
                
        
                rebirthBonus = o_rebirth * 10
                traits = ut.traits
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

                pets = vault['PETS']

                active_pet = {}
                pet_names = []

                for pet in pets:
                    pet_names.append(pet['NAME'])
                    if pet['NAME'] == d['PET']:
                        active_pet = pet

                power = list(active_pet.values())[3]
                pet_ability_power = (active_pet['BOND'] * active_pet['LVL']) + power
                bond = active_pet['BOND']
                lvl = active_pet['LVL']

                bond_message = ""
                lvl_message = ""
                if bond == 3:
                    bond_message = ":star2:"
                
                if lvl == 10:
                    lvl_message = ":star:"

                # Arm Information
                arm_name = arm['ARM']
                arm_passive = arm['ABILITIES'][0]
                arm_passive_type = list(arm_passive.keys())[0]
                arm_passive_value = list(arm_passive.values())[0]
                title_name= title['TITLE']
                title_passive = title['ABILITIES'][0]
                title_passive_type = list(title_passive.keys())[0]
                title_passive_value = list(title_passive.values())[0]

                o_1 = o_moveset[0]
                o_2 = o_moveset[1]
                o_3 = o_moveset[2]
                o_enhancer = o_moveset[3]
                
                # Move 1
                move1 = list(o_1.keys())[0]
                move1ap = list(o_1.values())[0] + card_lvl_ap_buff
                move1_stamina = list(o_1.values())[1]
                
                # Move 2
                move2 = list(o_2.keys())[0]
                move2ap = list(o_2.values())[0] + card_lvl_ap_buff
                move2_stamina = list(o_2.values())[1]

                # Move 3
                move3 = list(o_3.keys())[0]
                move3ap = list(o_3.values())[0] + card_lvl_ap_buff
                move3_stamina = list(o_3.values())[1]

                # Move Enhancer
                move4 = list(o_enhancer.keys())[0]
                move4ap = list(o_enhancer.values())[0]
                move4_stamina = list(o_enhancer.values())[1]
                move4enh = list(o_enhancer.values())[2]


                resolved = False
                focused = False
                att = 0
                defe = 0
                turn = 0

                passive_name = list(o_passive.keys())[0]
                passive_num = list(o_passive.values())[0]
                passive_type = list(o_passive.values())[1]

                atk_buff = ""
                def_buff = ""
                hlt_buff = ""
                message = ""
                if (oarm_universe == o_show) and (o_title_universe == o_show):
                    o_attack = o_attack + 20
                    o_defense = o_defense + 20
                    o_health = o_health + 100
                    o_max_health = o_max_health + 100
                    message = "_Universe Buff Applied_"
                    if o_destiny:
                        o_attack = o_attack + 25
                        o_defense = o_defense + 25
                        o_health = o_health + 150
                        o_max_health = o_max_health + 150
                        message = "_Destiny Buff Applied_"

                #Title errors 
                titled =False
                titleicon=":warning:"
                licon = ":trident:"
                if card_lvl == 200:
                    licon =":fleur_de_lis:"
                titlemessage = f"{titleicon} **{title_name}** ~ **INEFFECTIVE**"
                warningmessage = f"*Use {o_show} or Unbound Titles on this card*"
                if o_title_universe == "Unbound":
                    titled =True
                    titleicon = ":reminder_ribbon:"
                    titlemessage = f":reminder_ribbon: **{title_name}** {title_passive_type} *{title_passive_value}{enhancer_suffix_mapping[title_passive_type]}*"
                    warningmessage= f""
                elif o_title_universe == o_show:
                    titled =True
                    titleicon = ":reminder_ribbon:"
                    titlemessage = f":reminder_ribbon: **{title_name}** *{title_passive_type} {title_passive_value}{enhancer_suffix_mapping[title_passive_type]}*"
                    warningmessage= f""
                cardtitle = {'TITLE': title_name}
                card_file = showcard(card, o_max_health, o_health, o_max_stamina, o_stamina, resolved, cardtitle, focused, o_attack, o_defense, turn, move1ap, move2ap, move3ap, move4ap, move4enh, card_lvl, None)
                # card_back_file = cardback(card, o_max_health, o_health, o_max_stamina, o_stamina, resolved, arm, focused,
                #                     o_attack, o_defense, turn, passive_name, traitmessage, 0, None, None, passive_type, passive_num, active_pet, pet_ability_power, card_exp)


                embedVar = discord.Embed(title=f"{licon} {card_lvl} {message} {o_card} Build".format(self), description=textwrap.dedent(f"""\
                {titlemessage}
                :mechanical_arm: **{arm_name}** *{arm_passive_type} {arm_passive_value}{enhancer_suffix_mapping[arm_passive_type]}* {durability}
                :bird: **{active_pet['NAME']}** *{active_pet['TYPE']} {pet_ability_power}{enhancer_suffix_mapping[active_pet['TYPE']]}*
                :bird: **Bond** _{bond}_ {bond_message} / **Level** _{lvl}_ {lvl_message}
                
                :drop_of_blood: **{passive_name}:** *{passive_type} {passive_num}{enhancer_suffix_mapping[passive_type]}*
                :infinity: {traitmessage}
                {warningmessage}
                """)
                
                , colour=000000)
                # file = discord.File(fp=card_file,filename="image.png")
                embedVar.set_image(url="attachment://image.png")
                embedVar.set_thumbnail(url=active_pet['PATH'])
                if card_lvl != 200:
                    embedVar.set_footer(text=f"EXP Until Next Level: {150 - card_exp}\nRebirth Buff: +{rebirthBonus}", icon_url="https://cdn.discordapp.com/emojis/841486485826961448.gif?v=1")
                
                await ctx.send(file=card_file, embed=embedVar)
                # await ctx.send(files=[card_file, card_back_file])
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
                await ctx.send("There's an issue with your build. Check with support.")
                return
        else:
            await ctx.send(m.USER_NOT_REGISTERED, delete_after=3)


    @cog_ext.cog_slash(description="Check all your cards", guild_ids=main.guild_ids)
    async def cards(self, ctx):
        await ctx.defer()
        query = {'DISNAME': str(ctx.author)}
        d = db.queryUser(query)
        vault = db.queryVault({'OWNER': d['DISNAME']})
        try: 
            if vault:
                name = d['DISNAME'].split("#",1)[0]
                avatar = d['AVATAR']
                card_levels = vault['CARD_LEVELS']
                balance = vault['BALANCE']
                cards_list = vault['CARDS']
                total_cards = len(cards_list)
                cards=[]
                icon = ":coin:"
                if balance >= 150000:
                    icon = ":money_with_wings:"
                elif balance >=100000:
                    icon = ":moneybag:"
                elif balance >= 50000:
                    icon = ":dollar:"
                
                
                for card in cards_list:
                    index = cards_list.index(card)
                    resp = db.queryCard({"NAME": str(card)})
                    lvl = ""
                    card_available = resp['AVAILABLE']
                    card_exclusive = resp['EXCLUSIVE']
                    card_collection = resp['HAS_COLLECTION']
                    icon = ":flower_playing_cards:"
                    if card_available and card_exclusive:
                        icon = ":fire:"
                    elif card_available == False and card_exclusive ==False:
                        if card_collection:
                            icon =":sparkles:"
                        else:
                            icon = ":japanese_ogre:"
                    for cl in card_levels:
                        if card == cl['CARD']:
                            licon = ":trident:"
                            if cl['LVL'] == 200:
                                licon =":fleur_de_lis:"
                            lvl = f"{licon} **{cl['LVL']}**"
                    cards.append(textwrap.dedent(f"""
                    {icon} [{index}] **{resp['NAME']}** | {lvl}
                    :heart: {resp['HLT']} :dagger: {resp['ATK']} :shield: {resp['DEF']}
                    :earth_americas:  {resp['UNIVERSE']}"""))

                # Adding to array until divisible by 10
                while len(cards) % 10 != 0:
                    cards.append("")
                # Check if divisible by 10, then start to split evenly
                if len(cards) % 10 == 0:
                    first_digit = int(str(len(cards))[:1])
                    if len(cards) >= 89:
                        if first_digit == 1:
                            first_digit = 10
                    cards_broken_up = np.array_split(cards, first_digit)
                
                # If it's not an array greater than 10, show paginationless embed
                if len(cards) < 10:
                    embedVar = discord.Embed(title= f":flower_playing_cards: Cards\n**Balance**: :coin:{'{:,}'.format(balance)}", description="\n".join(cards), colour=0x7289da)
                    embedVar.set_thumbnail(url=avatar)
                    embedVar.set_footer(text=f"/equipcard card name: Equip Card\n/viewcard card name: View Cards Details")
                    await ctx.send(embed=embedVar)

                embed_list = []
                for i in range(0, len(cards_broken_up)):
                    globals()['embedVar%s' % i] = discord.Embed(title= f":flower_playing_cards: Cards\n**Balance**: {icon}{'{:,}'.format(balance)}", description="\n".join(cards_broken_up[i]), colour=0x7289da)
                    globals()['embedVar%s' % i].set_thumbnail(url=avatar)
                    globals()['embedVar%s' % i].set_footer(text=f"{total_cards} Total Cards\n/equipcard card name: Equip Card\n/viewcard card name: View Cards Details")
                    embed_list.append(globals()['embedVar%s' % i])

                paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
                paginator.add_reaction('⏮️', "first")
                paginator.add_reaction('⬅️', "back")
                paginator.add_reaction('🔐', "lock")
                paginator.add_reaction('➡️', "next")
                paginator.add_reaction('⏭️', "last")
                embeds = embed_list
                await paginator.run(embeds)
            else:
                newVault = db.createVault({'OWNER': d['DISNAME']})
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
            await ctx.send("There's an issue with loading your cards. Check with support.")
            return

    @cog_ext.cog_slash(description="Check all your titles", guild_ids=main.guild_ids)
    async def titles(self, ctx):
        await ctx.defer()
        query = {'DISNAME': str(ctx.author)}
        d = db.queryUser(query)
        vault = db.queryVault({'OWNER': d['DISNAME']})
        if vault:
            try:
                name = d['DISNAME'].split("#",1)[0]
                avatar = d['AVATAR']
                balance = vault['BALANCE']
                titles_list = vault['TITLES']
                total_titles = len(titles_list)
                titles=[]
                icon = ":coin:"
                if balance >= 150000:
                    icon = ":money_with_wings:"
                elif balance >=100000:
                    icon = ":moneybag:"
                elif balance >= 50000:
                    icon = ":dollar:"

                for title in titles_list:
                    index = titles_list.index(title)
                    resp = db.queryTitle({"TITLE": str(title)})
                    title_passive = resp['ABILITIES'][0]
                    title_passive_type = list(title_passive.keys())[0]
                    title_passive_value = list(title_passive.values())[0]
                    title_available = resp['AVAILABLE']
                    title_exclusive = resp['EXCLUSIVE']
                    icon = ":reminder_ribbon:"
                    if title_available and title_exclusive:
                        icon = ":fire:"
                    elif title_available == False and title_exclusive ==False:
                        icon = ":japanese_ogre:"
                    titles.append(textwrap.dedent(f"""
                    {icon} [{index}] **{resp['TITLE']}**
                    :microbe: **{title_passive_type}:** {title_passive_value}
                    :earth_africa: **Universe:** {resp['UNIVERSE']}"""))

                # Adding to array until divisible by 10
                while len(titles) % 10 != 0:
                    titles.append("")
                # Check if divisible by 10, then start to split evenly
                if len(titles) % 10 == 0:
                    first_digit = int(str(len(titles))[:1])
                    if len(titles) >= 89:
                        if first_digit == 1:
                            first_digit = 10
                    titles_broken_up = np.array_split(titles, first_digit)
                
                # If it's not an array greater than 10, show paginationless embed
                if len(titles) < 10:
                    embedVar = discord.Embed(title= f"Titles\n**Balance**: :coin:{'{:,}'.format(balance)}", description="\n".join(titles), colour=0x7289da)
                    embedVar.set_thumbnail(url=avatar)
                    embedVar.set_footer(text=f"/equiptitle title name: Equip Title\n/viewtitle title name: View Title Details")
                    await ctx.send(embed=embedVar)

                embed_list = []
                for i in range(0, len(titles_broken_up)):
                    globals()['embedVar%s' % i] = discord.Embed(title= f":reminder_ribbon: Titles\n**Balance**: {icon}{'{:,}'.format(balance)}", description="\n".join(titles_broken_up[i]), colour=0x7289da)
                    globals()['embedVar%s' % i].set_thumbnail(url=avatar)
                    globals()['embedVar%s' % i].set_footer(text=f"{total_titles} Total Titles\n/equiptitle title name: Equip Title\n/viewtitle title name: View Title Details")
                    embed_list.append(globals()['embedVar%s' % i])

                paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
                paginator.add_reaction('⏮️', "first")
                paginator.add_reaction('⬅️', "back")
                paginator.add_reaction('🔐', "lock")
                paginator.add_reaction('➡️', "next")
                paginator.add_reaction('⏭️', "last")
                embeds = embed_list
                await paginator.run(embeds)
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
                await ctx.send("There's an issue with your Titles list. Check with support.")
                return
        else:
            newVault = db.createVault({'OWNER': d['DISNAME']})

    @cog_ext.cog_slash(description="Check all your arms", guild_ids=main.guild_ids)
    async def arms(self, ctx):
        await ctx.defer()
        query = {'DISNAME': str(ctx.author)}
        d = db.queryUser(query)
        vault = db.queryVault({'OWNER': d['DISNAME']})
        if vault:
            try:
                name = d['DISNAME'].split("#",1)[0]
                avatar = d['AVATAR']
                balance = vault['BALANCE']
                arms_list = vault['ARMS']
                total_arms = len(arms_list)

                arms=[]
                icon = ":coin:"
                if balance >= 150000:
                    icon = ":money_with_wings:"
                elif balance >=100000:
                    icon = ":moneybag:"
                elif balance >= 50000:
                    icon = ":dollar:"

                for arm in arms_list:
                    index = arms_list.index(arm)
                    resp = db.queryArm({"ARM": str(arm['ARM'])})
                    arm_passive = resp['ABILITIES'][0]
                    arm_passive_type = list(arm_passive.keys())[0]
                    arm_passive_value = list(arm_passive.values())[0]
                    arm_available = resp['AVAILABLE']
                    arm_exclusive = resp['EXCLUSIVE']
                    icon = ":mechanical_arm:"
                    if arm_available and arm_exclusive:
                        icon = ":fire:"
                    elif arm_available == False and arm_exclusive ==False:
                        icon = ":japanese_ogre:"
                    arms.append(textwrap.dedent(f"""
                    {icon} [{index}] **{resp['ARM']}**
                    :microbe: **{arm_passive_type}:** {arm_passive_value}
                    :earth_africa: **Universe:** {resp['UNIVERSE']}
                    ⚒️ {arm['DUR']}
                    """))


                # Adding to array until divisible by 10
                while len(arms) % 10 != 0:
                    arms.append("")
                # Check if divisible by 10, then start to split evenly
                if len(arms) % 10 == 0:
                    first_digit = int(str(len(arms))[:1])
                    if len(arms) >= 89:
                        if first_digit == 1:
                            first_digit = 10
                    arms_broken_up = np.array_split(arms, first_digit)
                
                # If it's not an array greater than 10, show paginationless embed
                if len(arms) < 10:
                    embedVar = discord.Embed(title= f"Arms\n**Balance**: :coin:{'{:,}'.format(balance)}", description="\n".join(arms), colour=0x7289da)
                    embedVar.set_thumbnail(url=avatar)
                    embedVar.set_footer(text=f"/equiparm arm name: Equip Arm\n/viewarm arm name: View Arm Details")
                    await ctx.send(embed=embedVar)

                embed_list = []
                for i in range(0, len(arms_broken_up)):
                    globals()['embedVar%s' % i] = discord.Embed(title= f":mechanical_arm: Arms\n**Balance**: {icon}{'{:,}'.format(balance)}", description="\n".join(arms_broken_up[i]), colour=0x7289da)
                    globals()['embedVar%s' % i].set_thumbnail(url=avatar)
                    globals()['embedVar%s' % i].set_footer(text=f"{total_arms} Total Arms\n/equiparm arm name: Equip Arm\n/viewarm arm name: View Arm Details")
                    embed_list.append(globals()['embedVar%s' % i])

                paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
                paginator.add_reaction('⏮️', "first")
                paginator.add_reaction('⬅️', "back")
                paginator.add_reaction('🔐', "lock")
                paginator.add_reaction('➡️', "next")
                paginator.add_reaction('⏭️', "last")
                embeds = embed_list
                await paginator.run(embeds)
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
                await ctx.send("There's an issue with your Arms list. Check with support.")
                return
        else:
            newVault = db.createVault({'OWNER': d['DISNAME']})

    @cog_ext.cog_slash(description="Check all your pets", guild_ids=main.guild_ids)
    async def pets(self, ctx):
        await ctx.defer()
        query = {'DISNAME': str(ctx.author)}
        d = db.queryUser(query)
        vault = db.queryVault({'OWNER': d['DISNAME']})
        if vault:
            try:
                name = d['DISNAME'].split("#",1)[0]
                avatar = d['AVATAR']
                balance = vault['BALANCE']
                pets_list = vault['PETS']

                total_pets = len(pets_list)

                pets=[]
                icon = ":coin:"
                if balance >= 150000:
                    icon = ":money_with_wings:"
                elif balance >=100000:
                    icon = ":moneybag:"
                elif balance >= 50000:
                    icon = ":dollar:"
                bond_message = ""
                lvl_message = ""
                for pet in pets_list:
                    #cpetmove_ap= (cpet_bond * cpet_lvl) + list(cpet.values())[3] # Ability Power
                    bond_message = ""
                    if pet['BOND'] == 3:
                        bond_message = ":star2:"
                    lvl_message = ""
                    if pet['LVL'] == 10:
                        lvl_message = ":star:"
                    
                    pet_ability = list(pet.keys())[3]
                    pet_ability_power = list(pet.values())[3]
                    power = (pet['BOND'] * pet['LVL']) + pet_ability_power
                    pet_info = db.queryPet({'PET' : pet['NAME']})
                    if pet_info:
                        pet_available = pet_info['AVAILABLE']
                        pet_exclusive = pet_info['EXCLUSIVE']
                    icon = ":bird:"
                    if pet_available and pet_exclusive:
                        icon = ":fire:"
                    elif pet_available == False and pet_exclusive ==False:
                        icon = ":japanese_ogre:"
                    pets.append(textwrap.dedent(f"""
                    {icon} **{pet['NAME']}** | _B_ **{pet['BOND']}** {bond_message} / _L_ **{pet['LVL']} {lvl_message}**
                    :small_blue_diamond: **{pet_ability}:** {power}
                    :microbe: **Type:** {pet['TYPE']}"""))

                # Adding to array until divisible by 10
                while len(pets) % 10 != 0:
                    pets.append("")

                # Check if divisible by 10, then start to split evenly
                if len(pets) % 10 == 0:
                    first_digit = int(str(len(pets))[:1])
                    if len(pets) >= 89:
                        if first_digit == 1:
                            first_digit = 10
                    pets_broken_up = np.array_split(pets, first_digit)
                
                # If it's not an array greater than 10, show paginationless embed
                if len(pets) < 10:
                    embedVar = discord.Embed(title= f"Pets\n**Balance**: :coin:{'{:,}'.format(balance)}", description="\n".join(pets), colour=0x7289da)
                    embedVar.set_thumbnail(url=avatar)
                    embedVar.set_footer(text=f"/equippet pet name: Equip Pet\n/viewpet pet name: View Pet Details")
                    await ctx.send(embed=embedVar)

                embed_list = []
                for i in range(0, len(pets_broken_up)):
                    globals()['embedVar%s' % i] = discord.Embed(title= f":bird: Pets\n**Balance**: {icon}{'{:,}'.format(balance)}", description="\n".join(pets_broken_up[i]), colour=0x7289da)
                    globals()['embedVar%s' % i].set_thumbnail(url=avatar)
                    globals()['embedVar%s' % i].set_footer(text=f"{total_pets} Total Pets\n/equippet pet name: Equip Pet\n/viewpet pet name: View Pet Details")
                    embed_list.append(globals()['embedVar%s' % i])

                paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
                paginator.add_reaction('⏮️', "first")
                paginator.add_reaction('⬅️', "back")
                paginator.add_reaction('🔐', "lock")
                paginator.add_reaction('➡️', "next")
                paginator.add_reaction('⏭️', "last")
                embeds = embed_list
                await paginator.run(embeds)
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
                await ctx.send("There's an issue with your Pets list. Check with support.")
                return
        else:
            newVault = db.createVault({'OWNER': d['DISNAME']})

    @cog_ext.cog_slash(description="Check all your destiny lines", guild_ids=main.guild_ids)
    async def destinies(self, ctx):
        await ctx.defer()
        query = {'DISNAME': str(ctx.author)}
        d = db.queryUser(query)
        vault = db.queryVault({'OWNER': d['DISNAME']})
        if not vault['DESTINY']:
            await ctx.send("No Destiny Lines available at this time!")
            return
        if vault:
            try:
                name = d['DISNAME'].split("#",1)[0]
                avatar = d['AVATAR']
                balance = vault['BALANCE']
                destiny = vault['DESTINY']

                destiny_messages = []
                icon = ":coin:"
                if balance >= 150000:
                    icon = ":money_with_wings:"
                elif balance >=100000:
                    icon = ":moneybag:"
                elif balance >= 50000:
                    icon = ":dollar:"
                for d in destiny:
                    if not d['COMPLETED']:
                        destiny_messages.append(textwrap.dedent(f"""\
                        :sparkles: **{d["NAME"]}**
                        Defeat **{d['DEFEAT']}** with **{" ".join(d['USE_CARDS'])}** | **Current Progress:** {d['WINS']}/{d['REQUIRED']}
                        Win :flower_playing_cards: **{d['EARN']}**
                        """))

                if not destiny_messages:
                    await ctx.send("No Destiny Lines available at this time!")
                    return
                # Adding to array until divisible by 10
                while len(destiny_messages) % 10 != 0:
                    destiny_messages.append("")

                # Check if divisible by 10, then start to split evenly
                if len(destiny_messages) % 10 == 0:
                    first_digit = int(str(len(destiny_messages))[:1])
                    if len(destiny_messages) >= 89:
                        if first_digit == 1:
                            first_digit = 10
                    destinies_broken_up = np.array_split(destiny_messages, first_digit)
                
                # If it's not an array greater than 10, show paginationless embed
                if len(destiny_messages) < 10:
                    embedVar = discord.Embed(title= f"Destiny Lines\n**Balance**: :coin:{'{:,}'.format(balance)}", description="\n".join(destiny_messages), colour=0x7289da)
                    embedVar.set_thumbnail(url=avatar)
                    # embedVar.set_footer(text=f".equippet pet name: Equip Pet\n.viewpet pet name: View Pet Details")
                    await ctx.send(embed=embedVar)

                embed_list = []
                for i in range(0, len(destinies_broken_up)):
                    globals()['embedVar%s' % i] = discord.Embed(title= f":sparkles: Destiny Lines\n**Balance**: {icon}{'{:,}'.format(balance)}", description="\n".join(destinies_broken_up[i]), colour=0x7289da)
                    globals()['embedVar%s' % i].set_thumbnail(url=avatar)
                    # globals()['embedVar%s' % i].set_footer(text=f"{total_pets} Total Pets\n.equippet pet name: Equip Pet\n.viewpet pet name: View Pet Details")
                    embed_list.append(globals()['embedVar%s' % i])

                paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
                paginator.add_reaction('⏮️', "first")
                paginator.add_reaction('⬅️', "back")
                paginator.add_reaction('🔐', "lock")
                paginator.add_reaction('➡️', "next")
                paginator.add_reaction('⏭️', "last")
                embeds = embed_list
                await paginator.run(embeds)
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
                await ctx.send("There's an issue with your Destiny Line list. Check with support.")
                return
        else:
            newVault = db.createVault({'OWNER': d['DISNAME']})

    @cog_ext.cog_slash(description="Check all your quests", guild_ids=main.guild_ids)
    async def quests(self, ctx):
        await ctx.defer()
        query = {'DISNAME': str(ctx.author)}
        d = db.queryUser(query)
        vault = db.queryVault({'OWNER': d['DISNAME']})
        if not vault['QUESTS']:
            await ctx.send("No Quests available at this time!")
            return
        if vault:
            try:
                name = d['DISNAME'].split("#",1)[0]
                avatar = d['AVATAR']
                balance = vault['BALANCE']
                quests = vault['QUESTS']

                quest_messages = []
                for quest in quests:
                    completed = ""
                    if quest['GOAL'] == quest['WINS']:
                        completed = "🟢"
                    else:
                        completed = "🔴"
                    quest_messages.append(textwrap.dedent(f"""\
                    Defeat **{quest['OPPONENT']}** {quest['GOAL']} times in {quest['TYPE']} for :coin:{'{:,}'.format(quest['REWARD'])}! : {completed}
                    **Current Progress:** {quest['WINS']}/{quest['GOAL']}
                    
                    """))
                
                embedVar = discord.Embed(title= f":notepad_spiral: Quest Board", description=textwrap.dedent(f"""
                    **Balance**: :coin:{'{:,}'.format(balance)}
                    \n{"".join(quest_messages)}
                    """), colour=0x7289da)
                embedVar.set_footer(text="Use /tales or /dungeons to complete daily quest!", icon_url="https://cdn.discordapp.com/emojis/784402243519905792.gif?v=1")
                await ctx.send(embed=embedVar)
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
                await ctx.send("There's an issue with your Quest list. Check with support.")
                return
        else:
            newVault = db.createVault({'OWNER': d['DISNAME']})

    @cog_ext.cog_slash(description="Check your balance", guild_ids=main.guild_ids)
    async def bal(self, ctx):
        try:
            query = {'DISNAME': str(ctx.author)}
            d = db.queryUser(query)
            vault = db.queryVault({'OWNER': d['DISNAME']})
            icon = ":coin:"
            if vault:
                name = d['DISNAME'].split("#",1)[0]
                avatar = d['AVATAR']
                balance = vault['BALANCE']
                if balance >= 150000:
                    icon = ":money_with_wings:"
                elif balance >=100000:
                    icon = ":moneybag:"
                elif balance >= 50000:
                    icon = ":dollar:"
                if d['TEAM'] != 'PCG':
                    t = db.queryTeam({'TNAME' : d['TEAM']})
                    tbal = t['BANK']
                    if d['FAMILY'] != 'PCG':
                        f = db.queryFamily({'HEAD': d['FAMILY']})
                        fbal = f['BANK']
                embedVar = discord.Embed(title= f"{icon}{'{:,}'.format(balance)}", colour=0x7289da)
                await ctx.send(embed=embedVar)
            else:
                newVault = db.createVault({'OWNER': d['DISNAME']})
        except:
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
            
    @cog_ext.cog_slash(description="Check your build presets", guild_ids=main.guild_ids)
    async def preset(self, ctx):
        query = {'DISNAME': str(ctx.author)}
        d = db.queryUser(query)
        vault_query = {'OWNER': d['DISNAME']}
        vault = db.queryVault(vault_query)
        if vault:
            ownedcards = []
            ownedtitles = []
            ownedarms = []
            ownedpets = []
            for cards in vault['CARDS']:
                ownedcards.append(cards)
            for titles in vault['TITLES']:
                ownedtitles.append(titles)
            for arms in vault['ARMS']:
                ownedarms.append(arms)
            for pets in vault['PETS']:
                ownedpets.append(pets['NAME'])

            name = d['DISNAME'].split("#",1)[0]
            avatar = d['AVATAR']
            cards = vault['CARDS']
            titles = vault['TITLES']
            deck = vault['DECK']
            
            preset1_card = list(deck[0].values())[0]
            preset1_title = list(deck[0].values())[1]
            preset1_arm = list(deck[0].values())[2]
            preset1_pet = list(deck[0].values())[3]

            preset2_card = list(deck[1].values())[0]
            preset2_title = list(deck[1].values())[1]
            preset2_arm = list(deck[1].values())[2]
            preset2_pet = list(deck[1].values())[3]

            preset3_card = list(deck[2].values())[0]
            preset3_title = list(deck[2].values())[1]
            preset3_arm = list(deck[2].values())[2]
            preset3_pet = list(deck[2].values())[3]    
   
            listed_options = [f"1️⃣ | {preset1_title} {preset1_card} and {preset1_pet}\n**Card**: {preset1_card}\n**Title**: {preset1_title}\n**Arm**: {preset1_arm}\n**Pet**: {preset1_pet}\n\n", 
            f"2️⃣ | {preset2_title} {preset2_card} and {preset2_pet}\n**Card**: {preset2_card}\n**Title**: {preset2_title}\n**Arm**: {preset2_arm}\n**Pet**: {preset2_pet}\n\n", 
            f"3️⃣ | {preset3_title} {preset3_card} and {preset3_pet}\n**Card**: {preset3_card}\n**Title**: {preset3_title}\n**Arm**: {preset3_arm}\n**Pet**: {preset3_pet}\n\n"]
        
            embedVar = discord.Embed(title="What Preset would you like?", description=textwrap.dedent(f"""
            {"".join(listed_options)}
            """))
            embedVar.set_thumbnail(url=avatar)
            # embedVar.add_field(name=f"Preset 1:{preset1_title} {preset1_card} and {preset1_pet}", value=f"Card: {preset1_card}\nTitle: {preset1_title}\nArm: {preset1_arm}\nPet: {preset1_pet}", inline=False)
            # embedVar.add_field(name=f"Preset 2:{preset2_title} {preset2_card} and {preset2_pet}", value=f"Card: {preset2_card}\nTitle: {preset2_title}\nArm: {preset2_arm}\nPet: {preset2_pet}", inline=False)
            # embedVar.add_field(name=f"Preset 3:{preset3_title} {preset3_card} and {preset3_pet}", value=f"Card: {preset3_card}\nTitle: {preset3_title}\nArm: {preset3_arm}\nPet: {preset3_pet}", inline=False)
            util_buttons = [
                manage_components.create_button(
                    style=ButtonStyle.red,
                    label="1️⃣",
                    custom_id = "1"
                ),
                manage_components.create_button(
                    style=ButtonStyle.blue,
                    label="2️⃣",
                    custom_id = "2"
                ),
                manage_components.create_button(
                    style=ButtonStyle.green,
                    label="3️⃣",
                    custom_id = "3"
                ),
                manage_components.create_button(
                    style=ButtonStyle.grey,
                    label="Quit",
                    custom_id = "0"
                ),
            ]
            util_action_row = manage_components.create_actionrow(*util_buttons)
            components = [util_action_row]
            await ctx.send(embed=embedVar,components=[util_action_row])
            
            def check(button_ctx):
                return button_ctx.author == ctx.author
            try:
                button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[util_action_row], timeout=120,check=check)

                if  button_ctx.custom_id == "0":
                    await button_ctx.send(f"{ctx.author.mention}, No change has been made")
                    return
                elif  button_ctx.custom_id == "1":
                    for card in ownedcards :                     
                        if preset1_card in ownedcards:
                            for title in ownedtitles:
                                if preset1_title in ownedtitles:
                                    for arm in ownedarms:
                                        if preset1_arm in ownedarms:
                                            for pet in ownedpets:
                                                if preset1_pet in ownedpets:
                                                    response = db.updateUserNoFilter(query, {'$set': {'CARD': str(preset1_card), 'TITLE': str(preset1_title),'ARM': str(preset1_arm), 'PET': str(preset1_pet)}})
                                                    await button_ctx.send(response)
                                                    return
                                                else:
                                                    await button_ctx.send(f"{ctx.author.mention}, You No Longer Own {preset1_pet}")
                                                    return
                                        else:
                                            await button_ctx.send(f"{ctx.author.mention}, You No Longer Own {preset1_arm}")
                                            return
                                else:
                                    await button_ctx.send(f"{ctx.author.mention}, You No Longer Own {preset1_title}")
                                    return
                        else:
                            await button_ctx.send(f"{ctx.author.mention}, You No Longer Own {preset1_card}")
                            return
                elif  button_ctx.custom_id == "2":
                    for card in ownedcards :                     
                        if preset2_card in ownedcards:
                            for title in ownedtitles:
                                if preset2_title in ownedtitles:
                                    for arm in ownedarms:
                                        if preset2_arm in ownedarms:
                                            for pet in ownedpets:
                                                if preset2_pet in ownedpets:
                                                    response = db.updateUserNoFilter(query, {'$set': {'CARD': str(preset2_card), 'TITLE': str(preset2_title),'ARM': str(preset2_arm), 'PET': str(preset2_pet)}})
                                                    await button_ctx.send(response)
                                                    return
                                                else:
                                                    await button_ctx.send(f"{ctx.author.mention}, You No Longer Own {preset2_pet}")
                                                    return
                                        else:
                                            await button_ctx.send(f"{ctx.author.mention}, You No Longer Own {preset2_arm}")
                                            return
                                else:
                                    await button_ctx.send(f"{ctx.author.mention}, You No Longer Own {preset2_title}")
                                    return
                        else:
                            await button_ctx.send(f"{ctx.author.mention}, You No Longer Own {preset2_card}")
                            return
                elif  button_ctx.custom_id == "3":
                    for card in ownedcards :                     
                        if preset3_card in ownedcards:
                            for title in ownedtitles:
                                if preset3_title in ownedtitles:
                                    for arm in ownedarms:
                                        if preset3_arm in ownedarms:
                                            for pet in ownedpets:
                                                if preset3_pet in ownedpets:
                                                    response = db.updateUserNoFilter(query, {'$set': {'CARD': str(preset3_card), 'TITLE': str(preset3_title),'ARM': str(preset3_arm), 'PET': str(preset3_pet)}})
                                                    await button_ctx.send(response)
                                                    return
                                                else:
                                                    await button_ctx.send(f"{ctx.author.mention}, You No Longer Own {preset3_pet}")
                                                    return
                                        else:
                                            await button_ctx.send(f"{ctx.author.mention}, You No Longer Own {preset3_arm}")
                                            return
                                else:
                                    await button_ctx.send(f"{ctx.author.mention}, You No Longer Own {preset3_title}")
                                    return
                        else:
                            await button_ctx.send(f"{ctx.author.mention}, You No Longer Own {preset3_card}")
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
                await ctx.send("Preset Issue Seek support.")
        else:
            newVault = db.createVault({'OWNER': d['DISNAME']})

    @cog_ext.cog_slash(description="Save your current build as preset", guild_ids=main.guild_ids)
    async def savepreset(self, ctx):
        query = {'DISNAME': str(ctx.author)}
        d = db.queryUser(query)
        vault_query = {'OWNER': d['DISNAME']}
        vault = db.queryVault(vault_query)
        if vault:
            name = d['DISNAME'].split("#",1)[0]
            avatar = d['AVATAR']
            cards = vault['CARDS']
            titles = vault['TITLES']
            deck = vault['DECK']


            current_card = d['CARD']
            current_title = d['TITLE']
            current_arm= d['ARM']
            current_pet = d['PET']

            
            preset1_card = list(deck[0].values())[0]
            preset1_title = list(deck[0].values())[1]
            preset1_arm = list(deck[0].values())[2]
            preset1_pet = list(deck[0].values())[3]

            preset2_card = list(deck[1].values())[0]
            preset2_title = list(deck[1].values())[1]
            preset2_arm = list(deck[1].values())[2]
            preset2_pet = list(deck[1].values())[3]

            preset3_card = list(deck[2].values())[0]
            preset3_title = list(deck[2].values())[1]
            preset3_arm = list(deck[2].values())[2]
            preset3_pet = list(deck[2].values())[3]    
   
            listed_options = [f"📝 | {current_title} {current_card} & {current_pet}\n**Card**: {current_card}\n**Title**: {current_title}\n**Arm**: {current_arm}\n**Pet**: {current_pet}\n\n",
            f"1️⃣ | {preset1_title} {preset1_card} & {preset1_pet}\n**Card**: {preset1_card}\n**Title**: {preset1_title}\n**Arm**: {preset1_arm}\n**Pet**: {preset1_pet}\n\n", 
            f"2️⃣ | {preset2_title} {preset2_card} & {preset2_pet}\n**Card**: {preset2_card}\n**Title**: {preset2_title}\n**Arm**: {preset2_arm}\n**Pet**: {preset2_pet}\n\n", 
            f"3️⃣ | {preset3_title} {preset3_card} & {preset3_pet}\n**Card**: {preset3_card}\n**Title**: {preset3_title}\n**Arm**: {preset3_arm}\n**Pet**: {preset3_pet}\n\n"]
        
            embedVar = discord.Embed(title=f"Save Current Build", description=textwrap.dedent(f"""
            {"".join(listed_options)}
            """))
            util_buttons = [
                manage_components.create_button(
                    style=ButtonStyle.red,
                    label="📝 1️⃣",
                    custom_id = "1"
                ),
                manage_components.create_button(
                    style=ButtonStyle.blue,
                    label="📝 2️⃣",
                    custom_id = "2"
                ),
                manage_components.create_button(
                    style=ButtonStyle.green,
                    label="📝 3️⃣",
                    custom_id = "3"
                ),
                manage_components.create_button(
                    style=ButtonStyle.grey,
                    label="Quit",
                    custom_id = "0"
                ),
            ]
            util_action_row = manage_components.create_actionrow(*util_buttons)
            components = [util_action_row]
            await ctx.send(embed=embedVar,components=[util_action_row])

            
            def check(button_ctx):
                return button_ctx.author == ctx.author

            try:
                button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[util_action_row], timeout=120,check=check)

                if button_ctx.custom_id == "0":
                    await button_ctx.send(f"{ctx.author.mention}, No change has been made")
                    return
                elif button_ctx.custom_id == "1":
                    response = db.updateVaultNoFilter(vault_query, {'$set': {'DECK.0.CARD' :str(current_card), 'DECK.0.TITLE': str(current_title),'DECK.0.ARM': str(current_arm), 'DECK.0.PET': str(current_pet)}})
                    await button_ctx.send(response)
                    return
                elif button_ctx.custom_id == "2":
                    response = db.updateVaultNoFilter(vault_query, {'$set': {'DECK.1.CARD' :str(current_card), 'DECK.1.TITLE': str(current_title),'DECK.1.ARM': str(current_arm), 'DECK.1.PET': str(current_pet)}})
                    await button_ctx.send(response)
                    return
                elif button_ctx.custom_id == "3":
                    response = db.updateVaultNoFilter(vault_query, {'$set': {'DECK.2.CARD' :str(current_card), 'DECK.2.TITLE': str(current_title),'DECK.2.ARM': str(current_arm), 'DECK.2.PET': str(current_pet)}})
                    await button_ctx.send(response)
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
                await ctx.send("Preset Issue Seek support.")
        else:
            newVault = db.createVault({'OWNER': d['DISNAME']})

    @cog_ext.cog_slash(description="Open pop up shop", guild_ids=main.guild_ids)
    async def shop(self, ctx):
        all_universes = db.queryAllUniverse()
        user = db.queryUser({'DISNAME': str(ctx.author)})
        available_universes = []
        riftShopOpen = False
        shopName = ':shopping_cart:Pop Up Shop'
        if user['RIFT'] == 1:
            riftShopOpen = True
            shopName = ':crystal_ball: Rift Shop'
            
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
        
        
        # Pull all cards that don't require tournaments
        resp = db.queryShopCards()

        #
        vault_query = {'OWNER' : str(ctx.author)}
        vault = db.altQueryVault(vault_query)
        balance = vault['BALANCE']
        icon = ":coin:"
        if balance >= 150000:
            icon = ":money_with_wings:"
        elif balance >=100000:
            icon = ":moneybag:"
        elif balance >= 50000:
            icon = ":dollar:"
        cards = []
        card_text_list = []
        for card in resp:
            if card['UNIVERSE'] in available_universes:
                # Don't produce cards you can't afford
                if card['PRICE'] != 0 and card['PRICE'] < (vault['BALANCE'] + 1500) and card['AVAILABLE'] and card['EXCLUSIVE'] != True:
                    if card['NAME'] not in vault['CARDS']:
                        cards.append({'NAME': card['NAME'], 'PRICE': card['PRICE'], 'UNIVERSE': card['UNIVERSE'], 'STOCK': card['STOCK']})
        
        random_cards = random.sample(cards, min(len(cards), 10))
        for card in random_cards:
            if card['STOCK'] == 0:
                card_text_list.append(f"**{card['NAME']}**: :coin:{card['PRICE']} " + f"_{card['UNIVERSE']}_ **Out Of Stock**")
            else:
                card_text_list.append(f"**{card['NAME']}**: :coin:{card['PRICE']} " + f"_{card['UNIVERSE']}_")

        title_resp = db.queryShopTitles()
        titles = []
        title_text_list = []
        for title in title_resp:
            if title['UNIVERSE'] in available_universes or title['UNIVERSE'] == 'Unbound':
                if title['PRICE'] != 0 and title['PRICE'] < (vault['BALANCE'] + 1500) and title['AVAILABLE'] and title['EXCLUSIVE'] != True:
                    if title['TITLE'] not in vault['TITLES']:
                        titles.append({'TITLE': title['TITLE'], 'PRICE': title['PRICE'], 'UNIVERSE': title['UNIVERSE'], 'STOCK': title['STOCK']})

        random_titles = random.sample(titles, min(len(titles), 10))
        for title in random_titles:
            if title['STOCK'] == 0:
                title_text_list.append(f"**{title['TITLE']}**: :coin:{title['PRICE']} " + f"_{title['UNIVERSE']}_ **Out Of Stock**")
            else:
                title_text_list.append(f"**{title['TITLE']}**: :coin:{title['PRICE']} " + f"_{title['UNIVERSE']}_")
        
        
        arm_resp = db.queryShopArms()
        arms = []
        arm_text_list = []
        for arm in arm_resp:
            if arm['UNIVERSE'] in available_universes or arm['UNIVERSE'] == 'Unbound':
                if arm['PRICE'] != 0 and arm['PRICE'] < (vault['BALANCE'] + 1500) and arm['AVAILABLE'] and arm['EXCLUSIVE'] != True:
                    if arm['ARM'] not in vault['ARMS']:
                        arms.append({'ARM': arm['ARM'], 'PRICE': arm['PRICE'], 'UNIVERSE': arm['UNIVERSE'], 'STOCK': arm['STOCK']})

        random_arms = random.sample(arms, min(len(arms), 10))
        for arm in random_arms:
            if arm['STOCK'] == 0:
                arm_text_list.append(f"**{arm['ARM']}**: :coin:{arm['PRICE']} " + f"_{arm['UNIVERSE']}_ **Out Of Stock**")
            else:
                arm_text_list.append(f"**{arm['ARM']}**: :coin:{arm['PRICE']} " + f"_{arm['UNIVERSE']}_")
        
        embedVar1 = discord.Embed(title=f"{shopName}", description=textwrap.dedent(f"""
        **Balance:** {icon}{'{:,}'.format(vault['BALANCE'])}
        **/cardlist universe:** View Universe Card List
        **/viewcard card name:** View Cards
        **/buycard card name:** Buy Card
        """), colour=0x2ecc71, value='Page 1')
        # embedVar1.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620236723/PCG%20LOGOS%20AND%20RESOURCES/Party_Chat_Shop.png")
        embedVar1.add_field(name=":shopping_bags: Cards", value="\n".join(card_text_list))
        embedVar1.set_footer(text="Stock updated every day")

        embedVar2 = discord.Embed(title=f"{shopName}", description=textwrap.dedent(f"""
        **Balance:** :coin:{'{:,}'.format(vault['BALANCE'])}
        **/titlelist universe:** View Universe Title List
        **/viewtitle title name:** View Title Stats
        **/buytitle title name:** Buy Title
        """), colour=0x3498db, value='Page 2')
        # embedVar2.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620236723/PCG%20LOGOS%20AND%20RESOURCES/Party_Chat_Shop.png")
        embedVar2.add_field(name=":shopping_bags: Titles", value="\n".join(title_text_list))
        embedVar2.set_footer(text="Stock updated every day")

        embedVar3 = discord.Embed(title=f"{shopName}", description=textwrap.dedent(f"""
        **Balance:** :coin:{'{:,}'.format(vault['BALANCE'])}
        **/armlist universe:** View Universe Arm List
        **/viewarm arm name:** View Arm Stats
        **/buyarm arm name** Buy Arm
        """), colour=0xf1c40f, value='Page 3')
        # embedVar3.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620236723/PCG%20LOGOS%20AND%20RESOURCES/Party_Chat_Shop.png")
        embedVar3.add_field(name=":shopping_bags: Arm", value="\n".join(arm_text_list))
        embedVar3.set_footer(text="Stock updated every day")

        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
        paginator.add_reaction('⏮️', "first")
        paginator.add_reaction('⬅️', "back")
        paginator.add_reaction('🔐', "lock")
        paginator.add_reaction('➡️', "next")
        paginator.add_reaction('⏭️', "last")
        embeds = [embedVar1,embedVar2,embedVar3]
        await paginator.run(embeds)

def setup(bot):
    bot.add_cog(Profile(bot))