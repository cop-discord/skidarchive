async def setup(bot: "Slut"):
    from .utility import Utility

    await bot.add_cog(Utility(bot))
