import discord
from datetime import datetime
from discord.ext import commands
import random
import asyncio
import sys
import json
import logging
import tracemalloc
import error_code

with open('config.json', "r", encoding = "utf8") as file:
    data = json.load(file)

now = datetime.now()
date_time = '<'+now.strftime("%Y-%m-%d, %H:%M:%S")+'>'

prefix = data['command-prefix']
client = discord.Client()
intents = discord.Intents.all()

tracemalloc.start()

FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.NOTSET, filename='BotLog.log', filemode='w', format=FORMAT)

@client.event
async def on_ready():
    print(date_time+' 目前登入身份：',client.user)
    game = discord.Game(date_time)
    #online,offline,idle,dnd,invisible
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_voice_state_update(member, before, after):
    channel = after.channel
    try:
        if before.channel.members == [] and not before.channel.id == int(data['local-channel-id']):
            if before.channel.category_id == int(data['create-category-id']) and before.channel.name == member.name + ' 的頻道':
                await before.channel.delete()
    except:
         pass
    if channel.id == int(data['local-channel-id']):
        guild = after.channel.guild
        private_channels = discord.utils.get(guild.categories, id= int(data['create-category-id']))
        voice_channel = await guild.create_voice_channel(member.name + ' 的頻道', overwrites=None, category=private_channels)
        await member.move_to(voice_channel)
        await voice_channel.set_permissions(member, manage_channels=True, manage_permissions=True)
        print(date_time, member.name+' 建立了語音頻道')

@client.event
async def on_message(message):
    global data, prefix
    admin = False
    if message.author.id== int(data['admin-id-1']) or message.author.id== int(data['admin-id-2']):
        admin = True
    if message.author == client.user:
        return

    if message.content.startswith(prefix+'gay'):
        gay_temp = message.content.split(" ",2)
        if len(gay_temp) == 1:
            embed = discord.Embed(title='用法:', description='.gay <@user>', color=0x4b49d8)
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
    if message.content.startswith(prefix+'day'):
        await message.reply(date_time, mention_author=True)
    if message.content.startswith(prefix+'exit'):
        if admin == True:
            await message.delete()
            game = discord.Game(date_time)
            await client.change_presence(status=discord.Status.offline, activity=game)
            client.close()
            sys.exit()
        else:
            await error_code.no_permission(message)
    if message.content.startswith(prefix+'tlm'):
        if admin == True:
            await message.delete()
            time_limit_message_temp = message.content.split(" ",2)
            if len(time_limit_message_temp) == 1:
                embed = discord.Embed(title='用法:', description='.tlm <message>', color=0x4b49d8)
                embed.add_field(name="用途:", value="發送一個臨時訊息", inline=False)
                time_limit_error_message = await message.channel.send(embed=embed)
                await asyncio.sleep(10)
                await time_limit_error_message.delete()   
            else:
                text = time_limit_message_temp[1]+' '
                for i in range(2, len(time_limit_message_temp)):
                    text += time_limit_message_temp[i]
                time_limit_message = await message.channel.send(text)
                print(date_time, message.author,'發送了臨時訊息:',text)
                await asyncio.sleep(600)
                await time_limit_message.delete()
        else:
            await error_code.no_permission(message)
    if message.content.startswith(prefix+'copy'):
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
            await error_code.no_permission(message)
    if message.content.startswith(prefix+'reload'):
        if admin == True:
            print(date_time,'設定檔已重新加載')
            await message.delete()
            await message.channel.send('設定檔已重新加載')
            data = json.load(open('config.json'))
            prefix = data['command-prefix']
        else:
            await error_code.no_permission(message)
    if message.content.startswith(prefix):
        temp = message.content.split(" ",2)
        if len(temp) == 1:
            await message.reply('未知的指令', mention_author=True)

client.run(data['token'])