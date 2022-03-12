import discord
from discord.ext import commands
from pymongo import response
# from soupsieve import select
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
from .crownunlimited import showcard, cardback, enhancer_mapping, title_enhancer_mapping, enhancer_suffix_mapping, title_enhancer_suffix_mapping, passive_enhancer_suffix_mapping, battle_commands, Crest_dict, cardlevel, guild_buff_update_function, destiny as update_destiny_call
import random
import textwrap
from discord_slash import cog_ext, SlashContext
from dinteractions_Paginator import Paginator
import destiny as d


emojis = ['👍', '👎']

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Profile Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @cog_ext.cog_slash(description="Delete your account", guild_ids=main.guild_ids)
    async def deleteaccount(self, ctx):
        user = str(ctx.author)
        query = {'DID': str(ctx.author.id)}
        user_is_validated = db.queryUser(query)
        if user_is_validated:
            accept_buttons = [
                manage_components.create_button(
                    style=ButtonStyle.green,
                    label="Yes",
                    custom_id="yes"
                ),
                manage_components.create_button(
                    style=ButtonStyle.blue,
                    label="No",
                    custom_id="no"
                )
            ]
            accept_buttons_action_row = manage_components.create_actionrow(*accept_buttons)

            team = db.queryTeam({'TEAM_NAME': user_is_validated['TEAM'].lower()})

            await ctx.send(f"{ctx.author.mention}, are you sure you want to delete your account? " + "\n" + "All of your wins, purchases and other earnings will be removed from the system and can not be recovered. ", hidden=True, components=[accept_buttons_action_row])

            def check(button_ctx):
                return button_ctx.author == ctx.author

            try:
                button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[accept_buttons_action_row], timeout=120,check=check)

                if button_ctx.custom_id == "no":
                    await button_ctx.send("Account not deleted.")
                    return

                if button_ctx.custom_id == "yes":
                    if team:
                        transaction_message = f"{user_is_validated['DISNAME']} left the game."
                        team_query = {'TEAM_NAME': team['TEAM_NAME']}
                        new_value_query = {
                            '$pull': {
                                'MEMBERS': user_is_validated['DISNAME'],
                                'OFFICERS': user_is_validated['DISNAME'],
                                'CAPTAINS': user_is_validated['DISNAME'],
                            },
                            '$addToSet': {'TRANSACTIONS': transaction_message},
                            '$inc': {'MEMBER_COUNT': -1}
                            }
                        response = db.deleteTeamMember(team_query, new_value_query, str(ctx.author.id))
                    response = db.deleteVault({'DID': str(ctx.author.id)})
                    delete_user_resp = db.deleteUser(user)
                    await button_ctx.send("Account successfully deleted.")

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
            await ctx.send("You aren't registered.", hidden=True)


    @cog_ext.cog_slash(description="View your current build", guild_ids=main.guild_ids)
    async def build(self, ctx):
        query = {'DID': str(ctx.author.id)}
        d = db.queryUser(query)
        card = db.queryCard({'NAME':str(d['CARD'])})
        title = db.queryTitle({'TITLE': str(d['TITLE'])})
        arm = db.queryArm({'ARM': str(d['ARM'])})
        user_info = db.queryUser(query)
        vault = db.queryVault({'DID': d['DID']})
        if card:
            try:
                durability = ""
                base_arm_names = ['Reborn Stock', 'Stock', 'Deadgun', 'Glaive', 'Kings Glaive', 'Legendary Weapon']
                for a in vault['ARMS']:
                    if a['ARM'] == str(d['ARM']) and a['ARM'] in base_arm_names:
                        durability = f""
                    elif a['ARM'] == str(d['ARM']) and a['ARM'] not in base_arm_names:
                        durability = f"⚒️ {a['DUR']}"
                   
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
                performance_mode = d['PERFORMANCE']
                card_tier = card['TIER']
                
        
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
                    traitmessage = f"{mytrait['EFFECT']}: {mytrait['TRAIT']}"

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
                    bond_message = "🌟"
                
                if lvl == 10:
                    lvl_message = "⭐"

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
                titleicon="⚠️"
                licon = "🔱"
                if card_lvl == 200:
                    licon ="⚜️"
                titlemessage = f"{titleicon} {title_name} ~ INEFFECTIVE"
                warningmessage = f"Use {o_show} or Unbound Titles on this card"
                if o_title_universe == "Unbound":
                    titled =True
                    titleicon = "🎗️"
                    titlemessage = f"🎗️ {title_name}: {title_passive_type} {title_passive_value}{title_enhancer_suffix_mapping[title_passive_type]}"
                    warningmessage= f""
                elif o_title_universe == o_show:
                    titled =True
                    titleicon = "🎗️"
                    titlemessage = f"🎗️ {title_name}: {title_passive_type} {title_passive_value}{title_enhancer_suffix_mapping[title_passive_type]}"
                    warningmessage= f""
                cardtitle = {'TITLE': title_name}

                #<:PCG:769471288083218432>
                if performance_mode:
                    embedVar = discord.Embed(title=f"{licon}{card_lvl} {o_card}".format(self), description=textwrap.dedent(f"""\
                    :mahjong: **{card_tier}**
                    ❤️ **{o_max_health}**
                    🗡️ **{o_attack}**
                    🛡️ **{o_defense}**
                    🏃 **{o_speed}**

                    **{titlemessage}**
                    🦾 **{arm_name}: {arm_passive_type} {arm_passive_value}{enhancer_suffix_mapping[arm_passive_type]} {durability}**
                    🧬 **{active_pet['NAME']}: {active_pet['TYPE']}: {pet_ability_power}{enhancer_suffix_mapping[active_pet['TYPE']]} | Bond {bond} {bond_message} / Level {lvl} {lvl_message}**
                    🩸 **{passive_name}:** {passive_type} {passive_num}{passive_enhancer_suffix_mapping[passive_type]}                
                    
                    💥 **{move1}:** {move1ap}
                    ☄️ **{move2}:** {move2ap}
                    🏵️ **{move3}:** {move3ap}
                    🦠 **{move4}:** {move4enh} {move4ap}{enhancer_suffix_mapping[move4enh]}

                    ♾️ {traitmessage}
                    """),colour=000000)
                    embedVar.set_image(url="attachment://image.png")
                    if card_lvl != 500:
                        embedVar.set_footer(text=f"EXP Until Next Level: {150 - card_exp}\nRebirth Buff: +{rebirthBonus}\n{warningmessage}")
                    else:
                        embedVar.set_footer(text=f"Max Level\nRebirth Buff: +{rebirthBonus}\n{warningmessage}")
                    embedVar.set_author(name=f"{ctx.author}", icon_url=user_info['AVATAR'])
                    
                    await ctx.send(embed=embedVar)
                    return
                   
                else:
                    card_file = showcard(card, o_max_health, o_health, o_max_stamina, o_stamina, resolved, cardtitle, focused, o_attack, o_defense, turn, move1ap, move2ap, move3ap, move4ap, move4enh, card_lvl, None)

                    embedVar = discord.Embed(title=f"".format(self), colour=000000)
                    embedVar.set_image(url="attachment://image.png")
                    embedVar.set_author(name=textwrap.dedent(f"""\
                    {titlemessage}
                    🦾 {arm_name}: {arm_passive_type} {arm_passive_value}{enhancer_suffix_mapping[arm_passive_type]} {durability}
                    🧬 {active_pet['NAME']}: {active_pet['TYPE']}: {pet_ability_power}{enhancer_suffix_mapping[active_pet['TYPE']]} | Bond {bond} {bond_message} / Level {lvl} {lvl_message}
                    🩸 {passive_name}: {passive_type} {passive_num}{passive_enhancer_suffix_mapping[passive_type]}                
                    🏃 {o_speed}
                    """))
                    if card_lvl != 500:
                        embedVar.set_footer(text=f"EXP Until Next Level: {150 - card_exp}\nRebirth Buff: +{rebirthBonus}\n♾️ {traitmessage}\n{warningmessage}")
                    else:
                        embedVar.set_footer(text=f"Max Level")
                    
                    await ctx.send(file=card_file, embed=embedVar)
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
                await ctx.send("There's an issue with your build. Check with support.", hidden=True)
                return
        else:
            await ctx.send(m.USER_NOT_REGISTERED, hidden=True)


    @cog_ext.cog_slash(description="Check all your cards", guild_ids=main.guild_ids)
    async def cards(self, ctx):
        await ctx.defer()
        query = {'DID': str(ctx.author.id)}
        d = db.queryUser(query)
        vault = db.queryVault({'DID': d['DID']})
        try: 
            if vault:
                name = d['DISNAME'].split("#",1)[0]
                avatar = d['AVATAR']
                card_levels = vault['CARD_LEVELS']
                current_gems = []
                for gems in vault['GEMS']:
                    current_gems.append(gems['UNIVERSE'])
                balance = vault['BALANCE']
                cards_list = vault['CARDS']
                total_cards = len(cards_list)
                current_card = d['CARD']
                cards=[]
                icon = ":coin:"
                if balance >= 150000:
                    icon = ":money_with_wings:"
                elif balance >=100000:
                    icon = ":moneybag:"
                elif balance >= 50000:
                    icon = ":dollar:"
                
                embed_list = []

                for card in cards_list:
                    index = cards_list.index(card)
                    resp = db.queryCard({"NAME": str(card)})
                    card_tier = 0
                    lvl = ""
                    tier = ""
                    speed = 0
                    card_tier = f":mahjong: {resp['TIER']}"
                    card_available = resp['AVAILABLE']
                    card_exclusive = resp['EXCLUSIVE']
                    card_collection = resp['HAS_COLLECTION']
                    show_img = db.queryUniverse({'TITLE': resp['UNIVERSE']})['PATH']
                    o_show = resp['UNIVERSE']
                    icon = ":flower_playing_cards:"
                    if card_available and card_exclusive:
                        icon = ":fire:"
                    elif card_available == False and card_exclusive ==False:
                        if card_collection:
                            icon =":sparkles:"
                        else:
                            icon = ":japanese_ogre:"
                    card_lvl = 0
                    card_exp = 0
                    card_lvl_attack_buff = 0
                    card_lvl_defense_buff = 0
                    card_lvl_ap_buff = 0
                    card_lvl_hlt_buff = 0

                    for cl in card_levels:
                        if card == cl['CARD']:
                            licon = "🔱"
                            if cl['LVL'] == 200:
                                licon ="⚜️"
                            lvl = f"{licon} **{cl['LVL']}**"
                            card_lvl = cl['LVL']
                            card_exp = cl['EXP']
                            card_lvl_ap_buff = cl['AP']
                            card_lvl_attack_buff = cl['ATK']
                            card_lvl_defense_buff = cl['DEF']
                            card_lvl_hlt_buff = cl['HLT']
                            
                    
                    o_passive = resp['PASS'][0] 
                    o_moveset = resp['MOVESET']
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

                    passive_name = list(o_passive.keys())[0]
                    passive_num = list(o_passive.values())[0]
                    passive_type = list(o_passive.values())[1]

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
                        traitmessage = f"**{mytrait['EFFECT']}:** {mytrait['TRAIT']}"


                    embedVar = discord.Embed(title= f"{resp['NAME']}", description=textwrap.dedent(f"""
                    {icon} **[{index}]** 
                    {card_tier}: {lvl}
                    :heart: **{resp['HLT']}** :dagger: **{resp['ATK']}** :shield: **{resp['DEF']}** 🏃 **{resp['SPD']}**
                    
                    💥 **{move1}:** {move1ap}
                    ☄️ **{move2}:** {move2ap}
                    🏵️ **{move3}:** {move3ap}
                    🦠 **{move4}:** {move4enh} {move4ap}{enhancer_suffix_mapping[move4enh]}

                    🩸 **{passive_name}:** {passive_type} {passive_num}{passive_enhancer_suffix_mapping[passive_type]}
                    ♾️ {traitmessage}
                    """), colour=0x7289da)
                    embedVar.set_thumbnail(url=show_img)
                    embedVar.set_footer(text=f"/enhancers - 🩸 Enhancer Menu")
                    embed_list.append(embedVar)

                buttons = [
                    manage_components.create_button(style=3, label="Equip", custom_id="Equip"),
                    manage_components.create_button(style=1, label="Resell", custom_id="Resell"),
                    manage_components.create_button(style=1, label="Dismantle", custom_id="Dismantle"),
                    manage_components.create_button(style=1, label="Trade", custom_id="Trade"),
                    manage_components.create_button(style=2, label="Exit", custom_id="Exit")
                ]
                custom_action_row = manage_components.create_actionrow(*buttons)
                # custom_button = manage_components.create_button(style=3, label="Equip")

                async def custom_function(self, button_ctx):
                    if button_ctx.author == ctx.author:
                        updated_vault = db.queryVault({'DID': d['DID']})
                        sell_price = 0
                        selected_card = str(button_ctx.origin_message.embeds[0].title)
                        if button_ctx.custom_id == "Equip":
                            if selected_card in updated_vault['CARDS']:
                                selected_universe = custom_function
                                custom_function.selected_universe = selected_card
                                user_query = {'DID': str(ctx.author.id)}
                                response = db.updateUserNoFilter(user_query, {'$set': {'CARD': selected_card}})
                                await button_ctx.send(f":flower_playing_cards: **{selected_card}** equipped.")
                                self.stop = True
                            else:
                                await button_ctx.send(f"**{selected_card}** is no longer in your vault.")
                        
                        elif button_ctx.custom_id == "Resell":
                            card_data = db.queryCard({'NAME': selected_card})
                            card_name = card_data['NAME']
                            sell_price = sell_price + (card_data['PRICE'] * .07)
                            if card_name == current_card:
                                await button_ctx.send("You cannot resell equipped cards.")
                            elif card_name in updated_vault['CARDS']:
                                sell_buttons = [
                                    manage_components.create_button(
                                        style=ButtonStyle.green,
                                        label="Yes",
                                        custom_id="yes"
                                    ),
                                    manage_components.create_button(
                                        style=ButtonStyle.blue,
                                        label="No",
                                        custom_id="no"
                                    )
                                ]
                                sell_buttons_action_row = manage_components.create_actionrow(*sell_buttons)
                                await button_ctx.send(f"Are you sure you want to sell **{card_name}** for :coin:{round(sell_price)}?", components=[sell_buttons_action_row])
                                
                                def check(button_ctx):
                                    return button_ctx.author == ctx.author

                                
                                try:
                                    button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[sell_buttons_action_row], timeout=120, check=check)

                                    if button_ctx.custom_id == "no":
                                        await button_ctx.send("Sell cancelled. ")
                                        self.stop = True
                                    if button_ctx.custom_id == "yes":
                                        db.updateVaultNoFilter({'DID': str(ctx.author.id)},{'$pull':{'CARDS': card_name}})
                                        await main.bless(sell_price, ctx.author.id)
                                        await button_ctx.send("Sold.")
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
                                        'PLAYER': str(ctx.author),
                                        'type': type(ex).__name__,
                                        'message': str(ex),
                                        'trace': trace
                                    }))
                                    await ctx.send("There's an issue with selling one or all of your items.")
                                    return
                            else:
                                await button_ctx.send(f"**{card_name}** is no longer in your vault.")
                        
                        elif button_ctx.custom_id == "Dismantle":
                            card_data = db.queryCard({'NAME': selected_card})
                            card_tier =  card_data['TIER']
                            card_health = card_data['HLT']
                            card_name = card_data['NAME']
                            selected_universe = card_data['UNIVERSE']
                            dismantle_amount = (35000 * card_tier) + card_health
                            if card_name == current_card:
                                await button_ctx.send("You cannot dismantle equipped cards.")
                            elif card_name in updated_vault['CARDS']:
                                dismantle_buttons = [
                                    manage_components.create_button(
                                        style=ButtonStyle.green,
                                        label="Yes",
                                        custom_id="yes"
                                    ),
                                    manage_components.create_button(
                                        style=ButtonStyle.blue,
                                        label="No",
                                        custom_id="no"
                                    )
                                ]
                                dismantle_buttons_action_row = manage_components.create_actionrow(*dismantle_buttons)
                                await button_ctx.send(f"Are you sure you want to dismantle **{card_name}** for 💎 {round(dismantle_amount)}?", components=[dismantle_buttons_action_row])
                                
                                def check(button_ctx):
                                    return button_ctx.author == ctx.author

                                
                                try:
                                    button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[dismantle_buttons_action_row], timeout=120, check=check)

                                    if button_ctx.custom_id == "no":
                                        await button_ctx.send("Dismantle cancelled. ")
                                        self.stop = True
                                    if button_ctx.custom_id == "yes":
                                        if selected_universe in current_gems:
                                            query = {'DID': str(ctx.author.id)}
                                            update_query = {'$inc': {'GEMS.$[type].' + "GEMS": dismantle_amount}}
                                            filter_query = [{'type.' + "UNIVERSE": selected_universe}]
                                            response = db.updateVault(query, update_query, filter_query)
                                        else:
                                            response = db.updateVaultNoFilter({'DID': str(ctx.author.id)},{'$addToSet':{'GEMS': {'UNIVERSE': selected_universe, 'GEMS': dismantle_amount, 'UNIVERSE_HEART': False, 'UNIVERSE_SOUL': False}}})

                                        db.updateVaultNoFilter({'DID': str(ctx.author.id)},{'$pull':{'CARDS': card_name}})
                                        #await main.bless(sell_price, ctx.author.id)
                                        await button_ctx.send("Dismantled.")
                                        self.stop = True
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
                                        'PLAYER': str(ctx.author),
                                        'type': type(ex).__name__,
                                        'message': str(ex),
                                        'trace': trace
                                    }))
                                    await ctx.send("There's an issue with selling one or all of your items.")
                                    return
                            else:
                                await button_ctx.send(f"**{card_name}** is no longer in your vault.")

                        elif button_ctx.custom_id == "Trade":
                            
                            card_data = db.queryCard({'NAME' : selected_card})
                            card_name= card_data['NAME']
                            sell_price = card_data['PRICE'] * .10
                            mtrade = db.queryTrade({'MDID' : str(ctx.author.id), 'OPEN' : True})
                            mvalidation=False
                            bvalidation=False
                            item_already_in_trade=False
                            if card_name == current_card:
                                await button_ctx.send("You cannot trade equipped cards.")
                            else:
                                if mtrade:
                                    if selected_card in mtrade['MCARDS']:
                                        await ctx.send(f"{ctx.author.mention} card already in **Trade**")
                                        item_already_in_trade=True
                                    mvalidation=True
                                else:
                                    btrade = db.queryTrade({'BDID' : str(ctx.author.id), 'OPEN' : True})
                                    if btrade:
                                        if selected_card in btrade['BCARDS']:
                                            await ctx.send(f"{ctx.author.mention} card already in **Trade**")
                                            item_already_in_trade=True
                                        bvalidation=True
                                    else:
                                        await ctx.send(f"{ctx.author.mention} use **/trade** to open a **trade**")
                                        return
                                if item_already_in_trade:
                                    trade_buttons = [
                                        manage_components.create_button(
                                            style=ButtonStyle.green,
                                            label="Yes",
                                            custom_id="yes"
                                        ),
                                        manage_components.create_button(
                                            style=ButtonStyle.blue,
                                            label="No",
                                            custom_id="no"
                                        )
                                    ]
                                    trade_buttons_action_row = manage_components.create_actionrow(*trade_buttons)
                                    await button_ctx.send(f"Woudl you like to remove **{selected_card}** from the **Trade**?", components=[trade_buttons_action_row])
                                    
                                    def check(button_ctx):
                                        return button_ctx.author == ctx.author

                                    
                                    try:
                                        button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[trade_buttons_action_row], timeout=120, check=check)
                                        if button_ctx.custom_id == "no":
                                                await button_ctx.send("Happy Trading")
                                                self.stop = True
                                        if button_ctx.custom_id == "yes":
                                            neg_sell_price = 0 - abs(int(sell_price))
                                            if mvalidation:
                                                trade_query = {'MDID' : str(button_ctx.author.id), 'BDID' : str(mtrade['BDID']), 'OPEN' : True}
                                                update_query = {"$pull" : {'MCARDS': selected_card}, "$inc" : {'TAX' : int(neg_sell_price)}}
                                                resp = db.updateTrade(trade_query, update_query)
                                                await button_ctx.send("Returned.")
                                                self.stop = True
                                            elif bvalidation:
                                                trade_query = {'MDID' : str(btrade['MDID']),'BDID' : str(button_ctx.author.id), 'OPEN' : True}
                                                update_query = {"$pull" : {'BCARDS': selected_card}, "$inc" : {'TAX' : int(neg_sell_price)}}
                                                resp = db.updateTrade(trade_query, update_query)
                                                await button_ctx.send("Returned.")
                                                self.stop = True
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
                                            'PLAYER': str(ctx.author),
                                            'type': type(ex).__name__,
                                            'message': str(ex),
                                            'trace': trace
                                        }))
                                        await ctx.send("There's an issue with trading one or all of your items.")
                                        return   
                                elif mvalidation == True or bvalidation ==True:    #If user is valid
                                    sell_price = card_data['PRICE'] * .10
                                    trade_buttons = [
                                        manage_components.create_button(
                                            style=ButtonStyle.green,
                                            label="Yes",
                                            custom_id="yes"
                                        ),
                                        manage_components.create_button(
                                            style=ButtonStyle.blue,
                                            label="No",
                                            custom_id="no"
                                        )
                                    ]
                                    trade_buttons_action_row = manage_components.create_actionrow(*trade_buttons)
                                    await button_ctx.send(f"Are you sure you want to trade **{selected_card}**", components=[trade_buttons_action_row])
                                    try:
                                        button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[trade_buttons_action_row], timeout=120)
                                        if button_ctx.custom_id == "no":
                                                await button_ctx.send("Not this time. ")
                                                self.stop = True
                                        if button_ctx.custom_id == "yes":
                                            if mvalidation:
                                                trade_query = {'MDID' : str(ctx.author.id), 'BDID' : str(mtrade['BDID']), 'OPEN' : True}
                                                update_query = {"$push" : {'MCARDS': selected_card}, "$inc" : {'TAX' : int(sell_price)}}
                                                resp = db.updateTrade(trade_query, update_query)
                                                await button_ctx.send("Traded.")
                                                self.stop = True
                                            elif bvalidation:
                                                trade_query = {'MDID' : str(btrade['MDID']),'BDID' : str(ctx.author.id), 'OPEN' : True}
                                                update_query = {"$push" : {'BCARDS': selected_card}, "$inc" : {'TAX' : int(sell_price)}}
                                                resp = db.updateTrade(trade_query, update_query)
                                                await button_ctx.send("Traded.")
                                                self.stop = True
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
                                            'PLAYER': str(ctx.author),
                                            'type': type(ex).__name__,
                                            'message': str(ex),
                                            'trace': trace
                                        }))
                                        await ctx.send("There's an issue with trading one or all of your items.")
                                        return   
                            
                        elif button_ctx.custom_id == "Exit":
                            await button_ctx.defer(ignore=True)
                            self.stop = True
                    else:
                        await ctx.send("This is not your card list.")
                await Paginator(bot=self.bot, disableAfterTimeout=True, ctx=ctx, pages=embed_list, timeout=60, customActionRow=[
                    custom_action_row,
                    custom_function,
                ]).run()
            else:
                newVault = db.createVault({'OWNER': d['DISNAME'], 'DID' : d['DID']})
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
            await ctx.send("There's an issue with loading your cards. Check with support.", hidden=True)
            return


    @cog_ext.cog_slash(description="Check all your Titles", guild_ids=main.guild_ids)
    async def titles(self, ctx):
        await ctx.defer()
        query = {'DID': str(ctx.author.id)}
        d = db.queryUser(query)
        vault = db.queryVault({'DID': d['DID']})
        if vault:
            try:
                name = d['DISNAME'].split("#",1)[0]
                avatar = d['AVATAR']
                balance = vault['BALANCE']
                current_title = d['TITLE']
                titles_list = vault['TITLES']
                total_titles = len(titles_list)
                titles=[]
                current_gems = []
                for gems in vault['GEMS']:
                    current_gems.append(gems['UNIVERSE'])
                icon = ":coin:"
                if balance >= 150000:
                    icon = ":money_with_wings:"
                elif balance >=100000:
                    icon = ":moneybag:"
                elif balance >= 50000:
                    icon = ":dollar:"


                embed_list = []
                for title in titles_list:
                    index = titles_list.index(title)
                    resp = db.queryTitle({"TITLE": str(title)})
                    title_passive = resp['ABILITIES'][0]
                    title_passive_type = list(title_passive.keys())[0]
                    title_passive_value = list(title_passive.values())[0]
                    title_available = resp['AVAILABLE']
                    title_exclusive = resp['EXCLUSIVE']
                    icon = "🎗️"
                    if title_available and title_exclusive:
                        icon = ":fire:"
                    elif title_available == False and title_exclusive ==False:
                        icon = ":japanese_ogre:"
                    
                    embedVar = discord.Embed(title= f"{resp['TITLE']}", description=textwrap.dedent(f"""
                    {icon} **[{index}]**
                    :microbe: **{title_passive_type}:** {title_passive_value}
                    :earth_africa: **Universe:** {resp['UNIVERSE']}"""), 
                    colour=0x7289da)
                    embedVar.set_thumbnail(url=avatar)
                    embedVar.set_footer(text=f"{title_passive_type}: {title_enhancer_mapping[title_passive_type]}")
                    embed_list.append(embedVar)
                
                buttons = [
                    manage_components.create_button(style=3, label="Equip", custom_id="Equip"),
                    manage_components.create_button(style=1, label="Resell", custom_id="Resell"),
                    manage_components.create_button(style=1, label="Dismantle", custom_id="Dismantle"),
                    manage_components.create_button(style=1, label="Trade", custom_id="Trade"),
                    manage_components.create_button(style=2, label="Exit", custom_id="Exit")
                ]
                custom_action_row = manage_components.create_actionrow(*buttons)

                async def custom_function(self, button_ctx):
                    if button_ctx.author == ctx.author:
                        updated_vault = db.queryVault({'DID': d['DID']})
                        sell_price = 0
                        selected_title = str(button_ctx.origin_message.embeds[0].title)
                        if button_ctx.custom_id == "Equip":
                            if selected_title in updated_vault['TITLES']:
                                selected_universe = custom_function
                                custom_function.selected_universe = selected_title
                                user_query = {'DID': str(ctx.author.id)}
                                response = db.updateUserNoFilter(user_query, {'$set': {'TITLE': selected_title}})
                                await button_ctx.send(f"🎗️ **{selected_title}** equipped.")
                                self.stop = True
                            else:
                                await button_ctx.send(f"**{selected_title}** is no longer in your vault.")                           
                        
                        elif button_ctx.custom_id == "Resell":
                            title_data = db.queryTitle({'TITLE': selected_title})
                            title_name = title_data['TITLE']
                            sell_price = sell_price + (title_data['PRICE'] * .10)
                            if title_name == current_title:
                                await button_ctx.send("You cannot resell equipped titles.")
                            elif title_name in updated_vault['TITLES']:
                                sell_buttons = [
                                    manage_components.create_button(
                                        style=ButtonStyle.green,
                                        label="Yes",
                                        custom_id="yes"
                                    ),
                                    manage_components.create_button(
                                        style=ButtonStyle.blue,
                                        label="No",
                                        custom_id="no"
                                    )
                                ]
                                sell_buttons_action_row = manage_components.create_actionrow(*sell_buttons)
                                await button_ctx.send(f"Are you sure you want to sell **{title_name}** for :coin:{round(sell_price)}?", components=[sell_buttons_action_row])
                                
                                def check(button_ctx):
                                    return button_ctx.author == ctx.author

                                
                                try:
                                    button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[sell_buttons_action_row], timeout=120, check=check)

                                    if button_ctx.custom_id == "no":
                                        await button_ctx.send("Sell cancelled. Please press the Exit button if you are done reselling titles.")
                                        self.stop = True
                                    if button_ctx.custom_id == "yes":
                                        db.updateVaultNoFilter({'DID': str(ctx.author.id)},{'$pull':{'TITLES': title_name}})
                                        await main.bless(sell_price, ctx.author.id)
                                        await button_ctx.send("Sold.")
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
                                        'PLAYER': str(ctx.author),
                                        'type': type(ex).__name__,
                                        'message': str(ex),
                                        'trace': trace
                                    }))
                                    await ctx.send("There's an issue with selling one or all of your items.")
                                    return
                            else:
                                await button_ctx.send(f"**{title_name}** is no longer in your vault.")
                        
                        elif button_ctx.custom_id == "Dismantle":
                            title_data = db.queryTitle({'TITLE': selected_title})
                            title_name = title_data['TITLE']
                            selected_universe = title_data['UNIVERSE']
                            dismantle_amount = 1000
                            if title_name == current_title:
                                await button_ctx.send("You cannot resell equipped titles.")
                            elif title_name in updated_vault['TITLES']:
                                dismantle_buttons = [
                                    manage_components.create_button(
                                        style=ButtonStyle.green,
                                        label="Yes",
                                        custom_id="yes"
                                    ),
                                    manage_components.create_button(
                                        style=ButtonStyle.blue,
                                        label="No",
                                        custom_id="no"
                                    )
                                ]
                                dismantle_buttons_action_row = manage_components.create_actionrow(*dismantle_buttons)
                                await button_ctx.send(f"Are you sure you want to dismantle **{title_name}** for 💎 {round(dismantle_amount)}?", components=[dismantle_buttons_action_row])
                                
                                def check(button_ctx):
                                    return button_ctx.author == ctx.author

                                
                                try:
                                    button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[dismantle_buttons_action_row], timeout=120, check=check)

                                    if button_ctx.custom_id == "no":
                                        await button_ctx.send("Dismantle cancelled. ")
                                        self.stop = True
                                    if button_ctx.custom_id == "yes":
                                        if selected_universe in current_gems:
                                            query = {'DID': str(ctx.author.id)}
                                            update_query = {'$inc': {'GEMS.$[type].' + "GEMS": dismantle_amount}}
                                            filter_query = [{'type.' + "UNIVERSE": selected_universe}]
                                            response = db.updateVault(query, update_query, filter_query)
                                        else:
                                            response = db.updateVaultNoFilter({'DID': str(ctx.author.id)},{'$addToSet':{'GEMS': {'UNIVERSE': selected_universe, 'GEMS': dismantle_amount, 'UNIVERSE_HEART': False, 'UNIVERSE_SOUL': False}}})

                                        db.updateVaultNoFilter({'DID': str(ctx.author.id)},{'$pull':{'TITLES': title_name}})
                                        await main.bless(sell_price, ctx.author.id)
                                        await button_ctx.send("Dismantled.")
                                        self.stop = True
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
                                        'PLAYER': str(ctx.author),
                                        'type': type(ex).__name__,
                                        'message': str(ex),
                                        'trace': trace
                                    }))
                                    await ctx.send("There's an issue with selling one or all of your items.")
                                    return
                            else:
                                await button_ctx.send(f"**{title_name}** is no longer in your vault.")

                        elif button_ctx.custom_id == "Trade":
                            title_data = db.queryTitle({'TITLE' : selected_title})
                            title_name = title_data['TITLE']
                            if title_name == current_title:
                                await button_ctx.send("You cannot trade equipped titles.")
                                return
                            sell = title_data['PRICE'] * .10
                            mtrade = db.queryTrade({'MDID' : str(ctx.author.id), 'OPEN' : True})
                            mvalidation=False
                            bvalidation=False
                            item_already_in_trade=False
                            if mtrade:
                                if selected_title in mtrade['MTITLES']:
                                    await ctx.send(f"{ctx.author.mention} title already in **Trade**")
                                    item_already_in_trade=True
                                mvalidation=True
                            else:
                                btrade = db.queryTrade({'BDID' : str(ctx.author.id), 'OPEN' : True})
                                if btrade:
                                    if selected_title in btrade['BTITLES']:
                                        await ctx.send(f"{ctx.author.mention} title already in **Trade**")
                                        item_already_in_trade=True
                                    bvalidation=True
                                else:
                                    await ctx.send(f"{ctx.author.mention} use **/trade** to open a **trade**")
                                    return
                            if item_already_in_trade:
                                trade_buttons = [
                                    manage_components.create_button(
                                        style=ButtonStyle.green,
                                        label="Yes",
                                        custom_id="yes"
                                    ),
                                    manage_components.create_button(
                                        style=ButtonStyle.blue,
                                        label="No",
                                        custom_id="no"
                                    )
                                ]
                                trade_buttons_action_row = manage_components.create_actionrow(*trade_buttons)
                                await button_ctx.send(f"Woudl you like to remove **{selected_title}** from the **Trade**?", components=[trade_buttons_action_row])
                                
                                def check(button_ctx):
                                    return button_ctx.author == ctx.author

                                
                                try:
                                    button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[trade_buttons_action_row], timeout=120, check=check)
                                    if button_ctx.custom_id == "no":
                                            await button_ctx.send("Happy Trading")
                                            self.stop = True
                                    if button_ctx.custom_id == "yes":
                                        neg_sell_price = 0 - abs(int(sell_price))
                                        if mvalidation:
                                            trade_query = {'MDID' : str(button_ctx.author.id), 'BDID' : str(mtrade['BDID']), 'OPEN' : True}
                                            update_query = {"$pull" : {'MTITLES': selected_title}, "$inc" : {'TAX' : int(neg_sell_price)}}
                                            resp = db.updateTrade(trade_query, update_query)
                                            await button_ctx.send("Returned.")
                                            self.stop = True
                                        elif bvalidation:
                                            trade_query = {'MDID' : str(btrade['MDID']),'BDID' : str(button_ctx.author.id), 'OPEN' : True}
                                            update_query = {"$pull" : {'BTITLES': selected_title}, "$inc" : {'TAX' : int(neg_sell_price)}}
                                            resp = db.updateTrade(trade_query, update_query)
                                            await button_ctx.send("Returned.")
                                            self.stop = True
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
                                        'PLAYER': str(ctx.author),
                                        'type': type(ex).__name__,
                                        'message': str(ex),
                                        'trace': trace
                                    }))
                                    await ctx.send("There's an issue with trading one or all of your items.")
                                    return   
                            elif mvalidation == True or bvalidation ==True:    #If user is valid
                                sell_price = title_data['PRICE'] * .10
                                trade_buttons = [
                                    manage_components.create_button(
                                        style=ButtonStyle.green,
                                        label="Yes",
                                        custom_id="yes"
                                    ),
                                    manage_components.create_button(
                                        style=ButtonStyle.blue,
                                        label="No",
                                        custom_id="no"
                                    )
                                ]
                                trade_buttons_action_row = manage_components.create_actionrow(*trade_buttons)
                                await button_ctx.send(f"Are you sure you want to trade **{selected_title}**", components=[trade_buttons_action_row])
                                try:
                                    button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[trade_buttons_action_row], timeout=120)
                                    if button_ctx.custom_id == "no":
                                            await button_ctx.send("Not this time. ")
                                            self.stop = True
                                    if button_ctx.custom_id == "yes":
                                        if mvalidation:
                                            trade_query = {'MDID' : str(ctx.author.id), 'BDID' : str(mtrade['BDID']), 'OPEN' : True}
                                            update_query = {"$push" : {'MTITLES': selected_title}, "$inc" : {'TAX' : int(sell_price)}}
                                            resp = db.updateTrade(trade_query, update_query)
                                            await button_ctx.send("Traded.")
                                            self.stop = True
                                        elif bvalidation:
                                            trade_query = {'MDID' : str(btrade['MDID']),'BDID' : str(ctx.author.id), 'OPEN' : True}
                                            update_query = {"$push" : {'BTITLES': selected_title}, "$inc" : {'TAX' : int(sell_price)}}
                                            resp = db.updateTrade(trade_query, update_query)
                                            await button_ctx.send("Traded.")
                                            self.stop = True
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
                                        'PLAYER': str(ctx.author),
                                        'type': type(ex).__name__,
                                        'message': str(ex),
                                        'trace': trace
                                    }))
                                    await ctx.send("There's an issue with trading one or all of your items.")
                                    return   
                                                        
                        elif button_ctx.custom_id == "Exit":
                            await button_ctx.defer(ignore=True)
                            self.stop = True
                    else:
                        await ctx.send("This is not your Title list.")


                await Paginator(bot=self.bot, ctx=ctx, pages=embed_list, timeout=60, customActionRow=[
                    custom_action_row,
                    custom_function,
                ]).run()
      
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
                await ctx.send("There's an issue with your Titles list. Check with support.", hidden=True)
                return
        else:
            newVault = db.createVault({'OWNER': d['DISNAME'], 'DID' : d['DID']})


    @cog_ext.cog_slash(description="Check all your Arms", guild_ids=main.guild_ids)
    async def arms(self, ctx):
        await ctx.defer()
        query = {'DID': str(ctx.author.id)}
        d = db.queryUser(query)
        vault = db.queryVault({'DID': d['DID']})
        if vault:
            try:
                name = d['DISNAME'].split("#",1)[0]
                avatar = d['AVATAR']
                current_arm = d['ARM']
                balance = vault['BALANCE']
                arms_list = vault['ARMS']
                total_arms = len(arms_list)

                arms=[]
                current_gems = []
                for gems in vault['GEMS']:
                    current_gems.append(gems['UNIVERSE'])

                icon = ":coin:"
                if balance >= 150000:
                    icon = ":money_with_wings:"
                elif balance >=100000:
                    icon = ":moneybag:"
                elif balance >= 50000:
                    icon = ":dollar:"

                embed_list = []
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
 
                    embedVar = discord.Embed(title= f"{resp['ARM']}", description=textwrap.dedent(f"""
                    {icon} **[{index}]**
                    :microbe: **{arm_passive_type}:** {arm_passive_value}
                    :earth_africa: **Universe:** {resp['UNIVERSE']}
                    ⚒️ {arm['DUR']}
                    """), 
                    colour=0x7289da)
                    embedVar.set_thumbnail(url=avatar)
                    embedVar.set_footer(text=f"{arm_passive_type}: {enhancer_mapping[arm_passive_type]}")
                    embed_list.append(embedVar)
                
                buttons = [
                    manage_components.create_button(style=3, label="Equip", custom_id="Equip"),
                    manage_components.create_button(style=1, label="Resell", custom_id="Resell"),
                    manage_components.create_button(style=1, label="Dismantle", custom_id="Dismantle"),
                    manage_components.create_button(style=1, label="Trade", custom_id="Trade"),
                    manage_components.create_button(style=2, label="Exit", custom_id="Exit")
                ]
                custom_action_row = manage_components.create_actionrow(*buttons)

                async def custom_function(self, button_ctx):
                    if button_ctx.author == ctx.author:
                        u_vault = db.queryVault({'DID': d['DID']})
                        updated_vault = []
                        for arm in u_vault['ARMS']:
                            updated_vault.append(arm['ARM'])
                        
                        sell_price = 0
                        selected_arm = str(button_ctx.origin_message.embeds[0].title)
                        if button_ctx.custom_id == "Equip":
                            if selected_arm in updated_vault:
                                selected_universe = custom_function
                                custom_function.selected_universe = selected_arm
                                user_query = {'DID': str(ctx.author.id)}
                                response = db.updateUserNoFilter(user_query, {'$set': {'ARM': selected_arm}})
                                await button_ctx.send(f":mechanical_arm: **{selected_arm}** equipped.")
                                self.stop = True
                            else:
                                await button_ctx.send(f"**{selected_arm}** is no longer in your vault.")
                        
                        elif button_ctx.custom_id == "Resell":
                            arm_data = db.queryArm({'ARM': selected_arm})
                            arm_name = arm_data['ARM']
                            sell_price = sell_price + (arm_data['PRICE'] * .07)
                            if arm_name == current_arm:
                                await button_ctx.send("You cannot resell equipped arms.")
                            elif arm_name in updated_vault:
                                sell_buttons = [
                                    manage_components.create_button(
                                        style=ButtonStyle.green,
                                        label="Yes",
                                        custom_id="yes"
                                    ),
                                    manage_components.create_button(
                                        style=ButtonStyle.blue,
                                        label="No",
                                        custom_id="no"
                                    )
                                ]
                                sell_buttons_action_row = manage_components.create_actionrow(*sell_buttons)
                                await button_ctx.send(f"Are you sure you want to sell **{arm_name}** for :coin:{round(sell_price)}?", components=[sell_buttons_action_row])
                                
                                def check(button_ctx):
                                    return button_ctx.author == ctx.author

                                
                                try:
                                    button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[sell_buttons_action_row], timeout=120, check=check)

                                    if button_ctx.custom_id == "no":
                                        await button_ctx.send("Sell cancelled. Please press the Exit button if you are done reselling titles.")
                                        self.stop = True
                                    if button_ctx.custom_id == "yes":
                                        db.updateVaultNoFilter({'DID': str(ctx.author.id)},{'$pull':{'ARMS': {'ARM': str(arm_name)}}})
                                        await main.bless(sell_price, ctx.author.id)
                                        await button_ctx.send("Sold.")
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
                                        'PLAYER': str(ctx.author),
                                        'type': type(ex).__name__,
                                        'message': str(ex),
                                        'trace': trace
                                    }))
                                    await ctx.send("There's an issue with selling one or all of your items.")
                                    return
                            else:
                                await button_ctx.send(f"**{arm_name}** is no longer in your vault.")       
                        
                        elif button_ctx.custom_id == "Dismantle":
                            arm_data = db.queryArm({'ARM': selected_arm})
                            arm_name = arm_data['ARM']
                            selected_universe = arm_data['UNIVERSE']
                            dismantle_amount = 10000
                            if arm_name == current_arm:
                                await button_ctx.send("You cannot dismantle equipped arms.")
                            elif arm_name == "Stock" or arm_name == "Reborn Stock" or arm_name == "Deadgun" or arm_name == "Glaive" or arm_name == "Kings Glaive" or arm_name == "Legendary Weapon":
                                await button_ctx.send("You cannot dismantle Stock arms.")
                            elif arm_name in updated_vault:
                                dismantle_buttons = [
                                    manage_components.create_button(
                                        style=ButtonStyle.green,
                                        label="Yes",
                                        custom_id="yes"
                                    ),
                                    manage_components.create_button(
                                        style=ButtonStyle.blue,
                                        label="No",
                                        custom_id="no"
                                    )
                                ]
                                dismantle_buttons_action_row = manage_components.create_actionrow(*dismantle_buttons)
                                await button_ctx.send(f"Are you sure you want to dismantle **{arm_name}** for 💎 {round(dismantle_amount)}?", components=[dismantle_buttons_action_row])
                                
                                def check(button_ctx):
                                    return button_ctx.author == ctx.author

                                
                                try:
                                    button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[dismantle_buttons_action_row], timeout=120, check=check)

                                    if button_ctx.custom_id == "no":
                                        await button_ctx.send("Dismantle cancelled. ")
                                        self.stop = True
                                    if button_ctx.custom_id == "yes":
                                        if selected_universe in current_gems:
                                            query = {'DID': str(ctx.author.id)}
                                            update_query = {'$inc': {'GEMS.$[type].' + "GEMS": dismantle_amount}}
                                            filter_query = [{'type.' + "UNIVERSE": selected_universe}]
                                            response = db.updateVault(query, update_query, filter_query)
                                        else:
                                            response = db.updateVaultNoFilter({'DID': str(ctx.author.id)},{'$addToSet':{'GEMS': {'UNIVERSE': selected_universe, 'GEMS': dismantle_amount, 'UNIVERSE_HEART': False, 'UNIVERSE_SOUL': False}}})

                                        db.updateVaultNoFilter({'DID': str(ctx.author.id)},{'$pull':{'ARMS': {'ARM': str(arm_name)}}})
                                        await main.bless(sell_price, ctx.author.id)
                                        await button_ctx.send("Dismantled.")
                                        self.stop = True
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
                                        'PLAYER': str(ctx.author),
                                        'type': type(ex).__name__,
                                        'message': str(ex),
                                        'trace': trace
                                    }))
                                    await ctx.send("There's an issue with selling one or all of your items.")
                                    return
                            else:
                                await button_ctx.send(f"**{card_name}** is no longer in your vault.")
    
                        elif button_ctx.custom_id == "Trade":
                            arm_data = db.queryArm({'ARM' : selected_arm})
                            arm_name = arm_data['ARM']
                            if arm_name == current_arm:
                                await button_ctx.send("You cannot trade equipped arms.")
                                return
                            sell_price = arm_data['PRICE'] * .10
                            mtrade = db.queryTrade({'MDID' : str(ctx.author.id), 'OPEN' : True})
                            mvalidation=False
                            bvalidation=False
                            item_already_in_trade=False
                            if mtrade:
                                if selected_arm in mtrade['MARMS']:
                                    await ctx.send(f"{ctx.author.mention} arm already in **Trade**")
                                    item_already_in_trade=True
                                mvalidation=True
                            else:
                                btrade = db.queryTrade({'BDID' : str(ctx.author.id), 'OPEN' : True})
                                if btrade:
                                    if selected_arm in btrade['BARMS']:
                                        await ctx.send(f"{ctx.author.mention} arm already in **Trade**")
                                        item_already_in_trade=True
                                    bvalidation=True
                                else:
                                    await ctx.send(f"{ctx.author.mention} use **/trade** to open a **trade**")
                                    return
                            if item_already_in_trade:
                                trade_buttons = [
                                    manage_components.create_button(
                                        style=ButtonStyle.green,
                                        label="Yes",
                                        custom_id="yes"
                                    ),
                                    manage_components.create_button(
                                        style=ButtonStyle.blue,
                                        label="No",
                                        custom_id="no"
                                    )
                                ]
                                trade_buttons_action_row = manage_components.create_actionrow(*trade_buttons)
                                await button_ctx.send(f"Woudl you like to remove **{selected_arm}** from the **Trade**?", components=[trade_buttons_action_row])
                                
                                def check(button_ctx):
                                    return button_ctx.author == ctx.author

                                
                                try:
                                    button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[trade_buttons_action_row], timeout=120, check=check)
                                    if button_ctx.custom_id == "no":
                                            await button_ctx.send("Happy Trading")
                                            self.stop = True
                                    if button_ctx.custom_id == "yes":
                                        neg_sell_price = 0 - abs(int(sell_price))
                                        if mvalidation:
                                            trade_query = {'MDID' : str(button_ctx.author.id), 'BDID' : str(mtrade['BDID']), 'OPEN' : True}
                                            update_query = {"$pull" : {'MARMS': selected_arm}, "$inc" : {'TAX' : int(neg_sell_price)}}
                                            resp = db.updateTrade(trade_query, update_query)
                                            await button_ctx.send("Returned.")
                                            self.stop = True
                                        elif bvalidation:
                                            trade_query = {'MDID' : str(btrade['MDID']),'BDID' : str(button_ctx.author.id), 'OPEN' : True}
                                            update_query = {"$pull" : {'BARMS': selected_arm}, "$inc" : {'TAX' : int(neg_sell_price)}}
                                            resp = db.updateTrade(trade_query, update_query)
                                            await button_ctx.send("Returned.")
                                            self.stop = True
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
                                        'PLAYER': str(ctx.author),
                                        'type': type(ex).__name__,
                                        'message': str(ex),
                                        'trace': trace
                                    }))
                                    await ctx.send("There's an issue with trading one or all of your items.")
                                    return   
                            elif mvalidation == True or bvalidation ==True:    #If user is valid
                                sell_price = arm_data['PRICE'] * .10
                                trade_buttons = [
                                    manage_components.create_button(
                                        style=ButtonStyle.green,
                                        label="Yes",
                                        custom_id="yes"
                                    ),
                                    manage_components.create_button(
                                        style=ButtonStyle.blue,
                                        label="No",
                                        custom_id="no"
                                    )
                                ]
                                trade_buttons_action_row = manage_components.create_actionrow(*trade_buttons)
                                await button_ctx.send(f"Are you sure you want to trade **{selected_arm}**", components=[trade_buttons_action_row])
                                try:
                                    button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[trade_buttons_action_row], timeout=120)
                                    if button_ctx.custom_id == "no":
                                            await button_ctx.send("Not this time. ")
                                            self.stop = True
                                    if button_ctx.custom_id == "yes":
                                        if mvalidation:
                                            trade_query = {'MDID' : str(ctx.author.id), 'BDID' : str(mtrade['BDID']), 'OPEN' : True}
                                            update_query = {"$push" : {'MARMS': selected_arm}, "$inc" : {'TAX' : int(sell_price)}}
                                            resp = db.updateTrade(trade_query, update_query)
                                            await button_ctx.send("Traded.")
                                            self.stop = True
                                        elif bvalidation:
                                            trade_query = {'MDID' : str(btrade['MDID']),'BDID' : str(ctx.author.id), 'OPEN' : True}
                                            update_query = {"$push" : {'BARMS': selected_arm}, "$inc" : {'TAX' : int(sell_price)}}
                                            resp = db.updateTrade(trade_query, update_query)
                                            await button_ctx.send("Traded.")
                                            self.stop = True
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
                                        'PLAYER': str(ctx.author),
                                        'type': type(ex).__name__,
                                        'message': str(ex),
                                        'trace': trace
                                    }))
                                    await ctx.send("There's an issue with trading one or all of your items.")
                                    return   
                                        
                        elif button_ctx.custom_id == "Exit":
                            await button_ctx.defer(ignore=True)
                            self.stop = True
                    else:
                        await ctx.send("This is not your Arms list.")        

                await Paginator(bot=self.bot, ctx=ctx, pages=embed_list, timeout=60, customActionRow=[
                    custom_action_row,
                    custom_function,
                ]).run()
      
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
                await ctx.send("There's an issue with your Arms list. Check with support.", hidden=True)
                return
        else:
            newVault = db.createVault({'OWNER': d['DISNAME'], 'DID' : d['DID']})


    @cog_ext.cog_slash(description="Check all your Summons", guild_ids=main.guild_ids)
    async def summons(self, ctx):
        await ctx.defer()
        query = {'DID': str(ctx.author.id)}
        d = db.queryUser(query)
        vault = db.queryVault({'DID': d['DID']})
        if vault:
            try:
                name = d['DISNAME'].split("#",1)[0]
                avatar = d['AVATAR']
                balance = vault['BALANCE']
                current_summon = d['PET']
                pets_list = vault['PETS']

                total_pets = len(pets_list)

                pets=[]
                licon = ":coin:"
                if balance >= 150000:
                    licon = ":money_with_wings:"
                elif balance >=100000:
                    licon = ":moneybag:"
                elif balance >= 50000:
                    licon = ":dollar:"
                current_gems = []
                for gems in vault['GEMS']:
                    current_gems.append(gems['UNIVERSE'])
                bond_message = ""
                lvl_message = ""
                embed_list = []
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
                        pet_universe = pet_info['UNIVERSE']
                    icon = "🧬"
                    if pet_available and pet_exclusive:
                        icon = ":fire:"
                    elif pet_available == False and pet_exclusive ==False:
                        icon = ":japanese_ogre:"

                    embedVar = discord.Embed(title= f"{pet['NAME']}", description=textwrap.dedent(f"""
                    {icon}
                    _Bond_ **{pet['BOND']}** {bond_message}
                    _Level_ **{pet['LVL']} {lvl_message}**
                    :small_blue_diamond: **{pet_ability}:** {power}
                    :microbe: **Type:** {pet['TYPE']}"""), 
                    colour=0x7289da)
                    embedVar.set_thumbnail(url=avatar)
                    embedVar.set_footer(text=f"{pet['TYPE']}: {enhancer_mapping[pet['TYPE']]}")
                    embed_list.append(embedVar)
                
                buttons = [
                    manage_components.create_button(style=3, label="Equip", custom_id="Equip"),
                    manage_components.create_button(style=1, label="Trade", custom_id="Trade"),
                    manage_components.create_button(style=1, label="Dismantle", custom_id="Dismantle"),
                    manage_components.create_button(style=2, label="Exit", custom_id="Exit")
                ]
                custom_action_row = manage_components.create_actionrow(*buttons)

                async def custom_function(self, button_ctx):
                    if button_ctx.author == ctx.author:
                        updated_vault = db.queryVault({'DID': d['DID']})
                        sell_price = 0
                        selected_summon = str(button_ctx.origin_message.embeds[0].title)
                        user_query = {'DID': str(ctx.author.id)}
                        
                        if button_ctx.custom_id == "Equip":
                            response = db.updateUserNoFilter(user_query, {'$set': {'PET': str(button_ctx.origin_message.embeds[0].title)}})
                            await button_ctx.send(f"🧬 **{str(button_ctx.origin_message.embeds[0].title)}** equipped.")
                            self.stop = True
                        
                        elif button_ctx.custom_id =="Trade":
                            summon_data = db.queryPet({'PET' : selected_summon})
                            summon_name = summon_data['PET']
                            if summon_name == current_summon:
                                await button_ctx.send("You cannot trade equipped summons.")
                                return
                            sell_price = 5000
                            mtrade = db.queryTrade({'MDID' : str(ctx.author.id), 'OPEN' : True})
                            mvalidation=False
                            bvalidation=False
                            item_already_in_trade=False
                            if mtrade:
                                if selected_summon in mtrade['MSUMMONS']:
                                    await ctx.send(f"{ctx.author.mention} summon already in **Trade**")
                                    item_already_in_trade=True
                                mvalidation=True
                            else:
                                btrade = db.queryTrade({'BDID' : str(ctx.author.id), 'OPEN' : True})
                                if btrade:
                                    if selected_summon in btrade['BSUMMONS']:
                                        await ctx.send(f"{ctx.author.mention} summon already in **Trade**")
                                        item_already_in_trade=True
                                    bvalidation=True
                                else:
                                    await ctx.send(f"{ctx.author.mention} use **/trade** to open a **trade**")
                                    return
                            if item_already_in_trade:
                                trade_buttons = [
                                    manage_components.create_button(
                                        style=ButtonStyle.green,
                                        label="Yes",
                                        custom_id="yes"
                                    ),
                                    manage_components.create_button(
                                        style=ButtonStyle.blue,
                                        label="No",
                                        custom_id="no"
                                    )
                                ]
                                trade_buttons_action_row = manage_components.create_actionrow(*trade_buttons)
                                await button_ctx.send(f"Woudl you like to remove **{selected_summon}** from the **Trade**?", components=[trade_buttons_action_row])
                                
                                def check(button_ctx):
                                    return button_ctx.author == ctx.author
                                                             
                                try:
                                    button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[trade_buttons_action_row], timeout=120, check=check)
                                    if button_ctx.custom_id == "no":
                                            await button_ctx.send("Happy Trading")
                                            self.stop = True
                                    if button_ctx.custom_id == "yes":
                                        neg_sell_price = 0 - abs(int(sell_price))
                                        if mvalidation:
                                            trade_query = {'MDID' : str(button_ctx.author.id), 'BDID' : str(mtrade['BDID']), 'OPEN' : True}
                                            update_query = {"$pull" : {'MSUMMONS': selected_summon}, "$inc" : {'TAX' : int(neg_sell_price)}}
                                            resp = db.updateTrade(trade_query, update_query)
                                            await button_ctx.send("Returned.")
                                            self.stop = True
                                        elif bvalidation:
                                            trade_query = {'MDID' : str(btrade['MDID']),'BDID' : str(button_ctx.author.id), 'OPEN' : True}
                                            update_query = {"$pull" : {'BSUMMONS': selected_summon}, "$inc" : {'TAX' : int(neg_sell_price)}}
                                            resp = db.updateTrade(trade_query, update_query)
                                            await button_ctx.send("Returned.")
                                            self.stop = True
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
                                        'PLAYER': str(ctx.author),
                                        'type': type(ex).__name__,
                                        'message': str(ex),
                                        'trace': trace
                                    }))
                                    await ctx.send("There's an issue with trading one or all of your items.")
                                    return   
                            elif mvalidation == True or bvalidation ==True:    #If user is valid
                                sell_price = 5000
                                trade_buttons = [
                                    manage_components.create_button(
                                        style=ButtonStyle.green,
                                        label="Yes",
                                        custom_id="yes"
                                    ),
                                    manage_components.create_button(
                                        style=ButtonStyle.blue,
                                        label="No",
                                        custom_id="no"
                                    )
                                ]
                                trade_buttons_action_row = manage_components.create_actionrow(*trade_buttons)
                                await button_ctx.send(f"Are you sure you want to trade **{selected_summon}**", components=[trade_buttons_action_row])
                                try:
                                    button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[trade_buttons_action_row], timeout=120)
                                    if button_ctx.custom_id == "no":
                                            await button_ctx.send("Not this time. ")
                                            self.stop = True
                                    if button_ctx.custom_id == "yes":
                                        if mvalidation:
                                            trade_query = {'MDID' : str(ctx.author.id), 'BDID' : str(mtrade['BDID']), 'OPEN' : True}
                                            update_query = {"$push" : {'MSUMMONS': selected_summon}, "$inc" : {'TAX' : int(sell_price)}}
                                            resp = db.updateTrade(trade_query, update_query)
                                            await button_ctx.send("Traded.")
                                            self.stop = True
                                        elif bvalidation:
                                            trade_query = {'MDID' : str(btrade['MDID']),'BDID' : str(ctx.author.id), 'OPEN' : True}
                                            update_query = {"$push" : {'BSUMMONS': selected_summon}, "$inc" : {'TAX' : int(sell_price)}}
                                            resp = db.updateTrade(trade_query, update_query)
                                            await button_ctx.send("Traded.")
                                            self.stop = True
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
                                        'PLAYER': str(ctx.author),
                                        'type': type(ex).__name__,
                                        'message': str(ex),
                                        'trace': trace
                                    }))
                                    await ctx.send("There's an issue with trading one or all of your items.")
                                    return   
                        
                        elif button_ctx.custom_id == "Dismantle":
                            summon_data = db.queryPet({'PET' : selected_summon})
                            summon_name = summon_data['PET']
                            if summon_name == current_summon:
                                await button_ctx.send("You cannot dismanetle equipped summonss.")
                                return
                            dismantle_price = 5000   
                            level = int(pet['LVL'])
                            bond = int(pet['BOND'])
                            dismantle_amount = round((1000* level) + (dismantle_price * bond))
                            dismantle_buttons = [
                                manage_components.create_button(
                                    style=ButtonStyle.green,
                                    label="Yes",
                                    custom_id="yes"
                                ),
                                manage_components.create_button(
                                    style=ButtonStyle.blue,
                                    label="No",
                                    custom_id="no"
                                )
                            ]
                            dismantle_buttons_action_row = manage_components.create_actionrow(*dismantle_buttons)
                            await button_ctx.send(f"Are you sure you want to dismantle **{summon_name}** for 💎 {round(dismantle_amount)}?", components=[dismantle_buttons_action_row])
                            
                            def check(button_ctx):
                                return button_ctx.author == ctx.author

                            
                            try:
                                button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[dismantle_buttons_action_row], timeout=120, check=check)

                                if button_ctx.custom_id == "no":
                                    await button_ctx.send("Dismantle cancelled. ")
                                    self.stop = True
                                if button_ctx.custom_id == "yes":
                                    if pet_universe in current_gems:
                                        query = {'DID': str(ctx.author.id)}
                                        update_query = {'$inc': {'GEMS.$[type].' + "GEMS": dismantle_amount}}
                                        filter_query = [{'type.' + "UNIVERSE": pet_universe}]
                                        response = db.updateVault(query, update_query, filter_query)
                                    else:
                                        response = db.updateVaultNoFilter({'DID': str(ctx.author.id)},{'$addToSet':{'GEMS': {'UNIVERSE': pet_universe, 'GEMS': dismantle_amount, 'UNIVERSE_HEART': False, 'UNIVERSE_SOUL': False}}})
                                    
                                    db.updateVaultNoFilter({'DID': str(ctx.author.id)},{'$pull':{'PETS': {"NAME": str(summon_name)}}})
                                    #await main.bless(sell_price, ctx.author.id)
                                    await button_ctx.send("Dismantled.")
                                    self.stop = True
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
                                await ctx.send(f"ERROR:\nTYPE: {type(ex).__name__}\nMESSAGE: {str(ex)}\nLINE: {trace} ")
                                return
                        elif button_ctx.custom_id =="Exit":
                            await button_ctx.defer(ignore=True)
                            self.stop = True
                    else:
                        await ctx.send("This is not your Summons list.")
                await Paginator(bot=self.bot, ctx=ctx, pages=embed_list, timeout=60, customActionRow=[
                    custom_action_row,
                    custom_function,
                ]).run()

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
                await ctx.send("There's an issue with your Summons list. Check with support.", hidden=True)
                return
        else:
            newVault = db.createVault({'OWNER': d['DISNAME'], 'DID' : d['DID']})


    @cog_ext.cog_slash(description="Check all your destiny lines", guild_ids=main.guild_ids)
    async def destinies(self, ctx):
        await ctx.defer()
        query = {'DID': str(ctx.author.id)}
        d = db.queryUser(query)
        vault = db.queryVault({'DID': d['DID']})
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
            newVault = db.createVault({'OWNER': d['DISNAME'], 'DID' : d['DID']})


    @cog_ext.cog_slash(description="Check all your Quests", guild_ids=main.guild_ids)
    async def quests(self, ctx):
        await ctx.defer()
        query = {'DID': str(ctx.author.id)}
        d = db.queryUser(query)
        vault = db.queryVault({'DID': d['DID']})
        # server = db.queryServer({"GNAME": str(ctx.author.guild)})
        if not vault['QUESTS']:
            await ctx.send("You have no quests available at this time!", hidden=True)
            return
        if vault:
            try:
                guild_buff = guild_buff_update_function(self, d['TEAM'].lower())
                name = d['DISNAME'].split("#",1)[0]
                avatar = d['AVATAR']
                balance = vault['BALANCE']
                quests = vault['QUESTS']
                embed_list = []
                quest_messages = []

                buff_message = ""
                virus_message = ""

                # if server:
                #     server_buff = server['SERVER_BUFF_BOOL']
                #     server_virus = server['SERVER_VIRUS_BOOL']
                #     server_name = server['GNAME']

                #     if not server_buff:
                #         buff_message = f"No active buffs in **{server_name}**"
                #     if not server_virus:
                #         virus_message = f"No active viruses in **{server_name}**"

                for quest in quests:
                    guild_buff_msg = "🔴"
                    if guild_buff:                    
                        if guild_buff['Quest']:
                            guild_buff_msg = "🟢"


                    opponent = db.queryCard({'NAME': quest['OPPONENT']})
                    opponent_universe = db.queryUniverse({'TITLE': opponent['UNIVERSE']})
                    opponent_name = opponent['NAME']
                    opponent_universe_image = opponent_universe['PATH']
                    tales = opponent_universe['CROWN_TALES']
                    dungeon = opponent_universe['DUNGEONS']
                    goal = quest['GOAL']
                    wins = quest['WINS']
                    reward = '{:,}'.format(quest['REWARD'])
                    tales_message = ""
                    dungeon_message = ""
                    tales_index = 0
                    dungeon_index = 0
                    if opponent_name in tales:
                        for opp in tales:
                            tales_index = tales.index(opponent_name)
                        tales_message = f"**{opponent_name}** is fight number ⚔️ **{tales_index + 1}** in **Tales**"
                    
                    if opponent_name in dungeon:
                        for opp in dungeon:
                            dungeon_index = dungeon.index(opponent_name)
                        dungeon_message = f"**{opponent_name}** is fight number ⚔️ **{dungeon_index + 1}** in **Dungeon**"
                    
                    completed = ""
                    if quest['GOAL'] == quest['WINS']:
                        completed = "🟢"
                    else:
                        completed = "🔴"

                    icon = ":coin:"
                    if balance >= 150000:
                        icon = ":money_with_wings:"
                    elif balance >=100000:
                        icon = ":moneybag:"
                    elif balance >= 50000:
                        icon = ":dollar:"


                    embedVar = discord.Embed(title=f"{opponent_name}", description=textwrap.dedent(f"""\
                    **Quest**: Defeat {opponent_name} **{str(goal)}** times!
                    **Universe:** 🌍 {opponent['UNIVERSE']}
                    **Reward:** {icon} {reward}

                    **Guild Quest Buff:**  {guild_buff_msg}
                   
                    **Wins so far:** {str(wins)}
                    **Completed:** {completed}

                    {tales_message}
                    {dungeon_message}

                    {buff_message}
                    
                    {virus_message}
                    """))

                    embedVar.set_thumbnail(url=opponent_universe_image)
                    # embedVar.set_footer(text="Use /tales to complete daily quest!", icon_url="https://cdn.discordapp.com/emojis/784402243519905792.gif?v=1")
                    embed_list.append(embedVar)

                buttons = [
                    manage_components.create_button(style=3, label="Start Tales", custom_id="quests_tales"),
                    manage_components.create_button(style=3, label="Start Dungeon", custom_id="quests_dungeon"),
                ]
                custom_action_row = manage_components.create_actionrow(*buttons)

                async def custom_function(self, button_ctx):
                    if button_ctx.author == ctx.author:
                        selected_quest = str(button_ctx.origin_message.embeds[0].title)
                        if button_ctx.custom_id == "quests_tales":
                            mode = "Tales"
                            await button_ctx.defer(ignore=True)
                            card = db.queryCard({"NAME": selected_quest})
                            sowner = db.queryUser({'DID': str(ctx.author.id)})
                            universe = db.queryUniverse({"TITLE": card['UNIVERSE']})
                            selected_universe = universe['TITLE']
                            completed_universes = sowner['CROWN_TALES']
                            oguild = "PCG"
                            crestlist = []
                            crestsearch = False
                            # guild = server_name
                            oteam = sowner['TEAM']
                            ofam = sowner['FAMILY']
                            guild_buff = guild_buff_update_function(self, sowner['TEAM'].lower())
                            

                            if sowner['LEVEL'] < 4:
                                await button_ctx.send("🔓 Unlock **Tales** by completing **Floor 3** of the 🌑 **Abyss**! Use /abyss to enter the abyss.")
                                self.stop = True
                                return

                            if oteam != 'PCG':
                                team_info = db.queryTeam({'TEAM_NAME': oteam.lower()})
                                guildname = team_info['GUILD']
                                if guildname != "PCG":
                                    oguild = db.queryGuildAlt({'GNAME': guildname})
                                    if oguild:
                                        crestlist = oguild['CREST']
                                        crestsearch = True

                            currentopponent = 0
                            if guild_buff:
                                if guild_buff['Quest']:
                                    for opp in universe['CROWN_TALES']:
                                        if opp == card['NAME']:
                                            currentopponent = universe['CROWN_TALES'].index(opp)
                                            update_team_response = db.updateTeam(guild_buff['QUERY'], guild_buff['UPDATE_QUERY'])
                                       
                            await battle_commands(self, ctx, mode, universe, selected_universe, completed_universes, oguild,
                                    crestlist, crestsearch, sowner, oteam, ofam, currentopponent, None, None, None,
                                    None, None, None, None, None)
                            
                            self.stop = True
                        if button_ctx.custom_id == "quests_dungeon":
                            await button_ctx.defer(ignore=True)
                            mode = "Dungeon"
                            card = db.queryCard({"NAME": selected_quest})
                            user = db.queryUser({'DID': str(ctx.author.id)})
                            universe = db.queryUniverse({"TITLE": card['UNIVERSE']})
                            selected_universe = universe['TITLE']
                            completed_universes = user['CROWN_TALES']
                            oguild = "PCG"
                            crestlist = []
                            crestsearch = False
                            # guild = server_name
                            oteam = user['TEAM']
                            ofam = user['FAMILY']
                            sowner = user

                            if mode == "Dungeon" and sowner['LEVEL'] < 41:
                                await button_ctx.send("🔓 Unlock **Dungeons** by completing **Floor 40** of the 🌑 **Abyss**! Use /abyss to enter the abyss.")
                                self.stop = True
                                return

                            if universe['TITLE'] not in completed_universes:
                                await button_ctx.send("You have not unlocked this dungeon.")
                                self.stop = True
                                return


                            if oteam != 'PCG':
                                team_info = db.queryTeam({'TEAM_NAME': oteam.lower()})
                                guildname = team_info['GUILD']
                                if guildname != "PCG":
                                    oguild = db.queryGuildAlt({'GNAME': guildname})
                                    if oguild:
                                        crestlist = oguild['CREST']
                                        crestsearch = True

                            
                            currentopponent = 0

                            await battle_commands(self, ctx, mode, universe, selected_universe, completed_universes, oguild,
                                    crestlist, crestsearch, sowner, oteam, ofam, currentopponent, None, None, None,
                                    None, None, None, None, None)
                            
                            self.stop = True

                    else:
                        await ctx.send("This is not your Title list.")

                await Paginator(bot=self.bot, disableAfterTimeout=True, useQuitButton=True, ctx=ctx, pages=embed_list, timeout=60, customActionRow=[
                    custom_action_row,
                    custom_function,
                ]).run()

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
                await ctx.send("There's an issue with your Quest list. Check with support.", hidden=True)
                return
        else:
            newVault = db.createVault({'OWNER': d['DISNAME'], 'DID' : d['DID']})


    @cog_ext.cog_slash(description="Check your Balance", guild_ids=main.guild_ids)
    async def balance(self, ctx):
        try:
            query = {'DID': str(ctx.author.id)}
            d = db.queryUser(query)
            vault = db.queryVault({'DID': d['DID']})
            icon = ":coin:"
            if vault:
                name = d['DISNAME'].split("#",1)[0]
                avatar = d['AVATAR']
                balance = vault['BALANCE']
                if balance >= 1000000:
                    icon = ":money_with_wings:"
                elif balance >=500000:
                    icon = ":moneybag:"
                elif balance >= 100000:
                    icon = ":dollar:"
                if d['TEAM'] != 'PCG':
                    t = db.queryTeam({'TEAM_NAME' : d['TEAM'].lower()})
                    tbal = t['BANK']
                    if d['FAMILY'] != 'PCG':
                        f = db.queryFamily({'HEAD': d['FAMILY']})
                        fbal = f['BANK']
                embedVar = discord.Embed(title= f"{icon}{'{:,}'.format(balance)}", colour=0x7289da)
                await ctx.send(embed=embedVar)
            else:
                newVault = db.createVault({'OWNER': d['DISNAME'], 'DID' : d['DID']})
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
            

    @cog_ext.cog_slash(description="Check your Build Presets", guild_ids=main.guild_ids)
    async def preset(self, ctx):
        query = {'DID': str(ctx.author.id)}
        d = db.queryUser(query)
        vault_query = {'DID': d['DID']}
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
                ownedarms.append(arms['ARM'])
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
   
            listed_options = [f"1️⃣ | {preset1_title} {preset1_card} and {preset1_pet}\n**Card**: {preset1_card}\n**Title**: {preset1_title}\n**Arm**: {preset1_arm}\n**Summon**: {preset1_pet}\n\n", 
            f"2️⃣ | {preset2_title} {preset2_card} and {preset2_pet}\n**Card**: {preset2_card}\n**Title**: {preset2_title}\n**Arm**: {preset2_arm}\n**Summon**: {preset2_pet}\n\n", 
            f"3️⃣ | {preset3_title} {preset3_card} and {preset3_pet}\n**Card**: {preset3_card}\n**Title**: {preset3_title}\n**Arm**: {preset3_arm}\n**Summon**: {preset3_pet}\n\n"]
        
            embedVar = discord.Embed(title="What Preset would you like?", description=textwrap.dedent(f"""
            {"".join(listed_options)}
            """))
            embedVar.set_thumbnail(url=avatar)
            # embedVar.add_field(name=f"Preset 1:{preset1_title} {preset1_card} and {preset1_pet}", value=f"Card: {preset1_card}\nTitle: {preset1_title}\nArm: {preset1_arm}\nSummon: {preset1_pet}", inline=False)
            # embedVar.add_field(name=f"Preset 2:{preset2_title} {preset2_card} and {preset2_pet}", value=f"Card: {preset2_card}\nTitle: {preset2_title}\nArm: {preset2_arm}\nSummon: {preset2_pet}", inline=False)
            # embedVar.add_field(name=f"Preset 3:{preset3_title} {preset3_card} and {preset3_pet}", value=f"Card: {preset3_card}\nTitle: {preset3_title}\nArm: {preset3_arm}\nSummon: {preset3_pet}", inline=False)
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
                    await button_ctx.send(f"{ctx.author.mention}, No change has been made", hidden=True)
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
                                                    await button_ctx.send(f"{ctx.author.mention}, your build updated successfully!")
                                                    return
                                                else:
                                                    await button_ctx.send(f"{ctx.author.mention}, You No Longer Own {preset1_pet}", hidden=True)
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
                                                    await button_ctx.send(f"{ctx.author.mention}, your build updated successfully!")
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
                                                    await button_ctx.send(f"{ctx.author.mention}, your build updated successfully!")
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
                await ctx.send("Preset Issue Seek support.", hidden=True)
        else:
            newVault = db.createVault({'OWNER': d['DISNAME'], 'DID' : d['DID']})


    @cog_ext.cog_slash(description="Save your current Build as Preset", guild_ids=main.guild_ids)
    async def savepreset(self, ctx):
        query = {'DID': str(ctx.author.id)}
        d = db.queryUser(query)
        vault_query = {'DID': d['DID']}
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
   
            listed_options = [f"📝 | {current_title} {current_card} & {current_pet}\n**Card**: {current_card}\n**Title**: {current_title}\n**Arm**: {current_arm}\n**Summon**: {current_pet}\n\n",
            f"1️⃣ | {preset1_title} {preset1_card} & {preset1_pet}\n**Card**: {preset1_card}\n**Title**: {preset1_title}\n**Arm**: {preset1_arm}\n**Summon**: {preset1_pet}\n\n", 
            f"2️⃣ | {preset2_title} {preset2_card} & {preset2_pet}\n**Card**: {preset2_card}\n**Title**: {preset2_title}\n**Arm**: {preset2_arm}\n**Summon**: {preset2_pet}\n\n", 
            f"3️⃣ | {preset3_title} {preset3_card} & {preset3_pet}\n**Card**: {preset3_card}\n**Title**: {preset3_title}\n**Arm**: {preset3_arm}\n**Summon**: {preset3_pet}\n\n"]
        
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
                    if response:
                        await button_ctx.send("📝 1️⃣| Preset Updated!")
                        return
                elif button_ctx.custom_id == "2":
                    response = db.updateVaultNoFilter(vault_query, {'$set': {'DECK.1.CARD' :str(current_card), 'DECK.1.TITLE': str(current_title),'DECK.1.ARM': str(current_arm), 'DECK.1.PET': str(current_pet)}})
                    if response:
                        await button_ctx.send("📝 2️⃣| Preset Updated!")
                        return
                elif button_ctx.custom_id == "3":
                    response = db.updateVaultNoFilter(vault_query, {'$set': {'DECK.2.CARD' :str(current_card), 'DECK.2.TITLE': str(current_title),'DECK.2.ARM': str(current_arm), 'DECK.2.PET': str(current_pet)}})
                    if response:
                        await button_ctx.send("📝 3️⃣| Preset Updated!")
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
                await ctx.send("Preset Issue Seek support.", hidden=True)
        else:
            newVault = db.createVault({'OWNER': d['DISNAME'], 'DID' : d['DID']})


    @cog_ext.cog_slash(description="Open Crown Shop", guild_ids=main.guild_ids)
    async def shop(self, ctx):
        try:
            all_universes = db.queryAllUniverse()
            user = db.queryUser({'DID': str(ctx.author.id)})

            if user['LEVEL'] < 1:
                await ctx.send("🔓 Unlock the Shop by completing Floor 0 of the 🌑 Abyss! Use /abyss to enter the abyss.")
                return

            completed_tales = user['CROWN_TALES']
            completed_dungeons = user['DUNGEONS']
            available_universes = []
            riftShopOpen = False
            shopName = ':shopping_cart: Crown Shop'
            if user['RIFT'] == 1:
                riftShopOpen = True
                shopName = ':crystal_ball: Rift Shop'
                
            if riftShopOpen:    
                for uni in all_universes:
                    if uni['HAS_CROWN_TALES'] and uni['HAS_DUNGEON']:
                        available_universes.append(uni)
            else:
                for uni in all_universes:
                    if uni['TIER'] != 9 and uni['HAS_CROWN_TALES'] and uni['HAS_DUNGEON']:
                        available_universes.append(uni)
            
            vault_query = {'DID' : str(ctx.author.id)}
            vault = db.altQueryVault(vault_query)
            current_titles = vault['TITLES']
            current_cards = vault['CARDS']
            current_arms = []
            for arm in vault['ARMS']:
                current_arms.append(arm['ARM'])

            owned_card_levels_list = []
            for c in vault['CARD_LEVELS']:
                owned_card_levels_list.append(c['CARD'])

            owned_destinies = []
            for destiny in vault['DESTINY']:
                owned_destinies.append(destiny['NAME'])


            balance = vault['BALANCE']
            icon = ":coin:"
            if balance >= 150000:
                icon = ":money_with_wings:"
            elif balance >=100000:
                icon = ":moneybag:"
            elif balance >= 50000:
                icon = ":dollar:"


            embed_list = []
            for universe in available_universes:
                universe_name = universe['TITLE']
                universe_image = universe['PATH']
                adjusted_prices = price_adjuster(15000, universe_name, completed_tales, completed_dungeons)
                embedVar = discord.Embed(title= f"{universe_name}", description=textwrap.dedent(f"""
                *Welcome {ctx.author.mention}! {adjusted_prices['MESSAGE']}
                You have {icon}{'{:,}'.format(balance)} coins!*
                
                🎗️ **Title:** Title Purchase for 💵 {'{:,}'.format(adjusted_prices['TITLE_PRICE'])}
                🦾 **Arm:** Arm Purchase for 💵 {'{:,}'.format(adjusted_prices['ARM_PRICE'])}
                1️⃣ **1-3 Tier Card:** for 💵 {'{:,}'.format(adjusted_prices['C1'])}
                2️⃣ **3-5 Tier Card:** for 💰 {'{:,}'.format(adjusted_prices['C2'])}
                3️⃣ **5-7 Tier Card:** for 💸 {'{:,}'.format(adjusted_prices['C3'])}
                """), colour=0x7289da)
                embedVar.set_image(url=universe_image)
                #embedVar.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620236723/PCG%20LOGOS%20AND%20RESOURCES/Party_Chat_Shop.png")
                embed_list.append(embedVar)

            
            # Pull all cards that don't require tournaments
            # resp = db.queryShopCards()

            buttons = [
                manage_components.create_button(style=3, label="🎗️", custom_id="title"),
                manage_components.create_button(style=1, label="🦾", custom_id="arm"),
                manage_components.create_button(style=2, label="1️⃣", custom_id="t1card"),
                manage_components.create_button(style=2, label="2️⃣", custom_id="t2card"),
                manage_components.create_button(style=2, label="3️⃣", custom_id="t3card"),
            ]

            custom_action_row = manage_components.create_actionrow(*buttons)

            async def custom_function(self, button_ctx):
                if button_ctx.author == ctx.author:
                    updated_vault = db.queryVault({'DID': user['DID']})
                    balance = updated_vault['BALANCE']        
                    universe = str(button_ctx.origin_message.embeds[0].title)
                    if button_ctx.custom_id == "title":
                        updated_vault = db.queryVault({'DID': user['DID']})
                        current_titles = updated_vault['TITLES']
                        price = price_adjuster(50000, universe, completed_tales, completed_dungeons)['TITLE_PRICE']
                        if len(current_titles) >=25:
                            await button_ctx.send("You have max amount of Titles. Transaction cancelled.")
                            self.stop = True
                            return

                        if price > balance:
                            await button_ctx.send("Insufficent funds.")
                            self.stop = True
                            return
                        list_of_titles =[x for x in db.queryAllTitlesBasedOnUniverses({'UNIVERSE': str(universe)}) if not x['EXCLUSIVE'] and x['AVAILABLE']]
                        if not list_of_titles:
                            await button_ctx.send("There are no titles available for purchase in this range.")
                            self.stop = True
                            return

                        selection_length = len(list(list_of_titles)) - 1
                        if selection_length ==0:
                            title = list_of_titles[0]
                        else:
                            selection = random.randint(1,selection_length)
                            title = list_of_titles[selection]  
                        if title['TITLE'] in current_titles:                 
                            bless_amount = price
                            bless_reduction = 0
                            if universe_name in completed_tales:
                                bless_reduction = bless_amount * .25
                                bless_amount = round((bless_amount - bless_reduction)/2)
                            if universe_name in completed_dungeons:
                                bless_reduction = bless_amount * .50
                                bless_amount = round((bless_amount - bless_reduction)/2)
                            else: 
                                bless_amount = round(bless_amount /2)
                            await button_ctx.send(f"You already own **{title['TITLE']}**. You get a :coin:**{'{:,}'.format(bless_amount)}** refund!") 
                            await main.curse(bless_amount, str(ctx.author.id))
                        else:
                            response = db.updateVaultNoFilter(vault_query,{'$addToSet':{'TITLES': str(title['TITLE'])}})   
                            await main.curse(price, str(ctx.author.id))
                            await button_ctx.send(f"You purchased **{title['TITLE']}**.")


                    elif button_ctx.custom_id == "arm":
                        updated_vault = db.queryVault({'DID': user['DID']})
                        current_arms = []
                        for arm in updated_vault['ARMS']:
                            current_arms.append(arm['ARM'])
                        price = price_adjuster(25000, universe, completed_tales, completed_dungeons)['ARM_PRICE']
                        if len(current_arms) >=25:
                            await button_ctx.send("You have max amount of Arms. Transaction cancelled.")
                            self.stop = True
                            return
                        if price > balance:
                            await button_ctx.send("Insufficent funds.")
                            self.stop = True
                            return
                        list_of_arms = [x for x in db.queryAllArmsBasedOnUniverses({'UNIVERSE': str(universe)}) if not x['EXCLUSIVE'] and x['AVAILABLE']]
                        if not list_of_arms:
                            await button_ctx.send("There are no arms available for purchase in this range.")
                            self.stop = True
                            return

                        selection_length = len(list(list_of_arms)) - 1

                        if selection_length ==0:
                            arm = list_of_arms[0]
                        else:
                            selection = random.randint(1,selection_length)
                            arm = list_of_arms[selection]['ARM']
                        
                        if arm not in current_arms:
                            response = db.updateVaultNoFilter(vault_query,{'$addToSet':{'ARMS': {'ARM': str(arm), 'DUR': 25}}})
                            await main.curse(price, str(ctx.author.id))
                            await button_ctx.send(f"You purchased **{arm}**.")
                        else:
                            update_query = {'$inc': {'ARMS.$[type].' + 'DUR': 10}}
                            filter_query = [{'type.' + "ARM": str(arm)}]
                            resp = db.updateVault(vault_query, update_query, filter_query)
                            await main.curse(price, str(ctx.author.id))
                            await button_ctx.send(f"You purchased **{arm}**. Increased durability for the arm by 10 as you already own it.")

               
                    elif button_ctx.custom_id == "t1card":
                        updated_vault = db.queryVault({'DID': user['DID']})
                        current_cards = updated_vault['CARDS']
                        price = price_adjuster(100000, universe, completed_tales, completed_dungeons)['C1']
                        if len(current_cards) >= 25:
                            await button_ctx.send("You have max amount of Cards. Transaction cancelled.")
                            self.stop = True
                            return
                        acceptable = [1,2,3]
                        if price > balance:
                            await button_ctx.send("Insufficent funds.")
                            self.stop = True
                            return
                        list_of_cards = [x for x in db.queryAllCardsBasedOnUniverse({'UNIVERSE': str(universe), 'TIER': {'$in': acceptable}}) if not x['EXCLUSIVE'] and not x['HAS_COLLECTION']]
                        if not list_of_cards:
                            await button_ctx.send("There are no cards available for purchase in this range.")
                            self.stop = True
                            return

                        selection_length = len(list(list_of_cards)) - 1
                        if selection_length ==0:
                            card = list_of_cards[0]
                        else:
                            selection = random.randint(1,selection_length)
                            card = list_of_cards[selection]
                        card_name = card['NAME']
                        tier = 0

                        if card_name in current_cards:
                            await cardlevel(self,card['NAME'], str(ctx.author.id), "Purchase", universe)
                            await button_ctx.send(f"You received a level up for **{card_name}**!")
                            await main.curse(price, str(ctx.author.id))
                            
                        else:
                            response = db.updateVaultNoFilter(vault_query,{'$addToSet': {'CARDS': str(card_name)}})
                            await main.curse(price, str(ctx.author.id))

                            # Add Card Level config
                            if card_name not in owned_card_levels_list:
                                update_query = {'$addToSet': {
                                    'CARD_LEVELS': {'CARD': str(card_name), 'LVL': 0, 'TIER': int(tier),
                                                    'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0}}}
                                r = db.updateVaultNoFilter(vault_query, update_query)

                            # Add Destiny
                            for destiny in d.destiny:
                                if card_name in destiny["USE_CARDS"] and destiny['NAME'] not in owned_destinies:
                                    db.updateVaultNoFilter(vault_query, {'$addToSet': {'DESTINY': destiny}})
                                    await button_ctx.send(
                                        f"**DESTINY AWAITS!**\n**{destiny['NAME']}** has been added to your vault.", hidden=True)


                            await button_ctx.send(f"You purchased **{card_name}**!")
                            # self.stop = True
                            # return


                    elif button_ctx.custom_id == "t2card":
                        updated_vault = db.queryVault({'DID': user['DID']})
                        current_cards = updated_vault['CARDS']
                        price = price_adjuster(450000, universe, completed_tales, completed_dungeons)['C2']
                        if len(current_cards) >=25:
                            await button_ctx.send("You have max amount of Cards. Transaction cancelled.")
                            self.stop = True
                            return
                        acceptable = [3,4,5]
                        if price > balance:
                            await button_ctx.send("Insufficent funds.")
                            self.stop = True
                            return
                        list_of_cards = [x for x in db.queryAllCardsBasedOnUniverse({'UNIVERSE': str(universe), 'TIER': {'$in': acceptable}}) if not x['EXCLUSIVE'] and not x['HAS_COLLECTION']]
                        
                        if not list_of_cards:
                            await button_ctx.send("There are no cards available for purchase in this range.")
                            self.stop = True
                            return
                        
                        selection_length = len(list(list_of_cards)) - 1

                        if selection_length ==0:
                            card = list_of_cards[0]
                        else:
                            selection = random.randint(1,selection_length)
                            card = list_of_cards[selection]
                        card_name = card['NAME']
                        tier = 0

                        if card_name in current_cards:
                            await cardlevel(self,card['NAME'], str(ctx.author.id), "Purchase", universe)
                            await button_ctx.send(f"You received a level up for **{card_name}**!")
                            await main.curse(price, str(ctx.author.id))
                            
                        else:
                            response = db.updateVaultNoFilter(vault_query,{'$addToSet': {'CARDS': str(card_name)}})
                            await main.curse(price, str(ctx.author.id))

                            # Add Card Level config
                            if card_name not in owned_card_levels_list:
                                update_query = {'$addToSet': {
                                    'CARD_LEVELS': {'CARD': str(card_name), 'LVL': 0, 'TIER': int(tier),
                                                    'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0}}}
                                r = db.updateVaultNoFilter(vault_query, update_query)


                            # Add Destiny
                            for destiny in d.destiny:
                                if card_name in destiny["USE_CARDS"] and destiny['NAME'] not in owned_destinies:
                                    db.updateVaultNoFilter(vault_query, {'$addToSet': {'DESTINY': destiny}})
                                    await button_ctx.send(
                                        f"**DESTINY AWAITS!**\n**{destiny['NAME']}** has been added to your vault.", hidden=True)


                            await button_ctx.send(f"You purchased **{card_name}**!")
                            # self.stop = True
                            # return

                    elif button_ctx.custom_id == "t3card":
                        updated_vault = db.queryVault({'DID': user['DID']})
                        current_cards = updated_vault['CARDS']
                        price = price_adjuster(6000000, universe, completed_tales, completed_dungeons)['C3']
                        if len(current_cards) >=25:
                            await button_ctx.send("You have max amount of Cards. Transaction cancelled.")
                            self.stop = True
                            return
                        acceptable = [5,6,7]
                        if price > balance:
                            await button_ctx.send("Insufficent funds.")
                            self.stop = True
                            return
                        card_list_response = [x for x in db.queryAllCardsBasedOnUniverse({'UNIVERSE': str(universe), 'TIER': {'$in': acceptable}}) if not x['EXCLUSIVE'] and not x['HAS_COLLECTION']]
                        if not card_list_response:
                            await button_ctx.send("There are no cards available for purchase in this range.")
                            self.stop = True
                            return
                        else:
                            list_of_cards = []
                            for card in card_list_response:
                                if card['AVAILABLE'] and not card['EXCLUSIVE'] and not card['HAS_COLLECTION']:
                                    list_of_cards.append(card)


                        if not list_of_cards:
                            await button_ctx.send("There are no cards available for purchase in this range.")
                            self.stop = True
                            return

                        selection_length = len(list(list_of_cards)) - 1
                        if selection_length ==0:
                            card = list_of_cards[0]
                        else:
                            selection = random.randint(1,selection_length)
                            card = list_of_cards[selection]
                        card_name = card['NAME']
                        tier = 0

                        if card_name in current_cards:
                            await cardlevel(self,card['NAME'], str(ctx.author.id), "Purchase", universe)
                            await button_ctx.send(f"You received a level up for **{card_name}**!")
                            await main.curse(price, str(ctx.author.id))
                            
                        else:
                            response = db.updateVaultNoFilter(vault_query,{'$addToSet': {'CARDS': str(card_name)}})
                            await main.curse(price, str(ctx.author.id))

                            # Add Card Level config
                            if card_name not in owned_card_levels_list:
                                update_query = {'$addToSet': {
                                    'CARD_LEVELS': {'CARD': str(card_name), 'LVL': 0, 'TIER': int(tier),
                                                    'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0}}}
                                r = db.updateVaultNoFilter(vault_query, update_query)


                            # Add Destiny
                            for destiny in d.destiny:
                                if card_name in destiny["USE_CARDS"] and destiny['NAME'] not in owned_destinies:
                                    db.updateVaultNoFilter(vault_query, {'$addToSet': {'DESTINY': destiny}})
                                    await button_ctx.send(
                                        f"**DESTINY AWAITS!**\n**{destiny['NAME']}** has been added to your vault.", hidden=True)

                            await button_ctx.send(f"You purchased **{card_name}**!")

                            # self.stop = True
                            # return

                else:
                    await ctx.send("This is not your Shop.")
            await Paginator(bot=self.bot, useQuitButton=True, disableAfterTimeout=True, ctx=ctx, pages=embed_list, timeout=60, customActionRow=[
                custom_action_row,
                custom_function,
            ]).run()
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


    @cog_ext.cog_slash(description="Open Gem Crafting", guild_ids=main.guild_ids)
    async def craft(self, ctx):
        # Craft with Gems
        # Craft Universe Heart, Universe Soul, Skin Box
        poke_universes = ['Kanto Region', 'Johto Region', 'Hoenn Region', 'Sinnoh Region']
        try:
            gems = 0
            all_universes = db.queryAllUniverse()
            user = db.queryUser({'DID': str(ctx.author.id)})
            card_info = db.queryCard({"NAME": user['CARD']})
            destiny_alert_message = f"No Skins or Destinies available for {card_info['NAME']}"
            destiny_alert = False
            if user['LEVEL'] < 9:
                await ctx.send("🔓 Unlock Crafting by completeing Floor 8 of the 🌑 Abyss! Use /abyss to enter the abyss.")
                return

            
            
            #skin_alert_message = f"No Skins for {card_info['NAME']}"
            
                #skin_alert_message = f"No Skins for {card_info['NAME']}"
            available_universes = []
            riftShopOpen = False
            shopName = ':shopping_cart: Crown Shop'
            if user['RIFT'] == 1:
                riftShopOpen = True
                shopName = ':crystal_ball: Rift Shop'
                
            if riftShopOpen:    
                for uni in all_universes:
                    if uni['HAS_CROWN_TALES'] and uni['HAS_DUNGEON']:
                        available_universes.append(uni)
            else:
                for uni in all_universes:
                    if uni['TIER'] != 9 and uni['HAS_CROWN_TALES'] and uni['HAS_DUNGEON']:
                        available_universes.append(uni)
            
            vault_query = {'DID' : str(ctx.author.id)}
            vault = db.altQueryVault(vault_query)
            current_cards = vault['CARDS']
            owned_card_levels_list = []
            for c in vault['CARD_LEVELS']:
                owned_card_levels_list.append(c['CARD'])
                
            #Card skin query 
            list_of_card_skins = False
            skin_alert = False
            card_skin_message = "No Skins"
            new_skin_list = []
            
            list_of_card_skins = [x for x in db.queryAllCardsBasedOnUniverse({'SKIN_FOR' : card_info['NAME']})]
            
            if list_of_card_skins: 
                for skin in list_of_card_skins:
                    
                    if skin['NAME'] not in current_cards and skin['SKIN_FOR'] == user['CARD']:
                        new_skin_list.append(skin)
                        card_skin_message = f" {card_info['UNIVERSE']} Skins Available!"
                        skin_alert = True
           
                
                

            owned_destinies = []
            for destiny in vault['DESTINY']:
                owned_destinies.append(destiny['NAME'])
                d_card = ' '.join(destiny['USE_CARDS'])
                d_card_info = db.queryCard({"NAME": str(d_card)})
                if card_info['NAME'] in destiny['USE_CARDS'] or card_info['SKIN_FOR'] in d_card_info['NAME']:
                    #destiny_alert_message = f"{card_info['UNIVERSE']} Destinies Availble"
                    destiny_alert = True
            if len(owned_destinies) >= 1:
                destiny_Alert = True
            
                    
            if skin_alert == True and destiny_alert ==True:
                destiny_alert_message = f"{card_info['NAME']} Skins and Destinies Available!"
            elif skin_alert == True:
                destiny_alert_message = f"{card_info['NAME']} Skins Available!"
            elif destiny_alert == True:
                destiny_alert_message = f"{card_info['NAME']} Destinies Available!"
            
                    
            embed_list = []
            for universe in available_universes:
                universe_name = universe['TITLE']
                universe_image = universe['PATH']
                universe_heart = False
                universe_soul = False
                gems = 0
                for uni in vault['GEMS']:
                    if uni['UNIVERSE'] == universe_name:
                        gems = uni['GEMS']
                        universe_heart = uni['UNIVERSE_HEART']
                        universe_soul = uni['UNIVERSE_SOUL']
                heart_message = "Cannot Afford"
                soul_message = "Cannot Afford"
                destiny_message = "Cannot Afford"
                if universe_heart:
                    heart_message = "Owned"
                elif gems >= 1000000:
                    heart_message = "Craftable"
                if universe_soul:
                    soul_message = "Owned"
                elif gems >= 500000:
                    soul_message = "Craftable"
                if gems >= 800000 and universe_name == card_info['UNIVERSE'] and destiny_alert:
                    destiny_message = f"Destinies available"
                elif gems >= 800000 and destiny_alert:
                    destiny_message = f"{universe_name} Destinies available"
                elif gems >= 800000:
                    destiny_message = f"Affordable!"
                if universe_name != card_info['UNIVERSE'] and skin_alert:
                    card_skin_message = f"{card_info['UNIVERSE']} Skin Available!"
                    if card_info['UNIVERSE'] in poke_universes:
                        card_skin_message = f"Regional Pokemon Skins Available!"
                    
                embedVar = discord.Embed(title= f"{universe_name}", description=textwrap.dedent(f"""
                Welcome {ctx.author.mention}!
                You have 💎 *{'{:,}'.format(gems)}* **{universe_name}** gems !
                
                🎴 Card:  **{card_info['NAME']}** *{card_info['UNIVERSE']}*
                *{destiny_alert_message}*
                
                💟 **Universe Heart:** 💎 1,000,000 *{heart_message}*
                *Grants ability to level past 200*

                🌹 **Universe Soul:** 💎 500,000 *{soul_message}*
                *Grants double exp in this Universe*

                ✨ **Destiny Line:** 💎 800,000 *{destiny_message}*
                *Grants win for a Destiny Line*
                
                🃏 **Card Skins:** 💎 2,000,000 *{card_skin_message}*
                *Grants Card Skin*
                """), colour=0x7289da)
                embedVar.set_image(url=universe_image)
                embed_list.append(embedVar)

        
            buttons = [
                manage_components.create_button(style=3, label="💟", custom_id="UNIVERSE_HEART"),
                manage_components.create_button(style=1, label="🌹", custom_id="UNIVERSE_SOUL"),
                manage_components.create_button(style=1, label="✨", custom_id="Destiny"),
                manage_components.create_button(style=1, label="🃏", custom_id="Skin")
            ]

            custom_action_row = manage_components.create_actionrow(*buttons)

            async def custom_function(self, button_ctx):
                if button_ctx.author == ctx.author:
                    universe = str(button_ctx.origin_message.embeds[0].title)
                    if button_ctx.custom_id == "UNIVERSE_HEART":
                        price = 1000000
                        response = await craft_adjuster(self, ctx, vault, universe, price, button_ctx.custom_id, None)
                        if response['SUCCESS']:
                            await button_ctx.send(f"{response['MESSAGE']}")
                            self.stop = True
                        else:
                            await button_ctx.send(f"{response['MESSAGE']}")
                            self.stop = True                           

                    if button_ctx.custom_id == "UNIVERSE_SOUL":
                        price = 500000
                        response = await craft_adjuster(self, ctx, vault, universe, price, button_ctx.custom_id, None)
                        if response['SUCCESS']:
                            await button_ctx.send(f"{response['MESSAGE']}")
                            self.stop = True
                        else:
                            await button_ctx.send(f"{response['MESSAGE']}")
                            self.stop = True
                    if button_ctx.custom_id == "Destiny":
                        await button_ctx.defer(ignore=True)
                        price = 800000
                        response = await craft_adjuster(self, ctx, vault, universe, price, card_info, None)
                        if not response['SUCCESS']:
                            await button_ctx.send(f"{response['MESSAGE']}")
                            self.stop = True
                    if button_ctx.custom_id == "Skin":
                        await button_ctx.defer(ignore=True)
                        price = 2000000
                        response = await craft_adjuster(self, ctx, vault, universe, price, card_info, new_skin_list)
                        print(response)
                        if not response['SUCCESS']:
                            await button_ctx.send(f"{response['MESSAGE']}")
                            self.stop = True
                 
                else:
                    await ctx.send("This is not your Craft.")

            await Paginator(bot=self.bot, useQuitButton=True, disableAfterTimeout=True, ctx=ctx, pages=embed_list, timeout=60, customActionRow=[
                custom_action_row,
                custom_function,
            ]).run()
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

    # @cog_ext.cog_slash(description="Open Storage", guild_ids=main.guild_ids)
    # async def storage(self, ctx):
    #     vault_query = {'DID': str(ctx.author.id)}
    #     vault = db.altQueryVault(vault_query)
    #     storage = vault['STORAGE']
    #     hand = vault['CARDS']

async def craft_adjuster(self, player, vault, universe, price, item, skin_list):
    try:
        base_title = db.queryTitle({'TITLE':'Starter'})
        item_bools = [
            'UNIVERSE_HEART', 
            'UNIVERSE_SOUL'
        ]
        gems = 0
        universe_heart = False
        universe_soul = False
        has_gems_for = False
        negPriceAmount = 0 - abs(int(price))
        response = {}
        for uni in vault['GEMS']:
            if uni['UNIVERSE'] == universe:
                gems = uni['GEMS']
                universe_heart = uni['UNIVERSE_HEART']
                universe_soul = uni['UNIVERSE_SOUL']
                has_gems_for = True
        #owned levels
        owned_card_levels_list = []
        for c in vault['CARD_LEVELS']:
            owned_card_levels_list.append(c['CARD'])
            
        #owned Destinies
        owned_destinies = []
        for destiny in vault['DESTINY']:
            owned_destinies.append(destiny['NAME'])

        if has_gems_for:
            if gems >= price:
                if item not in item_bools:
                    if not skin_list:
                        if price == 2000000: #check if price is for skins
                            response = {"HAS_GEMS_FOR": True, "SUCCESS":  False, "MESSAGE": f"Your **{item['NAME']}** does not have Skins in **{universe}**!"}
                            return response
                        card_universe = item['UNIVERSE']
                        card_name = item['NAME']
                        card_has_destiny = False
                        destiny_wins = 0
                        destiny_required_wins = 0
                        destiny_name = ""
                        destiny_earn = ""
                        destiny_universe = ""
                        destiny_defeat = ""
                        cards_destiny_list = []
                        
                        if card_universe != universe:
                            response = {"HAS_GEMS_FOR": True, "SUCCESS":  False, "MESSAGE": f"Your **{card_name}** does not have a Destiny Line in **{universe}**!"}
                            # await player.send(f"Your **{card_name}** does not have a Destiny Line in **{universe}**!")
                            return response
                        
                        if vault['DESTINY']:
                            for destiny in vault['DESTINY']:
                                d_card = ' '.join(destiny['USE_CARDS'])
                                d_card_info = db.queryCard({"NAME": str(d_card)})
                                if card_name in destiny['USE_CARDS'] and not destiny['COMPLETED'] and card_universe == universe or item['SKIN_FOR'] == d_card_info['NAME']:
                                    card_has_destiny = True
                                    cards_destiny_list.append(destiny)
                                    destiny_wins = destiny['WINS']
                                    destiny_required_wins = destiny['REQUIRED']
                                    destiny_name = destiny['NAME']
                                    destiny_earn = destiny['EARN']
                                    destiny_universe = destiny['UNIVERSE']
                                    destiny_defeat = destiny['DEFEAT']
        
                        if card_has_destiny:
                            embed_list = []
                            for destiny in cards_destiny_list:
                                embedVar = discord.Embed(title= f"{destiny['DEFEAT']}", description=textwrap.dedent(f"""
                                ✨ **{destiny['NAME']}**

                                **Wins** - *{destiny['WINS']}*
                                **Wins Required To Complete** - *{destiny['REQUIRED']}*
                                **Defeat** - *{destiny['DEFEAT']}*
                                **Reward** - **{destiny['EARN']}**
                                """), colour=0x7289da)
                                embedVar.set_footer(text=f"Select a Destiny Line to apply win to")
                                embed_list.append(embedVar)
                            

                            try:

                                buttons = [
                                    manage_components.create_button(style=3, label="Craft Win", custom_id="craft_d_win")
                                ]
                                custom_action_row = manage_components.create_actionrow(*buttons)

                                async def custom_function(self, button_ctx):
                                    if button_ctx.author == player.author:
                                        selected_destiny = str(button_ctx.origin_message.embeds[0].title)
                                        if button_ctx.custom_id == "craft_d_win":
                                            r = await update_destiny_call(button_ctx.author, selected_destiny, "Tales")
                                           
                                            query = {'DID': str(vault['DID'])}
                                            update_query = {
                                                '$inc': {'GEMS.$[type].' + "GEMS": int(negPriceAmount)}
                                            }
                                            filter_query = [{'type.' + "UNIVERSE": universe}]
                                            res = db.updateVault(query, update_query, filter_query)
                                            await button_ctx.send(f"Craft Success!")
                                            response = {"HAS_GEMS_FOR": True, "SUCCESS":  True, "MESSAGE": "Craft Success!"}
                                            return response
                                            self.stop = True

                                await Paginator(bot=self.bot, disableAfterTimeout=True,useQuitButton=True, ctx=player, pages=embed_list, timeout=60, customActionRow=[
                                custom_action_row,
                                custom_function,
                                ]).run()

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
                                response = {"HAS_GEMS_FOR": True, "SUCCESS":  False, "MESSAGE": f"Craft Failed!"}
                                return response
                        else:
                            response = {"HAS_GEMS_FOR": True, "SUCCESS":  False, "MESSAGE": f"Your **{card_name}** does not have a Destiny Line in **{universe}**!"}
                            return response
                    else:
                        available_skins = skin_list
                        card_universe = item['UNIVERSE']
                        card_name = item['NAME']
                        card_has_skin = True
                        if card_universe != universe:
                            response = {"HAS_GEMS_FOR": True, "SUCCESS":  False, "MESSAGE": f"Your **{card_name}** does not have a Skin in **{universe}**!"}
                            return response
                        
                        if card_has_skin:
                            embed_list = []
                            for skins in skin_list:
                                s_moveset = skins['MOVESET']
                                s_passive = skins['PASS'][0]
                                s_enhancer = s_moveset[3]
                                move1 = s_moveset[0] 
                                move2 = s_moveset[1] 
                                move3 = s_moveset[2] 
                                
                                move1name = list(move1.keys())[0]
                                move2name = list(move2.keys())[0]
                                move3name = list(move2.keys())[0]
                                
                                move1ap = list(move1.values())[0]
                                move2ap = list(move2.values())[0]
                                move3ap = list(move3.values())[0]
                                
                                enhmove = list(s_enhancer.keys())[0]
                                enhap = list(s_enhancer.values())[0]
                                enh = list(s_enhancer.values())[2]
                                
                                passive_name = list(s_passive.keys())[0]
                                passive_num = list(s_passive.values())[0]
                                passive_type = list(s_passive.values())[1]
                                
                                traits = ut.traits
                                mytrait = {}
                                traitmessage = ''
                                o_show = skins['UNIVERSE']
                                for trait in traits:
                                    if trait['NAME'] == o_show:
                                        mytrait = trait
                                    if o_show == 'Kanto Region' or o_show == 'Johto Region' or o_show == 'Kalos Region' or o_show == 'Unova Region' or o_show == 'Sinnoh Region' or o_show == 'Hoenn Region' or o_show == 'Galar Region' or o_show == 'Alola Region':
                                        if trait['NAME'] == 'Pokemon':
                                            mytrait = trait
                                if mytrait:
                                    traitmessage = f"**{mytrait['EFFECT']}:** {mytrait['TRAIT']}"
                                    
                                skin_stats = showcard(skins, skins['HLT'],skins['HLT'], skins['STAM'],skins['STAM'], False, base_title, False, skins['ATK'], skins['DEF'], 0, move1ap, move2ap, move3ap, enhap, enh, 0, None )
                                embedVar = discord.Embed(title= f"{skins['NAME']}", description=textwrap.dedent(f"""
                                :mahjong: {skins['TIER']}: 🃏 **{skins['SKIN_FOR']}** 
                                :heart: **{skins['HLT']}** :dagger: **{skins['ATK']}** :shield: **{skins['DEF']}**
                                
                                💥 **{move1name}:** {move1ap}
                                ☄️ **{move2name}:** {move2ap}
                                🏵️ **{move3name}:** {move3ap}
                                🦠 **{enhmove}:** {enh} {enhap}{enhancer_suffix_mapping[enh]}

                                🩸 **{passive_name}:** {passive_type} {passive_num}{passive_enhancer_suffix_mapping[passive_type]}
                                ♾️ {traitmessage}
                                **Universe** - *{skins['UNIVERSE']}*
                                """), colour=0x7289da)
                                embedVar.set_footer(text=f"Select a Skin!")
                                embedVar.set_image(url="attachment://image.png")
                                embed_list.append(embedVar)
                        try:

                            buttons = [
                                manage_components.create_button(style=3, label="Craft Skin", custom_id="craft_skin")
                            ]
                            custom_action_row = manage_components.create_actionrow(*buttons)

                            async def custom_function(self, button_ctx):
                                if button_ctx.author == player.author:
                                    selected_skin = str(button_ctx.origin_message.embeds[0].title)
                                    if button_ctx.custom_id == "craft_skin":
                                        #r = await update_destiny_call(button_ctx.author, selected_destiny, "Tales")
                                        
                                        query = {'DID': str(vault['DID'])}
                                        skin_response = db.updateVaultNoFilter(query,{'$addToSet': {'CARDS': str(selected_skin)}})
                                        
                                        # Add Card Level config
                                        if selected_skin not in owned_card_levels_list:
                                            update_query = {'$addToSet': {
                                                'CARD_LEVELS': {'CARD': str(selected_skin), 'LVL': 0, 'TIER': int(0),
                                                                'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0}}}
                                            r = db.updateVaultNoFilter(query, update_query)
                                        
                                        #Add Destiny
                                        for destiny in d.destiny:
                                            if selected_skin in destiny["USE_CARDS"] and destiny['NAME'] not in owned_destinies:
                                                db.updateVaultNoFilter(query, {'$addToSet': {'DESTINY': destiny}})
                                                await button_ctx.send(
                                                    f"**DESTINY AWAITS!**\n**{destiny['NAME']}** has been added to your vault.", hidden=True)
                                        update_query = {
                                            '$inc': {'GEMS.$[type].' + "GEMS": int(negPriceAmount)}
                                        }
                                        filter_query = [{'type.' + "UNIVERSE": universe}]
                                        res = db.updateVault(query, update_query, filter_query)
                                        await button_ctx.send(f"Craft Success!")
                                        response = {"HAS_GEMS_FOR": True, "SUCCESS":  True, "MESSAGE": "Craft Success!"}
                                        return response
                                        self.stop = True
                                        

                            await Paginator(bot=self.bot, disableAfterTimeout=True,useQuitButton=True, ctx=player, pages=embed_list, timeout=60, customActionRow=[
                            custom_action_row,
                            custom_function,
                            ]).run()

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
                            response = {"HAS_GEMS_FOR": True, "SUCCESS":  False, "MESSAGE": f"Craft Failed!"}
                            return response
                        
                        

                if item in item_bools:
                    if item == "UNIVERSE_HEART" and universe_heart:
                        response = {"HAS_GEMS_FOR": True, "SUCCESS":  True, "MESSAGE": "You already have the Universe Heart for this universe!"}
                        return response
                    if item == "UNIVERSE_SOUL" and universe_soul:
                        response = {"HAS_GEMS_FOR": True, "SUCCESS":  True, "MESSAGE": "You already have the Universe Soul for this universe!"}
                        return response

                    query = {'DID': str(vault['DID'])}
                    update_query = {
                        '$inc': {'GEMS.$[type].' + "GEMS": int(negPriceAmount)}, 
                        '$set': {'GEMS.$[type].' + str(item): True}
                    }
                    filter_query = [{'type.' + "UNIVERSE": universe}]
                    res = db.updateVault(query, update_query, filter_query)

                    response = {"HAS_GEMS_FOR": True, "SUCCESS":  True, "MESSAGE": "Success!"}
                    return response
            else:
                    response = {"HAS_GEMS_FOR": True, "SUCCESS":  False, "MESSAGE": "Insufficent 💎!"}
                    return response
        else:
            response = {"HAS_GEMS_FOR": False, "SUCCESS":  False, "MESSAGE": "You have no 💎 for this Universe."}
            return response

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


def price_adjuster(price, selected_universe, completed_tales, completed_dungeons):
    new_price = price
    title_price = 50000
    arm_price = 25000
    c1 = 100000
    c2 = 450000
    c3 = 6000000
    message = ""
    if selected_universe in completed_tales:
        new_price = price - round(price * .25)
        title_price = title_price - round(title_price * .25)
        arm_price = arm_price - round(arm_price * .25)
        c1 = c1 - round(c1 * .25)
        c2 = c2 - round(c2 * .25)
        c3 = c3 - round(c3 * .25)
        message = "**25% Sale**"
    if selected_universe in completed_dungeons:
        new_price = round(price * .50)
        title_price = round(50000 * .50)
        arm_price = round(25000 * .50)
        c1 = round(c1 * .50)
        c2 = round(c2 * .50)
        c3 = round(c3 * .50)
        message = "**50% Sale**"

    response = {'NEW_PRICE': new_price,
    'TITLE_PRICE': title_price,
    'ARM_PRICE': arm_price,
    'C1': c1,
    'C2': c2,
    'C3': c3,
    'MESSAGE': message
    }
    return response


def setup(bot):
    bot.add_cog(Profile(bot))