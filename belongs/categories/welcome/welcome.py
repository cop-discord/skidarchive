import discord
from discord.ext.commands import (
    Cog,
    group,
    command,
    Context,
)
from discord.webhook import Webhook
from core import Slut


class Welcome(Cog):
    def __init__(self: "Welcome", bot: Slut, *args, **kwargs) -> None:
        self.bot: Margiela = bot


    @Cog.listener(name="on_member_join")
    async def MemberJoin(
        self: "Welcome", member: discord.Member | discord.User
    ) -> None:
        guild = member.guild
        channel = self.bot.get_channel(1169428737088028732)
        await channel.send(
            content=f"{member.mention}",
            embeds=[
                discord.Embed(
                    title=member,
                    description=(
                        f"<a:blackbat:1169441733558423652> welcome to {guild.name} <a:blackbat:1169441733558423652>\n"
                        "<:1_:1169441813480874065> Boost, inv & rep for perks <:1_:1169441813480874065>\n"
                        "<a:emoji_317:1169441861048471702> main vc’s for higher roles <a:emoji_317:1169441861048471702>\n"
                        "<:12knifs:1145534514781761556> join https://discord.gg/belongs <:12knifs:1145534514781761556>"
                    ),
                    color=0x34343C,
                ).set_thumbnail(
                    url=member.display_avatar.url,
                )
            ],
        )