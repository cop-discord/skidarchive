import discord, datetime
from discord.ext import commands
from backend.classes import Emojis, Colors
from cogs.events import sendmsgg, noperms, blacklist
from discord.ext.commands import Context

poj_cache = {}

class pingonjoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        async with self.bot.db.cursor() as cursor: 
            await cursor.execute("CREATE TABLE IF NOT EXISTS pingonjoin (guild_id INTEGER, message TEXT, channel INTEGER);") 
        await self.bot.db.commit()

    @commands.Cog.listener()
    async def on_guild_join(self, member: discord.Member):
        if member.bot: return   
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT * FROM pingonjoin WHERE guild_id = {}".format(member.guild.id))
            results = await cursor.fetchall()
        members = [m for m in member.guild.members if (datetime.datetime.now() - m.joined_at.replace(tzinfo=None)).total_seconds() < 180]
        for result in results: 
         channel = member.guild.get_channel(int(result[0]))
         if channel: 
          if len(members) < 10: 
            try: await channel.send(member.mention, delete_after=6)
            except: continue    
          else:           
           if not poj_cache.get(str(channel.id)): poj_cache[str(channel.id)] = []
           poj_cache[str(channel.id)].append(f"{member.mention}")
           if len(poj_cache[str(channel.id)]) == 10: 
            try: 
             await channel.send(' '.join([m for m in poj_cache[str(channel.id)]]), delete_after=6) 
             poj_cache[str(channel.id)] = []
            except:
             poj_cache[str(channel.id)] = [] 
             continue 

    @commands.hybrid_group(aliases=["poj"])
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @blacklist()
    async def pingonjoin(self, ctx):
        if ctx.invoked_subcommand is None:
            e = discord.Embed(title="Command: pingonjoin", description="ping new members when they join your server",color=Colors.default, timestamp=ctx.message.created_at)
            e.add_field(name="category", value="config")
            e.add_field(name="Arguments", value="[channel]")
            e.add_field(name="permissions", value="manage_guild", inline=True)
            e.add_field(name="Command Usage",value="```Syntax: ,pingonjoin add #chat\nSyntax: ,pingonjoin clear\nSyntax: ,pingonjoin show```", inline=False)
            await sendmsgg(self, ctx, None, e, None, None, None, None)
            return
        
    @pingonjoin.command()
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @blacklist()
    async def add(self, ctx: commands.Context, *, channel: discord.TextChannel): 
        if not ctx.author.guild_permissions.manage_messages: return await noperms(self, ctx, "manage_messages")
        try:
            async with self.bot.db.cursor() as cursor:
             await cursor.execute("INSERT INTO pingonjoin VALUES (?,?)", (channel.id, ctx.guild.id))
            embed = discord.Embed(description = f"> {Emojis.check} {ctx.author.mention}: successfully added ping new members on {channel.mention}", color = Colors.default)
            await sendmsgg(self, ctx, None, embed, None, None, None, None)
            await self.bot.db.commit()
        except Exception as e:
            print(e)

    @pingonjoin.command()
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @blacklist()
    async def clear(self, ctx):
        if not ctx.author.guild_permissions.manage_messages: return await noperms(self, ctx, "manage_messages")
        try:
            async with self.bot.db.cursor() as cursor:
                await cursor.execute("DELETE FROM pingonjoin WHERE guild_id = {}".format(ctx.guild.id))
            embed = discord.Embed(description = f"> {Emojis.check} {ctx.author.mention}: successfully cleared ping on join", color = Colors.default)
            await sendmsgg(self, ctx, None, embed, None, None, None, None)
            await self.bot.db.commit()
        except Exception as e:
            print(e)

    @pingonjoin.command()
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @blacklist()
    async def show(self, ctx: commands.Context): 
        if not ctx.author.guild_permissions.manage_guild: return await noperms(self, ctx, "manage_guild")
        try:
            async with self.bot.db.cursor() as cursor:
                await cursor.execute("SELECT * FROM pingonjoin WHERE guild_id = {}".format(ctx.guild.id))
                data = await cursor.fetchall()
                num = 0
                auto = ""
                if data:
                    for table in data:
                        response = table[0]
                        channel = self.bot.get_channel(response)
                        num += 1
                        auto += f"\n`{num}` {channel.mention}"
                    embed = discord.Embed(description = auto, color = Colors.default)
                    embed.set_author(name = "list of ping on join channels", icon_url = ctx.message.author.display_avatar)
                    await sendmsgg(self, ctx, None, embed, None, None, None, None)
        except Exception as e:
            print(e)

async def setup(bot) -> None:
    await bot.add_cog(pingonjoin(bot))