from discord import Intents, Status, AllowedMentions
from discord.ext.commands import Bot, Cog

from .client.patch.help import HelpCommand


class Slut(Bot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            intents=Intents.all(),
            command_prefix=";",
            case_insensitive=True,
            owner_ids=[1148300105758298123],
            allowed_mentions=AllowedMentions(
                everyone=False,
                roles=False,
                users=True,
                replied_user=True,
            ),
            help_command=HelpCommand(),
            status=Status.invisible,
            *args,
            **kwargs
        )

        self.run(
            token="MTAyNDI1OTg3OTY5Njg1OTE0Ng.GufdVg.Ye4b-FFFQWg69e8tE4zSRJZHbYBu2WEIZ_vKEM", reconnect=True
        )
    
    async def on_ready(self: "Slut") -> None:
        await self.load_extension("jishaku")