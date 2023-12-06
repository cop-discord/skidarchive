import os
from discord.ext import commands
import discord
from discord.ext import commands
from discord.ext import tasks
from keep_alive import keep_alive


intents = discord.Intents.default()
intents.members = True
intents.guilds = True

client = commands.Bot(command_prefix="$",
                      case_insensitive=False,
                      shard_id=4,
                      intents=intents)
client.remove_command('help')
  
@client.event
async def on_connect():
  await client.change_presence(activity=discord.Activity(
            type=discord.ActivityType.streaming,
            name=f"discord.gg/your",
            url='https://www.twitch.tv/actavis'))
  
@client.event
async def on_member_join(member):
    channellol = client.get_channel(1177806443299213322)
    print ("{} joined!".format(member.name))
    print (f'{member.guild.name}')
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label=f"Sent from {member.guild.name}", disabled=True))
    embed = discord.Embed(color=0x7289DA, description=f"Join our sponsored servers for a nitro giveaway, and add la#0001, qact, purecomboy, & our son generocity\n\nhttps://tear.lol/ \n\n https://discord.gg/backseat & https://discord.gg/your")
    embed.set_thumbnail(url=client.user.avatar.url)
    embed.set_author(name=f"{client.user.name}", icon_url=client.user.avatar.url)
    embed.set_footer(text="discord.gg/your")
    await member.send(f"`sponsored`: https://discord.gg/your & https://discord.gg/backseat \n add la#0001", embed=embed, view=view)
    await channellol.send(f"`{member.name}` joined `{member.guild.name}`")

@client.event
async def on_guild_join(guild):
    channellol = client.get_channel(1177806443299213322)
    haha = f'{len(guild.members)}'
    await channellol.send(f"i have been added to: `{guild.name}` with `{haha}` Members")

@client.event
async def on_guild_remove(guild):
    channellol = client.get_channel(1177806443299213322)
    haha = f'{len(guild.members)}'
    await channellol.send(f"i have been removed from: `{guild.name}` with `{haha}` Members")

@client.event
async def on_member_remove(member):
    channellol = client.get_channel(1177806443299213322)
    print ("{} left".format(member.name))
    print (f'{member.guild.name}')
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label=f"Sent from {member.guild.name}", disabled=True))
    embed = discord.Embed(color=0x7289DA, description=f"Join our sponsored servers for a nitro giveaway, and add la#0001, qact, purecomboy, & our son generocity\n\nhttps://tear.lol/ \n\n https://discord.gg/backseat & https://discord.gg/your")
    embed.set_thumbnail(url=client.user.avatar.url)
    embed.set_author(name=f"{client.user.name}", icon_url=client.user.avatar.url)
    embed.set_footer(text="discord.gg/your")
    await member.send(f"{member.mention}, `sponsored`: https://discord.gg/your & add la#0001", embed=embed, view=view) 	
    await channellol.send(f"`{member.name}` left `{member.guild.name}`")

keep_alive()
client.run('MTA3NTc5NzIyMTQ2NDg3MTAxMg.GIXaoz.pKc_O4F_U4hu01MPM9XVtCfsM0-P0DWaPJtULQ')