import discord, aiosqlite, os, asyncio, time, sys, random, aiohttp, datetime, requests, psutil, discord.ui
discord.http.Route.BASE = "https://canary.discord.com/api"
from datetime import datetime
from discord.ui import View, Button, Select
from discord.ext import commands, tasks 
from discord.gateway import DiscordWebSocket
from utils.classes import Emojis
from backend.classes import Emojis
from cogs.voicemaster import vmbuttons
from backend.classes import Colors, Emojis
from dotenv import load_dotenv
from cogs.music import Music
import requests

load_dotenv()

#responses = ["11% of people are left handed", "August has the highest percentage of births", "unless food is mixed with saliva you can't taste it", "the average person falls asleep in 7 minutes", "a bear has 42 teeth", "an ostrich's eye is bigger than its brain", "lemons contain more sugar than strawberries", "8% of people have an extra rib", "85% of plant life is found in the ocean", "Ralph Lauren's original name was Ralph Lifshitz", "rabbits like licorice", "the Hawaiian alphabet has 13 letters", "'Topolino' is the name for Mickey Mouse Italy", "a lobsters blood is colorless but when exposed to oxygen it turns blue", "armadillos have 4 babies at a time and are all the same sex", "reindeer like bananas", "the longest recorded flight of a chicken was 13 seconds", "birds need gravity to swallow", "the most commonly used letter in the alphabet is E", "the 3 most common languages in the world are Mandarin Chinese, Spanish and English", "dreamt is the only word that ends in mt", "the first letters of the months July through to November spell JASON"]
responses = ["bot is powered by [usebot](https://discord.gg/usebot)", "?? by [usebot](https://discord.gg/usebot)", "running [usebot](https://discord.gg/usebot) src"]

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "True"
os.environ["JISHAKU_RETAIN"] = "True"

async def identify(self):
    payload = {
        'op': self.IDENTIFY,
        'd': {
            'token': self.token,
            'properties': {
                '$os': sys.platform,#sys.platform,
                '$browser': 'Discord iOS',
                '$device': 'Discord iOS',
                '$referrer': '',
                '$referring_domain': ''
            },
            'compress': True,
            'large_threshold': 250,
            'v': 3
        }
    }

    if self.shard_id is not None and self.shard_count is not None:
        payload['d']['shard'] = [self.shard_id, self.shard_count]

    state = self._connection
    if state._activity is not None or state._status is not None:
        payload['d']['presence'] = {
            'status': state._status,
            'game': state._activity,
            'since': 0,
            'afk': False
        }

    if state._intents is not None:
        payload['d']['intents'] = state._intents.value

    await self.call_hooks('before_identify', self.shard_id, initial=self._initial_identify)
    await self.send_as_json(payload)

DiscordWebSocket.identify = identify

async def getprefix(bot, message):
       if not message.guild: return "<@1171112895250169937>"
       selfprefix = "<@1171112895250169937>" 
       guildprefix = "<@1171112895250169937>"
       async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT * FROM selfprefix WHERE user_id = {}".format(message.author.id)) 
        check = await cursor.fetchone()
        if check is not None:
         selfprefix = check[0]
        await cursor.execute("SELECT prefix, * FROM prefixes WHERE guild_id = {}".format(message.guild.id)) 
        res = await cursor.fetchone()
        if res is not None: 
            guildprefix = res[0]
        elif res is None:
            guildprefix = "<@1171112895250169937>"    

       return guildprefix, selfprefix  

def get_status(name: str): 
   if name == "competing": return discord.ActivityType.competing
   elif name == "streaming": return discord.ActivityType.streaming
   elif name == "playing": return discord.ActivityType.playing 
   elif name == "watching": return discord.ActivityType.watching
   elif name == "listening": return discord.ActivityType.listening
    
@tasks.loop(seconds=60)
async def status(): 
   list = [f""]
   activities = ["watching"]
   #emojiss = ["<:sparkles:>", "<:hearthands:>", "<:heart:>"]
   for a in activities:
    for l in list:
     #for t in emojiss:                                                                            #type=get_status(a)
      await bot.change_presence(status=discord.Status.idle, activity=discord.CustomActivity(name=l, state=l))#, emoji=t)) ##activity=discord.Activity
      await asyncio.sleep(60)

@tasks.loop(seconds=10)
async def female():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'female'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()["url"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    embed.set_image(url=urll)
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT * FROM female")
        results = await cursor.fetchall()
        for result in results:
            channel_id = result[1]
            try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll) ##eembed
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
            except:
                pass
        
@tasks.loop(seconds=10)
async def male():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'male'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()["url"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    embed.set_image(url=urll)
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT * FROM male")
        results = await cursor.fetchall()
        for result in results:
            channel_id = result[1]
            try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
                await msg.add_reaction("<:fire:1129806609099530300>")
                await asyncio.sleep(10.5)
            except:
                pass

@tasks.loop(seconds=10)
async def anime():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'anime'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()["url"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    embed.set_image(url=urll)
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT * FROM anime")
        results = await cursor.fetchall()
        for result in results:
            channel_id = result[1]
            try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
                await msg.add_reaction("<:fire:1129806609099530300>")
                await asyncio.sleep(10.5)
            except:
                pass

@tasks.loop(seconds=10)
async def ricon():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'random pfp'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()["url"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    embed.set_image(url=urll)
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT * FROM random")
        results = await cursor.fetchall()
        for result in results:
            channel_id = result[1]
            try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
                await msg.add_reaction("<:fire:1129806609099530300>")
                await asyncio.sleep(10.5)
            except:
                pass

@tasks.loop(seconds=10)
async def banner():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'banner'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()["url"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    embed.set_image(url=urll)
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT * FROM banner")
        results = await cursor.fetchall()
        for result in results:
            channel_id = result[1]
            try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
                await msg.add_reaction("<:fire:1129806609099530300>")
                await asyncio.sleep(10.5)
            except:
                pass
        
@tasks.loop(seconds=10)
async def match():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'match'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    #embed_index = discord.Embed()
    #embed_index.set_image(url="https://media.discordapp.net/attachments/1017627779275165737/1020106720703422515/2BA4AFF5-CBA7-4CC3-B31D-216B4319B775.png")
    embed.set_image(url=urll['avatar_url'])
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embed_banner = discord.Embed(color=0x2B2D31, description="[here is banner, pfp below](https://www.pinterest.com/proxypfps/)")#)#, timestamp=datetime.now())
    embed_banner.set_image(url=urll['banner_url'])
    #embed_banner.set_footer(text="? ", icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM match")
      results = await cursor.fetchall()
      for result in results:
        channel_id = result[1]
        try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                await msg.edit(embeds=[embed_banner, embed])
                await msg.add_reaction("<:fire:1129806609099530300>")
                await asyncio.sleep(10.5)
        except:
                pass
            
@tasks.loop(seconds=10)
async def fgif():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'female gif'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()["url"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    embed.set_image(url=urll)
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM fgifs")
      results = await cursor.fetchall()
      for result in results:
        channel_id = result[1]
        try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
                await msg.add_reaction("<:fire:1129806609099530300>")
                await asyncio.sleep(10.5)
        except:
                pass

@tasks.loop(seconds=10)
async def mgif():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'male gif'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()["url"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    embed.set_image(url=urll)
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM mgifs")
      results = await cursor.fetchall()
      for result in results:
        channel_id = result[1]
        try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
                await msg.add_reaction("<:fire:1129806609099530300>")
                await asyncio.sleep(10.5)
        except:
            pass

@tasks.loop(seconds=10)
async def agif():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'anime'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()["url"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    embed.set_image(url=urll)
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM agifs")
      results = await cursor.fetchall()
      for result in results:
        channel_id = result[1]
        try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
                await msg.add_reaction("<:fire:1129806609099530300>")
                await asyncio.sleep(10.5)
        except:
            pass
        
@tasks.loop(seconds=10)
async def autocar():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'cars'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()["url"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    embed.set_image(url=urll)
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM autocar")
      results = await cursor.fetchall()
      for result in results:
        channel_id = result[1]
        try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
                await msg.add_reaction("<:fire:1129806609099530300>")
                await asyncio.sleep(10.5)
        except:
            pass
        
@tasks.loop(seconds=10)
async def guns():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'guns'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()["url"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    embed.set_image(url=urll)
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM guns")
      results = await cursor.fetchall()
      for result in results:
        channel_id = result[1]
        try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
                await msg.add_reaction("<:fire:1129806609099530300>")
                await asyncio.sleep(10.5)
        except:
            pass
        
@tasks.loop(seconds=10)
async def faceless():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'faceless'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()["url"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    embed.set_image(url=urll)
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM faceless")
      results = await cursor.fetchall()
      for result in results:
        channel_id = result[1]
        try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
                await msg.add_reaction("<:fire:1129806609099530300>")
                await asyncio.sleep(10.5)
        except:
            pass

@tasks.loop(seconds=10)
async def autobody():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'nsfw pfp'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()["url"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    embed.set_image(url=urll)
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM autobody")
      results = await cursor.fetchall()
      for result in results:
        channel_id = result[1]
        try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
                await msg.add_reaction("<:fire:1129806609099530300>")
                await asyncio.sleep(10.5)
        except:
            pass
        
@tasks.loop(seconds=10)
async def autoshoes():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'shoes'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()["url"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    embed.set_image(url=urll)
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM autoshoes")
      results = await cursor.fetchall()
      for result in results:
        channel_id = result[1]
        try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
                await msg.add_reaction("<:runningshoe:1129806857293271181>")
                await asyncio.sleep(10.5)
        except:
            pass
        
@tasks.loop(seconds=10)
async def autojewellry():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'jewellry'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()["url"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    embed.set_image(url=urll)
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM jewellry")
      results = await cursor.fetchall()
      for result in results:
        channel_id = result[1]
        try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
                await msg.add_reaction("<:ring:1129807053146308698>")
                await asyncio.sleep(10.5)
        except:
            pass
        
@tasks.loop(seconds=10)
async def aesthetic():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'aesthetic'
    }
   
    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()["url"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    embed.set_image(url=urll)
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM aesthetic")
      results = await cursor.fetchall()
      for result in results:
        channel_id = result[1]
        try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
                await msg.add_reaction("<:hibiscus:1129807213108662355>")
                await asyncio.sleep(10.5)
        except:
            pass
        
@tasks.loop(seconds=10)
async def cartoon():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'cartoon'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()["url"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    embed.set_image(url=urll)
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM cartoon")
      results = await cursor.fetchall()
      for result in results:
        channel_id = result[1]
        try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
                await msg.add_reaction("<:popcorn:1129807420277915698>")
                await asyncio.sleep(10.5)
        except:
            pass
        
@tasks.loop(seconds=10)
async def ukdrill():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'drill'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()["url"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    embed.set_image(url=urll)
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM drill")
      results = await cursor.fetchall()
      for result in results:
        channel_id = result[1]
        try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
                await msg.add_reaction("<:gs_black_ninja:1127675959705878620>")
                await asyncio.sleep(10.5)
        except:
            pass
        
@tasks.loop(seconds=10)
async def hellokitty():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'hello kitty'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()["url"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    embed.set_image(url=urll)
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM hellokitty")
      results = await cursor.fetchall()
      for result in results:
        channel_id = result[1]
        try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
                await msg.add_reaction("<:hearthands:1129808272958951505>")
                await asyncio.sleep(10.5)
        except:
            pass
        
@tasks.loop(seconds=10)
async def money():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'money'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()["url"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    embed.set_image(url=urll)
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM money")
      results = await cursor.fetchall()
      for result in results:
        channel_id = result[1]
        try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
                await msg.add_reaction("<:moneywithwings:1129808274162729081>")
                await asyncio.sleep(10.5)
        except:
            pass
        
@tasks.loop(seconds=10)
async def smoking():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'smoke'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()["url"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    embed.set_image(url=urll)
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM smoking")
      results = await cursor.fetchall()
      for result in results:
        channel_id = result[1]
        try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
                await msg.add_reaction("<:cigarette:1129808270576582796>")
                await asyncio.sleep(10.5)
        except:
            pass
        
@tasks.loop(seconds=10)
async def animals():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'animals'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()["url"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    embed.set_image(url=urll)
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM animals")
      results = await cursor.fetchall()
      for result in results:
        channel_id = result[1]
        try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
                await msg.add_reaction("<:catwithwrysmile:1129808269079228499>")
                await asyncio.sleep(10.5)
        except:
            pass
        
@tasks.loop(seconds=10)
async def soft():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'soft'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()["url"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    #button = discord.ui.Button(label="invite use", style=discord.ButtonStyle.url, url="https://discord.com/api/oauth2/authorize?client_id=1094942437820076083&permissions=8&scope=bot")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    embed.set_image(url=urll)
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM soft")
      results = await cursor.fetchall()
      for result in results:
        channel_id = result[1]
        try:
                channel = bot.get_channel(channel_id)
                view = discord.ui.View()
                #view.add_item(button)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
                await msg.add_reaction("<:bouquet:1129808267820929095>")
                await asyncio.sleep(10.5)
        except:
            pass
        
@tasks.loop(seconds=10)
async def qvote():
    r = requests.post("https://api.usebot.lol/api/1.0/quote")
    urll = r.json()["quote"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=f"{urll}")#, timestamp=datetime.now())
    #embed.set_image(url=urll)
    #embed.description("{urll}")
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM quote")
      results = await cursor.fetchall()
      for result in results:
        channel_id = result[1]
        try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
                await msg.add_reaction("<:heartonfire:1129808265014943765>")
                await asyncio.sleep(10.5)
        except:
            pass

        
@tasks.loop(seconds=10)
async def bff():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'besties'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()["url"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    embed.set_image(url=urll)
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM besties")
      results = await cursor.fetchall()
      for result in results:
        channel_id = result[1]
        try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
                await msg.add_reaction("<:heartonfire:1129808265014943765>")
                await asyncio.sleep(10.5)
        except:
            pass
        
@tasks.loop(seconds=10)
async def couplesgif():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'couple gif'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()["url"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    embed.set_image(url=urll)
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM couplesgif")
      results = await cursor.fetchall()
      for result in results:
        channel_id = result[1]
        try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
                await msg.add_reaction("<:heartonfire:1129808265014943765>")
                await asyncio.sleep(10.5)
        except:
            pass
        
@tasks.loop(seconds=10)
async def couplespfp():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'couple'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()["url"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    embed.set_image(url=urll)
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM couplespfp")
      results = await cursor.fetchall()
      for result in results:
        channel_id = result[1]
        try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
                await msg.add_reaction("<:heartonfire:1129808265014943765>")
                await asyncio.sleep(10.5)
        except:
            pass

@tasks.loop(seconds=10)
async def kpopp():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'kpop'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()["url"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    embed.set_image(url=urll)
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM kpop")
      results = await cursor.fetchall()
      for result in results:
        channel_id = result[1]
        try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
                await msg.add_reaction("<:chopsticks:1143568523059269633>")
                await asyncio.sleep(10.5)
        except:
            pass
        
@tasks.loop(seconds=10)
async def emoidk():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'edgy'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()["url"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    embed.set_image(url=urll)
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM edgy")
      results = await cursor.fetchall()
      for result in results:
        channel_id = result[1]
        try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
                await msg.add_reaction("<:knife:1146431790052016289>")
                await asyncio.sleep(10.5)
        except:
            pass

@tasks.loop(seconds=10)
async def nike():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'nike'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()["url"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    embed.set_image(url=urll)
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM nike")
      results = await cursor.fetchall()
      for result in results:
        channel_id = result[1]
        try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
                await msg.add_reaction("<:runningshoe:1129806857293271181>")
                await asyncio.sleep(10.5)
        except:
            pass
        
@tasks.loop(seconds=10)
async def coree():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'core'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)
    urll = r.json()["url"]
    embeds = []
    eembed = discord.Embed(color=0x2B2D31, description=":repeatbutton: **loading image**")
    eembed.add_field(name=" ", value=f"{random.choice(responses)}")
    embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
    embed.set_image(url=urll)
    embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    embeds.append(embed)
    async with bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM core")
      results = await cursor.fetchall()
      for result in results:
        channel_id = result[1]
        try:
                channel = bot.get_channel(channel_id)
                msg = await channel.send(urll)
                #await msg.add_reaction("<a:loading:1129810812995911730>")
                #await asyncio.sleep(1.50)
                #await msg.clear_reactions()
                #await asyncio.sleep(1.90)
                #await msg.edit(embed=embed)
                #await msg.add_reaction("<:fire:1129806609099530300>")
                #await asyncio.sleep(10.5)
                await msg.add_reaction("<:kissmark_1f48b:1147152647242133645>")
                await asyncio.sleep(10.5)
        except:
            pass
        
@tasks.loop(seconds=10) 
async def automeme():    
 for j in range(50):
  async with bot.db.cursor() as cursor:
   await cursor.execute("SELECT * FROM automeme")
   results = await cursor.fetchall()
   for result in results:
    channel_id = result[1]
    async with aiohttp.ClientSession() as cs:
       async with cs.get('https://api.popcat.xyz/meme') as response3: 
        data3 = await response3.json()

        image = data3["image"]
        title = data3["title"]
        url = data3["url"]
        upvotes = data3["upvotes"]
        comments = data3["comments"]
        embed3 = discord.Embed(color=0x2B2D31)
        embed3.set_image(url=image)
        e = discord.Embed(color=0x2B2D31, description=f"[{title}]({url})")
        e.set_footer(text=f":heart: {upvotes} :thought_balloon: {comments}")
        try:
          channel = bot.get_channel(channel_id)
          await channel.send(embed=e)
          await asyncio.sleep(15)
        except:
                continue

@tasks.loop(seconds=10)
async def autonsfw():

    auth = {'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEwOTQ5NDI0Mzc4MjAwNzYwODMiLCJib3QiOnRydWUsImlhdCI6MTY4OTM1MzI5NX0.MZQhdNQfx4Lj3KgjGcL1C1_0wFp-IIDyesLGrro7gpY'}

    async with bot.db.cursor() as cursor:
        slay = bot.get_channel(1149638654571073617)
        button = discord.ui.Button(label="vote", style=discord.ButtonStyle.url, url="https://top.gg/bot/1094942437820076083/vote")
        view = discord.ui.View()
        view.add_item(button)
        await cursor.execute("SELECT * FROM autonsfw")
        results = await cursor.fetchall()
        for result in results:
            server = bot.get_guild(result[0])
            
            if not server:  # If the bot is not in the server
                print(f"Bot is not in the server: {result[0]}")
                continue

            owner_id = server.owner.id
            print(f"Checking vote for the owner: <@{owner_id}>")        

            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://top.gg/api/bots/1094942437820076083/check?userId={owner_id}", headers=auth) as r:
                    if r.status != 200:
                        print(f"Failed to check vote for the owner: <@{owner_id}>, status code: {r.status}, message: {await r.text()}")
                        continue

                    vote_data = await r.json()
                    if vote_data.get('voted') == 1:
                        msg = await slay.send(f"The owner: <@{owner_id}> has voted")
                        header = {
                        'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
                        }

                        type = {
                        'option': 'nsfw video'
                        }

                        async with session.post("https://api.usebot.lol/api", headers=header, json=type) as r:
                            urll = (await r.json())["url"]
                            embeds = []
                            eembed = discord.Embed(color=0x2B2D31, description="<:repeatbutton:1129817608770818068> **loading image**")
                            eembed.add_field(name=" ", value=f"{random.choice(responses)}")
                            embed = discord.Embed(color=0x2B2D31, description=" ")#, timestamp=datetime.now())
                            embed.set_image(url=urll)
                            embed.set_footer(text="powered by {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
                            embeds.append(embed)

                            channel_id = result[1]
                            try:
                                channel = bot.get_channel(channel_id)
                                await channel.send(content=f"[.]({urll})") ###[.]({urll})
                                #await msg.add_reaction("<a:loading:1129810812995911730>")
                                #await asyncio.sleep(1.50)
                                #await msg.clear_reactions()
                                #await asyncio.sleep(1.90)
                                #await msg.edit(embed=embed)
                                #await msg.add_reaction("<:kissmark_1f48b:1147152647242133645>")
                                await asyncio.sleep(13)
                            except:
                                pass
                    else:
                        msg = await slay.send(allowed_mentions=discord.AllowedMentions(users=True), view=view, content=f"The owner: <@{owner_id}> has not voted\nTo make stop sending this message please vote the bot or unset the autonsfw") ##print
                        # Send vote reminder

@tasks.loop(seconds=10) 
async def hentai():    
 for i in range(50):
  pics = ["hentai", "4k", "pussy", "bj", "cum"]
  async with bot.db.cursor() as cursor:
   await cursor.execute("SELECT * FROM hentai")
   results = await cursor.fetchall()
   for result in results:
    channel_id = result[1]
    async with aiohttp.ClientSession() as cs:
      async with cs.get(f"http://api.nekos.fun:8080/api/{random.choice(pics)}") as r: 
       res = await r.json()
       embed2 = discord.Embed(color=0x2f3136)
       embed2.set_image(url=res['image'])
       try:
        channel = bot.get_channel(channel_id)
        await channel.send(res['image'])
        await asyncio.sleep(13)  
       except:
            continue

@tasks.loop(seconds=60)
async def stats():
    embed1 = discord.Embed(color=0x2B2D31, description=f"<:repeatbutton:1129817608770818068> **loading informations**")
    embed = discord.Embed(color=0x2B2D31, description=f" ").set_thumbnail(url=bot.user.display_avatar)
    embed.add_field(name="Bot", value=f"Latency: `{round(bot.latency * 1000)}ms`\nServing: `{len(bot.guilds)} servers`\nMonitoring: `{len(set(bot.get_all_members()))} users`\nCommands: `{len(set(bot.walk_commands()))}`", inline=True)
    embed.add_field(name="System:", value=f"CPU Usage: `{psutil.cpu_percent()}%`\nMemory Usage: `{psutil.virtual_memory().percent}%`\nAvailable Memory: `{psutil.virtual_memory().available * 100 / psutil.virtual_memory().total}%`", inline=True)
    embed.set_footer(text="use", icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    slay = bot.get_channel(1143273173111033866)
    await slay.send(embed=embed)
    msg = await slay.send(embed=embed1)
    await msg.add_reaction("<a:w_w:1103337013656174652>")
    await asyncio.sleep(0.5)
    await msg.edit(embed=embed) 

@tasks.loop(seconds=60)
async def apistatus():
    header = {
    'Authorization': 'Bearer 464099bf-6179-4cd6-9fd1-e8e5041f52c5'
    }

    type = {
    'option': 'couple'
    }

    r = requests.post("https://api.usebot.lol/api", headers=header, json=type)

    embed1 = discord.Embed(color=0x2B2D31, description=f"<:repeatbutton:1129817608770818068> **loading api informations**")
    embed = discord.Embed(color=0x2B2D31, description=f" ")#.set_thumbnail(url=bot.user.display_avatar)
    embed.add_field(name="use API code status", value=r.status_code, inline=True)
    embed.set_footer(text="use", icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
    slay = bot.get_channel(1127519397385351299)
    await slay.send(embed=embed)
    msg = await slay.send(embed=embed1)
    await msg.edit(embed=embed) 

intents = discord.Intents.all() 

class Client(commands.AutoShardedBot): #commands.AutoShardedBot 
  def __init__(self):
    super().__init__(
        command_prefix=getprefix,
        shards_count=1,
        intents=intents,
        help_command=None, 
        case_insensitive=True,
        allowed_mentions=discord.AllowedMentions.none(),
        strip_after_prefix=True,  
        owner_ids=[1094511683554267197, 461914901624127489]
    ) 
    self.uptime = time.time()
    
  async def on_connect(self): 
    setattr(bot, "db", await aiosqlite.connect("main.db"))
    print("Attempting to connect to Discord's API")
    await self.load_extension("jishaku")
    for file in os.listdir("./cogs"): 
      if file.endswith(".py"):
        try: 
            await self.load_extension("cogs." + file[:-3])
            print("loaded extension {}".format(file[:-3])) 
        except Exception as e: 
           print("unable to load extension {} - {}".format(file[:-3], e))
        
  async def on_ready(self):
    await asyncio.sleep(10)
    self.add_view(vmbuttons())
    #await Music(self).start_node()
    status.start()
    female.start()
    male.start()
    anime.start()
    ricon.start()
    banner.start()
    match.start()
    fgif.start()
    mgif.start()
    agif.start()
    autocar.start()
    guns.start()
    faceless.start()
    autobody.start()
    autoshoes.start()
    autojewellry.start()
    aesthetic.start()
    cartoon.start()
    ukdrill.start()
    money.start()
    hellokitty.start()
    smoking.start()
    animals.start()
    soft.start()
    qvote.start()
    bff.start()
    couplesgif.start()
    couplespfp.start()
    kpopp.start()
    emoidk.start()
    nike.start()
    coree.start()
    automeme.start()
    autonsfw.start()
    hentai.start()
    #apistatus.start()
    print(f"logged in as {bot.user}")
bot = Client()
bot.run(os.getenv("use"), reconnect=True) #main bot token: MTA4MjY4MjM1NjkxOTQ1NTg0NQ.GXNEM4.ewvby2VBffSIb1XaHIPNaQHbU_0q6fBpol6IH0
