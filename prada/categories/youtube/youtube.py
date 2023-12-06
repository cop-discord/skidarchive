import os
import re
import ast
import io
import json
import random
import urllib
import discord
import inspect
import base64
import asyncio
import aiohttp
import datetime
import requests
import giphy_client
import aiosqlite
import button_paginator as pg
import timeago

from io import BytesIO
from discord import ui
from pyfiglet import Figlet
from asyncio import sleep
from urllib.request import urlopen
from discord.ext import commands
from discord.ext import tasks
from discord.ui import Button, View
from pytube import YouTube
from pytube.extract import video_info_url
from giphy_client.rest import ApiException

class youtube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        first_word = message.content.split(' ')
        if first_word[0].lower() == f"cut":
            if "youtube.com" in first_word[1]:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'}
                async with aiohttp.ClientSession() as session:
                    async with session.get(first_word[1], headers=headers) as resp:
                        x = str(resp.url)
                try:
                    async with message.channel.typing():
                        yt = YouTube(x)
                        download_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cut_videos")
                        os.makedirs(download_path, exist_ok=True)
                        yt.streams.get_highest_resolution().download(download_path, filename="cut.mp4")
                        embed = discord.Embed(color=discord.Color.random(), description=f"**[{yt.title}]({yt.channel_url})**")
                        embed.set_author(name=f"@{yt.author}", icon_url=yt.thumbnail_url)
                        embed.set_footer(
                            text=f"{int(yt.views):,} 👀| {message.author.name}#{message.author.discriminator}",
                            icon_url="https://cdn.discordapp.com/emojis/1001641960324468788.png")
                        await message.channel.send(file=discord.File(os.path.join(download_path, "cut.mp4")), embed=embed)
                except Exception as e:
                    await message.channel.send(f"Something went wrong - {e}")