async def setup(bot):
    from .welcome import Welcome
    
    await bot.add_cog(Welcome(bot))