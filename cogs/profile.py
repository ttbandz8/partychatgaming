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

            embedVar4 = discord.Embed(title="Pets", description="`.equippet name` - Select Your Pet\n`.viewpet Pet name` - View Pet Stats", colour=0x7289da)
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
   

        
            # embedVar = discord.Embed(title=f"{name}'s `Build Deck` Load Menu", description=f" What Preset would you like?")
            # embedVar.set_author(name="Press 0 to close Menu. Press 1, 2 or 3 to load a preset.")
            # embedVar.add_field(name=f"Preset 1:{preset1_title} {preset1_card}", value=f"Card: {preset1_card}\nTitle: {preset1_title}\nArm: {preset1_arm}\nPet: {preset1_pet}", inline=False)
            # embedVar.add_field(name=f"Preset 2:{preset2_title} {preset2_card}", value=f"Card: {preset2_card}\nTitle: {preset2_title}\nArm: {preset2_arm}\nPet: {preset2_pet}", inline=False)
            # embedVar.add_field(name=f"Preset 3:{preset3_title} {preset3_card}", value=f"Card: {preset3_card}\nTitle: {preset3_title}\nArm: {preset3_arm}\nPet: {preset3_pet}", inline=False)
            # embedVar.set_footer(text="Type Preset # to update current build!")
            # await ctx.send(embed=embedVar)

            embedVar2 = discord.Embed(title= f"BUILD :one:: {preset1_title} {preset1_card}", description=f"CARD: {preset1_card}\nTITLE: {preset1_title}\nARM: {preset1_arm}\nPET: {preset1_pet}", colour=0x7289da)
            embedVar2.set_thumbnail(url=avatar)
            embedVar2.set_footer(text="Press 0 to close Menu. Press 1 to LOAD this BUILD.")

            embedVar3 = discord.Embed(title= f"BUILD :two:: {preset2_title} {preset2_card}", description=f"CARD: {preset2_card}\nTITLE: {preset2_title}\nARM: {preset2_arm}\nPET: {preset2_pet}", colour=0x7289da)
            embedVar3.set_thumbnail(url=avatar)
            embedVar3.set_footer(text="Press 0 to close Menu.` Press 2 to LOAD this BUILD.")

            embedVar4 = discord.Embed(title= f"BUILD three:: {preset3_title} {preset3_card}", description=f"CARD: {preset3_card}\nTITLE: {preset3_title}\nARM: {preset3_arm}\nPET: {preset3_pet}", colour=0x7289da)
            embedVar4.set_thumbnail(url=avatar)
            embedVar4.set_footer(text="Press 0 to close Menu. Press 3 to LOAD this BUILD.")

            embedVar5 = discord.Embed(title= f"{name}'s Build `LOAD` Menu", description="This is the LOAD menu\nUse .savebuild to SAVE your current build to a preset slot!", colour=0x7289da)
            embedVar5.set_thumbnail(url=avatar)
            embedVar5.set_footer(text="Press 0 to close Menu. Press 1, 2 or 3 to LOAD a preset.")

            paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
            paginator.add_reaction('⏮️', "first")
            paginator.add_reaction('⏪', "back")
            paginator.add_reaction('🔐', "lock")
            paginator.add_reaction('⏩', "next")
            paginator.add_reaction('⏭️', "last")
            embeds = [embedVar2, embedVar3, embedVar4, embedVar5]
            await paginator.run(embeds)

            options =["0","1","2","3","4"]

            def check(msg):
                return msg.author == ctx.author and msg.content in options
            try:
                msg = await self.bot.wait_for("message",timeout=20.0, check=check)

                if msg.content == "0":
                    await ctx.send(f"{ctx.author.mention}, No change has been made")
                    return
                elif msg.content == "1":
                    response = db.updateUserNoFilter(query, {'$set': {'CARD': str(preset1_card), 'TITLE': str(preset1_title),'ARM': str(preset1_arm), 'PET': str(preset1_pet)}})
                    await ctx.send(response)
                elif msg.content == "2":
                    response = db.updateUserNoFilter(query, {'$set': {'CARD': str(preset2_card), 'TITLE': str(preset2_title),'ARM': str(preset2_arm), 'PET': str(preset2_pet)}})
                    await ctx.send(response)
                elif msg.content == "3":
                    response = db.updateUserNoFilter(query, {'$set': {'CARD': str(preset3_card), 'TITLE': str(preset3_title),'ARM': str(preset3_arm), 'PET': str(preset3_pet)}})
                    await ctx.send(response)
                else:
                    print("Bad selection")    
            except:
                await ctx.send(f"{ctx.author.mention}, No change has been made")
                return
        else:
            newVault = db.createVault({'OWNER': d['DISNAME']})


    @commands.command()
    async def savebuild(self, ctx):
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
   

        
            # embedVar = discord.Embed(title=f"{name}'s Build Deck Save Menu", description=f" Replace a `Preset` to `Save` your current `Build`!\n")
            # embedVar.set_author(name="Press 0 to close Menu. Press 1, 2 or 3 to overwrite preset.")
            # embedVar.add_field(name=f"Current Build:`{current_title} {current_card}`", value=f"Card: `{current_card}`\nTitle: `{current_title}`\nArm: `{current_arm}`\nPet: `{current_pet}`", inline=False)
            # embedVar.add_field(name=f"Preset 1:{preset1_title} {preset1_card}", value=f"Card: {preset1_card}\nTitle: {preset1_title}\nArm: {preset1_arm}\nPet: {preset1_pet}", inline=False)
            # embedVar.add_field(name=f"Preset 2:{preset2_title} {preset2_card}", value=f"Card: {preset2_card}\nTitle: {preset2_title}\nArm: {preset2_arm}\nPet: {preset2_pet}", inline=False)
            # embedVar.add_field(name=f"Preset 3:{preset3_title} {preset3_card}", value=f"Card: {preset3_card}\nTitle: {preset3_title}\nArm: {preset3_arm}\nPet: {preset3_pet}", inline=False)
            # embedVar.set_footer(text="Type Preset # to update current build!")
            # await ctx.send(embed=embedVar)

            embedVar2 = discord.Embed(title= f"BUILD :one:: {preset1_title} {preset1_card}", description=f"CARD: {preset1_card}\TITLE: {preset1_title}\ARM: {preset1_arm}\PET: {preset1_pet}", colour=0x7289da)
            embedVar2.set_thumbnail(url=avatar)
            embedVar2.set_footer(text="Press 0 to close Menu. Press 1 to OVERWRITE THIS PRESET.")

            embedVar3 = discord.Embed(title= f"BUILD :two:: {preset2_title} {preset2_card}", description=f"CARD: {preset2_card}\TITLE: {preset2_title}\ARM: {preset2_arm}\PET: {preset2_pet}", colour=0x7289da)
            embedVar3.set_thumbnail(url=avatar)
            embedVar3.set_footer(text="Press 0 to close Menu.` Press 2  to OVERWRITE THIS PRESET.")

            embedVar4 = discord.Embed(title= f"BUILD three:: {preset3_title} {preset3_card}", description=f"CARD: {preset3_card}\TITLE: {preset3_title}\ARM: {preset3_arm}\PET: {preset3_pet}", colour=0x7289da)
            embedVar4.set_thumbnail(url=avatar)
            embedVar4.set_footer(text="Press 0 to close Menu. Press 3 to OVERWRITE THIS PRESET.")

            embedVar5 = discord.Embed(title= f"{name}'s Build `SAVE` Menu", description="This is the SAVE menu\nUse .viewdeck to LOAD BUILDS !", colour=0x7289da)
            embedVar5.set_thumbnail(url=avatar)
            embedVar5.set_footer(text="Press 0 to close Menu. Press 1, 2 or 3 to SAVE a preset.")

            paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
            paginator.add_reaction('⏮️', "first")
            paginator.add_reaction('⏪', "back")
            paginator.add_reaction('🔐', "lock")
            paginator.add_reaction('⏩', "next")
            paginator.add_reaction('⏭️', "last")
            embeds = [embedVar2, embedVar3, embedVar4, embedVar5]
            await paginator.run(embeds)

            options =["0","1","2","3"]

            def check(msg):
                return msg.author == ctx.author and msg.content in options or msg.content == "0"
            try:
                msg = await self.bot.wait_for("message",timeout=20.0, check=check)

                if msg.content == "0":
                    await ctx.send(f"{ctx.author.mention}, No change has been made")
                    return
                elif msg.content == "1":
                    response = db.updateVaultNoFilter(vault_query, {'$set': {'DECK.0.CARD' :str(current_card), 'DECK.0.TITLE': str(current_title),'DECK.0.ARM': str(current_arm), 'DECK.0.PET': str(current_pet)}})
                    await ctx.send(response)
                elif msg.content == "2":
                    response = db.updateVaultNoFilter(vault_query, {'$set': {'DECK.1.CARD' :str(current_card), 'DECK.1.TITLE': str(current_title),'DECK.1.ARM': str(current_arm), 'DECK.1.PET': str(current_pet)}})
                    await ctx.send(response)
                elif msg.content == "3":
                    response = db.updateVaultNoFilter(vault_query, {'$set': {'DECK.2.CARD' :str(current_card), 'DECK.2.TITLE': str(current_title),'DECK.2.ARM': str(current_arm), 'DECK.2.PET': str(current_pet)}})
                    await ctx.send(response)
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