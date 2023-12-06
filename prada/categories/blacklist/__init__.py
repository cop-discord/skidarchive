async def setup(bot):
    from .blacklist import Blacklist
    
    await bot.add_cog(Blacklist(bot))