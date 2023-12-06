async def setup(bot):
    from .servers import Servers
    
    await bot.add_cog(Servers(bot))