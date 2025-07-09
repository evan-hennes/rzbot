import discord
import asyncio
from discord import app_commands
from discord.ext import commands

# function definitions for moderation commands
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