# bot.py
import os
import random
import sqlite3
import re
import datefinder
import logging
import sys
import threading
import datetime
import asyncio

from const import *
from db_cmds import *
from parser import *

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

# @tasks.loop(seconds=20)
async def check_birthdays():
    # threading.Timer(20, check_birthdays).start()
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    channel = discord.utils.get(guild.text_channels, name="general")
    if(not channel):
        print("No general channel found")
        return
    while True:
        print("checking bdays")
        birthdays = fetch_table('birthdays', bday_types,None,scan=1)
        for birthday in birthdays:
            print(birthday)
            await channel.send(birthday_response % birthday)
        await asyncio.sleep(86400)
    

@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    client.loop.create_task(check_birthdays())


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'census help':
        response = help_response
        await message.channel.send(response)
    
    if message.content.startswith('census add birthday'): 
        id_request = find_id(message.content)
        birthday_entry = find_date(message.content)

        if(id_request == None or birthday_entry == None):
            await message.add_reaction('❌')
            return

        day = birthday_entry[8:10]
        month = birthday_entry[5:7]
        year = birthday_entry[0:4]

        response = birthday_add_response % int(id_request)
        if(create_db_table('birthdays', bday_entries)):
            await message.add_reaction('❌')
            return
        if(addto_table('birthdays', bday_types,('%d,%d,%d,%d' % (int(id_request),int(year),int(month),int(day))))):
            await message.add_reaction('❌')
            return
        
        await message.add_reaction('✅')
        return
    

    if message.content.startswith('census check birthday'):
        id_request = find_id(message.content)
        if(id_request == None):
            await message.add_reaction('❌')
            return
       
        row = fetch_table('birthdays', bday_types,id_request)
        print(row)
        if(not row):
            await message.add_reaction('❌')
            return

        response = birthday_check_response % ((row[0]))
        await message.channel.send(response)
    
    if message.content.startswith('census remove birthday'):
        if(removefrom_table('birthdays',message.author.id)):
            await message.add_reaction('❌')
            return
        
        await message.add_reaction('✅')
        return





client.run(TOKEN)
