import discord, datetime, asyncio, aiohttp, requests, json, asyncio, os
from discord.ext import commands, tasks
from backend.classes import Colors, Emojis
from cogs.events import sendmsg, sendmsgg, blacklist, noperms
from dotenv import load_dotenv
from discord.ext.commands import Context

load_dotenv()

async def create_automod_rule(token, guild_id, feature, value, channel_id):
    trigger_type = None

    if feature == 'invites':
        trigger_type = 1
    elif feature == 'urls':
        trigger_type = 1
    elif feature == 'insults':
        trigger_type = 4
    elif feature == 'mention':
        trigger_type = 5
    elif feature == 'spam':
        trigger_type = 3
        
    if trigger_type:
        url = f"https://discord.com/api/v10/guilds/{guild_id}/auto-moderation/rules"
        headers = {
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json"
        }

        trigger_metadata = {
            "presets": [1, 2, 3]
        }

        if feature == 'urls':
            trigger_metadata["keyword_filter"] = ["*www*", "*https://*"]
            
        if feature == 'invites':
            trigger_metadata["keyword_filter"] = ["*discord.gg*"]


        if trigger_type == 1:
            data = {
                "name": f"{feature} rule",
                "creator_id": "1094942437820076083",
                "enabled": value,
                "event_type": 1,
                "trigger_type": trigger_type,
                "trigger_metadata": trigger_metadata,
                "actions": [
                    {
                        "type": 1,
                        "metadata": {
                            "channel_id": channel_id,
                            "duration_seconds": 10,
                            "custom_message": "action taken by use",
                        },
                    },
                    {
                        "type": 2,
                        "metadata": {
                            "channel_id": channel_id,
                            "reason": "action taken by use"
                        }
                    },
                    {
                        "type": 3,
                        "metadata": { 
                            "duration_seconds": 60 
                        }
                    }
                ],
            }
        else:
            data = {
            "name": f"{feature} rule",
            "creator_id": "1094942437820076083",
            "enabled": value,
            "event_type": 1,
            "trigger_type": trigger_type,
            "trigger_metadata": trigger_metadata,
            "actions": [
                {
                    "type": 1,
                    "metadata": {
                        "channel_id": channel_id,
                        "duration_seconds": 10,
                        "custom_message": "action taken by use",
                    },
                },
                {
                    "type": 2,
                    "metadata": {
                        "channel_id": channel_id,
                        "reason": "action taken by use"
                    }
                },
            ],
        }

        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=json.dumps(data)) as response:
                if response.status == 201 or response.status == 200:
                    print(f"{feature} rule created")
                else:
                    print(f"Error creating {feature} rule: {response.status} {await response.text()}")

class Automod(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot


    @commands.hybrid_command(name='automod')
    async def setupautomod(self, ctx, feature: str = None, value: bool = None, channelid: discord.TextChannel = None):
        if not ctx.author.guild_permissions.manage_guild:
            return await noperms(self, ctx, "manage_guild")
        if feature is None or value is None or channelid is None:
            await ctx.send(embed=discord.Embed(title="Error", description="Invalid feature name. Use invites, urls, insults , mention, spam\nExample: automod invites true/false #logs", color=Colors.default))
            return
        
        await create_automod_rule(self.bot.http.token, ctx.guild.id, feature, value, channelid.id)
        await ctx.send(embed=discord.Embed(title="Configuration", description=f": {feature}\n: {channelid.mention}\n: {value}", color=Colors.default))


async def setup(bot):
    await bot.add_cog(Automod(bot))             
