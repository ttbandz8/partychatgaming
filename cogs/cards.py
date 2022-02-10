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
import random
from .crownunlimited import showcard, cardback, enhancer_mapping, enhancer_suffix_mapping, passive_enhancer_suffix_mapping
from discord_slash import cog_ext, SlashContext
from discord_slash import SlashCommand
from discord_slash.utils import manage_components
from discord_slash.model import ButtonStyle
from dinteractions_Paginator import Paginator


class Cards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cards Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @cog_ext.cog_slash(description="Equip a Card", guild_ids=main.guild_ids)
    async def equipcard(self, ctx, card: str):
        card_name = card
        user_query = {'DID': str(ctx.author.id)}
        user = db.queryUser(user_query)

        vault_query = {'OWNER': str(ctx.author)}
        vault = db.altQueryVault(vault_query)

        resp = db.queryCard({'NAME': {"$regex": f"^{str(card)}$", "$options": "i"}})

        card_name = resp["NAME"]
        # Do not Check Tourney wins
        if card_name in vault['CARDS']:
            response = db.updateUserNoFilter(user_query, {'$set': {'CARD': str(card_name)}})
            await ctx.send(response)
        else:
            await ctx.send(m.USER_DOESNT_HAVE_THE_CARD, hidden=True)

    @cog_ext.cog_slash(description="View a Card", guild_ids=main.guild_ids)
    async def viewcard(self, ctx, card: str):
        card_name = card
        query = {'DID': str(ctx.author.id)}
        d = db.queryUser(query)
        card = db.queryCard({'NAME': {"$regex": f"^{str(card_name)}$", "$options": "i"}})
        try:
            if card:
                o_card = card['NAME']
                o_card_path = card['PATH']
                o_price = card['PRICE']
                o_exclusive = card['EXCLUSIVE']
                o_available = card['AVAILABLE']
                o_is_skin = card['IS_SKIN']
                o_skin_for = card['SKIN_FOR']
                o_max_health = card['HLT']
                o_health = card['HLT']
                o_stamina = card['STAM']
                o_max_stamina = card['STAM']
                o_moveset = card['MOVESET']
                o_attack = card['ATK']
                o_defense = card['DEF']
                o_type = card['TYPE']
                o_passive = card['PASS'][0]
                o_speed = card['SPD']
                o_show = card['UNIVERSE']
                o_has_collection = card['HAS_COLLECTION']
                traits = ut.traits
                show_img = db.queryUniverse({'TITLE': o_show})['PATH']
                o_collection = card['COLLECTION']
                performance_mode = d['PERFORMANCE']
                resolved = False
                focused = False
                dungeon = False
                title = {'TITLE': 'CARD PREVIEW'}
                arm = {'ARM': 'CARD PREVIEW'}

                if o_show == "Unbound":
                    await ctx.send("You cannot view this card at this time. ", hidden=True)
                    return

                price_message = ""
                card_icon = ""
                if o_is_skin:
                    price_message = "Card Skin"
                    card_icon = f"💎"
                elif o_exclusive or o_has_collection:
                    if o_has_collection == True:
                        price_message = "Destiny Only"
                        card_icon = f"✨"
                    else:
                        price_message = "Dungeon Only"
                        card_icon = f"🔥"
                        dungeon = True
                elif o_exclusive == False and o_available == False and o_has_collection == False:
                    price_message = "Boss Only"
                    card_icon = f"👹"
                else:
                    price_message = f"Shop & Drop"
                    card_icon = f"🎴"
                att = 0
                defe = 0
                turn = 0
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

                passive_name = list(o_passive.keys())[0]
                passive_num = list(o_passive.values())[0]
                passive_type = list(o_passive.values())[1]

                o_1 = o_moveset[0]
                o_2 = o_moveset[1]
                o_3 = o_moveset[2]
                o_enhancer = o_moveset[3]

                # Move 1
                move1 = list(o_1.keys())[0]
                move1ap = list(o_1.values())[0]
                move1_stamina = list(o_1.values())[1]

                # Move 2
                move2 = list(o_2.keys())[0]
                move2ap = list(o_2.values())[0]
                move2_stamina = list(o_2.values())[1]

                # Move 3
                move3 = list(o_3.keys())[0]
                move3ap = list(o_3.values())[0]
                move3_stamina = list(o_3.values())[1]

                # Move Enhancer
                move4 = list(o_enhancer.keys())[0]
                move4ap = list(o_enhancer.values())[0]
                move4_stamina = list(o_enhancer.values())[1]
                move4enh = list(o_enhancer.values())[2]
                active_pet = {}
                pet_ability_power = 0
                card_exp = 150


                message = ""
                tip = ""
                if o_is_skin:
                    message = f"{o_card} is a card Skin. "
                    tip = f"Earn the {o_skin_for} card and use gems to unlock this Skin!"
                elif o_has_collection == True or dungeon == True:
                    if o_has_collection:
                        message = f"{o_card} is a Destiny card. "
                        tip = f"Complete {o_show} Destiny: {o_collection} to unlock this card."
                    else:
                        message = f"{o_card} is a Dungeon card. "
                        tip = f"Find this card in the {o_show} Dungeon"
                elif o_has_collection == False and o_available == False and o_exclusive == False:
                    message = f"{o_card} is a Boss card. "
                    tip = f"Defeat {o_show} Boss to earn this card."
                elif o_attack > o_defense:
                    message = f"{o_card} is an offensive card. "
                    tip = f"Tip: Equipping {o_show} /titles and defensive /arms would help boost survivability"
                elif o_defense > o_attack:
                    message = f"{o_card} is a defensive card. "
                    tip = f"Tip: Equipping {o_show} /titles and offensive /arms would help boost killability"
                else:
                    message = f"{o_card} is a balanced card. "
                    tip = f"Tip: Equip {o_show} /titles and /arms that will maximize your Enhancer"

                
                if performance_mode:
                    embedVar = discord.Embed(title=f"{card_icon} {price_message} {o_card}", description=textwrap.dedent(f"""\
                    :mahjong: {card['TIER']}
                    ❤️ {o_max_health}
                    🗡️ {o_attack}
                    🛡️ {o_defense}
                    🏃 {o_speed}

                    🩸 {passive_name}: {passive_type} {passive_num}{passive_enhancer_suffix_mapping[passive_type]}                
                    
                    💥 {move1}: {move1ap}
                    ☄️ {move2}: {move2ap}
                    🏵️ {move3}: {move3ap}
                    🦠 {move4}: {move4enh} {move4ap} {passive_enhancer_suffix_mapping[move4enh]}   

                    ♾️ {traitmessage}
                    """), colour=000000)
                    embedVar.set_footer(text=f"{tip}")
                    await ctx.send(embed=embedVar)

                else:
                    card_file = showcard(card, o_max_health, o_health, o_max_stamina, o_stamina, resolved, title, focused,
                                        o_attack, o_defense, turn, move1ap, move2ap, move3ap, move4ap, move4enh, 0, None)

                    embedVar = discord.Embed(title=f"", colour=000000)
                    embedVar.set_image(url="attachment://image.png")
                    embedVar.set_thumbnail(url=show_img)
                    embedVar.set_author(name=textwrap.dedent(f"""\
                    {card_icon} {price_message}
                    Passive & Universe Trait
                    🩸 {passive_name}: {passive_type} {passive_num}{passive_enhancer_suffix_mapping[passive_type]}
                    ♾️ {traitmessage}
                    🏃 {o_speed}
                    """))
                    embedVar.set_footer(text=f"{tip}")

                    await ctx.send(file=card_file, embed=embedVar)
            else:
                await ctx.send(m.CARD_DOESNT_EXIST, hidden=True)
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
            return


def setup(bot):
    bot.add_cog(Cards(bot))
