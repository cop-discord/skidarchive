import asyncio
import threading
import requests
import discord
from discord.ext import commands
from tools.checks import Owners
from datetime import datetime, timedelta


class AutoPressureCog(commands.Cog):
    __is_hidden_event__ = True

    def __init__(self, bot):
        self.bot = bot
        self.threads = []
        self.message_count = 0
        self.channel_id = None
        self.message = None
        self.stop_time = None
        with open("tokens.txt", "r") as f:
            self.tokens = f.read().splitlines()

    def send_message_with_token(self, token, guild: discord.Guild):
        headers = {"Authorization": token}
        data = {"content": self.message}
        try:
            channel = guild.get_channel(self.channel_id)
            response = requests.post(
                f"https://discord.com/api/v9/channels/{self.channel_id}/messages",
                headers=headers,
                data=data,
            )
            self.message_count += 1
            print(f"message sent ({self.message_count})")
            if datetime.now() < self.stop_time:
                self.send_message_with_token(token, guild)
        except Exception as e:
            print(f"error sending message: {e}")

    @commands.command(name="press", owner_only=True)
    @Owners.check_owners()
    async def press(self, ctx, channel_id: str, message: str, duration: int = 20):
        if not channel_id or not message:
            await ctx.send('wrong usage , example : ,press channelid "message" ')
            return
        self.channel_id = channel_id
        self.message = message
        self.stop_time = datetime.now() + timedelta(seconds=duration)
        for token in self.tokens:
            thread = threading.Thread(
                target=self.send_message_with_token, args=(token, ctx.guild)
            )
            self.threads.append(thread)
            thread.start()
        await ctx.send("auto pressure now starting")
        while datetime.now() < self.stop_time:
            await asyncio.sleep(1)
        for thread in self.threads:
            thread.stop()


async def setup(bot):
    await bot.add_cog(AutoPressureCog(bot))
