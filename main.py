import discord
import asyncio
from discord import app_commands
from discord.ext import commands
from moderation import checkwarns_user, settroublemaker_user, removetroublemaker_user, warn_user, removewarn_user, clearwarns_user, nukewarns, timeout_user, removetimeout_user, ban_user, unban_user

# bot token goes here - make sure to remove before pushing to github
tok = ''

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
    bot.tree.clear_commands(guild=discord.Object(id=1238267373908262982))
    print(f'Logged in as {bot.user}')
    bot.tree.add_command(ping_bot)
    bot.tree.add_command(settroublemaker_user)
    bot.tree.add_command(removetroublemaker_user)
    bot.tree.add_command(checkwarns_user)
    bot.tree.add_command(warn_user)
    bot.tree.add_command(removewarn_user)
    bot.tree.add_command(clearwarns_user)
    bot.tree.add_command(nukewarns)
    bot.tree.add_command(timeout_user)
    bot.tree.add_command(removetimeout_user)
    bot.tree.add_command(ban_user)
    bot.tree.add_command(unban_user)
    await bot.tree.sync(guild=discord.Object(id=1238267373908262982))
    await bot.tree.sync()
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

# main program area
if __name__ == '__main__':
    try:
        bot.run(tok)
    except KeyboardInterrupt:
        asyncio.get_event_loop().close()
    except Exception as e:
        print(f'failed to run : {e}')
    # end try/except block
# end main program area