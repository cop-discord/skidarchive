import discord, os, asyncpg, typing, time, random, string, io, datetime, multiprocessing
from humanfriendly import format_timespan
from discord import Embed, Message
from discord.ext import commands, tasks
from discord.ext.commands import MinimalHelpCommand
from tools.utils import StartUp, create_db, Paginator
from io import BytesIO
from discord.ui import Button, View
from cogs.voicemaster import vmbuttons
from discord.gateway import DiscordWebSocket
from cogs.ticket import CreateTicket, DeleteTicket
import json
from cogs.music import Music
from tools.ext import Client, HTTP
from typing import Optional, List
from handlers.pfps import PFPS
import asyncio
import inspect

temp = "http://zplqmkhc-rotate:ci3sbpslnawy@p.webshare.io:80/"


def generate_key():
    return "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(6)
    )


async def checkthekey(key: str):
    check = await bot.db.fetchrow("SELECT * FROM cmderror WHERE code = $1", key)
    if check:
        newkey = await generate_key(key)
        return await checkthekey(newkey)
    return key


DiscordWebSocket.identify = StartUp.identify

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "True"
os.environ["JISHAKU_RETAIN"] = "True"


async def getprefix(bot, message):
    if not message.guild:
        return ";"
    check = await bot.db.fetchrow(
        "SELECT * FROM selfprefix WHERE user_id = $1", message.author.id
    )
    if check:
        selfprefix = check["prefix"]
    res = await bot.db.fetchrow(
        "SELECT * FROM prefixes WHERE guild_id = $1", message.guild.id
    )
    if res:
        guildprefix = res["prefix"]
    else:
        guildprefix = ";"
    if not check and res:
        selfprefix = res["prefix"]
    elif not check and not res:
        selfprefix = ";"
    return guildprefix, selfprefix


intents = discord.Intents.all()


class Context(commands.Context):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def find_role(self, name: str):
        for role in self.guild.roles:
            if role.name == "@everyone":
                continue
            if name.lower() in role.name.lower():
                return role
        return None

    async def send_success(self, message: str) -> discord.Message:
        return await self.reply(
            embed=discord.Embed(
                color=self.bot.color, description=f"> {self.author.mention}: {message}"
            )
        )

    async def send_nonefound(self, message: str) -> discord.Message:
        return await self.reply(
            embed=discord.Embed(
                color=self.bot.color,
                description=f"> 🔎 {self.author.mention}: {message}",
            )
        )

    async def help(self, message: str) -> discord.Message:
        return await self.reply(
            embed=discord.Embed(color=self.bot.color, description=f"> {message}")
        )

    async def send_error(self, message: str) -> discord.Message:
        return await self.reply(
            embed=discord.Embed(
                color=self.bot.color, description=f"> {self.author.mention}: {message}"
            )
        )

    async def error(self, message: str) -> discord.Message:
        return await self.reply(
            embed=discord.Embed(
                color=self.bot.color, description=f"> {self.author.mention}: {message}"
            )
        )

    async def send_warning(self, message: str) -> discord.Message:
        return await self.reply(
            embed=discord.Embed(
                color=self.bot.color, description=f"> {self.author.mention}: {message}"
            )
        )

    async def warn(self, message: str) -> discord.Message:
        return await self.reply(
            embed=discord.Embed(
                color=self.bot.color, description=f"> {self.author.mention}: {message}"
            )
        )

    async def send_neutral(self, message: str) -> discord.Message:
        return await self.send(
            embed=discord.Embed(
                color=self.bot.color, description=f"{self.author.mention}: {message}"
            )
        )

    async def paginator(self, embeds: List[discord.Embed]):
        if len(embeds) == 1:
            return await self.send(embed=embeds[0])
        view = Paginator(self, embeds)
        view.message = await self.reply(embed=embeds[0], view=view)

    async def cmdhelp(self):
        command = self.command
        commandname = (
            f"{str(command.parent)} {command.name}"
            if str(command.parent) != "None"
            else command.name
        )
        if command.cog_name == "owner":
            return
        if command.cog_name == "auth":
            return
        embed = discord.Embed(
            color=bot.color, title=commandname, description=f"`{command.description}`"
        )
        embed.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
        embed.add_field(
            name="usage",
            value=f"```{commandname} {command.usage if command.usage else ''}```",
            inline=False,
        )
        embed.set_footer(
            text=f"Aliases: {', '.join(map(str, command.aliases)) or 'none'} • Category: {command.help}"
        )
        await self.reply(embed=embed)

    async def create_pages(self):
        embeds = []
        p = 0
        for command in self.command.commands:
            commandname = (
                f"{str(command.parent)} {command.name}"
                if str(command.parent) != "None"
                else command.name
            )
            p += 1
            embeds.append(
                discord.Embed(
                    color=bot.color,
                    title=f"{commandname}",
                    description=f"`{command.description}`",
                )
                .set_author(name=bot.user.name, icon_url=bot.user.display_avatar.url)
                .add_field(
                    name="usage",
                    value=f"```{commandname} {command.usage if command.usage else ''}```",
                    inline=False,
                )
                .set_footer(
                    text=f"page: {p}/{len(self.command.commands)} • Aliases: {', '.join(a for a in command.aliases) if len(command.aliases) > 0 else 'none'} ・ Category: {command.help}"
                )
            )

        async def send_command_help(self, command: commands.Command):
            commandname = (
                f"{str(command.parent)} {command.name}"
                if str(command.parent) != "None"
                else command.name
            )
            if command.cog_name == "owner":
                return
            if command.cog_name == "auth":
                return
            embed = discord.Embed(
                color=bot.color, title=commandname, description=command.description
            )
            embed.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
            embed.add_field(
                name="usage",
                value=f"```{commandname} {command.usage if command.usage else ''}```",
                inline=False,
            )
            embed.set_footer(
                text=f"aliases: {', '.join(map(str, command.aliases)) or 'none'} • module: {command.help}"
            )
            channel = self.get_destination()
            await channel.send(embed=embed)

        async def send_group_help(self, group: commands.Group):
            ctx = self.context
            embeds = []
            p = 0
            for command in group.commands:
                commandname = (
                    f"{str(command.parent)} {command.name}"
                    if str(command.parent) != "None"
                    else command.name
                )
                p += 1
                embeds.append(
                    discord.Embed(
                        color=bot.color,
                        title=f"{commandname}",
                        description=command.description,
                    )
                    .set_author(
                        name=bot.user.name, icon_url=bot.user.display_avatar.url
                    )
                    .add_field(
                        name="usage",
                        value=f"```{commandname} {command.usage if command.usage else ''}```",
                        inline=False,
                    )
                    .set_footer(
                        text=f"page: {p}/{len(group.commands)} • aliases: {', '.join(a for a in command.aliases) if len(command.aliases) > 0 else 'none'} • module: {command.help}"
                    )
                )

            return await ctx.paginator(embeds)


async def get_genre(category):
    if category == "male_pfps":
        return random.choice(PFPS.male)
    elif category == "female_pfps":
        return random.choice(PFPS.female)
    elif category == "anime_pfps":
        return random.choice(PFPS.anime)
    elif category == "male_gifs":
        return random.choice(PFPS.male_gif)
    elif category == "female_gifs":
        return random.choice(PFPS.female_gif)
    elif category == "anime_gifs":
        return random.choice(PFPS.anime_gif)
    elif category == "banners":
        return random.choice(PFPS.banner)


@tasks.loop(minutes=10)
async def counter_update(bot: commands.AutoShardedBot):
    results = await bot.db.fetch("SELECT * FROM counters")
    for result in results:
        channel = bot.get_channel(int(result["channel_id"]))
        if channel:
            guild = channel.guild
            module = result["module"]
            if module == "members":
                target = str(guild.member_count)
            elif module == "humans":
                target = str(len([m for m in guild.members if not m.bot]))
            elif module == "bots":
                target = str(len([m for m in guild.members if m.bot]))
            elif module == "boosters":
                target = str(len(guild.premium_subscribers))
            elif module == "voice":
                target = str(sum(len(c.members) for c in guild.voice_channels))
            name = result["channel_name"].replace("{target}", target)
            await channel.edit(name=name, reason="updating counter")


@tasks.loop(minutes=1)
async def autopfp(bot: commands.AutoShardedBot):
    results = await bot.db.fetch("SELECT * FROM autopfp")
    for result in results:
        embed = discord.Embed(color=bot.color, title="")
        if result["genre"] == "random":
            links = await get_genre(
                random.choice(
                    [
                        "anime_pfps",
                        "anime_gifs",
                        "male_pfps",
                        "male_gifs",
                        "female_pfps",
                        "female_gifs",
                    ]
                )
            )
        if result["genre"] == "banner":
            links = await get_genre("banners")
        else:
            links = await get_genre(f"{result['genre']}_{result['type']}s")
        embed.set_image(url=links)
        button2 = Button(
            style=discord.ButtonStyle.link,
            label="Want this in your server? Invite Me!",
            url="https://discord.com/api/oauth2/authorize?client_id=1096702249364885624&permissions=8&scope=bot",
        )
        view = View()
        view.add_item(button2)
        channel_id = result["channel_id"]
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(embed=embed, view=view)
            await asyncio.sleep(10)


async def gwend_task(bot: commands.AutoShardedBot, result, date: datetime.datetime):
    members = json.loads(result["members"])
    winners = result["winners"]
    channel_id = result["channel_id"]
    message_id = result["message_id"]
    channel = bot.get_channel(channel_id)
    if channel:
        message = await channel.fetch_message(message_id)
        if message:
            wins = []
            if len(members) <= winners:
                embed = discord.Embed(
                    color=bot.color,
                    title=message.embeds[0].title,
                    description=f"Hosted by: <@!{result['host']}>\n\nNot enough entries to determine the winners!",
                )
                await message.edit(embed=embed, view=None)
            else:
                for _ in range(winners):
                    wins.append(random.choice(members))
                embed = discord.Embed(
                    color=bot.color,
                    title=message.embeds[0].title,
                    description=f"Ended <t:{int(date.timestamp())}:R>\nHosted by: <@!{result['host']}>",
                ).add_field(
                    name="winners",
                    value="\n".join([f"**{bot.get_user(w)}** ({w})" for w in wins]),
                )
                await message.edit(embed=embed, view=None)
                await message.reply(
                    f"**{result['title']}** winners:\n"
                    + "\n".join([f"<@{w}> ({w})" for w in wins])
                )
    await bot.db.execute(
        "INSERT INTO gw_ended VALUES ($1,$2,$3)",
        channel_id,
        message_id,
        json.dumps(members),
    )
    await bot.db.execute(
        "DELETE FROM giveaway WHERE channel_id = $1 AND message_id = $2",
        channel_id,
        message_id,
    )


@tasks.loop(seconds=5)
async def gw_loop(bot: commands.AutoShardedBot):
    results = await bot.db.fetch("SELECT * FROM giveaway")
    date = datetime.datetime.now()
    for result in results:
        if date.timestamp() > result["finish"].timestamp():
            await gwend_task(bot, result, date)


async def paginator(self, embeds: List[discord.Embed]):
    if len(embeds) == 1:
        return await self.send(embed=embeds[0])

    view = Paginator(self, embeds)
    view.message = await self.reply(embed=embeds[0], view=view)


async def cmdhelp(self):
    command = self.command
    commandname = (
        f"{str(command.parent)} {command.name}"
        if str(command.parent) != "None"
        else command.name
    )
    if command.cog_name == "owner":
        return
    if command.cog_name == "auth":
        return

    embed = discord.Embed(
        color=bot.color, title=commandname, description=f"`{command.description}`"
    )
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
    embed.add_field(
        name="usage",
        value=f"```{commandname} {command.usage if command.usage else ''}```",
        inline=False,
    )
    embed.set_footer(
        text=f"Aliases: {', '.join(map(str, command.aliases)) or 'none'} • Category: {command.help}"
    )
    await self.reply(embed=embed)


async def create_pages(self):
    embeds = []
    p = 0

    for command in self.command.commands:
        commandname = (
            f"{str(command.parent)} {command.name}"
            if str(command.parent) != "None"
            else command.name
        )
        p += 1
        embeds.append(
            discord.Embed(
                color=bot.color,
                title=f"{commandname}",
                description=f"`{command.description}`",
            )
            .set_author(name=bot.user.name, icon_url=bot.user.display_avatar.url)
            .add_field(
                name="usage",
                value=f"```{commandname} {command.usage if command.usage else ''}```",
                inline=False,
            )
            .set_footer(
                text=f"page: {p}/{len(self.command.commands)} • Aliases: {', '.join(a for a in command.aliases) if len(command.aliases) > 0 else 'none'} ・ Category: {command.help}"
            )
        )

    return await self.paginator(embeds)


class greed(commands.AutoShardedBot):
    __is_hidden_event__ = True

    def __init__(self):
        super().__init__(
            command_prefix=getprefix,
            help_command=None,
            intents=intents,
            allowed_mentions=discord.AllowedMentions(
                everyone=False, users=True, roles=False, replied_user=False
            ),
            case_sensitive=False,
            strip_after_prefix=True,
            description="*cut*",
            activity=discord.Activity(
                name="tear.lol",
                url="https://twitch.tv/cut",
                type=discord.ActivityType.competing,
            ),
            owner_ids=[628236220392275969, 1040008141301088276],
        )
        self.uptime = time.time()
        self.persistent_views_added = False
        self.cogs_loaded = False
        self.color = 0x2B2D31
        self.yes = "✔"
        self.no = "❌"
        self.warning = "⚠"
        self.left = "◀"
        self.right = "▶"
        self.proxy_url = "http://zplqmkhc-rotate:ci3sbpslnawy@p.webshare.io:80/"
        self.m_cd = commands.CooldownMapping.from_cooldown(
            1, 5, commands.BucketType.member
        )
        self.c_cd = commands.CooldownMapping.from_cooldown(
            1, 5, commands.BucketType.channel
        )
        self.m_cd2 = commands.CooldownMapping.from_cooldown(
            1, 10, commands.BucketType.member
        )
        self.global_cd = commands.CooldownMapping.from_cooldown(
            2, 3, commands.BucketType.member
        )
        self.ext = Client(self)

    async def create_db_pool(self):
        self.db = await asyncpg.create_pool(
            port=5432,
            user="postgres",
            database="postgres",
            password="zCfko8ZMTpxH6qzwYzyh6160kF2sQPcvR87mEN9bG6uLzCvDGXyX6AFUMaVRHfqlhKOhw7QgR4XivZFb2",
            host="db.efnskovmlwellenmssla.supabase.co",
        )

    async def get_context(self, message, *, cls=Context):
        return await super().get_context(message, cls=cls)

    async def setup_hook(self) -> None:
        print("Attempting to connect")
        self.session = HTTP()
        bot.loop.create_task(bot.create_db_pool())
        await self.load_extension("jishaku")
        self.add_view(vmbuttons())
        self.add_view(CreateTicket())
        self.add_view(DeleteTicket())
        bot.loop.create_task(StartUp.startup(bot))

    @property
    def ping(self) -> int:
        return round(self.latency * 1000) / 4

    def convert_datetime(self, date: datetime.datetime = None):
        if date is None:
            return None
        month = f"0{date.month}" if date.month < 10 else date.month
        day = f"0{date.day}" if date.day < 10 else date.day
        year = date.year
        minute = f"0{date.minute}" if date.minute < 10 else date.minute
        if date.hour < 10:
            hour = f"0{date.hour}"
            meridian = "AM"
        elif date.hour > 12:
            hour = f"0{date.hour - 12}" if date.hour - 12 < 10 else f"{date.hour - 12}"
            meridian = "PM"
        else:
            hour = date.hour
            meridian = "PM"
        return f"{month}/{day}/{year} at {hour}:{minute} {meridian} ({discord.utils.format_dt(date, style='R')})"

    def is_dangerous(self, role: discord.Role) -> bool:
        permissions = role.permissions
        return any(
            [
                permissions.kick_members,
                permissions.ban_members,
                permissions.administrator,
                permissions.manage_channels,
                permissions.manage_guild,
                permissions.manage_messages,
                permissions.manage_roles,
                permissions.manage_webhooks,
                permissions.manage_emojis_and_stickers,
                permissions.manage_threads,
                permissions.mention_everyone,
                permissions.moderate_members,
            ]
        )

    async def getbyte(self, video: str):
        return BytesIO(await self.session.read(video, proxy=self.proxy_url, ssl=False))

    async def prefixes(self, message: discord.Message) -> List[str]:
        prefixes = []
        for l in set(p for p in await self.command_prefix(self, message)):
            prefixes.append(l)
        return prefixes

    async def guild_change(self, mes: str, guild: discord.Guild) -> discord.Message:
        channel = self.get_channel(1120603031805886474)
        try:
            await channel.send(
                embed=discord.Embed(
                    color=self.color,
                    description=f"{mes} **{guild.name}** owned by **{guild.owner}** with **{guild.member_count}** members",
                )
            )
        except:
            pass

    async def on_guild_join(self, guild: discord.Guild):
        if not guild.chunked:
            await guild.chunk(cache=True)
        await self.guild_change("joined", guild)

    async def on_guild_remove(self, guild: discord.Guild):
        await self.guild_change("left", guild)

    async def channel_ratelimit(self, message: discord.Message) -> typing.Optional[int]:
        cd = self.c_cd
        bucket = cd.get_bucket(message)
        return bucket.update_rate_limit()

    async def member_ratelimit(self, message: discord.Message) -> typing.Optional[int]:
        cd = self.m_cd
        bucket = cd.get_bucket(message)
        return bucket.update_rate_limit()

    async def on_ready(self):
        await Music(self).start_node()
        await create_db(self)
        if self.cogs_loaded == False:
            await StartUp.loadcogs(self)
        counter_update.start(bot)
        autopfp.start(bot)
        gw_loop.start(bot)
        print(f"Connected in as {self.user} {self.user.id}")

    async def on_message_edit(self, before, after):
        if before.content != after.content:
            await self.process_commands(after)

    async def on_message(self, message: discord.Message):
        channel_rl = await self.channel_ratelimit(message)
        member_rl = await self.member_ratelimit(message)
        if channel_rl == True:
            return
        if member_rl == True:
            return
        if message.content == "<@{}>".format(self.user.id):
            embed = discord.Embed(
                color=bot.color,
                description=f"Prefix: "
                + " ".join(f"`{g}`" for g in await self.prefixes(message)),
            )
            return await message.reply(embed=embed)
        await bot.process_commands(message)

    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.NotOwner):
            pass
        elif isinstance(error, commands.CheckFailure):
            if isinstance(error, commands.MissingPermissions):
                return await ctx.send_warning(
                    f"This command requires **{error.missing_permissions[0]}** permissions"
                )
        elif isinstance(error, commands.CommandOnCooldown):
            if ctx.command.name != "hit":
                return  # await ctx.reply(embed=discord.Embed(color=0x6d827d, description=f"<:warning:1124999030158655519> {ctx.author.mention}: You are on cooldown. Try again in {format_timespan(error.retry_after)}"), mention_author=False)
        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.cmdhelp()
        elif isinstance(error, commands.EmojiNotFound):
            return await ctx.send_warning(
                f"Unable to convert {error.argument} into an **emoji**"
            )
        elif isinstance(error, commands.MemberNotFound):
            return await ctx.send_warning(f"Unable to find member **{error.argument}**")
        elif isinstance(error, commands.UserNotFound):
            return await ctx.send_warning(f"Unable to find user **{error.argument}**")
        elif isinstance(error, commands.RoleNotFound):
            return await ctx.send_warning(f"Couldn't find role **{error.argument}**")
        elif isinstance(error, commands.ChannelNotFound):
            return await ctx.send_warning(f"Couldn't find channel **{error.argument}**")
        elif isinstance(error, commands.UserConverter):
            return await ctx.send_warning(f"Couldn't convert that into an **user** ")
        elif isinstance(error, commands.MemberConverter):
            return await ctx.send_warning("Couldn't convert that into a **member**")
        elif isinstance(error, commands.BadArgument):
            return await ctx.send_warning(error.args[0])
        elif isinstance(error, commands.BotMissingPermissions):
            return await ctx.send_warning(
                "I do not have enough **permission** to do this"
            )
        elif isinstance(error, discord.HTTPException):
            return await ctx.send_warning("Unable to execute this command")
        else:
            key = await checkthekey(generate_key())
            trace = str(error)
            rl = await self.member_ratelimit(ctx.message)
            if rl == True:
                return
            await self.db.execute("INSERT INTO cmderror VALUES ($1,$2)", key, trace)
            await self.ext.send_error(
                ctx,
                f"An unexpected error was found while processing the command **{ctx.command.name}**. Please report the code `{key}` in our [**support server**](https://discord.gg/greedbot)",
            )


bot = greed()


@bot.check
async def cooldown_check(ctx: commands.Context):
    bucket = bot.global_cd.get_bucket(ctx.message)
    retry_after = bucket.update_rate_limit()
    if retry_after:
        raise commands.CommandOnCooldown(
            bucket, retry_after, commands.BucketType.member
        )
    return True


async def check_ratelimit(ctx):
    cd = bot.m_cd2.get_bucket(ctx.message)
    return cd.update_rate_limit()


@bot.check
async def is_chunked(ctx: commands.Context):
    if ctx.guild:
        if not ctx.guild.chunked:
            await ctx.guild.chunk(cache=True)
        return True


@bot.check
async def disabled_command(ctx: commands.Context):
    cmd = bot.get_command(ctx.invoked_with)
    if not cmd:
        return True
    check = await ctx.bot.db.fetchrow(
        "SELECT * FROM disablecommand WHERE command = $1 AND guild_id = $2",
        cmd.name,
        ctx.guild.id,
    )
    if check:
        await bot.ext.send_warning(ctx, f"The command **{cmd.name}** is **disabled**")
    return check is None


if __name__ == "__main__":
    token = "NjA1NTA2Mjc0ODk2OTA0MTky.GPOIS3._2kvzd9nOYh4ME-GVB_vVzmd6Ah5TSNWkTkErc"
    bot.run(token)
