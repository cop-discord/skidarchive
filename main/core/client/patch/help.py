from discord import Embed
from discord.ext.commands import MinimalHelpCommand


class HelpCommand(MinimalHelpCommand):
    def __init__(self: "HelpCommand", **options) -> None:
        super().__init__(
            command_attrs={
                "aliases": ["h"],
            },
            **options,
        )

    async def send_pages(self: "HelpCommand") -> None:
        _ = self.get_destination()

        await _.send(embed=Embed(description=self.paginator.pages[0]))