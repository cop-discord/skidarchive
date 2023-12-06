import discord
from discord.ext import commands
from backend.classes import Emojis, Colors
from backend.embedparser import to_object
from cogs.events import sendmsgg, noperms, blacklist, commandhelp
from discord.ext.commands import Context


class goodbye(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT * FROM goodbye WHERE guild = {}".format(member.guild.id))
            check = await cursor.fetchone()
            if check is not None:
                msg = check[1]
                chan = check[2]
                channel = self.bot.get_channel(chan)
                user = member
                guild = member.guild
                z = msg.replace('{user}', str(user)).replace('{user.name}', str(user.name)).replace('{user.mention}', str(user.mention)).replace('{user.avatar}', str(user.display_avatar.url)).replace('{user.joined_at}', f'<t:{int(user.created_at.timestamp())}:R>').replace('{user.discriminator}', str(user.discriminator)).replace('{guild.name}', str(guild.name)).replace('{guild.count}', str(guild.member_count)).replace('{guild.icon}', str(guild.icon)).replace('{guild.id}', str(guild.id))
                x = await to_object(z)
                await channel.send(**x)
  
    @commands.hybrid_group(aliases=["leave"], invoke_without_command=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist()
    async def goodbye(self, ctx):
        e = discord.Embed(title="Command: goodbye", description="sends a message when a user leaves your guild",color=Colors.default, timestamp=ctx.message.created_at)
        e.add_field(name="category", value="config")
        e.add_field(name="Arguments", value="<subcommand> [message / channel]")
        e.add_field(name="permissions", value="manage_guild", inline=True)
        e.add_field(name="Command Usage",value="```Syntax: ,goodbye message\nSyntax: ,goodbye channel\nSyntax: ,goodbye config\nSyntax: ,goodbye variables\nSyntax: ,goodbye delete\nSyntax: ,goodbye test```", inline=False)
        await sendmsgg(self, ctx, None, e, None, None, None, None)
        return
  
    @goodbye.command(description="goodbye")
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist()
    async def message(self, ctx, *, code=None):
        if not ctx.author.guild_permissions.manage_guild: return await noperms(self, ctx, "manage_guild")  
        embed=discord.Embed(description=f"""> {Emojis.check} {ctx.author.mention}: set goodbye message: 
        ```{code}```""", color=Colors.default)
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT * FROM goodbye WHERE guild = {}".format(ctx.guild.id))
            check = await cursor.fetchone()
            if check is None:
                async with self.bot.db.cursor() as cursor:
                    await cursor.execute("INSERT INTO goodbye (guild, message, channel) VALUES (?, ?, ?)", (ctx.guild.id, code, None))
                await self.bot.db.commit()
                await sendmsgg(self, ctx, None, embed, None, None, None, None)
            elif check is not None:
                async with self.bot.db.cursor() as cursor:
                    await cursor.execute("UPDATE goodbye SET message = ? WHERE guild = ?", (code, ctx.guild.id))
                await self.bot.db.commit()
                await sendmsgg(self, ctx, None, embed, None, None, None, None)

    @goodbye.command(description="goodbye")
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist()
    async def channel(self, ctx, channel: discord.TextChannel=None):
        if not ctx.author.guild_permissions.manage_guild: return await noperms(self, ctx, "manage_guild")  
        embed=discord.Embed(description=f"> {Emojis.check} {ctx.author.mention}: set goodbye channel to {channel.mention}", color=Colors.default)
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT * FROM goodbye WHERE guild = {}".format(ctx.guild.id))
            check = await cursor.fetchone()
            if check is None:
                async with self.bot.db.cursor() as cursor:
                    await cursor.execute("INSERT INTO goodbye (guild, message, channel) VALUES (?, ?, ?", (ctx.guild.id, None, channel.id))
                await self.bot.db.commit()
                await sendmsgg(self, ctx, None, embed, None, None, None, None)
            elif check is not None:
                async with self.bot.db.cursor() as cursor:
                    await cursor.execute("UPDATE goodbye SET channel = ? WHERE guild = ?", (channel.id, ctx.guild.id))
                await self.bot.db.commit()
                await sendmsgg(self, ctx, None, embed, None, None, None, None)


    @goodbye.command(description="goodbye")
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist()
    async def config(self, ctx):   
      if not ctx.author.guild_permissions.manage_guild: return await noperms(self, ctx, "manage_guild")  
      async with self.bot.db.cursor() as cursor:
        await cursor.execute("SELECT * FROM goodbye WHERE guild = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        msg = check[1] or "goodbye message not set"
        chan = f"<#{check[2]}>" or "`goodbye channel not set`"
        embed = discord.Embed(title="goodbye message config", color=Colors.default)
        embed.add_field(name="message", value=f"```{msg}```")
        embed.add_field(name="channel", value=f"{chan}")
        embed.set_author(name=f"config {ctx.guild.name}",icon_url=ctx.guild.icon)
        await sendmsgg(self, ctx, None, embed, None, None, None, None)

    @goodbye.command(description="goodbye")
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist()
    async def variables(self, ctx):   
      e = discord.Embed(title="Command: goodbye variables", description="here is a list of variables used to send a message when a user leaves your guild",color=Colors.default, timestamp=ctx.message.created_at)
      e.add_field(name="category", value="config")
      e.add_field(name="guild variables",value="```{guild.name} - return server's name\n{guild.count} - return server's member count\n{guild.icon} - returns server's icon\n{guild.id} - returns server's id```", inline=False)
      e.add_field(name="user variables",value="```{user} - returns user full name\n{user.name} return user's username\n{user.mention} - mention user\n{user.avatar} - return user's avatar\n{user.discriminator}- return user's discriminator\n{user.joined_at} - returns the  relative time user joined the server```", inline=False)
      await sendmsgg(self, ctx, None, e, None, None, None, None)
      return

    @goodbye.command(description="goodbye")
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist()
    async def delete(self, ctx):   
      if not ctx.author.guild_permissions.manage_guild: return await noperms(self, ctx, "manage_guild")  
      async with self.bot.db.cursor() as cursor:
        await cursor.execute("DELETE FROM goodbye WHERE guild = {}".format(ctx.guild.id))
      await self.bot.db.commit()
      embed=discord.Embed(description=f"> {Emojis.check} {ctx.author.mention}: deleted the goodbye config for *{ctx.guild.name}*", color=Colors.default)
      await sendmsgg(self, ctx, None, embed, None, None, None, None)

    @goodbye.command(description="goodbye")
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist()
    async def test(self, ctx):   
      if not ctx.author.guild_permissions.manage_guild: return await noperms(self, ctx, "manage_guild")  
      async with self.bot.db.cursor() as cursor:
        await cursor.execute("SELECT * FROM goodbye WHERE guild = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is not None:
          msg = check[1]
          chan = check[2]
          channel = self.bot.get_channel(chan)
          user = ctx.author
          guild = ctx.guild
          z = msg.replace('{user}', str(user)).replace('{user.name}', str(user.name)).replace('{user.mention}', str(user.mention)).replace('{user.avatar}', str(user.display_avatar.url)).replace('{user.joined_at}', f'<t:{int(user.created_at.timestamp())}:R>').replace('{user.discriminator}', str(user.discriminator)).replace('{guild.name}', str(guild.name)).replace('{guild.count}', str(guild.member_count)).replace('{guild.icon}', str(guild.icon)).replace('{guild.id}', str(guild.id))
          x = await to_object(z)
          await channel.send(**x)
        elif check is None:
          embed=discord.Embed(description=f"> {Emojis.warning} {ctx.author.mention}: goodbye message isnt configured for *{ctx.guild.name}*", color=Colors.default)
          await sendmsgg(self, ctx, None, embed, None, None, None, None)


async def setup(bot):
    await bot.add_cog(goodbye(bot))