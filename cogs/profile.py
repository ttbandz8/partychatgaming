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
    async def flex(self, ctx):
        query = {'DISNAME': str(ctx.author)}
        d = db.queryUser(query)
        card = db.queryCard({'NAME':str(d['CARD'])})
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
            o_show = card['SHOW']
            o_collection = card['COLLECTION']
            resolved = False
            focused = False
            title = {'TITLE': 'CARD PREVIEW'}
            card_file = showcard(card, o_max_health, o_health, o_max_stamina, o_stamina, resolved, title, focused)

            passive_name = list(o_passive.keys())[0]
            passive_num = list(o_passive.values())[0]
            passive_type = list(o_passive.values())[1]

            embedVar = discord.Embed(title=f"{o_card}".format(self), description=f"{o_card} from {o_show} is currently my primary card.", colour=000000)
            # embedVar.set_image(url=card_file)
            embedVar.add_field(name="Health", value=f"{o_max_health}")
            embedVar.add_field(name="Stamina", value=f"{o_max_stamina}")
            embedVar.add_field(name="Attack", value=f"{o_attack}")
            embedVar.add_field(name="Defense", value=f"{o_defense}")
            embedVar.add_field(name="Speed", value=f"{o_speed}")
            embedVar.add_field(name="Unique Passive", value=f"`{passive_name}: Increases {passive_type} by {passive_num}`", inline=False)

            await ctx.send(embed=embedVar)

            await ctx.send(file=card_file)
        else:
            await ctx.send(m.USER_NOT_REGISTERED, delete_after=3)

    @commands.command()
    async def vault(self, ctx):
        query = {'DISNAME': str(ctx.author)}
        d = db.queryUser(query)

        vault = db.queryVault({'OWNER': d['DISNAME']})
        if vault:
            name = d['DISNAME'].split("#",1)[0]
            avatar = d['AVATAR']
            balance = vault['BALANCE']
            cards = vault['CARDS']
            titles = vault['TITLES']
            arms = vault['ARMS']

            cards_broken_up = np.array_split(cards, 6)
            titles_broken_up = np.array_split(titles, 6)
            arms_broken_up = np.array_split(arms, 6)

            if len(cards) < 25:
                embedVar = discord.Embed(title= f":triangular_flag_on_post: " + f"{name}".format(self) +"\n" + f" :coin:{'{:,}'.format(balance)}", description=":bank: Your Party Chat Gaming Vault™️", colour=000000)
                embedVar.set_thumbnail(url=avatar)
                # embedVar.add_field(name="Balance" + " :fireworks:", value=f":coin:{balance}")
                if bool(cards):
                    embedVar.add_field(name="Cards" + " :fireworks:", value="\n".join(cards))
                else:
                    embedVar.set_footer(text="No Cards available")
                
                if bool(titles):
                    embedVar.add_field(name="Titles" + " :fireworks:", value="\n".join(titles))

                if bool(arms):
                    embedVar.add_field(name="Arms" + " :fireworks:", value="\n".join(arms))
                await ctx.send(embed=embedVar)
            else:
                embed_list = []
                for i in range(0, len(titles_broken_up)):
                    globals()['embedVar%s' % i] = discord.Embed(title= f":triangular_flag_on_post: " + f"{name}".format(self) +"\n" + f" :coin:{'{:,}'.format(balance)}", description=":bank: Your Party Chat Gaming Vault™️", colour=000000)
                    globals()['embedVar%s' % i].set_thumbnail(url=avatar)
                    # embedVar.add_field(name="Balance" + " :fireworks:", value=f":coin:{balance}")
                    if bool(cards):
                        globals()['embedVar%s' % i].add_field(name="Cards" + " :fireworks:", value="\n".join(cards_broken_up[i]))
                    else:
                        globals()['embedVar%s' % i].set_footer(text="No Cards available")
                    
                    if bool(titles):
                        globals()['embedVar%s' % i].add_field(name="Titles" + " :fireworks:", value="\n".join(titles_broken_up[i]))

                    if bool(arms):
                        globals()['embedVar%s' % i].add_field(name="Arms" + " :fireworks:", value="\n".join(arms_broken_up[i]))
                    embed_list.append(globals()['embedVar%s' % i])

                paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
                paginator.add_reaction('⏮️', "first")
                paginator.add_reaction('⏪', "back")
                paginator.add_reaction('🔐', "lock")
                paginator.add_reaction('⏩', "next")
                paginator.add_reaction('⏭️', "last")
                embeds = embed_list
                await paginator.run(embeds)
        else:
            newVault = db.createVault({'OWNER': d['DISNAME']})

    @commands.command()
    async def shop(self, ctx):
        resp = db.queryShopCards()
        vault_query = {'OWNER' : str(ctx.author)}
        vault = db.altQueryVault(vault_query)
        cards = []
        unavailable_cards = []
        for card in resp:
            if card['PRICE'] != 0 and card['PRICE'] < (vault['BALANCE'] + 1000):
                if card['NAME'] not in vault['CARDS']:
                    cards.append({card['NAME']: card['PRICE']})

        title_resp = db.queryShopTitles()
        titles = []
        unavailable_titles = []
        for title in title_resp:
            if title['PRICE'] != 0 and title['PRICE'] < (vault['BALANCE'] + 1000):
                if title['TITLE'] not in vault['TITLES']:
                    titles.append({title['TITLE']: title['PRICE']})

        arm_resp = db.queryShopArms()
        arms = []
        unavailable_arms = []
        for arm in arm_resp:
            if arm['PRICE'] != 0 and arm['PRICE'] < (vault['BALANCE'] + 1000):
                if arm['ARM'] not in vault['ARMS']:
                    arms.append({arm['ARM']: arm['PRICE']})

        
        cards_to_str = dict(ChainMap(*cards))
        n = dict(sorted(cards_to_str.items(), key=lambda item: item[1]))
        cards_sorted_list = "\n".join(f'{k} : ' +  f" :coin:{'{:,}'.format(v)}"  for k,v in n.items())
        cards_list_array = cards_sorted_list.split("\n")
        
        # Upon adding more cards, be sure it increate the number below
        cards_broken_up = np.array_split(cards_list_array, 5)

        # Upon adding more cards, be sure it increate the number below
        titles_to_str = dict(ChainMap(*titles))
        n = dict(sorted(titles_to_str.items(), key=lambda item: item[1]))
        titles_sorted_list = "\n".join(f'{k} : ' +  f" :coin:{'{:,}'.format(v)}"  for k,v in n.items())
        titles_list_array = titles_sorted_list.split("\n")
        titles_broken_up = np.array_split(titles_list_array, 5)

        # Upon adding more cards, be sure it increate the number below
        arms_to_str = dict(ChainMap(*arms))
        n = dict(sorted(arms_to_str.items(), key=lambda item: item[1]))
        arms_sorted_list = "\n".join(f'{k} : ' +  f" :coin:{'{:,}'.format(v)}"  for k,v in n.items())
        arms_list_array = arms_sorted_list.split("\n")
        arms_broken_up = np.array_split(arms_list_array, 5)
        
        embed_list = []
        for i in range(0, len(titles_broken_up)):
            globals()['embedVar%s' % i] = discord.Embed(title=f":shopping_cart: Flex Shop", description="To preview cards, use the #vc card command. " + "\n" + "You will unlock more purchasable items as you save and earn more gold. ", colour=000000, value='Page 1')
            globals()['embedVar%s' % i].set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620236723/PCG%20LOGOS%20AND%20RESOURCES/Party_Chat_Shop.png")
            globals()['embedVar%s' % i].add_field(name=":shopping_bags: Available Cards", value="\n".join(cards_broken_up[i]))
            globals()['embedVar%s' % i].add_field(name=":shopping_bags: Available Titles", value="\n".join(titles_broken_up[i]))
            globals()['embedVar%s' % i].add_field(name=":shopping_bags: Available Arms", value="\n".join(arms_broken_up[i]))
            embed_list.append(globals()['embedVar%s' % i])

        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
        paginator.add_reaction('⏮️', "first")
        paginator.add_reaction('⏪', "back")
        paginator.add_reaction('🔐', "lock")
        paginator.add_reaction('⏩', "next")
        paginator.add_reaction('⏭️', "last")
        embeds = embed_list
        await paginator.run(embeds)


def setup(bot):
    bot.add_cog(Profile(bot))