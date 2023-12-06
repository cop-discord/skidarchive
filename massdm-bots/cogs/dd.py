import discord
from discord.ext import commands, tasks
import asyncio

class DmCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dm_queue = asyncio.Queue()
        self.sent_users = 0
        self.total_dms = 0

    async def owner(ctx):
     if ctx.message.author.id == 628236220392275969 or if ctx.message.author.id == 1040008141301088276:
      return ctx.message.author.id == 628236220392275969

    @commands.command()
    @commands.check(owner)
    async def dmall(self, ctx, *, message):
        self.embed_msg = await ctx.send(embed=discord.Embed(description="now starting mass dm", color=0x2f3136))
        for member in ctx.guild.members:
            if not member.bot:
                self.total_dms += 1
                await self.dm_queue.put((member, message.format(user=member.mention)))
        self.dm_task.start()

    @tasks.loop(seconds=1.0)
    async def dm_task(self):
        while not self.dm_queue.empty():
            if not self.bot.is_ready():
                await asyncio.sleep(10)
                continue

            try:
                member, message = await self.dm_queue.get()
                await member.send(message)
                print(f"[+] user id of {member.id} has been dm'd mf")
                self.sent_users += 1
                if self.sent_users % 100 == 0:
                    await asyncio.sleep(5)
                    await self.embed_msg.edit(embed=discord.Embed(description=f"dms sent: {self.sent_users} / {self.total_dms}", color=0x2f3136))
            except discord.Forbidden:
                print(f"[x] {member.id} has dms disabled, removing them from the queue")
            except Exception as e:
                print(f"[x] an error occurred: {e}")
            finally:
                self.dm_queue.task_done()
        if not self.dm_task.is_running():
            await self.embed_msg.edit(embed=discord.Embed(description="mass dm has been finished", color=0x2f3136))

async def setup(bot):
    await bot.add_cog(DmCog(bot))