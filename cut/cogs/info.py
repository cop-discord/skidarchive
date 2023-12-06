import discord, asyncio, psutil
from discord import emoji
from discord.ui import Button, View
from discord.ext import commands
from datetime import datetime
from time import time
from discord.ui import View, Button, Select
import button_paginator as pg
from discord.ext.commands import Paginator as pg
from tools.utils import Paginator
from tools.emojis import emojis
from discord.ext.commands import MinimalHelpCommand
from tools.utils import EmbedBuilder
from typing import Optional, List
from tools.paginator import Paginator
from discord.ui import button, View


class Info(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    async def paginate(
        self,
        ctx: commands.Context,
        embeds: List[discord.Embed],
        max_entries: int,
        footer_override: bool = False,
    ):
        paginator = commands.Paginator()

        for embed in embeds:
            paginator.add_line(
                "\n".join([f"{field.name}\n{field.value}" for field in embed.fields])
            )

        for page in paginator.pages:
            await ctx.send(page)

    @commands.command(aliases=["h"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def help(self, ctx: commands.Context, command_name: str = None):
        if command_name is None:
            # Display general help with a link to view all commands
            return await ctx.help(
                f"Click [**here**](https://tear.lol/commands) to view **{len(set(self.bot.walk_commands()))}** commands"
            )
            # embeds = list()

            # embed = discord.Embed(description=f"```ini\n[ {len(set(self.bot.walk_commands()))} commands ]\n```\n")
            # for category in sorted(
            #     self.bot.cogs,
            #     key=lambda c: len(c),
            # ):
            #     if category.lower() in ("jishaku", "developer", "sentry"):
            #         continue
            #     embed.description += f"> [`{category}`](https://wock.cloud)\n"

            # embed.set_thumbnail(url=self.bot.user.display_avatar)
            # embeds.append(embed)

            # for name, category in sorted(self.bot.cogs.items(), key=lambda c: len(c[0])):
            #     if name.lower() in ("jishaku", "developer", "sentry"):
            #         continue
            #     embed = discord.Embed(description=f"```ini\n[ {category.qualified_name} ]\n[ {len(set(category.walk_commands()))} commands ]\n```\n")
            #     for command in category.walk_commands():
            #         if command.hidden:
            #             continue
            #         embed.description += f"> [`{command.qualified_name}`](https://wock.cloud)\n"

            #     embed.set_thumbnail(url=self.bot.user.display_avatar)
            #     embeds.append(embed)

            # await ctx.paginate(embeds)
        else:
            command: commands.Command = self.bot.get_command(command_name)
            if command is None:
                return await ctx.warn(f"Command `{command_name}` doesn't exist")

            embeds = []
            embed = discord.Embed(
                description=command.short_doc or "No description provided",
            )
            embed.description += (
                f"\n>>> ```bf\nSyntax: {ctx.prefix}{command.qualified_name} {command.usage or ''}\n"
                + (
                    f"Example: {ctx.prefix}{command.qualified_name} {command.help}"
                    if command.help
                    else ""
                )
                + "```"
            )
            embed.set_author(
                name=command.cog_name or "No category",
                icon_url=self.bot.user.display_avatar,
                url=f"https://docs.wock.cloud",
            )

            embed.add_field(
                name="Aliases",
                value=", ".join([f"`{alias}`" for alias in command.aliases]) or "`N/A`",
                inline=(False if len(command.aliases) >= 4 else True),
            )
            embed.add_field(
                name="Parameters",
                value=", ".join([f"`{param}`" for param in command.clean_params])
                or "`N/A`",
                inline=True,
            )
            embed.add_field(
                name="Permissions",
                value=", ".join(
                    [
                        f"`{check.__qualname__.split('.')[0]}`"
                        for check in command.checks
                    ]
                )
                or "`N/A`",
                inline=True,
            )
            if isinstance(command, commands.Group):
                embed.add_field(
                    name="Subcommands",
                    value="\n".join(
                        [
                            f"> `{subcommand.qualified_name}` - {subcommand.short_doc}"
                            for subcommand in sorted(
                                command.commands,
                                key=lambda c: c.qualified_name.lower(),
                            )
                            if not subcommand.hidden
                        ]
                    ),
                    inline=False,
                )
            embeds.append(embed)

            for embed in embeds:
                await ctx.send(embed=embed)

    @commands.command(description="check bot's latency", help="info")
    async def ping1231234123412341234141234(self, ctx: commands.Context):
        start = time()
        message = await ctx.reply(
            content=f"it took `{self.bot.ping}ms` to ping **the discord gods**"
        )
        finished = time() - start
        await message.edit(
            content=f"it took `{self.bot.ping}ms` to ping **the discord gods** (edit: `{finished}ms`)"
        )

    @commands.command(description="check bot's latency", help="info")
    async def ping(self, ctx: commands.Context):
        embed = discord.Embed(
            color=self.bot.color,
            description=f"> <:goodping:1177427085086703686> **Websocket**: `{self.bot.ping}ms`",
        )
        await ctx.reply(embed=embed)

    @commands.command(
        description="check for how long the bot has been running", help="info"
    )
    async def uptime(self, ctx: commands.Context):
        return await ctx.reply(
            embed=discord.Embed(
                color=self.bot.color,
                description=f"⏰ {ctx.author.mention}: **{self.bot.user.name}** has been running for **{self.bot.ext.uptime}**",
            )
        )

    @commands.command(
        description="check informations about the bot",
        help="info",
        aliases=["bi", "about", "info"],
    )
    async def botinfo(self, ctx: commands.Context):
        invite_link = discord.utils.oauth_url(
            self.bot.user.id, permissions=discord.Permissions.all()
        )

        # Bot statistics
        commands_count = len(set(self.bot.walk_commands()))
        latency = round(self.bot.latency * 1000, 1)
        lines_of_code = 19477  # Replace with the actual lines of code
        cpu_usage = 11.4  # Replace with the actual CPU usage

        # Server statistics
        guilds_count = len(self.bot.guilds)
        users_count = sum(guild.member_count for guild in self.bot.guilds)
        channels_count = sum(len(guild.channels) for guild in self.bot.guilds)
        roles_count = sum(len(guild.roles) for guild in self.bot.guilds)

        embed = discord.Embed(color=0x2B2D31)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_author(
            name=f"{self.bot.user.name}", icon_url=self.bot.user.avatar.url
        )

        embed.add_field(name=f"", value=f"**[`Invite`]({invite_link})**", inline=False)
        # Add fields for client information
        embed.add_field(
            name="**Client**",
            value=f">>> **Commands:** {commands_count}\n**Latency:** {latency} ms\n **Lines:** {lines_of_code}\n**CPU:** {cpu_usage}%",
            inline=True,
        )

        # Add fields for statistics
        embed.add_field(
            name="**Statistics**",
            value=f">>> **Guilds:** {guilds_count}\n**Users:** {users_count}\n**Channels:** {channels_count}\n**Roles:** {roles_count}",
            inline=True,
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Info(bot))
