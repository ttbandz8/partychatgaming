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
from collections import ChainMap
import DiscordUtils
from .crownunlimited import showcard
import random

emojis = ['👍', '👎']

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Profile Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @commands.command()
    async def d(self, ctx, user: User, args):
        if args == 'IWANTTODELETEMYACCOUNT':
            if str(ctx.author) == str(user):
                query = {'DISNAME': str(ctx.author)}
                user_is_validated = db.queryUser(query)
                if user_is_validated:

                    accept = await ctx.send(f"{ctx.author.mention}, are you sure you want to delete your account? " + "\n" + "All of your wins, tournament wins, shop purchases and other earnings will be removed from the system can can not be recovered. ", delete_after=10)
                    for emoji in emojis:
                        await accept.add_reaction(emoji)

                    def check(reaction, user):
                        return user == ctx.author and str(reaction.emoji) == '👍'

                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)

                        delete_user_resp = db.deleteUser(query)
                        vault = db.queryVault({'OWNER': user_is_validated['DISNAME']})
                        if vault:
                            db.deleteVault(vault)
                        else:
                            await ctx.send(delete_user_resp, delete_after=5)
                    except:
                        await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=3)
                
            else:
                await ctx.send("Invalid command", delete_after=5)

    @commands.command()
    async def build(self, ctx):
        query = {'DISNAME': str(ctx.author)}
        d = db.queryUser(query)
        card = db.queryCard({'NAME':str(d['CARD'])})
        title = db.queryTitle({'TITLE': str(d['TITLE'])})
        arm = db.queryArm({'ARM': str(d['ARM'])})
        vault = db.queryVault({'OWNER': d['DISNAME']})
        if card:
            o_card = card['NAME']
            o_card_path=card['PATH']
            o_max_health = card['HLT']
            o_health = card['HLT']
            o_stamina = card['STAM']
            o_max_stamina = card['STAM']
            o_moveset = card['MOVESET']
            o_attack = card['ATK']
            o_defense = card['DEF']
            o_type = card['TYPE']
            o_accuracy = card['ACC']
            o_passive = card['PASS'][0]
            o_speed = card['SPD']
            o_show = card['UNIVERSE']
            o_collection = card['COLLECTION']

            pets = vault['PETS']
            active_pet = {}
            pet_names = []

            for pet in pets:
                pet_names.append(pet['NAME'])
                if pet['NAME'] == d['PET']:
                    active_pet = pet

            pet_ability_power = list(active_pet.values())[3]

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


            resolved = False
            focused = False
            cardtitle = {'TITLE': 'CARD PREVIEW'}
            card_file = showcard(card, o_max_health, o_health, o_max_stamina, o_stamina, resolved, cardtitle, focused)

            passive_name = list(o_passive.keys())[0]
            passive_num = list(o_passive.values())[0]
            passive_type = list(o_passive.values())[1]

            embedVar = discord.Embed(title=f"{o_card}".format(self), colour=000000)
            embedVar.add_field(name=f"TITLE", value=f"`{title_name}`: Increase `{title_passive_type}` by `{title_passive_value}`")
            embedVar.add_field(name=f"ARM", value=f"`{arm_name}`: Increase `{arm_passive_type}` by `{arm_passive_value}`")
            embedVar.add_field(name=f"PET", value=f"`{active_pet['NAME']}`: Increase `{active_pet['TYPE']}` by `{pet_ability_power}`")
            embedVar.set_thumbnail(url=active_pet['PATH'])
            embedVar.set_image(url=o_card_path)
            embedVar.add_field(name="Health", value=f"`{o_max_health}`")
            embedVar.add_field(name="Stamina", value=f"`{o_max_stamina}`")
            embedVar.add_field(name="Attack", value=f"`{o_attack}`")
            embedVar.add_field(name="Defense", value=f"`{o_defense}`")
            embedVar.add_field(name="Speed", value=f"`{o_speed}`")
            embedVar.add_field(name="Unique Passive", value=f"`{passive_name}`: Increases `{passive_type} by {passive_num}`", inline=False)
            embedVar.add_field(name=f"{move1}", value=f"Power: `{move1ap}`", inline=False)
            embedVar.add_field(name=f"{move2}", value=f"Power: `{move2ap}`", inline=False)
            embedVar.add_field(name=f"{move3}", value=f"Power: `{move3ap}`", inline=False)
            embedVar.add_field(name=f"{move4}", value=f"`Enhancer`: Increases `{move4enh} by {move4ap}`", inline=False)
            embedVar.add_field(name="Unique Passive", value=f"`{passive_name}`: Increases `{passive_type} by {passive_num}`", inline=False)

            await ctx.send(embed=embedVar)
        else:
            await ctx.send(m.USER_NOT_REGISTERED, delete_after=3)

    @commands.command()
    async def vault(self, ctx):
        query = {'DISNAME': str(ctx.author)}
        d = db.queryUser(query)
        pet_name = d['PET']
        pet_query = {'PET': str(pet_name)}
        p = db.queryPet(pet_query)
        vault = db.queryVault({'OWNER': d['DISNAME']})
        if vault:
            name = d['DISNAME'].split("#",1)[0]
            avatar = d['AVATAR']
            balance = vault['BALANCE']
            cards = vault['CARDS']
            titles = vault['TITLES']
            arms = vault['ARMS']
            pets = vault['PETS']
            active_pet = {}
            pet_names = []

            for pet in pets:
                pet_names.append(pet['NAME'])
                if pet['NAME'] == pet_name:
                    active_pet = pet
       

            embedVar1 = discord.Embed(title= f"My Cards\n:coin:{'{:,}'.format(balance)}", description="`.equipcard name` -  Select Your Card\n`.viewcard card name` - View Cards", colour=0x7289da)
            embedVar1.set_thumbnail(url=avatar)
            embedVar1.add_field(name="Cards" + " :fireworks:", value=" | ".join(cards))

            embedVar2 = discord.Embed(title= f"My Titles\n:coin:{'{:,}'.format(balance)}", description="`.equiptitle name` - Select Your Title\n`.viewtitle title name` - View Title Stats", colour=0x7289da)
            embedVar2.set_thumbnail(url=avatar)
            embedVar2.add_field(name="Titles" + " :fireworks:", value=" | ".join(titles))

            embedVar3 = discord.Embed(title= f"My Arms\n:coin:{'{:,}'.format(balance)}", description="`.equiparm name` - Select Your Arm\n`.viewarm arm name` - View Arm Stats", colour=0x7289da)
            embedVar3.set_thumbnail(url=avatar)
            embedVar3.add_field(name="Arms" + " :fireworks:", value=" | ".join(arms))

            embedVar4 = discord.Embed(title= f"Pets:feet:\nLevel {active_pet['LVL']}: {active_pet['NAME']}-{active_pet['EXP']}XP", description="`.equippet name` - Select Your Pet\n`.viewpet Pet name` - View Pet Stats", colour=0x7289da)
            embedVar4.set_thumbnail(url=avatar)
            embedVar4.add_field(name="Pets" + " :fireworks:", value=" | ".join(pet_names))

            paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
            paginator.add_reaction('⏮️', "first")
            paginator.add_reaction('⏪', "back")
            paginator.add_reaction('🔐', "lock")
            paginator.add_reaction('⏩', "next")
            paginator.add_reaction('⏭️', "last")
            embeds = [embedVar1, embedVar2, embedVar3, embedVar4]
            await paginator.run(embeds)
        else:
            newVault = db.createVault({'OWNER': d['DISNAME']})

    @commands.command()
    async def shop(self, ctx):
        all_universes = db.queryAllUniverse()
        user = db.queryUser({'DISNAME': str(ctx.author)})
        available_universes = []
        for uni in all_universes:
            if uni['PREREQUISITE'] in user['CROWN_TALES']:
                available_universes.append(uni['TITLE'])
        
        # Pull all cards that don't require tournaments
        resp = db.queryShopCards()

        #
        vault_query = {'OWNER' : str(ctx.author)}
        vault = db.altQueryVault(vault_query)
        cards = []
        card_text_list = []
        for card in resp:
            if card['UNIVERSE'] in available_universes:
                # Don't produce cards you can't afford
                if card['PRICE'] != 0 and card['PRICE'] < (vault['BALANCE'] + 500) and card['AVAILABLE']:
                    if card['NAME'] not in vault['CARDS']:
                        cards.append({'NAME': card['NAME'], 'PRICE': card['PRICE'], 'UNIVERSE': card['UNIVERSE'], 'STOCK': card['STOCK']})
        
        random_cards = random.sample(cards, min(len(cards), 10))
        for card in random_cards:
            if card['STOCK'] == 0:
                card_text_list.append(f"{card['NAME']}: :coin:{card['PRICE']} " + f"_{card['UNIVERSE']}_ **Out Of Stock**")
            else:
                card_text_list.append(f"{card['NAME']}: :coin:{card['PRICE']} " + f"_{card['UNIVERSE']}_")

        title_resp = db.queryShopTitles()
        titles = []
        title_text_list = []
        for title in title_resp:
            if title['UNIVERSE'] in available_universes:
                if title['PRICE'] != 0 and title['PRICE'] < (vault['BALANCE'] + 500) and title['AVAILABLE']:
                    if title['TITLE'] not in vault['TITLES']:
                        titles.append({'TITLE': title['TITLE'], 'PRICE': title['PRICE'], 'UNIVERSE': title['UNIVERSE'], 'STOCK': title['STOCK']})

        random_titles = random.sample(titles, min(len(titles), 10))
        for title in random_titles:
            if title['STOCK'] == 0:
                title_text_list.append(f"{title['TITLE']}: :coin:{title['PRICE']} " + f"_{title['UNIVERSE']}_ **Out Of Stock**")
            else:
                title_text_list.append(f"{title['TITLE']}: :coin:{title['PRICE']} " + f"_{title['UNIVERSE']}_")
        
        
        arm_resp = db.queryShopArms()
        arms = []
        arm_text_list = []
        for arm in arm_resp:
            if arm['UNIVERSE'] in available_universes:
                if arm['PRICE'] != 0 and arm['PRICE'] < (vault['BALANCE'] + 500) and arm['AVAILABLE']:
                    if arm['ARM'] not in vault['ARMS']:
                        arms.append({'ARM': arm['ARM'], 'PRICE': arm['PRICE'], 'UNIVERSE': arm['UNIVERSE'], 'STOCK': arm['STOCK']})

        random_arms = random.sample(arms, min(len(arms), 10))
        for arm in random_arms:
            if arm['STOCK'] == 0:
                arm_text_list.append(f"{arm['ARM']}: :coin:{arm['PRICE']} " + f"_{arm['UNIVERSE']}_ **Out Of Stock**")
            else:
                arm_text_list.append(f"{arm['ARM']}: :coin:{arm['PRICE']} " + f"_{arm['UNIVERSE']}_")
        
        embedVar1 = discord.Embed(title=f":shopping_cart: Pop Up Shop", description=f"Current Balance :coin:{vault['BALANCE']}\n`.viewcard card name` - View Cards\n`.buycard card name` - Buy Card", colour=0x2ecc71, value='Page 1')
        embedVar1.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620236723/PCG%20LOGOS%20AND%20RESOURCES/Party_Chat_Shop.png")
        embedVar1.add_field(name=":shopping_bags: Cards", value="\n".join(card_text_list))
        embedVar1.set_footer(text="Stock updated every day")

        embedVar2 = discord.Embed(title=f":shopping_cart: Pop Up Shop", description=f"Current Balance :coin:{vault['BALANCE']}\n`.viewtitle title name` - View Title Stats\n`.buytitle title name` - Buy Title", colour=0x3498db, value='Page 2')
        embedVar2.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620236723/PCG%20LOGOS%20AND%20RESOURCES/Party_Chat_Shop.png")
        embedVar2.add_field(name=":shopping_bags: Titles", value="\n".join(title_text_list))
        embedVar2.set_footer(text="Stock updated every day")

        embedVar3 = discord.Embed(title=f":shopping_cart: Pop Up Shop", description=f"Current Balance :coin:{vault['BALANCE']}\n`.viewarm arm name` - View Arm Stats\n`.buyarm arm name` - Buy Arm", colour=0xf1c40f, value='Page 3')
        embedVar3.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620236723/PCG%20LOGOS%20AND%20RESOURCES/Party_Chat_Shop.png")
        embedVar3.add_field(name=":shopping_bags: Arm", value="\n".join(arm_text_list))
        embedVar3.set_footer(text="Stock updated every day")

        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
        paginator.add_reaction('⏮️', "first")
        paginator.add_reaction('⏪', "back")
        paginator.add_reaction('🔐', "lock")
        paginator.add_reaction('⏩', "next")
        paginator.add_reaction('⏭️', "last")
        embeds = [embedVar1,embedVar2,embedVar3]
        await paginator.run(embeds)

def setup(bot):
    bot.add_cog(Profile(bot))