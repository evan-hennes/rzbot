import discord
import asyncio
from discord import app_commands
from discord.ext import commands
from datetime import timedelta

# bot token goes here - make sure to remove before pushing to github
tok = ''

# warns dict - contains user ID's + their respective warns
warns = {}

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

@app_commands.command(name='warn', description='Warns a user for acting a fool')
async def warn_user(interaction):
    print('placeholder')
# end def warn_user

@app_commands.command(name='removewarn', description='Removes warning from a user')
async def removewarn_user(interaction):
    print('placeholder')
# end def removewarn_user

@app_commands.command(name='timeout', description='Times out a user for really acting a fool')
async def timeout_user(interaction):
    print('placeholder')
# end def timeout_user

@app_commands.command(name='removetimeout', description='Removes timeout from a user')
async def removetimeout_user(interaction):
    print('placeholder')
# end def removetimeout_user

@app_commands.command(name='ban', description='Bans a user for REALLY acting a fool')
async def ban_user(interaction):
    print('placeholder')
# end def ban_user

@app_commands.command(name='unban', description='Unbans a user')
async def unban_user(interaction):
    print('placeholder')
# end def unban_user

# bot functions
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    # register tree commands for sandbox
    sandbox = discord.Object(id = 1238267373908262982)
    bot.tree.copy_global_to(guild=sandbox)
    await bot.tree.sync(guild=sandbox)
    # register commands for official server - not yet needed
    # rzcord = discord.Object(id = 1108548717054808136)
    # bot.tree.copy_global_to(guild=rzcord)
    # await bot.tree.sync(guild=rzcord)
    print('Running')
# end def on_ready()

@bot.event
async def on_message(message):
    if 'bald' in message.content:
        try:
            await message.channel.send(f'sandman...')
        except Exception as e:
            await message.channel.send(f'Exception : {e}')
        # end try/except block
    # end if statement
    await bot.process_commands(message)
# end def on_message

if __name__ == '__main__':
    try:
        bot.run(tok)
    except KeyboardInterrupt:
        asyncio.get_event_loop().close()
    except Exception as e:
        print(f'failed to run : {e}')
    # end try/except block
# end main program area