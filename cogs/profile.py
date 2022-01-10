import discord
from discord.ext import commands
from pymongo import response
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
from .crownunlimited import showcard, cardback, enhancer_mapping, title_enhancer_mapping, enhancer_suffix_mapping, title_enhancer_suffix_mapping, passive_enhancer_suffix_mapping, Crest_dict, cardlevel
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
        query = {'DISNAME': str(ctx.author)}
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


            await ctx.send(f"{ctx.author.mention}, are you sure you want to delete your account? " + "\n" + "All of your wins, purchases and other earnings will be removed from the system and can not be recovered. ", hidden=True, components=[accept_buttons_action_row])

            def check(button_ctx):
                return button_ctx.author == ctx.author

            try:
                button_ctx: ComponentContext = await manage_components.wait_for_component(self.bot, components=[accept_buttons_action_row], timeout=120,check=check)

                if button_ctx.custom_id == "no":
                    await button_ctx.send("Account not deleted.")
                    return

                if button_ctx.custom_id == "yes":
                    delete_user_resp = db.deleteUser(user)
                    vault = db.queryVault({'OWNER': user})
                    if vault:
                        db.deleteVault(vault)

                    await button_ctx.send("Account successfully deleted.")

            except:
                await ctx.send(m.RESPONSE_NOT_DETECTED, hidden=True) 
        else:
            await ctx.send("You aren't registered.", hidden=True)


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
                performance_mode = d['PERFORMANCE']
                
        
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
                        embedVar.set_footer(text=f"EXP Until Next Level: {150 - card_exp}\nRebirth Buff: +{rebirthBonus}\n♾️ {traitmessage}\n{warningmessage}")
                    else:
                        embedVar.set_footer(text=f"Max Level")
                    
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
        query = {'DISNAME': str(ctx.author)}
        d = db.queryUser(query)
        vault = db.queryVault({'OWNER': d['DISNAME']})
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
                    :heart: **{resp['HLT']}** :dagger: **{resp['ATK']}** :shield: **{resp['DEF']}**
                    
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
                        updated_vault = db.queryVault({'OWNER': d['DISNAME']})
                        sell_price = 0
                        selected_card = str(button_ctx.origin_message.embeds[0].title)
                        if button_ctx.custom_id == "Equip":
                            if selected_card in updated_vault['CARDS']:
                                selected_universe = custom_function
                                custom_function.selected_universe = selected_card
                                user_query = {'DISNAME': str(ctx.author)}
                                response = db.updateUserNoFilter(user_query, {'$set': {'CARD': selected_card}})
                                await button_ctx.send(f":flower_playing_cards: **{selected_card}** equipped.")
                                self.stop = True
                            else:
                                await button_ctx.send(f"**{selected_card}** is no longer in your vault.")
                        
                        elif button_ctx.custom_id == "Resell":
                            card_data = db.queryCard({'NAME': selected_card})
                            card_name = card_data['NAME']
                            sell_price = sell_price + (card_data['PRICE'] * .30)
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
                                        db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$pull':{'CARDS': card_name}})
                                        await main.bless(sell_price, ctx.author)
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
                            card_name = card_data['NAME']
                            selected_universe = card_data['UNIVERSE']
                            dismantle_amount = round(card_data['PRICE'] * .01)
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
                                            query = {'OWNER': str(ctx.author)}
                                            update_query = {'$inc': {'GEMS.$[type].' + "GEMS": dismantle_amount}}
                                            filter_query = [{'type.' + "UNIVERSE": selected_universe}]
                                            response = db.updateVault(query, update_query, filter_query)
                                        else:
                                            response = db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$addToSet':{'GEMS': {'UNIVERSE': selected_universe, 'GEMS': dismantle_amount, 'UNIVERSE_HEART': False, 'UNIVERSE_SOUL': False}}})

                                        db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$pull':{'CARDS': card_name}})
                                        await main.bless(sell_price, ctx.author)
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
                            mtrade = db.queryTrade({'MERCHANT' : str(ctx.author), 'OPEN' : True})
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
                                    btrade = db.queryTrade({'BUYER' : str(ctx.author), 'OPEN' : True})
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
                                                trade_query = {'MERCHANT' : str(button_ctx.author), 'BUYER' : str(mtrade['BUYER']), 'OPEN' : True}
                                                update_query = {"$pull" : {'MCARDS': selected_card}, "$inc" : {'TAX' : int(neg_sell_price)}}
                                                resp = db.updateTrade(trade_query, update_query)
                                                await button_ctx.send("Returned.")
                                                self.stop = True
                                            elif bvalidation:
                                                trade_query = {'MERCHANT' : str(btrade['MERCHANT']),'BUYER' : str(button_ctx.author), 'OPEN' : True}
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
                                                trade_query = {'MERCHANT' : str(ctx.author), 'BUYER' : str(mtrade['BUYER']), 'OPEN' : True}
                                                update_query = {"$push" : {'MCARDS': selected_card}, "$inc" : {'TAX' : int(sell_price)}}
                                                resp = db.updateTrade(trade_query, update_query)
                                                await button_ctx.send("Traded.")
                                                self.stop = True
                                            elif bvalidation:
                                                trade_query = {'MERCHANT' : str(btrade['MERCHANT']),'BUYER' : str(ctx.author), 'OPEN' : True}
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
                            await button_ctx.send("Done.")
                            self.stop = True
                    else:
                        await ctx.send("This is not your card list.")
                await Paginator(bot=self.bot, disableAfterTimeout=True, ctx=ctx, pages=embed_list, timeout=60, customActionRow=[
                    custom_action_row,
                    custom_function,
                ]).run()
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
            await ctx.send("There's an issue with loading your cards. Check with support.", hidden=True)
            return

    @cog_ext.cog_slash(description="Check all your Titles", guild_ids=main.guild_ids)
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
                        updated_vault = db.queryVault({'OWNER': d['DISNAME']})
                        sell_price = 0
                        selected_title = str(button_ctx.origin_message.embeds[0].title)
                        if button_ctx.custom_id == "Equip":
                            if selected_title in updated_vault['TITLES']:
                                selected_universe = custom_function
                                custom_function.selected_universe = selected_title
                                user_query = {'DISNAME': str(ctx.author)}
                                response = db.updateUserNoFilter(user_query, {'$set': {'TITLE': selected_title}})
                                await button_ctx.send(f"🎗️ **{selected_title}** equipped.")
                                self.stop = True
                            else:
                                await button_ctx.send(f"**{selected_title}** is no longer in your vault.")                           
                        
                        elif button_ctx.custom_id == "Resell":
                            title_data = db.queryTitle({'TITLE': selected_title})
                            title_name = title_data['TITLE']
                            sell_price = sell_price + (title_data['PRICE'] * .30)
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
                                        db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$pull':{'TITLES': title_name}})
                                        await main.bless(sell_price, ctx.author)
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
                            dismantle_amount = round(title_data['PRICE'] * .03)
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
                                            query = {'OWNER': str(ctx.author)}
                                            update_query = {'$inc': {'GEMS.$[type].' + "GEMS": dismantle_amount}}
                                            filter_query = [{'type.' + "UNIVERSE": selected_universe}]
                                            response = db.updateVault(query, update_query, filter_query)
                                        else:
                                            response = db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$addToSet':{'GEMS': {'UNIVERSE': selected_universe, 'GEMS': dismantle_amount, 'UNIVERSE_HEART': False, 'UNIVERSE_SOUL': False}}})

                                        db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$pull':{'TITLES': title_name}})
                                        await main.bless(sell_price, ctx.author)
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
                            mtrade = db.queryTrade({'MERCHANT' : str(ctx.author), 'OPEN' : True})
                            mvalidation=False
                            bvalidation=False
                            item_already_in_trade=False
                            if mtrade:
                                if selected_title in mtrade['MTITLES']:
                                    await ctx.send(f"{ctx.author.mention} title already in **Trade**")
                                    item_already_in_trade=True
                                mvalidation=True
                            else:
                                btrade = db.queryTrade({'BUYER' : str(ctx.author), 'OPEN' : True})
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
                                            trade_query = {'MERCHANT' : str(button_ctx.author), 'BUYER' : str(mtrade['BUYER']), 'OPEN' : True}
                                            update_query = {"$pull" : {'MTITLES': selected_title}, "$inc" : {'TAX' : int(neg_sell_price)}}
                                            resp = db.updateTrade(trade_query, update_query)
                                            await button_ctx.send("Returned.")
                                            self.stop = True
                                        elif bvalidation:
                                            trade_query = {'MERCHANT' : str(btrade['MERCHANT']),'BUYER' : str(button_ctx.author), 'OPEN' : True}
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
                                            trade_query = {'MERCHANT' : str(ctx.author), 'BUYER' : str(mtrade['BUYER']), 'OPEN' : True}
                                            update_query = {"$push" : {'MTITLES': selected_title}, "$inc" : {'TAX' : int(sell_price)}}
                                            resp = db.updateTrade(trade_query, update_query)
                                            await button_ctx.send("Traded.")
                                            self.stop = True
                                        elif bvalidation:
                                            trade_query = {'MERCHANT' : str(btrade['MERCHANT']),'BUYER' : str(ctx.author), 'OPEN' : True}
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
                            await button_ctx.send("Done.")
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
            newVault = db.createVault({'OWNER': d['DISNAME']})

    @cog_ext.cog_slash(description="Check all your Arms", guild_ids=main.guild_ids)
    async def arms(self, ctx):
        await ctx.defer()
        query = {'DISNAME': str(ctx.author)}
        d = db.queryUser(query)
        vault = db.queryVault({'OWNER': d['DISNAME']})
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
                        u_vault = db.queryVault({'OWNER': d['DISNAME']})
                        updated_vault = []
                        for arm in u_vault['ARMS']:
                            updated_vault.append(arm['ARM'])
                        
                        sell_price = 0
                        selected_arm = str(button_ctx.origin_message.embeds[0].title)
                        if button_ctx.custom_id == "Equip":
                            if selected_arm in updated_vault:
                                selected_universe = custom_function
                                custom_function.selected_universe = selected_arm
                                user_query = {'DISNAME': str(ctx.author)}
                                response = db.updateUserNoFilter(user_query, {'$set': {'ARM': selected_arm}})
                                await button_ctx.send(f":mechanical_arm: **{selected_arm}** equipped.")
                                self.stop = True
                            else:
                                await button_ctx.send(f"**{selected_arm}** is no longer in your vault.")
                        
                        elif button_ctx.custom_id == "Resell":
                            arm_data = db.queryArm({'ARM': selected_arm})
                            arm_name = arm_data['ARM']
                            sell_price = sell_price + (arm_data['PRICE'] * .30)
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
                                        db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$pull':{'ARMS': {'ARM': str(arm_name)}}})
                                        await main.bless(sell_price, ctx.author)
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
                            dismantle_amount = round(arm_data['PRICE'] * .03)
                            if arm_name == current_arm:
                                await button_ctx.send("You cannot dismantle equipped arms.")
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
                                            query = {'OWNER': str(ctx.author)}
                                            update_query = {'$inc': {'GEMS.$[type].' + "GEMS": dismantle_amount}}
                                            filter_query = [{'type.' + "UNIVERSE": selected_universe}]
                                            response = db.updateVault(query, update_query, filter_query)
                                        else:
                                            response = db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$addToSet':{'GEMS': {'UNIVERSE': selected_universe, 'GEMS': dismantle_amount, 'UNIVERSE_HEART': False, 'UNIVERSE_SOUL': False}}})

                                        db.updateVaultNoFilter({'OWNER': str(ctx.author)},{'$pull':{'ARMS': {'ARM': str(arm_name)}}})
                                        await main.bless(sell_price, ctx.author)
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
                            mtrade = db.queryTrade({'MERCHANT' : str(ctx.author), 'OPEN' : True})
                            mvalidation=False
                            bvalidation=False
                            item_already_in_trade=False
                            if mtrade:
                                if selected_arm in mtrade['MARMS']:
                                    await ctx.send(f"{ctx.author.mention} arm already in **Trade**")
                                    item_already_in_trade=True
                                mvalidation=True
                            else:
                                btrade = db.queryTrade({'BUYER' : str(ctx.author), 'OPEN' : True})
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
                                            trade_query = {'MERCHANT' : str(button_ctx.author), 'BUYER' : str(mtrade['BUYER']), 'OPEN' : True}
                                            update_query = {"$pull" : {'MARMS': selected_arm}, "$inc" : {'TAX' : int(neg_sell_price)}}
                                            resp = db.updateTrade(trade_query, update_query)
                                            await button_ctx.send("Returned.")
                                            self.stop = True
                                        elif bvalidation:
                                            trade_query = {'MERCHANT' : str(btrade['MERCHANT']),'BUYER' : str(button_ctx.author), 'OPEN' : True}
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
                                            trade_query = {'MERCHANT' : str(ctx.author), 'BUYER' : str(mtrade['BUYER']), 'OPEN' : True}
                                            update_query = {"$push" : {'MARMS': selected_arm}, "$inc" : {'TAX' : int(sell_price)}}
                                            resp = db.updateTrade(trade_query, update_query)
                                            await button_ctx.send("Traded.")
                                            self.stop = True
                                        elif bvalidation:
                                            trade_query = {'MERCHANT' : str(btrade['MERCHANT']),'BUYER' : str(ctx.author), 'OPEN' : True}
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
                            await button_ctx.send("Done.")
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
            newVault = db.createVault({'OWNER': d['DISNAME']})

    @cog_ext.cog_slash(description="Check all your Summons", guild_ids=main.guild_ids)
    async def summons(self, ctx):
        await ctx.defer()
        query = {'DISNAME': str(ctx.author)}
        d = db.queryUser(query)
        vault = db.queryVault({'OWNER': d['DISNAME']})
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
                    manage_components.create_button(style=2, label="Exit", custom_id="Exit")
                ]
                custom_action_row = manage_components.create_actionrow(*buttons)

                async def custom_function(self, button_ctx):
                    if button_ctx.author == ctx.author:
                        updated_vault = db.queryVault({'OWNER': d['DISNAME']})
                        sell_price = 0
                        selected_summon = str(button_ctx.origin_message.embeds[0].title)
                        user_query = {'DISNAME': str(ctx.author)}
                        
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
                            mtrade = db.queryTrade({'MERCHANT' : str(ctx.author), 'OPEN' : True})
                            mvalidation=False
                            bvalidation=False
                            item_already_in_trade=False
                            if mtrade:
                                if selected_summon in mtrade['MSUMMONS']:
                                    await ctx.send(f"{ctx.author.mention} summon already in **Trade**")
                                    item_already_in_trade=True
                                mvalidation=True
                            else:
                                btrade = db.queryTrade({'BUYER' : str(ctx.author), 'OPEN' : True})
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
                                            trade_query = {'MERCHANT' : str(button_ctx.author), 'BUYER' : str(mtrade['BUYER']), 'OPEN' : True}
                                            update_query = {"$pull" : {'MSUMMONS': selected_summon}, "$inc" : {'TAX' : int(neg_sell_price)}}
                                            resp = db.updateTrade(trade_query, update_query)
                                            await button_ctx.send("Returned.")
                                            self.stop = True
                                        elif bvalidation:
                                            trade_query = {'MERCHANT' : str(btrade['MERCHANT']),'BUYER' : str(button_ctx.author), 'OPEN' : True}
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
                                            trade_query = {'MERCHANT' : str(ctx.author), 'BUYER' : str(mtrade['BUYER']), 'OPEN' : True}
                                            update_query = {"$push" : {'MSUMMONS': selected_summon}, "$inc" : {'TAX' : int(sell_price)}}
                                            resp = db.updateTrade(trade_query, update_query)
                                            await button_ctx.send("Traded.")
                                            self.stop = True
                                        elif bvalidation:
                                            trade_query = {'MERCHANT' : str(btrade['MERCHANT']),'BUYER' : str(ctx.author), 'OPEN' : True}
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
                                                        
                        elif button_ctx.custom_id =="Exit":
                            await button_ctx.send("Done.")
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

    @cog_ext.cog_slash(description="Check all your Quests", guild_ids=main.guild_ids)
    async def quests(self, ctx):
        await ctx.defer()
        query = {'DISNAME': str(ctx.author)}
        d = db.queryUser(query)
        vault = db.queryVault({'OWNER': d['DISNAME']})
        if not vault['QUESTS']:
            await ctx.send("No Quests available at this time!", hidden=True)
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
                embedVar.set_footer(text="Use /tales to complete daily quest!", icon_url="https://cdn.discordapp.com/emojis/784402243519905792.gif?v=1")
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
                await ctx.send("There's an issue with your Quest list. Check with support.", hidden=True)
                return
        else:
            newVault = db.createVault({'OWNER': d['DISNAME']})

    @cog_ext.cog_slash(description="Check your Balance", guild_ids=main.guild_ids)
    async def balance(self, ctx):
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
            
    @cog_ext.cog_slash(description="Check your Build Presets", guild_ids=main.guild_ids)
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
                                                    await button_ctx.send(response)
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
                await ctx.send("Preset Issue Seek support.", hidden=True)
        else:
            newVault = db.createVault({'OWNER': d['DISNAME']})

    @cog_ext.cog_slash(description="Save your current Build as Preset", guild_ids=main.guild_ids)
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
                await ctx.send("Preset Issue Seek support.", hidden=True)
        else:
            newVault = db.createVault({'OWNER': d['DISNAME']})

    @cog_ext.cog_slash(description="Open Crown Shop", guild_ids=main.guild_ids)
    async def shop(self, ctx):
        try:
            all_universes = db.queryAllUniverse()
            user = db.queryUser({'DISNAME': str(ctx.author)})
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
            
            vault_query = {'OWNER' : str(ctx.author)}
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
                    universe = str(button_ctx.origin_message.embeds[0].title)
                    if button_ctx.custom_id == "title":
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
                        selection = random.randint(1,len(list(list_of_titles)))
                        
                        title = list_of_titles[selection]

                        response = db.updateVaultNoFilter(vault_query,{'$addToSet':{'TITLES': str(title['TITLE'])}})   
                        await main.curse(price, str(ctx.author))
                        await button_ctx.send(f"You purchased **{title['TITLE']}**.")
                        self.stop = True

                    elif button_ctx.custom_id == "arm":
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
                        selection = random.randint(1,len(list(list_of_arms)))

                        arm = list_of_arms[selection]['ARM']

                        if arm not in current_arms:
                            response = db.updateVaultNoFilter(vault_query,{'$addToSet':{'ARMS': {'ARM': str(arm), 'DUR': 25}}})
                            await main.curse(price, str(ctx.author))
                            await button_ctx.send(f"You purchased **{arm}**.")
                            self.stop = True
                        else:
                            update_query = {'$inc': {'ARMS.$[type].' + 'DUR': 10}}
                            filter_query = [{'type.' + "ARM": str(arm)}]
                            resp = db.updateVault(vault_query, update_query, filter_query)
                            await main.curse(price, str(ctx.author))
                            await button_ctx.send(f"You purchased **{arm}**. Increased durability for the arm by 10 as you already own it.")
                            self.stop = True 
                    
                    elif button_ctx.custom_id == "t1card":
                        price = price_adjuster(30000, universe, completed_tales, completed_dungeons)['C1']
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

                        selection = random.randint(0, round(len(list_of_cards)))
                        card = list_of_cards[selection]
                        card_name = card['NAME']
                        tier = 0

                        if card_name in current_cards:
                            await cardlevel(card['NAME'], str(ctx.author), "Purchase")
                            await button_ctx.send(f"You received a level up for **{card_name}**!")
                            await main.curse(price, str(ctx.author))
                            self.stop = True
                            
                        else:
                            response = db.updateVaultNoFilter(vault_query,{'$addToSet': {'CARDS': str(card_name)}})
                            await main.curse(price, str(ctx.author))

                            # Add Card Level config
                            if card_name not in owned_card_levels_list:
                                update_query = {'$addToSet': {
                                    'CARD_LEVELS': {'CARD': str(card_name), 'LVL': 0, 'TIER': int(tier),
                                                    'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0}}}
                                r = db.updateVaultNoFilter(vault_query, update_query)

                            await button_ctx.send(f"You purchased **{card_name}**!")

                            # Add Destiny
                            for destiny in d.destiny:
                                if card_name in destiny["USE_CARDS"] and destiny['NAME'] not in owned_destinies:
                                    db.updateVaultNoFilter(vault_query, {'$addToSet': {'DESTINY': destiny}})
                                    await button_ctx.send(
                                        f"**DESTINY AWAITS!**\n**{destiny['NAME']}** has been added to your vault.", hidden=True)
                            self.stop = True

                    elif button_ctx.custom_id == "t2card":
                        price = price_adjuster(300000, universe, completed_tales, completed_dungeons)['C2']
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

                        selection = random.randint(0, round(len(list_of_cards)))
                        card = list_of_cards[selection]
                        card_name = card['NAME']
                        tier = 0

                        if card_name in current_cards:
                            await cardlevel(card['NAME'], str(ctx.author), "Purchase")
                            await button_ctx.send(f"You received a level up for **{card_name}**!")
                            await main.curse(price, str(ctx.author))
                            self.stop = True
                            
                        else:
                            response = db.updateVaultNoFilter(vault_query,{'$addToSet': {'CARDS': str(card_name)}})
                            await main.curse(price, str(ctx.author))

                            # Add Card Level config
                            if card_name not in owned_card_levels_list:
                                update_query = {'$addToSet': {
                                    'CARD_LEVELS': {'CARD': str(card_name), 'LVL': 0, 'TIER': int(tier),
                                                    'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0}}}
                                r = db.updateVaultNoFilter(vault_query, update_query)

                            await button_ctx.send(f"You purchased **{card_name}**!")

                            # Add Destiny
                            for destiny in d.destiny:
                                if card_name in destiny["USE_CARDS"] and destiny['NAME'] not in owned_destinies:
                                    db.updateVaultNoFilter(vault_query, {'$addToSet': {'DESTINY': destiny}})
                                    await button_ctx.send(
                                        f"**DESTINY AWAITS!**\n**{destiny['NAME']}** has been added to your vault.", hidden=True)
                            self.stop = True

                    elif button_ctx.custom_id == "t3card":
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
                        card_list_response = [x for x in db.queryAllCardsBasedOnUniverse({'UNIVERSE': str(universe), 'TIER': {'$in': acceptable}})]
                        list_of_cards = []
                        for card in card_list_response:
                            if card['AVAILABLE'] and not card['EXCLUSIVE'] and not card['HAS_COLLECTION']:
                                list_of_cards.append(card)

                        if not list_of_cards:
                            await button_ctx.send("There are no cards available for purchase in this range.")
                            self.stop = True
                            return

                        selection = random.randint(0, round(len(list_of_cards)))
                        card = list_of_cards[selection]
                        card_name = card['NAME']
                        tier = 0

                        if card_name in current_cards:
                            await cardlevel(card['NAME'], str(ctx.author), "Purchase")
                            await button_ctx.send(f"You received a level up for **{card_name}**!")
                            await main.curse(price, str(ctx.author))
                            self.stop = True
                            
                        else:
                            response = db.updateVaultNoFilter(vault_query,{'$addToSet': {'CARDS': str(card_name)}})
                            await main.curse(price, str(ctx.author))

                            # Add Card Level config
                            if card_name not in owned_card_levels_list:
                                update_query = {'$addToSet': {
                                    'CARD_LEVELS': {'CARD': str(card_name), 'LVL': 0, 'TIER': int(tier),
                                                    'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0}}}
                                r = db.updateVaultNoFilter(vault_query, update_query)

                            await button_ctx.send(f"You purchased **{card_name}**!")

                            # Add Destiny
                            for destiny in d.destiny:
                                if card_name in destiny["USE_CARDS"] and destiny['NAME'] not in owned_destinies:
                                    db.updateVaultNoFilter(vault_query, {'$addToSet': {'DESTINY': destiny}})
                                    await button_ctx.send(
                                        f"**DESTINY AWAITS!**\n**{destiny['NAME']}** has been added to your vault.", hidden=True)
                            self.stop = True
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
        try:
            all_universes = db.queryAllUniverse()
            user = db.queryUser({'DISNAME': str(ctx.author)})
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
            
            vault_query = {'OWNER' : str(ctx.author)}
            vault = db.altQueryVault(vault_query)
            current_cards = vault['CARDS']
            owned_card_levels_list = []
            for c in vault['CARD_LEVELS']:
                owned_card_levels_list.append(c['CARD'])

            owned_destinies = []
            for destiny in vault['DESTINY']:
                owned_destinies.append(destiny['NAME'])


            embed_list = []
            for universe in available_universes:
                universe_name = universe['TITLE']
                universe_image = universe['PATH']
                embedVar = discord.Embed(title= f"{universe_name}", description=textwrap.dedent(f"""
                Welcome {ctx.author.mention}!
                
                💟 **Universe Heart:** 💎 400,000
                🌹 **Universe Soul:** 💎 800,000
                """), colour=0x7289da)
                embedVar.set_image(url=universe_image)
                embed_list.append(embedVar)

        
            buttons = [
                manage_components.create_button(style=3, label="💟", custom_id="UNIVERSE_HEART"),
                manage_components.create_button(style=1, label="🌹", custom_id="UNIVERSE_SOUL")
            ]

            custom_action_row = manage_components.create_actionrow(*buttons)

            async def custom_function(self, button_ctx):
                if button_ctx.author == ctx.author:
                    universe = str(button_ctx.origin_message.embeds[0].title)
                    if button_ctx.custom_id == "UNIVERSE_HEART":
                        price = 400000
                        response = craft_adjuster(vault, universe, price, button_ctx.custom_id)
                        if response['SUCCESS']:
                            await button_ctx.send(f"{response['MESSAGE']}")
                            self.stop = True
                        else:
                            await button_ctx.send(f"{response['MESSAGE']}")
                            self.stop = True                           

                    if button_ctx.custom_id == "UNIVERSE_SOUL":
                        price = 800000
                        response = craft_adjuster(vault, universe, price, button_ctx.custom_id)
                        if response['SUCCESS']:
                            await button_ctx.send(f"{response['MESSAGE']}")
                            self.stop = True
                        else:
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


def craft_adjuster(vault, universe, price, item):
    try:
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

        if has_gems_for:
            if gems >= price:
                if item in item_bools:
                    query = {'OWNER': str(vault['OWNER'])}
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
    c1 = 30000
    c2 = 300000
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
        c1 = round(30000 * .50)
        c2 = round(300000 * 50)
        c3 = round(6000000 * .50)
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