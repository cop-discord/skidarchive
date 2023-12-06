from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core import Slut


async def setup(bot: "Slut"):
    from .mod import Moderation

    await bot.add_cog(Moderation(bot))
