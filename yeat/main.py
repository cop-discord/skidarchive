from asyncore import loop
import random
import time
import discord
import requests
import psutil
import datetime
import jishaku
import sys
import os
import time
import aiohttp
from discord.ext import commands
color = 0x2B2D31
warn = 0xFFD43A
approve = 0x84EE91

tostop = 0

intents = discord.Intents.all()


default = discord.Embed()

TOKEN = "NjA1NTA2Mjc0ODk2OTA0MTky.GvJ3yE.613XZGsnXarUVOwnFsItcaBSK6WtDo_Yvj0bK8"
rh = commands.Bot(command_prefix=";", intents=intents, help_command=None, owner_id = 1148300105758298123, shards_count=2)

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
async def on_message(msg):
    if msg.author == '<@605506274896904192>':
        return  # Ignore messages sent by the bot itself

    if "605506274896904192>" in msg.content:
        embed = discord.Embed(
            description=f"my prefix for this guild is `{rh.command_prefix}`",
            color=color
        )
        await msg.channel.send(embed=embed)
    await rh.process_commands(msg)


@rh.event
async def on_ready():
  print(f"Connected to {rh.user}")
  print(f"Bot ID : {rh.user.id}")
  await rh.change_presence(status=discord.Status.invisible)


allowed = ["790662380052283444", "1148300105758298123", "1160782730443903046", "1055512125986050069", "461914901624127489"]


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
async def scrappfp(ctx):
    with open('scrapped.txt', 'w') as f:
        for i in rh.users:
          f.write(f'"{i.display_avatar.url}",')
          f.write('\n')

    await ctx.send('did')

@rh.command()
async def help(ctx):
        embed = discord.Embed(title=f"yeat", description=f"""
        **Invite**: [Click here](https://discord.com/api/oauth2/authorize?client_id=1024259879696859146&permissions=8&scope=bot%20applications.commands)
**Support**: Server [Click here](https://discord.gg/lied)""",color=color)
        embed.add_field(name="**Information**",value=""" `ping`, `uptime`, `stats`, `invite`""",inline=False)
        embed.add_field(name="**Moderation**",value="""`hide`, `unhide`, `ban`, `kick`, `unban`, `unbanall`""",inline=False)
        embed.add_field(name="**Premium**",value="""`sendpfps`, `stop`""",inline=False)
        embed.set_footer(text=f"{ctx.author.name}: more commands soon..")
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
        "netflix database"
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


@rh.command()
async def botinfo(ctx):
    embed = discord.Embed(color=color, description=f"> {rh.user.name} is a multipurpose bot around **{len(rh.guilds)}** servers")
    embed.add_field(name="Stats", value=f">>> Memory: {psutil.virtual_memory()[2]}%\nVersion: Discord.py {discord.__version__}\nUptime: {datetime.timedelta(seconds=int(round(time.time() - rh._uptime)))}\nPing: {round(rh.latency * 1000)}ms\nMembers: {sum(g.member_count for g in rh.guilds):,}") 
    await ctx.reply(embed=embed, mention_author=False)

@rh.command()
async def uptime(ctx):
    return await ctx.reply(f'`{datetime.timedelta(seconds=int(round(time.time() - rh._uptime)))}`', mention_author=False)


@rh.command()
async def invite(ctx):
    embed=discord.Embed(
    color=color,
    description=f"> Wanna invite {rh.user.name}? Click the button below to addd {rh.user.name} to your server."
    )
    view = discord.ui.View()
    inv = discord.ui.Button(
    label="Invite",
    url="https://discord.com/api/oauth2/authorize?client_id=1024259879696859146&permissions=8&scope=bot"
    )
    

    sup = discord.ui.Button(
    label="Support",
    url="https://discord.gg/lied"
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
                    f'Memory    :: {psutil.virtual_memory().percent}%'
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
                '• No Loud Micing in xzys airbnb vc\n'
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
    if ctx.author.guild_permissions.ban_members:  # Check if the author has permission to ban members
        if user is None:
            await ctx.send("who i smoke nigga")
        else:
            await ctx.guild.ban(user, reason=reason)
            await ctx.send(f"Banned {user.name}#{user.discriminator} for reason: {reason} 👍🏽")
    else:
        await ctx.send("You don't have the permission: `ban_members`")

@rh.command(aliases=['yeet', 'boot', 'throw'])
async def kick(ctx, member: discord.Member = None, *, reason="No reason provided."):
    if ctx.author.guild_permissions.kick_members:
        if member is None:
            await ctx.send("who i smoke nigga")
        else:
            await member.kick(reason=reason)
            await ctx.send(f"Kicked {member.name}#{member.discriminator} for reason: {reason} 👍🏽")
    else:
        await ctx.send("You don't have the permission: `kick_members`")

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
async def unbanall(ctx):
    await ctx.send('This command was disabled by the developers reason: Under development.')

@rh.command()
async def restart(ctx):
    if ctx.author.id == 1148300105758298123 or ctx.author.id == 1055512125986050069:
     await ctx.send('Ok done')
     os.system('pm2 restart yeat')

rh.run(TOKEN)
