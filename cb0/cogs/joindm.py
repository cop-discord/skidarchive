import discord, aiosqlite, os, asyncio, time, sys, random, aiohttp, datetime, discord.ui
from discord.ext import commands
from backend.classes import Emojis, Colors
from backend.embedparser import to_object
from cogs.events import blacklist
from discord.ext.commands import Context
from discord.ui import Button, View

class joindm(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        async with self.bot.db.cursor() as cursor: 
            await cursor.execute("CREATE TABLE IF NOT EXISTS joindm (guild INTEGER, message TEXT);") 
        await self.bot.db.commit()

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT * FROM joindm WHERE guild = {}".format(member.guild.id))
            check = await cursor.fetchone()
            if check is not None:
                msg = check[1]
                user = member
                guild = member.guild
                z = msg.replace('{user}', f'{user}').replace('{user.name}', f'{user.name}').replace('{user.mention}', f'{user.mention}').replace('{user.avatar}', user.avatar.url).replace('{user.joined_at}', f'<t:{int(user.created_at.timestamp())}:R>').replace('{user.discriminator}', f'{user.discriminator}').replace('{guild.name}', f'{guild.name}').replace('{guild.count}', f'{guild.member_count}').replace('{guild.icon}', guild.icon.url).replace('{guild.id}', f'{guild.id}')
                x = await to_object(z)
                channel = user.dm_channel or await user.create_dm()
                button = discord.ui.Button(label=f"sent from {guild.name}", style=discord.ButtonStyle.red, disabled=True)
                view = discord.ui.View()
                view.add_item(button)
                await channel.send(**x)
                await channel.send(view=view)
  
    @commands.hybrid_group(invoke_without_command=True, description="joindm")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @blacklist()
    async def joindm(self, ctx):
        embed = discord.Embed(color=0x2B2D31, title="joindm", description="greet your users into your guild with a direct message")
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        embed.add_field(name="category", value="config")
        embed.add_field(name="commands", value=">>> ,joindm message\n,joindm config\n,joindm variables\n,joindm delete\n,joindm test", inline=False)
        embed.add_field(name="usage", value="```,joindm message hello {user}!```", inline=False)
        embed.set_footer(text=f"aliases: none")
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text="powered by use")
        await ctx.reply(embed=embed, mention_author=False)

  
    @joindm.command(help="configure a joindm message for your server", description="joindm")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @blacklist()
    async def message(self, ctx, *, code=None):
        if not ctx.author.guild_permissions.manage_guild:
            embed = discord.Embed(color=Colors.default, description=f"{Emojis.warn} you are missing permissions **manage_guild**")
            await ctx.reply(embed=embed, mention_author=False)
            return
        embed=discord.Embed(description=f"set joindm message to `{code}`", color=Colors.default)
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT * FROM joindm WHERE guild = {}".format(ctx.guild.id))
            check = await cursor.fetchone()
            if check is None:
                async with self.bot.db.cursor() as cursor:
                    await cursor.execute("INSERT INTO joindm (guild, message) VALUES (?, ?)", (ctx.guild.id, code))
                await self.bot.db.commit()
                await ctx.reply(embed=embed, mention_author=False)
            elif check is not None:
                async with self.bot.db.cursor() as cursor:
                    await cursor.execute("UPDATE joindm SET message = ? WHERE guild = ?", (code, ctx.guild.id))
                await self.bot.db.commit()
                await ctx.reply(embed=embed, mention_author=False)


    @joindm.command(help="check your joindm settings for your server", description="joindm")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @blacklist()
    async def config(self, ctx):   
      if not ctx.author.guild_permissions.manage_guild:
        embed = discord.Embed(color=Colors.default, description=f"{Emojis.warning} you are missing permissions **manage_guild**") 
        await ctx.reply(embed=embed, mention_author=False)
        return
        
      async with self.bot.db.cursor() as cursor:
        await cursor.execute("SELECT * FROM joindm WHERE guild = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        msg = check[1] or "joindm message not set"
        embed=discord.Embed(title="joindm message config", color=Colors.default)
        embed.add_field(name="message", value=f"`{msg}`")
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_footer(text="powered by use")
        await ctx.reply(embed=embed, mention_author=False)

    @joindm.command(help="view the joindm variables", description="joindm")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @blacklist()
    async def variables(self, ctx):   
      embed=discord.Embed(description="here is a list of variables used to greet your members", color=Colors.default)
      embed.add_field(name="member", value=">>> {user}\n{user.name}\n{user.mention}\n{user.avatar}\n{user.discriminator}\n{user.joined_at}")
      embed.add_field(name="guild", value=">>>{guild.name}\n{guild.count}\n{guild.icon}\n{guild.id}")
      embed.set_thumbnail(url=ctx.guild.icon.url)
      embed.set_footer(text="powered by use")
      await ctx.reply(embed=embed, mention_author=False)

    @joindm.command(help="delete your joindm config", description="joindm")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @blacklist()
    async def delete(self, ctx):   
      if not ctx.author.guild_permissions.manage_guild:
        embed = discord.Embed(color=Colors.default, description=f"{Emojis.warning} you are missing permissions **manage_guild**") 
        await ctx.reply(embed=embed, mention_author=False)
        return
      async with self.bot.db.cursor() as cursor:
        await cursor.execute("DELETE FROM joindm WHERE guild = {}".format(ctx.guild.id))
      await self.bot.db.commit()
      embed=discord.Embed(description=f"{Emojis.check} deleted the joindm config for *{ctx.guild.name}*", color=Colors.default)
      await ctx.reply(embed=embed, mention_author=False)

    @joindm.command(help="tests your joindm message", description="joindm")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @blacklist()
    async def test(self, ctx):   
        if not ctx.author.guild_permissions.manage_guild:
            embed = discord.Embed(color=Colors.default, description=f"{Emojis.warning} you are missing permissions **manage_guild**") 
            await ctx.reply(embed=embed, mention_author=False)
            return
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT * FROM joindm WHERE guild = {}".format(ctx.guild.id))
            check = await cursor.fetchone()
            if check is not None:
                msg = check[1]
                user = ctx.author
                guild = ctx.guild
                z = msg.replace('{user}', f'{user}').replace('{user.name}', f'{user.name}').replace('{user.mention}', f'{user.mention}').replace('{user.avatar}', user.avatar.url).replace('{user.joined_at}', f'<t:{int(user.created_at.timestamp())}:R>').replace('{user.discriminator}', f'{user.discriminator}').replace('{guild.name}', f'{guild.name}').replace('{guild.count}', f'{guild.member_count}').replace('{guild.icon}', guild.icon.url).replace('{guild.id}', f'{guild.id}')
                x = await to_object(z)
                channel = user.dm_channel or await user.create_dm()
                button = discord.ui.Button(label=f"sent from {guild.name}", style=discord.ButtonStyle.red, disabled=True)
                view = discord.ui.View()
                view.add_item(button)
                await channel.send(**x)
                await channel.send(view=view)
                embed=discord.Embed(description=f"{Emojis.check} joindm message has been sent in your direct messages", color=Colors.default)
                await ctx.reply(embed=embed, mention_author=False)
            elif check is None:
                embed=discord.Embed(description=f"{Emojis.warning} joindm message isnt configured for *{ctx.guild.name}*", color=Colors.default)
                await ctx.reply(embed=embed, mention_author=False)

async def setup(bot):
    await bot.add_cog(joindm(bot))