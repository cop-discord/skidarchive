import discord, json, datetime, aiohttp, sys, io, typing
from datetime import datetime
import button_paginator as pg
import yarl

def premium():
  async def predicate(ctx: commands.Context): 
    if ctx.command.name in ["ship"]: #"
      if ctx.author.id == ctx.guild.owner_id: return True     
    async with ctx.bot.db.cursor() as cursor:
        await cursor.execute("SELECT * FROM donor WHERE user_id = {}".format(ctx.author.id))     
        #await cursor.execute("SELECT * FROM authorize WHERE guild_id = {} AND tags = {}", ctx.guild.id, "true")           
    if check is None and res is None: 
      await ctx.send("Donator only")
      return False 
    return True 
  return commands.check(predicate) 