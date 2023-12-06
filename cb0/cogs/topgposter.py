import discord
from discord.ext import commands, tasks
import topgg
from dotenv import load_dotenv

load_dotenv()

class TopgShitBullshit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dbl_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEwOTQ5NDI0Mzc4MjAwNzYwODMiLCJib3QiOnRydWUsImlhdCI6MTY4OTM1MzI5NX0.MZQhdNQfx4Lj3KgjGcL1C1_0wFp-IIDyesLGrro7gpY"  # Set this to your bot's Top.gg token
        self.topggpy = topgg.DBLClient(self.bot, self.dbl_token, autopost=True, post_shard_count=True)
        self.update_stats.start()

    @tasks.loop(minutes=25)
    async def update_stats(self):
        topgchannel = self.bot.get_channel(1127519397385351299)
        """This function runs every 30 minutes to automatically update your server count."""
        try:
            await self.topggpy.post_guild_count()
            msg = await topgchannel.send(f"**Top.gg API:** Posted server count ({self.topggpy.guild_count}), shard count ({self.bot.shard_count})")
            await msg.add_reaction("<:check:1126571720816468129>")
        except Exception as e:
            msg = await topgchannel.send(f"**Top.gg API:** Failed to post server count\n{e.__class__.__name__}: {e}")
            await msg.add_reaction("<:warning:1126572583442206820>")

    @update_stats.before_loop
    async def before_update_stats(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(TopgShitBullshit(bot))