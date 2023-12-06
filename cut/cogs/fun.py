import discord, io, random, asyncio, aiohttp
from discord.ext import commands
from typing import List
from io import BytesIO
import requests
import json
import time
import dateutil
from tools.checks import Perms, Joint


class TypeRace:
    """TypeRace backend variables"""

    async def getanswer():
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://www.mit.edu/~ecprice/wordlist.100000") as r:
                byte = await r.read()
                data = str(byte, "utf-8")
                data = data.splitlines()
                mes = ""
                for _ in range(10):
                    mes = f"{mes}{random.choice(data)} "

                return mes

    def accurate(first: str, second: str):
        percentage = 0
        i = 0
        text1 = first.split()
        text2 = second.split()
        for t in text2:
            try:
                if t == text1[i]:
                    percentage += 10
                i += 1
            except:
                return percentage

        return percentage


class RockPaperScissors(discord.ui.View):
    def __init__(self, ctx: commands.Context):
        self.ctx = ctx
        self.get_emoji = {"rock": "🪨", "paper": "📰", "scissors": "✂️"}
        self.status = False
        super().__init__(timeout=10)

    async def disable_buttons(self):
        for item in self.children:
            item.disabled = True

        await self.message.edit(view=self)

    async def action(self, interaction: discord.Interaction, selection: str):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.client.ext.send_warning(
                interaction, "This is not your game", ephemeral=True
            )
        botselection = random.choice(["rock", "paper, scissors"])

        def getwinner():
            if botselection == "rock" and selection == "scissors":
                return interaction.client.user.id
            elif botselection == "rock" and selection == "paper":
                return interaction.user.id
            elif botselection == "paper" and selection == "rock":
                return interaction.client.user.id
            elif botselection == "paper" and selection == "scissors":
                return interaction.user.id
            elif botselection == "scissors" and selection == "rock":
                return interaction.user.id
            elif botselection == "scissors" and selection == "paper":
                return interaction.client.user.id
            else:
                return "tie"

        if getwinner() == "tie":
            await interaction.response.edit_message(
                embed=discord.Embed(
                    color=interaction.client.color,
                    title="Tie!",
                    description=f"```You both picked {self.get_emoji.get(selection)}```",
                )
            )
        elif getwinner() == interaction.user.id:
            await interaction.response.edit_message(
                embed=discord.Embed(
                    color=interaction.client.color,
                    title="You won!",
                    description=f"```You picked {self.get_emoji.get(selection)} and the bot picked {self.get_emoji.get(botselection)}```",
                )
            )
        else:
            await interaction.response.edit_message(
                embed=discord.Embed(
                    color=interaction.client.color,
                    title="Bot won!",
                    description=f"```You picked {self.get_emoji.get(selection)} and the bot picked {self.get_emoji.get(botselection)}```",
                )
            )
        await self.disable_buttons()
        self.status = True

    @discord.ui.button(emoji="☁")
    async def rock(self, interaction: discord.Interaction, button: discord.ui.Button):
        return await self.action(interaction, "rock")

    @discord.ui.button(emoji="📰")
    async def paper(self, interaction: discord.Interaction, button: discord.ui.Button):
        return await self.action(interaction, "paper")

    @discord.ui.button(emoji="✂️")
    async def scissors(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        return await self.action(interaction, "scissors")

    async def on_timeout(self):
        if self.status == False:
            await self.disable_buttons()


class BlackTea:
    """Backend variables for BlackTea"""

    MatchStart = {}
    lifes = {}

    async def get_string():
        lis = await BlackTea.get_words()
        word = random.choice([l for l in lis if len(l) > 3])
        return word[:3]

    async def get_words():
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://www.mit.edu/~ecprice/wordlist.100000") as r:
                byte = await r.read()
                data = str(byte, "utf-8")
                return data.splitlines()


class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(
        self, x: int, y: int, player1: discord.Member, player2: discord.Member
    ):
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y
        self.player1 = player1
        self.player2 = player2

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            if interaction.user != self.player1:
                return await interaction.client.ext.send_warning(
                    interaction, "You cannot interact with this", ephemeral=True
                )
            self.style = discord.ButtonStyle.danger
            self.label = "X"
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = f"It is now **{self.player2.name}**'s turn"
        else:
            if interaction.user != self.player2:
                return await interaction.client.ext.send_warning(
                    interaction, "You cannot interact with this", ephemeral=True
                )
            self.style = discord.ButtonStyle.success
            self.label = "O"
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = f"It is now **{self.player1.name}**'s turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = f"**{self.player1.name}** won!"
            elif winner == view.O:
                content = "**{}** won!".format(self.player2.name)
            else:
                content = "Its a **tie**!"

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


class TicTacToe(discord.ui.View):
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y, player1, player2))

    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self.view)


class fun(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
        self.joint_emoji = "🍃"
        self.smoke = "🌬️"
        self.joint_color = 0x2B2D31
        self.book = "📖"

    @commands.command(description="insult a member", help="fun", usage="[member]")
    async def insult(self, ctx: commands.Context, member: discord.Member):
        data = await self.bot.session.json(
            "https://evilinsult.com/generate_insult.php?lang=en&type=json"
        )
        embed = discord.Embed(
            title=f"You just got packed 🚬",
            description=f"```{data['insult']}```",
            color=self.bot.color,
        )
        await ctx.reply(content=member.mention, embed=embed)

    @commands.command(description="send a random dog image", help="fun")
    async def dog(self, ctx):
        response = requests.get("https://random.dog/woof.json")
        data = json.loads(response.text)
        image = data["url"]
        embed = discord.Embed(title=f"Doggos", color=self.bot.color)
        embed.set_image(url=image)
        embed.set_footer(
            icon_url=ctx.author.avatar, text=f"Requested by {ctx.author.name}"
        )
        await ctx.reply(embed=embed)

    @commands.command(description="send a random cat image", help="fun")
    async def cat(self, ctx):
        response = requests.get("https://cataas.com/cat?json=true")
        data = json.loads(response.text)
        image = data["url"]
        embed = discord.Embed(title=f"Kitty cat's", color=self.bot.color)
        embed.set_image(url=f"https://cataas.com/{image}")
        embed.set_footer(
            icon_url=ctx.author.avatar, text=f"Requested by {ctx.author.name}"
        )
        await ctx.reply(embed=embed)

    @commands.command(description="send a random bird image", help="fun")
    async def bird(self, ctx):
        response = requests.get("https://api.alexflipnote.dev/birb")
        data = json.loads(response.text)
        image = data["file"]
        embed = discord.Embed(title=f"Tweet Tweet its a Bird!", color=self.bot.color)
        embed.set_image(url=image)
        embed.set_footer(
            icon_url=ctx.author.avatar, text=f"Requested by {ctx.author.name}"
        )
        await ctx.reply(embed=embed)

    @commands.hybrid_command(description="send a random capybara image", help="fun")
    async def capybara(self, ctx):
        response = requests.get("https://api.capy.lol/v1/capybara?json=true")
        data = json.loads(response.text)
        image = data["data"]["url"]
        embed = discord.Embed(title=f"CAPYYYYY BARASSSS", color=self.bot.color)
        embed.set_image(url=image)
        embed.set_footer(
            icon_url=ctx.author.avatar, text=f"Requested by {ctx.author.name}"
        )
        await ctx.reply(embed=embed)

    @commands.command(description="say a message", help="fun", usage="[message]")
    async def say(self, ctx, *, msg):
        await ctx.message.delete()
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label=f"Said by {ctx.author}", disabled=True))
        await ctx.send(content=msg, view=view)

    @commands.command(
        name="choose",
        description="choose between multiple options",
        help="fun",
        usage="[choices]\nexample: ;choose apple, samsung, lg",
    )
    async def choose(self, ctx: commands.Context, *, choice: str):
        choices = choice.split(",")
        if len(choices) == 1:
            return await ctx.reply("put a ',' between your choices")
        await ctx.reply(content=f"{random.choice(choices)}")

    @commands.command(
        aliases=["ttt"],
        description="play tictactoe with a friend",
        help="fun",
        usage="[member]",
    )
    async def tictactoe(self, ctx: commands.Context, *, member: discord.Member):
        # if member is ctx.author: return await ctx.reply("you can't **play** with yourself")
        if member.bot:
            return await ctx.reply("bots can't play games")
        embed = discord.Embed(
            color=self.bot.color,
            description=f"**{ctx.author.name}** wants to play **tictactoe** with you, do you accept?",
        )
        style = discord.ButtonStyle.gray
        yes = discord.ui.Button(emoji=self.bot.yes, style=style)
        no = discord.ui.Button(emoji=self.bot.no, style=style)

        async def yes_callback(interaction: discord.Interaction):
            if interaction.user != member:
                em = discord.Embed(
                    color=self.bot.color,
                    description=f"{self.bot.warning} {interaction.user.mention}: You are not the author of this embed",
                )
                return await interaction.response.send_message(embed=em, ephemeral=True)
            vi = TicTacToe(ctx.author, member)
            await interaction.message.delete()
            vi.message = await ctx.send(
                content=f"Its **{ctx.author.name}** turn", embed=None, view=vi
            )

        async def no_callback(interaction: discord.Interaction):
            if interaction.user != member:
                em = discord.Embed(
                    color=self.bot.color,
                    description=f"{self.bot.warning} {interaction.user.mention}: You are not the author of this embed",
                )
                return await interaction.response.send_message(embed=em, ephemeral=True)
            await interaction.response.edit_message(
                f"Looks like **{interaction.user.name}** doesn't want to play tictactoe right now",
                view=None,
                content=ctx.author.mention,
            )

        yes.callback = yes_callback
        no.callback = no_callback
        view = discord.ui.View()
        view.add_item(yes)
        view.add_item(no)
        await ctx.send(embed=embed, view=view, content=member.mention)

    @commands.command(
        description="sends a definition of a word", help="fun", usage="[word]"
    )
    async def urban(self, ctx, *, word):
        embeds = []
        try:
            data = await self.bot.session.json(
                "http://api.urbandictionary.com/v0/define", params={"term": word}
            )
            defs = data["list"]
            for defi in defs:
                e = discord.Embed(
                    title=f"{word}'s Definition",
                    color=self.bot.color,
                    description=f"```{defi['definition']}```",
                )
                # e.set_author(name=word, url=defi["permalink"])
                e.add_field(
                    name="Example:", value=f"```{defi['example']}```", inline=False
                )
                e.set_footer(text=f"{defs.index(defi)+1}/{len(defs)}")
                embeds.append(e)
            return await ctx.paginator(embeds)
        except Exception as e:
            await ctx.send_warning("No definition found for **{}**".format(word))

    @commands.command(
        name="8ball",
        description="answers to your question",
        usage="[question]",
        help="fun",
    )
    async def mtball(self, ctx: commands.Context, *, arg):
        rand = [
            "**Yes**",
            "**No**",
            "**definitely yes**",
            "**Of course not**",
            "**Maybe**",
            "**Never**",
            "**Yes, dummy**",
            "**No wtf**",
        ]
        e = discord.Embed(
            color=self.bot.color,
            description=f"Question: {arg}\nAnswer: {random.choice(rand)}",
        )
        await ctx.reply(embed=e)

    @commands.command(
        description="ask a question to ben", help="fun", usage="[question]"
    )
    async def ben(self, ctx, *, question):
        rand = [
            "./tools/videos/benhoho.mp4",
            "./tools/videos/benno.mp4",
            "./tools/videos/benuhh.mp4",
            "./tools/videos/benyes.mp4",
        ]
        resp = random.choice(rand)
        await ctx.reply(file=discord.File(rf"{resp}"))

    @commands.command(
        description="check how many bitches an user has", help="fun", usage="<member>"
    )
    async def bitches(
        self, ctx: commands.Context, *, user: discord.Member = commands.Author
    ):
        choices = ["regular", "still regular", "lol", "xd", "id", "zero", "infinite"]
        if random.choice(choices) == "infinite":
            result = "∞"
        elif random.choice(choices) == "zero":
            result = "0"
        else:
            result = random.randint(0, 100)
        await ctx.send_neutral(f"{user.mention} has `{result}` bitches")

    @commands.command(description="play blacktea with your friends", help="fun")
    async def blacktea(self, ctx: commands.Context):
        try:
            if BlackTea.MatchStart[ctx.guild.id] is True:
                return await ctx.reply(
                    embed=discord.Embed(
                        color=self.bot.color,
                        description=f"{self.bot.warning} {ctx.author.mention}: Someone is already playing blacktea in this server",
                    )
                )
        except KeyError:
            pass

        BlackTea.MatchStart[ctx.guild.id] = True
        embed = discord.Embed(
            color=self.bot.color,
            title="BlackTea MatchMaking",
            description="```- Press 🍵 to join\n- Game starts in 20 seconds\n- The game need at least 2 players to start\n- Every player has 3 lifes\n- Say a word with the given letters```",
        )
        embed.set_author(
            name=ctx.author.global_name if ctx.author.global_name else ctx.author.name,
            icon_url=ctx.author.display_avatar.url,
        )
        mes = await ctx.send(embed=embed)
        await mes.add_reaction("🍵")
        await asyncio.sleep(20)
        me = await ctx.channel.fetch_message(mes.id)
        players = [user.id async for user in me.reactions[0].users()]
        # players.remove(self.bot.user.id)

        if len(players) < 2:
            BlackTea.MatchStart[ctx.guild.id] = False
            return await ctx.send(
                embed=discord.Embed(
                    color=self.bot.color,
                    description="😦 {}, not enough players joined to start blacktea".format(
                        ctx.author.mention
                    ),
                ),
                allowed_mentions=discord.AllowedMentions(users=True),
            )

        while len(players) > 1:
            for player in players:
                strin = await BlackTea.get_string()
                await ctx.send(
                    embed=discord.Embed(
                        color=self.bot.color,
                        description=f"⏰ <@{player}>, type a word containing **{strin.upper()}** in **10 seconds**",
                    )
                )

                def is_correct(msg):
                    return msg.author.id == player

                try:
                    message = await self.bot.wait_for(
                        "message", timeout=10, check=is_correct
                    )
                except asyncio.TimeoutError:
                    try:
                        BlackTea.lifes[player] = BlackTea.lifes[player] + 1
                        if BlackTea.lifes[player] == 3:
                            await ctx.send(
                                embed=discord.Embed(
                                    color=self.bot.color,
                                    description=f"☠ <@{player}>, you are eliminated",
                                )
                            )
                            BlackTea.lifes[player] = 0
                            players.remove(player)
                            continue
                    except KeyError:
                        BlackTea.lifes[player] = 0
                    await ctx.send(
                        embed=discord.Embed(
                            color=self.bot.color,
                            description=f"💥 <@{player}>, you didn't reply on time! **{2-BlackTea.lifes[player]}** lifes remaining",
                        )
                    )
                    continue
                i = 0
                for word in await BlackTea.get_words():
                    if (
                        strin.lower() in message.content.lower()
                        and word.lower() in message.content.lower()
                    ):
                        i = 1
                        pass
                if i == 0:
                    try:
                        BlackTea.lifes[player] = BlackTea.lifes[player] + 1
                        if BlackTea.lifes[player] == 3:
                            await ctx.send(
                                embed=discord.Embed(
                                    color=self.bot.color,
                                    description=f"☠ <@{player}>, you are eliminated",
                                )
                            )
                            BlackTea.lifes[player] = 0
                            players.remove(player)
                            continue
                    except KeyError:
                        BlackTea.lifes[player] = 0
                    await ctx.send(
                        embed=discord.Embed(
                            color=self.bot.color,
                            description=f"💥 <@{player}>, incorrect word! **{2-BlackTea.lifes[player]}** remaining",
                        )
                    )
                else:
                    await message.add_reaction("✅")
                    i = 0

        await ctx.send(
            embed=discord.Embed(
                color=self.bot.color, description=f"👑 <@{players[0]}> won the game"
            )
        )
        BlackTea.lifes[players[0]] = 0
        BlackTea.MatchStart[ctx.guild.id] = False

    @commands.command(
        aliases=["dicksize", "cocksize", "penissize"],
        description="returns a persons dick size",
        help="fun",
    )
    async def ppsize(self, ctx: commands.Context, user: discord.Member = None):
        size = "8" + "=" * random.randint(1, 12) + "D"
        if user is None:
            embed = discord.Embed(
                description=f"> :warning: - Please **mention a user** to view their dick size.",
                color=self.bot.color,
            )
            await ctx.reply(embed=embed)
            return
        embed = discord.Embed(
            title=f"{user}'s Dick Size:",
            description=f"```{size}```",
            color=self.bot.color,
        )
        await ctx.reply(embed=embed)

    @commands.command(description="returns how gay a person is", help="fun")
    async def howgay(self, ctx: commands.Context, user: discord.Member = None):
        if user is None:
            embed = discord.Embed(
                description=f"> :warning: - Please **mention a user** to view how gay they are.",
                color=self.bot.color,
            )
            await ctx.reply(embed=embed)
            return
        if user.id in self.bot.owner_ids:
            embed = discord.Embed(
                title=f"🏳️‍🌈 {user} is 0% gay 🏳️‍🌈", color=self.bot.color
            )
            await ctx.reply(embed=embed)
            return
        percentage = str(random.randint(15, 100)) + "%"
        embed = discord.Embed(
            title=f"🏳️‍🌈 {user} is {percentage} gay 🏳️‍🌈", color=self.bot.color
        )
        await ctx.reply(embed=embed)

    @commands.command(description="greed is being a little sus!", help="fun")
    async def check(self, ctx: commands.Context):
        await ctx.reply("**Im here bitch.**")

    @commands.command(description="returns random bible verse", help="fun")
    async def bible(self, ctx: commands.Context):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                "https://labs.bible.org/api/?passage=random&type=json"
            ) as r:
                byte = await r.read()
                data = str(byte, "utf-8")
                data = data.replace("[", "").replace("]", "")
                bible = json.loads(data)
                embed = discord.Embed(
                    color=self.bot.color, description=f"```{bible['text']}```"
                ).set_author(
                    name="{} {}:{}".format(
                        bible["bookname"], bible["chapter"], bible["verse"]
                    ),
                    icon_url="https://m.media-amazon.com/images/I/816Etq5qEwL._AC_UF894,1000_QL80_.jpg",
                )
                await ctx.reply(embed=embed)

    @commands.command(
        aliases=["rps"], description="play rock paper scissors with greed", help="fun"
    )
    async def rockpaperscisssors(self, ctx: commands.Context):
        view = RockPaperScissors(ctx)
        embed = discord.Embed(
            color=self.bot.color,
            title="Rock Paper Scissors!",
            description="```Click a button to play!```",
        )
        view.message = await ctx.reply(embed=embed, view=view)

    @commands.command(description="sends a random advice", help="fun")
    async def advice(self, ctx: commands.Context):
        byte = await self.bot.session.read("https://api.adviceslip.com/advice")
        data = str(byte, "utf-8")
        data = data.replace("[", "").replace("]", "")
        js = json.loads(data)
        embed = discord.Embed(
            title=f"You probably need some advice, here.",
            description=f"```{js['slip']['advice']}```",
            color=self.bot.color,
        )
        return await ctx.reply(embed=embed)

    @commands.command(description="see how fast are you typing", help="fun")
    async def typerace(self, ctx: commands.Context):
        answer = await TypeRace.getanswer()
        mam = answer
        timer = 30
        r = await self.bot.session.read(
            "https://textoverimage.moesif.com/image",
            params={
                "image_url": "https://singlecolorimage.com/get/18191c/600x300",
                "text": answer,
                "text_color": "f2f1f4ff",
                "text_size": "32",
                "y_align": "middle",
                "x_align": "center",
            },
        )
        embed = discord.Embed(
            color=self.bot.color,
            description=f"```You have to type the following text in 30 seconds```",
        )
        await ctx.reply(embed=embed, file=discord.File(BytesIO(r), filename="text.png"))
        startTime = time.time()

        def is_correct(msg):
            return msg.author == ctx.author

        try:
            guess = await self.bot.wait_for("message", check=is_correct, timeout=timer)
        except asyncio.TimeoutError:
            return await ctx.reply(
                embed=discord.Embed(
                    color=self.bot.color,
                    description="```🙁 you took too long to reply```",
                )
            )

        if guess.content == mam:
            fintime = time.time()
            total = fintime - startTime
            embed = discord.Embed(
                color=self.bot.color,
                title="Congratulations!",
                description=f"```You typed the message perfectly (100% accuracy) in {total:.2f} seconds```",
            )
            return await guess.reply(embed=embed)
        else:
            fintime = time.time()
            total = fintime - startTime
            embed = discord.Embed(
                title="Good Job!",
                color=self.bot.color,
                description="```You typed the sentence in {} seconds with an accuracy of {}%```".format(
                    f"{total:.2f}", TypeRace.accurate(guess.content, mam)
                ),
            )
            return await guess.reply(embed=embed)

    async def joint_send(self, ctx: commands.Context, message: str) -> discord.Message:
        embed = discord.Embed(
            color=self.joint_color,
            description=f"{self.joint_emoji} {ctx.author.mention}: {message}",
        )
        return await ctx.reply(embed=embed)

    async def smoke_send(self, ctx: commands.Context, message: str) -> discord.Message:
        embed = discord.Embed(
            color=self.bot.color,
            description=f"{self.smoke} {ctx.author.mention}: {message}",
        )
        return await ctx.reply(embed=embed)

    @commands.group(
        name="joint",
        invoke_without_command=True,
        description="Have fun with a joint",
        help="fun",
    )
    async def jointcmd(self, ctx):
        return await ctx.create_pages()

    @jointcmd.command(
        name="toggle",
        help="fun",
        description="toggle the server joint",
        brief="manage guild",
    )
    @Perms.get_perms("manage_guild")
    async def joint_toggle(self, ctx: commands.Context):
        check = await self.bot.db.fetchrow(
            "SELECT * FROM joint WHERE guild_id = {}".format(ctx.guild.id)
        )
        if not check:
            await self.bot.db.execute(
                "INSERT INTO joint VALUES ($1,$2,$3)", ctx.guild.id, 0, ctx.author.id
            )
            return await self.joint_send(ctx, "The joint is yours")
        await self.bot.db.execute("DELETE FROM joint WHERE guild_id = $1", ctx.guild.id)
        return await ctx.reply(
            embed=discord.Embed(
                color=self.bot.color,
                description=f"{self.smoke} {ctx.author.mention}: Got rid of the server's joint",
            )
        )

    @jointcmd.command(
        name="stats",
        help="fun",
        description="check joint stats",
        aliases=["status", "settings"],
    )
    @Joint.check_joint()
    async def joint_stats(self, ctx: commands.Context):
        check = await self.bot.db.fetchrow(
            "SELECT * FROM joint WHERE guild_id = $1", ctx.guild.id
        )
        embed = discord.Embed(
            color=self.joint_color,
            description=f"{self.smoke} hits: **{check['hits']}**\n{self.joint_emoji} Holder: <@{check['holder']}>",
        )
        embed.set_author(icon_url=ctx.guild.icon, name=f"{ctx.guild.name}'s joint")
        return await ctx.reply(embed=embed)

    @jointcmd.command(name="hit", help="fun", description="hit the server joint")
    @Joint.check_joint()
    @Joint.joint_owner()
    async def joint_hit(self, ctx: commands.Context):
        mes = await self.joint_send(ctx, "Hitting the **joint**.....")
        await asyncio.sleep(2)
        check = await self.bot.db.fetchrow(
            "SELECT * FROM joint WHERE guild_id = $1", ctx.guild.id
        )
        newhits = int(check["hits"] + 1)
        embed = discord.Embed(
            color=self.bot.color,
            description=f"{self.smoke} {ctx.author.mention}: You just hit the **joint**. This server has a total of **{newhits}** hits!",
        )
        await mes.edit(embed=embed)
        await self.bot.db.execute(
            "UPDATE joint SET hits = $1 WHERE guild_id = $2", newhits, ctx.guild.id
        )

    @joint_hit.error
    async def on_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, commands.CommandOnCooldown):
            return await self.joint_send(
                ctx, "You are getting too high! Please wait until you can hit again"
            )

    @jointcmd.command(
        name="pass",
        help="fun",
        description="pass the joint to someone else",
        usage="[member]",
    )
    @Joint.check_joint()
    @Joint.joint_owner()
    async def joint_pass(self, ctx: commands.Context, *, member: discord.Member):
        if member.id == self.bot.user.id:
            return await ctx.reply("Thank you, but i do not smoke")
        elif member.bot:
            return await ctx.send_warning("Bots do not smoke")
        elif member.id == ctx.author.id:
            return await ctx.send_warning("You already have the **joint**")
        await self.bot.db.execute(
            "UPDATE joint SET holder = $1 WHERE guild_id = $2", member.id, ctx.guild.id
        )
        await self.joint_send(ctx, f"Passing the **joint** to **{member.name}**")

    @jointcmd.command(name="steal", help="fun", description="steal the server's joint")
    @Joint.check_joint()
    async def joint_steal(self, ctx: commands.Context):
        check = await self.bot.db.fetchrow(
            "SELECT * FROM joint WHERE guild_id = $1", ctx.guild.id
        )
        if check["holder"] == ctx.author.id:
            return await self.joint_send(ctx, "You already have the **joint**")
        chances = ["yes", "yes", "yes", "no", "no"]
        if random.choice(chances) == "no":
            return await self.smoke_send(
                ctx,
                f"You tried to steal the **joint** and **{(await self.bot.fetch_user(int(check['holder']))).name}** hit you",
            )
        await self.bot.db.execute(
            "UPDATE joint SET holder = $1 WHERE guild_id = $2",
            ctx.author.id,
            ctx.guild.id,
        )
        return await self.joint_send(ctx, "You stole the server **joint**")


async def setup(bot):
    await bot.add_cog(fun(bot))
