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
        self.text_channel = []