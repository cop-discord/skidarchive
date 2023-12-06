import button_paginator as pg, datetime, aiohttp, humanfriendly, os, random, asyncio, discord, time, datetime, requests
from discord.ext import tasks, commands
from discord import Embed, File, TextChannel, Member, User, Role, Status, Message, Spotify, Message, AllowedMentions
from discord.ext.commands import Cog, command, Context, cooldown, BucketType, AutoShardedBot as Bot
from discord.ui import Button, View
from cogs.events import commandhelp, blacklist, sendmsg, noperms, sendmsgg
from backend.classes import Colors, Emojis, Func
from backend.untils import PaginatorView
from discord.ui import View, Button, Select
from PIL import Image
#from wordcloud import WordCloud
from colorthief import ColorThief
from typing import Union
from backend import http
from backend.embedparser import to_object
from io import BytesIO
from deep_translator import GoogleTranslator
from discord.ext.commands import Context

DISCORD_API_LINK = "https://discord.com/api/invite/"

class BlackTea: 
    """BlackTea backend variables"""
    MatchStart = {}
    lifes = {}
    
    async def get_string(): 
      lis = await BlackTea.get_words()
      word = random.choice(lis)
      return word[:3]

    async def get_words(): 
      async with aiohttp.ClientSession() as cs: 
       async with cs.get("https://dev.usebot.lol/words") as r: 
        byte = await r.read()
        data = str(byte, 'utf-8')
        return data.splitlines()
    
reaction_message_author = {}
reaction_message_author_avatar = {}
reaction_message_emoji_url = {}
reaction_message_emoji_name = {}
reaction_message_id = {}
edit_message_author = {}
edit_message_content1 = {}
edit_message_content2 = {}
edit_message_author_avatar = {}
edit_message_id = {}
downloadCount = 0

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds)


async def paginator(self, ctx, pages):
        if len(pages) == 1:
            await ctx.send(embed=pages[0])
            return

        def check(interaction):
            if interaction.user.id != ctx.author.id:
                return False

        class PaginatorView(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.bot = ctx.bot
                self.current = 0

            @discord.ui.button(style=discord.ButtonStyle.gray, label="<")
            async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
                if check(interaction) is False:
                    return interaction.response.defer()
                if self.current == 0 or self.current < 0:
                    await interaction.response.defer()
                    return
                try:
                    self.current -= 1
                    await interaction.response.edit_message(embed=pages[self.current])
                except:
                    await interaction.response.defer()

            @discord.ui.button(label=">", style=discord.ButtonStyle.gray)
            async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
                if check(interaction) is False:
                    return interaction.response.defer()
                if self.current == len(pages) - 1:
                    await interaction.response.defer()
                    return
                self.current += 1
                try:
                    await interaction.response.edit_message(embed=pages[self.current])
                except:
                    await interaction.response.defer()

            @discord.ui.button(label="x", style=discord.ButtonStyle.red)
            async def exit(self, interaction: discord.Interaction, button: discord.ui.Button):
                if check(interaction) is False:
                    return interaction.response.defer()
                await interaction.response.edit_message(content=":thumbsup_tone2: Stopped interaction", embed=None, view=None)
                self.stop()
                
        paginator = PaginatorView()
        await ctx.send(embed=pages[0], view=paginator)
        await paginator.wait()

class Utilityy(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot 
    
    @Cog.listener()
    async def on_ready(self):
     async with self.bot.db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS oldusernames (username TEXT, discriminator TEXT, time INTEGER, user INTEGER)")
            await cursor.execute("CREATE TABLE IF NOT EXISTS selfprefix (pref TEXT, user_id INTEGER)")
            await cursor.execute("CREATE TABLE IF NOT EXISTS snipe (guild_id INTEGER, channel_id INTEGER, author TEXT, content TEXT, attachment TEXT, avatar TEXT)")
            await cursor.execute("CREATE TABLE IF NOT EXISTS afk (guild_id INTEGER, user_id INTEGER, reason TEXT, time INTEGER);")
            await cursor.execute("CREATE TABLE IF NOT EXISTS selfprefix (pref TEXT, user_id INTEGER)")
            await cursor.execute("CREATE TABLE IF NOT EXISTS prefixes (guild_id INTEGER, prefix TEXT);") 
     await self.bot.db.commit()
    
    @Cog.listener()
    async def on_message_delete(self, message: Message):
        if not message.guild: return 
        if message.author.bot: return
        if message.attachments:
         attachment = message.attachments[0].url
        else:
         attachment = "none"

        author = str(message.author)
        content = message.content
        avatar = message.author.display_avatar.url
        async with self.bot.db.cursor() as curso: 
         await curso.execute("INSERT INTO snipe VALUES (?,?,?,?,?,?)", (message.guild.id, message.channel.id, author, content, attachment, avatar))
         await self.bot.db.commit()

    @Cog.listener()
    async def on_message(self, message: Message):
     if not message.guild: return 
     if message.author.bot: return
     if message.mentions: 
       async with self.bot.db.cursor() as cursor:
        for mem in message.mentions:
         await cursor.execute("SELECT * from afk where guild_id = {} AND user_id = {}".format(message.guild.id, mem.id)) 
         check = await cursor.fetchone()
         if check is not None:
          em = Embed(color=0x2B2D31, description=f"{mem.mention} is AFK since <t:{int(check[3])}:R> - **{check[2]}**")
          await sendmsg(self, message, None, em, None, None, None)

     async with self.bot.db.cursor() as curs:
        await curs.execute("SELECT * from afk where guild_id = {} AND user_id = {}".format(message.guild.id, message.author.id)) 
        check = await curs.fetchone()
        if check is not None:
         embed = Embed(color=0x2B2D31, description=f"<a:wave:1020721034934104074> Welcome back {message.author.mention}! You were AFK since <t:{int(check[3])}:R>")
         await sendmsg(self, message, None, embed, None, None, None)
         await curs.execute("DELETE FROM afk WHERE guild_id = {} AND user_id = {}".format(message.guild.id, message.author.id))
     await self.bot.db.commit()

    @Cog.listener()
    async def on_user_update(self, before, after):
     try:
      if before.name == after.name: return
      async with self.bot.db.cursor() as cursor:
        await cursor.execute("INSERT INTO oldusernames (username, discriminator, time, user) VALUES (?, ?, ?, ?)", (before.name, before.discriminator, int(datetime.datetime.now().timestamp()), before.id,))
        await self.bot.db.commit()
     except:
        pass

    @Cog.listener()
    async def on_message_edit(self, old, new):
     if old.author.bot: return
     if old.content == new.content: return
     edit_message_author[old.channel.id] = old.author
     edit_message_author_avatar[old.channel.id] = old.author.display_avatar.url
     edit_message_content1[old.channel.id] = old.content
     edit_message_content2[new.channel.id] = new.content
     edit_message_id[old.channel.id] = new.id   

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
      guild = self.bot.get_guild(payload.guild_id)
      member = guild.get_member(payload.user_id)  
      if member is None: return
      if member.bot: return
      reaction_message_author[payload.channel_id] = member.name
      reaction_message_author_avatar[payload.channel_id] = member.display_avatar.url   
      reaction_message_emoji_url[payload.channel_id] = payload.emoji.url
      reaction_message_emoji_name[payload.channel_id] = payload.emoji.name
      reaction_message_id[payload.channel_id] = payload.message_id 
    
    @command(help="play blacktea with your friends", description="fun")
    @cooldown(1, 20, BucketType.guild)
    @blacklist()
    async def blacktea(self, ctx: Context): 
     try:
      if BlackTea.MatchStart[ctx.guild.id] is True: 
       return await ctx.reply("somebody in this server is already playing blacktea", mention_author=False)
     except KeyError: pass 

     BlackTea.MatchStart[ctx.guild.id] = True 
     embed = Embed(color=Colors.default, title="BlackTea Matchmaking", description=f"⏰ Waiting for players to join. To join react with 🍵.\nThe game will begin in **20 seconds**")
     embed.add_field(name="goal", value="You have **10 seconds** to say a word containing the given group of **3 letters.**\nIf failed to do so, you will lose a life. Each player has **2 lifes**")
     embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)  
     mes = await ctx.send(embed=embed)
     await mes.add_reaction("🍵")
     await asyncio.sleep(20)
     me = await ctx.channel.fetch_message(mes.id)
     players = [user.id async for user in me.reactions[0].users()]
     players.remove(self.bot.user.id)

     if len(players) < 2:
      BlackTea.MatchStart[ctx.guild.id] = False
      return await ctx.send("😦 {}, not enough players joined to start blacktea".format(ctx.author.mention), allowed_mentions=AllowedMentions(users=True)) 
  
     while len(players) > 1: 
      for player in players: 
       strin = await BlackTea.get_string()
       await ctx.send(f"⏰ <@{player}>, type a word containing **{strin.upper()}** in **10 seconds**", allowed_mentions=AllowedMentions(users=True))
      
       def is_correct(msg): 
        return msg.author.id == player
      
       try: 
        message = await self.bot.wait_for('message', timeout=10, check=is_correct)
       except asyncio.TimeoutError: 
          try: 
            BlackTea.lifes[player] = BlackTea.lifes[player] + 1  
            if BlackTea.lifes[player] == 3: 
              await ctx.send(f" <@{player}>, you're eliminated ☠️", allowed_mentions=AllowedMentions(users=True))
              BlackTea.lifes[player] = 0
              players.remove(player)
              continue 
          except KeyError:  
            BlackTea.lifes[player] = 0   
          await ctx.send(f"💥 <@{player}>, you didn't reply on time! **{2-BlackTea.lifes[player]}** lifes remaining", allowed_mentions=AllowedMentions(users=True))    
          continue
       if not strin.lower() in message.content.lower() or not message.content.lower() in await BlackTea.get_words():
          try: 
            BlackTea.lifes[player] = BlackTea.lifes[player] + 1  
            if BlackTea.lifes[player] == 3: 
              await ctx.send(f" <@{player}>, you're eliminated ☠️", allowed_mentions=AllowedMentions(users=True))
              BlackTea.lifes[player] = 0
              players.remove(player)
              continue 
          except KeyError:  
            BlackTea.lifes[player] = 0 
          await ctx.send(f"💥 <@{player}>, incorrect word! **{2-BlackTea.lifes[player]}** lifes remaining", allowed_mentions=AllowedMentions(users=True))
       else: await message.add_reaction("✅")  
          
     await ctx.send(f"👑 <@{players[0]}> won the game!", allowed_mentions=AllowedMentions(users=True))
     BlackTea.lifes[players[0]] = 0
     BlackTea.MatchStart[ctx.guild.id] = False  

    # @command(help="set your own prefix", usage="[prefix]", description="utility")
    # @cooldown(1, 4, BucketType.user)
    # @blacklist()
    # async def selfprefix(self, ctx: Context, prefix=None):
    #   if prefix == None:
    #     await commandhelp(self, ctx, ctx.command.name)
    #     return 
      
    #   async with self.bot.db.cursor() as cursor:
    #    if prefix.lower() == "none": 
    #     await cursor.execute("SELECT * FROM selfprefix WHERE user_id = {}".format(ctx.author.id)) 
    #     check = await cursor.fetchone()
    #     if check is not None:
    #       await cursor.execute("DELETE FROM selfprefix WHERE user_id = {}".format(ctx.author.id))
    #       await self.bot.db.commit()
    #       await sendmsg(self, ctx, None, Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention}: removed your self prefix"), None, None, None)
    #     elif check is None:
    #        await sendmsg(self, ctx, None, Embed(color=Colors.red, description=f"{Emojis.wrong} {ctx.author.mention}: you don't have a self prefix"), None, None, None) 
    #    else:    
    #     await cursor.execute("SELECT * FROM selfprefix WHERE user_id = {}".format(ctx.author.id)) 
    #     result = await cursor.fetchone()
    #     if result is not None:
    #      sql = ("UPDATE selfprefix SET pref = ? WHERE user_id = ?")
    #      val = (prefix, ctx.author.id)
    #      await cursor.execute(sql, val)
    #      embed = Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention}: self prefix changed to `{prefix}`")
    #      await sendmsg(self, ctx, None, embed, None, None, None)
    #      await self.bot.db.commit()  
    #     elif result is None:
    #      sql = ("INSERT INTO selfprefix VALUES(?,?)")
    #      val = (prefix, ctx.author.id)
    #      await cursor.execute(sql, val)
    #      embed =Embed(color=Colors.green, description=f"{Emojis.check} {ctx.author.mention}: self prefix changed to `{prefix}`")
    #      await sendmsg(self, ctx, None, embed, None, None, None)
    #      await self.bot.db.commit()    
        
    # @command(aliases=['wc'], description="utility", help="send a wordcloud with channel's messages")
    # async def wordcloud(self, ctx: Context, limit: int=None):
    #     if limit is None or limit > 100: limit = 100
    #     async with ctx.typing():
    #         text=[message.content async for message in ctx.channel.history(limit=limit)]
    #         wc = WordCloud(mode = "RGBA", background_color=None,  height=400, width=700)
    #         wc.generate(' '.join(text))
    #         wc.to_file(filename=f'{ctx.author.id}.png')
    
    #         await ctx.send(file=File(f"{ctx.author.id}.png"))
    #         os.remove(f'{ctx.author.id}.png')

    @command(help="clear your usernames", description="utility", aliases=["clearusernames", "clearusers"])
    @cooldown(1, 3, BucketType.user)
    @blacklist()
    async def clearnames(self, ctx):
        try:
            async with self.bot.db.cursor() as cursor:
                await cursor.execute("DELETE FROM oldusernames WHERE user = ?", (ctx.author.id,))
            await sendmsg(self, ctx, "<:thumbsup:1129811199626854534>", None, None, None, None)
            await self.bot.db.commit()
        except Exception as e:
            print(e)
    
    # @command(help="changes the guild prefix", usage="[prefix]", description="utility")
    # @cooldown(1, 4, BucketType.user)
    # @blacklist()
    # async def prefix(self, ctx: Context, prefix=None):
    #   if not ctx.author.guild_permissions.manage_guild:
    #     await noperms(self, ctx, "manage_guild")
    #     return 
    #   if prefix == None:
    #     await commandhelp(self, ctx, ctx.command.name)
    #     return 
      
    #   async with self.bot.db.cursor() as cursor:
    #    await cursor.execute("SELECT prefix, * FROM prefixes WHERE guild_id = {}".format(ctx.guild.id)) 
    #    check = await cursor.fetchone()
    #    if check is not None:
    #     sql = ("UPDATE prefixes SET prefix = ? WHERE guild_id = ?")
    #     val = (prefix, ctx.guild.id)
    #     await cursor.execute(sql, val)
    #     embed = Embed(color=0x2B2D31, description=f"guild prefix changed to `{prefix}`")
    #     await sendmsg(self, ctx, None, embed, None, None, None)
    #    elif check is None:
    #     sql = ("INSERT INTO prefixes VALUES(?,?)")
    #     val = (ctx.guild.id, prefix)
    #     await cursor.execute(sql, val)
    #     embed =Embed(color=0x2B2D31, description=f"guild prefix changed to `{prefix}`")
    #     await sendmsg(self, ctx, None, embed, None, None, None)
    #    await self.bot.db.commit()         
            
    @command(aliases = ['names', 'usernames'], help="check an user's past usernames", usage="<user>", description="utility")
    @cooldown(1, 4, BucketType.user)
    @blacklist()
    async def pastusernames(self, ctx, member: User = None):
        try:
            if member == None:
                member = ctx.author
            async with self.bot.db.cursor() as cursor:
                await cursor.execute("SELECT username, discriminator, time FROM oldusernames WHERE user = ?", (member.id,))
                data = await cursor.fetchall()
                i=0
                k=1
                l=0
                number = []
                messages = []
                num = 0
                auto = ""
                if data:
                    for table in data:
                        username = table[0]
                        discrim = table[1]
                        num += 1
                        auto += f"\n`{num}` {username}#{discrim}: <t:{int(table[2])}:R> "
                        k+=1
                        l+=1
                        if l == 10:
                          messages.append(auto)
                          number.append(Embed(color=0x2B2D31).set_author(name = f"{member}'s past usernames", icon_url = member.display_avatar))
                          i+=1
                          auto = ""
                          l=0
                    messages.append(auto)
                    embed = Embed(description = auto, color = 0x2B2D31)
                    embed.set_author(name = f"{member}'s past usernames", icon_url = member.display_avatar)
                    number.append(embed)
                    if len(number) > 1:
                     paginator = pg.Paginator(self.bot, number, ctx, invoker=ctx.author.id)
                     paginator.add_button('prev', emoji= "<:left:1018156480991612999>")
                     paginator.add_button('goto', emoji = "<:filter:1073308758945562705>")
                     paginator.add_button('next', emoji="<:right:1018156484170883154>")
                     await paginator.start()  
                    else:
                      await sendmsg(self, ctx, None, embed, None, None, None)      
                else:
                    await sendmsg(self, ctx, f"no logged usernames for {member}", None, None, None, None)
        except Exception as e:
            print(e)  

    @command(help="let everyone know you are away", description="utility", usage="<reason>")
    @cooldown(1, 4, BucketType.user)
    @blacklist()
    async def afk(self, ctx: Context, *, reason=None):
      if reason is None: 
        reason = "AFK"
      
      ts = int(datetime.datetime.now().timestamp())   
      async with self.bot.db.cursor() as cursor:
       await cursor.execute("SELECT * FROM afk WHERE guild_id = {} AND user_id = {}".format(ctx.guild.id, ctx.author.id))
       result = await cursor.fetchone() 
       if result is None:
        sql =  ("INSERT INTO afk VALUES(?,?,?,?)")
        val = (ctx.guild.id, ctx.author.id, reason, ts)
        await cursor.execute(sql, val)
        await self.bot.db.commit()
        embed = Embed(color=0x2B2D31, description=f"{ctx.author.mention}: You're now AFK with the status: **{reason}**")
        await sendmsg(self, ctx, None, embed, None, None, None)

    @command(aliases=["es"], help="check the latest edited messsage from a channel", usage="<channel>", description="utility") 
    @cooldown(1, 4, BucketType.user)
    @blacklist()
    async def editsnipe(self, ctx, *, channel: TextChannel=None):
     if channel is None: 
      channel = ctx.channel 
     try:
        em = Embed(color=0x2B2D31, description=f"edited message in {channel.mention}- [jump](https://discord.com/channels/{ctx.guild.id}/{channel.id}/{edit_message_id[channel.id]})")
        em.set_author(name=edit_message_author[channel.id], icon_url=edit_message_author_avatar[channel.id])
        em.add_field(name="old", value=edit_message_content1[channel.id])
        em.add_field(name="new", value=edit_message_content2[channel.id])
        await sendmsg(self, ctx, None, em, None, None, None)
     except:
        await sendmsg(self, ctx, f"there is no edited message in {channel.mention}", None, None, None, None)

    @command(aliases=["rs"], help="check the latest reaction removal of a channel", usage="<channel>", description="utility")
    @cooldown(1, 4, BucketType.user)
    @blacklist()
    async def reactionsnipe(self, ctx, *, channel: TextChannel=None):
        if channel is None:
         channel = ctx.channel 
        try: 
         em = Embed(color=0x2B2D31, description=f"{reaction_message_emoji_name[channel.id]}\n[emoji link]({reaction_message_emoji_url[channel.id]})\n[message link](https://discord.com/channels/{ctx.guild.id}/{channel.id}/{reaction_message_id[channel.id]})")
         em.set_author(name=reaction_message_author[channel.id], icon_url=reaction_message_author_avatar[channel.id])
         em.set_image(url=reaction_message_emoji_url[channel.id])
         await sendmsg(self, ctx, None, em, None, None, None)
        except: 
          await sendmsg(self, ctx, "there is no deleted reaction in {}".format(channel.mention), None, None, None, None)

    @commands.hybrid_command(description="Shows the Spotify song a user is listening to")
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @blacklist()
    async def spotify(self, ctx, user: discord.Member = None):
        try:
            if user == None:
                user = ctx.author
                pass
            if user.activities:
                for activity in user.activities:
                    if str(activity).lower() == "spotify":
                        embed = discord.Embed(color=0x2B2D31)
                        embed.add_field(
                            name="**Song**", value=f"**[{activity.title}](https://open.spotify.com/embed/track/{activity.track_id})**", inline=True)
                        embed.add_field(
                            name="**Artist**", value=f"**[{activity.artist}](https://open.spotify.com/embed/track/{activity.track_id})**", inline=True)
                        embed.set_thumbnail(url=activity.album_cover_url)
                        embed.set_author(
                            name=ctx.message.author.name, icon_url=ctx.message.author.avatar)
                        embed.set_footer(
                            text=f"Album: {activity.album}", icon_url=activity.album_cover_url)
                        await sendmsg(self, ctx, None, embed, None, None, None, None)
                        return
            embed = discord.Embed(
                description=f"{Emojis.wrong} {ctx.message.author.mention}: **{user}** is not listening to spotify", colour=Colors.default)
            await sendmsg(self, ctx, None, embed, None, None, None, None)
            return
        except Exception as e:
            print(e)
      
    @command(aliases=["s"], help="check the latest deleted message from a channel", usage="<channel>", description="utility")
    @cooldown(1, 2, BucketType.user)
    @blacklist()
    async def snipe(self, ctx: Context):
     async with self.bot.db.cursor() as cursor: 
      await cursor.execute("SELECT * FROM snipe WHERE guild_id = {} AND channel_id = {}".format(ctx.guild.id, ctx.channel.id))
      chec = await cursor.fetchall()
      embeds = []
      try:
       results = chec[::-1]
       i=0
       for check in results: 
        i+=1
        sniped = check
        em = Embed(color=0x2B2D31, description=sniped[3] + f"\n[Video]({check[4]})" if ".mp4" in sniped[4] or ".mov" in sniped[4] else sniped[3])
        em.set_author(name=sniped[2], icon_url=sniped[5]) 
        em.set_footer(text="{}/{}".format(i, len(results)))
        if check[4] != "none":
           em.set_image(url=sniped[4] if not ".mp4" in sniped[4] or not ".mov" in sniped[4] else "")
        embeds.append(em)
       if len(embeds) == 1: return await ctx.reply(embed=embeds[0], mention_author=False)
       else:  
        paginator = pg.Paginator(self.bot, embeds, ctx, invoker=ctx.author.id)
        paginator.add_button('prev', emoji= "<:left:1018156480991612999>")
        paginator.add_button('delete', emoji = "<:stop:1018156487232720907>")
        paginator.add_button('next', emoji="<:right:1018156484170883154>")
        await paginator.start() 
      except IndexError:
        if len(check) == 0: return await sendmsg(self, ctx, None, Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention}: there are no deleted messages in {ctx.channel.mention}"), None, None, None)
        await sendmsg(self, ctx, None, Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention}: current snipe limit is **{len(check)}**"), None, None, None)

    @command(aliases=["mc"], description="utility", help="check how many members does your server have")
    @cooldown(1, 2, BucketType.user)
    @blacklist()
    async def membercount(self, ctx: Context):
      b=len(set(b for b in ctx.guild.members if b.bot))
      h=len(set(b for b in ctx.guild.members if not b.bot))
      embed = Embed(color=0x2B2D31)
      embed.set_author(name=f"{ctx.guild.name}'s member count", icon_url=ctx.guild.icon)
      embed.add_field(name=f"members (+{len([m for m in ctx.guild.members if (datetime.datetime.now() - m.joined_at.replace(tzinfo=None)).total_seconds() < 3600*24 and not m.bot])})", value=h)
      embed.add_field(name="total", value=ctx.guild.member_count) 
      embed.add_field(name="bots", value=b)
      await ctx.reply(embed=embed)

    @command(description="utility", help="see someone's banner", usage="<user>", aliases=["av"])
    @cooldown(1, 2, BucketType.user)
    @blacklist()
    async def avatar(self, ctx: Context, *, member: Union[Member, User]=None):
      if member is None: 
        member = ctx.author 

      if isinstance(member, Member): 
        button1 = Button(label="default avatar", url=member.avatar.url if member.avatar is not None else "https://none.none")
        button2 = Button(label="server avatar", url=member.display_avatar.url)
        embed = Embed(color=0x2B2D31, title=f"{member.name}'s avatar", url=member.display_avatar.url)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        embed.set_image(url=member.display_avatar.url)
        view = View()
        view.add_item(button1)
        view.add_item(button2)    
        await ctx.reply(embed=embed, view=view)
      elif isinstance(member, User):
        button3 = Button(label="default avatar", url=member.display_avatar.url)
        embed = Embed(color=0x2B2D31, title=f"{member.name}'s avatar", url=member.display_avatar.url)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        embed.set_image(url=member.display_avatar.url)
        view = View()
        view.add_item(button3)  
        await ctx.reply(embed=embed, view=view)  
    
    @command(description="utility", help="see someone's banner", usage="<user>", aliases=["bnnr"])
    @cooldown(1, 4, BucketType.user)
    @blacklist()
    async def banner(self, ctx: commands.Context, *, member: discord.User=commands.Author):
     user = await self.bot.fetch_user(member.id)
     if not user.banner: return await ctx.send(f"**{user}** doesn't have a banner") 
     embed = discord.Embed(color=0x2B2D31, title=f"{user.name}'s banner", url=user.banner.url)
     embed.set_image(url=user.banner.url)
     return await ctx.reply(embed=embed) 

    @cooldown(1, 4, BucketType.user)
    @blacklist()
    async def inrole(self, ctx: Context, *, role: Role=None):
            if role is None:
             await commandhelp(self, ctx, ctx.command.name)
             return 

            i=0
            k=1
            l=0
            mes = ""
            number = []
            messages = []
            for member in role.members:
              mes = f"{mes}`{k}` {member} - ({member.id})\n"
              k+=1
              l+=1
              if l == 10:
               messages.append(mes)
               number.append(Embed(color=0x2B2D31, title=f"members in {role.name} [{len(role.members)}]", description=messages[i]))
               i+=1
               mes = ""
               l=0
    
            messages.append(mes)
            embed = Embed(color=0x2B2D31, title=f"members in {role.name} [{len(role.members)}]", description=messages[i])
            number.append(embed)
            if len(number) > 1:
             paginator = pg.Paginator(self.bot, number, ctx, invoker=ctx.author.id)
             paginator.add_button('prev', emoji= "<:left:1018156480991612999>")
             paginator.add_button('delete', emoji = "<:stop:1018156487232720907>")
             paginator.add_button('next', emoji="<:right:1018156484170883154>")
             await paginator.start()    
            else:
              await sendmsg(self, ctx, None, embed, None, None, None)

    @command(help="see all server boosters", description="utility")
    @cooldown(1, 4, BucketType.user)
    @blacklist()
    async def boosters(self, ctx: Context):
            if not ctx.guild.premium_subscriber_role:
                e = Embed(color=Colors.red, description=f"{Emojis.wrong} {ctx.author.mention}: booster role doesn't exist")
                await sendmsg(self, ctx, None, e, None, None, None)
                return 
            if len(ctx.guild.premium_subscriber_role.members) == 0:
                e = Embed(color=Colors.red, description=f"{Emojis.wrong} {ctx.author.mention}: this server doesn't have any boosters")
                await sendmsg(self, ctx, None, e, None, None, None)
                return 

            i=0
            k=1
            l=0
            mes = ""
            number = []
            messages = []
            for member in ctx.guild.premium_subscriber_role.members: 
              mes = f"{mes}`{k}` {member} - <t:{int(member.premium_since.timestamp())}:R> \n"
              k+=1
              l+=1
              if l == 10:
               messages.append(mes)
               number.append(Embed(color=0x2B2D31, title=f"{ctx.guild.name} boosters [{len(ctx.guild.premium_subscriber_role.members)}]", description=messages[i]))
               i+=1
               mes = ""
               l=0
    
            messages.append(mes)
            embed = Embed(color=0x2B2D31, title=f"{ctx.guild.name} boosters [{len(ctx.guild.premium_subscriber_role.members)}]", description=messages[i])
            number.append(embed)
            if len(number) > 1:
             paginator = pg.Paginator(self.bot, number, ctx, invoker=ctx.author.id)
             paginator.add_button('prev', emoji= "<:left:1018156480991612999>")
             paginator.add_button('delete', emoji = "<:stop:1018156487232720907>")
             paginator.add_button('next', emoji="<:right:1018156484170883154>")
             await paginator.start()
            else:
              await sendmsg(self, ctx, None, embed, None, None, None)  
    
    @command(help="see all server roles", description="utility")
    @cooldown(1, 4, BucketType.user)
    @blacklist()
    async def roles(self, ctx: Context):
            i=0
            k=1
            l=0
            mes = ""
            number = []
            messages = []
            for role in ctx.guild.roles: 
              mes = f"{mes}`{k}` {role.mention} - <t:{int(role.created_at.timestamp())}:R> ({len(role.members)} members)\n"
              k+=1
              l+=1
              if l == 10:
               messages.append(mes)
               number.append(Embed(color=0x2B2D31, title=f"{ctx.guild.name} roles [{len(ctx.guild.roles)}]", description=messages[i]))
               i+=1
               mes = ""
               l=0
    
            messages.append(mes)
            embed = Embed(color=0x2B2D31, title=f"{ctx.guild.name} roles [{len(ctx.guild.roles)}]", description=messages[i])
            number.append(embed)
            if len(number) > 1:
             paginator = pg.Paginator(self.bot, number, ctx, invoker=ctx.author.id)
             paginator.add_button('prev', emoji= "<:left:1018156480991612999>")
             paginator.add_button('delete', emoji = "<:stop:1018156487232720907>")
             paginator.add_button('next', emoji="<:right:1018156484170883154>")
             await paginator.start() 
            else:
              await sendmsg(self, ctx, None, embed, None, None, None)

    @command(help="see all server's bots", description="utility")
    @cooldown(1, 4, BucketType.user)
    @blacklist()
    async def bots(self, ctx: Context):
            i=0
            k=1
            l=0
            b=0
            mes = ""
            number = []
            messages = []
            for member in ctx.guild.members:
             if member.bot:  
              b+=1   
              mes = f"{mes}`{k}` {member} - ({member.id})\n"
              k+=1
              l+=1
              if l == 10:
               messages.append(mes)
               number.append(Embed(color=0x2B2D31, title=f"{ctx.guild.name} bots [{b}]", description=messages[i]))
               i+=1
               mes = ""
               l=0
    
            messages.append(mes)
            embed = Embed(color=0x2B2D31, title=f"{ctx.guild.name} bots [{b}]", description=messages[i])
            number.append(embed)
            if len(number) > 1:
             paginator = pg.Paginator(self.bot, number, ctx, invoker=ctx.author.id)
             paginator.add_button('prev', emoji= "<:left:1018156480991612999>")
             paginator.add_button('delete', emoji = "<:stop:1018156487232720907>")
             paginator.add_button('next', emoji="<:right:1018156484170883154>")
             await paginator.start()  
            else:
              await sendmsg(self, ctx, None, embed, None, None, None)
                
    @commands.hybrid_command(aliases=["ui", "whois"])
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @blacklist()
    async def userinfo(self, ctx: commands.Context, *, member: Union[discord.Member, discord.User] = None):
        if member is None:
            member = ctx.author

        k = 0
        for guild in self.bot.guilds:
            if guild.get_member(member.id) is not None:
                k += 1

        if isinstance(member, discord.Member):
            if str(member.status) == "online":
                status = "<:OnlineStatus:1107321260704268288>"
            elif str(member.status) == "dnd":
                status = "<:o_dnd:1107321258913300562>"
            elif str(member.status) == "idle":
                status = "<:Idle:1107321262449115168>"
            elif str(member.status) == "offline":
                status = "<:OfflineStatus:1107321263682228244>"
            embed = discord.Embed(color=0x2B2D31)
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_author(name=member.name,
                             icon_url=member.display_avatar.url)
            embed.add_field(
                name="joined", value=f"<t:{int(member.joined_at.timestamp())}:F>\n<t:{int(member.joined_at.timestamp())}:R>", inline=False)
            members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
            embed.add_field(name="join position", value=str(
                members.index(member) + 1), inline=False)
            if member.activity:
                activity = member.activity.name
            else:
                activity = ""

            embed.add_field(name="status", value=status +
                            " " + activity, inline=False)
            embed.add_field(
                name="registered", value=f"<t:{int(member.created_at.timestamp())}:F>\n<t:{int(member.created_at.timestamp())}:R>", inline=False)
            if len(member.roles) > 1:
                role_string = ' '.join([r.mention for r in member.roles][1:])
                embed.add_field(name="roles [{}]".format(
                    len(member.roles) - 1), value=role_string, inline=False)
            embed.set_footer(text='ID: ' + str(member.id) +
                             f" | {k} mutual server(s)")
            await sendmsgg(self, ctx, None, embed, None, None, None, None)
            return
        elif isinstance(member, discord.User):
            e = discord.Embed(color=0x2B2D31)
            e.set_author(name=f"{member}", icon_url=member.display_avatar.url)
            e.set_thumbnail(url=member.display_avatar.url)
            e.add_field(
                name="registered", value=f"<t:{int(member.created_at.timestamp())}:F>\n<t:{int(member.created_at.timestamp())}:R>", inline=False)
            e.set_footer(text='ID: ' + str(member.id) +
                         f" | {k} mutual server(s)")
            await sendmsgg(self, ctx, None, e, None, None, None, None)

    @command(help="show server information", aliases=["si", "serverinfo", "guild"], description="utility", usage="[subcommand] <server id>", brief="server info - shows server info\nserver avatar - shows server's avatar\nserver banner - shows server's banner\nserver splash - shows server's invite background")
    @cooldown(1, 4, BucketType.user)
    @blacklist()
    async def server(self, ctx: Context, choice=None, *, id: int=None):
      if choice == "info" or choice is None:
        if id is None:
           guild = ctx.guild
        else:
            guild = self.bot.get_guild(id)
        
        if guild is None:
            e = Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention}: unable to find this guild")
            await sendmsg(self, ctx, None, e, None, None, None)
            return 

        i=0
        j=0
        icon=""
        splash=""
        banner=""  
        if guild.icon is not None:
         icon = f"[icon]({guild.icon.url})"
        else:
         icon = "no icon"

        if guild.splash is not None:
         splash = f"[splash]({guild.splash.url})"
        else:
         splash = "no splash"

        if guild.banner is not None:
         banner = f"[banner]({guild.banner.url})"
        else:
         banner = "no banner"

        for member in guild.members:  
         if member.bot:
            j+=1
         else:
            i+=1 
        if guild.description is None:
            desc = ""
        else:
            desc = guild.description 
        
        if guild.premium_subscriber_role is None:
            b = 0
        else:
            b = len(guild.premium_subscriber_role.members) 

       #embed = Embed(color=0x2B2D31, title=f"{guild.name} ・ shard {guild.shard_id}/{self.bot.shard_count-1}", description=f"created <t:{int(guild.created_at.timestamp())}:F> (<t:{int(guild.created_at.timestamp())}:R>)\n{desc}")   
        embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="owner", value=f"{guild.owner.mention}\n{guild.owner}")
        embed.add_field(name=f"channels ({len(ctx.guild.channels)})", value=f"**text:** {len(guild.text_channels)}\n**voice:** {len(guild.voice_channels)}\n**categories** {len(guild.categories)}")
        embed.add_field(name="members", value=f"**users:** {i} ({(i/guild.member_count) * 100:.2f}%)\n**bots:** {j} ({(j/guild.member_count) * 100:.2f}%)\n**total:** {guild.member_count}")
        embed.add_field(name="links", value=f"{icon}\n{splash}\n{banner}")
        embed.add_field(name="info", value=f"**verification:** {guild.verification_level}\n**vanity:** {guild.vanity_url_code}")
        embed.add_field(name="counts", value=f"**roles:** {len(guild.roles)}/250\n**boosts:** {guild.premium_subscription_count} (level {guild.premium_tier})\n**boosters:** {b}\n**emojis:** {len(guild.emojis)}/{guild.emoji_limit*2}\n**stickers:** {len(guild.stickers)}/{guild.sticker_limit}")
        embed.set_footer(text=f"ID: {guild.id}")
        await sendmsg(self, ctx, None, embed, None, None, None)
      elif choice == "banner":
        if id is None:
           guild = ctx.guild
        else:
            guild = self.bot.get_guild(id)
        
        if guild is None:
            e = Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention}: unable to find this guild")
            await sendmsg(self, ctx, None, e, None, None, None)
            return 

        if not guild.banner:
            em = Embed(color=Colors.yellow, description=f"{Emojis.wrong} {ctx.author.mention}: this server has no banner")
            await sendmsg(self, ctx, None, em, None, None, None)
            return 

        embed = Embed(color=0x2B2D31, title=f"{guild.name}'s banner", url=guild.banner.url)   
        embed.set_image(url=guild.banner.url)
        await sendmsg(self, ctx, None, embed, None, None, None)
      elif choice == "avatar" or choice == "icon":
        if id is None:
           guild = ctx.guild
        else:
            guild = self.bot.get_guild(id)
        
        if guild is None:
            e = Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention}: unable to find this guild")
            await sendmsg(self, ctx, None, e, None, None, None)
            return 

        if not guild.icon:
            em = Embed(color=Colors.yellow, description=f"{Emojis.wrong} {ctx.author.mention}: this server has no icon")
            await sendmsg(self, ctx, None, em, None, None, None)
            return 

        embed = Embed(color=0x2B2D31, title=f"{guild.name}'s avatar", url=guild.icon.url)   
        embed.set_image(url=guild.icon.url)
        await sendmsg(self, ctx, None, embed, None, None, None)   
      elif choice == "splash":
        if id is None:
           guild = ctx.guild
        else:
            guild = self.bot.get_guild(id)
        
        if guild is None:
            e = Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention}: unable to find this guild")
            await sendmsg(self, ctx, None, e, None, None, None)
            return 

        if not guild.splash:
            em = Embed(color=Colors.yellow, description=f"{Emojis.wrong} {ctx.author.mention}: this server has no splash")
            await sendmsg(self, ctx, None, em, None, None, None)
            return 

        embed = Embed(color=0x2B2D31, title=f"{guild.name}'s splash", url=guild.splash.url)   
        embed.set_image(url=guild.splash.url)
        await sendmsg(self, ctx, None, embed, None, None, None)
      else:
        await commandhelp(self, ctx, ctx.command.name)  

    @command(help="shows the number of invites an user has", usage="<user>", description="utility")
    @cooldown(1, 3, BucketType.user)
    @blacklist()
    async def invites(self, ctx: Context, *, member: Member=None):
      if member is None: member = ctx.author 
      inviteuses = 0 
      invites = await ctx.guild.invites()
      for invite in invites:
        if invite.inviter.id == member.id:
         inviteuses = inviteuses + invite.uses
      await sendmsg(self, ctx, f"{member} has **{inviteuses}** invites", None, None, None, None)

    @command(help="gets the invite link with administrator permission of a bot", description="utility", usage="[bot id]")
    @cooldown(1, 4, BucketType.user)
    @blacklist()
    async def getbotinvite(self, ctx, id: User=None):
     if id is None:
        await commandhelp(self, ctx, ctx.command.name)
        return
     else:    
      if not id.bot: return await sendmsg(self, ctx, "this isn't a bot", None, None, None, None)
      embed = Embed(color=0x2B2D31, description=f"**[invite the bot](https://discord.com/api/oauth2/authorize?client_id={id.id}&permissions=8&scope=bot%20applications.commands)**")
      await sendmsg(self, ctx, None, embed, None, None, None)
   
    @command(help="gets the banner from a server based by invite code\n(pretend doesn't need to be in the server)", description="utility", usage="[invite code]")
    @cooldown(1, 4, BucketType.user)
    @blacklist()
    async def sbanner(self, ctx, *, link=None):
     if link == None:
      await commandhelp(self, ctx, ctx.command.name)
      return  

     invite_code = link
     async with aiohttp.ClientSession() as cs:
      async with cs.get(DISCORD_API_LINK + invite_code) as r:
       data = await r.json()

     try: 
      format = ""
      if "a_" in data["guild"]["banner"]:
        format = ".gif"
      else:
        format = ".png"

      embed = Embed(color=0x2B2D31, title=data["guild"]["name"] + "'s banner")
      embed.set_image(url="https://cdn.discordapp.com/banners/" + data["guild"]["id"] + "/" + data["guild"]["banner"] + f"{format}?size=1024")
      await sendmsg(self, ctx, None, embed, None, None, None)
     except:
      e = Embed(color=Colors.red, description=f"{Emojis.wrong} {ctx.author.mention}: Couldn't get **" + data["guild"]["name"] + "'s** banner")
      await sendmsg(self, ctx, None, e, None, None, None)
    @command(help=f"gets the splash from a server based by invite code\nuse doesn't need to be in the server)", description="utility", usage="[invite code]")
    @cooldown(1, 4, BucketType.user)
    @blacklist()
    async def splash(self, ctx, *, link=None):
     if link == None:
      await commandhelp(self, ctx, ctx.command.name)
      return

     try: 
      invite_code = link
      async with aiohttp.ClientSession() as cs:
       async with cs.get(DISCORD_API_LINK + invite_code) as r:
        data = await r.json()

      embed = Embed(color=0x2B2D31, title=data["guild"]["name"] + "'s splash")
      embed.set_image(url="https://cdn.discordapp.com/splashes/" + data["guild"]["id"] + "/" + data["guild"]["splash"] + ".png?size=1024")
      await sendmsg(self, ctx, None, embed, None, None, None)
     except:
      e = Embed(color=Colors.red, description=f"{Emojis.wrong} {ctx.author.mention}: Couldn't get **" + data["guild"]["name"] + "'s** splash image")
      await sendmsg(self, ctx, None, e, None, None, None)

    @command(help="gets the icon from a server based by invite code", description="utility", usage="[invite code]")
    @blacklist()
    async def sicon(self, ctx, *, link=None):
      if link == None:
        embed = Embed(color=0x2B2D31, title=f"{ctx.guild.name}'s icon")
        embed.set_image(url=ctx.guild.icon)
        await sendmsg(self, ctx, None, embed, None, None, None)
      else:
        invite_code = link
        async with aiohttp.ClientSession() as cs:
          async with cs.get(DISCORD_API_LINK + invite_code) as r:
            data = await r.json()

          format = ""
          if "a_" in data["guild"]["icon"]:
            format = ".gif"
          else:
            format = ".png"
              
          embed = Embed(color=0x2B2D31, title=f"{ctx.guild.name}'s icon")
          embed.set_image(url="https://cdn.discordapp.com/icons/" + data["guild"]["id"] + "/" + data["guild"]["icon"] + f"{format}?size=1024")
          await sendmsg(self, ctx, None, embed, None, None, None)           
  
    @command(help="gets information about a github user", aliases=["gh"], description="utility", usage="[user]")
    @cooldown(1, 4, BucketType.user)
    @blacklist()
    async def github(self, ctx, *, user=None):
        if user == None:
            await commandhelp(self, ctx, ctx.command.name)
            return
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f'https://api.github.com/users/{user}') as r:
                    res = await r.json()
                    name=res['login']
                    avatar_url=res['avatar_url']
                    html_url=res['html_url']
                    email=res['email']
                    public_repos=res['public_repos']
                    followers=res['followers']
                    following=res['following']
                    twitter = res['twitter_username']
                    location=res['location']
                    embed = Embed(color=0x2B2D31, title = f"@{name}", url=html_url)
                    embed.set_thumbnail(url=avatar_url)
                    embed.add_field(name="Followers", value=followers)
                    embed.add_field(name="Following", value=following)
                    embed.add_field(name="Repos", value=public_repos)
                    if email:
                        embed.add_field(name="Email", value=email)
                    if location:
                        embed.add_field(name="Location", value=location)
                    if twitter:
                        embed.add_field(name="Twitter", value=twitter)
                    
                    embed.set_thumbnail(url=avatar_url)
                    await sendmsg(self, ctx, None, embed, None, None, None)
        except:
            e = Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention}: Could not find [@{user}](https://github.com/@{user})")
            await sendmsg(self, ctx, None, e, None, None, None) 

    @command(aliases=["tr"], description="translate a message", help="utility", usage="[language] [message]")
    @cooldown(1, 4, BucketType.user)
    @blacklist()
    async def translate(self, ctx: Context, lang: str, *, mes: str): 
      translated = GoogleTranslator(source="auto", target=lang).translate(mes)
      embed = Embed(color=Colors.yellow, description="```{}```".format(translated), title="translated to {}".format(lang))
      await ctx.reply(embed=embed)

    @command(aliases=["firstmsg"], description="utility", help="get the first message", usage="<channel>")
    @cooldown(1, 4, BucketType.user)
    @blacklist()
    async def firstmessage(self, ctx: Context, *, channel: TextChannel=None):
     channel = channel or ctx.channel 
     messages = [mes async for mes in channel.history(oldest_first=True, limit=1)]
     message = messages[0]
     embed = Embed(color=0x2B2D31, title="first message in #{}".format(channel.name), description=message.content, timestamp=message.created_at)
     embed.set_author(name=message.author, icon_url=message.author.display_avatar)
     view = View()
     view.add_item(Button(label="jump to message", url=message.jump_url))
     await ctx.reply(embed=embed, view=view) 
  

    @command(description="utility", help="see all members joined within 24 hours")
    @cooldown(1, 4, BucketType.user)
    @blacklist()
    async def joins(self, ctx: Context): 
      members = [m for m in ctx.guild.members if (datetime.datetime.now() - m.joined_at.replace(tzinfo=None)).total_seconds() < 3600*24]      
      if len(members) == 0: return await ctx.send("no members joined in the last **24** hours")
      members = sorted(members, key=lambda m: m.joined_at)
      i=0
      k=1
      l=0
      mes = ""
      number = []
      messages = []
      for member in members[::-1]: 
        mes = f"{mes}`{k}` {member} - {discord.utils.format_dt(member.joined_at, style='R')}\n"
        k+=1
        l+=1
        if l == 10:
         messages.append(mes)
         number.append(Embed(color=Colors.yellow, title=f"joined today [{len(members)}]", description=messages[i]))
         i+=1
         mes = ""
         l=0
    
      messages.append(mes)
      embed = Embed(color=Colors.yellow, title=f"joined today [{len(members)}]", description=messages[i])
      number.append(embed)
      await ctx.paginator( number)
    
    @command(description="utility", help="see all muted mebmers")
    async def muted(self, ctx: Context): 
            members = [m for m in ctx.guild.members if m.is_timed_out()]
            if len(members) == 0: return await ctx.send("there are no muted members")
            i=0
            k=1
            l=0
            mes = ""
            number = []
            messages = []
            for member in members: 
              mes = f"{mes}`{k}` {member} - <t:{int(member.timed_out_until.timestamp())}:R> \n"
              k+=1
              l+=1
              if l == 10:
               messages.append(mes)
               number.append(Embed(color=Colors.yellow, title=f"{ctx.guild.name} muted members [{len(members)}]", description=messages[i]))
               i+=1
               mes = ""
               l=0
    
            messages.append(mes)
            embed = Embed(color=Colors.yellow, title=f"{ctx.guild.name} muted members [{len(members)}]", description=messages[i])
            number.append(embed)
            await ctx.paginator( number)      

    @commands.hybrid_command(
        name='bans',
        usage= "bans",
        aliases=["banlist"],
        description="show a list of the server's banned members",
        extras={'permissions': 'ban members'}
    )
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def bans(self, ctx: Context):

        if not [b async for b in ctx.guild.bans(limit=1)]:
            return await ctx.send_error(f"there aren't any **bans** in {ctx.guild.name}")
            
        embed = discord.Embed(color=Colors.default, title=f'Bans in {ctx.guild.name}', description='')  # Initialize as an empty string
        async for ban in ctx.guild.bans(limit=10):
            embed.description += f'{ban.user.mention}: **{ban.user}** ( `{ban.user.id}` )\n'  # Concatenate the string

        paginator = pg.Paginator(self.bot, [embed], ctx, invoker=None)  # Pass embed as a list
        paginator.add_button("prev", emoji="<:left:1107307769582850079>")
        paginator.add_button("goto", emoji="<:filter:1113850464832868433>")
        paginator.add_button("next", emoji="<:right:1107307767041105920>")
        paginator.add_button("delete", emoji="<:page_cancel:1121826948520362045>")
        await paginator.start()

    @commands.hybrid_command(
        description="shows application info",
        usage="appinfo <botid>",
        aliases=["ai", "app", "a", "app-info"]
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def appinfo(self, ctx, id: int):
        try:
            response = await self.bot.session.get(f"https://discord.com/api/applications/{id}/rpc")
            res = await response.json()
        except:
            return await ctx.reply("Invalid application id")

        avatar = f"https://cdn.discordapp.com/avatars/{res['id']}/{res['icon']}.png?size=1024"

        embed = discord.Embed(color=0x2B2D31, title=res["name"], description=res["description"] or "No description for this application found")
        embed.add_field(
            name="general",
            value=f"**id**: {res['id']}\n**name**: {res['name']}\n**bot public**: {res['bot_public']}\n**bot require code grant**: {res['bot_require_code_grant']}",
        )
        embed.set_thumbnail(url=avatar)

        return await ctx.reply(embed=embed)

    @command(help=f"reverse image searches your image", description="utility", usage="[image]", aliases=["rev"])
    @blacklist()
    async def reverse(self, ctx, *, img):
        try:
            link=f"https://images.google.com/searchbyimage?image={img}"
            em = discord.Embed(description=f"{ctx.author}'s reverse search", color=Colors.yellow).set_footer(text=f"Requested by {ctx.author}")
            view = discord.ui.View()
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.link, label='reverse', url=link))
            await ctx.send(embed=em, view=view)
        except Exception as e:
            print(f"[ERROR]: {e}")
    
    @command(help=f"reverse image searches your avatar", description="utility", usage="[user]", aliases=["revav", "rav"])
    @blacklist()
    async def reverseav(self, ctx, *, user: Union[discord.Member, discord.User] = None):
        if user is None:
            user = ctx.author
        if isinstance(user, int):
            user = await self.bot.fetch_user(user)
        try:
            link=f"https://images.google.com/searchbyimage?image={user.display_avatar}"
            em = discord.Embed(color=Colors.yellow, description=f"{user.name}'s reverse search").set_footer(text=f"Requested by {ctx.author}")
            view = discord.ui.View()
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.link, label=f"{user.name}'s revav", url=link))
            await ctx.send(embed=em, view=view)
        except Exception as e:
            print(f"[ERROR]: {e}")

    @commands.hybrid_command(aliases=["webshoty", "sa"])
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def webshot(self, ctx, *, link:str = None) -> None:
      if link == None:
          em = discord.Embed(color=0x2f3136,description=f"> You dont type a __site__ for search")
          await ctx.send(embed=em)
          return
      links = ["https://", "http://"]
      if not (link.startswith(tuple(links))):
          await ctx.send(embed=discord.Embed(color=0x2f3136, description=f"> You didn't input __https __ before the link provided"))
          return
      else:
          n = discord.Embed(description=f"> Preview {link.replace('https://', '').replace('http://', '')}", color=0x2f3136)
          n.set_image(url='https://screenshot.abstractapi.com/v1/?api_key=0dafa21d1dee43189b2931633e447892&url=' + str(link.replace("http://", "https://")))
          await ctx.reply(embed=n, mention_author=False)

    @command(help=f"deletes the channel and clones it", description="utility", usage="[NONE]", aliases=['clone'])
    @blacklist()
    async def nuke(self, ctx):
        if not ctx.author.guild_permissions.manage_channels:
            await noperms(self, ctx, "manage_channels")
            return
        invoker = ctx.author.id
        channel = ctx.channel

        class disabledbuttons(discord.ui.View):
            @discord.ui.button(
                style=discord.ButtonStyle.grey,
                disabled=True,
                emoji=Emojis.check,
            )
            async def confirm(
                self, interaction: discord.Interaction, button: discord.Button
            ):

                if interaction.user.id != invoker:
                    return
                await channel.delete()
                ch = await interaction.channel.clone(
                    name=interaction.channel.name,
                    reason=f"original channel nuked by {invoker}",
                )
                ch = await interaction.guild.fetch_channel(ch.id)
                e = discord.Embed(description=f"<@{invoker}>: channel has been nuked successfully", color=Colors.yellow)
                await ch.send(embed=e)

            @discord.ui.button(
                style=discord.ButtonStyle.grey,
                disabled=True,
                emoji=Emojis.wrong,
            )
            async def cancel(
                self, interaction: discord.Interaction, button: discord.Button
            ):
                embed = discord.Embed(description="Are you sure you want to nuke this channel?\nIt will remove all webhooks and invites.", color=Colors.yellow)
                await interaction.response.edit_message(content=None, embed=embed, view=None)
                embed = discord.Embed(description=f"<@{interaction.user.id}>: channel nuke has been cancelled", color=0xf7f9f8)
                await interaction.channel.send(embed=embed)

        class buttons(discord.ui.View):
            @discord.ui.button(
                style=discord.ButtonStyle.grey, emoji=Emojis.check
            )
            async def confirm(
                self, interaction: discord.Interaction, button: discord.Button
            ):

                if interaction.user.id != invoker:
                    return
                await channel.delete()
                ch = await interaction.channel.clone(
                    name=interaction.channel.name,
                    reason=f"original channel nuked by {invoker}",
                )
                ch = await interaction.guild.fetch_channel(ch.id)
                e = discord.Embed(description=f"<@{invoker}>: channel has been nuked successfully", color=Colors.yellow)
                await ch.send(embed=e)

            @discord.ui.button(
                style=discord.ButtonStyle.grey, emoji=Emojis.wrong
            )
            async def cancel(
                self, interaction: discord.Interaction, button: discord.Button
            ):
                embed = discord.Embed(description="Are you sure you want to nuke this channel?\nIt will remove all webhooks and invites.", color=Colors.yellow)
                await interaction.response.edit_message(content=None, embed=embed, view=disabledbuttons())
                embed = discord.Embed(description=f"<@{interaction.user.id}>: channel nuke has been cancelled", color=Colors.yellow)
                await interaction.channel.send(embed=embed)
        embed = discord.Embed(description="Are you sure you want to nuke this channel?\nIt will remove all webhooks and invites.", color=Colors.yellow)
        await ctx.reply(embed=embed, view=buttons())
        
    @commands.hybrid_command(help="build a custom embed", description="utility")
    @commands.cooldown(1, 4, commands.BucketType.user)
    @blacklist()
    async def embed(self, ctx: commands.Context, *, code):
     if not ctx.author.guild_permissions.manage_guild: 
       await noperms(self, ctx, "manage_guild")
       return 
     await ctx.channel.typing()
     x = await to_object(code)
     await ctx.send(**x)


    @commands.hybrid_command(name = "color", description = "View hex color",aliases=["hex"], usage = "hex [color]")
    @commands.cooldown(1, 3, commands.BucketType.guild)
    async def color(self, ctx, hex_code: str):
        try:
            # Remove the '#' symbol from the hex code if present
            hex_code = hex_code.strip("#")

            # Convert the hex code to an integer
            color_int = int(hex_code, 16)

            # Create a color object from the integer value
            color = discord.Color(color_int)

            # Create the embed
            embed = discord.Embed(
                title="Color",
                description=f"Hex Code: {hex_code}",
                color=color
            )
            embed.set_thumbnail(url=f"https://dummyimage.com/200x200/{hex_code}/{hex_code}.png")

            await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"<:mirodeny:1117144156507209829> An error occurred: {e}",
                color=0xfc5b6d
            )
            await ctx.send(embed=embed)


    @commands.hybrid_command(name = "extract", description = "show dominant color from image",aliases=["et"], usage = "et [attachment]")
    async def extract(self, ctx, attachment: discord.Attachment):
        try:
            image_data = await attachment.read()
            image = Image.open(BytesIO(image_data))
            image = image.resize((200, 200))

            dominant_color = self.extract_dominant_color(image)
            color_image_url = self.upload_color_image(dominant_color)

            embed = discord.Embed(
                title="Dominant Color",
                description="Here is the dominant color extracted from the image:",
                color=int(dominant_color[1:], 16)  # Convert hex color to decimal color value
            )
            embed.add_field(
                name="Hex Color",
                value=dominant_color,
                inline=True
            )
            embed.set_thumbnail(url=color_image_url)

            await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"<:mirodeny:1117144156507209829> An error occurred: {e}",
                color=0xfc5b6d
            )
            await ctx.send(embed=embed)

    def extract_dominant_color(self, image):
        temp_file = "temp_image.png"
        image.save(temp_file)

        color_thief = ColorThief(temp_file)
        dominant_color = color_thief.get_color(quality=1)

        hex_color = '#{:02x}{:02x}{:02x}'.format(dominant_color[0], dominant_color[1], dominant_color[2])

        return hex_color

    def upload_color_image(self, hex_color):
        url = f"https://dummyimage.com/100x100/{hex_color[1:]}/{hex_color[1:]}.png"
        response = requests.get(url)
        if response.status_code == 200:
            return url
        return None
    
    @commands.hybrid_command(description="utility")
    async def vote(self, ctx):
        button = discord.ui.Button(label="vote use", style=discord.ButtonStyle.url, url="https://top.gg/bot/1094942437820076083/vote")
        view = discord.ui.View()
        view.add_item(button)
        await ctx.reply(view=view)


async def setup(bot):
    await bot.add_cog(Utilityy(bot))        