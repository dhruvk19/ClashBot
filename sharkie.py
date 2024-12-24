import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

version = 'v1.1'

load_dotenv('.env')
TOKEN = os.getenv('DISCORD_TOKEN')
CLASH_TOKEN = os.getenv('CLASH_TOKEN')
headers = {
    'authorization': f'Bearer {CLASH_TOKEN}'
}

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)
   


@bot.event
async def on_ready():
    activity = discord.Activity(name='the live replays', type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)
    print('We have logged in as {0.user}'.format(bot))

    # admin commands that help with managment of the server
    await bot.load_extension("admin_commands")
    print('Admin commands loaded')

    await bot.load_extension("clash_admin_commands")
    print('Clash admin commands loaded')

    

if __name__ == "__main__":
    bot.run(TOKEN)
    