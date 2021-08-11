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
from collections import Counter
from discord_slash import cog_ext, SlashContext

emojis = ['👍', '👎']

class Matches(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Matches Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @cog_ext.cog_slash(description="Analysis on Card", guild_ids=main.guild_ids)
    async def analysis(self, ctx, card: str):
        name = card
        match_query = {"CARD": card}
        response = db.queryManyMatches(match_query)
        if response:
            card = db.queryCard({"NAME": name})
            path = card['PATH']
            title_tales_matches = []
            title_dungeon_matches = []
            title_boss_matches = []
            title_pvp_matches = []
            universe_tales_matches = []
            universe_dungeon_matches = []
            arm_tales_matches = []
            arm_dungeon_matches = []
            arm_boss_matches = []
            arm_pvp_matches = []
            most_played = []

            for matches in response:
                most_played.append(matches['PLAYER'])
                if matches['UNIVERSE_TYPE'] == "Tales":
                    title_tales_matches.append(matches['TITLE'])
                    arm_tales_matches.append(matches['ARM'])
                    universe_tales_matches.append(matches['UNIVERSE'])
                if matches['UNIVERSE_TYPE'] == "Dungeon":
                    title_dungeon_matches.append(matches['TITLE'])
                    arm_dungeon_matches.append(matches['ARM'])
                    universe_dungeon_matches.append(matches['UNIVERSE'])
                if matches['UNIVERSE_TYPE'] == "Boss":
                    title_boss_matches.append(matches['TITLE'])
                    arm_boss_matches.append(matches['ARM'])
                if matches['UNIVERSE_TYPE'] == "PVP":
                    title_pvp_matches.append(matches['TITLE'])
                    arm_pvp_matches.append(matches['ARM'])
            
            card_main = most_frequent(most_played)

            if title_tales_matches and arm_tales_matches:
                tale_title = most_frequent(title_tales_matches)
                tale_arm = most_frequent(arm_tales_matches)
                tale_universe = most_frequent(universe_tales_matches)
                tale_message = textwrap.dedent(f"""\
                _Most Used Title:_ **{tale_title}**
                _Most Used Arm:_ **{tale_arm}**
                _Most Played Universe:_ **{tale_universe}**
                """)
            else:
                tale_message = textwrap.dedent(f"""\
                _Not enough data for analysis_
                """)

            if title_dungeon_matches and arm_dungeon_matches:
                dungeon_title = most_frequent(title_dungeon_matches)
                dungeon_arm = most_frequent(arm_dungeon_matches)
                dungeon_universe = most_frequent(universe_dungeon_matches)
                dungeon_message = textwrap.dedent(f"""\
                _Most Used Title:_ **{dungeon_title}**
                _Most Used Arm:_ **{dungeon_arm}**
                _Most Played Universe:_ **{dungeon_universe}**
                """)
            else:
                dungeon_message = textwrap.dedent(f"""\
                _Not enough data for analysis_
                """)

            if title_boss_matches and arm_boss_matches:
                boss_title = most_frequent(title_boss_matches)
                boss_arm = most_frequent(arm_boss_matches)
                boss_message = textwrap.dedent(f"""\
                _Most Used Title:_ **{boss_title}**
                _Most Used Arm:_ **{boss_arm}**
                """)
            else:
                boss_message = textwrap.dedent(f"""\
                _Not enough data for analysis_
                """)

            if title_pvp_matches and arm_pvp_matches:
                pvp_title = most_frequent(title_pvp_matches)
                pvp_arm = most_frequent(arm_pvp_matches)
                pvp_message = textwrap.dedent(f"""\
                _Most Used Title:_ **{pvp_title}**
                _Most Used Arm:_ **{pvp_arm}**
                """)
            else:
                pvp_message = textwrap.dedent(f"""\
                _Not enough data for analysis_
                """)
            
            embedVar = discord.Embed(title=f":crown: {name} | _Crown Analysis_".format(self), description=textwrap.dedent(f"""\
**Card Master**
{card_main}

**Tales Stats:**
{tale_message}

**Dungeon Stats:**
{dungeon_message}

**Boss Stats:**
{boss_message}

**Pvp Stats:**
{pvp_message}
            """), colour=000000)
            embedVar.set_image(url=path)
            # embedVar.set_footer(text=f".enhance - Enhancement Menu")
            await ctx.send(embed=embedVar)

            
            
        else:
            await ctx.send("Not enough data for analysis")
            return

def most_frequent(List):
    occurence_count = Counter(List)
    return occurence_count.most_common(1)[0][0]

def setup(bot):
    bot.add_cog(Matches(bot))