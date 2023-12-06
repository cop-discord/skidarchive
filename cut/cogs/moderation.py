import discord, humanfriendly, json, datetime, asyncio
from discord.ext import commands
from discord import Message, Member, User, Embed, PermissionOverwrite
from discord.ext.commands import cooldown, BucketType, CooldownMapping
from tools.checks import Perms, Mod
from tools.utils import NoStaff, GoodRole, Invoke
from typing import Union
from discord import Embed
from tools.utils import EmbedBuilder, GoodRole, NoStaff


class ClearMod(discord.ui.View):
    def __init__(self, ctx: commands.Context):
        super().__init__()
        self.ctx = ctx
        self.status = False

    @discord.ui.button(emoji="<:check:1124998964358426675>")
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.client.ext.send_warning(
                interaction, "You are not the author of this embed"
            )
        check = await interaction.client.db.fetchrow(
            "SELECT * FROM mod WHERE guild_id = $1", interaction.guild.id
        )
        channelid = check["channel_id"]
        roleid = check["role_id"]
        logsid = check["jail_id"]
        channel = interaction.guild.get_channel(channelid)
        role = interaction.guild.get_role(roleid)
        logs = interaction.guild.get_channel(logsid)
        try:
            await channel.delete()
        except:
            pass
        try:
            await role.delete()
        except:
            pass
        try:
            await logs.delete()
        except:
            pass
        await interaction.client.db.execute(
            "DELETE FROM mod WHERE guild_id = $1", interaction.guild.id
        )
        self.status = True
        return await interaction.response.edit_message(
            view=None,
            embed=discord.Embed(
                color=interaction.client.color,
                description=f"{interaction.client.yes} {interaction.user.mention}: Disabled",
            ),
        )

    @discord.ui.button(emoji="<:stop:1124999008142774303>")
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.client.ext.send_warning(
                interaction, "You are not the author of this embed"
            )
        await interaction.response.edit_message(
            embed=discord.Embed(
                color=interaction.client.color, description="aborting action.."
            ),
            view=None,
        )
        self.status = True

    async def on_timeout(self) -> None:
        if self.status == False:
            for item in self.children:
                item.disabled = True

            await self.message.edit(view=self)


class ModConfig:
    async def sendlogs(
        bot: commands.AutoShardedBot,
        action: str,
        author: discord.Member,
        victim: Union[discord.Member, discord.User],
        reason: str,
    ):
        check = await bot.db.fetchrow(
            "SELECT channel_id FROM mod WHERE guild_id = $1", author.guild.id
        )
        if check:
            res = await bot.db.fetchrow(
                "SELECT count FROM cases WHERE guild_id = $1", author.guild.id
            )
            case = int(res["count"]) + 1
            await bot.db.execute(
                "UPDATE cases SET count = $1 WHERE guild_id = $2", case, author.guild.id
            )
            embed = discord.Embed(color=bot.color, title=f"case #{case} | {action}")
            embed.add_field(
                name="User:", value=f"```{victim}({victim.id})```", inline=False
            )
            embed.add_field(
                name="Moderator:", value=f"```{author}({author.id})```", inline=False
            )
            embed.add_field(name="Reason:", value=f"```{reason}```", inline=False)
            embed.set_thumbnail(url=victim.avatar)
            try:
                await author.guild.get_channel(int(check["channel_id"])).send(
                    embed=embed
                )
            except:
                pass

    async def send_dm(
        ctx: commands.Context, member: discord.Member, action: str, reason: str
    ):
        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(label=f"sent from {ctx.guild.name}", disabled=True)
        )
        embed = discord.Embed(
            color=ctx.bot.color,
            description=f"You have been **{action}** in {ctx.guild.name}\n{f'reason: {reason}' if reason != 'No reason provided' else ''}",
        )
        try:
            await member.send(embed=embed)
        except:
            pass


class Mod(commands.Cog):
    __is_hidden_event__ = True

    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        check = await self.bot.db.fetchrow(
            "SELECT * FROM mod WHERE guild_id = {}".format(channel.guild.id)
        )
        if check:
            await channel.set_permissions(
                channel.guild.get_role(int(check["role_id"])),
                view_channel=False,
                reason="overwriting permissions for jail role",
            )

    @commands.command(
        description="disable the moderation features in your server", help="moderation"
    )
    @Perms.get_perms("administrator")
    async def unsetme(self, ctx: commands.Context):
        check = await self.bot.db.fetchrow(
            "SELECT * FROM mod WHERE guild_id = $1", ctx.guild.id
        )
        if not check:
            return await ctx.send_warning(
                "Moderation is **not** enabled in this server"
            )
        view = ClearMod(ctx)
        view.message = await ctx.reply(
            view=view,
            embed=discord.Embed(
                color=self.bot.color,
                description=f"{ctx.author.mention} Are you sure you want to **disable** jail?",
            ),
        )

    @commands.command(
        description="enable the moaderation features in your server", help="moderation"
    )
    @Perms.get_perms("administrator")
    async def setme(self, ctx: commands.Context):
        check = await self.bot.db.fetchrow(
            "SELECT * FROM mod WHERE guild_id = $1", ctx.guild.id
        )
        if check:
            return await ctx.send_warning(
                "Moderation is **already** enabled in this server"
            )
        await ctx.typing()
        role = await ctx.guild.create_role(name="cut-jail")
        for channel in ctx.guild.channels:
            await channel.set_permissions(role, view_channel=False)
        overwrite = {
            role: discord.PermissionOverwrite(view_channel=True),
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
        }
        over = {ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False)}
        category = await ctx.guild.create_category(name="cut mod", overwrites=over)
        text = await ctx.guild.create_text_channel(
            name="mod-logs", overwrites=over, category=category
        )
        jai = await ctx.guild.create_text_channel(
            name="jail", overwrites=overwrite, category=category
        )
        await self.bot.db.execute(
            "INSERT INTO mod VALUES ($1,$2,$3,$4)",
            ctx.guild.id,
            text.id,
            jai.id,
            role.id,
        )
        await self.bot.db.execute("INSERT INTO cases VALUES ($1,$2)", ctx.guild.id, 0)
        return await ctx.send_success("Enabled **moderation** for this server")

    @commands.command(
        description="clone a channel", help="moderation", brief="server owner"
    )
    @Perms.server_owner()
    async def nuke(self, ctx: commands.Context):
        embed = discord.Embed(
            color=self.bot.color, description=f"Do you want to **nuke** this channel?"
        )
        yes = discord.ui.Button(emoji=self.bot.yes)
        no = discord.ui.Button(emoji=self.bot.no)

        async def yes_callback(interaction: discord.Interaction):
            if not interaction.user == ctx.guild.owner:
                return await self.bot.ext.send_warning(
                    interaction,
                    "You are not the **author** of this embed",
                    ephemeral=True,
                )
            c = await interaction.channel.clone()
            await c.edit(position=ctx.channel.position)
            await ctx.channel.delete()
            await c.send(content="first")

        async def no_callback(interaction: discord.Interaction):
            if not interaction.user == ctx.guild.owner:
                return await self.bot.ext.send_warning(
                    interaction,
                    "You are not the **author** of this embed",
                    ephemeral=True,
                )
            await interaction.response.edit_message(
                embed=discord.Embed(
                    color=self.bot.color, description="aborting action..."
                ),
                view=None,
            )

        yes.callback = yes_callback
        no.callback = no_callback
        view = discord.ui.View()
        view.add_item(yes)
        view.add_item(no)
        await ctx.reply(embed=embed, view=view)

    @commands.command(
        description="ban a member from your server",
        help="moderation",
        usage="[member] <reason>",
    )
    @Perms.get_perms("ban_members")
    async def ban(
        self,
        ctx: commands.Context,
        member: NoStaff,
        *,
        reason: str = "No reason provided",
    ):
        await ctx.guild.ban(user=member, reason=reason + " | {}".format(ctx.author))
        await ModConfig.send_dm(ctx, member, "banned", reason)
        await ModConfig.sendlogs(
            self.bot, "ban", ctx.author, member, reason + " | " + str(ctx.author)
        )
        if not await Invoke.invoke_send(ctx, member, reason):
            await ctx.send_success(f"**{member}** was banned - {reason}")

    @commands.command(
        description="kick a member from your server",
        help="moderation",
        usage="[member] <reason>",
    )
    @Perms.get_perms("kick_members")
    async def kick(
        self,
        ctx: commands.Context,
        member: NoStaff,
        *,
        reason: str = "No reason provided",
    ):
        await ctx.guild.kick(user=member, reason=reason + " | {}".format(ctx.author))
        await ModConfig.send_dm(ctx, member, "kicked", reason)
        await ModConfig.sendlogs(
            self.bot, "kick", ctx.author, member, reason + " | " + str(ctx.author)
        )
        if not await Invoke.invoke_send(ctx, member, reason):
            await ctx.send_success(f"**{member}** was kicked - {reason}")

    @commands.command(
        description="ban an user then immediately unban them",
        help="moderation",
        usage="[member] <reason>",
    )
    @Perms.get_perms("ban_members")
    async def softban(
        self,
        ctx: commands.Context,
        member: NoStaff,
        *,
        reason: str = "No reason provided",
    ):
        embed = discord.Embed(
            color=self.bot.color,
            description=f"Are you sure you want to softban **{member}**",
        )
        yes = discord.ui.Button(emoji=self.bot.yes)
        no = discord.ui.Button(emoji=self.bot.no)

        async def yes_callback(interaction: discord.Interaction):
            if not interaction.user == ctx.author:
                return await interaction.client.ext.send_warning(
                    interaction, "You are not the author of thid embed"
                )
            await ctx.guild.ban(user=member, reason=reason + " | {}".format(ctx.author))
            await ctx.guild.unban(user=member)
            await interaction.response.edit_message(
                embed=discord.Embed(
                    color=self.bot.color,
                    description=f"{self.bot.yes} {interaction.user.mention}: softbanned **{member}**",
                ),
                view=None,
            )

        async def no_callback(interaction: discord.Interaction):
            if not interaction.user == ctx.author:
                return await interaction.client.ext.send_warning(
                    interaction, "You are not the owner of this embed"
                )
            await interaction.response.edit_message(
                embed=discord.Embed(
                    color=self.bot.color, description="aborting action..."
                ),
                view=None,
            )

        yes.callback = yes_callback
        no.callback = no_callback
        view = discord.ui.View()
        view.add_item(yes)
        view.add_item(no)
        await ctx.reply(embed=embed, view=view)

    @commands.command(
        description="mute members in your server",
        help="moderation",
        brief="moderate members",
        usage="[member] [time] <reason>",
        aliases=["timeout"],
    )
    @Perms.get_perms("moderate_members")
    async def mute(
        self,
        ctx: commands.Context,
        member: NoStaff,
        time: str = "60s",
        *,
        reason="No reason provided",
    ):
        tim = humanfriendly.parse_timespan(time)
        until = discord.utils.utcnow() + datetime.timedelta(seconds=tim)
        await member.timeout(until, reason=reason + " | {}".format(ctx.author))
        if not await Invoke.invoke_send(ctx, member, reason):
            await ctx.send_success(
                f"**{member}** has been muted for {humanfriendly.format_timespan(tim)} | {reason}"
            )
        await ModConfig.sendlogs(
            self.bot,
            "mute",
            ctx.author,
            member,
            reason + " | " + humanfriendly.format_timespan(tim),
        )
        await ModConfig.send_dm(
            ctx, member, "muted", reason + " | " + humanfriendly.format_timespan(tim)
        )

    @commands.command(
        description="unmute a member in your server",
        help="moderation",
        brief="moderate members",
        usage="[member] <reason>",
        aliases=["untimeout"],
    )
    @Perms.get_perms("moderate_members")
    async def unmute(
        self,
        ctx: commands.Context,
        member: NoStaff,
        *,
        reason: str = "No reason provided",
    ):
        if not member.is_timed_out():
            return await ctx.send_warning(f"**{member}** is not muted")
        await member.edit(
            timed_out_until=None, reason=reason + " | {}".format(ctx.author)
        )
        await ModConfig.sendlogs(self.bot, "unmute", ctx.author, member, reason)
        if not await Invoke.invoke_send(ctx, member, reason):
            await ctx.send_success(f"unmuted **{member}**")

    @commands.command(description="see all muted mebmers", help="utility")
    @Perms.get_perms("moderate_members")
    async def muted(self, ctx: commands.Context):
        members = [m for m in ctx.guild.members if m.is_timed_out()]
        if len(members) == 0:
            return await ctx.send_error("There are no muted members")
        i = 0
        k = 1
        l = 0
        mes = ""
        number = []
        messages = []
        for member in members:
            mes = f"{mes}`{k}` {member.mention} - <t:{int(member.timed_out_until.timestamp())}:R> \n"
            k += 1
            l += 1
            if l == 10:
                messages.append(mes)
                number.append(
                    Embed(
                        color=self.bot.color,
                        title=f"{ctx.guild.name} Muted Members, ({len(members)})",
                        description=messages[i],
                    )
                )
                i += 1
                mes = ""
                l = 0

        messages.append(mes)
        embed = Embed(
            color=self.bot.color,
            title=f"{ctx.guild.name} Muted Members, ({len(members)})",
            description=messages[i],
        )
        number.append(embed)
        await ctx.paginator(number)

    @commands.command(description="see all banned members", help="utility")
    @Perms.get_perms("ban_members")
    async def bans(self, ctx: commands.Context):
        banned = [m async for m in ctx.guild.bans()]
        if len(banned) == 0:
            return await ctx.send_warning("There are no banned people in this server")
        i = 0
        k = 1
        l = 0
        mes = ""
        number = []
        messages = []
        for m in banned:
            mes = f"{mes}`{k}` **{m.user}** - `{m.reason or 'No reason provided'}` \n"
            k += 1
            l += 1
            if l == 10:
                messages.append(mes)
                number.append(
                    Embed(
                        color=self.bot.color,
                        title=f"{ctx.guild.name} Banned Members, ({len(banned)})",
                        description=messages[i],
                    )
                )
                i += 1
                mes = ""
                l = 0

        messages.append(mes)
        embed = Embed(
            color=self.bot.color,
            title=f"{ctx.guild.name} Banned Members, ({len(banned)})",
            description=messages[i],
        )
        number.append(embed)
        await ctx.paginator(number)

    @commands.command(
        description="unban an user from your server",
        help="moderation",
        usage="[member]",
    )
    async def unban(
        self,
        ctx: commands.Context,
        member: discord.User,
        *,
        reason: str = "No reason provided",
    ):
        try:
            await ctx.guild.unban(
                user=member, reason=reason + " | {}".format(ctx.author)
            )
            if not await Invoke.invoke_send(ctx, member, reason):
                await ctx.send_success(f"**{member}** has been unbanned")
        except discord.NotFound:
            return await ctx.send_warning(f"**{member}** is not banned")

    @commands.command(
        description="removes all staff roles from a member",
        help="moderation",
        usage="[member] <reason>",
    )
    @Perms.get_perms("administrator")
    async def strip(
        self,
        ctx: commands.Context,
        member: NoStaff,
        *,
        reason: str = "No reason provided",
    ):
        await ctx.channel.typing()
        await member.edit(
            roles=[
                role
                for role in member.roles
                if not role.is_assignable()
                or not self.bot.is_dangerous(role)
                or role.is_premium_subscriber()
            ],
            reason=reason + " | Moderator: {}".format(ctx.author),
        )
        await ctx.send_success(f"Removed **{member}'s** roles")
        await ModConfig.sendlogs(self.bot, "strip", ctx.author, member, reason)

    @commands.command(
        aliases=["p"],
        description="bulk delete messages",
        help="moderation",
        brief="manage messages",
        usage="[messages]",
    )
    @Perms.get_perms("manage_messages")
    async def purge(
        self, ctx: commands.Context, amount: int, *, member: NoStaff = None
    ):
        if member is None:
            await ctx.channel.purge(
                limit=amount + 1, bulk=True, reason=f"purge invoked by {ctx.author}"
            )
            return
        messages = []
        async for m in ctx.channel.history():
            if m.author.id == member.id:
                messages.append(m)
            if len(messages) == amount:
                break
        messages.append(ctx.message)
        await ctx.channel.delete_messages(messages)
        return

    @commands.command(
        description="bulk delete messages sent by bots",
        help="moderation",
        usage="[amount]",
        aliases=["bc", "botclear"],
    )
    @Perms.get_perms("manage_messages")
    async def botpurge(self, ctx: commands.Context, amount: int):
        mes = []
        async for message in ctx.channel.history():
            if len(mes) == amount:
                break
            if message.author.bot:
                mes.append(message)

        mes.append(ctx.message)
        await ctx.channel.delete_messages(mes)
        return

    @commands.command(
        description="jail a member",
        usage="[member]",
        help="moderation",
        brief="manage channels",
    )
    @Perms.get_perms("manage_channels")
    @Mod.is_mod_configured()
    async def jail(
        self,
        ctx: commands.Context,
        member: NoStaff,
        *,
        reason: str = "No reason provided",
    ):
        check = await self.bot.db.fetchrow(
            "SELECT * FROM jail WHERE guild_id = $1 AND user_id = $2",
            ctx.guild.id,
            member.id,
        )
        if check:
            return await ctx.send_warning(f"**{member}** is already jailed")
        if reason == None:
            reason = "No reason provided"
        roles = [
            r.id for r in member.roles if r.name != "@everyone" and r.is_assignable()
        ]
        sql_as_text = json.dumps(roles)
        await self.bot.db.execute(
            "INSERT INTO jail VALUES ($1,$2,$3)", ctx.guild.id, member.id, sql_as_text
        )
        chec = await self.bot.db.fetchrow(
            "SELECT * FROM mod WHERE guild_id = $1", ctx.guild.id
        )
        roleid = chec["role_id"]
        try:
            jail = ctx.guild.get_role(roleid)
            new = [r for r in member.roles if not r.is_assignable()]
            new.append(jail)
            if not await Invoke.invoke_send(ctx, member, reason):
                await member.edit(
                    roles=new, reason=f"jailed by {ctx.author} - {reason}"
                )
            await ctx.send_success(f"**{member}** got jailed - {reason}")
            await ModConfig.sendlogs(self.bot, "jail", ctx.author, member, reason)
            c = ctx.guild.get_channel(int(chec["jail_id"]))
            if c:
                await c.send(
                    f"{member.mention}, you have been **jailed!** Wait for a staff member to unjail you!"
                )
        except:
            return await ctx.send_error(f"There was a problem jailing **{member}**")

    @commands.command(
        description="unjail a member",
        usage="[member] [reason]",
        help="moderation",
        brief="manage channels",
    )
    @Perms.get_perms("manage_channels")
    @Mod.is_mod_configured()
    async def unjail(
        self,
        ctx: commands.Context,
        member: discord.Member,
        *,
        reason: str = "No reason provided",
    ):
        check = await self.bot.db.fetchrow(
            "SELECT * FROM jail WHERE guild_id = $1 AND user_id = $2",
            ctx.guild.id,
            member.id,
        )
        if not check:
            return await ctx.send_warning(f"**{member}** is not jailed")
        sq = check["roles"]
        roles = json.loads(sq)
        try:
            await member.edit(
                roles=[
                    ctx.guild.get_role(role)
                    for role in roles
                    if ctx.guild.get_role(role)
                ],
                reason=f"unjailed by {ctx.author}",
            )
        except:
            pass
        await self.bot.db.execute(
            "DELETE FROM jail WHERE user_id = {} AND guild_id = {}".format(
                member.id, ctx.guild.id
            )
        )
        if not await Invoke.invoke_send(ctx, member, reason):
            await ctx.send_success(f"Unjailed **{member}**")
        await ModConfig.sendlogs(self.bot, "unjail", ctx.author, member, reason)

    @commands.command(
        aliases=["sm"],
        description="add slowmode to a channel",
        help="moderation",
        usage="[seconds] <channel>",
    )
    @Perms.get_perms("manage_channels")
    async def slowmode(
        self, ctx: commands.Context, seconds: str, channel: discord.TextChannel = None
    ):
        chan = channel or ctx.channel
        tim = humanfriendly.parse_timespan(seconds)
        await chan.edit(
            slowmode_delay=tim, reason="slowmode invoked by {}".format(ctx.author)
        )
        return await ctx.send_success(
            f"Slowmode set to **{humanfriendly.format_timespan(tim)}** for {chan.mention}"
        )

    @commands.command(
        description="lock a channel", help="moderation", usage="<channel>"
    )
    @Perms.get_perms("manage_channels")
    async def lock(self, ctx: commands.Context, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        return await ctx.send_success(f"Locked {channel.mention}")

    @commands.command(
        description="unlock a channel", help="moderation", usage="<channel>"
    )
    @Perms.get_perms("manage_channels")
    async def unlock(self, ctx: commands.Context, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        # if channel.has_permissions(send_messages=True): return await ctx.send_error("This channel is already **unlocked**")
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        return await ctx.send_success(f"Unlocked {channel.mention}")

    @commands.command(
        description="hide a channel", help="moderation", usage="<channel>"
    )
    @Perms.get_perms("manage_channels")
    async def hide(self, ctx: commands.Context, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.view_channel = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        return await ctx.send_success(f"Hidden {channel.mention}")

    @commands.command(
        description="reveal a channel", help="moderation", usage="<channel>"
    )
    @Perms.get_perms("manage_channels")
    async def reveal(self, ctx: commands.Context, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.view_channel = True
        # if channel.has_permissions(send_messages=True): return await ctx.send_error("This channel is already **unlocked**")
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        return await ctx.send_success(f"Revealed {channel.mention}")

    @commands.group(invoke_without_command=True)
    async def role(self, ctx):
        await ctx.create_pages()

    @role.command(
        name="add",
        description="add a role to a member",
        help="moderation",
        usage="[member] [role]",
    )
    @Perms.get_perms("manage_roles")
    async def role_add(
        self, ctx: commands.Context, user: discord.Member, *, role: GoodRole
    ):
        if role in user.roles:
            return await ctx.send_error(f"**{user}** has this role already")
        await user.add_roles(role)
        return await ctx.send_success(f"Added {role.mention} to **{user.name}**")

    @role.command(
        name="remove",
        description="remove a role from a member",
        help="moderation",
        usage="[member] [role]",
    )
    @Perms.get_perms("manage_roles")
    async def role_remove(
        self, ctx: commands.Context, user: discord.Member, *, role: GoodRole
    ):
        if not role in user.roles:
            return await ctx.send_error(f"**{user}** doesn't have this role")
        await user.remove_roles(role)
        return await ctx.send_success(f"Removed {role.mention} from **{user.name}**")

    @role.command(
        name="create", description="create a role", help="moderation", usage="[name]"
    )
    @Perms.get_perms("manage_roles")
    async def role_create(self, ctx: commands.Context, *, name: str):
        role = await ctx.guild.create_role(
            name=name, reason="Role created by {}".format(ctx.author)
        )
        return await ctx.send_success(f"Created role {role}")

    @role.command(
        description="delete a role",
        help="moderation",
        usage="[role]",
        brief="manage roles",
    )
    @Perms.get_perms("manage_roles")
    async def delete(self, ctx: commands.Context, *, role: GoodRole):
        await role.delete()
        return await ctx.send_success("Deleted the role")

    @role.group(
        invoke_without_command=True, help="moderation", description="edit a role"
    )
    async def edit(self, ctx: commands.Context):
        return await ctx.create_pages()

    @edit.command(
        description="make a role visible separately.. or not",
        brief="manage roles",
        help="moderation",
        usage="[role] [true or false]",
    )
    @Perms.get_perms("manage_roles")
    async def hoist(self, ctx: commands.Context, role: GoodRole, state: str):
        if not state.lower() in ["true", "false"]:
            return await ctx.send_error(f"**{state}** can be only true or false")
        await role.edit(hoist=bool(state.lower() == "true"))
        return await ctx.send_success(
            f"{f'The role is now hoisted' if role.hoist is True else 'The role is not hoisted anymore'}"
        )

    @edit.command(
        aliases=["pos"],
        description="change a role's position",
        help="moderation",
        usage="[role] [position]",
        brief="manage roles",
    )
    @Perms.get_perms("manage_roles")
    async def position(self, ctx: commands.Context, role: GoodRole, *, position: int):
        await role.edit(position=position)
        return await ctx.send_success(f"Changed role position to `{position}`")

    @edit.command(
        brief="manage roles",
        description="change a role's name",
        help="moderation",
        usage="[role] [name]",
    )
    @Perms.get_perms("manage_roles")
    async def name(self, ctx: commands.Context, role: GoodRole, *, name: str):
        await role.edit(name=name, reason=f"role edited by {ctx.author}")
        return await ctx.send_success(f"Role name changed to **{name}**")

    @edit.command(
        description="change a role's color", help="moderation", usage="[role] [color]"
    )
    @Perms.get_perms("manage_roles")
    async def color(self, ctx: commands.Context, role: GoodRole, *, color: str):
        try:
            color = color.replace("#", "")
            await role.edit(color=int(color, 16), reason=f"role edited by {ctx.author}")
            return await ctx.reply(
                embed=discord.Embed(
                    color=role.color,
                    description=f"{self.bot.yes} {ctx.author.mention}: Changed role's color",
                )
            )
        except:
            return await ctx.send_error("Unable to change the role's color")

    @edit.command(
        description="change a role's icon",
        brief="manage roles",
        help="moderation",
        usage="[role] <emoji>",
    )
    @Perms.get_perms("manage_roles")
    async def icon(
        self,
        ctx: commands.Context,
        role: GoodRole,
        emoji: Union[discord.PartialEmoji, str],
    ):
        if isinstance(emoji, discord.PartialEmoji):
            by = await emoji.read()
            await role.edit(display_icon=by)
        elif isinstance(emoji, str):
            await role.edit(display_icon=str(emoji))
        return await ctx.send_success("Changed role icon")

    @role.group(
        invoke_without_command=True,
        name="humans",
        description="mass add or remove roles from members",
        help="moderation",
    )
    async def rolehumans(self, ctx: commands.Context):
        return await ctx.create_pages()

    @rolehumans.command(
        name="remove",
        description="remove a role from all members in this server",
        help="moderation",
        usage="[role]",
        brief="manage_roles",
    )
    @Perms.get_perms("manage_roles")
    async def rolehumansremove(self, ctx: commands.Context, *, role: GoodRole):
        message = await ctx.reply(
            embed=discord.Embed(
                color=self.bot.color,
                description=f"{ctx.author.mention} Removing {role.mention} from all humans...",
            )
        )
        try:
            for member in [m for m in ctx.guild.members if not m.bot]:
                if not role in member.roles:
                    continue
                await member.remove_roles(role)

            await message.edit(
                embed=discord.Embed(
                    color=self.bot.color,
                    description=f"{self.bot.yes} {ctx.author.mention}: Removed {role.mention} from all humans",
                )
            )
        except Exception:
            await message.edit(
                embed=discord.Embed(
                    color=self.bot.color,
                    description=f"{self.bot.no} {ctx.author.mention}: Unable to remove {role.mention} from all humans",
                )
            )

    @rolehumans.command(
        name="add",
        description="add a role to all humans in this server",
        help="moderation",
        usage="[role]",
        brief="manage_roles",
    )
    @Perms.get_perms("manage_roles")
    async def rolehumansadd(self, ctx: commands.Context, *, role: GoodRole):
        message = await ctx.reply(
            embed=discord.Embed(
                color=self.bot.color,
                description=f"{ctx.author.mention}: Adding {role.mention} to all humans...",
            )
        )
        try:
            for member in [m for m in ctx.guild.members if not m.bot]:
                if role in member.roles:
                    continue
                await member.add_roles(role)

            await message.edit(
                embed=discord.Embed(
                    color=self.bot.color,
                    description=f"{self.bot.yes} {ctx.author.mention}: Added {role.mention} to all humans",
                )
            )
        except Exception:
            await message.edit(
                embed=discord.Embed(
                    color=self.bot.color,
                    description=f"{self.bot.no} {ctx.author.mention}: Unable to add {role.mention} to all humans",
                )
            )

    @role.group(
        invoke_without_command=True,
        name="all",
        description="mass add or remove roles from members",
        help="moderation",
    )
    async def roleall(self, ctx: commands.Context):
        return await ctx.create_pages()

    @roleall.command(
        name="remove",
        description="remove a role from all members in this server",
        help="moderation",
        usage="[role]",
        brief="manage_roles",
    )
    @Perms.get_perms("manage_roles")
    async def roleallremove(self, ctx: commands.Context, *, role: GoodRole):
        message = await ctx.reply(
            embed=discord.Embed(
                color=self.bot.color,
                description=f"{ctx.author.mention} Removing {role.mention} from all members...",
            )
        )
        try:
            for member in ctx.guild.members:
                if not role in member.roles:
                    continue
                await member.remove_roles(role)

            await message.edit(
                embed=discord.Embed(
                    color=self.bot.color,
                    description=f"{self.bot.yes} {ctx.author.mention}: Removed {role.mention} from all members",
                )
            )
        except Exception:
            await message.edit(
                embed=discord.Embed(
                    color=self.bot.color,
                    description=f"{self.bot.no} {ctx.author.mention}: Unable to remove {role.mention} from all members",
                )
            )

    @roleall.command(
        name="add",
        description="add a role to all members in this server",
        help="moderation",
        usage="[role]",
        brief="manage_roles",
    )
    @Perms.get_perms("manage_roles")
    async def rolealladd(self, ctx: commands.Context, *, role: GoodRole):
        message = await ctx.reply(
            embed=discord.Embed(
                color=self.bot.color,
                description=f"{ctx.author.mention}: Adding {role.mention} to all members...",
            )
        )
        try:
            for member in ctx.guild.members:
                if role in member.roles:
                    continue
                await member.add_roles(role)

            await message.edit(
                embed=discord.Embed(
                    color=self.bot.color,
                    description=f"{self.bot.yes} {ctx.author.mention}: Added {role.mention} to all members",
                )
            )
        except Exception:
            await message.edit(
                embed=discord.Embed(
                    color=self.bot.color,
                    description=f"{self.bot.no} {ctx.author.mention}: Unable to add {role.mention} to all members",
                )
            )

    @commands.hybrid_command(
        aliases=["setnick", "nick"],
        description="change an user's nickname",
        usage="[member] <nickname>",
        help="moderation",
    )
    @Perms.get_perms("manage_nicknames")
    @Mod.is_mod_configured()
    async def nickname(self, ctx, member: NoStaff, *, nick: str = None):
        if nick == None or nick.lower() == "none":
            return await ctx.send_success(f"Cleared **{member.name}'s** nickname")
        await member.edit(nick=nick)
        return await ctx.send_success(
            f"Changed **{member.name}'s** nickname to **{nick}**"
        )

    @commands.command(
        aliases=["vcmute"],
        description="mute a member in a voice channel",
        brief="moderate members",
        usage="[member]",
        help="moderation",
    )
    @Perms.get_perms("moderate_members")
    async def voicemute(self, ctx: commands.Context, *, member: NoStaff):
        if not member.voice.channel:
            return await ctx.send_warning(f"**{member}** is **not** in a voice channel")
        if member.voice.self_mute:
            return await ctx.send_warning(f"**{member}** is **already** voice muted")
        await member.edit(mute=True, reason=f"Voice muted by {ctx.author}")
        return await ctx.send_success(f"Voice muted **{member}**")

    @commands.command(
        aliases=["vcunmute"],
        description="unmute a member in a voice channel",
        brief="moderate members",
        usage="[member]",
        help="moderation",
    )
    @Perms.get_perms("moderate_members")
    async def voiceunmute(self, ctx: commands.Context, *, member: NoStaff):
        if not member.voice.channel:
            return await ctx.send_warning(f"**{member}** is **not** in a voice channel")
        if not member.voice.self_mute:
            return await ctx.send_warning(f"**{member}** is **not** voice muted")
        await member.edit(mute=True, reason=f"Voice muted by {ctx.author}")
        return await ctx.send_success(f"Voice muted **{member}**")

    @commands.group(name="clear", invoke_without_command=True)
    async def mata_clear(self, ctx):
        return await ctx.create_pages()

    @mata_clear.command(
        help="moderation",
        description="clear messages that contain a certain word",
        usage="[word]",
        brief="manage messages",
    )
    async def contains(self, ctx: commands.Context, *, word: str):
        messages = [
            message
            async for message in ctx.channel.history(limit=300)
            if word in message.content
        ]
        if len(messages) == 0:
            return await ctx.send_warning(
                f"No messages containing **{word}** in this channel"
            )
        await ctx.channel.delete_messages(messages)

    @commands.group(invoke_without_command=True)
    @Perms.get_perms("manage_messages")
    @Mod.is_mod_configured()
    async def warn(
        self,
        ctx: commands.Context,
        member: NoStaff = None,
        *,
        reason: str = "No reason provided",
    ):
        if member is None:
            return await ctx.create_pages()
        date = datetime.datetime.now()
        await self.bot.db.execute(
            "INSERT INTO warns VALUES ($1,$2,$3,$4,$5)",
            ctx.guild.id,
            member.id,
            ctx.author.id,
            f"{date.day}/{f'0{date.month}' if date.month < 10 else date.month}/{str(date.year)[-2:]} at {datetime.datetime.strptime(f'{date.hour}:{date.minute}', '%H:%M').strftime('%I:%M %p')}",
            reason,
        )
        await ctx.send_success(f"Warned **{member}** | {reason}")
        await ModConfig.sendlogs(self.bot, "warn", ctx.author, member, reason)
        await ModConfig.send_dm(ctx, member, "warned", reason)

    @warn.command(
        description="clear all warns from an user",
        help="moderation",
        usage="[member]",
        brief="manage messages",
    )
    @Perms.get_perms("manage_messages")
    @Mod.is_mod_configured()
    async def clear(self, ctx: commands.Context, *, member: NoStaff):
        check = await self.bot.db.fetch(
            "SELECT * FROM warns WHERE guild_id = $1 AND user_id = $2",
            ctx.guild.id,
            member.id,
        )
        if len(check) == 0:
            return await ctx.send_warning("this user has no warnings".capitalize())
        await self.bot.db.execute(
            "DELETE FROM warns WHERE guild_id = $1 AND user_id = $2",
            ctx.guild.id,
            member.id,
        )
        await ctx.send_success(f"Removed **{member.name}'s** warns")

    @warn.command(
        name="list",
        description="shows all warns of an user",
        help="moderation",
        usage="[member]",
    )
    @Mod.is_mod_configured()
    async def list(self, ctx: commands.Context, *, member: discord.Member):
        check = await self.bot.db.fetch(
            "SELECT * FROM warns WHERE guild_id = $1 AND user_id = $2",
            ctx.guild.id,
            member.id,
        )
        if len(check) == 0:
            return await ctx.send_warning("this user has no warnings".capitalize())
        i = 0
        k = 1
        l = 0
        mes = ""
        number = []
        messages = []
        for result in check:
            mes = f"{mes}`{k}` {result['time']} by **{await self.bot.fetch_user(result['author_id'])}** - {result['reason']}\n"
            k += 1
            l += 1
            if l == 10:
                messages.append(mes)
                number.append(
                    discord.Embed(
                        color=self.bot.color,
                        title=f"{member.name} Warns, ({len(check)})",
                        description=messages[i],
                    )
                )
                i += 1
                mes = ""
                l = 0

        messages.append(mes)
        embed = discord.Embed(
            color=self.bot.color,
            title=f"{member.name} Warns, ({len(check)})",
            description=messages[i],
        ).set_footer(text="All times are GMT")
        number.append(embed)
        await ctx.paginator(number)

    @commands.command(
        description="shows all warns of an user", help="moderation", usage="[member]"
    )
    @Mod.is_mod_configured()
    async def warns(self, ctx: commands.Context, *, member: discord.Member):
        return await ctx.invoke(self.bot.get_command("warn list"), member=member)

    @role.group(
        invoke_without_command=True,
        name="bots",
        description="mass add or remove roles from members",
        help="moderation",
    )
    async def rolebots(self, ctx: commands.Context):
        return await ctx.create_pages()

    @rolebots.command(
        name="remove",
        description="remove a role from all bots in this server",
        help="moderation",
        usage="[role]",
        brief="manage_roles",
    )
    @Perms.get_perms("manage_roles")
    async def rolebotsremove(self, ctx: commands.Context, *, role: GoodRole):
        embed = discord.Embed(
            color=self.bot.color,
            description=f"{ctx.author.mention} Removing {role.mention} from all bots....",
        )
        message = await ctx.reply(embed=embed)
        try:
            for member in [m for m in ctx.guild.members if m.bot]:
                if not role in member.roles:
                    continue
                await member.remove_roles(role)

            await message.edit(
                embed=discord.Embed(
                    color=self.bot.color,
                    description=f"{self.bot.yes} {ctx.author.mention}: Removed {role.mention} from all bots",
                )
            )
        except Exception:
            await message.edit(
                embed=discord.Embed(
                    color=self.bot.color,
                    description=f"{self.bot.no} {ctx.author.mention}: Unable to remove {role.mention} from all bots",
                )
            )

    @rolebots.command(
        name="add",
        description="add a role to all bots in this server",
        help="moderation",
        usage="[role]",
        brief="manage_roles",
    )
    @Perms.get_perms("manage_roles")
    async def rolebotsadd(self, ctx: commands.Context, *, role: GoodRole):
        embed = discord.Embed(
            color=self.bot.color,
            description=f"{ctx.author.mention}: Adding {role.mention} to all bots....",
        )
        message = await ctx.reply(embed=embed)
        try:
            for member in [m for m in ctx.guild.members if m.bot]:
                if role in member.roles:
                    continue
                await member.add_roles(role)

            await message.edit(
                embed=discord.Embed(
                    color=self.bot.color,
                    description=f"{self.bot.yes} {ctx.author.mention}: Added {role.mention} to all bots",
                )
            )
        except Exception:
            await message.edit(
                embed=discord.Embed(
                    color=self.bot.color,
                    description=f"{self.bot.no} {ctx.author.mention}: Unable to add {role.mention} to all bots",
                )
            )


async def setup(bot):
    await bot.add_cog(Mod(bot))
