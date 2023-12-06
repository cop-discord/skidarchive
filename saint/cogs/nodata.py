import discord
from discord.ext import commands

class nodata(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS nodata (user INTEGER)")
            await cursor.execute("CREATE TABLE IF NOT EXISTS pingonjoin (channel_id BIGINT, guild_id BIGINT)")
            await cursor.execute("CREATE TABLE IF NOT EXISTS boostconfig (channel INTEGER, message TEXT, guild INTEGER)")
            await cursor.execute("CREATE TABLE IF NOT EXISTS reaction_roles (role_id INTEGER, message_id INTEGER, emoji TEXT, PRIMARY KEY (role_id, message_id, emoji))")
            await cursor.execute("CREATE TABLE IF NOT EXISTS autoreact (trigger TEXT, emoji TEXT, guild INTEGER)")
            await cursor.execute("CREATE TABLE IF NOT EXISTS seen (guild_id INTEGER, user_id INTEGER, time INTEGER);")
            await cursor.execute("CREATE TABLE IF NOT EXISTS goodbye (guild INTEGER, message TEXT, channel INTEGER);")
            await cursor.execute("CREATE TABLE IF NOT EXISTS welcome (guild_id INTEGER, message TEXT, channel INTEGER);") 
            await cursor.execute("CREATE TABLE IF NOT EXISTS stfu (user_id INTEGER, guild_id INTEGER);")
            await cursor.execute("CREATE TABLE IF NOT EXISTS skull (user_id INTEGER, guild_id INTEGER);")
            await cursor.execute("CREATE TABLE IF NOT EXISTS restore (guild_id INTEGER, user_id INTEGER, roles TEXT);")
            await cursor.execute("CREATE TABLE IF NOT EXISTS selfprefix (pref TEXT, user_id INTEGER);")
            await cursor.execute("CREATE TABLE IF NOT EXISTS prefixes (guild_id INTEGER, prefix TEXT);")
            await cursor.execute("CREATE TABLE IF NOT EXISTS snipe (guild_id INTEGER, channel_id INTEGER, author TEXT, content TEXT, attachment TEXT, avatar TEXT);")
        await self.bot.db.commit()

async def setup(bot):
    await bot.add_cog(nodata(bot))

    