# bot.py
import os
import random

import logging
import sys
import datetime
import asyncio
import csv


from const import *
from db_cmds import *
from parser import *

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents().all()
# intents.members = True
# intents.voice_states = True

client = discord.Client(intents = intents)



receipt_message = None
receipt_image = None

async def check_birthdays():
    #check to see if the hour is correct
    now = datetime.datetime.now()
    if(now.hour != 1):
        return

    #check to see if there is a general channel to post  
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    channel = discord.utils.get(guild.text_channels, name="general")  #TODO configurable default channel to post
    if(not channel):
        print("No general channel found")
        return

    print("checking bdays")
    birthdays = fetch_table_response('birthday', generic_types,'%02d-%02d' % (dt.month,dt.day))
    if(birthdays != None):
        for birthday in birthdays:
            print(birthday)
            await channel.send(birthday_response % birthday)
    
    return

async def check_reminders():
    remindme_list = []
    # found_reminder_list = []
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    channel = discord.utils.get(guild.text_channels, name="general")  #TODO configurable default channel to post
    if(not channel):
        print("No general channel found")
        return

    with open(REMINDME_CSV,'r') as b:
        remindme = csv.reader(b)
        remindme_list.extend(remindme)
    
    
    for entry in remindme_list:
        entry[1] = int(entry[1]) - 60
        if(entry[1] <= 0):
            await channel.send(REMINDME_MESSAGE % (entry[0],entry[2]))
            remindme_list.remove(entry)

    if(len(remindme_list) == 0):
        with open(REMINDME_CSV,'w+') as b:
            return
    
    
    with open(REMINDME_CSV,'w') as b:
        writer = csv.writer(b)
        for entry in remindme_list:
            writer.writerow(entry)




async def check_minute():
    while True:
        await check_reminders()
        await asyncio.sleep(60)

# does hourly routine check
async def check_hour():
    while True:
        await check_birthdays()
        await asyncio.sleep(3600)

# 
    
# Run startup commands
@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    await client.change_presence(activity=discord.Game(name=status))
    client.loop.create_task(check_hour())
    client.loop.create_task(check_minute())


@client.event
async def on_message(message):
    if message.author == client.user:
        return


    if message.content == ';;help':
        response = help_response
        await message.channel.send(response)
        return

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
        return
    

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

    if message.content.startswith(';;receipt'):
        # print(receipt_message)
        global receipt_image
        global receipt_message
        if(receipt_message == None):
            await message.add_reaction('❌')
            return
        await message.channel.send(receipt_message)
        if(receipt_image != None):
            await message.channel.send(file=receipt_image)
            await asyncio.sleep(5)
        receipt_image = None
        receipt_message = None
        return

    if message.content.startswith(';;remindme'):
        # date = find_date(message.content)
        time = find_time(message.content)
        
        remind_message = ''
        if(time == 0):
            date =  list(datefinder.find_dates(message.content))
            now = datetime.datetime.now()
            try:
                time = (date[0]-now).total_seconds()
            except:
                await message.add_reaction('❌')
                return
        
        if(time <= 0):
            await message.add_reaction('❌')
            return
        try:
            remind_message = message.content.split('"')[1::2][0]
        except:
            await message.add_reaction('❌')
            return
        try:
            test = int(time) - 60
        except:
            await message.add_reaction('❌')
            return
        id_request = find_id(message.content)
        if(id_request == None):
            id_request = message.author.id
        entry = [str(id_request),int(time),str(remind_message)]
        with open(REMINDME_CSV,'a') as b:
            writer = csv.writer(b)
            writer.writerow(entry)
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
    
    if message.content.startswith(';;'):
        await message.channel.send(error_response)
        return




@client.event
async def on_message_delete(message):
    if message.author.bot:
        print('bot message deleted')
        return
    global receipt_message
    global receipt_image
    receipt_message = receipt_message_response % (message.author.id,message.content)
    print(receipt_message)
    for attachment in message.attachments:
        if any(attachment.filename.lower().endswith(image) for image in image_types):
            receipt_image = await attachment.to_file()
            return
    return

@client.event 
async def on_message_edit(before, after):
    global receipt_message
    receipt_message = receipt_message_response % (before.author.id,before.content)
    print(receipt_message)
    return


@client.event
async def on_voice_state_update(member, before, after):
    if(member.id == 251275244528992256 and after.channel != None):
        vc = await after.channel.connect()
        vc.play(discord.FFmpegPCMAudio("Recording.mp3"))
        await asyncio.sleep(10)
        await vc.disconnect()
    return

@client.event
async def on_user_update(before,after):
    if(before.avatar != after.avatar):
        guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
        channel = discord.utils.get(guild.text_channels, name="general")  #TODO configurable default channel to post
        if(not channel):
            print("No general channel found")
            return
        await channel.send(PROFILE_UPDATE % after.id)
    return

@client.event
async def on_member_update(before,after):
    # print(after.activities)
    for after_activity in after.activities:
        if after_activity.name == 'Counter-Strike: Global Offensive':
            for before_activity in before.activities:
                if before_activity.name == 'Counter-Strike: Global Offensive':
                    return
        
            guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
            channel = discord.utils.get(guild.text_channels, name="general")  #TODO configurable default channel to post
            if(not channel):
                print("No general channel found")
                return
            await channel.send("cs? <@249349397396062209> <@186009915582578688> <@157676060564127744> <@307580925506486273> <@227973840733470721>")    
    return

client.run(TOKEN)
