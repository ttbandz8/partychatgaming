import discord
from discord.ext import commands
import DiscordUtils
import bot as main
import db
import classes as data
import messages as m
import numpy as np
import help_commands as h

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Create an event within a Cog
    # Because you're in a Cog, self must be the first parameter in all events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Games Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @commands.command()
    async def newgame(self, ctx, *args):
        if ctx.author.guild_permissions.administrator == True:
            game_name = " ".join([*args])
            # games = [x for x in db.query_all_games()][0]
            
            response = db.addGame(data.newGame({'GAME': game_name}))
            await ctx.send(response, delete_after=5)
        else:
            await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=5)


    @commands.command()
    async def addgamealiases(self, ctx, *args):
        if ctx.author.guild_permissions.administrator == True:
            admin = db.queryUser({'DISNAME': str(ctx.author)})
            if not args:
                await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=5)
            else:
                # game = admin['GAMES'][0]
                test_game = "Call Of Duty Mobile"

                aliases = []

                for title in args:
                    aliases.append(title)

                query = {'GAME': test_game}
                new_value = {'$set': {'ALIASES': aliases}}

                response = db.updateGame(query, new_value)
                await ctx.send(m.UPDATE_COMPLETE, delete_after=5)

    @commands.command()
    async def addgamealias(self, ctx, *args):
        if ctx.author.guild_permissions.administrator == True:
            alias = " ".join([*args])
            admin = db.queryUser({'DISNAME': str(ctx.author)})
            if not args:
                await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=5)
            else:
                # game = admin['GAMES'][0]
                test_game = "Call Of Duty Mobile"

                query = {'GAME': test_game}
                new_value = {'$addToSet': {'ALIASES': alias}}

                response = db.updateGame(query, new_value)
                await ctx.send(m.UPDATE_COMPLETE, delete_after=5)

    @commands.command()
    async def addgametypes(self, ctx, *args):
        if ctx.author.guild_permissions.administrator == True:
            admin = db.queryUser({'DISNAME': str(ctx.author)})
            if not args:
                await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=5)
            else:
                # game = admin['GAMES'][0]
                test_game = "Call Of Duty Mobile"

                types = []

                for gametype in args:
                    types.append(gametype)

                query = {'GAME': test_game}
                new_value = {'$set': {'TYPE': types}}

                response = db.updateGame(query, new_value)
                await ctx.send(m.UPDATE_COMPLETE, delete_after=5)

    @commands.command()
    async def addgameimage(self, ctx, args):
        if ctx.author.guild_permissions.administrator == True:
            admin = db.queryUser({'DISNAME': str(ctx.author)})
            if not args:
                await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=5)
            else:

                test_game = "Call Of Duty Mobile"

                query = {'GAME': test_game}
                new_value = {'$set': {'IMAGE_URL': args}}

                response = db.updateGame(query, new_value)
                await ctx.send(m.UPDATE_COMPLETE, delete_after=5)


    @commands.command()
    async def deletegame(self, ctx, *args):
        if ctx.author.guild_permissions.administrator == True:
            game_name = " ".join([*args])
            admin = db.queryUser({'DISNAME': str(ctx.author)})
            if not args:
                await ctx.send(m.RESPONSE_NOT_DETECTED, delete_after=5)
            else:
                query = {'GAME': game_name}
                response = db.deleteGame(query)
                await ctx.send(m.DELETE_COMPLETE, delete_after=5)

    @commands.command()
    # @commands.check(validate_user)
    async def lkg(self, ctx):
        data = db.query_all_games()

        if data:

            game_list = []
            for game in data:
                game_list.append(game)

            game_title_list = []

            for title in game_list:
                game_title_list.append(title['GAME'])

            embedVar = discord.Embed(title=f"Games Lookup", description=":bank: Party Chat Gaming Database", colour=000000)
            embedVar.add_field(name="Games", value="\n".join(game_title_list))
            embedVar.set_footer(text="More games will be added soon. ")

            await ctx.send(embed=embedVar, delete_after=20)
        else:
            await ctx.send(m.NO_GAMES_AVAILABLE, delete_after=5)


def setup(bot):
    bot.add_cog(Games(bot))