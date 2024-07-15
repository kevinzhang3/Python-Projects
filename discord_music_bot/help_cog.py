import discord 
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.help_msg = """
```
Commands:
m.help - displays all commands
m.p <song> searches for the given song in youtube and plays it in the channel you are currently in.
```

"""