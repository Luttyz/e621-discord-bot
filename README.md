# e621 discord bot
A simple discord bot made in python for viewing e621 posts and pools, made by @dox-net, with extra QOL improvements added by Luttyz.
# Commands
./femboy - Command made using the reddit api to grab a random image from r/femboy<br>
./e621 or ./e926 - search for posts on e621, use tags within command<br>
./e621pool or ./e926pool - with a pool id look through a pool on e621<br><br>
./e621, ./e926 and their pool counterparts can all be shortened to ./e6 and ./e9<br><br>
Note: because discord.py doesn't support embedding videos, WebM posts are disabled by default, you can change this behavior by adding `+webm` to your message.

# Video example
###### e621/e926 command<br>
https://user-images.githubusercontent.com/109423445/187699711-5daa73b9-e33a-4f90-8ba0-fd29afa0329e.mp4

# Running
Depending on if you have already ran a Discord bot before, you might want to install <a href="https://github.com/Luttyz/e621-discord-bot/blob/main/requirements.txt">the dependencies</a> by doing `pip install requirements.txt`.<br>

Running the bot is as simple as adding your bot's token at the end of the bot.py file and doing `python3 bot.py`, although only Python 3.9 and higher seems to be supported.<br>

You can invite this bot to your server <a href="https://discord.com/oauth2/authorize/?permissions=387136&scope=bot&client_id=989510170839236628">here</a>. Do note that it will not check for if the channel is NSFW or not, this feature has been removed due to the main use case of this instance. The bot also currently requests Discord for all special intents whereas it only needs to read message, this might be fixed later if I get around to it.
