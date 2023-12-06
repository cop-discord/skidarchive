from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core import Slut


async def setup(bot: "Slut"):
    from .info import Information

    await bot.add_cog(Information(bot))
