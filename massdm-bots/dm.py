import discord
import asyncio
import argparse
import os
from discord.ext import commands
import discord_ios

parser = argparse.ArgumentParser(
    prog="massdm",
    description="abort",
)
parser.add_argument(
    "-t",
    "--test",
    action="store_true",
    help="ngl i stole this from keron",
)
args = parser.parse_args()

intents = discord.Intents.all()

prefix = "^" if args.test else ";"

bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.remove_command("help")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.custom, state="discord.gg/your", name="discord.gg/your", url="https://twitch.tv/shottas"))
    print(f"logged in as {bot.user}")

@bot.event
async def on_connect():
    await load_cogs()
    await bot.tree.sync()

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension("cogs." + filename[:-3])

if __name__ == "__main__":
    token = ("MTA5NjcwMjI0OTM2NDg4NTYyNA.GW63Rp.Da_WaoBFEbgfWFf0fD5wTD8Oy4CN-Y-Im9LnF8")
    bot.run(token)