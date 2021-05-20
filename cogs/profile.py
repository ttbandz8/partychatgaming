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

        if d:
            card = db.queryCard({'NAME': d['CARD']})
            name = d['DISNAME'].split("#",1)[0]
            games = d['GAMES']
            ign = d['IGN']
            team = d['TEAM']
            title = d['TITLE']
            avatar = d['AVATAR']
            matches = d['MATCHES']
            tournament_wins = d['TOURNAMENT_WINS']


            matches_to_string = dict(ChainMap(*matches))
            ign_to_string = dict(ChainMap(*ign))

            game_text = '\n'.join(str(x) for x in games)
            titles_text = ' '.join(str(x) for x in title)
            matches_text = "\n".join(f'{k}: {"/".join([str(int) for int in v])}' for k,v in matches_to_string.items())

            
            img = Image.open(requests.get(card['PATH'], stream=True).raw)

            draw = ImageDraw.Draw(img)
            header = ImageFont.truetype("KomikaTitle-Paint.ttf", 60)
            tournament_wins_font = ImageFont.truetype("RobotoCondensed-Bold.ttf", 35)
            p = ImageFont.truetype("Roboto-Bold.ttf", 25)

            # profile_pic = Image.open(requests.get(d['AVATAR'], stream=True).raw)
            # profile_pic_resized = profile_pic.resize((120, 120), resample=0)
            # img.paste(profile_pic_resized, (1045, 30))
            draw.text((95,45), name, (255, 255, 255), font=header, align="left")
            draw.text((5,65), str(tournament_wins), (255, 255, 255), font=tournament_wins_font, align="center")
            draw.text((60, 320), game_text, (255, 255, 255), font=p, align="left")
            draw.text((368, 320), team, (255, 255, 255), font=p, align="center")
            draw.text((635, 320), titles_text, (255, 255, 255), font=p, align="center")
            draw.text((1040, 320), matches_text, (255, 255, 255), font=p, align="center")

            img.save("text.png")

            await ctx.send(file=discord.File("text.png"))

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

            cards_broken_up = np.array_split(cards, 6)
            titles_broken_up = np.array_split(titles, 6)

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
        
        embed_list = []
        for i in range(0, len(titles_broken_up)):
            globals()['embedVar%s' % i] = discord.Embed(title=f":shopping_cart: Flex Shop", description="To preview cards, use the #vc card command. " + "\n" + "You will unlock more purchasable items as you save and earn more gold. ", colour=000000, value='Page 1')
            globals()['embedVar%s' % i].set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620236723/PCG%20LOGOS%20AND%20RESOURCES/Party_Chat_Shop.png")
            globals()['embedVar%s' % i].add_field(name=":shopping_bags: Available Cards", value="\n".join(cards_broken_up[i]))
            globals()['embedVar%s' % i].add_field(name=":shopping_bags: Available Titles", value="\n".join(titles_broken_up[i]))
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