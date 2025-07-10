import discord
import asyncio
import sqlite3
from discord import app_commands
from discord.ext import commands
from datetime import timedelta

# connect to DB for moderation actions
con = sqlite3.connect('acts.db')
cur = con.cursor()

# create warns table
cur.execute('CREATE TABLE IF NOT EXISTS warns(' \
    'wid INTEGER PRIMARY KEY AUTOINCREMENT, ' \
    'uid INTEGER, ' \
    'date DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP), ' \
    'reason TEXT)'
)

# function definitions for moderation commands
@app_commands.command(name='checkwarns', description='Pulls a user\'s warn history')
async def checkwarns_user(interaction : discord.Interaction, user : discord.Member):
    uid = user.id
    res = cur.execute(f'SELECT * FROM warns WHERE uid = {uid}')
    res = res.fetchall()
    if len(res) == 0: 
        await interaction.response.send_message(f'User {user.mention} has no warns.')
    else:
        warns = f'# Warn Log for {user.mention}\n'
        for warn in res: warns += f'> **Warn ID** : {warn[0]}\n> **Date** : {warn[2]}\n> **Reason** : {warn[3]}\n'
        await interaction.response.send_message(warns)
    # end if/else block
# end def checkwarns_user

@app_commands.command(name='warn', description='Warns a user for acting a fool')
async def warn_user(interaction : discord.Interaction, user : discord.Member, rsn : str = 'None'):
    uid = user.id
    cur.execute('INSERT INTO WARNS (uid, reason) VALUES (?, ?)', (uid, rsn))
    con.commit()
    await interaction.response.send_message(f'{user.mention} warned with reason: **{rsn}**')
# end def warn_user

@app_commands.command(name='removewarn', description='Removes warning from a user')
async def removewarn_user(interaction : discord.Interaction, wid : int):
    cur.execute(f'DELETE FROM warns WHERE wid = {wid}')
    con.commit()
    await interaction.response.send_message(f'Warn **{wid}** successfully deleted.')
# end def removewarn_user

@app_commands.command(name='timeout', description='Times out a user for really acting a fool')
async def timeout_user(interaction : discord.Interaction, user : discord.Member, duration : str, rsn : str = 'None'):
    dig = ''
    unit = ''
    for char in duration:
        if char.isnumeric(): dig += char
        elif char.isalpha(): unit += char
        else: continue
    dig = int(dig)
    if unit == 'm' or unit == 'min' or unit == 'mins' or unit == 'minute' or unit == 'minutes':
        end = discord.utils.utcnow() + timedelta(minutes=dig)
        await user.timeout(end, reason=rsn)
        await interaction.response.send_message(f'User {user.mention} timed out for **{dig}** minutes with reason: **{rsn}**.')
    elif unit == 'h' or unit == 'hs' or unit == 'hr' or unit == 'hrs' or unit == 'hour' or unit == 'hours':
        end = discord.utils.utcnow() + timedelta(hours=dig)
        await user.timeout(end, reason=rsn)
        await interaction.response.send_message(f'User {user.mention} timed out for **{dig}** hours with reason: **{rsn}**.')
    elif unit == 'd' or unit == 'ds' or unit == 'day' or unit == 'days':
        end = discord.utils.utcnow() + timedelta(days=dig)
        await user.timeout(end, reason=rsn)
        await interaction.response.send_message(f'User {user.mention} timed out for **{dig}** days with reason: **{rsn}**.')
    elif unit == 'w' or unit == 'ws' or unit == 'wk' or unit == 'wks' or unit == 'week' or unit == 'weeks':
        end = discord.utils.utcnow() + timedelta(weeks=dig)
        await user.timeout(end, reason=rsn)
        await interaction.response.send_message(f'User {user.mention} timed out for **{dig}** weeks with reason: **{rsn}**.')
    else:
        await interaction.response.send_message('Invalid syntax - please try again.')
    # end if/else logic
# end def timeout_user

@app_commands.command(name='removetimeout', description='Removes timeout from a user')
async def removetimeout_user(interaction : discord.Interaction, user : discord.Member, rsn : str = 'None'):
    await user.timeout(None, reason=rsn)
    await interaction.response.send_message(f'User {user.mention} removed from timeout with reason: **{rsn}**.')
# end def removetimeout_user

@app_commands.command(name='ban', description='Bans a user for REALLY acting a fool')
async def ban_user(interaction : discord.Interaction, user : discord.Member, rsn : str = 'None'):
    await user.ban(reason=rsn)
    await interaction.response.send_message(f'User **{user.name}** has been banned with reason: **{rsn}**.')
# end def ban_user

@app_commands.command(name='unban', description='Unbans a user')
async def unban_user(interaction : discord.Interaction, user : discord.User, rsn : str = 'None'):
    await interaction.guild.unban(user, reason=rsn)
    await interaction.response.send_message(f'User **{user.name}** has been unbanned with reason: **{rsn}**.')
# end def unban_user