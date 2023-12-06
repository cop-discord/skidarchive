import discord ; from discord.ext import commands ; from discord import Embed ; from backend.classes import Colors, Emojis ; from cogs.events import noperms, blacklist
from discord.ext.commands import Context

class voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        async with self.bot.db.cursor() as cursor: 
            await cursor.execute("CREATE TABLE IF NOT EXISTS vmutelock (channel_id INTEGER, mute BOOLEAN);")
            await self.bot.db.commit()

    @commands.hybrid_command(help=f"mass moves users", description="voice", usage="[channel]", aliases=["moveall", "dragall"])
    @blacklist()
    async def massmove(self, ctx, destination: discord.VoiceChannel):
        if not ctx.author.guild_permissions.move_members:
            await noperms(self, ctx, "move_members")
            return
        origin=ctx.author.voice.channel
        if origin.members:
            if origin != destination:
                moved = []
                for member in origin.members:
                    await member.edit(voice_channel=destination, reason=f"Massmoved by {ctx.author}")
                    moved.append(member)
                    e = Embed(
                       description=f"{Emojis.check} Moved **`{len(moved)}`** members from **`{origin.name}`** to **`{destination.name}`**",
                       color=0x2B2D31
                    )
                await ctx.reply(embed=e, mention_author=False)
            else:
                    e = Embed(
                       description=f"{Emojis.warning} You can only move members to a different voice channel",
                       color=0x2B2D31
                    )
                    await ctx.reply(embed=e, mention_author=False)
        else:
                    e = Embed(
                       description=f"{Emojis.warning} **`{origin.name}`** is an empty voice channel",
                       color=0x2B2D31
                    )
                    await ctx.reply(embed=e, mention_author=False)
    
    @commands.hybrid_command(help="drags a member", description="voice", usage="[user]")
    @blacklist()
    async def drag(self, ctx, member: discord.Member, channel: discord.VoiceChannel):
        if not ctx.author.guild_permissions.move_members:
            await noperms(self, ctx, "move_members")
            return
        if not member.voice or not member.voice.channel:
            e = Embed(
                description=f"{Emojis.warning} {member.mention} is not connected to a voice channel",
                color=0x2B2D31
            )
            await ctx.reply(embed=e, mention_author=False)               
            return
        if not channel:
            e = Embed(
                description=f"{Emojis.warning} mention a user and a channel to drag to",
                color=0x2B2D31
            )
            await ctx.reply(embed=e, mention_author=False)  
            return
        try:
            await member.move_to(channel)
            await ctx.send(f"Successfully dragged {member.name} to {channel.name}!")
        except:
            await ctx.send(f"Could not drag {member.name} to {channel.name}.")

    @commands.hybrid_command(help="server mutes a member", description="voice", usage="[user]")
    @blacklist()
    async def vmute(self, ctx, member: discord.Member):
        if not ctx.author.guild_permissions.mute_members:
            await noperms(self, ctx, "mute_members")
            return
        if not member.voice:
            e = Embed(
               description=f"{Emojis.warning} {member.name} is not in a voice channel",
               color=0x2B2D31
            )
            await ctx.reply(embed=e, mention_author=False)
            return
        
        await member.edit(mute=True)
        e = Embed(
            description=f"{Emojis.check} {member.name} just got server muted",
            color=0x2B2D31
        )
        await ctx.reply(embed=e, mention_author=False)

    @commands.hybrid_command(help="server deafens a member", description="voice", usage="[user]", aliases=["sdeaf"])
    @blacklist()
    async def vdeafen(self, ctx, member: discord.Member):
        if not ctx.author.guild_permissions.deafen_members:
            await noperms(self, ctx, "deafen_members")
            return
        if not member.voice:
            e = Embed(
               description=f"{Emojis.warning} {member.name} is not in a voice channel",
               color=0x2B2D31
            )
            await ctx.reply(embed=e, mention_author=False)
            return
        
        await member.edit(deafen=True)
        e = Embed(
            description=f"{Emojis.check} {member.name} just got server deafened",
            color=0x2B2D31
        )
        await ctx.reply(embed=e, mention_author=False)

    @commands.hybrid_command(help="unserver mutes a member", description="voice", usage="[user]")
    @blacklist()
    async def vumute(self, ctx, member: discord.Member):
        if not ctx.author.guild_permissions.mute_members:
            await noperms(self, ctx, "mute_members")
            return
        if not member.voice:
            e = Embed(
               description=f"{Emojis.warning} {member.name} is not in a voice channel",
               color=0x2B2D31
            )
            await ctx.reply(embed=e, mention_author=False)
            return
        
        await member.edit(mute=False)
        e = Embed(
            description=f"{Emojis.check} {member.name} just got unserver muted",
            color=0x2B2D31
        )
        await ctx.reply(embed=e, mention_author=False)

    @commands.hybrid_command(help="unserver deafens a member", description="voice", usage="[user]", aliases=["vudeaf"])
    @blacklist()
    async def vudeafen(self, ctx, member: discord.Member):
        if not ctx.author.guild_permissions.deafen_members:
            await noperms(self, ctx, "deafen_members")
            return
        if not member.voice:
            e = Embed(
               description=f"{Emojis.warning} {member.name} is not in a voice channel",
               color=0x2B2D31
            )
            await ctx.reply(embed=e, mention_author=False)
            return
        
        await member.edit(deafen=False)
        e = Embed(
            description=f"{Emojis.check} {member.name} just got unserver deafened",
            color=0x2B2D31
        )
        await ctx.reply(embed=e, mention_author=False)

    @commands.hybrid_command(help="disconnects a member", description="voice", usage="[user]", aliases=["vdc"])
    @blacklist()
    async def vdisconnect(self, ctx, member: discord.Member = None):
        if not ctx.author.guild_permissions.move_members:
            await noperms(self, ctx, "move_members")
            return
        if not member:
            e = Embed(
                description=f"{Emojis.warning} mention a user to disconnect from the voice channel",
                color=0x2B2D31
            )
            await ctx.reply(embed=e, mention_author=False)            
            return

        if not member.voice or not member.voice.channel:
            e = Embed(
                description=f"{Emojis.warning} {member.mention} is not connected to a voice channel",
                color=0x2B2D31
            )
            await ctx.reply(embed=e, mention_author=False)               
            return

        await member.move_to(None)
        e = Embed(
            description=f"{Emojis.check} disconnected {member.mention} from the voice channel",
            color=0x2B2D31
        )
        await ctx.reply(embed=e, mention_author=False)
    @commands.hybrid_command(help="create voice channel", description="voice", usage="[voicename]", aliases=['voicecreate', 'voicemake', 'makevoice'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    @blacklist()
    async def createvoice(self, ctx, channel_name):
        if channel_name is None:
            embed = discord.Embed(color=0x2B2D31, title="voice channel", description="create or delete a voice channel")
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            embed.add_field(name="category", value="voice")
            embed.add_field(name="commands", value=",createvoice\n,deletevoice", inline=False)
            embed.add_field(name="usage", value=f"```,createvoice .gg/runs```", inline=False)
            embed.add_field(name=f"aliases", value= "voicecreate, voicemake, makevoice\nvoicedelete, removevoice, voiceremove")
            await ctx.reply(embed=embed, mention_author=False)
            return
        if not ctx.author.guild_permissions.manage_channels:
            await noperms(self, ctx, "manage_channels")
            return
        guild = ctx.guild
        echnl = discord.utils.get(guild.channels, name=channel_name)        
        if not echnl:
            channel_name = await guild.create_voice_channel(channel_name)
            await ctx.message.delete()
            e = Embed(description=f'{Emojis.check} The **{channel_name}** voice channel has been created.')
            await ctx.send(embed = e)
        else:
            e = Embed(description=f'{Emojis.warning} That voice channel already exists.')
            await ctx.reply(embed = e, mention_author=False)   

    @commands.hybrid_command(help="delete voice channel", description="voice", usage="[channel]", aliases=['voicedelete', 'removevoice', 'voiceremove'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    @blacklist()
    async def deletevoice(self, ctx, channel_name):
        if channel_name is None:
            embed = discord.Embed(color=0x2B2D31, title="voice channel", description="create or delete a voice channel")
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            embed.add_field(name="category", value="voice")
            embed.add_field(name="commands", value=",createvoice\n,deletevoice", inline=False)
            embed.add_field(name="usage", value=f"```,createvoice .gg/kys```", inline=False)
            embed.add_field(name=f"aliases", value= "voicecreate, voicemake, makevoice\nvoicedelete, removevoice, voiceremove")
            await ctx.reply(embed=embed, mention_author=False)            
            return
        if not ctx.author.guild_permissions.manage_channels:
            await noperms(self, ctx, "manage_channels")
            return
        server = ctx.guild
        voice_channel = discord.utils.get(server.voice_channels, name=channel_name)
        if voice_channel:
            await voice_channel.delete()
            await ctx.message.delete()
            e = Embed(description=f'{Emojis.check} The **{channel_name}** voice channel has been deleted.')
            await ctx.send(embed = e)
        else:
            e = Embed(description=f'{Emojis.warning} The voice channel **{channel_name}** does not exist.')
            await ctx.reply(embed = e, mention_author=False)   

    @commands.hybrid_command(help="mute all members in a voice channel", description="voice", usage="[NONE]")
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def vmuteall(self, ctx):
        if ctx.author.voice:
            voice_channel = ctx.author.voice.channel
            muted_members = []
            for member in voice_channel.members:
                if not member.bot and member != ctx.author:
                    await member.edit(mute=True)
                    muted_members.append(member.display_name)
            if muted_members:
                e = Embed(
                    description=f"{Emojis.check} all members in {voice_channel.mention} just got server muted",
                    color=0x2B2D31
                )            
                await ctx.reply(embed=e, mention_author=False)

            else:
                e = Embed(
                description=f"{Emojis.warning} There was no one to mute in {voice_channel.mention} except for you",
                color=0x2B2D31
                )
                await ctx.reply(embed=e, mention_author=False)
        else:
            e = Embed(
               description=f"{Emojis.warning} you are not in a voice channel",
               color=0x2B2D31
            )
            await ctx.reply(embed=e, mention_author=False)   

    @commands.hybrid_command(help="unmutes all members in a voice channel", description="voice", usage="[NONE]")
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def vunmuteall(self, ctx):
        if ctx.author.voice:
            voice_channel = ctx.author.voice.channel
            muted_members = []
            for member in voice_channel.members:
                if not member.bot and member != ctx.author:
                    await member.edit(mute=False)
                    muted_members.append(member.display_name)
            if muted_members:
                e = Embed(
                    description=f"{Emojis.check} all members in {voice_channel.mention} just got unserver muted",
                    color=0x2B2D31
                )            
                await ctx.reply(embed=e, mention_author=False)
            else:
                e = Embed(
                description=f"{Emojis.warning} There was no one to unmute in {voice_channel.mention}",
                color=0x2B2D31
                )
                await ctx.reply(embed=e, mention_author=False)
        else:
            e = Embed(
               description=f"{Emojis.warning} you are not in a voice channel",
               color=0x2B2D31
            )
            await ctx.reply(embed=e, mention_author=False)   

    @commands.hybrid_command(help="deafens all members in a voice channel", description="voice", usage="[NONE]", aliases=['vdeafall'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def vdeafenall(self, ctx):
        if ctx.author.voice:
            voice_channel = ctx.author.voice.channel
            muted_members = []
            for member in voice_channel.members:
                if not member.bot and member != ctx.author:
                    await member.edit(deafen=True)
                    muted_members.append(member.display_name)
            if muted_members:
                e = Embed(
                    description=f"{Emojis.check} all members in {voice_channel.mention} just got server deafened",
                    color=0x2B2D31
                )            
                await ctx.reply(embed=e, mention_author=False)
            else:
                e = Embed(
                description=f"{Emojis.warning} There was no one to deafen in {voice_channel.mention} except for you",
                color=0x2B2D31
                )
                await ctx.reply(embed=e, mention_author=False)
        else:
            e = Embed(
               description=f"{Emojis.warning} you are not in a voice channel",
               color=0x2B2D31
            )
            await ctx.reply(embed=e, mention_author=False)   

    @commands.hybrid_command(help="undeafens all members in a voice channel", description="voice", usage="[NONE]", aliases=['vudeafall'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def vudeafenall(self, ctx):
        if ctx.author.voice:
            voice_channel = ctx.author.voice.channel
            muted_members = []
            for member in voice_channel.members:
                if not member.bot and member != ctx.author:
                    await member.edit(deafen=False)
                    muted_members.append(member.display_name)
            if muted_members:
                e = Embed(
                    description=f"{Emojis.check} all members in {voice_channel.mention} just got unserver deafened",
                    color=0x2B2D31
                )            
                await ctx.reply(embed=e, mention_author=False)

            else:
                e = Embed(
                description=f"{Emojis.warning} There was no one to undeafen in {voice_channel.mention}",
                color=0x2B2D31
                )
                await ctx.reply(embed=e, mention_author=False)
        else:
            e = Embed(
               description=f"{Emojis.warning} you are not in a voice channel",
               color=0x2B2D31
            )
            await ctx.reply(embed=e, mention_author=False)   

    @commands.hybrid_command(help="disconnects all members in a voice channel", description="voice", usage="[NONE]", aliases=['vdcall'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def vdisconnectall(self, ctx):
        if ctx.author.voice:
            voice_channel = ctx.author.voice.channel
            for member in voice_channel.members:
                if member != ctx.author:
                        await member.move_to(None)
            else:
                e = Embed(
                description=f"{Emojis.check} all members in {voice_channel.mention} just got disconnected",
                color=0x2B2D31
                )
                await ctx.reply(embed=e, mention_author=False)
        else:
            e = Embed(
               description=f"{Emojis.warning} you are not in a voice channel",
               color=0x2B2D31
            )

async def setup(bot):
    await bot.add_cog(voice(bot))