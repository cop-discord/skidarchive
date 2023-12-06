import discord 
import asyncio
import psutil
import platform
import datetime
import typing
from typing import Union
from discord.ext import commands 

from tools.bot import DiscordBot
from tools.context import HarmContext

class moderation(commands.Cog):
    def __init__(self, bot: DiscordBot):
      self.bot = bot 


    @commands.hybrid_command()
    @commands.bot_has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: typing.Union[discord.Member, discord.User]=None, *, reason="No reason provided."):
      
        if member is None:
            embed = discord.Embed(title='ban').set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
            embed.add_field(
                name='Usage',
                value=f"```bf\nSyntax: $ban (member)\nExample: $ban @newyorkians```"
            )
            await ctx.send(embed=embed)
            return

        if member == ctx.author:
            await ctx.send("You cannot ban yourself.")
            return

        if ctx.author.top_role <= member.top_role:
            await ctx.send("You cannot ban a member with the same or higher role than you.")
            return

        if member == self.bot.user:
            await ctx.send("I cannot be banned.")
            return

        try:
            await ctx.guild.ban(user=member, reason=reason + f" | Banned by {ctx.author}")
            await ctx.send(f"{member} has been banned | {reason}")
            await self.send_dm(ctx.guild, member, reason, ctx.author)
        except discord.Forbidden:
            await ctx.send("I don't have permissions to ban members.")
        except BadArgument:
            await ctx.send("Invalid member provided. Please mention a user, use their username, or provide their user ID.")

    @commands.hybrid_command()
    @commands.bot_has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason="No reason provided."):
      if member is None:
          embed = discord.Embed(title='kick').set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
          embed.add_field(
              name='Usage',
              value=f"```bf\nSyntax: $kick (member)\nExample: $kick @newyorkians```"
          )
          await ctx.send(embed=embed)
          return

      if member == ctx.author:
          await ctx.send("You cannot kick yourself.")
          return

      if member == self.bot.user:
          await ctx.send("I cannot kick myself.")
          return

      if ctx.author.top_role <= member.top_role:
          await ctx.send("You cannot kick a member with the same or higher role than you.")
          return

      try:
          await self.send_kick_dm(ctx.guild, member, reason, ctx.author)
      except discord.Forbidden:
          await ctx.send("I don't have permission to send DMs to the user.")

      try:
          await member.kick(reason=reason + f"| moderater {ctx.author}")
          await ctx.send(f"{member.mention} has been kicked from the server | {reason}")
      except discord.Forbidden:
          await ctx.send("I don't have permission to kick members.")
      except discord.HTTPException:
          await ctx.send("An error occurred while trying to kick the member.")

    @commands.hybrid_command()
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def hide(ctx, targets: discord.Role):
        channel = ctx.channel
        
        overwrite = discord.PermissionOverwrite()
        overwrite.read_messages = False  # Hide the ability to read messages
        
        # If roles are specified, apply the permission overwrite to those roles
        if targets:
            for role in targets:
                await channel.set_permissions(role, overwrite=overwrite)
            await ctx.send(f"The channel has been hidden from specified roles.")
        else:
            # If no roles are specified, hide the channel from everyone
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            await ctx.send("The channel has been hidden from everyone.")

async def setup(bot: DiscordBot) -> None:
   return await bot.add_cog(moderation(bot))     
