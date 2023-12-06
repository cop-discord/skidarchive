import discord
import asyncio
import argparse
import os
from discord.ext import commands

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

prefix = "^" if args.test else "x"

bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.remove_command("help")

@bot.event
async def on_ready():
    await load_cogs()
    print(f"logged in as {bot.user}")

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension("cogs." + filename[:-3])

if __name__ == "__main__":
    token = ("MTA5NjcwMjI0OTM2NDg4NTYyNA.GW63Rp.Da_WaoBFEbgfWFf0fD5wTD8Oy4CN-Y-Im9LnF8")
    bot.run(token)