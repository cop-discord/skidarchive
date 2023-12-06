from typing import Type

from discord import Message
from discord.ext.commands import Cog, Context, command

from core import Slut


class Developer(Cog, description=">.<"):
    def __init__(self, bot: Slut) -> None:
        self.bot: Slut = bot
    
    async def cog_check(self: "Developer", ctx: Context) -> bool:
         return await self.bot.is_owner(ctx.author)
    
    @command(name="reload", aliases=["rl"])
    async def reload(self: "Developer", ctx: Context, *, name: str) -> None:
        """
        Reload extension(s).
        """

        pass