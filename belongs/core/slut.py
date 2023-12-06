import os, discord
from typing import List, Optional
from os import environ

from discord import (
    Intents,
    Status,
    AllowedMentions,
    Message,
)
from discord.ext.commands import (
    Bot,
    when_mentioned_or,
    Context,
    CommandError,
)

from .client import HelpCommand, logging
import config

log = logging.getLogger(__name__)
environ["JISHAKU_HIDE"] = "True"
environ["JISHAKU_RETAIN"] = "True"
environ["JISHAKU_NO_UNDERSCORE"] = "True"
environ["JISHAKU_SHELL_NO_DM_TRACEBACK"] = "True"



class Slut(Bot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            owner_ids=config.owner_ids,
            intents=Intents.all(),
            command_prefix=self.get_prefix,
            help_command=None,
            case_insensitive=True,
            strip_after_prefix=True,
            allowed_mentions=AllowedMentions(
                replied_user=False,
                everyone=False,
                roles=False,
                users=True,
            ),
            status=Status.invisible,
            description=">w<",
            *args,
            **kwargs,
        )

        self.channel_cd = discord.ext.commands.CooldownMapping.from_cooldown(3, 3, discord.ext.commands.BucketType.channel)
        self.user_cd = discord.ext.commands.CooldownMapping.from_cooldown(3, 3, discord.ext.commands.BucketType.user)
        self.run(token=config.token)

    async def get_prefix(self: "Slut", message: Message) -> List[str]:
        return when_mentioned_or(",")(self, message)

    
    def channel_cooldown(self, message: Message) -> Optional[int]:
        bucket = self.channel_cd.get_bucket(message)
        return bucket.update_rate_limit()
    
    def user_cooldown(self, message: Message) -> Optional[int]:
        bucket = self.user_cd.get_bucket(message)
        return bucket.update_rate_limit()

    def cooldown(self, message: Message) -> bool:
        if self.channel_cooldown(message) or self.user_cooldown(message):
            return True
        return False

    async def load_cogs(self: "Slut"):
        """Load cogs from the 'categories' folder and its subfolders."""
        print("Loading cogs...")
        for category_folder in os.listdir("./categories"):
            category_path = os.path.join("./categories", category_folder)
            if os.path.isdir(category_path):
                for file in os.listdir(category_path):
                    if file.endswith(".py"):
                        cog_name = f"categories.{category_folder}.{file[:-3]}"
                        try:
                            await self.load_extension(cog_name)  # Await load_extension
                            print(f"Loaded cog: {cog_name}")
                        except Exception as e:
                            print(f"Failed to load cog {cog_name}: {e}")

    async def on_connect(self) -> None:
        await self.load_cogs()  # Properly await the load_cogs method


    async def on_ready(self: "Slut") -> None:
        await self.change_presence(status=discord.Status.online, activity=discord.Activity(
                ##type=discord.ActivityType.custom,
                ## state="tear.lol/discord",
                name="discord.gg/belongs",
                url="https://twitch.tv/belongs",
                type=discord.ActivityType.streaming,
            ),
        )
        log.info("yea")
        await self.load_extension("jishaku")