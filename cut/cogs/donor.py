from io import BytesIO
import discord, uwuipy
from discord.ext import commands
from tools.checks import Perms, Mod
from typing import Union
from datetime import datetime
from tools.utils import NoStaff
from PIL import Image
import pytesseract
import io
import json
import requests

valid = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]


def OCRImage(imageLink):
    response = requests.get(imageLink)
    img = Image.open(io.BytesIO(response.content))
    text = pytesseract.image_to_string(img)
    return text


def key(s):
    return s[2]


def checktag(table: str) -> bool:
    if len(table) > 10:
        return False
    for i in table:
        if not i in valid:
            return False
    return True


async def get_tags(bot, type, tag):
    if type == "str":
        results = await bot.db.fetch(
            "SELECT * FROM oldusernames WHERE username = $1", tag
        )
        data = [r for r in results]
    elif type == "int":
        results = await bot.db.fetch(
            "SELECT * FROM oldusernames WHERE discriminator = $1", str(tag)
        )
        data = [
            r
            for r in results
            if (
                datetime.now() - datetime.fromtimestamp(float(r["time"]))
            ).total_seconds()
            < 6 * 3600
        ]
    data.sort(key=key, reverse=True)
    return data


def premium():
    async def predicate(ctx: commands.Context):
        check = await ctx.bot.db.fetchrow(
            "SELECT * FROM donor WHERE user_id = $1", ctx.author.id
        )
        if check is None:
            await ctx.send_warning(
                "You are not a donor. Use command donate to view how to become one :)"
            )
            return False
        return True

    return commands.check(predicate)


async def get_usernames(bot, type, username):
    if type == "str":
        results = await bot.db.fetch(
            "SELECT * FROM oldusernames WHERE username = $1", username
        )
        data = [r for r in results]
    data.sort(key=key, reverse=True)
    return data


class donor(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.command(
        description="remove the hardban from an user", help="donor", usage="[user]"
    )
    @Perms.get_perms("ban_members")
    @premium()
    async def unhardban(self, ctx: commands.Context, *, member: discord.User):
        check = await self.bot.db.fetchrow(
            "SELECT * FROM hardban WHERE guild_id = $1 AND banned = $2",
            ctx.guild.id,
            member.id,
        )
        if not check:
            return await ctx.send_warning(f"**{member}** is not hardbanned")
        await self.bot.db.execute(
            "DELETE FROM hardban WHERE guild_id = $1 AND banned = $2",
            ctx.guild.id,
            member.id,
        )
        await ctx.guild.unban(member, reason="unhardbanned by {}".format(ctx.author))
        await ctx.reply("👍")

    @commands.command(
        description="hardban an user from the server", help="donor", usage="[user]"
    )
    @Perms.get_perms("ban_members")
    @premium()
    async def hardban(
        self, ctx: commands.Context, *, member: Union[discord.Member, discord.User]
    ):
        if isinstance(member, discord.Member):
            if member.id == ctx.author.id:
                return await ctx.send_warning("You cannot hardban yourself")
            if member.id == self.bot.user.id:
                return await ctx.reply("im invicible")
            if await Mod.check_hieracy(ctx, member):
                che = await self.bot.db.fetchrow(
                    "SELECT * FROM hardban WHERE guild_id = $1 AND banned = $2",
                    ctx.guild.id,
                    member.id,
                )
                if che:
                    return await ctx.send_success(
                        f"**{member}** has been hardbanned by **{await self.bot.fetch_user(che['author'])}**"
                    )
                await ctx.guild.ban(
                    member, reason="hardbanned by {}".format(ctx.author)
                )
                await self.bot.db.execute(
                    "INSERT INTO hardban VALUES ($1,$2,$3)",
                    ctx.guild.id,
                    member.id,
                    ctx.author.id,
                )
                await ctx.reply("👍")

    @commands.command(
        description="find names with certain discriminators",
        help="donor",
        aliases=["pomelo"],
    )
    @premium()
    async def lookup(self, ctx: commands.Context, tag: str = "0001"):
        try:
            t = int(tag)
            type = "int"
        except:
            t = str(tag)
            type = "str"

        data = await get_tags(self.bot, type, tag)
        i = 0
        k = 1
        l = 0
        number = []
        messages = []
        num = 0
        auto = ""
        if data:
            for table in data:
                username = table[0]
                if checktag(username) is False:
                    continue
                discrim = table[1]
                num += 1
                auto += f"\n`{num}` {username}#{discrim}: <t:{int(table[2])}:R> "
                k += 1
                l += 1
                if l == 10:
                    messages.append(auto)
                    number.append(
                        discord.Embed(
                            color=self.bot.color,
                            title="Searches by tag"
                            if type == "int"
                            else "Searches by name",
                            description=auto,
                        ).set_author(
                            name=ctx.author.name, icon_url=ctx.author.display_avatar
                        )
                    )
                    i += 1
                    auto = ""
                    l = 0
            messages.append(auto)
            embed = discord.Embed(
                color=self.bot.color,
                title="Searches by tag" if type == "int" else "Searches by name",
                description=auto,
            ).set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
            number.append(embed)
            await ctx.paginator(number)
        else:
            return await ctx.send_warning(f"no **{tag}** tags available")

    @commands.command(
        description="purge an amount of messages sent by you",
        help="donor",
        usage="[amount]",
        aliases=["me"],
    )
    @premium()
    async def selfpurge(self, ctx: commands.Context, amount: int):
        mes = []
        async for message in ctx.channel.history():
            if len(mes) == amount + 1:
                break
            if message.author == ctx.author:
                mes.append(message)

        await ctx.channel.delete_messages(mes)

    @commands.command(
        description="returns the text in a image you provide",
        help="donor",
        usage="[imageurl]",
    )
    @premium()
    async def ocr(self, ctx: commands.Context, url):
        content = OCRImage(url)
        embed = discord.Embed(
            color=self.bot.color,
            title="OCR - Optical character recognition",
            description=f"```{content}```",
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        return await ctx.reply(embed=embed)

    @commands.command(
        description="force nicknames an user",
        help="donor",
        usage="[member] [nickname]\nif none is passed as nickname, the force nickname gets removed",
        aliases=["locknick"],
        brief="manage nicknames",
    )
    @Perms.get_perms("manage_nicknames")
    @premium()
    async def forcenick(
        self, ctx: commands.Context, member: NoStaff, *, nick: str = "none"
    ):
        if nick.lower() == "none":
            check = await self.bot.db.fetchrow(
                "SELECT * FROM forcenick WHERE user_id = {} AND guild_id = {}".format(
                    member.id, ctx.guild.id
                )
            )
            if check is None:
                return await ctx.send_warning(f"**No** forcenick found for {member}")
            await self.bot.db.execute(
                "DELETE FROM forcenick WHERE user_id = {} AND guild_id = {}".format(
                    member.id, ctx.guild.id
                )
            )
            await member.edit(nick=None)
            await ctx.reply("👍")
        else:
            check = await self.bot.db.fetchrow(
                "SELECT * FROM forcenick WHERE user_id = {} AND guild_id = {}".format(
                    member.id, ctx.guild.id
                )
            )
            if check is None:
                await self.bot.db.execute(
                    "INSERT INTO forcenick VALUES ($1,$2,$3)",
                    ctx.guild.id,
                    member.id,
                    nick,
                )
            else:
                await self.bot.db.execute(
                    "UPDATE forcenick SET nickname = '{}' WHERE user_id = {} AND guild_id = {}".format(
                        nick, member.id, ctx.guild.id
                    )
                )
            await member.edit(nick=nick)
            await ctx.reply("👍")


async def setup(bot):
    await bot.add_cog(donor(bot))
