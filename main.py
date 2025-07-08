import discord
import asyncio
from discord import app_commands
from discord.ext import commands
from datetime import timedelta

# bot token goes here - make sure to remove before pushing to github
tok = ''

# offenders dict - contains user ID's + their respective warns

# discord intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# setup bot command prefixes
bot = commands.Bot(command_prefix='>', intents=intents)

# define slash commands
@app_commands.command(name='ping', description='Pings Bot to ensure it is working')
async def ping_bot(interaction):
    await interaction.response.send_message(f'Pong!\nLatency: **{bot.latency * 1000}**ms')
    print('bot pinged')
# end def ping_bot

# bot functions
@bot.event
async def on_ready():
    await bot.tree.sync()
    print('Running')
# end def on_ready()

if __name__ == '__main__':
    try:
        bot.run(tok)
    except KeyboardInterrupt:
        asyncio.get_event_loop().close()
    except Exception as e:
        print(f'failed to run : {e}')