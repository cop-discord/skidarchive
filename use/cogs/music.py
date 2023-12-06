import asyncio, random, discord, async_timeout, pomice
from typing import Literal
from discord.ext import commands
from discord.ext.commands import Context

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.music = "đźŽµ"
    
    async def start_node(self):
      await self.bot.wait_until_ready()
      self.bot.node = await pomice.NodePool().create_node(bot=self.bot, host="23.26.60.10", port=2333, password="wetnakedboy123!", identifier="usebot", secure=False, spotify_client_id="cbbe1d3cae1642dd8819e8746195c664", spotify_client_secret="6f09eb14821948bd8c5b185228bd1a0d", apple_music=True)
    
    async def music_send(self, ctx: commands.Context, message: str) -> discord.Message:
      return await ctx.send(embed=discord.Embed(color=0x2B2D31, description=f"{self.music} {ctx.author.mention}: {message}"))
    
    @commands.Cog.listener()
    async def on_pomice_track_end(self, player: pomice.Player, track: pomice.Track, reason: str):
        await player.next()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if member.id != self.bot.user.id: return
        if not hasattr(self.bot, "node") or (player := self.bot.node.get_player(member.guild.id)) is None: return
        if not after.channel:
            await player.destroy()

    async def get_player(self, ctx: commands.Context, *, connect: bool = True):
        if not hasattr(self.bot, "node"):
            return await ctx.send("No nodes available")
        if not ctx.author.voice:
            return await ctx.send("You're not **connected** to a voice channel")
        if ctx.guild.me.voice and ctx.guild.me.voice.channel != ctx.author.voice.channel:
            return await ctx.send("I'm **already** connected to a voice channel")
        if (player := self.bot.node.get_player(ctx.guild.id)) is None or not ctx.guild.me.voice:
            if not connect:
                return await ctx.send("I'm not **connected** to a voice channel")
            else:
                await ctx.author.voice.channel.connect(cls=Player, self_deaf=True)
                player = self.bot.node.get_player(ctx.guild.id)
                player.invoke_id = ctx.channel.id
                await player.set_volume(65)

        return player

    @commands.hybrid_command(description="play a song", help="play a song", usage="[url / name]")
    async def play(self, ctx: commands.Context, *, query: str):
        player: Player = await self.get_player(ctx)
        result = await player.node.get_tracks(query=query, ctx=ctx)
        if not result:
            return await ctx.send(f"No results found for **{query}**")
        elif isinstance(result, pomice.Playlist):
            for track in result.tracks:
                await player.insert(track)
        else:
            track = result[0]
            await player.insert(track)
            if player.is_playing:
                await self.music_send(ctx, f"Added [{track.title}]({track.uri}) to the queue")
            
        if not player.is_playing:
            await player.next()

    @commands.hybrid_command(description="music", help="skip the song")
    async def skip(self, ctx: commands.Context):
        player: Player = await self.get_player(ctx, connect=False)
        if player.is_playing:
            await self.music_send(ctx, "Skipped the song")
            await player.skip()
        else:
            await ctx.send("There isn't a track playing")

    @commands.hybrid_command(description="music", help="set a loop for the track", usage="[type]\ntypes: off, track, queue")
    async def loop(self, ctx: commands.Context, option: Literal["track", "queue", "off"]):
        player: Player = await self.get_player(ctx, connect=False)
        if option == "off":
            if not player.loop:
                return await ctx.send("**Loop** isn't set")
        elif option == "track":
            if not player.is_playing:
                return await ctx.send("No **tracks** playing")
        elif option == "queue":
            if not player.queue._queue:
                return await ctx.send("There aren't any **tracks** in the queue")

        await self.music_send(ctx, f"**{option}** looping the queue")
        await player.set_loop(option if option != "off" else False)

    @commands.hybrid_command(description="music", help="pause the player")
    async def pause(self, ctx: commands.Context):
        player: Player = await self.get_player(ctx, connect=False)
        if player.is_playing and not player.is_paused:
            await self.music_send(ctx, "Paused the player")
            await player.set_pause(True)
        else:
            await ctx.sene_warning("No **track** is playing")

    @commands.hybrid_command(description="music", help="resume the player")
    async def resume(self, ctx: commands.Context):
        player: Player = await self.get_player(ctx, connect=False)
        if player.is_playing and player.is_paused:
            await self.music_send(ctx, "Resumed the player")
            await player.set_pause(False)
        else:
            await ctx.send("No **track** playing")

    @commands.hybrid_command(description="music", help="set player volume", usage="[volume]")
    async def volume(self, ctx: commands.Context, vol: int):
        player: Player = await self.get_player(ctx, connect=False)
        if not 0 <= vol <= 150:
            return await ctx.send("Volume should be between 0 and 150")
        await player.set_volume(vol)
        await self.music_send(ctx, f"Volume set to **{vol}**")

    @commands.hybrid_command(description="music", help="stop the player", aliases=["dc"])
    async def stop(self, ctx: commands.Context):
        player: Player = await self.get_player(ctx, connect=False)
        await player.teardown()
        await self.music_send(ctx, "Stopped the player")

async def setup(bot):
    await bot.add_cog(Music(bot))

class Player(pomice.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.invoke_id: int = None
        self.track: pomice.Track = None
        self.queue: asyncio.Queue = asyncio.Queue()
        self.waiting: bool = False
        self.loop: str = False

    async def play(self, track: pomice.Track):
        await super().play(track)

    async def insert(self, track: pomice.Track):
        await self.queue.put(track)

        return True

    async def next(self, no_vc: bool = False):
        if no_vc:
            if self.is_playing or self.waiting: return
        
        self.waiting = True
        if self.loop == "track" and self.track:
            track = self.track
        else:
            try:
                with async_timeout.timeout(300):
                    track = await self.queue.get()
                    if self.loop == "queue":
                        await self.queue.put(track)
            except asyncio.TimeoutError:
                return await self.teardown()

        await self.play(track)
        self.track = track
        self.waiting = False
        if (channel := self.guild.get_channel(self.invoke_id)):
            await channel.send(embed=discord.Embed(color=0x2B2D31, description=f"đźŽµ {track.requester.mention}: Now Playing [{track.title}]({track.uri})"))

        return track

    async def skip(self):
        if self.is_paused:
            await self.set_pause(False)

        return await self.stop()

    async def set_loop(self, state: str):
        self.loop = state

    async def teardown(self):
        try:
            self.queue._queue.clear()
            await self.destroy()
        except:
            pass
