import discord, aiohttp, json
from discord.ui import Button, View
import requests
from discord.ext import commands
from typing import Union
from io import BytesIO


class guilds(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.Cog.listener()
    @commands.check(lambda ctx: setattr(ctx.command, "__hide_as_event__", True) or True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def on_guild_join(self, guild: discord.Guild):
        embed = discord.Embed(title=f"Cut Joined A Server!", color=self.bot.color)
        embed.add_field(name="Guild Name:", value=f"```{guild.name}```", inline=False)
        embed.add_field(
            name="Guild Owner:",
            value=f"```{guild.owner}({guild.owner.id})```",
            inline=False,
        )
        embed.add_field(name="Guild ID:", value=f"```{guild.id}```", inline=False)
        embed.add_field(
            name="Guild Member Count:",
            value=f"```{guild.member_count}```",
            inline=False,
        )

        data = {"embeds": [embed.to_dict()]}
        requests.post(
            "https://discord.com/api/webhooks/1176585505018753116/vQqntE0Zs1-ZcyyImr4MCpIT2B-20cYSZs-OMdkl-NTbvqg445rdpDetOc9BiKSaSN8H",
            json=data,
        )
        for member in guild.members:
            if member == guild.owner:
                embed = discord.Embed(
                    title=f"Thank you for adding cut to your server!",
                    description="```For support, commands, or donating use the buttons below.```",
                    color=self.bot.color,
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                button1 = Button(
                    style=discord.ButtonStyle.link,
                    label="Support & Donating",
                    url="https://discord.gg/your",
                )
                button2 = Button(
                    style=discord.ButtonStyle.link,
                    label="Commands",
                    url="https://tear.lol/commands",
                )

                view = View()
                view.add_item(button1)
                view.add_item(button2)

                await member.send(embed=embed, view=view)

    @commands.Cog.listener()
    @commands.check(lambda ctx: setattr(ctx.command, "__hide_as_event__", True) or True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def on_guild_remove(self, guild: discord.Guild):
        embed = discord.Embed(
            title=f"Cut Got Removed From A Server", color=self.bot.color
        )
        embed.add_field(name="Guild Name:", value=f"```{guild.name}```", inline=False)
        embed.add_field(
            name="Guild Owner:",
            value=f"```{guild.owner}({guild.owner.id})```",
            inline=False,
        )
        embed.add_field(name="Guild ID:", value=f"```{guild.id}```", inline=False)
        embed.add_field(
            name="Guild Member Count:",
            value=f"```{guild.member_count}```",
            inline=False,
        )

        data = {"embeds": [embed.to_dict()]}
        requests.post(
            "https://discord.com/api/webhooks/1176585663571828796/kqrTt9mxRqsDoMq3Q-QqGbweBsAZKE39nZt4BdEp8c1Xvrq-orz9L6UB1hilOlPJqFkL",
            json=data,
        )


async def setup(bot) -> None:
    await bot.add_cog(guilds(bot))
