async def setup(bot):
    from .dev import Developer
    
    await bot.add_cog(Developer(bot))