import discord, time, platform, asyncio, random
from discord.ext import commands 
from cogs.events import seconds_to_dhms, blacklist, commandhelp
from backend.classes import Emojis, Colors
from discord.ext.commands import Context
from discord.ui import View, Button, Select
import psutil
import platform

my_system = platform.uname()


class info(commands.Cog): 
    def __init__(self, bot: commands.AutoShardedBot): 
      self.bot = bot  

    @commands.hybrid_command(help="check the bot's latency", description="info")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist()
    async def ping(self, ctx: commands.Context):
        responses = ["discord.com", "use's servers", "north korea", "6ix9ines ankle monitor", "no one", "minecraft servers", "your mom", "your lost dad", "your wifi"]
        pings = format(round(self.bot.latency * 1000))
        embed1 = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading ping**")
        embed = discord.Embed(color=0x2B2D31, description=f"it took **{pings}ms** to ping **{random.choice(responses)}**")
        embed.set_footer(text="use", icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
        msg = await ctx.send(embed=embed1)
        await asyncio.sleep(0.5)
        await msg.edit(embed=embed)

    @commands.hybrid_command(help="check bot's statistics", aliases=["about", "bi", "info"], description="info")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist()
    async def botinfo(self, ctx):
        embed1 = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **getting informations from client**")
        msg = await ctx.reply(embed=embed1)
        lis = []
        for i in self.bot.owner_ids:
            user = await self.bot.fetch_user(i)
            lis.append(user.name)
        embed = discord.Embed(color=0x2B2D31, title=f"{self.bot.user.name} | About").set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.add_field(name="Founder", value=f"`Discord:` `{' '.join(l for l in lis)}`\n`Server:` [here](https://discord.gg/f7FTGEcC5r) & [backup](https://discord.gg/Ug5nuXSD68)", inline=False)
        button = discord.ui.Button(label="invite", style=discord.ButtonStyle.url, url="https://canary.discord.com/api/oauth2/authorize?client_id=1094942437820076083&permissions=41221484826111&scope=bot%20applications.commands")
        view = discord.ui.View()
        view.add_item(button)
        embed.add_field(name="Stats", value=f"`Users:` `{sum(g.member_count for g in self.bot.guilds)}`\n`Servers:` `{len(self.bot.guilds)}`", inline=False)
        embed.add_field(name="System:", value=f"`Latency:` `{round(self.bot.latency * 1000)}ms`\n`Language:` `Python`\n`System`: `{my_system.system}`\n`CPU Usage:` `{psutil.cpu_percent(interval=0.6)}%`\n`Memory Usage:` `{psutil.virtual_memory().percent}%`", inline=True)
        embed.add_field(name="Shard", value=f"`This ShardID:` `{ctx.guild.shard_id}`\n`ShardLatency:` `{self.bot.get_shard(ctx.guild.shard_id).latency} ms`", inline=False)
        embed.set_footer(text="use", icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
        await msg.edit(embed=embed, view=view)##      embed.add_field(name="System:", value=f"`Latency:` `{round(self.bot.latency * 1000)}ms`\n`Language:` `Python`\n`System`: `{my_system.system}`\n`CPU Usage:` `{psutil.cpu_percent(interval=0.6)}%`\n`Memory Usage:` `{psutil.virtual_memory().percent}%`", inline=True)
    
    @commands.hybrid_command(help="invite the bot in your server", aliases=["inv"], description="info")
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist()
    async def invite(self, ctx):
        embed = discord.Embed(color=0x2B2D31, description=f"invite **{self.bot.user.name}** in your server")
        embed.set_footer(text="use", icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
        button = discord.ui.Button(label="invite", style=discord.ButtonStyle.url, url="https://discord.com/api/oauth2/authorize?client_id=1094942437820076083&permissions=8&scope=bot")
        button2 = discord.ui.Button(label="support", style=discord.ButtonStyle.url, url="https://discord.gg/f7FTGEcC5r")
        view = discord.ui.View()
        view.add_item(button)
        view.add_item(button2)
        await ctx.reply(embed=embed, view=view, mention_author=True)   
        
    @commands.hybrid_command(help="check bot's commands", aliases=["h", "cmd", "cmds", "commands", "command"], usage="<command name>", description="info")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist()
    async def help(self, ctx: commands.Context, *, command=None):
        if command is not None: return await commandhelp(self, ctx, command) 
        options = [
            discord.SelectOption(
                label="home",
                description="go back to the home menu",
                emoji="<:home:1096525140935835748>",
            ),
            discord.SelectOption(
                label="info",
                description="information commands",
                emoji="<:info:1096526336639647795>",
            ),
            discord.SelectOption(
              label="lastfm",
              description="last fm commands",
              emoji="<:tvmusic1:1097229817994297435>",
            ),
            discord.SelectOption(
             label="moderation",
             description="moderation commands",
             emoji="<:hammer:1097231050859610182>",
            ),
            discord.SelectOption(
              label="welcome",
              description="welcome commands",
              emoji="<:handwave:1112410034366861312>",
            ),
            discord.SelectOption(
              label="joindm",
              description="joindm commands",
              emoji="<:handspock:1112410328957997218>",
            ),
            discord.SelectOption(
              label="goodbye",
              description="goodbye commands",
              emoji="<:arrowright:1113906058541408316>",
            ),
            discord.SelectOption(
              label="boost",
              description="boost commands",
              emoji="<:boost:1113905264920383628>",
            ),
            discord.SelectOption(
              label="voice",
              description="voice commands",
              emoji="<:phonecross:1112409479145848962>",
            ),
            discord.SelectOption(
              label="reactionrole",
              description="reactionrole commands",
              emoji="<:diced6:1112411005771849858>",
            ),
            discord.SelectOption(
              label="utility",
              description="utility commands",
              emoji="<:settings:1112411593511280700>",
            ),
            discord.SelectOption(
              label="music",
              description="music commands",
              emoji="<:waveformpath:1119292561631227945>",
            ),
            discord.SelectOption(
              label="emoji",
              description="emoji commands",
              emoji="<:smile1:1097233234976317631>",
            ),
            discord.SelectOption(
                label="autopost",
                description="autopost commands",
                emoji="<:photo:1112412257343778890>",
            ),
            discord.SelectOption(
                label="fun",
                description="fun commands",
                emoji="<:kite:1112412535451295805>",
            ),
             discord.SelectOption(
                label="roleplay",
                description="roleplay commands",
                emoji="<:theatermasks:1112412789848416327>",
            ),
            discord.SelectOption(
                label="dev",
                description="dev commands",
                emoji="<:1081672767260336208:1102986585147973663>",
            )
        ]
        embed = discord.Embed(color=0x2B2D31, title=" ", description=" ").set_author(name=self.bot.user.name, icon_url=self.bot.user.display_avatar.url).set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.add_field(name="help", value="use the dropdown menu below to see commands", inline=False)
        embed.add_field(name="support", value="if u stuck using bot join our [support server](https://discord.gg/f7FTGEcC5r)", inline=False)
        embed.add_field(name=" ", value="```\n() - required\n<> - argument\n```", inline=False)
        embed.set_footer(text=f"{len(set(self.bot.walk_commands()))} commands", icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
        select = discord.ui.Select(placeholder="select category", options=options)

        async def select_callback(interaction: discord.Interaction):
          if interaction.user != ctx.author: 
            embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {interaction.user.mention}: This is not your message")
            await interaction.response.send_message(embed=embed, view=None, ephemeral=True) 
            return 
          if select.values[0] == "home":
            embed = discord.Embed(color=0x2B2D31, title=" ", description=" ").set_author(name=self.bot.user.name, icon_url=self.bot.user.display_avatar.url).set_thumbnail(url=self.bot.user.display_avatar.url)
            embed.add_field(name="help", value="use the dropdown menu below to see commands", inline=False)
            embed.add_field(name="support", value="if u stuck using bot join our [support server](https://discord.gg/f7FTGEcC5r)", inline=False)
            embed.add_field(name=" ", value="```\n() - required\n<> - argument\n```", inline=False)
            embed.set_footer(text=f"{len(set(self.bot.walk_commands()))} commands")
            await interaction.response.edit_message(embed=embed)   
          else:
            cmds = []
            em = discord.Embed(color=0x2B2D31, description=f"{select.values[0]} commands\n<> - optional argument\n[] - required argument").set_thumbnail(url=self.bot.user.display_avatar.url)
            for cmd in set(self.bot.walk_commands()): 
             if cmd.description == select.values[0]: 
              if cmd.parent is not None: cmds.append(str(cmd.parent) + " " + cmd.name)
              else: cmds.append(cmd.name)
            em.add_field(name="commands", value=", ".join(f"`{c}`" for c in cmds) , inline=False) 
            await interaction.response.edit_message(embed=em) 
                        
        select.callback = select_callback 

        view = discord.ui.View()
        view.add_item(select)
        await ctx.reply(embed=embed, view=view)  
        
    @commands.hybrid_command(aliases=["cs"])
    async def clearsnipe(self, ctx):
        lis = ["snipe"]
        for l in lis:
         async with self.bot.db.cursor() as cursor:
             await cursor.execute(f"DELETE FROM {l}")
             await self.bot.db.commit()
             await ctx.send(embed=discord.Embed(color=Colors.default, description=f"cleared all snipes"))

async def setup(bot):
    await bot.add_cog(info(bot))      
