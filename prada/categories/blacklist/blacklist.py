import discord
from discord.ext import commands
import json

class BlacklistCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.owner_id = {628236220392275969}  # Replace with your owner's ID
        self.blacklist = self.load_blacklist()

    def load_blacklist(self):
        try:
            with open('blacklist.json', 'r') as f:
                data = json.load(f)
                return {
                    'users': set(data['blacklist']['users']),
                    'guilds': set(data['blacklist']['guilds'])
                }
        except (FileNotFoundError, json.JSONDecodeError):
            return {'users': set(), 'guilds': set()}

    def save_blacklist(self):
        with open('blacklist.json', 'w') as f:
            json.dump({'blacklist': {'users': list(self.blacklist['users']), 'guilds': list(self.blacklist['guilds'])}}, f)

    def is_owner(self, user_id):
        return user_id in self.owner_id

    def is_blacklisted(self, user_id, guild_id):
        return user_id in self.blacklist['users'] or guild_id in self.blacklist['guilds']

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if self.is_blacklisted(None, guild.id):
            await guild.leave()
            print(f"Left unauthorized guild: {guild.name} ({guild.id})")

    @commands.command()
    async def authorize(self, ctx, guild_id: int):
        """Authorize a guild to use the bot."""
        if not self.is_owner(ctx.author.id):
            return

        if guild_id not in self.blacklist['guilds']:
            return await ctx.send("Guild is not blacklisted.")

        self.blacklist['guilds'].remove(guild_id)
        self.save_blacklist()
        await ctx.send(f"Guild {guild_id} has been authorized.")

    @commands.command()
    async def blacklist(self, ctx, target: discord.User):
        """Blacklist a user or guild from using the bot."""
        if not self.is_owner(ctx.author.id):
            return

        if isinstance(target, discord.User):
            if target.id in self.blacklist['users']:
                return await ctx.send("User is already blacklisted.")
            self.blacklist['users'].add(target.id)
            self.save_blacklist()
            await ctx.send(f"User {target.id} has been blacklisted.")
        elif isinstance(target, discord.Guild):
            if target.id in self.blacklist['guilds']:
                return await ctx.send("Guild is already blacklisted.")
            self.blacklist['guilds'].add(target.id)
            self.save_blacklist()
            await ctx.send(f"Guild {target.id} has been blacklisted.")