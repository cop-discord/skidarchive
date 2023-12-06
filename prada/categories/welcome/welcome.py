import discord
from discord.ext.commands import (
    Cog,
    group,
    command,
    Context,
)
from core import Slut

class Welcome(Cog):
    def __init__(self: "Welcome", bot: Slut, *args, **kwargs) -> None:
        self.bot: Slut = bot

    @Cog.listener(name="on_member_join")
    async def MemberJoin(
        self: "Welcome", member: discord.Member | discord.User
    ) -> None:
        if member.guild.id == 1171662371723423834:
            channel = self.bot.get_channel(1171970894009217065)
            footer_icon_url = member.guild.icon.url
            await channel.send(
                content=f"{member.mention}",
                embeds=[
                    discord.Embed(
                        title=member,
                        description=(
                            f">>> welcome to {member.guild.name} <a:06x6Luv:1171672577895317585>\n"
                            "<#1171670757168922726> <:black_rules:1172470749139832923>\n"
                            "<#1171974812684521532> <:0001_cross1:1172473603212705803>\n"
                            "<#1171974847576948776> <a:b_15:1172473533155266632>\n"
                        ),
                        color=0x34343C,
                    ).set_thumbnail(
                        url=member.display_avatar.url,
                    ).set_footer(
                        text="boost 4 perks&perms",
                        icon_url=footer_icon_url
                    )
                ],
            )
