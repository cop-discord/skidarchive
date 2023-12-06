from asyncore import loop
import random
import discord_ios
import time
import discord
import requests
import psutil
import datetime
import jishaku
import asyncio
import sys
import os
import time
import aiohttp
from discord import Member, User
from typing import Union, Optional
from jishaku.features.baseclass import Feature
from jishaku.flags import Flags
from jishaku.math import mean_stddev
from jishaku.modules import ExtensionConverter
from jishaku.repl import inspections
from jishaku.types import ContextA
from discord.ext import commands
color = 0x2B2D31
warn = 0xFFD43A
approve = 0x84EE91

tostop = 0

intents = discord.Intents.all()


default = discord.Embed()

rh = commands.Bot(command_prefix=";", intents=intents, help_command=None,
            owner_ids=[1148300105758298123, 1055512125986050069]
    )

rh.channel_cd = commands.CooldownMapping.from_cooldown(3, 5, commands.BucketType.channel)
rh.user_cd = commands.CooldownMapping.from_cooldown(3, 5, commands.BucketType.user)


rh.deleted_messages = {}

async def noperms(self, ctx, permission):
    await ctx.send(f"{ctx.author.mention}: you are missing permission `{permission}`")



    def channel_cooldown(self, message: discord.Message) -> Optional[int]:
        bucket = self.channel_cd.get_bucket(message)
        return bucket.update_rate_limit()
    
    def user_cooldown(self, message: discord.Message) -> Optional[int]:
        bucket = self.user_cd.get_bucket(message)
        return bucket.update_rate_limit()

    def cooldown(self, message: discord.Message) -> bool: 
        if self.channel_cooldown(message) or self.user_cooldown(message):
            return True 

        return False

blacklisted_users = [366379400389984277]

def randnum(fname):
  lines = open(fname).read().splitlines()
  return random.choice(lines)

rh._uptime = time.time()

@rh.event
async def on_guild_join(guild):
    # Set the bot's nickname to 'wockhardt' when it joins a new server
    await guild.me.edit(nick='social')
    print(f'Changed nickname to "wockhardt" in {guild.name}')

@rh.event
async def on_ready() -> None:
  print(f"Connected to {rh.user}")
  print(f"Bot ID : {rh.user.id}")
  await rh.load_extension("jishaku")
  await rh.change_presence(status=discord.Status.invisible)

allowed = []


@rh.command()
async def stop(ctx): 
  global tostop
  if ctx.author.id == 1148300105758298123 or ctx.author.id == 1055512125986050069 or allowed:
    tostop += 1
    embed = discord.Embed(description="<:approve:1148728529412948018> stopping pfps", color=approve)
    await ctx.send(embed=embed)
  else:
      embed = discord.Embed(description="<:warning:1148728334377820260> this command is **premium**", color=warn)
      await ctx.send(embed=embed)


@rh.command()
async def sendpfps(ctx):
  global tostop
  if ctx.author.id == 1148300105758298123 or ctx.author.id == 1055512125986050069 or allowed: #kindly change the id names to your id's.
    tostop = 0
    embed = discord.Embed(description="<:approve:1148728529412948018> sending pfps", color=approve)
    await ctx.send(embed=embed)
    while tostop == 0:

      embed = discord.Embed(color=0x2B2D31)
      embed.set_image(url=randnum('scraped.txt'))
      await ctx.send(embed=embed)
      time.sleep(3)
  else:
      embed = discord.Embed(description="<:warning:1148728334377820260> this command is **premium**", color=warn)
      await ctx.send(embed=embed)



@rh.command()
async def help(ctx): 
    embed = discord.Embed(title=f"saint", description=f"""**Invite**: [Click here](https://discord.com/api/oauth2/authorize?client_id=1024259879696859146&permissions=8&scope=bot%20applications.commands)\n**Support**: [Click here](https://discord.gg/lied)""",color=color)
    embed.add_field(name="**Information**",value=""" `rtt`, `ping`, `uptime`, `stats`, `invite`, `greed`, `commands`""",inline=False)
    embed.add_field(name="**Utility**",value="""`invites`, `enlarge`, `steal`, `membercount`, `botlist`""",inline=False)
    embed.add_field(name="**Moderation**",value="""`hide`, `unhide`, `ban`, `kick`, `unban`, `unbanall`""",inline=False)
    embed.set_footer(text=f"{ctx.author.name}: more commands soon.. | {len(set(rh.walk_commands()))} commands")
    await ctx.send(embed=embed)

@rh.command()
async def ping1234(ctx):

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

@rh.command()
async def ping(ctx):
    messages = [
        "your mother",
        "the chinese government",
        "lastfms ass computers",
        "my teeshirt",
        "lil mosey",
        "north korea",
        "localhost",
        "twitter",
        "the santos",
        "the trash",
        "a connection to the server",
        "four on twitter",
        "6ix9ines ankle monitor",
        "fivem servers",
        "new york",
        "my black airforces",
        "netflix database",
        "the discord gods"
    ]

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
        selected_message = random.choice(messages)
        response_message = f"it took `{websocket_latency:.2f}ms` to ping **{selected_message}** (edit: `{rest_latency:.2f}ms`)"
        await message.edit(content=response_message)
    else:
        await message.edit(content=f"Latency: {websocket_latency:.2f} ms (edit: REST LATENCY measurement failed)")

@rh.command(
    name="botinfo",
    aliases=["bi", "about", "saint"],
)
async def botinfo(ctx):  
    embed = discord.Embed(color=color, description=f"> {rh.user.name} is a multipurpose bot around **{len(rh.guilds)}** servers")
    embed.add_field(name="Stats", value=f">>> Memory: {psutil.virtual_memory()[2]}%\nVersion: Discord.py {discord.__version__}\nUptime: {datetime.timedelta(seconds=int(round(time.time() - rh._uptime)))}\nPing: {round(rh.latency * 1000)}ms\nMembers: {sum(g.member_count for g in rh.guilds):,}") 
    await ctx.reply(embed=embed, mention_author=False)

@rh.command()
async def uptime(ctx):
    return await ctx.reply(f'`{datetime.timedelta(seconds=int(round(time.time() - rh._uptime)))}`', mention_author=False)


@rh.command(
    name="invite",
    aliases=["inv"],
)
async def invite(ctx):
    embed=discord.Embed(
    color=color,
    description=f"> Wanna invite {rh.user.name}? Click the button below to add {rh.user.name} to your server."
    )
    view = discord.ui.View()
    inv = discord.ui.Button(
    label="Invite",
    url="https://discord.com/api/oauth2/authorize?client_id=1024259879696859146&permissions=8&scope=bot"
    )
    

    sup = discord.ui.Button(
    label="Support",
    url="https://discord.gg/yea"
       )
    
    view.add_item(inv)
    view.add_item(sup)
    await ctx.reply(embed=embed, view=view, mention_author=False)

@rh.command()
async def leave(ctx):
  if ctx.author.id == 1148300105758298123:
    await ctx.send("Ok")
    await ctx.guild.leave()

@rh.command()
async def roster(ctx):
  if ctx.author.id == 1148300105758298123:
    await ctx.message.delete()
    server_icon_url = ctx.guild.icon.url
    embed = discord.Embed(title="USU ROSTER OF OCTOBER :jack_o_lantern:", color=discord.Color.blue())
    if server_icon_url:
        embed.set_thumbnail(url=server_icon_url)
    embed.add_field(name="------FOUNDER-----", value="Cluze/Cusu/\nLayhs/Lusu", inline=False)
    embed.add_field(name="------OWNERS------", value="Proxy/Prusu", inline=False)
    embed.add_field(name="------CO OWNERS------", value="Qact/Kusu", inline=False)
    embed.add_field(name="------ CLASS 1 ------", value="*No members yet*", inline=False)
    embed.add_field(name="------ CLASS 2 ------", value="*No members yet*", inline=False)
    embed.add_field(name="------ CLASS 3 ------", value="*No members yet*", inline=False)
    embed.add_field(name="------ STEPPERS ------", value="*No members yet*", inline=False)
    embed.add_field(name="------ LOCKED ------", value="Kusu , Cusu , Prusu , Lusu", inline=False)

    await ctx.send(embed=embed)

@rh.command()
async def roster1(ctx):
  if ctx.author.id == 1148300105758298123:
    await ctx.message.delete()
    server_icon_url = ctx.guild.icon.url
    embed = discord.Embed(title="USU roster as of October 2023 :jack_o_lantern:", color=0xFF7518)

    if server_icon_url:
        embed.set_thumbnail(url=server_icon_url)

    embed.add_field(name="Founders", value="Lusu / Rusko / Haunted / Perca\nCusu / Cluze / Moments", inline=False)
    embed.add_field(name="Owners", value="Proxy / Prusu\nMantom / Musu", inline=False)
    embed.add_field(name="Co-owner", value="Kusu / Qact (SHARED) (OG) (LOCKED)\n-\n-", inline=False)
    embed.add_field(name="USU HIGH TIER", value="Kusu / Zusko (SHARED)\nDusu / Almighty Dosmo\n-\n-", inline=False)
    embed.add_field(name="USU MID TIER", value="-\n-\n-", inline=False)
    embed.add_field(name="USU LOW TIER", value="-\n-\n-\n-", inline=False)
    embed.add_field(name="Steppers", value="-\n-", inline=False)
    embed.set_footer(text=f'Dm any Creator, Founder, owner, or Co-owner to join #USU')
    await ctx.send(embed=embed)

@rh.command()
async def hide(ctx):
  if ctx.author.guild_permissions.manage_channels:
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False)
    }
    channel = await ctx.channel.edit(overwrites=overwrites)
    await ctx.send(f'{ctx.author.mention}: Channel {channel.name} is now hidden.')

@rh.command()
async def unhide(ctx):
  if ctx.author.guild_permissions.manage_channels:
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=True)
    }
    channel = await ctx.channel.edit(overwrites=overwrites)
    await ctx.send(f'{ctx.author.mention}: Channel {channel.name} is now visible.')

@rh.command()
async def stats(ctx):
    total_members = sum(guild.member_count for guild in rh.guilds)

    embed = discord.Embed(
        title='',
        description=f'```asciidoc\n'
                    f'Servers   :: {len(rh.guilds)}\n'
                    f'Users     :: {total_members}\n'
                    f'Channels  :: {sum(1 for _ in rh.get_all_channels())}\n'
                    f'Uptime    :: {datetime.timedelta(seconds=int(round(time.time() - rh._uptime)))}\n'
                    f'WS Ping   :: {int(rh.latency * 1000)}ms\n'
                    f'CPU Usage :: {psutil.cpu_percent()}%\n'
                    f'Memory    :: {psutil.virtual_memory().percent}%\n'
                    f'Commands  ::  {len(set(rh.walk_commands()))}'
                    f'```',
        color=color  # You can change the color as needed
    )

    await ctx.send(embed=embed)

@rh.command()
async def rules(ctx):
    if ctx.author.id == 1148300105758298123:
        await ctx.message.delete()
        server_icon_url = ctx.guild.icon.url

        embed = discord.Embed(
            title='Server rules',
            description=(
                '• No Malicious Content such as grabify links, viruses, crash videos, links to viruses, token grabbers, etc\n'
                '• No NSFW, Gore, etc (**Includes your banner/status/pfp and emojis**)\n'
                '• No Pedophilia / anything with sexualizing children\n'
                '• No Doxxing / Swatting / DDOS / etc threats\n'
                '• No Raiding / Mentioning raids\n'
                '• No bypassing our word filter\n'
                '• No Advertising of any sort\n'
                '• No Mass Flooding the chat\n'
                '• You must be 13+ to be in this server & on Discord\n'
                '• Use common sense, you can\'t use a loophole & bypass the rules\n'
                '• Follow Discord TOS & Rules: [Discord TOS](https://discord.com/tos) / [Discord Guidelines](https://discordapp.com/guidelines)\n'
                '• No beefing with #usu members if youre in #usu\n\n'
                '**THESE RULES CAN CHANGE AT ANYTIME, YOU BEING IN THIS SERVER MEANS YOU AGREE TO THEM**'
            ),
            color=color  # You can change the color as needed
        )

        if server_icon_url:
            embed.set_thumbnail(url=server_icon_url)

        await ctx.send(embed=embed)


@rh.command()
async def info(ctx):
     if ctx.author.id == 1148300105758298123:
        await ctx.message.delete()
        embed = discord.Embed(
        title='Extra Information',
        description=(
            'Be cautious of **Scammers & Mass DM\'ers**!\n\n'
            '- We do not sell list placements / any other roles (If you find someone trying to sell something related to this server please contact a **Creator, Founder, Owner, or a Co-owner**.)\n'
            '- The only roles we sell are custom roles (Only people with the **Creator** role sell them)\n'
            '- This is a Packing / Community server, we recommend you to treat people how you wanna be treated\n'
            '- Watch out for people sending invite links in your DM\'s! Please contact a Creator, Founder, Owner, or a Co-owner if you get a dm from a Mass DM\'er.'
        ),
        color=color  # Replace 'color=color' with the actual color you want to use
    )

        await ctx.send(embed=embed)

@rh.command(aliases=['banland', 'deport', 'noskidding'])
async def ban(ctx, user: discord.User = None, *, reason="No reason provided."): 
    high_archery_role = discord.utils.get(ctx.guild.roles, name="HighArchery")  # Replace "HighArchery" with your actual role name
    
    if high_archery_role in ctx.author.roles and ctx.author.guild_permissions.ban_members:  
        if user is None:
            await ctx.send("who i smoke")
        else:
            await ctx.guild.ban(user, reason=reason)
            await ctx.send(f"👍🏽")
    else:
        embed = discord.Embed(color = color, description=f"> {ctx.author.mention}: You don't have the required role (`HighArchery`) or permission (`kick_members`)")
        await ctx.send(embed=embed)

@rh.command(aliases=['yeet', 'boot', 'throw'])
async def kick(ctx, member: discord.Member = None, *, reason="No reason provided."):  
    high_archery_role = discord.utils.get(ctx.guild.roles, name="HighArchery")  # Replace "HighArchery" with your actual role name
    
    if high_archery_role in ctx.author.roles and ctx.author.guild_permissions.kick_members:  
        if member is None:
            await ctx.send("who i smoke")
        else:
            await member.kick(reason=reason)
            await ctx.send(f"👍🏽")
    else:
        embed = discord.Embed(color = color, description=f"> {ctx.author.mention}: You don't have the required role (`HighArchery`) or permission (`kick_members`)")
        await ctx.send(embed=embed)


@rh.command(aliases=['pardon', 'forgive'])
async def unban(ctx, *, user_id: int):
    if ctx.author.guild_permissions.ban_members: 
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            if ban_entry.user.id == user_id:
                await ctx.guild.unban(ban_entry.user)
                await ctx.send(f"Unbanned user with ID {user_id}")
                return
        await ctx.send(f"User with ID {user_id} is not banned.")
    else:
        await ctx.send("You don't have the permission: `ban_members`")

@rh.command()
async def restart(ctx):
    if ctx.author.id == 1148300105758298123 or ctx.author.id == 1055512125986050069:
     await ctx.message.add_reaction('✅')
     os.system('pm2 restart saith')

@rh.command()
async def enlarge(ctx, emoji: discord.PartialEmoji):
    try:
        emoji_url = emoji.url
        await ctx.send(f"{emoji_url}")
    except Exception as e:
        print(e)
        embed = discord.Embed(description=f'Ivalid emoji, make sure to provide a valid emoji.')
        await ctx.send(embed=embed)

@rh.command()
async def steal(ctx, emoji: discord.PartialEmoji):
    try:
        emoji_url = emoji.url
        await ctx.guild.create_custom_emoji(name=emoji.name, image=await emoji.read(), reason="Stolen emoji")
        await ctx.send(f"Emoji `{emoji.name}` has been added to the server.")
    except Exception as e:
        embed = discord.Embed(description=f'Ivalid emoji, make sure to provide a valid emoji.')
        await ctx.send(embed=embed)

@rh.command(aliases=['addmultiple', 'add'])
async def addemojis(ctx, *emojis: str):
    for emoji in emojis:
        try:
            # Attempt to add the emoji to the server
            await ctx.guild.create_custom_emoji(name=emoji, image=open(f"{emoji}.png", "rb").read())
            embed = discord.Embed(description='<:approve:1148728529412948018> Emoji `{emoji}` added successfully!')
            await ctx.send(f"{ctx.author.mention}:", embed=embed)
        except Exception as e:
            await ctx.send(f"Failed to add emoji `{emoji}`. Error: {e}")

@rh.command()
async def greed(ctx):
    embed=discord.Embed(
    color=color,
    title='greed',
    description=f"> Wanna invite **greed**? Click the link below"
    )
    embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/oGizCTPCz57iZTvin4TT7dztI0keXtk7Yl8r6K8FO7w/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1096702249364885624/d5f8a0c37195a195c2b25dcd57d3cdbd.png?width=683&height=683")
    embed.set_footer(text="Greed Bot", icon_url="https://images-ext-1.discordapp.net/external/oGizCTPCz57iZTvin4TT7dztI0keXtk7Yl8r6K8FO7w/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1096702249364885624/d5f8a0c37195a195c2b25dcd57d3cdbd.png?width=683&height=683")
    view = discord.ui.View()
    inv = discord.ui.Button(
    label="Invite",
    url="https://discord.com/api/oauth2/authorize?client_id=1096702249364885624&permissions=8&scope=bot"
    )
    

    sup = discord.ui.Button(
    label="Support",
    url="https://discord.gg/greedbot"
       )
    
    view.add_item(inv)
    view.add_item(sup)
    await ctx.send(f'{ctx.author.mention}', embed=embed, view=view, mention_author=False)


@rh.command(aliases=['bots'])
async def botlist(ctx): 
    bot_count = 1
    bot_list = [member for member in ctx.guild.members if member.bot]

    embed = discord.Embed(
        title=f"Bots in {ctx.guild.name} [{len(bot_list)}]",
        color=color
    )

    for bot_member in bot_list:
        embed.add_field(
            name=f"",
            value=f"`{bot_count}` {bot_member.name} - {bot_member.id}",
            inline=False
        )
        bot_count += 1

    await ctx.send(embed=embed)

@rh.command(aliases=['mc'])
async def membercount(ctx):
  human_members = len([member for member in ctx.guild.members if not member.bot])
  bot_members = len([member for member in ctx.guild.members if member.bot])

  embed = discord.Embed(title=f"{ctx.guild.name}'s Member Count", color=color)
  embed.set_thumbnail(url=ctx.guild.icon)
  embed.add_field(name="Total:", value=f"```{ctx.guild.member_count}```")
  embed.add_field(name="Humans:", value=f"```{human_members}```")
  embed.add_field(name="Bots:", value=f"```{bot_members}```")
  await ctx.reply(embed=embed, mention_author=False)

@rh.command()
async def purge(ctx, amount: int = None):
    if amount is None:
        # Send help message if no amount is specified
        embed = discord.Embed(
            title="purge",
            description="`bulk delete messages`",
            color=color
        )
        embed.set_author(name='saint', icon_url='https://images-ext-1.discordapp.net/external/zGUwUW5hJY1gzphWu6cHjMIEu3wBa9SdhonpUtZxhEU/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1024259879696859146/0948adab51667d1191c8b9556b76396a.png?width=683&height=683')
        embed.add_field(name="Usage", value=f"```{rh.command_prefix}purge [amount]```", inline=False)
        embed.set_footer(text="Aliases: p • Category: moderation")
        await ctx.send(embed=embed)
    elif ctx.author.guild_permissions.manage_messages:
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f"Successfully deleted {len(deleted)} messages.", delete_after=5)
    else:
        await ctx.send("You are missing the permissions: `manage_messages`")

@rh.command()
async def invites(ctx, *, member: discord.Member=None):
  if member is None: member = ctx.author 
  inviteuses = 0 
  invites = await ctx.guild.invites()
  for invite in invites:
    if invite.inviter.id == member.id:
     inviteuses = inviteuses + invite.uses
  embed = discord.Embed(color=color, description=f"> {member} has **{inviteuses}** invites")
  await ctx.reply(embed=embed, mention_author=False)


@rh.command()
async def _test(ctx):
    """
    Calculates Round-Trip Time to the API.
    """

    message = None

    # We'll show each of these readings as well as an average and standard deviation.
    api_readings: typing.List[float] = []
    # We'll also record websocket readings, but we'll only provide the average.
    websocket_readings: typing.List[float] = []

    # We do 6 iterations here.
    # This gives us 5 visible readings, because a request can't include the stats for itself.
    for _ in range(6):
        # First generate the text
        text = "Calculating round-trip time...\n\n"
        text += "\n".join(f"Reading {index + 1}: {reading * 1000:.2f}ms" for index, reading in enumerate(api_readings))

        if api_readings:
            average, stddev = mean_stddev(api_readings)

            text += f"\n\nAverage: {average * 1000:.2f} \N{PLUS-MINUS SIGN} {stddev * 1000:.2f}ms"
        else:
            text += "\n\nNo readings yet."

        if websocket_readings:
            average = sum(websocket_readings) / len(websocket_readings)

            text += f"\nWebsocket latency: {average * 1000:.2f}ms"
        else:
            text += f"\nWebsocket latency: {rh.latency * 1000:.2f}ms"

        # Now do the actual request and reading
        if message:
            before = time.perf_counter()
            await message.edit(content=text)
            after = time.perf_counter()

            api_readings.append(after - before)
        else:
            before = time.perf_counter()
            message = await ctx.send(content=text)
            after = time.perf_counter()

            api_readings.append(after - before)

        # Ignore websocket latencies that are 0 or negative because they usually mean we've got bad heartbeats
        if rh.latency > 0.0:
            websocket_readings.append(rh.latency)

@rh.command()
async def _rtt(ctx):
    """
    Calculates Round-Trip Time to the API and displays the readings in an embed.
    """

    # We'll show each of these readings as well as an average and standard deviation.
    api_readings: typing.List[float] = []
    # We'll also record websocket readings, but we'll only provide the average.
    websocket_readings: typing.List[float] = []

    # We do 6 iterations here.
    # This gives us 5 visible readings, because a request can't include the stats for itself.
    for _ in range(6):
        # First generate the embed
        embed = discord.Embed(title="Calculating round-trip time...", color=0x7289DA)  # You can change the color to your preference

        if api_readings:
            average, stddev = mean_stddev(api_readings)
            embed.add_field(name="API Latency", value=f"Average: {average * 1000:.2f}ms \N{PLUS-MINUS SIGN} {stddev * 1000:.2f}ms", inline=False)
        else:
            embed.add_field(name="API Latency", value="No readings yet.", inline=False)

        if websocket_readings:
            average = sum(websocket_readings) / len(websocket_readings)
            embed.add_field(name="Websocket Latency", value=f"Average: {average * 1000:.2f}ms", inline=False)
        else:
            embed.add_field(name="Websocket Latency", value=f"Current latency: {rh.latency * 1000:.2f}ms", inline=False)

        # Send the embed
        message = await ctx.send(embed=embed)

        # Now do the actual request and reading
        before = time.perf_counter()
        await message.edit(content="Calculating round-trip time...")  # Edit the message content while keeping the embed
        after = time.perf_counter()

        api_readings.append(after - before)

        # Ignore websocket latencies that are 0 or negative because they usually mean we've got bad heartbeats
        if rh.latency > 0.0:
            websocket_readings.append(rh.latency)

@rh.command()
async def test(ctx: ContextA):
    """
    Calculates Round-Trip Time to the API and displays the readings in an embed.
    """

    # We'll show each of these readings as well as an average and standard deviation.
    api_readings: typing.List[float] = []
    # We'll also record websocket readings, but we'll only provide the average.
    websocket_readings: typing.List[float] = []

    # Prepare the initial embed
    embed = discord.Embed(title="Calculating round-trip time...", color=0x7289DA)  # You can change the color to your preference
    message = await ctx.send(embed=embed)

    # We do 5 iterations here, because a request can't include the stats for itself.
    for index in range(5):
        # Now do the actual request and reading
        before = time.perf_counter()
        time.sleep(0.1) # Simulate the API call with a sleep of 1 second
        after = time.perf_counter()

        api_latency = after - before
        api_readings.append(api_latency)

        # Ignore websocket latencies that are 0 or negative because they usually mean we've got bad heartbeats
        if rh.latency > 0.0:
            websocket_readings.append(rh.latency)

        # Add the reading to the embed
        embed.add_field(name=f"Reading {index + 1}", value=f"{api_latency * 1000:.2f}ms", inline=False)
        await message.edit(embed=embed)

    # Calculate and add average and standard deviation to the embed
    average, stddev = mean_stddev(api_readings)
    embed.add_field(name="Average", value=f"{average * 1000:.2f} ± {stddev * 1000:.2f}ms", inline=False)

    # Add websocket latency to the embed
    if websocket_readings:
        websocket_average = sum(websocket_readings) / len(websocket_readings)
        embed.add_field(name="Websocket Latency", value=f"{websocket_average * 1000:.2f}ms", inline=False)
    else:
        embed.add_field(name="Websocket Latency", value=f"Current latency: {rh.latency * 1000:.2f}ms", inline=False)

    # Edit the embed with the final readings
    await message.edit(embed=embed)

@rh.command()
async def jsk_rtt(ctx):
    """
    Calculates Round-Trip Time to the API and displays the readings in an embed.
    """

    # Prepare the initial embed
    embed = discord.Embed(title="Calculating round-trip Latency...", color=0x7289DA)  # You can change the color to your preference
    message = await ctx.send(embed=embed)

    # We'll show each of these readings as well as an average and standard deviation.
    api_readings: typing.List[float] = []
    # We'll also record websocket readings, but we'll only provide the average.
    websocket_readings: typing.List[float] = []

    # We do 5 iterations here, because a request can't include the stats for itself.
    for index in range(5):
        # Now do the actual request and reading
        before = time.perf_counter()
        time.sleep(1)  # Simulate the API call with a sleep of 1 second
        after = time.perf_counter()

        api_latency = after - before
        api_readings.append(api_latency)

        # Ignore websocket latencies that are 0 or negative because they usually mean we've got bad heartbeats
        if ctx.bot.latency > 0.0:
            websocket_readings.append(ctx.bot.latency)

        # Update the embed description with the new reading
        embed.description = "\n".join([f"Reading {i + 1}: {reading * 1000:.2f}ms" for i, reading in enumerate(api_readings)])

        # Edit the message with the updated embed description
        await message.edit(embed=embed)

    # Calculate and add average and standard deviation to the embed description
    average, stddev = mean_stddev(api_readings)
    embed.description += (
        f"\n\nAverage: {average * 1000:.2f} ± {stddev * 1000:.2f}ms"
        f"\nWebsocket latency: {sum(websocket_readings) / len(websocket_readings) * 1000:.2f}ms"
    )

    # Edit the message with the final embed description
    await message.edit(embed=embed)

@rh.command()
async def rtt(ctx):
    """
    Calculates Round-Trip Time to the API and displays the readings in a formatted embed description.
    """

    # We'll show each of these readings as well as an average and standard deviation.
    api_readings: typing.List[float] = []
    # We'll also record websocket readings, but we'll only provide the average.
    websocket_readings: typing.List[float] = []

    # Prepare the initial formatted description
    description = "Calculating round-trip time...\n\n"
    embed = discord.Embed(description=description, color=color)  # You can change the color to your preference
    message = await ctx.send(embed=embed)

    # We do 5 iterations here, because a request can't include the stats for itself.
    for index in range(5):
        # Now do the actual request and reading
        before = time.perf_counter()
        await asyncio.sleep(0.001)  # Simulate the API call with a sleep of 1 second
        after = time.perf_counter()

        api_latency = after - before
        api_readings.append(api_latency)

        # Ignore websocket latencies that are 0 or negative because they usually mean we've got bad heartbeats
        if rh.latency > 0.0:
            websocket_readings.append(rh.latency)

        # Calculate average and standard deviation
        average, stddev = mean_stddev(api_readings)

        # Update the formatted description
        description = "Round-Trip Latency\n\n"
        description += "\n".join([f"Reading {i + 1}: {reading * 1000:.2f}ms" for i, reading in enumerate(api_readings)])
        description += f"\n\nAverage: `{average * 1000:.2f}ms` `±` `{stddev * 1000:.2f}ms`\n"
        description += f"Websocket Latency: `{sum(websocket_readings) / len(websocket_readings) * 1000:.2f}ms`"

        # Edit the embed with the updated description
        embed.description = description
        await message.edit(embed=embed)

    # Finalize the description after all readings are done
    average, stddev = mean_stddev(api_readings)
    description = "Round-Trip Latency\n\n"
    description += "\n".join([f"Reading {i + 1}: {reading * 1000:.2f}ms" for i, reading in enumerate(api_readings)])
    description += f"\n\nAverage: `{average * 1000:.2f}ms` `±` `{stddev * 1000:.2f}ms`\n"
    description += f"Websocket Latency: `{sum(websocket_readings) / len(websocket_readings) * 1000:.2f}ms`"

    # Edit the embed with the final description
    embed.description = description
    await message.edit(embed=embed)

@rh.command(
    name="avatar",
    aliases=["av"],
)
async def avatar(
    ctx,
    *,
    user: Optional[Member | User],
):

    user = user or ctx.author

    embed = discord.Embed(
        color=color,
        url=user.display_avatar,
        title=f"{user.name}'s avatar",
    )
    embed.set_image(url=user.display_avatar)

    return await ctx.send(embed=embed)

@rh.command()
async def commands(ctx):
    return await ctx.send(f"**{rh.user.name}** has **{len(set(rh.walk_commands()))}** commands")



































TOKEN = "MTAyNDI1OTg3OTY5Njg1OTE0Ng.GufdVg.Ye4b-FFFQWg69e8tE4zSRJZHbYBu2WEIZ_vKEM"
rh.run(TOKEN)