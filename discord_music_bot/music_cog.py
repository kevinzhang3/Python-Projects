import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

# this cog class will be assigned to the bot and will serve as the functionality/implementation of searching and playing music
class music_cog(commands.cog):
    def __init__(self, bot):
        self.bot = bot

        self.playing = False
        self.paused = False

        # music queue
        self.queue = []

        # best audio quality, and no playlists (does not work with bot)
        self.YDL_OPTS = {'format': 'bestaudio', 'noplaylist': 'True'}

        # only deal with audio
        self.FFMPEG_OPTIONS = {'options': '-vn'}

        self.vc = None

    def search(self, item):
        with YoutubeDL(self.YDL_OPTS) as ydl:
            try:
                vid = ydl.extract_info(f"ytsearch:{item}", download=False)['entries'][0]
            except Exception:
                return False
            return {'source': vid['formats'][0]['url'], 'title': vid['title']}
        
    def skip(self):
        # base case to stop recursion
        if len(self.queue > 0):
            self.playing = True

            # the url of the song to by played taken from the first element of the queue
            m_url = self.queue[0][0]['source']

            # dequeue the song
            self.queue.pop(0)

            # play the song in vc using FFmpeg and the options defined, after the song finishes playing, call play_next again recursively
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda x: self.skip())
        else:
            self.playing = False

    async def start(self, msg):
        # check for songs
        if len(self.queue) > 0:

            self.playing = True
            m_url = self.queue[0][0]['source']

            # check if bot is currently in vc
            if self.vc == None or not self.vc.is_connected():
                # attempt to join vc
                self.vc = await self.queue[0][1].connect()

                # send error message if failed to join vc
                if self.vc == None:
                    await msg.send("Could not connect to the voice channel.")
                    return
            # move from one vc to another
            else:
                await self.vc.move_to(self.queue[0][1])

            # dequeue and play song
            self.queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda x: self.skip())

        else:
            self.playing = False

    @commands.command(name='play', aliases=["p"], help='Play song from YouTube.')
    async def play(self, msg, *args):
        query = " ".join(args)