import discord, pytz, humanize, os, arrow, humanfriendly, asyncio, json, aiohttp, requests, random, re, datetime,  humanfriendly, instaloader, time
from datetime import timedelta, timezone, datetime
from timezonefinder import TimezoneFinder
from typing import Optional, Union
from discord import Message, Member, User, Embed, Guild, Invite
from discord.ext.commands import has_permissions, Cog, command, Context, AutoShardedBot as Bot, hybrid_command, hybrid_group, group, check, MissingPermissions, MissingRequiredArgument
from time import perf_counter
from io import BytesIO
from jishaku.math import mean_stddev
from discord.ext import commands
from discord import Embed, File, TextChannel, Member, User, Role
from discord.utils import format_dt



from core import Slut

user_afk_status = {}

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds)

def human_format(number):
    if number > 999: return humanize.naturalsize(number, False, True) 
    return number 


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
       async with cs.get("https://www.mit.edu/~ecprice/wordlist.10000") as r: 
        byte = await r.read()
        data = str(byte, 'utf-8')
        return data.splitlines()



class Timezone(object):
  def __init__(self, bot: Bot): 
   """
   Get timezones of people
   """
   self.bot = bot
   self.clock = "🕑"
   self.months = {
     '01': 'January',
     '02': 'February',
     '03': 'March',
     '04': 'April',
     '05': 'May',
     '06': 'June',
     '07': 'July',
     '08': 'August',
     '09': 'September',
     '10': 'October',
     '11': 'November',
     '12': 'December'
   }


class Utility(Cog):
    def __init__(self, bot: Slut) -> None:
        self.bot: Slut = bot
        self.tz = Timezone(self.bot)
        self.timezone = pytz.timezone('America/New_York')
        self.deleted_messages = {}


    async def send_insufficient_permissions_message(self, ctx, permission):
        embed = discord.Embed(
            color=0x2B2D31,
            description=f"> {ctx.author.mention}: You have **insufficient** permissions (`{permission}`) to execute this command."
        )
        await ctx.send(embed=embed)


    def format_afk_time(self, start_time):
        total_seconds = int(time.time() - start_time)
        if total_seconds < 60:
            return f"{total_seconds} second{'s' if total_seconds != 1 else ''}"
        elif total_seconds < 3600:
            minutes = total_seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''}"
        elif total_seconds < 86400:
            hours = total_seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''}"
        else:
            days = total_seconds // 86400
            return f"{days} day{'s' if days != 1 else ''}"


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Check if the message is a command
        ctx = await self.bot.get_context(message)
        if ctx.valid:
            return

        if message.author.id in user_afk_status:
            afk_info = user_afk_status[message.author.id]
            embed = discord.Embed(description=f"> 👋 Welcome back, you were away for **{self.format_afk_time(afk_info['start_time'])}** ", color=0x2f3136)
            await message.reply(embed=embed, mention_author=False)
            user_afk_status.pop(message.author.id)

        mentioned_users = message.mentions
        if mentioned_users:
            for mentioned_user in mentioned_users:
                if mentioned_user.id in user_afk_status:
                    afk_info = user_afk_status[mentioned_user.id]
                    status = afk_info['reason'] if afk_info['reason'] else "AFK"
                    embed = discord.Embed(description=f"> {message.author.mention}: {mentioned_user.mention} is AFK with the status: **{status}** (since **{self.format_afk_time(afk_info['start_time'])}** ago)", color=0x2f3136)
                    await message.reply(embed=embed, mention_author=False)
        await self.bot.process_commands(message)

    @command(name="afk", description="Afk man js afk dude its self-explanitory dude")
    async def afk(self, ctx, *, reason="AFK"):
        await ctx.typing()
        user_afk_status[ctx.author.id] = {
            "start_time": time.time(),
            "reason": reason
        }
        embed = discord.Embed(description=f"> {ctx.author.mention}: You're now **AFK** with the status: **{reason}**", color=0x2f3136)
        await ctx.send(embed=embed)


    def contains_invite_link(self, content):
        invite_pattern = r"(https?:\/\/)?(discord\.(gg|io|me|li)|discordapp\.com\/invite)\/\w+"
        invite_regex = re.compile(invite_pattern)
        return bool(invite_regex.search(content))

    @Cog.listener()
    async def on_message_delete(self, message):
        if message.content:
            channel_id = message.channel.id
            if channel_id not in self.deleted_messages:
                self.deleted_messages[channel_id] = []

            content = message.content
            if self.contains_invite_link(content):
                content = f"This message contains an invite link."

            self.deleted_messages[channel_id].append((content, message.author.name, message.created_at))


    @command(aliases=['s'])
    async def snipe(self: "Utility", ctx, index: int = 1):
        channel_id = ctx.channel.id
        if channel_id in self.deleted_messages:
            deleted_list = self.deleted_messages[channel_id]
            total_deleted = len(deleted_list)
            if 1 <= index <= total_deleted:
                content, author, created_at = deleted_list[-index]

                embed = discord.Embed(description=content, color=0x2f3136)
                embed.set_author(name=author)

                central_tz = pytz.timezone('America/New_York')
                created_at_central = created_at.astimezone(central_tz)

                embed.set_footer(text=f"{index}/{total_deleted}  |  {created_at_central.strftime('%I:%M %p')}")


                await ctx.send(embed=embed)
            else:
                await ctx.send("Invalid message.")
        else:
            await ctx.send("No recently deleted messages to snipe.")


    @command(help="play blacktea with your friends", description="fun")
    async def blacktea(self, ctx: Context): 
     try:
      if BlackTea.MatchStart[ctx.guild.id] is True: 
       return await ctx.reply("somebody in this server is already playing blacktea", mention_author=False)
     except KeyError: pass 

     BlackTea.MatchStart[ctx.guild.id] = True 
     embed = Embed(color=0x2B2D31, title="BlackTea Matchmaking", description=f"⏰ Waiting for players to join. To join react with 🍵.\nThe game will begin in **20 seconds**")
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
       

    @command(name='clearsnipe', aliases=['cs'])
    async def clearsnipe(self, ctx):
          channel_id = ctx.channel.id
          if ctx.author.guild_permissions.manage_messages:
           if channel_id in self.deleted_messages:
            del self.deleted_messages[channel_id]
            await ctx.message.add_reaction("✅")
          else:
             embed = discord.Embed(color=0x2B2D31, description=f"> {ctx.author.mention}: You have **insufficient** permissions (`manage_messages`) to execute permission to execute `clearsnipe`.")
             await ctx.send(embed=embed)

    @command(name="icon")
    async def icon(
        self: "Information",
        ctx: Context,
        *,
        server: Optional[Guild | Invite],
    ) -> Message:
        server = server or ctx.guild

        if isinstance(server, Invite):
            server = server.guild

        if not server.icon:
            return await ctx.send("No server icon")

        embed = Embed(
            color=0x2B2D31,
            title=f"{server.name}'s icon",
            url=server.icon
        )
        embed.set_image(
            url=server.icon
        )

        return await ctx.send(embed=embed)

    @command(
        name="avatar",
        aliases=["av"],
    )
    async def avatar(
        self: "Information",
        ctx: Context,
        *,
        user: Optional[Member | User],
    ) -> Message:
        """ 
        Get the avatar of a member or user.
        """

        user = user or ctx.author

        embed = Embed(
            color=0x2B2D31,
            url=user.display_avatar,
            title=f"{user.name}'s avatar",
        )
        embed.set_image(url=user.display_avatar)

        return await ctx.send(embed=embed)

    @command(aliases=['ig'])
    async def instagram(self, ctx, ig_username):
        await ctx.typing()
        self.loader = instaloader.Instaloader()
        try:
            profile = instaloader.Profile.from_username(self.loader.context, ig_username)

 
            embed = discord.Embed(title=f'@{profile.username}', color=0x2B2D31)
            embed.set_thumbnail(url=profile.profile_pic_url)
            embed.add_field(name='Posts', value=str(profile.mediacount), inline=True)
            embed.add_field(name='Followers', value=str(profile.followers), inline=True)
            embed.add_field(name='Following', value=str(profile.followees), inline=True)


            await ctx.send(embed=embed)

        except instaloader.ProfileNotExistsException:
            await ctx.send(f'Instagram profile "@{ig_username}" not found.')

    @command(name="nuke")
    @commands.has_permissions(administrator=True)
    async def nuke(self, ctx):
        try:
            if ctx.author == ctx.guild.owner:
                confirmation_message = await ctx.send(embed=discord.Embed(description="Are you sure you want to clone this channel? (y/n)", color=0x2B2D31))

                if confirmation_message:
                    def check(message):
                        return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() in ["y", "n"]

                    try:
                        response_message = await self.bot.wait_for("message", check=check, timeout=30)
                    except asyncio.TimeoutError:
                        await confirmation_message.delete()
                        return await ctx.send("Nuke command timed out.")

                    await confirmation_message.delete()

                    if response_message.content.lower() == "y":
                        channel = ctx.channel
                        new_c = await channel.clone(reason="channel cloned from nuke")
                        await ctx.channel.edit(position=ctx.channel.position)
                        await ctx.channel.delete()
                        await new_c.send("first")
                    else:
                        await ctx.send("Nuke command cancelled.")
                else:
                    await ctx.send("Invalid channel.")
            else:
                embed = discord.Embed(
                    description=f"{ctx.author.mention}: This command can be used only by **{ctx.guild.owner.display_name}**",
                    color=discord.Color.red()
                )
                await ctx.reply(embed=embed)

        except discord.errors.Forbidden:
            await ctx.send("I don't have permissions to delete channels.")

    async def send_insufficient_permissions_message(self, ctx, permission):
        embed = discord.Embed(color=0x2B2D31, description=f"> {ctx.author.mention}: You have **insufficient** permissions (`{permission}`) to execute this command.")
        await ctx.send(embed=embed)

    @command()
    async def steal(self, ctx, emoji: discord.PartialEmoji = None):  
        try:
            if ctx.author.guild_permissions.manage_emojis:
                if emoji is None:
                    raise MissingRequiredArgument("emoji")
                emoji_url = emoji.url
                await ctx.guild.create_custom_emoji(name=emoji.name, image=await emoji.read(), reason="Stolen emoji")
                await ctx.send(f"Emoji `{emoji.name}` has been added to the server.")
            else:
                raise MissingPermissions(["manage_emojis"])
        except MissingPermissions as e:
            await self.send_insufficient_permissions_message(ctx, "manage_emojis")
        except MissingRequiredArgument as e:
            await ctx.send(f"Error: {e}")
        except Exception as e:
            embed = discord.Embed(description=f'Invalid emoji, make sure to provide a valid emoji.')
            await ctx.send(embed=embed)

    @command(aliases=['addemojis', 'add', 'am'])
    async def addmultiple(self, ctx: commands.Context, *emoji: Union[discord.Emoji, discord.PartialEmoji]):
        if not ctx.author.guild_permissions.manage_emojis_and_stickers:
            await self.send_insufficient_permissions_message(ctx, "manage_emojis_and_stickers")
            return

        if len(emoji) == 0:
            return await commandhelp(self, ctx, ctx.command.name)

        if len(emoji) > 20:
            return await ctx.reply("you can only add up to 20 emojis at once")

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

        added_emojis = ', '.join(emojis)
        await ctx.send(f"Added {added_emojis}")

    @command(
        name="enlarge",
        aliases=["e"],
    )
    async def enlarge(self, ctx, emoji: discord.PartialEmoji):
        try:
            emoji_url = emoji.url
            await ctx.send(f"{emoji_url}")
        except Exception as e:
            print(e)
            embed = discord.Embed(description=f'Invalid emoji, make sure to provide a valid emoji.')
            await ctx.send(embed=embed)

    @command(help="see all server's bots", description="utility")     
    async def bots(self, ctx: Context):
        bots = [member for member in ctx.guild.members if member.bot]
        
        if not bots:
            await ctx.send("There are no bots in this server.")
            return

        embed = Embed(color=0x2B2D31, title=f"{ctx.guild.name} bots [{len(bots)}]", description="")

        for i, member in enumerate(bots, start=1):
            embed.description += f"`{i}` {member} - ({member.id})\n"

        await ctx.send(embed=embed)

    @command(aliases=['mc'])
    async def membercount(self: "Information", ctx) -> None:
        human_members = len([member for member in ctx.guild.members if not member.bot])
        bot_members = len([member for member in ctx.guild.members if member.bot])

        embed = discord.Embed(title=f"{ctx.guild.name}'s Member Count", color=0x2B2D31)
        embed.set_thumbnail(url=ctx.guild.icon)
        embed.add_field(name="Total:", value=f"{ctx.guild.member_count}")
        embed.add_field(name="Humans:", value=f"{human_members}")
        embed.add_field(name="Bots:", value=f"{bot_members}")
        await ctx.reply(embed=embed, mention_author=False)

    # Define your convert_datetime method
    def convert_datetime123(self, dt):
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    # Define your convert and human_format methods
    def convert(self, seconds):
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return "%d:%02d:%02d" % (hour, minutes, seconds)

    def human_format(self, number):
        if number > 999:
            return humanize.naturalsize(number, False, True)
        return number

    def convert_datetime123(self, dt):
        dt = dt.astimezone(self.timezone)
        formatted_date = dt.strftime("%m/%d/%Y at %I:%M %p")
        return formatted_date


    def ordinal(self, n):
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10 if n % 10 < 4 and n % 100 not in {11, 12, 13} else 0, 'th')
        return f"{n}{suffix}"

    def convert_datetime(self, dt):
        relative_time = format_dt(dt, "R")
        specific_time = dt.strftime("%m/%d/%y at %I:%M %p")
        return f"{specific_time} ({relative_time})"

    @command(name="userinfo", aliases=['ui'])
    async def userinfo(self, ctx: Context, *, member: Union[Member, User] = None):
        await ctx.typing()
        if member is None:
            member = ctx.author

        if isinstance(member, Member):
            members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
            author_index = members.index(ctx.author) + 1
            author_position = self.ordinal(author_index)
            member_index = members.index(member) + 1
            member_position = self.ordinal(member_index)
            formatted_time = self.convert_datetime(member.joined_at)

            e = Embed(description=f"**joined:** {formatted_time}\n**created:** {self.convert_datetime(member.created_at)}", color=member.color)
            e.set_author(name=f"{ctx.author.name} • {author_position} member", icon_url=member.display_avatar.url)

            roles = member.roles[1:][::-1]
            if len(roles) > 0:
                e.add_field(name=f"roles ({len(roles)})", value=' '.join([r.mention for r in roles]) if len(roles) < 5 else ' '.join([r.mention for r in roles[:4]]) + f" ... and {len(roles)-4} more")

            e.set_thumbnail(url=member.display_avatar.url)

            try:
                e.set_footer(text='ID: ' + str(member.id) + f" | {len(member.mutual_guilds)} mutual server(s)")
            except AttributeError:
                e.set_footer(text='ID: ' + str(member.id))

            await ctx.reply(embed=e)


    @command(
      name="serverinfo",
      description="shows the information for your server",
      aliases=["si"]
    )
    async def server(self, ctx: Context, choice=None, *, id: int=None):
      if choice == "info" or choice is None:
        if id is None:
           guild = ctx.guild
        else:
            guild = self.bot.get_guild(id)
        
        if guild is None:
            e = Embed(color=0x2B2D31, description=f"> {ctx.author.mention}: unable to find this guild")
            await ctx.send(embed=e)
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

        embed = Embed(color=0x2B2D31, title=guild.name, description=f"created <t:{int(guild.created_at.timestamp())}:F> (<t:{int(guild.created_at.timestamp())}:R>)\n{desc}")   
        if guild.icon is not None:
            embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="owner", value=f"{guild.owner.mention}\n{guild.owner}")
        embed.add_field(name=f"channels ({len(ctx.guild.channels)})", value=f"**text:** {len(guild.text_channels)}\n**voice:** {len(guild.voice_channels)}\n**categories** {len(guild.categories)}")
        embed.add_field(name="members", value=f"**users:** {i} ({(i/guild.member_count) * 100:.2f}%)\n**bots:** {j} ({(j/guild.member_count) * 100:.2f}%)\n**total:** {guild.member_count}")
        embed.add_field(name="links", value=f"{icon}\n{splash}\n{banner}")
        embed.add_field(name="info", value=f"**verification:** {guild.verification_level}\n**vanity:** {guild.vanity_url_code}")
        embed.add_field(name="counts", value=f"**roles:** {len(guild.roles)}/250\n**boosts:** {guild.premium_subscription_count} (level {guild.premium_tier})\n**boosters:** {b}\n**emojis:** {len(guild.emojis)}/{guild.emoji_limit*2}\n**stickers:** {len(guild.stickers)}/{guild.sticker_limit}")
        embed.set_footer(text=f"ID: {guild.id}")
        await ctx.send(embed=embed)
      elif choice == "banner":
        if id is None:
           guild = ctx.guild
        else:
            guild = self.bot.get_guild(id)
        
        if guild is None:
            e = Embed(color=0x2B2D31, description=f"{Emojis.warning} {ctx.author.mention}: unable to find this guild")
            await ctx.send(embed=e)
            return 

        if not guild.banner:
            em = Embed(color=0x2B2D31, description=f"> {ctx.author.mention}: this server has no banner")
            await ctx.send(embed=em)
            return 

        embed = Embed(color=0x2B2D31, title=f"{guild.name}'s banner", url=guild.banner.url)   
        embed.set_image(url=guild.banner.url)
        await ctx.send(embed=embed)
      elif choice == "avatar" or choice == "icon":
        if id is None:
           guild = ctx.guild
        else:
            guild = self.bot.get_guild(id)
        
        if guild is None:
            e = Embed(color=0x2B2D31, description=f"{Emojis.warning} {ctx.author.mention}: unable to find this guild")
            await ctx.send(embed=e)
            return 

        if not guild.icon:
            em = Embed(color=0x2B2D31, description=f"> {ctx.author.mention}: this server has no icon")
            await ctx.send(embed=em)
            return 
        
        if guild.icon is not None:
            embed = Embed(color=0x2B2D31, title=f"{guild.name}'s avatar", url=guild.icon.url)   
            embed.set_image(url=guild.icon.url)
            await ctx.send(embed=embed)  
      elif choice == "splash":
        if id is None:
           guild = ctx.guild
        else:
            guild = self.bot.get_guild(id)
        
        if guild is None:
            e = Embed(color=0x2B2D31, description=f"> {ctx.author.mention}: unable to find this guild")
            await ctx.send(embed=em)
            return 

        if not guild.splash:
            embed = Embed(color=0x2B2D31, description=f"> {ctx.author.mention}: this server has no splash")
            await ctx.reply(embed=embed)
            return 

        embed = Embed(color=0x2B2D31, title=f"{guild.name}'s splash", url=guild.splash.url)   
        embed.set_image(url=guild.splash.url)
        await ctx.reply(embed=embed)