# Music_discord_bot
A bot that will be able to play audio on discord.

## How it works

The bot is made using the discord.Client from the discord library. 

It waits for messages and treats those with the m. prefix as commands, does not actually use the @command from the discord.Bot. Used the Client instead of the Bot because I wanted to make something familiar and very fast.

The bot automatically connects to the user's voice channel(currently made only for a specific channel, the channel id being the identificator in this case, this is so it only connects to my channel called music, personal preferrence and can be easily changed).

The bot listens for the m.p <item> command, searches for the items on youtube and plays the first result using the youtube_dl library.
  
The bot uses a config.py file where it stores the discord TOKEN.
