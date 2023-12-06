async def setup(bot):
    from .events import events
    
    await bot.add_cog(events(bot))