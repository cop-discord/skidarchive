import discord

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="+", self_bot=True, help_command=None,intents=intents) # Change prefix here
bot.remove_command("help")
intents.presences=True
@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready.")
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.streaming, name=f"discord.gg/board",url='https://www.youtube.com/watch?v=KZqIKhDTcfE'))
    print(f"streaming on {bot.user} | {bot.user.id}")

bot.run("MTEyMjU1OTU1ODc0NTg0OTg1Ng.GTha0K.oyYwTJFKATULeC9-95l9Y-9UbNFNrvpuR9vL5Y", bot=True, reconnect=True)