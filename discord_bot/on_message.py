import discord 
from   discord.ext import commands
import asyncio
import youtube_dl

# list of commands for our bot
help = '''
    These are my commands: 
    m.p - play an audio or add it to queue
    m.c - clear the queue
    m.n - play next audio
    m.s - stop streaming
    m.q - display current queue

    Also I need to be in a voice channel in order to work, so just connect to one before trying my music related commands.
    '''
audio_queue = list()

# listen for messages from users
def on_message(client):
    # commands to do on certain receives messages
    @client.event
    async def on_message(message):
        # get the current voice channel
        if client.voice_clients: voice_client = client.voice_clients[0]

        # ignore our own bot's chat
        if message.author == client.user: return 

        # command to see our bot help guide
        if message.content.startswith("m.help"): await message.channel.send(help)

        # command to clear audio queue
        if message.content.startswith("m.c"): 
            audio_queue.clear()
            await message.channel.send("Cleared audio queue!")

        # command to stop audio player
        if message.content.startswith("m.s"): 
            audio_queue.clear()
            # I have no idea why but if I do it twice it works
            client.voice_clients[0].stop()
            client.voice_clients[0].stop()
            await message.channel.send("Stopped audio queue!")

        # command to play next audio in queue
        if message.content.startswith("m.n"):
            if len(audio_queue) == 0:
                audio_queue.clear()
                # I have no idea why but if I do it twice it works
                client.voice_clients[0].stop()
                client.voice_clients[0].stop()
                await message.channel.send("Stopped audio queue!")
            
            client.voice_clients[0].stop()
            # play the next audio in queue
            await playthrough(audio_queue, voice_client, client)
            await message.channel.send("Skipped audio in queue!")

        # command to display current audio queue
        if message.content.startswith("m.q"): 
            if len(audio_queue) == 0:
                await message.channel.send("Queue is empty!") 
                return
            await message.channel.send("Queue is: " + ', '.join(audio_queue))

        # in order to play music check if the bot is connected to a voice channel
        # otherwise music related commands are redundant
        if client.voice_clients:
            if message.content.startswith("m.p"):

                # isolate the name of the audio
                link = message.content.replace("m.p", "")
                # if the name of the audio is empty ignore it
                if len(link) == 0: 
                    await message.channel.send("Please enter a something more!")
                    return
                print("SEARCHING FOR: ", link)
                # notify the user of the added audio in the queue 
                await message.channel.send(f"Added {link} to queue!")

                # add the audio to the end of the list
                audio_queue.append(link)
                print(audio_queue)

                # put the audio in playthrough
                await playthrough(audio_queue, voice_client, client)

# function made for playing the next audio in queue
async def next_playthrough(audio_queue, voice_client, client):    
    # it will try to play the first item in the list
    # before playing it remove it from the list
    # that is why it will start playing the next item
    try:
        audio_queue.pop(0)
        await play_this(audio_queue[0], voice_client)
        return 
    except Exception:
    # if we cannot play the audio it means there is one playing already
    # if so keep checking in 5 seconds to see if we can play audio
        await asyncio.sleep(5)
        await playthrough(audio_queue, voice_client, client)

# function made for playing through the audio_queue
async def playthrough(audio_queue, voice_client, client):    
    # it will try to play the first item in the list
    # after playing it remove it from the list
    # that is why we allways play only the first item in the list
    try:
        await play_this(audio_queue[0], voice_client)
        audio_queue.pop(0)
        return 
    except Exception:
    # if we cannot play the audio it means there is one playing already
    # if so keep checking in 5 seconds to see if we can play audio
        await asyncio.sleep(5)
        await playthrough(audio_queue, voice_client, client)

async def play_this(link, voice_client):
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
                
    # because of default_search set to auto if we provide a name not a link it will automatically search for it on youtube and retrieve the first result on the page
    # usually the first result for music is the most accurate so it should work in most cases !!! but it is not perfect !!!

    YDL_OPTIONS = {
        'format': 'bestaudio/best', 
        'noplaylist':False,
        'default_search': 'auto',
        'continue_dl': True,
    }

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        # extract yt info for certain video
        info = ydl.extract_info(link, download=False)
        # isolate the url element of the info
        I_URL = info['entries'][0]['formats'][0]['url']
        # create audio source from the url
        source = await discord.FFmpegOpusAudio.from_probe(I_URL, **FFMPEG_OPTIONS)
        #play the audio source on discord
        voice_client.play(source)