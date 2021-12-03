import discord 
from   discord.ext import commands
import asyncio

# list of commands for our bot
help = '''
    These are my commands: 
    spot.q    - add song to queue
    spot.pl   - play a playlist from user(current user is the admin of server)
    spot.n    - play next song
    spot.stop - stop streaming
    '''

# listen for messages from users
def on_message(client):
    # commands to do on certain receives messages
    @client.event
    async def on_message(message):
        # ignore our own bot's chat
        if message.author == client.user: return 

        # ping command for testing if bot is alive
        if message.content.startswith("pork"): await message.channel.send("pig")

        # command to se our bot help guide
        if message.content.startswith("spot.help"): await message.channel.send(help)