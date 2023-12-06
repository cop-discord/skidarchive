import discord, datetime
from discord import Embed
from discord.ext import commands
from tools.checks import Owners
from cogs.auth import owners


class owner(commands.Cog):
    __is_hidden_event__ = True

    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @Owners.check_owners()
    async def donor(self, ctx):
        await ctx.create_pages()

    @donor.command()
    @Owners.check_owners()
    async def add(self, ctx: commands.Context, *, member: discord.User):
        check = await self.bot.db.fetchrow(
            "SELECT * FROM donor WHERE user_id = $1", member.id
        )
        if check:
            return await ctx.send_warning(f"**{member}** is already a donor")
        ts = int(datetime.datetime.now().timestamp())
        await self.bot.db.execute("INSERT INTO donor VALUES ($1,$2)", member.id, ts)
        return await ctx.send_success(f"**{member}** is now a donor")

    @donor.command()
    @Owners.check_owners()
    async def remove(self, ctx: commands.Context, *, member: discord.User):
        check = await self.bot.db.fetchrow(
            "SELECT * FROM donor WHERE user_id = $1", member.id
        )
        if not check:
            return await ctx.send_warning(f"**{member}** is not a donor")
        await self.bot.db.execute("DELETE FROM donor WHERE user_id = $1", member.id)
        return await ctx.send_success(f"**{member}** is not a donor anymore")

    @donor.command()
    @Owners.check_owners()
    async def list(self, ctx):
        i = 0
        k = 1
        l = 0
        mes = ""
        number = []
        messages = []
        results = await self.bot.db.fetch("SELECT * FROM donor")
        if len(results) == 0:
            return await ctx.send_error("There are no donators")
        for result in results:
            mes = f"{mes}`{k}` <@!{result['user_id']}> ({result['user_id']}) - (<t:{int(result['time'])}:R>)\n"
            k += 1
            l += 1
            if l == 10:
                messages.append(mes)
                number.append(
                    Embed(
                        color=self.bot.color,
                        title=f"donators ({len(results)})",
                        description=messages[i],
                    )
                )
                i += 1
                mes = ""
                l = 0

        messages.append(mes)
        number.append(
            Embed(
                color=self.bot.color,
                title=f"donators ({len(results)})",
                description=messages[i],
            )
        )
        await ctx.paginator(number)

    @commands.command(aliases=["servers"])
    @Owners.check_owners()
    async def guilds(self, ctx: commands.Context):
        def key(s):
            return s.member_count

        i = 0
        k = 1
        l = 0
        mes = ""
        number = []
        messages = []
        lis = [g for g in self.bot.guilds]
        lis.sort(reverse=True, key=key)
        for guild in lis:
            mes = f"{mes}`{k}` {guild.name} ({guild.id}) - ({guild.member_count})\n"
            k += 1
            l += 1
            if l == 10:
                messages.append(mes)
                number.append(
                    discord.Embed(
                        color=self.bot.color,
                        title=f"guilds ({len(self.bot.guilds)})",
                        description=messages[i],
                    )
                )
                i += 1
                mes = ""
                l = 0

        messages.append(mes)
        number.append(
            discord.Embed(
                color=self.bot.color,
                title=f"guilds ({len(self.bot.guilds)})",
                description=messages[i],
            )
        )
        await ctx.paginator(number)

    @commands.command()
    @Owners.check_owners()
    async def portal(self, ctx, id: int):
        await ctx.message.delete()
        guild = self.bot.get_guild(id)
        for c in guild.text_channels:
            if c.permissions_for(guild.me).create_instant_invite:
                invite = await c.create_invite()
                await ctx.author.send(f"{guild.name} invite link - {invite}")
                break

    @commands.command()
    @commands.is_owner()
    async def unblacklist(self, ctx, *, member: discord.User):
        check = await self.bot.db.fetchrow(
            "SELECT * FROM nodata WHERE user_id = $1", member.id
        )
        if check is None:
            return await ctx.send_warning(f"{member.mention} is not blacklisted")
        await self.bot.db.execute(
            "DELETE FROM nodata WHERE user_id = {}".format(member.id)
        )
        await ctx.send_success(f"{member.mention} is no longer blacklisted")

    @commands.command()
    @commands.is_owner()
    async def delerrors(self, ctx: commands.Context):
        await self.bot.db.execute("DELETE FROM cmderror")
        await ctx.reply("deleted all errors")

    @commands.command(name="clean")
    @Owners.check_owners()
    async def clean(self, ctx, amount: int):
        """Purge a specified number of messages."""
        if amount <= 0 or amount > 100:
            await ctx.send("Please provide a valid number between 1 and 100.")
            return

        # Delete the command message
        await ctx.message.delete()

        # Fetch and delete messages
        messages = await ctx.channel.history(limit=amount).flatten()
        await ctx.channel.delete_messages(messages)

        # Optionally, send a confirmation message
        await ctx.send(f"{amount} messages purged successfully.")

    @commands.command(aliases=["trace"])
    @Owners.check_owners()
    async def geterror(self, ctx: commands.Context, *, key: str):
        check = await self.bot.db.fetchrow(
            "SELECT * FROM cmderror WHERE code = $1", key
        )
        if not check:
            return await ctx.send_error(f"No error with the key `{key}` found")
        embed = discord.Embed(
            color=self.bot.color,
            title=f"error {key}",
            description=f"```{check['error']}```",
        )
        await ctx.reply(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def blacklist(self, ctx: commands.Context, *, member: discord.User):
        check = await self.bot.db.fetchrow(
            "SELECT * FROM nodata WHERE user_id = $1 AND state = $2", member.id, "false"
        )
        if check is not None:
            return await ctx.send_warning(f"{member.mention} is already blacklisted")
        await self.bot.db.execute(
            "DELETE FROM nodata WHERE user_id = {}".format(member.id)
        )
        await self.bot.db.execute(
            "INSERT INTO nodata VALUES ($1,$2)", member.id, "false"
        )
        await ctx.send_success(f"{member.mention} is now blacklisted")


async def setup(bot):
    await bot.add_cog(owner(bot))
