from typing import Type
from discord import VoiceChannel
from discord import Message
from discord.ext.commands import Cog, Context, command

from core import Slut


class vc(Cog, description=">.<"):
    def __init__(self, bot: Slut) -> None:
        self.bot: Slut = bot
        self.voice_client = None  # Define voice_client attribute in the __init__ method

    async def cog_check(self, ctx: Context):
        return await self.bot.is_owner(ctx.author)

    @command(name="join", description="Makes the bot join a voice channel or stage channel")
    async def join(self, ctx):
        if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel
            self.voice_client = await channel.connect()
            await ctx.send(f'Joined {channel.name}')
        else:
            await ctx.send('You need to be in a voice channel to use this command.')

    @command(name="disconnect", aliases=["dc"], description="Makes the bot leave the current voice channel or stage channel")
    async def disconnect(self, ctx):
        if self.voice_client and self.voice_client.is_connected() and self.voice_client.channel.id == ctx.author.voice.channel.id:
            await self.voice_client.disconnect()
            self.voice_client = None  # Reset the voice client instance
            await ctx.send('Left the voice channel.')
        else:
            await ctx.send('I am not in the correct voice channel.')

    # Optionally, you can add more commands or functions here.