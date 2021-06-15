from re import T
import discord
from discord.ext import commands
import bot as main
import db
import classes as data
import messages as m
import numpy as np
import help_commands as h
import unique_traits as ut
# Converters
from discord import User
from discord import Member
from PIL import Image, ImageFont, ImageDraw
import requests
from collections import ChainMap
import DiscordUtils
from .crownunlimited import showcard
import random
import textwrap

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

            embedVar = discord.Embed(title=f"{title_name} {o_card} & {active_pet['NAME']}:".format(self), description=textwrap.dedent(f"""\
            **Health:** {o_max_health}
            **Stamina:** {o_max_stamina}
            **Attack:** {o_attack}
            **Defense:** {o_defense}
            **Speed:** {o_speed}
            _Title:_ **{title_name}:** {title_passive_type} {title_passive_value}
            _Arm:_ **{arm_name}:** {arm_passive_type} {arm_passive_value}
            _Pet:_ **{active_pet['NAME']}:** {active_pet['TYPE']} {pet_ability_power}

            _**Moveset**_
            **{move1}:** {move1ap}
            **{move2}:** {move2ap}
            **{move3}:** {move3ap}
            **{move4}:** {move4enh} by {move4ap}
            
            _Unique Passive:_ **{passive_name}:** {passive_type} by {passive_num}

            {traitmessage}
            """)
            
            , colour=000000)
            embedVar.set_thumbnail(url=active_pet['PATH'])
            embedVar.set_image(url=o_card_path)
            embedVar.set_footer(text=f".enhance - Enhancement Menu")

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
            quests = vault['QUESTS']
            active_pet = {}
            pet_names = []

            quest_messages = []
            for quest in quests:
                completed = ""
                if quest['GOAL'] == quest['WINS']:
                    completed = "🟢"
                else:
                    completed = "🔴"

                quest_messages.append(textwrap.dedent(f"""\
                Defeat **{quest['OPPONENT']}** {quest['GOAL']} times in {quest['TYPE']} for :coin:{quest['REWARD']}! : {completed}
                **Current Progress:** {quest['WINS']}/{quest['GOAL']}
                
                """))

            for pet in pets:
                pet_names.append(pet['NAME'])
                if pet['NAME'] == pet_name:
                    active_pet = pet
       


            embedVar1 = discord.Embed(title= f"Cards", description=textwrap.dedent(f"""
            **Balance**: :coin:{'{:,}'.format(balance)}
            ***.equipcard card name:***  Equip Card
            ***.viewcard card name:*** View Cards Details
            
            {", ".join(cards)}
            """), colour=0x7289da)
            # embedVar1.set_thumbnail(url=avatar)

            embedVar2 = discord.Embed(title= f"Titles", description=textwrap.dedent(f"""
            **Balance**: :coin:{'{:,}'.format(balance)}
            ***.equiptitle title name:***  Equip Title
            ***.viewtitle title name:*** View Title Details
            
            {", ".join(titles)}
            """), colour=0x7289da)
            # embedVar2.set_thumbnail(url=avatar)

            embedVar3 = discord.Embed(title= f"Arms", description=textwrap.dedent(f"""
            **Balance**: :coin:{'{:,}'.format(balance)}
            ***.equiparm arm name:***  Equip Arm
            ***.viewarm arm name:*** View Arm Details
            
            {", ".join(arms)}
            """), colour=0x7289da)
            # embedVar3.set_thumbnail(url=avatar)
            
            embedVar4 = discord.Embed(title= f"Pets", description=textwrap.dedent(f"""
            **Balance**: :coin:{'{:,}'.format(balance)}
            ***.equippet pet name:***  Equip Pet
            ***.viewpet pet name:*** View Pet Details
            
            {", ".join(pet_names)}
            """), colour=0x7289da)
            if quests:
                embedVar5 = discord.Embed(title= f"Quest Board", description=textwrap.dedent(f"""
                **Balance**: :coin:{'{:,}'.format(balance)}
                \n{"".join(quest_messages)}
                """), colour=0x7289da)
                # embedVar4.set_thumbnail(url=avatar)
            else:
                embedVar5 = discord.Embed(title= f"Quest Board", description="Use .daily to receive Quests!", colour=0x7289da)
                # embedVar4.set_thumbnail(url=avatar)

            paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
            paginator.add_reaction('⏮️', "first")
            paginator.add_reaction('⏪', "back")
            paginator.add_reaction('🔐', "lock")
            paginator.add_reaction('⏩', "next")
            paginator.add_reaction('⏭️', "last")
            embeds = [embedVar1, embedVar2, embedVar3, embedVar4, embedVar5]
            await paginator.run(embeds)
        else:
            newVault = db.createVault({'OWNER': d['DISNAME']})

    @commands.command()
    async def viewdeck(self, ctx):
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
   

        
            embedVar = discord.Embed(title=f"{name}'s `Build Deck` Load Menu", description=f" What Preset would you like?")
            embedVar.set_author(name="Press 0 to close Menu. Press 1, 2 or 3 to load a preset.")
            embedVar.add_field(name=f"Preset 1:{preset1_title} {preset1_card} and {preset1_pet}", value=f"Card: {preset1_card}\nTitle: {preset1_title}\nArm: {preset1_arm}\nPet: {preset1_pet}", inline=False)
            embedVar.add_field(name=f"Preset 2:{preset2_title} {preset2_card} and {preset2_pet}", value=f"Card: {preset2_card}\nTitle: {preset2_title}\nArm: {preset2_arm}\nPet: {preset2_pet}", inline=False)
            embedVar.add_field(name=f"Preset 3:{preset3_title} {preset3_card} and {preset3_pet}", value=f"Card: {preset3_card}\nTitle: {preset3_title}\nArm: {preset3_arm}\nPet: {preset3_pet}", inline=False)
            embedVar.set_footer(text="Type Preset # to update current build!")
            await ctx.send(embed=embedVar)

            options =["0","1","2","3","4"]

            def check(msg):
                return msg.author == ctx.author and msg.content in options
            try:
                msg = await self.bot.wait_for("message",timeout=15, check=check)

                if msg.content == "0":
                    await ctx.send(f"{ctx.author.mention}, No change has been made")
                    return
                elif msg.content == "1":
                    response = db.updateUserNoFilter(query, {'$set': {'CARD': str(preset1_card), 'TITLE': str(preset1_title),'ARM': str(preset1_arm), 'PET': str(preset1_pet)}})
                    await ctx.send(response)
                    return
                elif msg.content == "2":
                    response = db.updateUserNoFilter(query, {'$set': {'CARD': str(preset2_card), 'TITLE': str(preset2_title),'ARM': str(preset2_arm), 'PET': str(preset2_pet)}})
                    await ctx.send(response)
                    return
                elif msg.content == "3":
                    response = db.updateUserNoFilter(query, {'$set': {'CARD': str(preset3_card), 'TITLE': str(preset3_title),'ARM': str(preset3_arm), 'PET': str(preset3_pet)}})
                    await ctx.send(response)
                    return
                else:
                    print("Bad selection")    
            except:
                await ctx.send(f"{ctx.author.mention}, No change has been made")
                return
        else:
            newVault = db.createVault({'OWNER': d['DISNAME']})

    @commands.command()
    async def savedeck(self, ctx):
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
   

        
            embedVar = discord.Embed(title=f"{name}'s Build Deck Save Menu", description=f" Replace a `Preset` to `Save` your current `Build`!\n")
            embedVar.set_author(name="Press 0 to close Menu. Press 1, 2 or 3 to overwrite preset.")
            embedVar.add_field(name=f"Current Build:`{current_title} {current_card}` and `{current_pet}`", value=f"Card: `{current_card}`\nTitle: `{current_title}`\nArm: `{current_arm}`\nPet: `{current_pet}`", inline=False)
            embedVar.add_field(name=f"Preset 1:{preset1_title} {preset1_card} and {preset1_pet}", value=f"Card: {preset1_card}\nTitle: {preset1_title}\nArm: {preset1_arm}\nPet: {preset1_pet}", inline=False)
            embedVar.add_field(name=f"Preset 2:{preset2_title} {preset2_card} and {preset2_pet}", value=f"Card: {preset2_card}\nTitle: {preset2_title}\nArm: {preset2_arm}\nPet: {preset2_pet}", inline=False)
            embedVar.add_field(name=f"Preset 3:{preset3_title} {preset3_card} and {preset3_pet}", value=f"Card: {preset3_card}\nTitle: {preset3_title}\nArm: {preset3_arm}\nPet: {preset3_pet}", inline=False)
            embedVar.set_footer(text="Type Preset # to update current build!")
            await ctx.send(embed=embedVar)

            options =["0","1","2","3"]

            def check(msg):
                return msg.author == ctx.author and msg.content in options or msg.content == "0"
            try:
                msg = await self.bot.wait_for("message",timeout=15, check=check)

                if msg.content == "0":
                    await ctx.send(f"{ctx.author.mention}, No change has been made")
                    return
                elif msg.content == "1":
                    response = db.updateVaultNoFilter(vault_query, {'$set': {'DECK.0.CARD' :str(current_card), 'DECK.0.TITLE': str(current_title),'DECK.0.ARM': str(current_arm), 'DECK.0.PET': str(current_pet)}})
                    await ctx.send(response)
                    return
                elif msg.content == "2":
                    response = db.updateVaultNoFilter(vault_query, {'$set': {'DECK.1.CARD' :str(current_card), 'DECK.1.TITLE': str(current_title),'DECK.1.ARM': str(current_arm), 'DECK.1.PET': str(current_pet)}})
                    await ctx.send(response)
                    return
                elif msg.content == "3":
                    response = db.updateVaultNoFilter(vault_query, {'$set': {'DECK.2.CARD' :str(current_card), 'DECK.2.TITLE': str(current_title),'DECK.2.ARM': str(current_arm), 'DECK.2.PET': str(current_pet)}})
                    await ctx.send(response)
                    return
                else:
                    print("Bad selection")    
            except:
                await ctx.send(f"{ctx.author.mention}, No change has been made")
                return
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
                if card['PRICE'] != 0 and card['PRICE'] < (vault['BALANCE'] + 500) and card['AVAILABLE'] and card['EXCLUSIVE'] != True:
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
            if title['UNIVERSE'] in available_universes or title['UNIVERSE'] == 'Unbound':
                if title['PRICE'] != 0 and title['PRICE'] < (vault['BALANCE'] + 500) and title['AVAILABLE'] and title['EXCLUSIVE'] != True:
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
            if arm['UNIVERSE'] in available_universes or arm['UNIVERSE'] == 'Unbound':
                if arm['PRICE'] != 0 and arm['PRICE'] < (vault['BALANCE'] + 500) and arm['AVAILABLE'] and arm['EXCLUSIVE'] != True:
                    if arm['ARM'] not in vault['ARMS']:
                        arms.append({'ARM': arm['ARM'], 'PRICE': arm['PRICE'], 'UNIVERSE': arm['UNIVERSE'], 'STOCK': arm['STOCK']})

        random_arms = random.sample(arms, min(len(arms), 10))
        for arm in random_arms:
            if arm['STOCK'] == 0:
                arm_text_list.append(f"{arm['ARM']}: :coin:{arm['PRICE']} " + f"_{arm['UNIVERSE']}_ **Out Of Stock**")
            else:
                arm_text_list.append(f"{arm['ARM']}: :coin:{arm['PRICE']} " + f"_{arm['UNIVERSE']}_")
        
        embedVar1 = discord.Embed(title=f":shopping_cart: Pop Up Shop", description=textwrap.dedent(f"""
        **Balance:** :coin:{vault['BALANCE']}
        **.viewcard card name:** View Cards
        **.buycard card name:** Buy Card
        """), colour=0x2ecc71, value='Page 1')
        # embedVar1.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620236723/PCG%20LOGOS%20AND%20RESOURCES/Party_Chat_Shop.png")
        embedVar1.add_field(name=":shopping_bags: Cards", value="\n".join(card_text_list))
        embedVar1.set_footer(text="Stock updated every day")

        embedVar2 = discord.Embed(title=f":shopping_cart: Pop Up Shop", description=textwrap.dedent(f"""
        **Balance:** :coin:{vault['BALANCE']}
        **.viewtitle title name:** View Title Stats
        **.buytitle title name:** Buy Title
        """), colour=0x3498db, value='Page 2')
        # embedVar2.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620236723/PCG%20LOGOS%20AND%20RESOURCES/Party_Chat_Shop.png")
        embedVar2.add_field(name=":shopping_bags: Titles", value="\n".join(title_text_list))
        embedVar2.set_footer(text="Stock updated every day")

        embedVar3 = discord.Embed(title=f":shopping_cart: Pop Up Shop", description=textwrap.dedent(f"""
        **Balance:** :coin:{vault['BALANCE']}
        **.viewarm arm name:** View Arm Stats
        **.buyarm arm name** Buy Arm
        """), colour=0xf1c40f, value='Page 3')
        # embedVar3.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620236723/PCG%20LOGOS%20AND%20RESOURCES/Party_Chat_Shop.png")
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