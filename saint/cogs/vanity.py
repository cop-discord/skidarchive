import discord, datetime
from discord.ext import commands ; from datetime import datetime
from backend import classes
from backend.classes import Emojis, Colors
from cogs.events import blacklist
from discord.ext.commands import Context


class vanity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_presence_update(self, before: discord.Member, after: discord.Member):

        user = after
        guild = after.guild
        try:
            db = classes.read_json('vanity')
            vanity = db[str(after.guild.id)]['vanity']
            try: ba = str(before.activity.name).lower()
            except: ba = 'none'
            try: aa = str(after.activity.name).lower()
            except: aa = 'none'
            if ba == aa: return
            if db[str(after.guild.id)]['vanity'] in aa and db[str(after.guild.id)]['vanity'] not in ba:
                try:
                    x = after.guild.get_role(db[str(after.guild.id)]['role'])
                    await after.add_roles(x, reason='saint vanity: vanity in status')
                except: pass
                try:
                    z = await after.guild.fetch_channel(db[str(after.guild.id)]['channel'])
                    await z.send(f'{after.mention}', embed=discord.Embed(color=0x2B2D31, description=f"{db[str(after.guild.id)]['message'].format(user=user, guild=guild, vanity=vanity)}"))
                except: pass
            elif db[str(after.guild.id)]['vanity'] not in aa and db[str(after.guild.id)]['vanity'] in ba:
                try:
                    x = after.guild.get_role(db[str(after.guild.id)]['role'])
                    await after.remove_roles(x, reason='saint vanity: vanity removed from status')
                except: pass

        except:
            #traceback.print_exc()
            pass

    @commands.hybrid_command(aliases=['guildvanity'], description="vanity")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist()
    async def gv(self, ctx: commands.Context):
        if ctx.guild.vanity_url_code is None:
            embed=discord.Embed(color=0x2B2D31, description=f"> **This server does not have a vanity.**")
            embed.set_footer(text="No Vanity")

        elif ctx.guild.vanity_url_code is not None:
            embed=discord.Embed(color=0x2B2D31, description=f"> **Guild Vanity:** {ctx.guild.vanity_url_code}")
            
        await ctx.send(embed=embed)

    @commands.hybrid_group(name='vanity', aliases=['v'], invoke_without_command=True, description="vanity")
    @commands.has_permissions(manage_guild=True)
    @blacklist()
    async def vanity(self, ctx):

        subcmds = ",vanity clear\n,vanity role\n,vanity channel\n,vanity message\n,vanity set"
        subcmds = f"```{subcmds}```"
        note1 = discord.Embed(color=0x2B2D31, timestamp=datetime.now())
        note1.set_author(name=f"vanity", icon_url=self.bot.user.display_avatar)
        note1.add_field(name=f"Info", value=f"> **description:** manage the guild's vanity role\n> **aliases:** v")  
        note1.add_field(name=f"Sub Cmds", value=subcmds, inline=False)
        await ctx.reply(embed=note1)

    @vanity.command(name='clear', description="vanity")
    @commands.has_permissions(manage_guild=True)
    @blacklist()
    async def vanity_clear(self, ctx):

        try:
            db = classes.read_json('vanity')
            db.pop(str(ctx.guild.id))
            classes.write_json(db, 'vanity')
        except:
            pass
        await ctx.reply('<:thumbsup:1129811199626854534>')

    @vanity.command(name='role', description="vanity")
    @commands.has_permissions(manage_guild=True)
    @blacklist()
    async def vanity_role(self, ctx, *, role: discord.Role=None):

        try:
            db = classes.read_json('vanity')
            db[str(ctx.guild.id)]['role'] = role.id 
            classes.write_json(db, 'vanity')
        except:
            db = classes.read_json('vanity')
            db[str(ctx.guild.id)] = {}
            classes.write_json(db, 'vanity')
            db = classes.read_json('vanity')
            db[str(ctx.guild.id)]['role'] = role.id
            db[str(ctx.guild.id)]['channel'] = None
            db[str(ctx.guild.id)]['message'] = None
            db[str(ctx.guild.id)]['vanity'] = None
            classes.write_json(db, 'vanity')
        await ctx.send('<:thumbsup:1129811199626854534>')

    @vanity.command(name='channel', description="vanity")
    @commands.has_permissions(manage_guild=True)
    @blacklist()
    async def vanity_channel(self, ctx, *, channel: discord.TextChannel):

        try:
            db = classes.read_json('vanity')
            db[str(ctx.guild.id)]['channel'] = channel.id 
            classes.write_json(db, 'vanity')
        except:
            db = classes.read_json('vanity')
            db[str(ctx.guild.id)] = {}
            classes.write_json(db, 'vanity')
            db = classes.read_json('vanity')
            db[str(ctx.guild.id)]['role'] = None
            db[str(ctx.guild.id)]['channel'] = channel.id
            db[str(ctx.guild.id)]['message'] = None
            db[str(ctx.guild.id)]['vanity'] = None
            classes.write_json(db, 'vanity')
        await ctx.send('<:thumbsup:1129811199626854534>')

    @vanity.command(name='message', description="vanity")
    @commands.has_permissions(manage_guild=True)
    @blacklist()
    async def vanity_message(self, ctx, *, message: str=None):

        try:
            db = classes.read_json('vanity')
            db[str(ctx.guild.id)]['message'] = message 
            classes.write_json(db, 'vanity')
        except:
            db = classes.read_json('vanity')
            db[str(ctx.guild.id)] = {}
            classes.write_json(db, 'vanity')
            db = classes.read_json('vanity')
            db[str(ctx.guild.id)]['role'] = None
            db[str(ctx.guild.id)]['channel'] = None
            db[str(ctx.guild.id)]['message'] = message
            db[str(ctx.guild.id)]['vanity'] = None
            classes.write_json(db, 'vanity')
        await ctx.send('<:thumbsup:1129811199626854534>')

    @vanity.command(name='set', description="vanity")
    @commands.has_permissions(manage_guild=True)
    @blacklist()
    async def vanity_set(self, ctx, vanity: str=None):

        try:
            db = classes.read_json('vanity')
            db[str(ctx.guild.id)]['vanity'] = vanity 
            classes.write_json(db, 'vanity')
        except:
            db = classes.read_json('vanity')
            db[str(ctx.guild.id)] = {}
            classes.write_json(db, 'vanity')
            db = classes.read_json('vanity')
            db[str(ctx.guild.id)]['role'] = None
            db[str(ctx.guild.id)]['channel'] = None
            db[str(ctx.guild.id)]['message'] = None
            db[str(ctx.guild.id)]['vanity'] = vanity
            classes.write_json(db, 'vanity')
        await ctx.send('<:thumbsup:1129811199626854534>')


    @commands.Cog.listener()
    @blacklist()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.BotMissingPermissions):
            permissions = '\n'.join([x.lower() for x in error.missing_permissions])
            permissions = permissions.replace('_', ' ')
            await ctx.reply(embed=discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention}**:** i'm missing the **{permissions}** permission"))

        elif isinstance(error, commands.MissingPermissions):
            permissions = '\n'.join([i.lower() for i in error.missing_permissions])
            permissions = permissions.replace('_', ' ')
            await ctx.reply(embed=discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention}**:** you're missing the **{permissions}** permission"))

async def setup(bot):
    await bot.add_cog(vanity(bot))