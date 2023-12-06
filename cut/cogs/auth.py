import discord
from discord.ext import commands

owners = [628236220392275969, 1040008141301088276]


class Auth(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Auth(bot))
