from typing import Type
import os
from discord import Message, Embed
import discord
import aiohttp
from discord.ext.commands import Cog, Context, command
from config import owner_ids
from core import Slut


class Servers(Cog, description=">.<"):
    def __init__(self, bot: Slut) -> None:
        self.bot: Slut = bot


    @command(aliases=["guilds"])
    async def servers(self, ctx):
        if ctx.author.id not in owner_ids:  # assuming owner_ids is defined in config
            return

        guilds = self.bot.guilds
        total_guilds = len(guilds)
        page_size = 10
        current_page = 0

        def generate_embed(page):
            start_index = page * page_size
            end_index = min((page + 1) * page_size, total_guilds)
            description = "\n".join([f"`{i + 1}` {guild.name} ({guild.id}) - ({guild.member_count})" for i, guild in enumerate(guilds[start_index:end_index])])
            return discord.Embed(color=0x2B2D31, title=f"guilds ({total_guilds})", description=description)

        message = await ctx.send(embed=generate_embed(current_page))

        emojis = ["⬅️", "❌", "➡️"]  # Emojis for back, delete, and next
        for emoji in emojis:
            await message.add_reaction(emoji)

        def check(reaction, user):
            return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in emojis

        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
            except TimeoutError:
                break

            if str(reaction.emoji) == emojis[0]:  # Back
                current_page = max(0, current_page - 1)
            elif str(reaction.emoji) == emojis[1]:  # Delete
                await message.clear_reactions()
                break
            elif str(reaction.emoji) == emojis[2]:  # Next
                current_page = min(total_guilds // page_size, current_page + 1)

            await message.edit(embed=generate_embed(current_page))
            await reaction.remove(ctx.author)