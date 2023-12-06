import discord, datetime
from discord.ext import commands
from tools.checks import Perms
from tools.utils import EmbedBuilder

messages = {}
max_messages = 15
cooldown = 3 * 60


class Joindm(commands.Cog):
    __is_hidden_event__ = True

    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.Cog.listener()
    @commands.check(lambda ctx: setattr(ctx.command, "__hide_as_event__", True) or True)
    async def on_member_join(self, member: discord.Member):
        check = await self.bot.db.fetchrow(
            "SELECT * FROM joindm WHERE guild_id = $1", member.guild.id
        )
        if check:
            if not messages.get(str(member.guild.id)):
                messages[str(member.guild.id)] = []
            messages[str(member.guild.id)].append(datetime.datetime.now())
            expired = [
                msg
                for msg in messages[str(member.guild.id)]
                if (datetime.datetime.now() - msg).total_seconds() > cooldown
            ]
            for msg_time in expired:
                messages[str(member.guild.id)].remove(msg_time)
            if len(messages[str(member.guild.id)]) > max_messages:
                return
            mes = check["message"]
            view = discord.ui.View()
            view.add_item(
                discord.ui.Button(label=f"Sent from {member.guild.name}", disabled=True)
            )
            x = await EmbedBuilder.to_object(
                EmbedBuilder.embed_replacement(member, mes)
            )
            if x[0] and x[1]:
                x = await EmbedBuilder.to_object(
                    EmbedBuilder.embed_replacement(member, mes)
                )
                try:
                    await member.send(content=x[0], embed=x[1], view=view)
                except:
                    pass
            else:
                try:
                    await member.send(
                        content=EmbedBuilder.embed_replacement(
                            member, check["message"]
                        ),
                        view=view,
                    )
                except:
                    pass

    @commands.group(invoke_without_command=True)
    async def joindm(self, ctx: commands.Context):
        embeds = []
        embed = discord.Embed(
            color=self.bot.color,
            description=self.joindm.short_doc or "No description provided",
        )
        embed.description += (
            f"\n>>> ```bf\nSyntax: {ctx.prefix}{self.joindm.qualified_name} {self.joindm.usage or ''}\n"
            + (
                f"Example: {ctx.prefix}{self.joindm.qualified_name} {self.joindm.help}"
                if self.joindm.help
                else ""
            )
            + "```"
        )
        embed.set_author(
            name=self.joindm.cog_name or "No category",
            icon_url=self.bot.user.display_avatar,
            url=f"https://tear.lol/",
        )
        if isinstance(self.joindm, commands.Group):
            embed.add_field(
                name="Subcommands",
                value="\n".join(
                    [
                        f"> `{subcommand.qualified_name}` - {subcommand.short_doc}"
                        for subcommand in sorted(
                            self.joindm.commands,
                            key=lambda c: c.qualified_name.lower(),
                        )
                        if not subcommand.hidden
                    ]
                ),
                inline=False,
            )
        embeds.append(embed)

        for embed in embeds:
            await ctx.send(embed=embed)

    @joindm.command(
        name="message",
        description="set a joindm message",
        help="config",
        usage="[message]",
    )
    @Perms.get_perms("manage_guild")
    async def joindm_message(self, ctx: commands.Context, *, message: str):
        check = await self.bot.db.fetchrow(
            "SELECT * FROM joindm WHERE guild_id = $1", ctx.guild.id
        )
        if check:
            await self.bot.db.execute(
                "UPDATE joindm SET message = $1 WHERE guild_id = $2",
                message,
                ctx.guild.id,
            )
        else:
            await self.bot.db.execute(
                "INSERT INTO joindm VALUES ($1,$2)", ctx.guild.id, message
            )
        await ctx.send_success(f"Joindm message set to\n```{message}```")

    @joindm.command(
        name="remove", description="remove the joindm message", help="config"
    )
    @Perms.get_perms("manage_guild")
    async def joindm_remove(self, ctx: commands.Context):
        check = await self.bot.db.fetchrow(
            "SELECT * FROM joindm WHERE guild_id = $1", ctx.guild.id
        )
        if not check:
            return await ctx.send_warning("Joindm is **not** enabled")
        await self.bot.db.execute(
            "DELETE FROM joindm WHERE guild_id = $1", ctx.guild.id
        )
        return await ctx.send_success("Joindm has been **deleted**")

    @joindm.command(name="test", description="test the joindm message", help="config")
    @Perms.get_perms("manage_guild")
    async def joindm_test(self, ctx):
        check = await self.bot.db.fetchrow(
            "SELECT * FROM joindm WHERE guild_id = $1", ctx.guild.id
        )
        if not check:
            return await ctx.send_warning("Joindm is **not** enabled")
        member = ctx.author
        mes = check["message"]
        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(label=f"Sent from {member.guild.name}", disabled=True)
        )
        x = await EmbedBuilder.to_object(
            EmbedBuilder.embed_replacement(ctx.author, mes)
        )
        if x[0] and x[1]:
            try:
                await member.send(content=x[0], embed=x[1], view=view)
            except:
                pass
        else:
            try:
                await member.send(
                    EmbedBuilder.embed_replacement(ctx.author, mes), view=view
                )
            except:
                pass
        return await ctx.send_success("**Check your dm's** if you received one")


async def setup(bot):
    await bot.add_cog(Joindm(bot))
