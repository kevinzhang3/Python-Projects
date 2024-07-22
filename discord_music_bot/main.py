import discord
from discord.ext import commands
import os, asyncio

# import cogs
from help_cog import help_cog
from music_cog import music_cog

i = discord.Intents.all()

# makes it so all commands must be prefixed with "m."
bot = commands.Bot(command_prefix="m.", intents=i)

bot.remove_command("help")

bot.add_cog(music_cog)
bot.add_cog(help_cog)

bot.run(os.getenv("token"))