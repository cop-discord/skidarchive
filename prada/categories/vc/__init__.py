async def setup(bot):
    from .vc import vc
    
    await bot.add_cog(vc(bot))