from random import choice
from discord import Embed, Member, User, Spotify, Role, TextChannel, Color
from discord.ext.commands import (
    Context,
    command,
    Cog,
    Author,
    is_owner,
    group,
    AutoShardedBot as Bot,
)
import discord, uwuipy, datetime, io, arrow, aiogtts, os
from tools.checks import Perms
from typing import Union
from discord.ui import View, Button
import requests
from deep_translator import GoogleTranslator
from discord.ext import tasks
from io import BytesIO
import time
from ttapi import TikTokApi
from aiogtts import aiogTTS
from handlers.lastfmhandler import Handler
import urllib.request
from bs4 import BeautifulSoup
from PIL import Image
import numpy as np
import json
import humanize
import instaloader
from datetime import datetime
import fortnite_api


api = fortnite_api.FortniteAPI(api_key="633b1210-acc9-4a0e-8569-b3bd7bcbb036")
tiktok = TikTokApi(debug=False)
DISCORD_API_LINK = "https://discord.com/api/invite/"


def human_format(number):
    if number > 999:
        return humanize.naturalsize(number, False, True)
    return number


@tasks.loop(seconds=10)
async def bday_task(bot: Bot):
    results = await bot.db.fetch("SELECT * FROM birthday")
    for result in results:
        if (
            arrow.get(result["bday"]).day == arrow.utcnow().day
            and arrow.get(result["bday"]).month == arrow.utcnow().month
        ):
            if result["state"] == "false":
                member = await bot.fetch_user(result["user_id"])
                if member:
                    try:
                        await member.send(f"🎂 Happy birthday gang <@{member.id}>!!")
                        await bot.db.execute(
                            "UPDATE birthday SET state = $1 WHERE user_id = $2",
                            "true",
                            result["user_id"],
                        )
                    except:
                        continue
        else:
            if result["state"] == "true":
                await bot.db.execute(
                    "UPDATE birthday SET state = $1 WHERE user_id = $2",
                    "false",
                    result["user_id"],
                )


class Utility(Cog):
    __is_hidden_event__ = True

    def __init__(self, bot: Bot):
        self.bot = bot
        self.lastfmhandler = Handler("289e4e09a1126fd938c1e1deeed869c7")
        self.cake = "🎂"

    async def make_request(self, url: str, action: str = "get", params: dict = None):
        r = await self.bot.session.get(url, params=params)
        if action == "get":
            return await r.json()
        if action == "read":
            return await r.read()

    async def bday_send(self, ctx: Context, message: str) -> discord.Message:
        return await ctx.reply(
            embed=discord.Embed(
                color=self.bot.color,
                description=f"{self.cake} {ctx.author.mention}: {message}",
            )
        )

    @Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        bday_task.start(self.bot)

    @command(
        description="gets the invite link with administrator permission of a bot",
        help="utility",
        usage="[bot id]",
    )
    async def getbotinvite(self, ctx: Context, id: User):
        if not id.bot:
            return await ctx.send_error("This is **not** a bot")
        embed = Embed(
            color=self.bot.color,
            description=f"```Click the button below to invite {id.name}.```",
        )
        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label=f"invite {id.name}",
                url=f"https://discord.com/api/oauth2/authorize?client_id={id.id}&permissions=8&scope=bot%20applications.commands",
            )
        )
        await ctx.reply(embed=embed, view=view)

    @command(
        aliases=["tts", "speech"],
        description="convert your message to mp3",
        help="utility",
        usage="[message]",
    )
    async def texttospeech(self, ctx: Context, *, txt: str):
        lol = BytesIO()
        vc = aiogTTS()
        await vc.save(txt, "tts.mp3", lang="en")
        await vc.write_to_fp(txt, lol, slow=False, lang="en")
        await ctx.reply(file=discord.File(fp="tts.mp3", filename="tts.mp3"))
        return os.remove("tts.mp3")

    @command(
        description="search for images on google",
        help="utility",
        usage="[query]",
        aliases=["img", "google"],
    )
    async def image(self, ctx: Context, *, query: str):
        embeds = []
        data = await self.bot.session.json(
            "https://notsobot.com/api/search/google/images",
            params={"query": query, "safe": "True"},
        )
        for item in data:
            embeds.append(
                Embed(
                    color=self.bot.color,
                    title=f"Search results for {query}",
                    description=item["header"],
                    url=item["url"],
                )
                .set_image(url=item["image"]["url"])
                .set_footer(text=f"1/{len(data)} (Safe Search active)")
                .set_author(
                    name=ctx.author.global_name
                    if ctx.author.global_name
                    else ctx.author.name,
                    icon_url=ctx.author.display_avatar.url,
                )
            )
        await ctx.paginator(embeds)

    @command(
        description="show information abt an invite",
        help="utility",
        usage="[invite code]",
        aliases=["ii"],
    )
    async def inviteinfo(self, ctx: Context, code: str):
        invite_code = code
        data = await self.bot.session.json(
            DISCORD_API_LINK + invite_code, proxy=self.bot.proxy_url, ssl=False
        )
        name = data["guild"]["name"]
        id = data["guild"]["id"]
        description = data["guild"]["description"]
        boosts = data["guild"]["premium_subscription_count"]
        features = ", ".join(f for f in data["guild"]["features"])
        avatar = f"https://cdn.discordapp.com/icons/{data['guild']['id']}/{data['guild']['icon']}.{'gif' if 'a_' in data['guild']['icon'] else 'png'}?size=1024"
        banner = f"https://cdn.discordapp.com/banners/{data['guild']['id']}/{data['guild']['banner']}.{'gif' if 'a_' in data['guild']['banner'] else 'png'}?size=1024"
        splash = f"https://cdn.discordapp.com/splashes/{data['guild']['id']}/{data['guild']['splash']}.png?size=1024"
        embed = Embed(
            color=self.bot.color,
            title=f"invite info for {code}",
            url="https://discord.gg/{}".format(code),
            description=f"**{description}**",
        )
        embed.set_author(icon_url=avatar, name=f"{name} ({id})")
        embed.set_thumbnail(url=avatar)
        embed.add_field(
            name="NSWF?",
            value="```false```" if data["guild"]["nsfw"] is False else "```true```",
        )
        embed.add_field(name="Boosts:", value="```{}```".format(boosts))
        embed.add_field(
            name="Server Features:", value="```{}```".format(features), inline=False
        )
        view = View()
        view.add_item(Button(label="Icon", url=avatar))
        view.add_item(Button(label="Banner", url=banner))
        view.add_item(Button(label="Splash", url=splash))
        await ctx.reply(embed=embed, view=view)

    @command(
        description="get the first message from a channel",
        help="utility",
        usage="<channel>",
        aliases=["firstmsg"],
    )
    async def firstmessage(self, ctx: Context, *, channel: TextChannel = None):
        channel = channel or ctx.channel
        messages = [mes async for mes in channel.history(oldest_first=True, limit=1)]
        message = messages[0]
        embed = Embed(
            color=self.bot.color,
            title="first message in {}".format(channel.mention),
            description=f"```{message.content}```",
        )
        view = View()
        view.add_item(Button(label="Click to jump!", url=message.jump_url))
        await ctx.reply(embed=embed, view=view)

    @command(
        description="see informations about the server", help="utility", aliases=["si"]
    )
    async def serverinfo(self, ctx: Context):
        owner = (
            ctx.guild.owner.global_name
            if ctx.guild.owner.global_name
            else ctx.guild.owner.name
        )
        desc = ctx.guild.description if ctx.guild.description else ""
        icon = f"[Server Icon]({ctx.guild.icon})" if ctx.guild.icon else ""
        banner = f"[Server Banner]({ctx.guild.banner})" if ctx.guild.banner else ""
        splash = f"[Server Splash]({ctx.guild.splash})" if ctx.guild.splash else ""
        embed = discord.Embed(
            title=f"{ctx.guild.name}",
            description=f"Created <t:{int(ctx.guild.created_at.timestamp())}:R> owned by **{owner}**\n{desc}",
            color=self.bot.color,
        )
        embed.add_field(
            name="Info:",
            value=f"```Verification: {ctx.guild.verification_level}\nVanity: {ctx.guild.vanity_url}\nBoosts: {ctx.guild.premium_subscription_count} (Level {ctx.guild.premium_tier})```",
            inline=False,
        )
        embed.add_field(
            name=f"Channels:",
            value=f"```Total: {len(ctx.guild.channels)}\nText: {len(ctx.guild.text_channels)}\nVoice: {len(ctx.guild.voice_channels)}\nCategories: {len(ctx.guild.categories)}```",
            inline=False,
        )
        embed.add_field(
            name="Counts:",
            value=f"```Roles: {len(ctx.guild.roles)}/250\nEmojis: {len(ctx.guild.emojis)}/{ctx.guild.emoji_limit*2}\nStickers: {len(ctx.guild.stickers)}/{ctx.guild.sticker_limit}```",
            inline=False,
        )
        embed.add_field(
            name="Links:", value=f"{icon}\n{banner}\n{splash}", inline=False
        )
        embed.set_thumbnail(url=ctx.guild.icon)
        embed.set_image(url=ctx.guild.banner)
        embed.set_footer(text=f"ID: {ctx.guild.id}")
        await ctx.reply(embed=embed)

    @group(aliases=["guild"], invoke_without_command=True)
    async def server(self, ctx: Context):
        return await ctx.invoke(self.bot.get_command("serverinfo"))

    @server.command(description="show information about the server", help="utility")
    async def info(self, ctx: Context):
        return await ctx.invoke(self.bot.get_command("serverinfo"))

    @command(
        description="get role informations",
        help="utility",
        usage="[role]",
        aliases=["ri"],
    )
    async def roleinfo(self, ctx: Context, *, role: Union[Role, str]):
        if isinstance(role, str):
            role = ctx.find_role(role)
            if role is None:
                return await ctx.send_warning(f"**{role.name}** is not a valid role")

        perms = (
            ", ".join([str(p[0]) for p in role.permissions if bool(p[1]) is True])
            if role.permissions
            else "none"
        )
        embed = Embed(
            color=role.color,
            title="@{} - `{}`".format(role.name, role.id),
            timestamp=role.created_at,
        )
        embed.set_thumbnail(
            url=role.display_icon if not isinstance(role.display_icon, str) else None
        )
        embed.add_field(name="Members:", value=str(len(role.members)))
        embed.add_field(name="Mentionable:", value=str(role.mentionable).lower())
        embed.add_field(name="Hoist:", value=str(role.hoist).lower())
        embed.add_field(name="permissions", value=f"```{perms}```", inline=False)
        await ctx.reply(embed=embed)

    @command(
        description="see when an user was last seen", help="utility", usage="[member]"
    )
    async def seen(self, ctx, *, member: Member):
        check = await self.bot.db.fetchrow(
            "SELECT * FROM seen WHERE guild_id = {} AND user_id = {}".format(
                ctx.guild.id, member.id
            )
        )
        if check is None:
            return await ctx.send_warning(f"I have not seen **{member}**")
        ts = check["time"]
        embed = Embed(
            color=self.bot.color,
            description="{}: **{}** was last seen <t:{}:R>".format(
                ctx.author.mention, member, ts
            ),
        )
        await ctx.reply(embed=embed)

    @command(
        description="clear the snipes in the server",
        help="utility",
        aliases=["cs", "clearsnipes"],
    )
    @Perms.get_perms("manage_messages")
    async def clearsnipe(self, ctx):
        lis = ["snipe"]
        for l in lis:
            await self.bot.db.execute(
                f"DELETE FROM {l} WHERE guild_id = $1", ctx.guild.id
            )
        await ctx.send_success("**Cleared** all snipes")

    @command(
        aliases=["s"],
        description="check the latest deleted message from a channel",
        help="utility",
    )
    async def snipe(self, ctx: Context, *, number: int = 1):
        check = await self.bot.db.fetch(
            "SELECT * FROM snipe WHERE guild_id = {} AND channel_id = {}".format(
                ctx.guild.id, ctx.channel.id
            )
        )
        if len(check) == 0:
            return await ctx.send_nonefound(
                "**No deleted messages** found in this channel"
            )
        if number > len(check):
            return await ctx.send_warning(
                f"snipe limit is **{len(check)}**".capitalize()
            )
        sniped = check[::-1][number - 1]
        em = Embed(
            color=self.bot.color,
            description=sniped["content"],
            timestamp=sniped["time"],
        )
        em.set_author(name=sniped["author"], icon_url=sniped["avatar"])
        em.set_footer(text="{}/{}".format(number, len(check)))
        if sniped["attachment"] != "none":
            if ".mp4" in sniped["attachment"] or ".mov" in sniped["attachment"]:
                url = sniped["attachment"]
                r = await self.bot.session.read(url)
                bytes_io = BytesIO(r)
                file = discord.File(fp=bytes_io, filename="video.mp4")
                return await ctx.reply(embed=em, file=file)
            else:
                try:
                    em.set_image(url=sniped["attachment"])
                except:
                    pass
        return await ctx.reply(embed=em)

    @command(
        aliases=["es"],
        description="get the most recent edited messages from the channel",
        help="utility",
        usage="<number>",
    )
    async def editsnipe(self, ctx: Context, number: int = 1):
        results = await self.bot.db.fetch(
            "SELECT * FROM editsnipe WHERE guild_id = $1 AND channel_id = $2",
            ctx.guild.id,
            ctx.channel.id,
        )
        if len(results) == 0:
            return await ctx.send_warning(
                "There are **no edited messages** in this channel"
            )
        if number > len(results):
            return await ctx.send_warning(
                f"The maximum amount of snipes is **{len(results)}**"
            )
        sniped = results[::-1][number - 1]
        embed = Embed(color=self.bot.color)
        embed.set_author(name=sniped["author_name"], icon_url=sniped["author_avatar"])
        embed.add_field(name="Before:", value=f"```{sniped['before_content']}```")
        embed.add_field(
            name="After", value=f"```{sniped['after_content']}```", inline=False
        )
        embed.set_footer(text=f"{number}/{len(results)}")
        await ctx.reply(embed=embed)

    @command(help="afk", description="afk man", usage="[command]")
    async def afk(self, ctx, *, reason="AFK"):
        result = await self.bot.db.fetchrow(
            "SELECT * FROM afk WHERE guild_id = $1 AND user_id = $2",
            ctx.guild.id,
            ctx.author.id,
        )
        if result is None:
            await self.bot.db.execute(
                "INSERT INTO afk (guild_id, user_id, reason) VALUES ($1, $2, $3)",
                ctx.guild.id,
                ctx.author.id,
                reason,
            )
            embed = discord.Embed(
                description=f"> <:ZzZ:1174909359365570580> {ctx.author.mention}: You're now AFK with the status: **{reason}**",
                color=0x54BBFF,
            )
            await ctx.send(embed=embed)

    @Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        mentioned_users = message.mentions
        for user in mentioned_users:
            result = await self.bot.db.fetchrow(
                "SELECT * FROM afk WHERE guild_id = $1 AND user_id = $2",
                message.guild.id,
                user.id,
            )
            if result:
                await message.channel.send(
                    embed=discord.Embed(
                        description=f"> <:ZzZ:1174909359365570580> {user.mention} is AFK: **{result['reason']}**",
                        color=0x54BBFF,
                    )
                )

        result = await self.bot.db.fetchrow(
            "SELECT * FROM afk WHERE guild_id = $1 AND user_id = $2",
            message.guild.id,
            message.author.id,
        )
        if result:
            await self.bot.db.execute(
                "DELETE FROM afk WHERE guild_id = $1 AND user_id = $2",
                message.guild.id,
                message.author.id,
            )

    @command(
        description="uwuify a message",
        help="utility",
        usage="[message]",
        aliases=["uwu"],
    )
    async def uwuify(self, ctx: Context, *, message: str):
        uwu = uwuipy.uwuipy()
        uwu_message = uwu.uwuify(message)
        await ctx.reply(uwu_message)

    @command(description="delete your name history", help="utility")
    async def clearnames(self, ctx: Context):
        embed = Embed(
            color=self.bot.color,
            description="Are you sure you want to clear your usernames?",
        )
        yes = discord.ui.Button(emoji=self.bot.yes)
        no = discord.ui.Button(emoji=self.bot.no)

        async def yes_callback(interaction: discord.Interaction):
            if interaction.user.id != ctx.author.id:
                return await self.bot.ext.send_warning(
                    interaction,
                    "You are **not the author** of this embed",
                    ephemeral=True,
                )
            await self.bot.db.execute(
                "DELETE FROM oldusernames WHERE user_id = $1", ctx.author.id
            )
            return await interaction.response.edit_message(
                view=None,
                embed=discord.Embed(
                    color=self.bot.color,
                    description=f"{self.bot.yes} {interaction.user.mention}: Your name history has been **deleted**",
                ),
            )

        async def no_callback(interaction: discord.Interaction):
            if interaction.user.id != ctx.author.id:
                return await self.bot.ext.send_warning(
                    interaction,
                    "You are **not the author** of this embed",
                    ephemeral=True,
                )
            return await interaction.response.edit_message(
                view=None,
                embed=discord.Embed(
                    color=self.bot.color, description=f"aborting action..."
                ),
            )

        yes.callback = yes_callback
        no.callback = no_callback
        view = discord.ui.View()
        view.add_item(yes)
        view.add_item(no)
        await ctx.reply(embed=embed, view=view)

    @command(
        description="see the old names for a user",
        help="utility",
        usage="<user>",
        aliases=["names"],
    )
    async def usernames(self, ctx, member: User = None):
        if not member:
            member = ctx.author
        check = await self.bot.db.fetch(
            "SELECT * FROM oldusernames WHERE user_id = $1", member.id
        )
        i = 0
        k = 1
        l = 0
        num = 0
        mes = ""
        number = []
        messages = []
        if check:
            for chec in check[::-1]:
                username = chec["username"]
                num += 1
                mes += f"\n`{num}` {username}"
                k += 1
                l += 1
                if l == 10:
                    messages.append(mes)
                    number.append(
                        Embed(color=self.bot.color, description=mes).set_author(
                            name=f"Past usernames for {member.name}",
                            icon_url=member.display_avatar.url,
                        )
                    )
                    i += 1
                    mes = ""
                    l = 0
            messages.append(mes)
            number.append(
                Embed(color=self.bot.color, description=mes).set_author(
                    name=f"Past usernames for {member.name}",
                    icon_url=member.display_avatar.url,
                )
            )
            return await ctx.paginator(number)
        else:
            return await ctx.send_warning(
                f"no changed usernames found for **{member}**".capitalize()
            )

    @group(description="see all server boosters", help="utility")
    async def boosters(self, ctx: Context):
        if (
            not ctx.guild.premium_subscriber_role
            or len(ctx.guild.premium_subscriber_role.members) == 0
        ):
            return await ctx.send_warning(
                "this server **does not** have any boosters".capitalize()
            )
        i = 0
        k = 1
        l = 0
        mes = ""
        number = []
        messages = []
        for member in ctx.guild.premium_subscriber_role.members:
            mes = f"{mes}`{k}` {member}\n"
            k += 1
            l += 1
            if l == 10:
                messages.append(mes)
                number.append(
                    Embed(
                        color=self.bot.color,
                        title=f"{ctx.author.guild.name} Boosters, ({len(ctx.guild.premium_subscriber_role.members)})",
                        description=messages[i],
                    )
                )
                i += 1
                mes = ""
                l = 0

        messages.append(mes)
        number.append(
            Embed(
                color=self.bot.color,
                title=f"{ctx.author.guild.name} Boosters, ({len(ctx.guild.premium_subscriber_role.members)})",
                description=messages[i],
            )
        )
        await ctx.paginator(number)

    @boosters.command(name="lost", description="display lost boosters", help="utility")
    async def boosters_lost(self, ctx: Context):
        results = await self.bot.db.fetch(
            "SELECT * FROM boosterslost WHERE guild_id = $1", ctx.guild.id
        )
        if len(results) == 0:
            return await ctx.send_warning("There are **no** lost boosters")
        i = 0
        k = 1
        l = 0
        mes = ""
        number = []
        messages = []
        for result in results[::-1]:
            mes = f"{mes}`{k}` <@!{int(result['user_id'])}> - <t:{result['time']}:R> \n"
            k += 1
            l += 1
            if l == 10:
                messages.append(mes)
                number.append(
                    Embed(
                        color=self.bot.color,
                        title=f"{ctx.author.guild.name} Lost Boosters, ({len(results)})",
                        description=messages[i],
                    )
                )
                i += 1
                mes = ""
                l = 0

        messages.append(mes)
        embed = Embed(
            color=self.bot.color,
            title=f"{ctx.author.guild.name} Lost Boosters, ({len(results)})",
            description=messages[i],
        )
        number.append(embed)
        await ctx.paginator(number)

    @command(
        description="see an user avatar",
        help="utility",
        usage="<member>",
        aliases=["av"],
    )
    async def avatar(self, ctx: Context, member: Union[Member, User] = None):
        if member is None:
            member = ctx.author
        if isinstance(member, Member):
            embed = Embed(
                color=self.bot.color,
                title=f"{member.name}'s Avatar",
                url=member.display_avatar.url,
            )
            embed.set_image(url=member.display_avatar.url)
            await ctx.reply(embed=embed)
        elif isinstance(member, User):
            embed = Embed(
                color=self.bot.color,
                title=f"{member.name}'s Avatar",
                url=member.display_avatar.url,
            )
            embed.set_author(
                name=ctx.author.name, icon_url=ctx.author.display_avatar.url
            )
            embed.set_image(url=member.display_avatar.url)
            await ctx.reply(embed=embed)

    @command(
        description="check how many members does your guild has",
        help="utility",
        aliases=["mc"],
    )
    async def membercount(self, ctx: Context):
        human_members = len([member for member in ctx.guild.members if not member.bot])
        bot_members = len([member for member in ctx.guild.members if member.bot])

        embed = discord.Embed(
            title=f"{ctx.guild.name}'s Member Count", color=self.bot.color
        )
        embed.set_thumbnail(url=ctx.guild.icon)
        embed.add_field(name="Total:", value=f"```{ctx.guild.member_count}```")
        embed.add_field(name="Humans:", value=f"```{human_members}```")
        embed.add_field(name="Bots:", value=f"```{bot_members}```")
        await ctx.reply(embed=embed)

    @command(description="see an user banner", help="utility")
    async def banner(self, ctx: Context, *, member: User = Author):
        user = await self.bot.fetch_user(member.id)
        if not user.banner:
            return await ctx.send_warning(f"**{user}** doesn't have a banner")
        embed = discord.Embed(
            color=self.bot.color, title=f"{user.name}'s Banner", url=user.banner.url
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        embed.set_image(url=user.banner.url)
        return await ctx.reply(embed=embed)

    @command(description="see a list of server roles", help="utility")
    async def roles(self, ctx):
        i = 0
        k = 1
        l = 0
        mes = ""
        number = []
        messages = []
        for role in ctx.guild.roles:
            mes = f"{mes}`{k}` <@&{role.id}> - `{len(role.members)} members`\n"
            k += 1
            l += 1
            if l == 10:
                messages.append(mes)
                number.append(
                    Embed(
                        color=self.bot.color,
                        title=f"Roles in {ctx.guild.name}, ({len(ctx.guild.roles)})",
                        description=messages[i],
                    )
                )
                i += 1
                mes = ""
                l = 0

        messages.append(mes)
        number.append(
            Embed(
                color=self.bot.color,
                title=f"Roles in {ctx.guild.name}, ({len(ctx.guild.roles)})",
                description=messages[i],
            )
        )
        await ctx.paginator(number)

    @command(description="see a list of the bots in your server", help="utility")
    async def bots(self, ctx):
        i = 0
        k = 1
        l = 0
        mes = ""
        number = []
        messages = []
        b = len(set(b for b in ctx.guild.members if b.bot))
        for m in ctx.guild.members:
            if m.bot:
                mes = f"{mes}`{k}` {m.mention} - `{m.id}`\n"
                k += 1
                l += 1
                if l == 10:
                    messages.append(mes)
                    number.append(
                        Embed(
                            color=self.bot.color,
                            title=f"Bots in {ctx.guild.name}, ({b})",
                            description=messages[i],
                        )
                    )
                    i += 1
                    mes = ""
                    l = 0

        messages.append(mes)
        number.append(
            Embed(
                color=self.bot.color,
                title=f"Bots in {ctx.guild.name}, ({b})",
                description=messages[i],
            )
        )
        await ctx.paginator(number)

    @command(
        description="show users information",
        help="utility",
        usage="<user>",
        aliases=["ui"],
    )
    async def userinfo(self, ctx: Context, *, member: Union[Member, User] = None):
        if member == None:
            member = ctx.author
        user = await self.bot.fetch_user(member.id)
        pos = sum(
            m.joined_at < member.joined_at
            for m in ctx.guild.members
            if m.joined_at is not None
        )
        role_string = " ".join([r.mention for r in member.roles][1:])
        embed = discord.Embed(color=self.bot.color)
        embed.set_thumbnail(url=member.avatar)
        embed.set_image(url=user.banner)
        embed.add_field(
            name="Created:",
            value=(
                f"<t:{int(member.created_at.timestamp())}:F>\n<t:{int(member.created_at.timestamp())}:R>"
            ),
            inline=False,
        )
        embed.add_field(
            name="Joined:",
            value=(
                f"<t:{int(member.joined_at.timestamp())}:F>\n<t:{int(member.joined_at.timestamp())}:R>"
            ),
            inline=False,
        )
        embed.add_field(
            name=f"Roles ({len(member.roles)}):", value=role_string, inline=False
        )
        embed.set_footer(text=f"ID: {member.id} | Join Position - {pos}")
        await ctx.reply(embed=embed)

    @group(
        invoke_without_command=True,
        description="show what an user is listening on spotify",
        help="utility",
        usage="<member>",
        aliases=["sp"],
    )
    async def spotify(self, ctx: Context, *, member: Member = None):
        if not member:
            member = ctx.author
        a = next((a for a in member.activities if isinstance(a, Spotify)), None)
        if not a:
            return await ctx.send_warning("You are not listening to **spotify**")
        await ctx.reply(
            f"||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||https://open.spotify.com/track/{a.track_id}"
        )

    @group(
        invoke_without_command=True,
        help="utility",
        description="check member's birthday",
        aliases=["bday"],
    )
    async def birthday(self, ctx: Context, *, member: Member = None):
        if member is None:
            member = ctx.author
        rocks = "'s"
        date = await self.bot.db.fetchrow(
            "SELECT bday FROM birthday WHERE user_id = $1", member.id
        )
        if not date:
            return await ctx.send_warning(
                f"**{'Your' if member == ctx.author else str(member) + rocks}** birthday is **not** set"
            )
        date = date["bday"]
        if "ago" in arrow.get(date).humanize(granularity="day"):
            date = date.replace(year=date.year + 1)
        else:
            date = date
        if arrow.get(date).humanize(granularity="day") == "in 0 days":
            date = "tomorrow"
        elif (
            arrow.get(date).day == arrow.utcnow().day
            and arrow.get(date).month == arrow.utcnow().month
        ):
            date = "today"
        else:
            date = arrow.get(date + datetime.timedelta(days=1)).humanize(
                granularity="day"
            )
        await self.bday_send(
            ctx,
            f"{'Your' if member == ctx.author else '**' + member.name + rocks + '**'} birthday is **{date}**",
        )

    @birthday.command(
        name="set",
        help="utility",
        description="set your birthday",
        usage="[month] [day]",
    )
    async def bday_set(self, ctx: Context, month: str, day: str):
        try:
            if len(month) == 1:
                mn = "M"
            elif len(month) == 2:
                mn = "MM"
            elif len(month) == 3:
                mn = "MMM"
            else:
                mn = "MMMM"
            if "th" in day:
                day = day.replace("th", "")
            if "st" in day:
                day = day.replace("st", "")
            if len(day) == 1:
                dday = "D"
            else:
                dday = "DD"
            ts = f"{month} {day} {datetime.date.today().year}"
            if "ago" in arrow.get(ts, f"{mn} {dday} YYYY").humanize(granularity="day"):
                year = datetime.date.today().year + 1
            else:
                year = datetime.date.today().year
            string = f"{month} {day} {year}"
            date = arrow.get(string, f"{mn} {dday} YYYY")
            check = await self.bot.db.fetchrow(
                "SELECT * FROM birthday WHERE user_id = $1", ctx.author.id
            )
            if not check:
                await self.bot.db.execute(
                    "INSERT INTO birthday VALUES ($1,$2,$3)",
                    ctx.author.id,
                    date.datetime,
                    "false",
                )
            else:
                await self.bot.db.execute(
                    "UPDATE birthday SET bday = $1 WHERE user_id = $2",
                    date.datetime,
                    ctx.author.id,
                )
            await self.bday_send(
                ctx, f"Your birthday has been set as **{month} {day}**"
            )
        except:
            return await ctx.send_error(
                f"usage: `{ctx.clean_prefix}birthday set [month] [day]`"
            )

    @birthday.command(name="unset", help="utility", description="unset your birthday")
    async def bday_unset(self, ctx: Context):
        check = await self.bot.db.fetchrow(
            "SELECT bday FROM birthday WHERE user_id = $1", ctx.author.id
        )
        if not check:
            return await ctx.send_warning("Your birthday is **not** set")
        await self.bot.db.execute(
            "DELETE FROM birthday WHERE user_id = $1", ctx.author.id
        )
        await ctx.send_warning("**Removed** your birthday")

    @command(description="see all members in a role", help="utility", usage="[role]")
    async def inrole(self, ctx: Context, *, role: Union[Role, str]):
        if isinstance(role, str):
            role = ctx.find_role(role)
            if role is None:
                return await ctx.send_warning("This isn't a valid role")

        if len(role.members) == 0:
            return await ctx.send_error("Nobody (even u) has this role")
        i = 0
        k = 1
        l = 0
        mes = ""
        number = []
        messages = []
        for member in role.members:
            mes = f"{mes}`{k}` {member.mention} - `{member.id}`\n"
            k += 1
            l += 1
            if l == 10:
                messages.append(mes)
                number.append(
                    Embed(
                        color=self.bot.color,
                        title=f"Members in {role.name}, ({len(role.members)})",
                        description=messages[i],
                    )
                )
                i += 1
                mes = ""
                l = 0

        messages.append(mes)
        embed = Embed(
            color=self.bot.color,
            title=f"Members in {role.name}, ({len(role.members)})",
            description=messages[i],
        )
        number.append(embed)
        await ctx.paginator(number)

    @command(description="see all members joined within 24 hours", help="utility")
    async def joins(self, ctx: Context):
        members = [
            m
            for m in ctx.guild.members
            if (
                datetime.datetime.now() - m.joined_at.replace(tzinfo=None)
            ).total_seconds()
            < 3600 * 24
        ]
        if len(members) == 0:
            return await ctx.send_error("No members joined in the last **24** hours")
        members = sorted(members, key=lambda m: m.joined_at)
        i = 0
        k = 1
        l = 0
        mes = ""
        number = []
        messages = []
        for member in members[::-1]:
            mes = f"{mes}`{k}` {member.mention} - `{discord.utils.format_dt(member.joined_at, style='R')}`\n"
            k += 1
            l += 1
            if l == 10:
                messages.append(mes)
                number.append(
                    Embed(
                        color=self.bot.color,
                        title=f"Joined today, ({len(members)})",
                        description=messages[i],
                    )
                )
                i += 1
                mes = ""
                l = 0

        messages.append(mes)
        embed = Embed(
            color=self.bot.color,
            title=f"Joined today, ({len(members)})",
            description=messages[i],
        )
        number.append(embed)
        await ctx.paginator(number)

    @command(
        help="utility",
        description="check the weather from a location",
        usage="[country]",
    )
    async def weather(self, ctx: Context, *, location: str):
        url = "http://api.weatherapi.com/v1/current.json"
        params = {"key": "dc1babe05aa74260b9f171215231410", "q": location}
        data = await self.bot.session.json(url, params=params)
        place = data["location"]["name"]
        country = data["location"]["country"]
        temp_c = data["current"]["temp_c"]
        temp_f = data["current"]["temp_f"]
        wind_mph = data["current"]["wind_mph"]
        wind_kph = data["current"]["wind_kph"]
        humidity = data["current"]["humidity"]
        condition_text = data["current"]["condition"]["text"]
        condition_image = "http:" + data["current"]["condition"]["icon"]
        time = datetime.datetime.fromtimestamp(
            int(data["current"]["last_updated_epoch"])
        )
        embed = discord.Embed(
            color=self.bot.color,
            title=f"{condition_text} in {place}, {country}",
            timestamp=time,
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url=condition_image)
        embed.add_field(name="Temperature:", value=f"```{temp_c} °C / {temp_f} °F```")
        embed.add_field(name="Humidity:", value=f"```{humidity}%```")
        embed.add_field(name="Wind:", value=f"```{wind_mph} mph / {wind_kph} kph```")
        return await ctx.reply(embed=embed)

    @command(
        description="shows the number of invites an user has",
        usage="<user>",
        help="utility",
    )
    async def invites(self, ctx: Context, *, member: Member = None):
        if member is None:
            member = ctx.author
        invites = await ctx.guild.invites()
        embed = Embed(
            color=self.bot.color,
            title=f"{member.name}'s Invites",
            description=f"```{member} has {sum(invite.uses for invite in invites if invite.inviter.id == member.id)} invites```",
        )
        await ctx.reply(embed=embed)

    @command(
        description="gets information about a github user",
        aliases=["gh"],
        help="utility",
        usage="[user]",
    )
    async def github(self, ctx, *, user: str):
        try:
            res = await self.bot.session.json(f"https://api.github.com/users/{user}")
            name = res["login"]
            avatar_url = res["avatar_url"]
            html_url = res["html_url"]
            email = res["email"]
            public_repos = res["public_repos"]
            followers = res["followers"]
            following = res["following"]
            twitter = res["twitter_username"]
            location = res["location"]
            embed = Embed(color=self.bot.color, title=f"@{name}", url=html_url)
            embed.set_thumbnail(url=avatar_url)
            embed.add_field(name="Followers", value=f"```{followers}```")
            embed.add_field(name="Following", value=f"```{following}```")
            embed.add_field(name="Repos", value=f"```{public_repos}```")
            if email:
                embed.add_field(name="Email", value=f"```{email}```")
            if location:
                embed.add_field(name="Location", value=f"```{location}```")
            if twitter:
                embed.add_field(name="Twitter", value=f"```{twitter}```")
            embed.set_thumbnail(url=avatar_url)
            await ctx.reply(embed=embed)
        except:
            return await ctx.send_warning(
                f"Could not find [@{user}](https://github.com/{user})"
            )

    @command(
        aliases=["tr"],
        description="translate a message",
        help="utility",
        usage="[language] [message]",
    )
    async def translate(self, ctx: Context, lang: str, *, mes: str):
        translated = GoogleTranslator(source="auto", target=lang).translate(mes)
        embed = Embed(
            color=self.bot.color,
            description="```{}```".format(translated),
            title="Translated to {}".format(lang),
        )
        await ctx.reply(embed=embed)

    @command(
        description="get a random tiktok video", help="utility", aliases=["foryou"]
    )
    async def fyp(self, ctx: Context):
        await ctx.typing()
        fyp_videos = await tiktok.feed.for_you(count=1)
        videos = []
        for vid in fyp_videos:
            videos.append(vid)

        video = choice(videos)
        no_watermark_download = video["download_urls"]["no_watermark"]
        video_binary = await tiktok.video.get_video_binary(no_watermark_download)
        bytes_io = BytesIO(video_binary)
        embed = Embed(color=self.bot.color)
        embed.description = f'[{video["description"]}]({video["video_url"]})'
        embed.set_author(
            name="@" + video["author"]["username"],
            icon_url=video["author"]["avatar_url"],
        )
        embed.set_footer(
            text=f"❤️ {human_format(video['stats']['likes'])} 💬 {human_format(video['stats']['comment_count'])} 🔗 {human_format(video['stats']['shares'])} ({human_format(video['stats']['views'])} views)"
        )
        await ctx.reply(
            embed=embed, file=discord.File(fp=bytes_io, filename="pleasehelpgreed.mp4")
        )

    @command(description="get a server's icon", help="utility", aliases=["sicon"])
    async def servericon(self, ctx: Context, *, id: int = None):
        guild = ctx.guild
        if not guild.icon:
            return await ctx.send_warning("this server has no icon".capitalize())
        embed = Embed(
            color=self.bot.color, title=f"{guild.name}'s icon", url=guild.icon.url
        )
        embed.set_image(url=guild.icon.url)
        await ctx.reply(embed=embed)

    @command(description="get a server's banner", help="utility", aliases=["sbanner"])
    async def serverbanner(self, ctx: Context):
        guild = ctx.guild
        if not guild.banner:
            return await ctx.send_warning("this server has no banner".capitalize())
        embed = Embed(
            color=self.bot.color, title=f"{guild.name}'s banner", url=guild.banner.url
        )
        embed.set_image(url=guild.banner.url)
        await ctx.reply(embed=embed)

    @command(
        description="get a server's invite background image",
        help="utility",
        aliases=["ssplash"],
    )
    async def serversplash(self, ctx: Context):
        guild = ctx.guild
        if not guild.splash:
            return await ctx.send_warning("this server has no splash".capitalize())
        embed = Embed(
            color=self.bot.color,
            title=f"{guild.name}'s invite background",
            url=guild.splash.url,
        )
        embed.set_image(url=guild.splash.url)
        await ctx.reply(embed=embed)

    @command(
        description="get a internet protocall address information",
        help="utility",
        usage="[ip]",
    )
    async def ipinfo(self, ctx: Context, ip=None):
        await ctx.typing()
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()

        if "ip" in data:
            embed = discord.Embed(title=f"{ip} Information", color=self.bot.color)
            embed.add_field(
                name="Location:",
                value=f"```{data['city']}, {data['region']}, {data['country']}```",
                inline=False,
            )
            embed.add_field(
                name="Lat/Long:", value=f"```{data['loc']}```", inline=False
            )
            embed.add_field(
                name="Organization:", value=f"```{data['org']}```", inline=False
            )
            embed.set_footer(icon_url=ctx.author.avatar, text=ctx.author.name)
            await ctx.reply(embed=embed)
        else:
            await ctx.send_error("**Invalid** IP address.")

    @command(
        description="get a instagrams account information",
        help="utility",
        usage="[username]",
        aliases=["iginfo", "ig"],
    )
    async def instagram(self, ctx: Context, username):
        await ctx.typing()
        L = instaloader.Instaloader()
        try:
            profile = instaloader.Profile.from_username(L.context, username)
            embed = discord.Embed(
                title=f"{profile.username}, {profile.full_name}", color=self.bot.color
            )
            embed.set_thumbnail(url=profile.profile_pic_url)
            embed.add_field(
                name="Followers:", value=f"{profile.followers}", inline=True
            )
            embed.add_field(
                name="Following:", value=f"{profile.followees}", inline=True
            )
            embed.add_field(name="Posts:", value=f"{profile.mediacount}", inline=True)
            embed.add_field(
                name="Biography:", value=f"```{profile.biography}```", inline=False
            )
            await ctx.reply(embed=embed)
        except instaloader.exceptions.ProfileNotExistsException:
            await ctx.send_error("Instagram profile not found.")

    @command(
        description="get a instagrams post information",
        help="utility",
        usage="[url]",
        aliases=["igpost"],
    )
    async def instagrampost(self, ctx: Context, post_url):
        await ctx.typing()
        L = instaloader.Instaloader()
        try:
            post = instaloader.Post.from_shortcode(L.context, post_url.split("/")[-2])
            views = post.video_view_count if post.is_video else None
            likes = post.likes
            comments = post.comments
            if post.is_video:
                image_url = post.video_url
                urllib.request.urlretrieve(image_url, f"{post.owner_username}.mp4")
                embed = discord.Embed(
                    description=f"[{post.caption}]({post_url})", color=self.bot.color
                )
                embed.set_author(
                    icon_url=post.owner_profile.profile_pic_url,
                    name=post.owner_username,
                )
                embed.set_footer(text=f"❤️ {likes} 💬 {comments} | {views} views")
                await ctx.reply(
                    file=discord.File(f"{post.owner_username}.mp4"), embed=embed
                )
                os.remove(f"{post.owner_username}.mp4")
                L.close()
            else:
                image_url = post.url
                urllib.request.urlretrieve(image_url, f"{post.owner_username}.png")
                embed = discord.Embed(
                    description=f"[{post.caption}]({post_url})", color=self.bot.color
                )
                embed.set_author(
                    icon_url=post.owner_profile.profile_pic_url,
                    name=post.owner_username,
                )
                embed.set_footer(text=f"❤️ {likes} 💬 {comments}")
                await ctx.reply(
                    file=discord.File(f"{post.owner_username}.png"), embed=embed
                )
                os.remove(f"{post.owner_username}.png")
                L.close()
        except Exception as e:
            await ctx.send_warning(
                f"Instagram's API has put greed on a **cooldown** please try again later..."
            )

    @command(
        description="get a tiktok's post information",
        help="utility",
        usage="[url]",
        aliases=["ttpost"],
    )
    async def tiktokpost(self, ctx: Context, url):
        if "tiktok" in url:
            async with ctx.typing():
                x = await self.bot.session.json(
                    "https://tikwm.com/api/", params={"url": url}
                )
                video = x["data"]["play"]
                file = discord.File(
                    fp=await self.bot.getbyte(video), filename="tiktok.mp4"
                )
                embed = discord.Embed(
                    color=self.bot.color, description=f"[{x['data']['title']}]({url})"
                ).set_author(
                    name=f"@{x['data']['author']['unique_id']}",
                    icon_url=x["data"]["author"]["avatar"],
                )
                x = x["data"]
                embed.set_footer(
                    text=f"❤️ {self.bot.ext.human_format(x['digg_count'])}  💬 {self.bot.ext.human_format(x['comment_count'])}  🔗 {self.bot.ext.human_format(x['share_count'])}  👀 {self.bot.ext.human_format(x['play_count'])}"
                )
                await ctx.reply(embed=embed, file=file)
        else:
            await ctx.send_warning("Please mention a **valid tiktok url**")

    @command(
        description="Check Bitcoin wallet balance, total sent, total received, and value in USD",
        help="utility",
        usage="[address]",
        aliases=["btcbal", "btcwal"],
    )
    async def btcwallet(self, ctx: Context, wallet_address):
        api_url = f"https://blockchain.info/rawaddr/{wallet_address}"

        response = requests.get(api_url)
        data = response.json()

        if response.status_code == 200:
            balance_satoshis = data["final_balance"]
            balance_btc = balance_satoshis / 100000000  # Convert satoshis to BTC

            total_sent_satoshis = data["total_sent"]
            total_sent_btc = total_sent_satoshis / 100000000

            total_received_satoshis = data["total_received"]
            total_received_btc = total_received_satoshis / 100000000

            btc_to_usd_api_url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
            btc_to_usd_response = requests.get(btc_to_usd_api_url)
            btc_to_usd_data = btc_to_usd_response.json()
            btc_to_usd = btc_to_usd_data["bpi"]["USD"]["rate_float"]

            balance_usd = balance_btc * btc_to_usd
            total_sent_usd = total_sent_btc * btc_to_usd
            total_received_usd = total_received_btc * btc_to_usd

            embed = discord.Embed(color=self.bot.color, title=f"{wallet_address}")
            embed.add_field(
                name="Balance:",
                value=f"```{balance_btc:.8f} BTC (${balance_usd:.2f})```",
            )
            embed.add_field(
                name="Total Sent:",
                value=f"```{total_sent_btc:.8f} BTC (${total_sent_usd:.2f})```",
                inline=False,
            )
            embed.add_field(
                name="Total Received:",
                value=f"```{total_received_btc:.8f} BTC (${total_received_usd:.2f})```",
            )
            embed.set_thumbnail(
                url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Bitcoin.svg/1200px-Bitcoin.svg.png"
            )
            await ctx.reply(embed=embed)
        else:
            await ctx.send_warning("Please mention a **valid BTC address.**")

    @command(
        description="Make a images background transparent",
        help="utility",
        usage="[url]",
    )
    async def transparent(self, ctx: Context, url):
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))

        image = image.convert("RGBA")
        data = np.array(image)

        white = np.all(data == [255, 255, 255, 255], axis=-1)
        data[white] = [255, 255, 255, 0]

        transparent_image = Image.fromarray(data, "RGBA")

        output_buffer = BytesIO()
        transparent_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        await ctx.reply(
            file=discord.File(output_buffer, filename="transparent_image.png")
        )

    @group(invoke_without_command=True)
    async def fortnite(self, ctx):
        await ctx.create_pages()

    @fortnite.command(
        description="View the recent fortnite map and poi's.", help="utility"
    )
    async def map(self, ctx: Context):
        try:
            data = api.map.fetch()

            embed = discord.Embed(color=self.bot.color)
            embed.set_image(url=data.poi_image)
            await ctx.reply(embed=embed)
        except:
            await ctx.send_warning("The third party API is **down** atm.")

    @fortnite.command(
        description="View the recent fortnite battle royale news.", help="utility"
    )
    async def news(self, ctx: Context):
        try:
            data = api.news.fetch()

            embed = discord.Embed(color=self.bot.color)
            embed.set_image(url=data.br.image)
            await ctx.reply(embed=embed)
        except:
            await ctx.send_warning("The third party API is **down** atm.")

    @fortnite.command(description="View todays fortnite itemshop.", help="utility")
    async def itemshop(self, ctx: Context, day, month, year):
        date = datetime.now().strftime("%d-%m-%Y")
        embed = discord.Embed(color=self.bot.color)
        embed.set_image(url=f"https://bot.fnbr.co/shop-image/fnbr-shop-{date}.png")
        await ctx.reply(embed=embed)

    @fortnite.command(
        description="View a past fortnite item shop.",
        help="utility",
        usage="[day] [month] [year]\nexample: fortnite pastitemshop 10 11 2018",
    )
    async def pastitemshop(self, ctx: Context, day, month, year):
        embed = discord.Embed(color=self.bot.color)
        embed.set_image(
            url=f"https://bot.fnbr.co/shop-image/fnbr-shop-{day}-{month}-{year}.png"
        )
        await ctx.reply(embed=embed)

    @fortnite.command(
        description="View a a users fortnite stats.", help="utility", usage="[username]"
    )
    async def stats(self, ctx: Context, user):
        data = api.stats.fetch_by_name(name=user)

        embed = discord.Embed(color=self.bot.color, title=f"{user} Stats")
        embed.add_field(name="Score:", value=f"```{data.stats.all.overall}```")
        embed.add_field(name="Top 3:", value=f"```{data.stats.all.overall.top5}```")
        embed.add_field(name="Top 12:", value=f"```{data.stats.all.overall.top12}```")
        embed.add_field(name="Kills:", value=f"```{data.stats.all.overall.kills}```")
        embed.add_field(
            name="KPM:", value=f"```{data.stats.all.overall.kills_per_match}```"
        )
        embed.add_field(name="KD:", value=f"```{data.stats.all.overall.kd}```")
        embed.add_field(
            name="Matches:", value=f"```{data.stats.all.overall.matches}```"
        )
        embed.add_field(
            name="WinRate:", value=f"```{data.stats.all.overall.win_rate}```"
        )
        embed.add_field(
            name="Mins Played:", value=f"```{data.stats.all.overall.minutes_played}```"
        )
        embed.set_image(
            url="https://upload.wikimedia.org/wikipedia/commons/7/7c/Fortnite_F_lettermark_logo.png"
        )
        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Utility(bot))
