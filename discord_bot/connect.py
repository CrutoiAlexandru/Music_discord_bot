import discord
import config as config
import discord_bot.on_message as on_message
import discord_bot.on_voice_state_change as on_voice_state_change

# start connection to our discord server
def connect():
    # create a new discord client
    client = discord.Client()

    # print logged in when bot is ready for use
    @client.event
    async def on_ready():
        print("Logged in")

    # listen for voice state updates of the users and connect to their voice channel
    on_voice_state_change.voice_channel_connect(client)
    
    # listen for messages from users
    on_message.on_message(client)

    # run our new client with our private token
    client.run(config.TOKEN)