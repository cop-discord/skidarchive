import discord, time, platform, asyncio, random
from discord.ext import commands 
from cogs.events import seconds_to_dhms, blacklist, commandhelp
from backend.classes import Emojis, Colors
from discord.ext.commands import Context
import psutil
import platform

my_system = platform.uname()


class info(commands.Cog): 
    def __init__(self, bot: commands.AutoShardedBot): 
      self.bot = bot  

    @commands.hybrid_command(help="check the bot's latency", description="info")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist()
    async def ping(ctx):
        message = await ctx.send("Pinging...")

        websocket_latency = rh.latency * 1000

        api_url = "https://discord.com/api/v10/gateway"
        start_time = time.time()
        try:
        response = requests.get(api_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to measure API latency: {str(e)}")
        rest_latency = None
    else:
        end_time = time.time()
        rest_latency = (end_time - start_time) * 1000

    if rest_latency is not None:
        await message.edit(content=f"Latency: `{websocket_latency:.2f}ms` (edit: `{rest_latency:.2f}ms`)")
    else:
        await message.edit(content=f"Latency: {websocket_latency:.2f} ms (edit: REST LATENCY measurement failed)")
    @commands.hybrid_command(help="check the bot's uptime", description="info")
    @commands.cooldown(1, 3, commands.BucketType.user)  
    @blacklist()
    async def uptime(self, ctx: commands.Context):  
     uptime = int(time.time() - self.bot.uptime)
     e = discord.Embed(color=0x2f3136, description=f"⏰ **{self.bot.user.name}'s** uptime: **{seconds_to_dhms(uptime)}**")
     await ctx.reply(embed=e, mention_author=False) 

    @commands.hybrid_command(help="check bot's statistics", description="info")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist()
    async def botinfo(self, ctx: commands.Context):
        embed = discord.Embed(color=Colors.default, description=f"> {self.bot.user.name} is a multipurpose bot around **{len(self.bot.guilds)}** servers")
        embed.add_field(name="Stats", value=f">>> Memory: {psutil.virtual_memory()[2]}%\nVersion: Discord.py {discord.__version__}\nPing: {round(self.bot.latency * 1000)}ms\nMembers: {sum(g.member_count for g in self.bot.guilds):,}") 
        await ctx.reply(embed=embed, mention_author=False)

    @commands.hybrid_command(help="invite the bot in your server", aliases=["inv"], description="info")
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist()
    async def invite(self, ctx):
        view = discord.ui.View()
        inv = discord.ui.Button(
        label="Invite",
          url="https://discord.com/api/oauth2/authorize?client_id=624987392494796820&permissions=8&scope=bot"
    )
    

        sup = discord.ui.Button(
        label="Support",
        url="https://discord.gg/abkkQJyUDQ"
       )
    
        view.add_item(inv)
        view.add_item(sup)
    
        await ctx.reply(view=view, mention_author=False)

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
              label="vanity",
              description="vanity commands",
              emoji="<:linkalt:1112410666175832126>",
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
        await ctx.reply(embed=embed, view=view, mention_author=False)  

async def setup(bot):
    await bot.add_cog(info(bot))      
