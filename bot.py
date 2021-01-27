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


async def check_birthdays():
    #check to see if there is a general channel to post  
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    channel = discord.utils.get(guild.text_channels, name="general")  #TODO configurable default channel to post
    if(not channel):
        print("No general channel found")
        return

    while True:
        print("checking bdays")
        birthdays = fetch_table('birthdays', bday_types,None,scan=1)
        if(birthdays != None):
            for birthday in birthdays:
                print(birthday)
                await channel.send(birthday_response % birthday)
        #come back 24 hours to check for bday again        
        await asyncio.sleep(86400)
    
# Run startup commands
@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    await client.change_presence(activity=discord.Game(name=status))
    client.loop.create_task(check_birthdays())


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!c help':
        response = help_response
        await message.channel.send(response)
    
    if message.content.startswith('!c add birthday'): 
        id_request = find_id(message.content)
        birthday_entry = find_date(message.content)

        if(birthday_entry == None): #invalid date, send error emoji and return
            await message.add_reaction('❌')
            return

        if(id_request == None): #if no user mentioned assume author id
            id_request = message.author.id

        # currently having issues with using whole dates, splitting into month, day, year circumvents the error
        day = birthday_entry[8:10]
        month = birthday_entry[5:7]
        year = birthday_entry[0:4]

        response = birthday_add_response % int(id_request)
        if(create_db_table('birthdays', bday_entries)): # create bday table if not created yet, return error if cannot create table
            await message.add_reaction('❌')
            return
        if(addto_table('birthdays', bday_types,('%d,%d,%d,%d' % (int(id_request),int(year),int(month),int(day))))): #insert bday and user id into bday table
            await message.add_reaction('❌')
            return
        
        await message.add_reaction('✅')
        return
    
    # check census database
    if message.content.startswith('!c check birthday'):
        id_request = find_id(message.content)
        if(id_request == None):
            id_request = message.author.id
       
        row = fetch_table('birthdays', bday_types,id_request)
        if(not row):
            await message.add_reaction('❌')
            return

        response = birthday_check_response % ((row[0]))
        await message.channel.send(response)
    
    # remove census database
    if message.content.startswith('!c remove birthday'):
        if(removefrom_table('birthdays',message.author.id)):
            await message.add_reaction('❌')
            return
        
        await message.add_reaction('✅')
        return





client.run(TOKEN)
