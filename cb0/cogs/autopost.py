import discord, aiohttp, datetime, random, random, asyncio, traceback
from discord.ext import commands, tasks 
from cogs.events import commandhelp, blacklist
from io import BytesIO
from backend.classes import Colors, Emojis
from discord.ext.commands import Context
from discord.ui import View, Button, Select
from typing import Union
import typing


class autopost(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
  
    @commands.Cog.listener()
    async def on_ready(self):
      async with self.bot.db.cursor() as cursor: 
        await cursor.execute("CREATE TABLE IF NOT EXISTS female (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS male (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS anime (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS banner (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS random (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS fgifs (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS mgifs (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS agifs (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS automeme (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS match (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS autocar (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS guns (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS faceless (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS autobody (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS autoshoes (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS jewellry (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS aesthetic (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS cartoon (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS drill (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS hellokitty (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS money (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS smoking (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS animals (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS soft (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS quote (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS couplesgif (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS couplespfp (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS kpop (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS edgy (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS besties (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS core (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS nike (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS autonsfw (guild_id INTEGER, channel_id INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS hentai (guild_id INTEGER, channel_id INTEGER)")
      await self.bot.db.commit() 

    @commands.hybrid_group(invoke_without_command=True) 
    @blacklist()
    async def autopost(self, ctx):
       pass

    @autopost.command(aliases=["genre", "help", "list"], description="autopost")
    @blacklist()
    async def genres(self, ctx):
       embed = discord.Embed(color=0x2B2D31, title="autopfp genres", description="")
       embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
       embed.add_field(name="genres", value="*autopfp*\n> female\n> male\n> anime\n> random\n**autogif**\n> female\n> male\n> anime", inline=True)
       embed.add_field(name="examples", value="> `autopfp add female #pfps`\n> `autogif remove female #pfps`", inline=True)   
       embed.add_field(name="extrapost genres", value="> sets\n> cars\n> guns\n> faceless\n> body\n> shoes\n> jewellry\n> aesthetic\n> cartoon\n> drill\n> hellokitty\n> money\n> smoking\n> soft\n> animals\n> besties\n> couples/pfp/gif\n> kpop\n> edgy\n> core\n> nike", inline=True)
       embed.add_field(name="extrapost examples", value="> `extrapost add guns #guns`", inline=True)   
       embed.add_field(name="autonsfw genres", value="> porn\n> hentai", inline=True)
       embed.add_field(name="autonsfw examples", value="> `autonsfw add porn #porn`", inline=True)
       await ctx.reply(embed=embed, mention_author=True, delete_after=50) 

    @autopost.command(aliases=["channel"], description="autopfp")
    @blacklist()
    async def channels(self, ctx):
      k = 0
      async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM female WHERE guild_id = {}".format(ctx.guild.id))
        female = await cursor.fetchone()
        await cursor.execute("SELECT * FROM male WHERE guild_id = {}".format(ctx.guild.id))
        male = await cursor.fetchone()
        await cursor.execute("SELECT * FROM anime WHERE guild_id = {}".format(ctx.guild.id))
        anime = await cursor.fetchone()
        await cursor.execute("SELECT * FROM random WHERE guild_id = {}".format(ctx.guild.id))
        random = await cursor.fetchone()        
        await cursor.execute("SELECT * FROM fgifs WHERE guild_id = {}".format(ctx.guild.id))
        fgifs = await cursor.fetchone()        
        await cursor.execute("SELECT * FROM mgifs WHERE guild_id = {}".format(ctx.guild.id))
        mgifs = await cursor.fetchone()        
        await cursor.execute("SELECT * FROM agifs WHERE guild_id = {}".format(ctx.guild.id))
        agifs = await cursor.fetchone()        
        await cursor.execute("SELECT * FROM banner WHERE guild_id = {}".format(ctx.guild.id))
        autobanner = await cursor.fetchone()        
        await cursor.execute("SELECT * FROM automeme WHERE guild_id = {}".format(ctx.guild.id))
        automeme = await cursor.fetchone()        
        await cursor.execute("SELECT * FROM autonsfw WHERE guild_id = {}".format(ctx.guild.id))
        autonsfw = await cursor.fetchone()
        if female is not None:
            female_id = f"<#{female[1]}>"
            k = k +1
        elif female is None:
            female_id = "not set"
        if male is not None:
            male_id = f"<#{male[1]}>"
            k = k +1
        elif male is None:
            male_id = "not set"
        if anime is not None:
            anime_id = f"<#{anime[1]}>"
            k = k +1
        elif anime is None:
            anime_id = "not set"
        if random is not None:
            random_id = f"<#{random[1]}>"
            k = k +1
        elif random is None:
            random_id = "not set"
        if fgifs is not None:
            fgifs_id = f"<#{fgifs[1]}>"
            k = k +1
        elif fgifs is None:
            fgifs_id = "not set"
        if mgifs is not None:
            mgifs_id = f"<#{mgifs[1]}>"
            k = k +1
        elif mgifs is None:
            mgifs_id = "not set"
        if agifs is not None:
            agifs_id = f"<#{agifs[1]}>"
            k = k +1
        elif agifs is None:
            agifs_id = "not set"
        if autobanner is not None:
            autobanner_id = f"<#{autobanner[1]}>"
            k = k +1
        elif autobanner is None:
            autobanner_id = "not set"
        if automeme is not None:
            automeme_id = f"<#{automeme[1]}>"
            k = k +1
        elif automeme is None:
            automeme_id = "not set"
        if autonsfw is not None:
            autonsfw_id = f"<#{autonsfw[1]}>"
            k = k +1
        elif autonsfw is None:
            autonsfw_id = "not set"
        embed = discord.Embed(color=0x2B2D31, title="autopost channels")
        embed.add_field(name="autopfp", value=f"**female** {female_id}\n**male** {male_id}\n**anime** {anime_id}\n**random** {random_id}", inline=False)
        embed.add_field(name="autogif", value=f"**female** {fgifs_id}\n**male** {mgifs_id}\n**anime** {agifs_id}", inline=False)
        embed.add_field(name="extra", value=f"**banners** {autobanner_id}\n**memes** {automeme_id}\n**nsfw** {autonsfw_id}", inline=False)
        embed.set_footer(text=f"{k}/10 channels set", icon_url="https://cdn.discordapp.com/emojis/1043225723739058317.gif?size=96&quality=lossless")
        embed.set_thumbnail(url=ctx.guild.icon.url)
        await ctx.reply(embed=embed, mention_author=False, delete_after=11) 
        return

    @commands.hybrid_command(help="adds autopfp module for your server", description="autopost", brief="> autopfp add [genre] [channel] - adds your autopfp channel\n> autopfp remove [genre] - removes your autopfp channel")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist()
    async def autopfp(self, ctx: commands.Context, decide: str=None, genre: str=None, channel: Union[discord.TextChannel, discord.ForumChannel, discord.Thread] = None):
      if not ctx.author.guild_permissions.manage_guild:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} you are missing permissions `manage_guild`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        return 
      if decide == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: autopfp add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return
      if decide == "add" and genre == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: autopfp add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return
      if decide == "remove" and genre == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: autopfp add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return
      if decide == "add" and genre == "female" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: autopfp add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      if decide == "add" and genre == "male" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: autopfp add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      if decide == "add" and genre == "anime" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: autopfp add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      if decide == "add" and genre == "random" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: autopfp add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return
      elif decide == "add" and genre == "female" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM female WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO female VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(ctx.guild.get_channel_or_thread(channel.id).id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending female icons to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add autopfp channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add autopfp channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting female icons for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "female":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM female WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} autopfps for female icons isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM female WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} autopfps for female icons removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
      elif decide == "add" and genre == "male" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM male WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO male VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(ctx.guild.get_channel_or_thread(channel.id).id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending male icons to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add autopfp channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add autopfp channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting male icons for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "male":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM male WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} autopfps for male icons isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM male WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} autopfps for male icons removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
      elif decide == "add" and genre == "anime" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM anime WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO anime VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending anime icons to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add autopfp channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add autopfp channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting anime icons for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "anime":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM anime WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} autopfps for anime icons isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM anime WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} autopfps for anime icons removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
      elif decide == "add" and genre == "random" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM random WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO random VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending random icons to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add autopfp channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add autopfp channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting random icons for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "random":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM random WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} autopfps for random icons isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM random WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} autopfps for random icons removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return

    @commands.hybrid_command(aliases=["autogifs"], help="adds autogif module for your server", description="autopost", brief="> autogif add [genre] [channel] - adds your autogif channel\n> autopfp remove [genre] - removes your autogif channel")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist()
    async def autogif(self, ctx: commands.Context, decide: str=None, genre: str=None, channel: Union[discord.TextChannel, discord.ForumChannel, discord.Thread] = None):
      if not ctx.author.guild_permissions.manage_guild:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} you are missing permissions `manage_guild`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        return 
      if decide == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: autogif add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      if decide == "add" and genre == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: autopfp add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return
      if decide == "remove" and genre == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: autopfp add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return
      if decide == "add" and genre == "female" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: autogif add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      if decide == "add" and genre == "male" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: autogif add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      if decide == "add" and genre == "anime" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: autogif add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      elif decide == "add" and genre == "female" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM fgifs WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO fgifs VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending female gifs to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add autogif channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add autogif channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting female gifs for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "female":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM fgifs WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} autogifs for female gifs isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM fgifs WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} autogifs for female gifs removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
      elif decide == "add" and genre == "male" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM mgifs WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO mgifs VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending male gifs to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add autogif channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add autogif channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting male gifs for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "male":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM mgifs WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} autogifs for male gifs isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM mgifs WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} autogifs for male gifs removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
      elif decide == "add" and genre == "anime" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM agifs WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO agifs VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending anime gifs to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add autogif channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add autogif channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting anime gifs for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "anime":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM agifs WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} autogifs for anime gifs isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM agifs WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} autogifs for anime gifs removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return

    @commands.hybrid_command(aliases=["autoextra", "extra"], help="adds autogif module for your server", description="autopost", brief="> autogif add [genre] [channel] - adds your autogif channel\n> autopfp remove [genre] - removes your autogif channel")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist()
    async def extrapost(self, ctx: commands.Context, decide: str = None, genre: str = None, channel: Union[discord.TextChannel, discord.ForumChannel, discord.Thread] = None):
      if not ctx.author.guild_permissions.manage_guild:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} you are missing permissions `manage_guild`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        return 
      if decide == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: extrapost add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      if decide == "add" and genre == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: extrapost add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return
      if decide == "remove" and genre == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: extrapost add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return
      if decide == "add" and genre == "sets" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: extrapost add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      if decide == "add" and genre == "cars" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: extrapost add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      if decide == "add" and genre == "guns" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: extrapost add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      if decide == "add" and genre == "faceless" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: extrapost add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      if decide == "add" and genre == "body" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: extrapost add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      if decide == "add" and genre == "shoes" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: extrapost add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      if decide == "add" and genre == "jewellry" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: extrapost add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      if decide == "add" and genre == "aesthetic" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: extrapost add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return
      if decide == "add" and genre == "cartoon" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: extrapost add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      if decide == "add" and genre == "drill" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: extrapost add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      if decide == "add" and genre == "hellokitty" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: extrapost add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return
      if decide == "add" and genre == "money" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: extrapost add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      if decide == "add" and genre == "smoking" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: extrapost add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      if decide == "add" and genre == "soft" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: extrapost add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      if decide == "add" and genre == "animals" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: extrapost add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      if decide == "add" and genre == "couplesgif" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: extrapost add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      if decide == "add" and genre == "couplespfp" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: extrapost add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      if decide == "add" and genre == "besties" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: extrapost add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      if decide == "add" and genre == "kpop" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: extrapost add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      if decide == "add" and genre == "nike" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: extrapost add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      elif decide == "add" and genre == "sets" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM match WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO match VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending match pfps & gifs to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add sets channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add sets channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting match pfps for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "sets":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM match WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} autopost for sets isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM match WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} autopost for sets is removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
      elif decide == "add" and genre == "cars" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM autocar WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO autocar VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending car pfp & gifs to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add car channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add car channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting car pfps & gifs for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "cars":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM autocar WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} autopost for cars isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM autocar WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} autopost for cars is  removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
      elif decide == "add" and genre == "guns" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM guns WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO guns VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending gun pfps to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add gun channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add gun channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting gun pfps for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "guns":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM guns WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.green, description=f"{Emojis.warning} {ctx.author.mention} autopost for gun pfps isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM guns WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} autopost for gun pfps is removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
      elif decide == "add" and genre == "faceless" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM faceless WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO faceless VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending faceless pfps to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add faceless channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add faceless channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting faceless pfps for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "faceless":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM faceless WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} autopost for faceless pfps isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM faceless WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} autopost for faceless pfps is removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
      elif decide == "add" and genre == "body" and channel != None:
       if channel.is_nsfw() is False:
          e = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} {channel.mention} is age restricted")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM autobody WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO autobody VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending body pfps to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add body channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add body channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting body pfps for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "body":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM autobody WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} autopost for body pfps isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM autobody WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} autopost for body pfps is removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
      elif decide == "add" and genre == "shoes" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM autoshoes WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO autoshoes VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending shoes pfps to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add shoes channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add shoes channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting shoes pfps for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "shoes":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM autoshoes WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} autopost for shoes pfps isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM autoshoes WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} autopost for shoes pfps is removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
      elif decide == "add" and genre == "jewellry" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM jewellry WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO jewellry VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending jewellry pfps to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add jewellry channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add jewellry channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting jewellry pfps for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "jewellry":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM jewellry WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} autopost for jewellry pfps isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM jewellry WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} autopost for jewellry pfps is removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
      elif decide == "add" and genre == "aesthetic" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM aesthetic WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO aesthetic VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending aesthetic pfps to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add aesthetic channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add aesthetic channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting aesthetic pfps for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "aesthetic":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM aesthetic WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} autopost for aesthetic pfps isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM aesthetic WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} autopost for aesthetic pfps is removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
      elif decide == "add" and genre == "cartoon" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM cartoon WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO cartoon VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending cartoon pfps to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add cartoon channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add cartoon channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting cartoon pfps for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "cartoon":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM cartoon WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} autopost for cartoon pfps isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM cartoon WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} autopost for cartoon pfps is removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
      elif decide == "add" and genre == "drill" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM drill WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO drill VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending drill pfps to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add drill channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add drill channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting drill pfps for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "drill":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM drill WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} autopost for drill pfps isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM drill WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} autopost for drill pfps is removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
      elif decide == "add" and genre == "hellokitty" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM hellokitty WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO hellokitty VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending hellokitty pfps to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add hellokitty channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add hellokitty channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting hellokitty pfps for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "hellokitty":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM hellokitty WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} autopost for hellokitty pfps isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM hellokitty WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} autopost for hellokitty pfps is removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
      elif decide == "add" and genre == "money" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM money WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO money VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending money pfps to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add money channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add money channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting money pfps for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "money":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM money WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} autopost for money pfps isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM money WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} autopost for money pfps is removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
      elif decide == "add" and genre == "smoking" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM smoking WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO smoking VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending smoking pfps to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add smoking channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add smoking channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting smoking pfps for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "smoking":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM smoking WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} autopost for smoking pfps isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM smoking WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} autopost for smoking pfps is removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
      elif decide == "add" and genre == "animals" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM animals WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO animals VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending animals pfps to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add animals channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add animals channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting animals pfps for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "animals":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM animals WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} autopost for animals pfps isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM animals WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} autopost for animals pfps is removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
      elif decide == "add" and genre == "soft" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM soft WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO soft VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending soft pfps to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add soft channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add soft channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting soft pfps for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "soft":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM soft WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} autopost for soft pfps isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM soft WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} autopost for soft pfps is removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
      elif decide == "add" and genre == "quote" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM quote WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO quote VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending quote to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add quote channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add quote channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting quote for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "quote":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM quote WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} quote isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM quote WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} quote is removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
      elif decide == "add" and genre == "besties" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM besties WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO besties VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending besties pfps to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add besties channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add besties channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting besties pfps for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "besties":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM besties WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} besties channel isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM besties WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} besties is removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
      elif decide == "add" and genre == "couplesgif" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM couplesgif WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO couplesgif VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending couplesgif pfps to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add couplesgif channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add couplesgif channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting couplesgif pfps for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "couplesgif":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM couplesgif WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} couplesgif channel isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM couplesgif WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} couplesgif is removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
      elif decide == "add" and genre == "couplespfp" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM couplespfp WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO couplespfp VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending couplespfp pfps to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add couplespfp channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add couplespfp channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting couplespfp pfps for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "couplespfp":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM couplespfp WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} couplespfp channel isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM couplespfp WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} couplespfp is removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
      elif decide == "add" and genre == "kpop" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM kpop WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO kpop VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending kpop pfps to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add kpop channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add kpop channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting kpop pfps for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "kpop":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM kpop WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} kpop channel isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM kpop WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} kpop is removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return  
      elif decide == "add" and genre == "edgy" and channel != None:
       if channel.is_nsfw() is False:
          e = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} {channel.mention} is age restricted")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM edgy WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO edgy VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending edgy pfps to {channel.mention}")
                embe.add_field(name="WARNING", value="this genre can contain: **blood, gore, sh** remove it right now if you are sensitive!")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add edgy channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add edgy channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting edgy pfps for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "edgy":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM edgy WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} edgy channel isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM edgy WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} edgy is removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
      elif decide == "add" and genre == "core" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM core WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO core VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending core to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add core channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add core channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting core for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "core":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM core WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} core isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM core WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} core is removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
      elif decide == "add" and genre == "nike" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM nike WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO nike VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending nike pfps to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add nike channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add nike channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting nike for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "nike":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM nike WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} nike isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM nike WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} nike is removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return

    @commands.hybrid_command(aliases=["autobanners"], help="adds autobanner module for your server", description="autopost", brief="> autobanner add [channel] - adds your autobanner channel\n> autobanner remove - removes your autobanner channel")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist()
    async def autobanner(self, ctx: commands.Context, decide: str=None, channel: Union[discord.TextChannel, discord.ForumChannel, discord.Thread] = None):
      if not ctx.author.guild_permissions.manage_guild:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} you are missing permissions `manage_guild`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        return 
      if decide == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: autobanner add [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete() 
        return 
      if decide == "add" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: autobanner add [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      elif decide == "add" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM banner WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO banner VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} added autobanner channel to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add autobanner channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add autobanner channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} autobanner channel is already added, please remove it before adding a new one")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM banner WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} autobanner channel isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM banner WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} autobanner channel removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return

    @commands.hybrid_command(help="adds automeme module for your server", description="autopost", brief="> automeme add [channel] - adds your auto meme channel\n> automeme remove - removes your automeme channel")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist()
    async def automeme(self, ctx: commands.Context, decide: str=None, channel: Union[discord.TextChannel, discord.ForumChannel, discord.Thread] = None):
      if not ctx.author.guild_permissions.manage_guild:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} you are missing permissions `manage_guild`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        return 
      if decide == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: automeme add [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete() 
        return 
      if decide == "add" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: automeme add [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      elif decide == "add" and channel != None:
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM automeme WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO automeme VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} added automeme channel to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add automeme channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add automeme channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} automeme channel is already added, please remove it before adding a new one")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM automeme WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} automeme channel isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM automeme WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} automeme channel removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return

    # @commands.hybrid_command(help="adds autonsfw module for your server", description="autopost", brief="> autonsfw add [channel] - adds your auto meme channel\n> autonsfw remove - removes your autonsfw channel")
    # @commands.cooldown(1, 10, commands.BucketType.user)
    # @blacklist()
    # async def autonsfw(self, ctx: commands.Context, decide: str=None, channel: Union[discord.TextChannel, discord.ForumChannel, discord.Thread] = None):
    #   if not ctx.author.guild_permissions.manage_guild:
    #     embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} you are missing permissions `manage_guild`") 
    #     await ctx.reply(embed=embed, mention_author=True, delete_after=50)
    #     return 
    #   if decide == None:
    #     embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: autonsfw add [channel]`") 
    #     await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
    #     await ctx.message.delete()
    #     return 
    #   if decide == "add" and channel == None:
    #     embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: autonsfw add [channel]`") 
    #     await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
    #     await ctx.message.delete()
    #     return 
    #   elif decide == "add" and channel != None:
    #    if channel.is_nsfw() is False:
    #       e = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} {channel.mention} is age restricted")
    #       await ctx.reply(embed=e, mention_author=True, delete_after=50)
    #       return 
    #    async with self.bot.db.cursor() as cursor: 
    #     await cursor.execute("SELECT * FROM autonsfw WHERE guild_id = {}".format(ctx.guild.id))
    #     check = await cursor.fetchone()
    #     if check is None:
    #      url = self.bot.user.avatar.url   
    #      async with aiohttp.ClientSession() as ses: 
    #        async with ses.get(url) as r:
    #         try:
    #          if r.status in range (200, 299):
    #             img = BytesIO(await r.read())
    #             bytes = img.getvalue()
    #             await cursor.execute("INSERT INTO autonsfw VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
    #             await self.bot.db.commit()
    #             embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} added autonsfw channel to {channel.mention}")
    #             embe.add_field(name=" ", value="**autonsfw won't start until you vote for it. That means you need to vote every 12 hours. Join our support server to get notifications when you are able to vote for our bot.**")
    #             button = discord.ui.Button(label="vote", style=discord.ButtonStyle.url, url="https://top.gg/bot/1094942437820076083/vote")
    #             button1 = discord.ui.Button(label="support", style=discord.ButtonStyle.url, url="https://discord.gg/FS2XFzGTF8")
    #             view = discord.ui.View()
    #             view.add_item(button)
    #             view.add_item(button1)
    #             await ctx.reply(view=view, embed=embe, mention_author=True)
    #             return
    #          else:
    #             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add nsfw channel")
    #             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
    #         except:
    #          embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add nsfw channel")
    #          await ctx.reply(embed=embed, mention_author=True, delete_after=50)
    #     elif check is not None:
    #      embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} nsfw channel is already added, please remove it before adding a new one")
    #      await ctx.reply(embed=embed, mention_author=True, delete_after=50)
    #      return 
    #   elif decide == "remove":
    #    async with self.bot.db.cursor() as cursor:  
    #     await cursor.execute("SELECT * FROM autonsfw WHERE guild_id = {}".format(ctx.guild.id))
    #     check = await cursor.fetchone()
    #     if check is None: 
    #      embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} autonsfw channel isn't added")
    #      await ctx.reply(embed=embed, mention_author=True, delete_after=50)
    #      return  
    #     elif check is not None:   
    #       await cursor.execute("DELETE FROM autonsfw WHERE guild_id = {}".format(ctx.guild.id))
    #       await self.bot.db.commit()
    #       e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} autonsfw channel removed")
    #       await ctx.reply(embed=e, mention_author=True, delete_after=50)
    #      return
        
    @commands.hybrid_command(aliases=["autonsfws", "nsfw"], help="adds autogif module for your server", description="autopost", brief="> autogif add [genre] [channel] - adds your autogif channel\n> autopfp remove [genre] - removes your autogif channel")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist()
    async def autonsfw(self, ctx: commands.Context, decide: str=None, genre: str=None, channel: Union[discord.TextChannel, discord.ForumChannel, discord.Thread] = None):
      if not ctx.author.guild_permissions.manage_guild:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} you are missing permissions `manage_guild`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        return 
      if decide == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: autonsfw add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      if decide == "add" and genre == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: autonsfw add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return
      if decide == "remove" and genre == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: autonsfw add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return
      if decide == "add" and genre == "porn" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: autonsfw add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      if decide == "add" and genre == "hentai" and channel == None:
        embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} `syntax: autonsfw add [genre] [channel]`") 
        await ctx.reply(embed=embed, mention_author=True, delete_after=50) 
        await ctx.message.delete()
        return 
      elif decide == "add" and genre == "porn" and channel != None:
       if channel.is_nsfw() is False:
          e = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} {channel.mention} is age restricted")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM autonsfw WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO autonsfw VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe.add_field(name=" ", value="**autonsfw won't start until you vote for it. That means you need to vote every 12 hours. Join our support server to get notifications when you are able to vote for our bot.**")
                button = discord.ui.Button(label="vote", style=discord.ButtonStyle.url, url="https://top.gg/bot/1094942437820076083/vote")
                button1 = discord.ui.Button(label="support", style=discord.ButtonStyle.url, url="https://discord.gg/FS2XFzGTF8")
                view = discord.ui.View()
                view.add_item(button)
                view.add_item(button1)
                await ctx.reply(view=view, embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add porn channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add porn channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting porn for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "porn":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM autonsfw WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} porn isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM autonsfw WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} porn removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
      elif decide == "add" and genre == "hentai" and channel != None:
       if channel.is_nsfw() is False:
          e = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} {channel.mention} is age restricted")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
       async with self.bot.db.cursor() as cursor: 
        await cursor.execute("SELECT * FROM hentai WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None:
         url = self.bot.user.avatar.url   
         async with aiohttp.ClientSession() as ses: 
           async with ses.get(url) as r:
            try:
             if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                await cursor.execute("INSERT INTO hentai VALUES (?, ?)", (ctx.guild.id, ctx.guild.get_channel_or_thread(channel.id).id))
                await self.bot.db.commit()
                embe = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} now sending hentai gifs to {channel.mention}")
                await ctx.reply(embed=embe, mention_author=True)
                return
             else:
                embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add hentai channel")
                await ctx.reply(embed=embed, mention_author=True, delete_after=50)
            except:
             embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} failed to add hentai channel")
             await ctx.reply(embed=embed, mention_author=True, delete_after=50)
        elif check is not None:
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} i am already posting hentai gifs for this server, please remove it to add it to another channel")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return 
      elif decide == "remove" and genre == "hentai":
       async with self.bot.db.cursor() as cursor:  
        await cursor.execute("SELECT * FROM hentai WHERE guild_id = {}".format(ctx.guild.id))
        check = await cursor.fetchone()
        if check is None: 
         embed = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention} hentai isn't added")
         await ctx.reply(embed=embed, mention_author=True, delete_after=50)
         return  
        elif check is not None:   
          await cursor.execute("DELETE FROM hentai WHERE guild_id = {}".format(ctx.guild.id))
          await self.bot.db.commit()
          e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention} hentai removed")
          await ctx.reply(embed=e, mention_author=True, delete_after=50)
          return
        
                            
async def setup(bot) -> None:
    await bot.add_cog(autopost(bot))