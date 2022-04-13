import discord
from datetime import datetime
from discord.ext import tasks, commands
import random
import asyncio
import sys
import json
import os
import logging
import tracemalloc
import error_code, self_test

check_config = os.path.isfile('config.json')
if check_config == False:
    print('load config file --- fail')
    self_test.error()
else:
    print('load config file --- ok')
    import lang

check_lang = os.path.isdir('lang/')
if check_lang == False:
    print('load lang folder --- fail')
    self_test.error()
else:
    print('load lang folder --- ok')

with open('config.json', "r", encoding = "utf8") as file:
    data = json.load(file)

self_test.check(data)
Lang = lang.lang_chose(data['language'])

if data['debug-mode'] == 'true':
    FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    logging.basicConfig(level=logging.NOTSET, filename='BotLog.log', filemode='w', format=FORMAT)
    print(Lang['debug-enabled'])
else:
    print(Lang['debug-disabled'])

now = datetime.now()
date_time = '<'+now.strftime("%Y-%m-%d, %H:%M:%S")+'>'
prefix = data['command-prefix']
client = discord.Client()
intents = discord.Intents.all()

tracemalloc.start()

@client.event
async def on_ready():
    print(date_time, Lang['login-name'], client.user)
    if data['custom-activity'] != '':
        game = discord.Game(data['custom-activity'])
    else:
        game = discord.Game(date_time)
    #online,offline,idle,dnd,invisible
    await client.change_presence(status=discord.Status.online, activity=game)
    
@client.event
async def on_voice_state_update(member, before, after):
    channel = after.channel
    try:
        if before.channel.members == [] and not before.channel.id == int(data['local-channel-id']):
            if before.channel.category_id == int(data['create-category-id']) and before.channel.name == member.name + Lang['create-channel-name']:
                await before.channel.delete()
    except:
        pass
    if channel.id == int(data['local-channel-id']):
        guild = after.channel.guild
        private_channels = discord.utils.get(guild.categories, id= int(data['create-category-id']))
        voice_channel = await guild.create_voice_channel(member.name + Lang['create-channel-name'], overwrites=None, category=private_channels)
        await member.move_to(voice_channel)
        await voice_channel.set_permissions(member, manage_channels=True, manage_permissions=True)
        print(date_time, member.name, Lang['when-channel-create'])

@client.event
async def on_message(message):
    global data, prefix, Lang
    admin = False
    if message.author.id== int(data['admin-id-1']) or message.author.id== int(data['admin-id-2']):
        admin = True
    if message.author == client.user:
        return
    
    if message.content.startswith(prefix+'gay') and data['command-gay'] == 'true':
        gay_temp = message.content.split(" ",2)
        if len(gay_temp) == 1:
            embed = discord.Embed(title=Lang['usage'], description=prefix+'gay '+Lang['@user'], color=0x4b49d8)
            gay_error_message = await message.channel.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
            await gay_error_message.delete()
        else:
            embed = discord.Embed(title=message.mentions[0].name+' #'+message.mentions[0].discriminator, description=str(random.randrange(100))+'% gay', color=0x4b49d8)
            gay_message = await message.channel.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
            await gay_message.delete()
    if message.content.startswith(prefix+'time') and data['command-time'] == 'true':
        await message.reply(date_time, mention_author=True)
        return
    if message.content.startswith(prefix+'exit') and data['command-exit'] == 'true':
        if admin == True:
            await message.delete()
            game = discord.Game(date_time)
            await client.change_presence(status=discord.Status.offline, activity=game)
            sys.exit()
        else:
            await error_code.permission(message, Lang)
    if message.content.startswith(prefix+'tlm') and data['command-tlm'] == 'true':
        if admin == True:
            await message.delete()
            time_limit_message_temp = message.content.split(" ",2)
            if len(time_limit_message_temp) == 1:
                embed = discord.Embed(title=Lang['usage'], description=prefix+'tlm '+Lang['message'], color=0x4b49d8)
                embed.add_field(name=Lang['uses'], value=Lang['temp-message'], inline=False)
                time_limit_error_message = await message.channel.send(embed=embed)
                await asyncio.sleep(10)
                await time_limit_error_message.delete()   
            else:
                text = time_limit_message_temp[1]+' '
                for i in range(2, len(time_limit_message_temp)):
                    text += time_limit_message_temp[i]
                time_limit_message = await message.channel.send(text)
                print(date_time, message.author,Lang['sent-temp-message'],text)
                await asyncio.sleep(600)
                await time_limit_message.delete()
        else:
            await error_code.permission(message, Lang)
    if message.content.startswith(prefix+'copy') and data['command-copy'] == 'true':
        if admin == True:
            await message.delete()
            copy_temp = message.content.split(" ",2)
            guild = message.channel.guild
            existing_channel = discord.utils.get(guild.channels, name=message.channel.name)
            if len(copy_temp) == 1:
                if existing_channel is not None:
                    await existing_channel.clone()
            else:
                if existing_channel is not None and copy_temp[1]=='-d':
                    await existing_channel.clone()
                    await existing_channel.delete()
        else:
            await error_code.permission(message, Lang)
    if message.content.startswith(prefix+'reload') and data['command-reload'] == 'true':
        if admin == True:
            print(date_time, Lang['reloaded'])
            await message.delete()
            await message.channel.send(Lang['reloaded'])
            data = json.load(open('config.json'))
            prefix = data['command-prefix']
            Lang = lang.lang_chose(data['language'])
            if data['custom-activity'] != '':
                game = discord.Game(data['custom-activity'])
            else:
                game = discord.Game(date_time)
            await client.change_presence(status=discord.Status.online, activity=game)
        else:
            await error_code.permission(message, Lang)
    if message.content.startswith(prefix+'chlang') and data['command-chlang'] == 'true':
        if admin == True:
            await message.delete()
            chlang_temp = message.content.split(" ",2)
            checked = await lang.chlang_check(message, chlang_temp[1], Lang)
            if checked == False:
                return
            elif len(chlang_temp) == 1 or len(chlang_temp) >= 3:
                embed = discord.Embed(title=Lang['usage'], description=prefix+'chlang '+Lang['language'], color=0x4b49d8)
                embed.add_field(name=Lang['uses'], value=Lang['change-lang-message'], inline=False)
                chlang_error_message = await message.channel.send(embed=embed)
                await asyncio.sleep(10)
                await chlang_error_message.delete()
            else:
                chlang = 'lang/'+chlang_temp[1]+'.json'
                with open(chlang, "r", encoding = "utf8") as lang_file:
                    Lang = json.load(lang_file)
                await message.channel.send(Lang['lang-changed'])
        else:
            await error_code.permission(message, Lang)
    if message.content.startswith(prefix+'chact') and data['command-chact'] == 'true':
        if admin == True:
            await message.delete()
            chact_temp = message.content.split(" ",2)
            if len(chact_temp) == 1:
                embed = discord.Embed(title=Lang['usage'], description=prefix+'chact '+Lang['message'], color=0x4b49d8)
                chact_error_message = await message.channel.send(embed=embed)
                await asyncio.sleep(10)
                await chact_error_message.delete()
            else:
                chact = chact_temp[1]+' '
                for i in range(2, len(chact_temp)):
                    chact += chact_temp[i]
                game = discord.Game(chact)
                await client.change_presence(status=discord.Status.online, activity=game)
                await message.channel.send(Lang['activity-changed']+' '+chact)
        else:
            await error_code.permission(message, Lang)
    if message.content.startswith(prefix):
        temp = message.content.split(" ",2)
        if len(temp) == 1:
            await message.reply(Lang['unknown-command'], mention_author=True)
    if message.channel.id == int(data['picture-only-channel-id']) and message.content != "":
        await message.channel.purge(limit=1)

client.run(data['token'])