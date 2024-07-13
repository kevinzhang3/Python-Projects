import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

# this cog class will be assigned to the bot and will serve as the functionality/implementation of searching and playing music
class music_cog(commands.cog):
    def __init__(self, bot):
        self.bot = bot