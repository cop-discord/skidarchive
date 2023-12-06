from typing import Type
import os
from discord import Message, Embed
import discord
import aiohttp
from discord.ext.commands import Cog, Context, command
from config import owner_ids
from core import Slut


class Developer(Cog, description=">.<"):
    def __init__(self, bot: Slut) -> None:
        self.bot: Slut = bot
        self.owner_ids = [628236220392275969, 1040008141301088276]

    @command(aliases=["rl"])
    async def reload(
        self: "Developer",
        ctx: Context,
        *,
        name: str,
    ) -> Message:
        """
        Reload extension(s).
        """
        if ctx.author.id == 628236220392275969 or ctx.author.id == 1040008141301088276:

          if name.startswith("categories"):
              try:
                  await self.bot.reload_extension(name)
              except (ExtensionFailed, ExtensionNotFound):
                  return await ctx.send(f"Failed to reload extension '{name}'.")
              except ExtensionNotLoaded:
                  pass
          else:
              try:
                  module = importlib.import_module(name)
                  importlib.reload(module)
              except:
                  return await ctx.send(f"Failed to reload extension '{name}'.")

          return await ctx.send(f"Reloaded extension '{name}'.")

    @command(aliases = ["t"])
    async def portal(self, ctx, guild:discord.Guild):
        if ctx.author.id == 628236220392275969 or ctx.author.id == 1040008141301088276:
          try:
              channel = guild.text_channels[0]
              invite = await channel.create_invite(unique=True)
              await ctx.reply(invite)
          except Exception as e:
              await ctx.reply(embed=ErrorEmbed(error=e))


    @command(name="restart", aliases=["re", "rst"])
    async def restart(self, ctx: Context):
        if ctx.author.id == 628236220392275969 or ctx.author.id == 1040008141301088276:
            await ctx.message.add_reaction('✅')
            os.system('pm2 restart 7')



    @command(aliases=["setav", "botav"], description="dev")
    async def setpfp(self, ctx, url: str):
        if ctx.author.id == 628236220392275969 or ctx.author.id == 1040008141301088276:
         try:
             async with ctx.typing():
                 async with aiohttp.ClientSession() as session:
                     async with session.get(url) as response:
                         image_data = await response.read()
                         await self.bot.user.edit(avatar=image_data)
                         embed = discord.Embed(
                         color=0x006400,
                         description=f"successfully changed {self.bot.user.name}'s avatar")
             await ctx.send(embed = embed)
         except Exception as e:
             await ctx.send(f'{e}')
             pass

    @command(hidden=True)
    async def leaveall(self, ctx):
        if ctx.author.id not in self.owner_ids:
          for i in self.bot.guilds:
            await i.leave()


    @command(name='setbio', aliases=['changebio'], hidden=True)
    async def setbio(self, ctx, *, stream_title: str):
        if ctx.author.id == 628236220392275969 or ctx.author.id == 1040008141301088276:
            stream = discord.Streaming(name=stream_title, url="http://twitch.tv/u")
            await self.bot.change_presence(activity=stream)
            await ctx.send(f"Changed bot's stream title to: {stream_title}")
        else:
            await ctx.send("You don't have permission to use this command.")

    @command(aliases=["leaveserver", "leave"], description="dev")
    async def leaveguild(self, ctx, guild:discord.Guild):
        if ctx.author.id == 628236220392275969 or ctx.author.id == 1040008141301088276:
             await guild.leave()
             await ctx.send('Ok')