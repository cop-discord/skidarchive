import discord, aiohttp, button_paginator as pg
from cogs.events import noperms, commandhelp, blacklist, sendmsg
from backend.classes import Colors, Emojis
from discord.ext import commands
from typing import Union
from io import BytesIO
from discord.ext.commands import Context

class emoji(commands.Cog):
   def __init__(self, bot):
      self.bot = bot
    
   @commands.command(help="add an emoji", description="emoji", usage="[emoji] <name>")
   @commands.cooldown(1, 4, commands.BucketType.user)
   @blacklist()
   async def addemoji(self, ctx, emoji: Union[discord.Emoji, discord.PartialEmoji]=None, *, name=None):
    if (not ctx.author.guild_permissions.manage_emojis_and_stickers):
     await noperms(self, ctx, "manage_emojis_and_stickers")
     return
    if emoji is None: return await commandhelp(self, ctx, ctx.command.name) 
    if name == None:
        name = emoji.name

    url = emoji.url
    async with aiohttp.ClientSession() as ses: 
     async with ses.get(url) as r:
        try:
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                emoji = await ctx.guild.create_custom_emoji(image=bytes, name=name)
                await sendmsg(self, ctx, f"added emoji `{name}` | {emoji}", None, None, None, None)
        except discord.HTTPException as re:
          pass

   @commands.command(help="add multiple emojis", description="emoji", usage="[emojis]", aliases=["am"])
   @commands.cooldown(1, 6, commands.BucketType.guild)
   @blacklist()
   async def addmultiple(self, ctx: commands.Context, *emoji: Union[discord.Emoji, discord.PartialEmoji]):
    if (not ctx.author.guild_permissions.manage_emojis_and_stickers):
     await noperms(self, ctx, "manage_emojis_and_stickers")
     return
    if len(emoji) == 0: return await commandhelp(self, ctx, ctx.command.name) 
    if len(emoji) > 50: return await ctx.reply("you can only add up to 50 emojis at once")
    emojis = []
    await ctx.channel.typing()
    for emo in emoji:
        url = emo.url
        async with aiohttp.ClientSession() as ses: 
          async with ses.get(url) as r:
             try:
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                emoj = await ctx.guild.create_custom_emoji(image=bytes, name=emo.name)
                emojis.append(f"{emoj}")
             except discord.HTTPException as re:
               pass

    embed = discord.Embed(color=Colors.default, title=f"added {len(emoji)} emojis") 
    embed.description = "".join(map(str, emojis))    
    await sendmsg(self, ctx, None, embed, None, None, None)

   @commands.command(help="add an emoji from an image link or attachment", description="emoji", usage="[image url] <name>", aliases=["imgemoji"])
   @commands.cooldown(1, 4, commands.BucketType.user)
   @blacklist()
   async def imgaddemoji(self, ctx, url=None, *, name):
    if (not ctx.author.guild_permissions.manage_emojis_and_stickers):
     await noperms(self, ctx, "manage_emojis_and_stickers")
     return
    if url is None:
        if not ctx.message.attachments: 
            await commandhelp(self, ctx, ctx.command.name)
            return 
        url = ctx.message.attachments[0].url

    async with aiohttp.ClientSession() as ses: 
      async with ses.get(url) as r:
        try:
            if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                emoji = await ctx.guild.create_custom_emoji(image=bytes, name=name)
                embed=discord.Embed(color=Colors.default, description=f"{Emojis.check} added emoji `{name}` | {emoji}")
                await sendmsg(self, ctx, None, embed, None, None, None)
            else:
                embed=discord.Embed(color=Colors.default, description=f"{Emojis.warning} failed to add emoji")
                await sendmsg(self, ctx, None, embed, None, None, None)
        except discord.HTTPException:
            embed=discord.Embed(color=Colors.default, description=f"{Emojis.warning} failed to add emoji")
            await sendmsg(self, ctx, None, embed, None, None, None)

   @commands.command(help="add a sticker", description="emoji", usage="[attach sticker / message link]", aliases=["addsticker"])
   @commands.cooldown(1, 4, commands.BucketType.user)
   @blacklist()
   async def stealsticker(self, ctx: commands.Context):
     if not ctx.author.guild_permissions.manage_emojis_and_stickers:
      await noperms(self, ctx, "manage_emojis_and_stickers")
      return   
     if ctx.message.stickers:
      try:
       url = ctx.message.stickers[0].url
       name = ctx.message.stickers[0].name
       async with aiohttp.ClientSession() as cs:
        async with cs.get(url) as r:
          img_data = await r.read()

       tobytess = BytesIO(img_data)
       file = discord.File(fp=tobytess)
       sticker = await ctx.guild.create_sticker(name=name, description=name, emoji="skull", file=file, reason=f"sticker created by {ctx.author}")
       format = str(sticker.format) 
       form = format.replace("StickerFormatType.", "")
       embed = discord.Embed(color=Colors.default, title="sticker added")
       embed.set_thumbnail(url=url)
       embed.add_field(name="values", value=f"name: `{name}`\nid: `{sticker.id}`\nformat: `{form}`\nlink: [url]({url})")
       await sendmsg(self, ctx, None, embed, None, None, None)
      except Exception as error:
       embed = discord.Embed(color=Colors.default, description=f"{Emojis.warning} {ctx.author.mention} unable to add this sticker - {error}")
       await sendmsg(self, ctx, None, embed, None, None, None)
     elif not ctx.message.stickers:
      def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

      e = discord.Embed(color=Colors.default, description=f"{Emojis.warning} {ctx.author.mention} you have **15** seconds to send a sticker")
      await sendmsg(self, ctx, None, e, None, None, None)
      try:
          message = await self.bot.wait_for('message', timeout=15, check=check)
      except TimeoutError:
          await sendmsg(self, ctx, f"{Emojis.warning} {ctx.author.mention} you didn't send a sticker in time", None, None, None, discord.AllowedMentions(users=True))
          return

      if message.stickers:
       try:
        url = message.stickers[0].url
        name = message.stickers[0].name
        async with aiohttp.ClientSession() as cs:
         async with cs.get(url) as r:
          img_data = await r.read()

        tobytess = BytesIO(img_data)
        file = discord.File(fp=tobytess)
        sticker = await ctx.guild.create_sticker(name=name, description=name, emoji="skull", file=file, reason=f"sticker created by {ctx.author}")
        format = str(sticker.format) 
        form = format.replace("StickerFormatType.", "")
        embed = discord.Embed(color=Colors.default, title="sticker added")
        embed.set_thumbnail(url=url)
        embed.add_field(name="values", value=f"name: `{name}`\nid: `{sticker.id}`\nformat: `{form}`\nlink: [url]({url})")
        await sendmsg(self, ctx, None, embed, None, None, None)
       except:
        embed = discord.Embed(color=Colors.default, description=f"{Emojis.warning} {ctx.author.mention} unable to add this sticker")
        await sendmsg(self, ctx, None, embed, None, None, None)  
      else:
       e = discord.Embed(color=Colors, description=f"{Emojis.warning} {ctx.author.mention} this isn't a sticker")
       await sendmsg(self, ctx, None, e, None, None, None) 
        
   @commands.command(help="returns a list of server's emojis", description="emoji", aliases=["el"])
   @commands.cooldown(1, 3, commands.BucketType.user)
   @blacklist()
   async def emojilist(self, ctx: commands.Context):
            i=0
            k=1
            l=0
            mes = ""
            number = []
            messages = []
            for emoji in ctx.guild.emojis:
              mes = f"{mes}`{k}` {emoji} - ({emoji.name})\n"
              k+=1
              l+=1
              if l == 10:
               messages.append(mes)
               number.append(discord.Embed(color=Colors.default, title=f"emojis in {ctx.guild.name} [{len(ctx.guild.emojis)}]", description=messages[i]))
               i+=1
               mes = ""
               l=0
    
            messages.append(mes)
            number.append(discord.Embed(color=Colors.default, title=f"emojis in {ctx.guild.name} [{len(ctx.guild.emojis)}]", description=messages[i]))
            paginator = pg.Paginator(self.bot, number, ctx, invoker=ctx.author.id)
            paginator.add_button('prev', emoji= "<:left:1018156480991612999>")
            paginator.add_button('delete', emoji = "<:stop:1018156487232720907>")
            paginator.add_button('next', emoji="<:right:1018156484170883154>")
            await paginator.start()            

   @commands.command(aliases=["downloademoji", "e"], help="gets an image version of your emoji", description="emoji", usage="[emoji]")
   @commands.cooldown(1, 4, commands.BucketType.user)
   @blacklist()
   async def enlarge(self, ctx, emoji: Union[discord.PartialEmoji, str]=None):
    if emoji is None:
     await commandhelp(self, ctx, ctx.command.name)
     return  
    elif isinstance(emoji, discord.PartialEmoji): 
      await sendmsg(self, ctx, emoji.url, None, None, None, None)
      return
    elif isinstance(emoji, str):
      ordinal = ord(emoji)
      await sendmsg(self, ctx, f"https://twemoji.maxcdn.com/v/latest/72x72/{ordinal:x}.png", None, None, None, None)
    else:
       e = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention}: emoji not found")
       await sendmsg(self, ctx, None, e, None, None, None)

async def setup(bot) -> None:
    await bot.add_cog(emoji(bot))   
