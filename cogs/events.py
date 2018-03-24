import discord
from discord.ext import commands

class Events:

    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        "This event displays message when logged in as bot and change the status of bot"

        print("Logged in as {}".format(self.bot.user.name))
        print("with id {}".format(self.bot.user.id))
        print("------------")
        await self.bot.change_presence(game=discord.Game(name=' with your mom', url="https://www.twitch.tv/mailadmin", type=1))

    
    async def on_message(self,message):
        "Greet user with 'Hello!' when they type 'hello' in channel bot is allowed to send message"

        if message.content.startswith('hello'): #or message.content.startswith('Hello'): 
            channel = message.channel
            user_id = str(message.author.id)
            await channel.send('Hello Ningen!  {mention}'.format(mention='<@'+user_id+'>'))



def setup(bot):
    bot.add_cog(Events(bot))
