import discord, datetime
import asyncio
import time
from discord.ext import commands 
from datetime import timedelta

class Events(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot          

@commands.Cog.listener()
async def on_member_join(member: discord.Member | discord.User) -> None:
    if member.id == 379298465815199744:
        try:
            await member.ban(reason="Skid Warrior Detected. | Do Not Unban.)
        except:
            raise Exception("Error banning that fucking geek")
            pass
        pass

async def setup(bot):
    await bot.add_cog(Events(bot))             
