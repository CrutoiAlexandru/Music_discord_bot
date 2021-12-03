import discord 
from   discord.ext import commands
import asyncio

# connect to the first voice channel the user is connected to
# at the moment it does not update the channel if the user connected to another
def voice_channel_connect(client):
    @client.event
    async def on_voice_state_update(member, before, after):
        # keep track of the user's voice state, if connected True otherwise False
        voice_state = True

        # try to get the user's voice channel
        try:
            voice_cl = member.voice.channel
        except Exception:
            # if we can't get user's voice channel it means he is not connected to a voice channel
            print('user is disconnected from voice')
            voice_state = False

        # try to connect to a voice channel if the user connects
        try:
            await voice_cl.connect()
        # if the client is already connected to a voice channel treat the exception
        except Exception:
            print('client already connected to voice channel')
        
        # try to get the client's voice channel and disconnect from it
        try:    
            voice_disc = client.voice_clients[0]
            
            # if the user is not connected to a voice channel disconnect
            if voice_state == False:    await voice_disc.disconnect()
        # do not disconnect if the user is connected and treat the exception
        except Exception:
            print('user is in channel so we do not disconnect')
            return