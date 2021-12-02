import discord 
from discord.ext import commands
import filelist.wishlist as wishlist
import threading
import asyncio

# list of commands for our bot
help = '''
    These are my commands: 
    ping    - let's play
    fl.wl   - add a torrent to wishlist
    fl.rm   - remove a torrent from the wishlist
    fl.show - show the wishlist items
    '''

# listen for messages from users
def on_message(client):
    # commands to do on certain receives messages
    @client.event
    async def on_message(message):
        # ignore our own bot's chat
        if message.author == client.user: return 

        # ping command for testing if bot is alive
        if message.content.startswith("ping"): await message.channel.send("pong")

        # command to se our bot help guide
        if message.content.startswith("fl.help"): await message.channel.send(help)

        # wishlist command
        # add to our wishlist list(wishlist) of torrents
        if message.content.startswith("fl.wl"): 
            # isolate only the torrent to be added
            torrent = message.content.replace("fl.wl", "")
            torrent = torrent.replace(" ", "")

            wishlist.wishlist(torrent)

            # send a message to confirm the torrent name
            await message.channel.send("Added to wishlist: " + torrent)

        # remove command
        # remove from our wishlist list(wishlist) of torrents
        if message.content.startswith("fl.rm"): 
            # isolate only the torrent to be added
            torrent = message.content.replace("fl.rm", "")
            torrent = torrent.replace(" ", "")

            wishlist.remove(torrent)

            # send a message to confirm the torrent name
            await message.channel.send("Removed from wishlist: " + torrent)

        # show command
        # show our wishlist items
        if message.content.startswith("fl.show"): 
            # send a message to show wishlist
            await message.channel.send("This is your wishlist:\n" + wishlist.show())

        # run our data feed non-stop 
        # but only after the first chat message
        async def background_torrents_run(message):
            # call the run function
            await client.wait_until_ready()
            
            while not client.is_closed():
                await asyncio.sleep(25)
                await wishlist.run(message)

        client.loop.create_task(background_torrents_run(message))