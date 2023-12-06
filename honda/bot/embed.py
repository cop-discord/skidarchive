import discord


class Embed(discord.Embed):
	def __init__(self, desc):
		super().__init__(color=0x2B2D31,description=desc)
  
class ErrorEmbed(discord.Embed):
	def __init__(self, error):
		super().__init__(color=0x2B2D31,description=error)