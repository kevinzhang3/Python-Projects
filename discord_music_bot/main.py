import discord
from discord.ext import commands
import os

from help_cog import help_cog
from music_cog import music_cog

# makes it so all commands must be prefixed with "m."
bot = commands.Bot(command_prefix="m.")

bot.add_cog(music_cog)
bot.add_cog(help_cog)

bot.run(os.getenv("token"))