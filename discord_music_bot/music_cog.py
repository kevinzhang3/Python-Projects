import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

# this cog class will be assigned to the bot and will serve as the functionality/implementation of searching and playing music
class music_cog(commands.Cog):
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

    async def start(self, ctx):
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
                    await ctx.send("Could not connect to the voice channel.")
                    return
            # move from one vc to another
            else:
                await self.vc.move_to(self.queue[0][1])

            # dequeue and play song
            self.queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda x: self.skip())

        else:
            self.playing = False

    # command for user to play music using the bot, can also be called with 'p'
    @commands.command(name='play', aliases=['p'], help='Play song from YouTube.')
    async def play(self, ctx, *args):
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("User must connect to a voice channel.")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Incorrect format. Try again.")
            else:
                await ctx.send("Song added to queue")
                self.queue.append([song, voice_channel])

                if self.playing == False:
                    await self.start(ctx) 

    # pause command for user to pause music output, or resume if paused
    @commands.command(name='pause', help='Pauses the current song, or resumes a paused song.')
    async def pause(self, ctx, *args):
        if self.playing:
            self.playing = False
            self.paused = True
            self.vc.pause()
        elif self.paused:
            self.playing = True
            self.paused = False
            self.vc.resume()

    # resumes current song
    @commands.command(name='resume', aliases=['r'], help='Resumes output of the current song.')
    async def resume(self, ctx, *args):
        if self.paused:
            self.playing = True
            self.paused = False
            self.vc.resume()

    # skips to the next song in queue
    @commands.command(name='skip', aliases=['s'], help='Skip to the next song in queue.')
    async def skip(self, ctx, *args):
        if self.vc != None and self.vc:
            self.vc.stop()
            await self.start(ctx)
    
    # displays the state of the queue
    @commands.command(name='queue', aliases=['q'], help='Displays all songs in the queue.')
    async def queue(self, ctx):
        output = ""

        # will only print 4
        for i in range(0, len(self.queue)):
            if i > 4:
                break
            output += self.queue[i][0]['title'] + '\n'  
        
        if output != "":
            await ctx.send(output)
        else:
            await ctx.send("The queue is empty.")
    
    # clears the queue
    @commands.command(name='clear', aliases=['c'], help='Clears all songs from queue.')
    async def clear(self, ctx, *args):
        if self.vc != None and self.playing:
            self.vc.stop()
        self.queue.clear()
        await ctx.send("Queue has been cleared.")

    # force the bot to leave the current vc
    @commands.command(name='leave', aliases=['l', 'disconnect'], help='Forces bot out of current voice channel.')
    async def leave(self, ctx):
        self.playing = False
        self.paused = False
        await self.vc.disconnect()