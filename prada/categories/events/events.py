import discord, aiohttp
from discord.ext import commands

class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.webhook_url = 'https://discord.com/api/webhooks/1172847688396574720/26JgpF03FrOt2-VP1V0AeEZK78c4ohpWesJm_fzO28BOUJK2IOH3mLyPzTBvy32ELZd5'
        self.session = aiohttp.ClientSession()


    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(
            description=f"`{ctx.command.name}` was successfully invoked by `{ctx.author.name}` in `{guild.name}` (`{guild.id}`)",
            color=0x2f3136
        )
        embed.set_footer(text=f"{guild.member_count} members")
        print(f'{ctx.command.name} was successfully invoked by {ctx.author.name} in {guild.name} ({guild.id})')
        async with self.session.post(self.webhook_url, json={"embeds": [embed.to_dict()]}):
            pass



    @commands.Cog.listener(name="on_member_join")
    async def MemberJoin(
        self: "Welcome", member: discord.Member | discord.User
    ) -> None:
        if member.guild.id == 1172580235481456660:
            channel = self.bot.get_channel(1173322314050445383)
            footer_icon_url = member.guild.icon.url
            await channel.send(
                content=f"{member.mention}",
                embeds=[
                    discord.Embed(
                        title="welcome to {member.guild.name} <a:blackbat:1096922843264065567>",
                        description=f
                            f">>> welcome {member}"
                            "rep /belongs <:CH_IconBoostStar:1110120367768489994>"
                            "main with friends & vc <:Star:1170223769319649280>" 
                            "boost for roles and perks <:Star:1170223769319649280>"
                        ),
                        color=0x34343C,
                    ).set_thumbnail(
                        url=member.display_avatar.url,
                    ).set_footer(
                        text="we now have {member_count} members !",
                        icon_url=footer_icon_url
                    )
                ],
            )
