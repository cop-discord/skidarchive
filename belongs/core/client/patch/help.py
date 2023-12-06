from discord import Embed
from discord.ext.commands import MinimalHelpCommand, Command


class HelpCommand(MinimalHelpCommand):
    def __init__(self: "HelpCommand", **options) -> None:
        super().__init__(
            command_attrs={
                "hidden": True,
                "aliases": ["h"],
            },
            **options,
        )
    
    async def send_pages(self: "HelpCommand") -> None:
        _ = self.get_destination()

        for page in self.paginator.pages:
            await _.send(embed=Embed(description=page, color=0x2B2D31))