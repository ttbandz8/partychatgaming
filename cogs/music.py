import discord
import asyncio
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
import youtube_dl
import in_game_music as igm

song_queue = []
ingamemusic = []

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
YDL_OPTIONS = {'format': 'bestaudio/best',
        'noplaylist' : True,
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],}

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Music Cog is ready!')

    async def cog_check(self, ctx):
        if ctx.author.guild_permissions.administrator == True:
             return True
        else:
            return False
        # return await main.validate_user(ctx)

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You Need To Join A Voice Channel")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)
    
    @commands.command()
    async def kick(self, ctx):
        print(ctx.channel)
        await ctx.voice_client.disconnect()
    
    @commands.command()
    async def igm(self, ctx):
        guild = ctx.guild
        if guild:
            overwrites = {
                        guild.default_role: discord.PermissionOverwrite(speak=False),
                        guild.me: discord.PermissionOverwrite(speak=False),
                    ctx.author: discord.PermissionOverwrite(speak=False),
                    }
            voice_channel = await guild.create_voice_channel("In Game Music", overwrites=overwrites)
        await voice_channel.connect()

        ingamemusic = igm.in_game_music_queue

        vc = ctx.voice_client
        playing = vc.is_playing()
        if not playing:
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(ingamemusic[0], download=False)
                url2 = info['formats'][0]['url']
                source = await discord.FFmpegOpusAudio.from_probe(url2, executable="ffmpeg/bin/ffmpeg.exe", **FFMPEG_OPTIONS)
                vc.play(source, after=lambda e: play_next_igm(ctx))
        else:
            print(song_queue)


        

    @commands.command()
    async def play(self,ctx, url):
        if ctx.author.voice is None:
            await ctx.send("You Need To Join A Voice Channel")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

        song_queue.append(url)
        # ctx.voice_client.stop()
        vc = ctx.voice_client
        playing = vc.is_playing()
        if not playing:
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                url2 = info['formats'][0]['url']
                source = await discord.FFmpegOpusAudio.from_probe(url2, executable="ffmpeg/bin/ffmpeg.exe", **FFMPEG_OPTIONS)
                vc.play(source, after=lambda e: play_next(ctx))
        else:
            print(song_queue)


    @commands.command()
    async def next(self, ctx):
        voice = ctx.voice_client
        print("NEXT")
        if len(song_queue) > 1:
            await play_next(voice)
        else:
            await ctx.send("No songs in queue!")

    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send("Paused")

    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send("Resume")

#Plays the next song in the queue
async def play_next_igm(vc):
    voice = vc
    if len(ingamemusic) > 1:
        voice.stop()
        del ingamemusic[0]
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(ingamemusic[0], download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, executable="ffmpeg/bin/ffmpeg.exe", **FFMPEG_OPTIONS)
            voice.play(source, after=lambda e: play_next(voice))
        voice.is_playing()

#Plays the next song in the queue
async def play_next(vc):
    voice = vc
    if len(song_queue) > 1:
        voice.stop()
        del song_queue[0]
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(song_queue[0], download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, executable="ffmpeg/bin/ffmpeg.exe", **FFMPEG_OPTIONS)
            voice.play(source, after=lambda e: play_next(voice))
        voice.is_playing()

def setup(bot):
    bot.add_cog(Music(bot))