import discord, datetime
from discord.ext import commands
from discord import app_commands
from discord.ui import Modal, View, Button
from deep_translator import GoogleTranslator
from discord.ext.commands import Context

@app_commands.context_menu(name="translate")
async def translate(interaction: discord.Interaction, message: discord.Message): 
  if not message.content: return await interaction.response.send_message(embed=discord.Embed(color=0x2B2D31, description="{} {}: There is no message to translate".format(interaction.client.warning, interaction.user.mention)), ephemeral=True)
  options = [
    discord.SelectOption(
      label="english"
    ),
    discord.SelectOption(
      label="croatian"
    ),
    discord.SelectOption(
      label="french"
    ),
    discord.SelectOption(
      label="spanish"
    ),
    discord.SelectOption(
      label="arabic"
    ),
    discord.SelectOption(
      label="russian"
    ),
    discord.SelectOption(
      label="german"
    ),
    discord.SelectOption(
      label="swedish"
    ),
    discord.SelectOption(
      label="chinese"
    ),
    discord.SelectOption(
      label="japanese"
    ),
    discord.SelectOption(
      label="italian"
    )
  ]
  select = discord.ui.Select(options=options, placeholder="select a language...")
  embed = discord.Embed(color=0x2B2D31, description="🔍 {}: Select the language you want to translate `{}` in".format(interaction.user.mention, message.content))

  async def select_callback(inter: discord.Interaction): 
    if inter.user.id != interaction.user.id: return await inter.response.send_message(embed=discord.Embed(color=0x2B2D31, description="{} {}: You are not the author of this embed".format(interaction.client.warning, inter.user.mention)), ephemeral=True)
    translated = GoogleTranslator(source="auto", target=select.values[0]).translate(message.content)
    e = discord.Embed(color=0x2B2D31, title="translated to {}".format(select.values[0]), description="```{}```".format(translated))
    v = discord.ui.View()
    v.add_item(discord.ui.Button(label="original message", url=message.jump_url))
    await inter.response.edit_message(embed=e, view=v)
  select.callback = select_callback  

  view = View()
  view.add_item(select)
  await interaction.response.send_message(embed=embed, view=view)

@app_commands.context_menu(name="user avatar")
async def user_avatar(interaction: discord.Interaction, member: discord.Member):
        button1 = Button(label="default avatar", url=member.avatar.url or member.default_avatar.url)
        button2 = Button(label="server avatar", url=member.display_avatar.url)
        embed = discord.Embed(color=0x2B2D31, title=f"{member.name}'s avatar", url=member.display_avatar.url)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        embed.set_image(url=member.display_avatar.url)
        view = View()
        view.add_item(button1)
        view.add_item(button2) 
        await interaction.response.send_message(embed=embed, view=view)

@app_commands.context_menu(name="user banner")
async def user_banner(interaction: discord.Interaction, member: discord.Member): 
     user = await interaction.client.fetch_user(member.id)
     if not user.banner:
      if user.accent_colour is None: return await interaction.client.ext.send_error(interaction, "**{}** Doesn't have a banner".format(str(user)), ephemeral=True) 
      hexcolor = hex(user.accent_colour.value)
      hex2 = hexcolor.replace("0x", "")
      e = discord.Embed(color=0x2B2D31, title=f"{user.name}'s banner", url=f"https://singlecolorimage.com/get/{hex2}/400x100")
      e.set_image(url=f"https://singlecolorimage.com/get/{hex2}/400x100")
      return await interaction.response.send_message(embed=e)
       
     embed = discord.Embed(color=0x2B2D31, title=f"{user.name}'s banner", url=user.banner.url)
     embed.set_image(url=user.banner.url)
     await interaction.response.send_message(embed=embed)


class Cog(commands.Cog):
 def __init__(self, bot: commands.AutoShardedBot):
    self.bot = bot
    try:
            self.bot.tree.add_command(user_avatar)
            self.bot.tree.add_command(translate)
            self.bot.tree.add_command(user_banner)
            print("added")
    except:
            self.bot.tree.remove_command("user avatar", type=discord.AppCommandType.message)
            self.bot.tree.remove_command("translate", type=discord.AppCommandType.message)
            self.bot.tree.remove_command("user banner", type=discord.AppCommandType.user)
            self.bot.tree.add_command(user_avatar)
            self.bot.tree.add_command(translate)
            self.bot.tree.add_command(user_banner)

 @app_commands.command(name="poll", description="create a poll")
 async def poll(self, ctx: discord.Interaction, question: str, first: str, second: str):
  embed = discord.Embed(color=0x2B2D31, title=question, description=f"1️⃣ - {first}\n\n2️⃣ - {second}")
  embed.set_footer(text=f"poll created by {ctx.user}")
  channel = self.bot.get_channel(ctx.channel.id)
  await ctx.response.send_message('poll sent', ephemeral=True)
  mes = await channel.send(embed=embed)
  emoji1 = '1️⃣'
  emoji2 = '2️⃣'
  await mes.add_reaction(emoji1)
  await mes.add_reaction(emoji2)    

async def setup(bot) -> None:
    await bot.add_cog(Cog(bot))    