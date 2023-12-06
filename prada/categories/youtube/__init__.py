async def setup(bot):
    from .youtube import youtube
    
    await bot.add_cog(youtube(bot))