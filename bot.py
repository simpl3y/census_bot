# bot.py
import os
import random

import logging
import sys
import datetime
import asyncio


from const import *
from db_cmds import *
from parser import *

import discord
from dotenv import load_dotenv

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
chatbot = ChatBot("Census Bot")
trainer = ListTrainer(chatbot)

chatbot_trainer_log = []

async def check_birthdays():
    #check to see if there is a general channel to post  
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    channel = discord.utils.get(guild.text_channels, name="general")  #TODO configurable default channel to post
    if(not channel):
        print("No general channel found")
        return

    if(create_db_table('birthday',generic_entries)):
        print("No Birthday Table")
        return

    while True:
        print("checking bdays")
        dt = datetime.datetime.today()
        birthdays = fetch_table_response('birthday', generic_types,'%02d-%02d' % (dt.month,dt.day))
        if(birthdays != None):
            for birthday in birthdays:
                print(birthday)
                await channel.send(birthday_response % birthday)
        print('come back 24 hours to check for bday again')        
        await asyncio.sleep(86400)

async def bot_trainer():
    while True:
        if(len(chatbot_trainer_log)):
            trainer.train(chatbot_trainer_log)
        chatbot_trainer_log.clear()
        print("Cleared bot logs")
        await asyncio.sleep(60)

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
    client.loop.create_task(bot_trainer())

@client.event
async def on_message(message):
    if message.author == client.user:
        return


    if message.content == ';;help':
        response = help_response
        await message.channel.send(response)

    # create new table
    if message.content.startswith(';;new'):
        word_split = message.content.split()
        if(create_db_table(word_split[1].lower(),generic_entries)):
            await message.add_reaction('❌')
            return

        print("Created table %s" % word_split[1].lower())
        await message.add_reaction('✅')
        response = question_created_response % (len(list_tables()) - 1)
        await message.channel.send(response)
    

    if message.content.startswith(';;list'):
        tables = list_tables()
        if(not tables):
            await message.add_reaction('❌')
            return
        
        response = list_response + ', '.join(tables)
        await message.channel.send(response)
        return


    # check specified entry
    if(message.content.startswith(';;check')):
        word_split = message.content.split()
        id_request = find_id(message.content)
        if(id_request == None):
            id_request = message.author.id

        entry = fetch_table(word_split[1], generic_types,id_request)
        if(not entry):
            await message.add_reaction('❌')
            return

        if(word_split[1] == 'birthday'):
            response = birthday_check_response % (entry)
        else:
            tables = list_tables()
            num = tables.index(word_split[1])
            response = generic_check_response % (num,entry,interesting_response_list[random.randint(0,3)])
        await message.channel.send(response)
        return

    # manual add to a table
    if(message.content.startswith(';;add')):
        word_split = message.content.split()
        id_request = find_id(message.content)
        if(id_request == None):
            id_request = message.author.id

        if(word_split[1] == 'birthday'):
            entry = find_date(message.content)
            if(entry == None):
                await message.add_reaction('❌')
                return
        else:
            index = message.content.find(word_split[1]) + len(word_split[1])
            entry = ' '.join(message.content[index:].split())
            entry = entry.replace('\'','\'\'')
            entry = entry.replace('<@!%s> ' % id_request,'')
        print (entry)
        if(addto_table(word_split[1].lower(), generic_types,'%d,\'%s\'' % (int(id_request),entry))):
            await message.add_reaction('❌')
            return

        await message.add_reaction('✅')
        return
    
    # remove census answer
    if message.content.startswith(';;remove'):
        word_split = message.content.split()
        if(removefrom_table(word_split[1],message.author.id)):
            await message.add_reaction('❌')
            return
        
        await message.add_reaction('✅')
        return

    if(message.channel.name == 'census'):
        answer = find_census_answer(message.content)
        if(answer == None):
            return
        tables = list_tables()
        if(int(answer[0]) >= len(tables)):
            return
        if(addto_table(tables[answer[0]], generic_types,'%d,\'%s\'' % (message.author.id,' '.join(answer[1].split())))):
            return

        await message.add_reaction('✅')
        return

    
    if client.user.mentioned_in(message):
        try:
            await message.channel.send(chatbot.get_response(message.content.split(' ', 1)[1]))
        except:
            await message.add_reaction('❌')

    if(message.channel.name == 'general'): #collect chat logs for training
        if(find_id(message.content)):
            return
        if(len(message.content) == 0):
            return
        chatbot_trainer_log.append(message.content)




client.run(TOKEN)
