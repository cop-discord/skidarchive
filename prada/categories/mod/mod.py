import discord, datetime
from typing import Optional
import asyncio
from discord.ext import commands
from discord import Message, Member, User, Embed, PermissionOverwrite
from discord.ext.commands import Cog, command, Context, CommandError, cooldown, BucketType, CooldownMapping
from datetime import timedelta, datetime
import pytz
from core import Slut

class Moderation(Cog):
    def __init__(self, bot: Slut) -> None:
        self.bot: Slut = bot
        self.ladder_control = CooldownMapping.from_cooldown(3, 3, BucketType.member)
        self.lock = asyncio.Lock()

    @staticmethod
    def has_audit_log_permissions(ctx):
        return ctx.guild.me.guild_permissions.view_audit_log

    @command(aliases=["auditlog", "logs"])
    async def audit(self, ctx):
        # Check if the author has the view_audit_log permission
        if not ctx.author.guild_permissions.view_audit_log:
            await self.send_insufficient_permissions_message(ctx, "view_audit_log")
            return

        # Fetch the audit log entries
        audit_logs = await asyncio.gather(*(entry for entry in ctx.guild.audit_logs(limit=10)))

        # Create an embed for each entry
        embeds = []
        for entry in audit_logs:
            embed = discord.Embed(title="Audit Log", color=discord.Color.blue())
            embed.add_field(name="Action", value=entry.action, inline=False)
            embed.add_field(name="User", value=f"{entry.user} ({entry.user.id})", inline=False)
            embed.add_field(name="Target", value=entry.target, inline=False)
            embed.add_field(name="Reason", value=entry.reason, inline=False)
            embeds.append(embed)

        # Send the first page
        current_page = 0
        message = await ctx.send(embed=embeds[current_page])

        # Add reactions for pagination
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")

        def check(reaction, user):
            return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ["⬅️", "➡️"]

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)

                if str(reaction.emoji) == "➡️" and current_page < len(embeds) - 1:
                    current_page += 1
                elif str(reaction.emoji) == "⬅️" and current_page > 0:
                    current_page -= 1

                await message.edit(embed=embeds[current_page])
                await message.remove_reaction(reaction, user)
            except TimeoutError:
                break


    async def send_insufficient_permissions_message(self, ctx, permission):
        embed = discord.Embed(
            color=0x2B2D31,
            description=f"> {ctx.author.mention}: You have **insufficient** permissions (`{permission}`) to execute this command."
        )
        await ctx.send(embed=embed)

    async def purge_messages(self, channel, check):
        async with self.lock:
            try:
                # Fetch recent messages to be purged
                messages = []
                async for message in channel.history(limit=100):
                    messages.append(message)

                # Filter messages based on the check function
                messages_to_purge = [message for message in messages if check(message)]

                if messages_to_purge:
                    # Purge the messages
                    await channel.delete_messages(messages_to_purge)

            except discord.Forbidden:
                print(f"Bot does not have the 'Manage Messages' permission in {channel.name}")

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        """
        Automatically mute morons which ladder type.
        """

        if (
            message.author.bot
            or not message.content
            or not isinstance(message.author, Member)
        ):
            return

        if len(message.content) >= 6 or message.author.premium_since:
            return

        # You can add your ladder typing logic here

        bucket = self.ladder_control.get_bucket(message)
        if bucket and bucket.update_rate_limit():
            await message.author.timeout(
                timedelta(minutes=5),
                reason=f"User caught ladder typing in #{message.channel}",
            )

            await message.channel.send(
                f"Cleaning up after that moron {message.author}...",
            )

            # Purge only the recent ladder-typed messages by the user
            await self.purge_messages(message.channel, lambda m: m.author == message.author and len(m.content) < 6)
    @command()
    async def unbanall(self, ctx: Context):
        if ctx.author.guild_permissions.ban_members:
            banned_users = await ctx.guild.bans()
            banned_user_count = len(banned_users)
            start_time = datetime.utcnow()

            # Sending initial embed
            initial_embed = Embed(
                description=f"Unbanning {banned_user_count} users...",
                color=0xFF5733
            )
            initial_message = await ctx.send(embed=initial_embed)

            # Unbanning users
            for ban_entry in banned_users:
                await ctx.guild.unban(ban_entry.user)

            # Calculate the time taken for unbanning
            end_time = datetime.utcnow()
            time_taken = end_time - start_time
            ms = time_taken.total_seconds() * 1000

            # Sending final embed
            final_embed = Embed(
                title="Mass Unban Complete",
                description=f"Successfully unbanned {banned_user_count} users in {ms:.2f} ms.",
                color=0x00FF00
            )
            final_embed.set_footer(text=f"Command executed by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)

            # Delete the initial embed message and send the final embed
            await initial_message.delete()
            await ctx.send(embed=final_embed)
        else:
            await ctx.send("You don't have permission to unban all users.")

    @command(aliases=['yeet', 'boot', 'throw'])
    async def kick(self, ctx: Context, member: discord.Member = None, *, reason: str = "No reason provided."):
        if ctx.author.guild_permissions.kick_members:
            if member is None:
                embed = discord.Embed(description="Kick members from your server", color=0x2B2D31)
                embed.set_author(name='prada', icon_url="https://images-ext-1.discordapp.net/external/RXCCokquRxmkpev1ANTQdRW_wTjo7UrN86wZesQuwKM/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/605506274896904192/8a04d2a10549a949b765624dcb0eb00c.png?width=632&height=632")
                embed.add_field(name="Usage", value="`kick [member] <reason>`", inline=False)
                embed.set_footer(text="Aliases: yeet, boot, throw • Category: moderation • Permissions: Kick Members • Today at {}".format(datetime.now().strftime('%I:%M %p')))
                await ctx.send(embed=embed)
            else:
                # Check if the user invoking the command has a higher role than the target user
                if ctx.author.top_role > member.top_role:
                    await member.kick(reason=reason)

                    # Sending DM to the kicked user
                    dm_embed = discord.Embed(title="Kicked", color=0xFF5733, timestamp=datetime.utcnow())
                    dm_embed.add_field(name="Server", value=ctx.guild.name, inline=True)
                    dm_embed.add_field(name="Moderator", value=f"{ctx.author.name}#{ctx.author.discriminator}", inline=True)
                    dm_embed.add_field(name="Reason", value=reason, inline=True)
                    dm_embed.set_footer(text="If you would like to dispute this punishment, contact a staff member")
                    utc_now = datetime.utcnow()
                    eastern = pytz.timezone('America/New_York')
                    eastern_now = utc_now.replace(tzinfo=pytz.utc).astimezone(eastern)
                    author_user = ctx.author
                    timestamp=eastern_now 
                    dm_embed.set_thumbnail(url=author_user.avatar.url)
                    try:
                        await member.send(embed=dm_embed)
                    except discord.Forbidden:
                        await ctx.send(f"👍 - couldn't send a direct message to **{member.name}**")
                        await ctx.message.add_reaction('✅')
                else:
                    await ctx.send("You cannot kick a user with an equal or higher role.")
        else:
            embed = discord.Embed(color=0x2B2D31, description=f"> {ctx.author.mention}: You have **insufficient** permissions (`kick_members`) to execute `kick`.")
            await ctx.send(embed=embed)


    @command(aliases=['banland', 'deport', 'noskidding'])
    async def ban(self, ctx: Context, user: discord.Member = None, *, reason: str = "No reason provided."):
        if ctx.author.guild_permissions.ban_members:
            if user is None:
                embed = discord.Embed(description="Ban members from your server", color=0x2B2D31)
                embed.set_author(name='prada', icon_url='https://images-ext-1.discordapp.net/external/RXCCokquRxmkpev1ANTQdRW_wTjo7UrN86wZesQuwKM/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/605506274896904192/8a04d2a10549a949b765624dcb0eb00c.png?width=632&height=632')
                embed.add_field(name="Usage", value="`ban [member] <reason>`", inline=False)
                embed.set_footer(text="Aliases: banland, deport, noskidding • Category: moderation • Permissions: Ban Members • Today at {}".format(datetime.now().strftime('%I:%M %p')))
                await ctx.send(embed=embed)
            else:
                # Check if the user invoking the command has a higher role than the target user
                if ctx.author.top_role > user.top_role:
                    await ctx.guild.ban(user, reason=reason)

                    # Sending DM to the banned user
                    dm_embed = discord.Embed(title="Banned", color=0xFF5733, timestamp=datetime.utcnow())
                    dm_embed.add_field(name="Server", value=ctx.guild.name, inline=True)
                    dm_embed.add_field(name="Moderator", value=f"{ctx.author.name}#{ctx.author.discriminator}", inline=True)
                    dm_embed.add_field(name="Reason", value=reason, inline=True)
                    dm_embed.set_footer(text="If you would like to dispute this punishment, contact a staff member")
                    utc_now = datetime.utcnow()
                    eastern = pytz.timezone('America/New_York')
                    eastern_now = utc_now.replace(tzinfo=pytz.utc).astimezone(eastern)
                    author_user = ctx.author
                    timestamp=eastern_now 
                    dm_embed.set_thumbnail(url=author_user.avatar.url)
                    try:
                        await user.send(embed=dm_embed)
                    except discord.Forbidden:
                        await ctx.send(f"👍 - couldn't send a direct message to **{user.name}**")

                    await ctx.message.add_reaction('✅')
                else:
                    await ctx.send("You cannot ban a user with an equal or higher role.")
        else:
            embed = discord.Embed(color=0x2B2D31, description=f"> {ctx.author.mention}: You have **insufficient** permissions (`ban_members`) to execute `ban`.")
            await ctx.send(embed=embed)
	
    @command(name="purge", aliases=['p'])
    async def purge(self, ctx: Context, amount: int = None):
        if amount is None:
            # Send help message if no amount is specified
            embed = discord.Embed(
                title="purge",
                description="`bulk delete messages`",
                color=0x2B2D31  # Set your desired color here
            )
            embed.set_author(name='prada', icon_url='https://images-ext-1.discordapp.net/external/RXCCokquRxmkpev1ANTQdRW_wTjo7UrN86wZesQuwKM/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/605506274896904192/8a04d2a10549a949b765624dcb0eb00c.png?width=632&height=632')  # Set your avatar URL here
            embed.add_field(name="Usage", value=f"```;purge [amount]```", inline=False)
            embed.set_footer(text="Aliases: p • Category: moderation")
            await ctx.send(embed=embed)
        elif ctx.author.guild_permissions.manage_messages:
            await ctx.message.delete()
            deleted = await ctx.channel.purge(limit=amount)
            await ctx.send(f"Successfully deleted {len(deleted)} messages.", delete_after=5)
        else:
            embed = discord.Embed(color=0x2B2D31, description=f"> {ctx.author.mention}: You have **insufficient** permissions (`manage_messages`) to execute permission to execute `purge`.")
            await ctx.send(embed=embed)

    @command(aliases=['strip'])
    async def staffstrip(self, ctx: Context, member: discord.Member):
        if ctx.author.guild_permissions.manage_roles:
            permissions_to_check = ['ban_members', 'kick_members', 'administrator']
        
        if ctx.author.guild_permissions.manage_roles:
            roles_to_remove = []
            for role in member.roles:
                for permission in permissions_to_check:
                    if getattr(role.permissions, permission):
                        roles_to_remove.append(role)

            if roles_to_remove:
                await member.remove_roles(*roles_to_remove)
                await ctx.send(f"Removed roles with permissions: `administrator`, `kick_members`, `ban_members`, `manage_guild` from {member.name}.")
            else:
                await ctx.send(f"No roles found with the specified permissions.")
        else:
            await ctx.send("You don't have permission to manage roles.")


    @command()
    async def softban(self, ctx: Context, user: discord.User, *, reason: Optional[str] = "No reason provided."):
        if ctx.author.guild_permissions.ban_members:
            await ctx.guild.ban(user, reason=reason)
            await ctx.guild.unban(user)
            await ctx.message.add_reaction('✅')
        else:
            await ctx.send("You don't have permission to softban users.")

    @command()
    async def lock(self, ctx: Context):
        if ctx.author.guild_permissions.manage_channels:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
            await ctx.send("Channel locked.")
        else:
            await ctx.send("You don't have permission to lock this channel.")

    @command()
    async def unlock(self, ctx: Context):
        if ctx.author.guild_permissions.manage_channels:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
            await ctx.send("Channel unlocked.")
        else:
            await ctx.send("You don't have permission to unlock this channel.")

    @command()
    async def hide(self, ctx: Context):
        if ctx.author.guild_permissions.manage_channels:
            overwrites = ctx.channel.overwrites_for(ctx.guild.default_role)
            overwrites.view_channel = False
            await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send("Channel hidden.")
        else:
            await ctx.send("You don't have permission to hide this channel.")

    @command()
    async def unhide(self, ctx: Context):
        if ctx.author.guild_permissions.manage_channels:
            overwrites = ctx.channel.overwrites_for(ctx.guild.default_role)
            overwrites.view_channel = None  # None restores the permission to inherit
            await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send("Channel unhidden.")
        else:
            await ctx.send("You don't have permission to unhide this channel.")

    @command()
    async def role(self, ctx: Context, member: discord.Member, *, role_name: str):
        if ctx.author.guild_permissions.manage_roles:
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if role:
                if role in member.roles:
                    await member.remove_roles(role)
                    await ctx.send(f"Removed {role.name} role from {member.mention}.")
                else:
                    await member.add_roles(role)
                    await ctx.send(f"Added {role.name} role to {member.mention}.")
            else:
                await ctx.send(f"Role '{role_name}' not found.")
        else:
            await self.send_insufficient_permissions_message(ctx, "manage_roles")

    @command(aliases=["sm"], help="add slowmode to a channel", description="moderation", usage="<channel>")
    async def slowmode(self, ctx, seconds: int=None, channel: discord.TextChannel=None):
        if ctx.author.guild_permissions.manage_roles:
            if seconds is None:
                embed = discord.Embed(color=0x2B2D31, description=f"{ctx.author.mention}: provide seconds for this channel")
                await ctx.send(embed=embed)
            else:
                chan = channel or ctx.channel
                await chan.edit(slowmode_delay=seconds)
                embed = discord.Embed(color=0x2B2D31, description=f"{ctx.author.mention} set slowmode time for {chan.mention} to **{seconds} seconds**")
                await ctx.send(embed=embed)
        else:
            await self.send_insufficient_permissions_message(ctx, "manage_roles")


    async def send_insufficient_permissions_message(self, ctx, permission):
        embed = discord.Embed(
            color=0x2B2D31,
            description=f"> {ctx.author.mention}: You have **insufficient** permissions (`{permission}`) to execute this `{ctx.command.name}`."
        )
        await ctx.send(embed=embed)
