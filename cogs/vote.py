from itertools import filterfalse
import discord
from discord.ext import commands
import bot as main
import db
import classes as data
import messages as m
import numpy as np
import help_commands as h
import textwrap
import DiscordUtils
import destiny as d
# Converters
from discord import User
from discord import Member
from PIL import Image, ImageFont, ImageDraw
import requests
from discord_slash import cog_ext, SlashContext
from discord_slash.utils import manage_components
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_commands import create_option, create_choice
from dinteractions_Paginator import Paginator
# import topgg

from discord.ext import commands

import dbl


class TopGG(commands.Cog):
    """
    This example uses dblpy's webhook system.
    In order to run the webhook, at least webhook_port must be specified (number between 1024 and 49151).
    """

    def __init__(self, bot):
        self.bot = bot
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijk1NTcwNDkwMzE5ODcxMTgwOCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjQ5MDAyNDYzfQ.OGIjvyo2mlOrfZTTLoyIODNKzvk_7o-0tP5zwA31JsE'  # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token, webhook_path='/dblwebhook', webhook_auth='P@ssw11rd', webhook_port=5000)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Voting Cog is ready!')

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        """An event that is called whenever someone votes for the bot on top.gg."""
        print("Received an upvote:", "\n", data, sep="")

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        """An event that is called whenever someone tests the webhook system for your bot on top.gg."""
        print("Received a test upvote:", "\n", data, sep="")


def setup(bot):
    bot.add_cog(TopGG(bot))