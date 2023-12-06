import discord, requests, json, aiohttp, random, asyncio
from discord import app_commands
from discord import Member
from discord.ext import commands
from backend.classes import Colors, Emojis
from cogs.events import commandhelp, blacklist
from discord.ext.commands import Context


class roleplay(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(help="cuddle with someone", usage="[member]", description="roleplay")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist()
    async def cuddle(self, ctx, user: discord.Member=None):
        if user is None:
            embed=discord.Embed(color=Colors.default, title="", description="`syntax: cuddle [member]`")
            await ctx.send(embed=embed, mention_author=True)
        else:
            r = requests.get("http://api.nekos.fun:8080/api/cuddle")
            res = r.json()
            em = discord.Embed(color=Colors.default, description=f"*aww how cute! {ctx.author.mention} is cuddling with {user.mention}*")
            em.set_image(url=res['image'])
            await ctx.reply(embed=em, mention_author=True)
          
    @commands.hybrid_command(help="slap someone", usage="[member]", description="roleplay")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist()
    async def slap(self, ctx, user: discord.Member=None):
        if user is None:
            embed=discord.Embed(color=Colors.default, title="", description="`syntax: slap [member]`")
            await ctx.send(embed=embed, mention_author=True)
        else:
            r = requests.get("http://api.nekos.fun:8080/api/slap")
            res = r.json()
            em = discord.Embed(color=Colors.default, description=f"*{ctx.author.mention} slapped {user.mention}*")
            em.set_image(url=res['image'])
            await ctx.reply(embed=em, mention_author=True)

    @commands.hybrid_command(help="pat someone", usage="[member]", description="roleplay")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist()
    async def pat(self, ctx, user: discord.Member=None):
        if user is None:
            embed=discord.Embed(color=Colors.default, title="", description="`syntax: pat [member]`")
            await ctx.send(embed=embed, mention_author=True)
        else:
            r = requests.get("http://api.nekos.fun:8080/api/pat")
            res = r.json()
            em = discord.Embed(color=Colors.default, description=f"*aww how cute! {ctx.author.mention} pat {user.mention}*")
            em.set_image(url=res['image'])
            await ctx.reply(embed=em, mention_author=True)

    @commands.hybrid_command(help="hug someone", usage="[member]", description="roleplay")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist()
    async def hug(self, ctx, user: discord.Member=None):
        if user is None:
            embed=discord.Embed(color=Colors.default, title="", description="`syntax: hug [member]`")
            await ctx.send(embed=embed, mention_author=True)
        else:
            r = requests.get("http://api.nekos.fun:8080/api/hug")
            res = r.json()
            em = discord.Embed(color=Colors.default, description=f"*aww how cute! {ctx.author.mention} hugged {user.mention}*")
            em.set_image(url=res['image'])
            await ctx.reply(embed=em, mention_author=True)

    @commands.hybrid_command(help="kiss someone", usage="[member]", description="roleplay")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist()
    async def kiss(self, ctx, user: discord.Member=None):
        if user is None:
            embed=discord.Embed(color=Colors.default, title="", description="`syntax: kiss [member]`")
            await ctx.send(embed=embed, mention_author=True)
        else:
            r = requests.get("http://api.nekos.fun:8080/api/kiss")
            res = r.json()
            em = discord.Embed(color=Colors.default, description=f"*aww how cute! {ctx.author.mention} kissed {user.mention}*")
            em.set_image(url=res['image'])
            await ctx.reply(embed=em, mention_author=True)

    @commands.hybrid_command(help="feed someone?....", usage="[member]", description="roleplay")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist()
    async def feed(self, ctx, user: discord.Member=None):
        if user is None:
            embed=discord.Embed(color=Colors.default, title="", description="`syntax: feed [member]`")
            await ctx.send(embed=embed, mention_author=True)
        else:
            r = requests.get("http://api.nekos.fun:8080/api/feed")
            res = r.json()
            em = discord.Embed(color=Colors.default, description=f"*aww how cute! {ctx.author.mention} is feeding {user.mention}*")
            em.set_image(url=res['image'])
            await ctx.reply(embed=em, mention_author=True)

    @commands.hybrid_command(help="tickle someone", usage="[member]", description="roleplay")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist()
    async def tickle(self, ctx, user: discord.Member=None):
        if user is None:
            embed=discord.Embed(color=Colors.default, title="", description="`syntax: tickle [member]`")
            await ctx.send(embed=embed)
        else:
            r = requests.get("http://api.nekos.fun:8080/api/tickle")
            res = r.json()
            em = discord.Embed(color=Colors.default, description=f"*aw! look at the flirts! {ctx.author.mention} is tickling {user.mention}*")
            em.set_image(url=res['image'])
            await ctx.reply(embed=em, mention_author=True)

    @commands.hybrid_command(help="cry", description="roleplay", usage="[member]")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist()
    async def cry(self, ctx, user: discord.Member=None):
        if user is None:
            embed=discord.Embed(color=Colors.default, title="", description="`syntax: cry [member]`")
            await ctx.send(embed=embed)
        else:
            r = requests.get("http://api.nekos.fun:8080/api/cry")
            res = r.json()
            em = discord.Embed(color=Colors.default, description=f"*aww! {ctx.author.mention} is crying")
            em.set_image(url=res['image'])
            await ctx.reply(embed=em, mention_author=True)

    @commands.hybrid_command(help="funny", description="roleplay", usage="[member]")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist()
    async def laugh(self, ctx, user: discord.Member=None):
        if user is None:
            embed=discord.Embed(color=Colors.default, title="", description="`syntax: laugh [member]`")
            await ctx.send(embed=embed)
        else:
            r = requests.get("http://api.nekos.fun:8080/api/laugh")
            res = r.json()
            em = discord.Embed(color=Colors.default)
            em.set_image(url=res['image'])
            await ctx.reply(embed=em, mention_author=True)

    @commands.hybrid_command(help="senpai notice meeeee!", usage="[member]", description="roleplay")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist()
    async def poke(self, ctx, user: discord.Member=None):
        if user is None:
            embed=discord.Embed(color=Colors.default, title="", description="`syntax: poke [member]`")
            await ctx.send(embed=embed)
        else:
            r = requests.get("http://api.nekos.fun:8080/api/poke")
            res = r.json()
            em = discord.Embed(color=Colors.default, description=f"*aw how cute! {ctx.author.mention} is poking {user.mention}!*")
            em.set_image(url=res['image'])
            await ctx.reply(embed=em, mention_author=True)

    @commands.hybrid_command(help="b-baka!!!", description="roleplay", usage="[member]")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist()
    async def baka(self, ctx, user: discord.Member=None):
        if user is None:
            embed=discord.Embed(color=Colors.default, title="", description="`syntax: baka [member]`")
            await ctx.send(embed=embed)
        else:
            r = requests.get("http://api.nekos.fun:8080/api/baka")
            res = r.json()
            em = discord.Embed(color=Colors.default)
            em.set_image(url=res['image'])
            await ctx.reply(embed=em, mention_author=True)
  
async def setup(bot):
    await bot.add_cog(roleplay(bot))