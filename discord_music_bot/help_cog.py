import discord 
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.help_msg = """
```
Commands:
m.help - displays all commands
m.p <song> searches for the given song in youtube and plays it in the channel you are currently
m.q - displays all songs currently in queue
m.skip - skips the current song
m.clear - clears the music queue
m.leave - disconnect muse from the voice channel
m.pause - pause whatever is currently playing
m.resume - resume music
```
"""
        self.text_channel_text = []
 
    # listener for the on_ready command which activates when the bot succesfully connects to discord and can begin functionality (sends help msg in this case)
    @commands.Cog.listener()
    async def on_ready(self):
        # go through all guilds
        for guild in self.bot.guilds:
            # iterate through text channels and append to list
            for channel in guild.text_channels:
                self.text_channel_text.append(channel)
        
        # send help msg to all
        await self.send_to_all(self.help_msg)
    
    async def send_to_all(self, msg):
        for text_channel in self.text_channel_text:
            await text_channel.send(msg)

    @commands.command(name="help", help="Displays all available commands.")
    async def help(self, ctx):
        await ctx.send(self.help_msg)