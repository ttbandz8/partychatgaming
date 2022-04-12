# from operator import is_
# from urllib import response
import db
import time
import classes as data
import bot as main
import messages as m
from discord.ext import commands
import numpy as np
import help_commands as h
import destiny as d
# Converters
from discord import User
from discord_slash import SlashCommand
from discord_slash.utils import manage_components
from discord_slash.model import ButtonStyle
import textwrap
from discord_slash import cog_ext, SlashContext
from dinteractions_Paginator import Paginator
from discord_slash.utils.manage_commands import create_option, create_choice
import os
import logging
import textwrap
import unique_traits as ut
now = time.asctime()


print("Crown Utilities initiated")

def storage_limit_hit(player_info, vault):
    storage_amount = len(vault['STORAGE'])
    storage_allowed_amount = player_info['STORAGE_TYPE'] * 15
    limit_hit = False

    if storage_amount >= storage_allowed_amount:
        limit_hit = True
    return limit_hit


async def store_drop_card(player, card_name, card_universe, vault, owned_destinies, bless_amount_if_max_cards, bless_amount_if_card_owned, mode, is_shop, price):
    try:
        user = await main.bot.fetch_user(player)
        player_info = db.queryUser({"DID": str(player)})
        storage_limit_has_been_hit = storage_limit_hit(player_info, vault)

        current_storage = vault['STORAGE']
        current_cards_in_vault = vault['CARDS']

        vault_query = {'DID': str(player)}
        hand_length = len(current_cards_in_vault)


        list1 = current_cards_in_vault
        list2 = current_storage
        list2.extend(list1)
        current_cards = list2

        card_owned = False
        for owned_card in current_cards:
            if owned_card == card_name:
                card_owned = True

        if card_owned:
            if is_shop:
                await cardlevel(card_name, player, mode, card_universe)
                await curse(int(price), str(player))
                return f"You earned experience points for 🎴: **{card_name}**"
            await cardlevel(card_name, player, mode, card_universe)
            await bless(int(bless_amount_if_card_owned), player)
            return f"You earned experience points for 🎴: **{card_name}** & :coin: **{'{:,}'.format(bless_amount_if_card_owned)}**"
        else:
            if hand_length < 25:
                response = db.updateVaultNoFilter(vault_query,{'$addToSet': {'CARDS': str(card_name)}})
                if is_shop:
                    await curse(int(price), str(player))

                # Add Card Level config
                if not card_owned:
                    update_query = {'$addToSet': {
                        'CARD_LEVELS': {'CARD': str(card_name), 'LVL': 0, 'TIER': 0,
                                        'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0}}}
                    r = db.updateVaultNoFilter(vault_query, update_query)

                # Add Destiny
                for destiny in d.destiny:
                    if card_name in destiny["USE_CARDS"] and destiny['NAME'] not in owned_destinies:
                        db.updateVaultNoFilter(vault_query, {'$addToSet': {'DESTINY': destiny}})
                        await user.send(
                            f"**DESTINY AWAITS!**\n**{destiny['NAME']}** has been added to your vault.")

                return f"You earned 🎴: **{card_name}**!"

            
            if hand_length >= 25 and not storage_limit_has_been_hit:
                if is_shop:
                    response = await route_to_storage(player, card_name, current_cards, card_owned, price, card_universe, owned_destinies, "Purchase")
                    return response
                else:
                    update_query = {'$addToSet': {
                        'CARD_LEVELS': {'CARD': card_name, 'LVL': 0, 'TIER': 0, 'EXP': 0, 'HLT': 0,
                                        'ATK': 0, 'DEF': 0, 'AP': 0}}}
                    response = db.updateVaultNoFilter(vault_query, {'$addToSet': {'STORAGE': card_name}})
                    r = db.updateVaultNoFilter(vault_query, update_query)
                    message = ""
                    for destiny in d.destiny:
                        if card_name in destiny["USE_CARDS"] and destiny['NAME'] not in owned_destinies:
                            db.updateVaultNoFilter(vault_query, {'$addToSet': {'DESTINY': destiny}})
                            await user.send(
                                f"**DESTINY AWAITS!**\n**{destiny['NAME']}** has been added to your vault.")

                    return f"**{card_name}** has been added to your storage 💼!\n{message}"


            if hand_length >= 25 and storage_limit_has_been_hit:
                if is_shop:
                    return "You have max amount of Cards. Transaction cancelled."   
                else:
                    await bless(int(bless_amount_if_max_cards), player)
                    return f"You're maxed out on Cards! You earned :coin: {str(bless_amount_if_max_cards)} instead!"

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
            'player': str(player),
            'type': type(ex).__name__,
            'message': str(ex),
            'trace': trace
        }))
        # guild = main.bot.get_guild(543442011156643871)
        # channel = guild.get_channel(957061470192033812)
        # await channel.send(f"'PLAYER': **{str(player)}**, TYPE: {type(ex).__name__}, MESSAGE: {str(ex)}, TRACE: {trace}")


async def route_to_storage(player, card_name, current_cards, card_owned, price, universe, owned_destinies, mode):
    try:
        user = await main.bot.fetch_user(player)
        msg = ""

        user_query = {"DID": str(player)}
        vault_query = {"DID": str(player)}
        update_query = {
            "$addToSet": {"STORAGE": card_name}
        }
        update_storage = db.updateVaultNoFilter(user_query, update_query)
        

        if card_owned:
            await cardlevel(card_name, str(player), mode, universe)
            msg = f"You received a level up for **{card_name}**!"
            await curse(int(price), str(player))
            return msg
        else:
            await curse(int(price), str(player))

            update_query = {'$addToSet': {
                'CARD_LEVELS': {'CARD': str(card_name), 'LVL': 0, 'TIER': 0,
                                'EXP': 0, 'HLT': 0, 'ATK': 0, 'DEF': 0, 'AP': 0}}}
            r = db.updateVaultNoFilter(vault_query, update_query)

            msg = f"**{card_name}** has been purchased and added to Storage!\n"

            for destiny in d.destiny:
                if card_name in destiny["USE_CARDS"] and destiny['NAME'] not in owned_destinies:
                    db.updateVaultNoFilter(vault_query, {'$addToSet': {'DESTINY': destiny}})
                    await user.send(
                        f"**DESTINY AWAITS!**\n**{destiny['NAME']}** has been added to your vault.")


            msg = f"**{card_name}** has been purchased and added to Storage!"
            return msg

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
            'player': str(player),
            'type': type(ex).__name__,
            'message': str(ex),
            'trace': trace
        }))
        # guild = main.bot.get_guild(543442011156643871)
        # channel = guild.get_channel(957061470192033812)
        # await channel.send(f"'PLAYER': **{str(player)}**, TYPE: {type(ex).__name__}, MESSAGE: {str(ex)}, TRACE: {trace}")


# async def bless_all(ctx, amount: int):
#     guild = main.bot.get_guild(main.guild_id)
#     channel = guild.get_channel(main.guild_channel)
#     message_channel = channel
#     try:
#         all_users = db.queryAllVault()
#         for user in all_users:
#             await bless(amount, user['DID'])
#         await ctx.send(f"All Crown Unlimited Players have been blessed. 👑")
#     except Exception as e:
#     print(e)


async def corrupted_universe_handler(ctx, universe, difficulty):
    try:
        # if universe['CORRUPTION_LEVEL'] == 499:
        # updated_corruption_level = db.updateUniverse({'TITLE': universe['TITLE']}, {'$inc': {'CORRUPTION_LEVEL': 1}})
        query = {"DID": str(ctx.author.id)}
        vault = db.queryVault(query)
        
        gem_list = vault['GEMS']
        gem_reward = 80000
        if difficulty == "HARD":
            gem_reward = 180000

        if gem_list:
            for uni in gem_list:
                if uni['UNIVERSE'] == universe:
                    update_query = {
                        '$inc': {'GEMS.$[type].' + "GEMS": gem_reward}
                    }
                    filter_query = [{'type.' + "UNIVERSE": uni['UNIVERSE']}]
                    res = db.updateVault(query, update_query, filter_query)
                    return f"You earned 💎 {'{:,}'.format(gem_reward)}"
        else:
            return "You must dismantle a card from this universe to enable crafting."

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
            'player': str(player),
            'type': type(ex).__name__,
            'message': str(ex),
            'trace': trace
        }))

    

async def cardlevel(card: str, player, mode: str, universe: str):
    try:
        vault = db.queryVault({'DID': str(player)})
        player_info = db.queryUser({'DID': str(player)})
        guild_buff = await guild_buff_update_function(player_info['TEAM'].lower())
        if player_info['DIFFICULTY'] == "EASY":
            return


        card_uni = db.queryCard({'NAME': card})['UNIVERSE']
        user = await main.bot.fetch_user(str(player))

        cardinfo = {}
        for x in vault['CARD_LEVELS']:
            if x['CARD'] == str(card):
                cardinfo = x
        
        has_universe_heart = False
        has_universe_soul = False

        if universe != "n/a":
            for gems in vault['GEMS']:
                if gems['UNIVERSE'] == card_uni and gems['UNIVERSE_HEART']:
                    has_universe_heart = True
                if gems['UNIVERSE'] == card_uni and gems['UNIVERSE_SOUL']:
                    has_universe_soul = True

        lvl = cardinfo['LVL']
        lvl_req = 150
        exp = cardinfo['EXP']
        exp_gain = 0
        if has_universe_soul:
            if mode == "Dungeon":
                exp_gain = 65
            if mode == "Tales":
                exp_gain = 35
            if mode == "Purchase":
                exp_gain = 150
        else:
            if mode == "Dungeon":
                exp_gain = 30
            if mode == "Tales":
                exp_gain = 15
            if mode == "Purchase":
                exp_gain = 150


        hlt_buff = 0
        atk_def_buff = 0
        ap_buff = 0

        if lvl < 200:
            if guild_buff:
                if guild_buff['Level']:
                    exp_gain = 150
                    update_team_response = db.updateTeam(guild_buff['QUERY'], guild_buff['UPDATE_QUERY'])

            # Experience Code
            if exp < (lvl_req - 1):
                query = {'DID': str(player)}
                update_query = {'$inc': {'CARD_LEVELS.$[type].' + "EXP": exp_gain}}
                filter_query = [{'type.' + "CARD": str(card)}]
                response = db.updateVault(query, update_query, filter_query)

            # Level Up Code
            if exp >= (lvl_req - exp_gain):
                if (lvl + 1) % 2 == 0:
                    atk_def_buff = 1
                if (lvl + 1) % 3 == 0:
                    ap_buff = 1
                if (lvl + 1) % 20 == 0:
                    hlt_buff = 25
                query = {'DID': str(player)}
                update_query = {'$set': {'CARD_LEVELS.$[type].' + "EXP": 0},
                                '$inc': {'CARD_LEVELS.$[type].' + "LVL": 1, 'CARD_LEVELS.$[type].' + "ATK": atk_def_buff,
                                        'CARD_LEVELS.$[type].' + "DEF": atk_def_buff,
                                        'CARD_LEVELS.$[type].' + "AP": ap_buff, 'CARD_LEVELS.$[type].' + "HLT": hlt_buff}}
                filter_query = [{'type.' + "CARD": str(card)}]
                response = db.updateVault(query, update_query, filter_query)
                await user.send(f"**{card}** leveled up!")

        if lvl < 500 and lvl >= 200 and has_universe_heart:
            if guild_buff:
                if guild_buff['Level']:
                    exp_gain = 150
                    update_team_response = db.updateTeam(guild_buff['QUERY'], guild_buff['UPDATE_QUERY'])

            # Experience Code
            if exp < (lvl_req - 1):
                query = {'DID': str(player)}
                update_query = {'$inc': {'CARD_LEVELS.$[type].' + "EXP": exp_gain}}
                filter_query = [{'type.' + "CARD": str(card)}]
                response = db.updateVault(query, update_query, filter_query)

            # Level Up Code
            if exp >= (lvl_req - exp_gain):
                if (lvl + 1) % 2 == 0:
                    atk_def_buff = 1
                if (lvl + 1) % 3 == 0:
                    ap_buff = 1
                if (lvl + 1) % 20 == 0:
                    hlt_buff = 25
                query = {'DID': str(player)}
                update_query = {'$set': {'CARD_LEVELS.$[type].' + "EXP": 0},
                                '$inc': {'CARD_LEVELS.$[type].' + "LVL": 1, 'CARD_LEVELS.$[type].' + "ATK": atk_def_buff,
                                        'CARD_LEVELS.$[type].' + "DEF": atk_def_buff,
                                        'CARD_LEVELS.$[type].' + "AP": ap_buff, 'CARD_LEVELS.$[type].' + "HLT": hlt_buff}}
                filter_query = [{'type.' + "CARD": str(card)}]
                response = db.updateVault(query, update_query, filter_query)
                await user.send(f"**{card}** leveled up!")
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
            'player': str(player),
            'type': type(ex).__name__,
            'message': str(ex),
            'trace': trace
        }))
        # guild = main.bot.get_guild(543442011156643871)
        # channel = guild.get_channel(957061470192033812)
        # await channel.send(f"'PLAYER': **{str(player)}**, TYPE: {type(ex).__name__}, MESSAGE: {str(ex)}, TRACE: {trace}")


async def guild_buff_update_function(team):
    try:
        team_query = {'TEAM_NAME': team.lower()}
        team_info = db.queryTeam(team_query)
        if team_info:
            guild_buff_count = len(team_info['GUILD_BUFFS'])
            guild_buff_active = team_info['GUILD_BUFF_ON']
            guild_buffs = team_info['GUILD_BUFFS']


            if guild_buff_active:
                filter_query = [{'type.' + "TYPE": guild_buff_active}]
                guild_buff_update_query = {}
                quest_buff = False
                rift_buff = False
                level_buff = False
                stat_buff = False
                index = 0

                active_guild_buff = team_info['ACTIVE_GUILD_BUFF']
                for buff in guild_buffs:
                    if buff['TYPE'] == active_guild_buff:
                        index = guild_buffs.index(buff)

                        if buff['TYPE'] == "Rift":
                            rift_buff = True
                        
                        if buff['TYPE'] == "Quest":
                            quest_buff = True

                        if buff['TYPE'] == "Level":
                            level_buff = True

                        if buff['TYPE'] == "Stat":
                            stat_buff = True
                        
                        if buff['USES'] == 1:
                            
                            if guild_buff_count == 1:
                                guild_buff_update_query = {
                                        '$pull': {
                                            'GUILD_BUFFS': {'TYPE': active_guild_buff, 'USES': 1}
                                        },
                                        '$set': {
                                            'GUILD_BUFF_ON': False,
                                            'GUILD_BUFF_AVAILABLE': False,
                                            'ACTIVE_GUILD_BUFF': "",
                                        },
                                        '$push': {
                                            'TRANSACTIONS': f"{active_guild_buff} Buff has been used up"
                                        }
                                    }

                            else:
                                guild_buff_update_query = {
                                        "$pull": {
                                            'GUILD_BUFFS': {'TYPE': active_guild_buff, 'USES': 1}
                                        },
                                        '$set': {
                                            'GUILD_BUFF_ON': False,
                                            'ACTIVE_GUILD_BUFF': "",
                                        },
                                        '$push': {
                                            'TRANSACTIONS': f"{active_guild_buff} Buff has been used up"
                                        }
                                    }
                        
                        else:
                            guild_buff_update_query = {
                                '$inc': {
                                    f"GUILD_BUFFS.{index}.USES": -1
                                }

                            }
                
                response = {
                    'Quest': quest_buff,
                    'Rift': rift_buff,
                    'Level': level_buff,
                    'Stat': stat_buff,
                    'QUERY': team_query,
                    'UPDATE_QUERY': guild_buff_update_query,
                    'FILTER_QUERY': filter_query
                    }
                
                return response
            else:
                return False                     
        else:
            return False
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
            'team': str(team),
            'type': type(ex).__name__,
            'message': str(ex),
            'trace': trace
        }))
        # guild = main.bot.get_guild(543442011156643871)
        # channel = guild.get_channel(957061470192033812)
        # await channel.send(f"'TEAM': **{str(team)}**, TYPE: {type(ex).__name__}, MESSAGE: {str(ex)}, TRACE: {trace}")


async def bless(amount, user):
    try:
        blessAmount = amount
        posBlessAmount = 0 + abs(int(blessAmount))
        query = {'DID': str(user)}
        vaultOwner = db.queryUser(query)
        if vaultOwner:
            vault = db.queryVault({'DID' : vaultOwner['DID']})
            update_query = {"$inc": {'BALANCE': posBlessAmount}}
            db.updateVaultNoFilter(vault, update_query)
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


async def blessteam(amount, team):
    try:
        blessAmount = amount
        posBlessAmount = 0 + abs(int(blessAmount))
        query = {'TEAM_NAME': str(team)}
        team_data = db.queryTeam(query)
        if team_data:
            update_query = {"$inc": {'BANK': posBlessAmount}}
            db.updateTeam(query, update_query)
        else:
            print("Cannot find Guild")
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


async def curseteam(amount, team):
    try:
        curseAmount = amount
        negCurseAmount = 0 - abs(int(curseAmount))
        query = {'TEAM_NAME': str(team)}
        team_data = db.queryTeam(query)
        if team_data:
            update_query = {"$inc": {'BANK': int(negCurseAmount)}}
            db.updateTeam(query, update_query)
        else:
            print("cant find team")
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


async def blessfamily(amount, family):
    try:
        blessAmount = amount
        posBlessAmount = 0 + abs(int(blessAmount))
        query = {'HEAD': str(family)}
        family_data = db.queryFamily(query)
        if family_data:
            house = family_data['HOUSE']
            house_data = db.queryHouse({'HOUSE': house})
            multiplier = house_data['MULT']
            posBlessAmount = posBlessAmount * multiplier
            update_query = {"$inc": {'BANK': posBlessAmount}}
            db.updateFamily(query, update_query)
        else:
            print("Cannot find family")
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


async def blessfamily_Alt(amount, family):
    try:
        blessAmount = amount
        posBlessAmount = 0 + abs(int(blessAmount))
        query = {'HEAD': str(family)}
        family_data = db.queryFamily(query)
        if family_data:
            house = family_data['HOUSE']
            house_data = db.queryHouse({'HOUSE': house})
            posBlessAmount = posBlessAmount
            update_query = {"$inc": {'BANK': posBlessAmount}}
            db.updateFamily(query, update_query)
        else:
            print("Cannot find family")
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


async def cursefamily(amount, family):
    try:
        curseAmount = amount
        negCurseAmount = 0 - abs(int(curseAmount))
        query = {'HEAD': str(family)}
        family_data = db.queryFamily(query)
        if family_data:
            update_query = {"$inc": {'BANK': int(negCurseAmount)}}
            db.updateFamily(query, update_query)
        else:
            print("cant find family")
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


async def blessguild(amount, guild):
    try:
        blessAmount = amount
        posBlessAmount = 0 + abs(int(blessAmount))
        query = {'GNAME': str(guild)}
        guild_data = db.queryGuildAlt(query)
        if guild_data:
            hall = guild_data['HALL']
            hall_data = db.queryHall({'HALL': hall})
            multiplier = hall_data['MULT']
            posBlessAmount = posBlessAmount * multiplier
            query = {'GNAME': str(guild_data['GNAME'])}
            update_query = {"$inc": {'BANK': int(posBlessAmount)}}
            db.updateGuildAlt(query, update_query)
        else:
            print("Cannot find guild")
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


async def curseguild(amount, guild):
    try:
        curseAmount = amount
        negCurseAmount = 0 - abs(int(curseAmount))
        query = {'GNAME': str(guild)}
        guild_data = db.queryGuildAlt(query)
        if guild_data:
            query = {'GNAME':str(guild_data['GNAME'])}
            update_query = {"$inc": {'BANK': int(negCurseAmount)}}
            db.updateGuildAlt(query, update_query)
        else:
            print("cant find guild")
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


async def curse(amount, user):
    try:
        curseAmount = int(amount)
        negCurseAmount = 0 - abs(int(curseAmount))
        query = {'DID': str(user)}
        vaultOwner = db.queryUser(query)
        if vaultOwner:
            vault = db.queryVault({'DID' : vaultOwner['DID']})
            update_query = {"$inc": {'BALANCE': int(negCurseAmount)}}
            db.updateVaultNoFilter(vault, update_query)
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


async def player_check(ctx):
    query = {'DID': str(ctx.author.id)}
    valid = db.queryUser(query)
    if valid:
        return True
    else:
        await ctx.send(f"{ctx.author.mention}, you must register using /register to play Crown Unlimited.")
        return False