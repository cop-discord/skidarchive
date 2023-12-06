import discord, aiohttp
from discord.ext import commands


class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.webhook_url = "https://discord.com/api/webhooks/1172847688396574720/26JgpF03FrOt2-VP1V0AeEZK78c4ohpWesJm_fzO28BOUJK2IOH3mLyPzTBvy32ELZd5"
        self.session = aiohttp.ClientSession()

    @commands.Cog.listener()
    @commands.check(lambda ctx: setattr(ctx.command, "__hide_as_event__", True) or True)
    async def on_command_completion(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(
            description=f"`{ctx.command.name}` was successfully invoked by `{ctx.author.name}` in `{guild.name}` (`{guild.id}`)",
            color=0x2F3136,
        )
        embed.set_footer(text=f"{guild.member_count} members")
        print(
            f"{ctx.command.name} was successfully invoked by {ctx.author.name} in {guild.name} ({guild.id})"
        )
        async with self.session.post(
            self.webhook_url, json={"embeds": [embed.to_dict()]}
        ):
            pass


async def setup(bot):
    await bot.add_cog(events(bot))
