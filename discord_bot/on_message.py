import discord 
from   discord.ext import commands
import asyncio

# list of commands for our bot
help = '''
    These are my commands: 
    m.q    - add song to queue
    m.pl   - play a playlist from user(current user is the admin of server)
    m.n    - play next song
    m.stop - stop streaming

    Also I need to be in a voice channel in order to work, so just connect to one before trying my music related commands.
    '''

# listen for messages from users
def on_message(client):
    # commands to do on certain receives messages
    @client.event
    async def on_message(message):
        # ignore our own bot's chat
        if message.author == client.user: return 

        # command to se our bot help guide
        if message.content.startswith("m.help"): await message.channel.send(help)

        # in order to play music check if the bot is connected to a voice channel
        # otherwise music related commands are redundant
        if client.voice_clients: