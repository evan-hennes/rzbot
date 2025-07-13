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
    'modid INTEGER, ' \
    'date DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP), ' \
    'reason TEXT)'
)

# create troublemakers table
cur.execute('CREATE TABLE IF NOT EXISTS goobers(' \
    'uid INTEGER,' \
    'modid INTEGER)'
)

# function definitions for moderation commands
# ---section 1 - troublemaker related commands---
@app_commands.command(name='settroublemaker', description='Designates a user as a troublemaker - automatically times them out for 24h upon being warned')
async def settroublemaker_user(interaction : discord.Interaction, user : discord.Member):
    try:
        uid = user.id
        modid = interaction.user.id
        if len(cur.execute(f'SELECT * FROM goobers WHERE uid = {uid}').fetchall()) != 0: 
            await interaction.response.send_message(f'User {user.mention} is already designated as a troublemaker.')
        else:
            cur.execute('INSERT INTO goobers (uid, modid) VALUES (?, ?)', (uid,modid))
            con.commit()
            await interaction.response.send_message(f'User {user.mention} designated as a troublemaker.')
    except Exception as e:
        await interaction.response.send_message(f'Error: {e}')
    # end try/except block
# end def settroublemaker_user

@app_commands.command(name='removetroublemaker', description='Removes a user\'s designation as a troublemaker')
async def removetroublemaker_user(interaction : discord.Interaction, user : discord.Member):
    try:
        uid = user.id
        cur.execute(f'DELETE FROM goobers WHERE uid = {uid}')
        con.commit()
        await interaction.response.send_message(f'User {user.mention} is now a good boy.')
    except Exception as e:
        await interaction.response.send_message(f'Error: {e}')
    # end try/except block
# end def removetroublemaker_user

# ---section 2 - warn related commands---
@app_commands.command(name='checkwarns', description='Pulls a user\'s warn history')
async def checkwarns_user(interaction : discord.Interaction, user : discord.Member):
    try:
        uid = user.id
        res = cur.execute(f'SELECT * FROM warns WHERE uid = {uid}')
        res = res.fetchall()
        if len(res) == 0: 
            await interaction.response.send_message(f'User {user.mention} has no warns.')
        else:
            warns = f'# Warn Log for {user.mention}\n'
            # print(res)
            for warn in res: warns += f'> **Warn ID** : {warn[0]}\n> **Issuing Moderator** : <@{warn[2]}>\n> **Date** : {warn[3]}\n> **Reason** : {warn[4]}\n\n'
            await interaction.response.send_message(warns)
        # end if/else block
    except Exception as e:
        await interaction.response.send_message(f'Error: {e}')
    # end try/except block
# end def checkwarns_user

@app_commands.command(name='warn', description='Warns a user for acting a fool')
async def warn_user(interaction : discord.Interaction, user : discord.Member, rsn : str = 'None'):
    try:
        # print(interaction.user.name)
        uid = user.id
        cur.execute('INSERT INTO warns (uid, modid, reason) VALUES (?, ?, ?)', (uid, interaction.user.id, rsn))
        con.commit()
        await interaction.response.send_message(f'{user.mention} warned with reason: **{rsn}**')
        # log warning in designated channel
        channel = interaction.client.get_channel(1393422647257206804)
        date = cur.execute(f'SELECT * FROM warns WHERE wid = {cur.lastrowid}')
        date = date.fetchall()
        # print(date)
        await channel.send(f'> **Warn ID** : {cur.lastrowid}\n> **Issuing Moderator** : {interaction.user.mention}\n> **User** : {user.mention}\n> **Date** : {date[0][3]}\n> **Reason** : {rsn}')
        goober = cur.execute(f'SELECT * FROM goobers WHERE uid = {uid}')
        goober = goober.fetchall()
        if len(goober) > 0: await user.timeout(discord.utils.utcnow() + timedelta(days=1), reason='Automatic timeout - user is designated as a troublemaker.')
    except Exception as e:
        await interaction.response.send_message(f'Error: {e}')
    # end try/except block
# end def warn_user

@app_commands.command(name='removewarn', description='Removes warning from a user')
async def removewarn_user(interaction : discord.Interaction, wid : int):
    try:
        cur.execute(f'DELETE FROM warns WHERE wid = {wid}')
        con.commit()
        await interaction.response.send_message(f'Warn **{wid}** successfully deleted.')
    except Exception as e:
        await interaction.response.send_message(f'Error: {e}')
    # end try/except block
# end def removewarn_user

@app_commands.command(name='clearwarns', description='Clears a user\'s warns')
async def clearwarns_user(interaction: discord.Interaction, user : discord.Member):
    try:
        uid = user.id
        cur.execute(f'DELETE FROM warns WHERE uid = {uid}')
        con.commit()
        await interaction.response.send_message(f'Warns cleared for {user.mention}')
    except Exception as e:
        await interaction.response.send_message(f'Error: {e}')
    # end try/except block
# end def clearwarns_user

@app_commands.command(name='nukewarns', description='Clears all warns from the database - do NOT use this unless absolutely necessary')
async def nukewarns(interaction : discord.Interaction):
    try:
        # drop table & recreate it
        cur.execute('DROP TABLE warns')
        cur.execute('CREATE TABLE IF NOT EXISTS warns(' \
            'wid INTEGER PRIMARY KEY AUTOINCREMENT, ' \
            'uid INTEGER, ' \
            'modid INTEGER, ' \
            'date DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP), ' \
            'reason TEXT)'
        )
        con.commit()
        await interaction.response.send_message('All warns removed successfully.')
    except Exception as e:
        await interaction.response.send_message(f'Error: {e}')
    # end try/except block
# end def nukewarns

# ---section 3 - timeout related commands---
@app_commands.command(name='timeout', description='Times out a user for really acting a fool')
async def timeout_user(interaction : discord.Interaction, user : discord.Member, duration : str, rsn : str = 'None'):
    try:
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
    except Exception as e:
        await interaction.response.send_message(f'Error: {e}')
    # end try/except block
# end def timeout_user

@app_commands.command(name='removetimeout', description='Removes timeout from a user')
async def removetimeout_user(interaction : discord.Interaction, user : discord.Member, rsn : str = 'None'):
    try:
        await user.timeout(None, reason=rsn)
        await interaction.response.send_message(f'User {user.mention} removed from timeout with reason: **{rsn}**.')
    except Exception as e:
        await interaction.response.send_message(f'Error: {e}')
    # end try/except block
# end def removetimeout_user

# ---section 4 - ban related commands---
@app_commands.command(name='ban', description='Bans a user for REALLY acting a fool')
async def ban_user(interaction : discord.Interaction, user : discord.Member, rsn : str = 'None'):
    try:
        await user.ban(reason=rsn)
        await interaction.response.send_message(f'User **{user.name}** has been banned with reason: **{rsn}**.')
    except Exception as e:
        await interaction.response.send_message(f'Error: {e}')
    # end try/except block
# end def ban_user

@app_commands.command(name='unban', description='Unbans a user')
async def unban_user(interaction : discord.Interaction, user : discord.User, rsn : str = 'None'):
    try:
        await interaction.guild.unban(user, reason=rsn)
        await interaction.response.send_message(f'User **{user.name}** has been unbanned with reason: **{rsn}**.')
    except Exception as e:
        await interaction.response.send_message(f'Error: {e}')
    # end try/except block
# end def unban_user