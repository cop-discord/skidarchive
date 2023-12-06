import time
import psutil
import discord
import datetime
import pytz
from datetime import timedelta, datetime
from typing import Optional
from discord import Message, Member, User, Embed
from discord.ext.commands import Cog, command, Context
from time import perf_counter
from discord import Guild, Invite
from jishaku.math import mean_stddev

from core import Slut

class Information(Cog):
    def __init__(self, bot: Slut) -> None:
        self.bot: Slut = bot
        self._uptime = time.time()
        self.support = "https://discord.gg/your"
        self.invite = "https://discord.com/api/oauth2/authorize?client_id=605506274896904192&permissions=8&scope=applications.commands%20bot"

    @command(name="rtt")
    async def rtt(self: "Information", ctx: Context) -> Optional[Message]:
        """
        View the round-trip latency to the Discord API.
        """

        message: Optional[Message] = None
        embed = Embed(color=0x2B2D31, title="Round-Trip Latency")

        api_readings: List[float] = []
        websocket_readings: List[float] = []

        for _ in range(5):
            if api_readings:
                embed.description = (
                    ">>> "
                    + "\n".join(
                        f"Trip {index + 1}: {reading * 1000:.2f}ms"
                        for index, reading in enumerate(api_readings)
                    )
                )

            text = ""

            if api_readings:
                average, stddev = mean_stddev(api_readings)

                text += f"Average: `{average * 1000:.2f}ms` `\N{PLUS-MINUS SIGN}` `{stddev * 1000:.2f}ms`"

            if websocket_readings:
                average = sum(websocket_readings) / len(websocket_readings)

                text += f"\nWebsocket Latency: `{average * 1000:.2f}ms`"
            else:
                text += f"\nWebsocket latency: `{self.bot.latency * 1000:.2f}ms`"

            if message:
                embed = message.embeds[0]
                embed.clear_fields()
                embed.add_field(
                    name="​",
                    value=text,
                )

                before = perf_counter()
                await message.edit(embed=embed)
                after = perf_counter()

                api_readings.append(after - before)
            else:
                embed.add_field(
                    name="​",
                    value=text,
                )

                before = perf_counter()
                message = await ctx.send(embed=embed)
                after = perf_counter()

                api_readings.append(after - before)

            if self.bot.latency > 0.0:
                websocket_readings.append(self.bot.latency)

        if message:
            return message

    @command(name="uptime")
    async def uptime(
        self: "Information",
        ctx: Context,
    ) -> Optional[Message]:
 
        """
        Checks the bot's uptime.
        """

        return await ctx.reply(f'`{timedelta(seconds=int(round(time.time() - self._uptime)))}`', mention_author=False)

    @command(name="ping")
    async def ping(self, ctx: Context) ->  Optional[Message]:
 
        """
        Checks the bot's ping.
        """
        start_time = time.time()
        message = await ctx.send("Pinging...")
        end_time = time.time()
        latency = (end_time - start_time) * 1000  # Convert to milliseconds
        latency_edit = latency / 1000  # Convert to seconds for edit message
        edit_time = latency / 1000  # Convert to seconds for edit message

        await message.edit(content=f"It took `{self.bot.latency * 1000:.2f}ms` to ping **`@la#0001` & `@7334.` on discord** (edit: `{edit_time:.15f}ms`)")

    @command(name="shards")
    async def shards(self, ctx: Context) -> Optional[Message]:
        """
        Checks the bot's shards.
        """
        shard_count = self.bot.shard_count
        shard_id = ctx.guild.shard_id if ctx.guild else 0  # Get the shard ID of the current guild
        
        embed = discord.Embed(
            description=f'```asciidoc\n'
                        f'Total Shards   :: {shard_count}\n'
                        f'Server Shard   :: {shard_id}\n'
                        f'```',
            color=0x2B2D31
        )

        return await ctx.send(embed=embed)

    @command(name="botinfo", aliases=['about', 'saint', 'bi', 'stats'])
    async def botinfo(
        self: "Information",
        ctx: Context,
    ) -> Optional[Message]:
 
        """
        Checks the bot's info.
        """

        # Get bot statistics
        total_members = sum(guild.member_count for guild in self.bot.guilds)
        unique_members = len(set(self.bot.get_all_members()))
        online_members = sum(1 for member in self.bot.get_all_members() if member.status != discord.Status.offline)

        total_channels = sum(1 for _ in self.bot.get_all_channels())
        text_channels = sum(1 for channel in self.bot.get_all_channels() if isinstance(channel, discord.TextChannel))
        voice_channels = sum(1 for channel in self.bot.get_all_channels() if isinstance(channel, discord.VoiceChannel))

        # Get memory usage
        process = psutil.Process()
        memory_usage = process.memory_info().rss / (1024 ** 2)  # in MB
        total_commands = len(self.bot.commands)


        embed = discord.Embed(title=f'*kayo*', description=f"Bot statistics, developed by **tbh#0001**, & **7334.**\n**Memory:** {memory_usage:.2f}MB **Commands:** {total_commands}", color=0x2f3136)
        embed.set_thumbnail(url=self.bot.user.avatar.url) 
        embed.set_author(name="", url=self.bot.user.avatar.url)
        embed.add_field(name="Members", value=f"{total_members} total\n{unique_members} unique\n{online_members} unique online", inline=True)
        embed.add_field(name="Channels", value=f"{total_channels} total\n{text_channels} text\n{voice_channels} voice", inline=True)
        embed.add_field(name="Guilds", value=f"{len(self.bot.guilds)} (public)\n 1 (private)", inline=True)
        eastern = pytz.timezone('America/New_York')
        eastern_now = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(eastern)
        embed.timestamp=eastern_now 

        await ctx.send(embed=embed)


    @command(name="invite", aliases=['inv'])
    async def invite(
        self: "Information",
        ctx: Context
    ) -> Optional[Message]:
        """
        Invite the bot.
        """
        view = discord.ui.View()
        inv = discord.ui.Button(
        label="Invite",
        url=f"{self.invite}"
       )
        sup = discord.ui.Button(
        label="Support",
        url=f"{self.support}"
       )
       
        view.add_item(inv)
        view.add_item(sup)
        await ctx.reply(view=view, mention_author=False)

    @command()
    async def support(
        self: "Information",
        ctx: Context
    ) -> Optional[Message]:
 
        """
        Join the support server.
        """
        view = discord.ui.View()
        sup = discord.ui.Button(
        label="Support",
        url=f"{self.support}"
       )
       
        view.add_item(sup)
        await ctx.reply(view=view, mention_author=False)