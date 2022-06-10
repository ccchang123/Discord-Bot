import asyncio
import hashlib
import json
import logging
import os
import random
import re
import shutil
import socket
import sys
import time
import tracemalloc
import zipfile
import datetime

import discord
import mechanize
import requests
import wget
import youtube_dl
from discord import FFmpegPCMAudio
from discord.ext import commands, tasks
from discord.opus import *
from discord_components import *
from dislash import *
from pandas import Categorical
from ping3 import ping as pin
from youtubesearchpython import VideosSearch

from lib import error_code, reset, self_test, web

if os.path.isfile('RunMeFirst.bat'):
    os.remove('RunMeFirst.bat')
if not os.path.isdir('C:\\ffmpeg'):
    print('Downloading required resources...')
    wget.download('https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip', './')
    zf = zipfile.ZipFile('ffmpeg-master-latest-win64-gpl.zip', 'r')
    zf.extractall()
    os.rename('ffmpeg-master-latest-win64-gpl', 'ffmpeg')
    os.system(r'move ./ffmpeg C:\\')
if os.path.isfile('Discord-Bot-main.zip'):
    os.remove('Discord-Bot-main.zip')

def copyright():
    info = """-------------------------------------------------------\n
            Ivrj zber vasbezngvba va tvguho:
                 uggcf://ovg.yl/3S2wwFd\n
                         Jvxv:
                 uggcf://ovg.yl/3YNo42k\n
                     Vaivgr gur obg:
                 uggcf://ovg.yl/3ZzlTLW\n
    Pbclevtug © 2022 PUNAT, LH-UFV. Nyy evtugf erfreirq.\n
-------------------------------------------------------"""
    d = {}
    for c in (65, 97):
        for i in range(26):
            d[chr(i+c)] = chr((i+13) % 26 + c)
    copyright_world = "".join([d.get(c, c) for c in info])
    return copyright_world

print(copyright())

if not os.path.isfile('config.json'):
    print('load config file --- fail')
    self_test.error()
else:
    print('load config file --- success')
    from lib import lang

self_test.check_config()
self_test.check_file()

with open('config.json', "r", encoding = "utf8") as file:
    data = json.load(file)

version = '117a9d51a5563221118cdb43d746b70ddfc429c492ff76751948a26b9a61beb6c847fd7da26984926ced71c2b77c813689bec51f72d3528899c1c23e3488534c'
self_test.check_version(data, version)

def load_serverdata():
    global server_data, serverdata_keys, serverdata_values
    with open('database/serverdata.json', "r", encoding = "utf8") as serverdata_file:
        server_data = json.load(serverdata_file)
    serverdata_keys = list(server_data.keys())
    serverdata_values = list(server_data.values())

def load_userdata():
    global user_data, userdata_keys, userdata_values
    with open('database/userdata.json', "r", encoding = "utf8") as userdata_file:
        user_data = json.load(userdata_file)
    userdata_keys = list(user_data.keys())
    userdata_values = list(user_data.values())

def add_lang():
    global lang_list, Lang
    lang_list = []
    Lang = {}
    for k in os.listdir('lang'):
        if k.endswith(".json"):
            with open(f'lang/{k}', "r", encoding = "utf8") as langdata_file:
                lang_data = json.load(langdata_file)
            lang = k.split(".",2)
            lang_list.append(lang[0])
            Lang[lang[0]] = lang_data

load_serverdata()
load_userdata()
add_lang()
self_test.check(data, lang_list)

global_Lang = lang.lang_chose(data['language'], lang_list, data)

print(global_Lang['version'], data['version'])
if data['debug-mode']:
    if not os.path.isdir('log/'):
        os.mkdir('log')
    file_name = datetime.datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime('%Y-%m-%d')
    if os.path.isfile('log/'+yesterday+'.log'):
        log_zipfile = zipfile.ZipFile('log/'+yesterday+'.zip', 'w', zipfile.ZIP_DEFLATED)
        log_zipfile.write('log/'+yesterday+'.log')
        log_zipfile.close()
        os.remove('log/'+yesterday+'.log')
    FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    logging.basicConfig(level=logging.NOTSET, filename='log/'+file_name+'.log', filemode='a', format=FORMAT)
    print(global_Lang['debug-enabled'])
else:
    print(global_Lang['debug-disabled'])

prefix = data['command-prefix']
intents = discord.Intents.all()
intents.members = True
intents.guilds = True
bot = ComponentsBot(data['command-prefix'],intents = intents)
bot.remove_command('help')
interClient = InteractionClient(bot, show_warnings=False)
guild_id = [int(i) for i in list(server_data['guilds'].keys())]

def now_time():
    now = datetime.datetime.now()
    date_time = '['+now.strftime("%Y-%m-%d, %H:%M:%S")+']'
    return date_time

with open('database/salt.json', "r", encoding = "utf8") as salt_file:
    user_salt = json.load(salt_file)

def salt(id):
    global user_salt
    salt = ''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+-*/=~`!@#$%^&(){}[]\'"<>?\\|,0123456789:;_', 16))
    if not user_salt.__contains__(str(id)):
        user_salt[str(id)] = str(salt)
    with open("database/salt.json", "w") as salt_file:
        json.dump(user_salt, salt_file, indent = 4)

tracemalloc.start()

async def main_menu_1(ctx):
    embed = discord.Embed(title='❗｜'+Lang[server_data['language'][str(ctx.guild.id)]]['menu-name'], color=0x81FA28)
    menu_1 = await ctx.send(embed=embed, content='', components=[SelectMenu(placeholder=Lang[server_data['language'][str(ctx.guild.id)]]['menu-select'], options= [
                                                    SelectOption(label=Lang[server_data['language'][str(ctx.guild.id)]]['menu-music'], value=Lang[server_data['language'][str(ctx.guild.id)]]['menu-music'], emoji='🎧'),
                                                    SelectOption(label=prefix+'chlang', value=prefix+'chlang', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-chlang'], emoji='🇺🇳'),
                                                    SelectOption(label=prefix+'add', value=prefix+'add', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-add'], emoji='🛠'),
                                                    SelectOption(label=prefix+'addadmin', value=prefix+'addadmin', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-addadmin'], emoji='🛠'),
                                                    SelectOption(label=prefix+'addbypass', value=prefix+'addbypass', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-addbypass'], emoji='✅'),
                                                    SelectOption(label=prefix+'ban', value=prefix+'ban', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-ban'], emoji='🚫'),
                                                    SelectOption(label=prefix+'clear', value=prefix+'clear', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-clear'], emoji='🗑'),
                                                    SelectOption(label=prefix+'copy', value=prefix+'copy', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-copy'], emoji='✂'),
                                                    SelectOption(label=prefix+'copy -d', value=prefix+'copy'+'-d', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-copy-delete'], emoji='✂'),
                                                    SelectOption(label=prefix+'clearwarn', value=prefix+'clearwarn', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-clearwarn'], emoji='🗑'),
                                                    SelectOption(label=prefix+'cd', value=prefix+'cd', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-cd'], emoji='🗑'),
                                                    SelectOption(label=prefix+'ci', value=prefix+'ci', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-ci'], emoji='😎'),
                                                    SelectOption(label=prefix+'check', value=prefix+'check', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-check'], emoji='❓'),
                                                    SelectOption(label=prefix+'exit', value=prefix+'exit', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-exit'], emoji='⏹'),
                                                    SelectOption(label=prefix+'gay', value=prefix+'gay', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-gay'], emoji='💕'),
                                                    SelectOption(label=prefix+'kick', value=prefix+'kick', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-kick'], emoji='🦵'),
                                                    SelectOption(label=prefix+'mute', value=prefix+'mute', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-mute'], emoji='🔈'),
                                                    SelectOption(label=prefix+'ping', value=prefix+'ping', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-ping'], emoji='📌'),
                                                    SelectOption(label=prefix+'reload', value=prefix+'reload', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-reload'], emoji='🔄'),
                                                    SelectOption(label=prefix+'remove', value=prefix+'remove', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-remove'], emoji='🗑'),
                                                    SelectOption(label=prefix+'removeadmin', value=prefix+'removeadmin', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-removeadmin'], emoji='🗑'),
                                                    SelectOption(label=prefix+'removebypass', value=prefix+'removebypass', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-removebypass'], emoji='🗑'),
                                                    SelectOption(label=prefix+'set', value=prefix+'set', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-set'], emoji='⚙'),
                                                    SelectOption(label=Lang[server_data['language'][str(ctx.guild.id)]]['next-page'], value=Lang[server_data['language'][str(ctx.guild.id)]]['next-page'], emoji='➡')
                                                ],
                                                custom_id='main_menu_1'
    )])
    while True:
        interaction = await bot.wait_for('select_option', check = lambda inter: inter.custom_id == 'main_menu_1')
        res = interaction.values[0]
        try:
            if res == prefix+'clear':
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], color=0xEC2E2E)
                embed.add_field(name=prefix+'clear '+Lang[server_data['language'][str(ctx.guild.id)]]['count'], value=Lang[server_data['language'][str(ctx.guild.id)]]['message-clear-tip']+Lang[server_data['language'][str(ctx.guild.id)]]['count']+Lang[server_data['language'][str(ctx.guild.id)]]['message-clear-tip-count'], inline=False)
                embed.add_field(name=prefix+'clear '+Lang[server_data['language'][str(ctx.guild.id)]]['count']+Lang[server_data['language'][str(ctx.guild.id)]]['@user'], value=Lang[server_data['language'][str(ctx.guild.id)]]['message-clear-tip']+Lang[server_data['language'][str(ctx.guild.id)]]['@user']+Lang[server_data['language'][str(ctx.guild.id)]]["someone's"]+' '+Lang[server_data['language'][str(ctx.guild.id)]]['count']+Lang[server_data['language'][str(ctx.guild.id)]]['message-clear-tip-count'], inline=False)
                await interaction.send(embed=embed)
            elif res == prefix+'chlang':
                lang_search_list = []
                op = []
                num = 0
                for i in list(Lang.keys()):
                    with open('lang/'+i+'.json', 'r', encoding = "utf8") as lang_list:
                        lang_name = json.load(lang_list)
                    lang_search_list.append(i)
                    op.append(SelectOption(label=lang_name['name'], value=str(num), emoji='🔍'))
                    num += 1
                sele = await interaction.send(content=Lang[server_data['language'][str(ctx.guild.id)]]['search_result'], components=[SelectMenu(placeholder=Lang[server_data['language'][str(ctx.guild.id)]]['menu-select'], options= op,
                                                custom_id='lang_select'
                )])
                interaction = await bot.wait_for('select_option', check = lambda inter: inter.custom_id == 'lang_select')
                res = interaction.values[0]
                for j in range(len(op)):
                    try:
                        if res == str(j):
                            language = lang_search_list[j]
                            serverdata_dict = {}
                            for i in range(len(serverdata_keys)):
                                serverdata_dict[serverdata_keys[i]] = serverdata_values[i]
                            serverdata_values_dict = serverdata_values[serverdata_keys.index('language')]
                            serverdata_values_dict[str(ctx.guild.id)] = language
                            serverdata_dict['language'] = serverdata_values_dict
                            with open("database/serverdata.json", "w") as serverdata_file:
                                json.dump(serverdata_dict, serverdata_file, indent = 4)
                            load_serverdata()
                            embed = discord.Embed(title='🇺🇳｜'+Lang[server_data['language'][str(ctx.guild.id)]]['lang-changed'], color=0x81FA28)
                            await interaction.send(embed=embed)
                            print(now_time(), Lang[server_data['language'][str(ctx.guild.id)]]['lang-changed'], language, Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
                            break
                        else:
                            continue
                    except:
                        return
            elif res == prefix+'copy':
                await interaction.send(Lang[server_data['language'][str(ctx.guild.id)]]['selected']+res)
                await copy(ctx)
            elif res == prefix+'copy'+'-d':
                await interaction.send(Lang[server_data['language'][str(ctx.guild.id)]]['selected']+res)
                await copy(ctx, '-d')
            elif res == prefix+'gay':
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'gay '+Lang[server_data['language'][str(ctx.guild.id)]]['@user'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'exit':
                await interaction.send(Lang[server_data['language'][str(ctx.guild.id)]]['selected']+res)
                await exit(ctx)
            elif res == prefix+'reload':
                await interaction.send(Lang[server_data['language'][str(ctx.guild.id)]]['selected']+res)
                await reload(ctx)
            elif res == prefix+'ban':
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'ban '+Lang[server_data['language'][str(ctx.guild.id)]]['@user']+Lang[server_data['language'][str(ctx.guild.id)]]['reason'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'kick':
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'kick '+Lang[server_data['language'][str(ctx.guild.id)]]['@user']+Lang[server_data['language'][str(ctx.guild.id)]]['reason'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'clearwarn':
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'clearwarn '+Lang[server_data['language'][str(ctx.guild.id)]]['@user']+' (-a)', color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'addbypass':
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'addbypass '+Lang[server_data['language'][str(ctx.guild.id)]]['@user'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'addadmin':
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'addadmin '+Lang[server_data['language'][str(ctx.guild.id)]]['@user'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'removebypass':
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'removebypass '+Lang[server_data['language'][str(ctx.guild.id)]]['@user'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'removeadmin':
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'removeadmin '+Lang[server_data['language'][str(ctx.guild.id)]]['@user'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'mute':
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'mute '+Lang[server_data['language'][str(ctx.guild.id)]]['@user']+Lang[server_data['language'][str(ctx.guild.id)]]['reason'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'cd':
                await interaction.send(Lang[server_data['language'][str(ctx.guild.id)]]['selected']+res)
                await cd(ctx)
            elif res == prefix+'ci':
                await interaction.send(Lang[server_data['language'][str(ctx.guild.id)]]['selected']+res)
                await ci(ctx)
            elif res == prefix+'ping':
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'ping [IP]', color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == Lang[server_data['language'][str(ctx.guild.id)]]['menu-music']:
                await menu_1.delete()
                await music_menu(ctx)
            elif res == Lang[server_data['language'][str(ctx.guild.id)]]['next-page']:
                await menu_1.delete()
                await main_menu_2(ctx)
            elif res == prefix+'add':
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], color=0xEC2E2E)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-picture-only-channel'], value=prefix+'add picture-only-channel'+Lang[server_data['language'][str(ctx.guild.id)]]['channel']+' ...', inline=False)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-chat-filter'], value=prefix+'add chat-filter'+Lang[server_data['language'][str(ctx.guild.id)]]['regex'], inline=False)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-enter-voice-channel'], value=prefix+'add enter-voice-channel'+Lang[server_data['language'][str(ctx.guild.id)]]['channel']+' ...', inline=False)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-voice-category'], value=prefix+'add voice-category'+Lang[server_data['language'][str(ctx.guild.id)]]['category'], inline=False)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-reaction-roles'], value=prefix+'add reaction-roles'+Lang[server_data['language'][str(ctx.guild.id)]]['reaction']+Lang[server_data['language'][str(ctx.guild.id)]]['role'], inline=False)
                await interaction.send(embed=embed)
            elif res == prefix+'remove':
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], color=0xEC2E2E)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-picture-only-channel'], value=prefix+'remove picture-only-channel'+Lang[server_data['language'][str(ctx.guild.id)]]['channel']+' ...', inline=False)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-chat-filter'], value=prefix+'remove chat-filter'+Lang[server_data['language'][str(ctx.guild.id)]]['regex'], inline=False)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-enter-voice-channel'], value=prefix+'remove enter-voice-channel'+Lang[server_data['language'][str(ctx.guild.id)]]['channel']+' ...', inline=False)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-voice-category'], value=prefix+'remove voice-category'+Lang[server_data['language'][str(ctx.guild.id)]]['category'], inline=False)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-reaction-roles'], value=prefix+'remove reaction-roles'+Lang[server_data['language'][str(ctx.guild.id)]]['reaction'], inline=False)
                await interaction.send(embed=embed)
            elif res == prefix+'check':
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], color=0xEC2E2E)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['check-chat-filter'], value=prefix+'check chat-filter', inline=False)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['check-picture-only-channel'], value=prefix+'check picture-only-channel', inline=False)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['check-private-voice-channel'], value=prefix+'check private-voice-channel', inline=False)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['check-auto-action'], value=prefix+'check auto-action', inline=False)
                await interaction.send(embed=embed)
            elif res == prefix+'set':
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], color=0xEC2E2E)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-auto-action'], value=prefix+'set auto-action'+Lang[server_data['language'][str(ctx.guild.id)]]['count']*3, inline=False)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-chat-filter-action'], value=prefix+'set chat-filter-action'+Lang[server_data['language'][str(ctx.guild.id)]]['action'], inline=False)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-music-bot'], value=prefix+'set music-bot'+Lang[server_data['language'][str(ctx.guild.id)]]['true_or_false'], inline=False)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-commands'], value=prefix+'set commands'+Lang[server_data['language'][str(ctx.guild.id)]]['command']+Lang[server_data['language'][str(ctx.guild.id)]]['true_or_false'], inline=False)
                await interaction.send(embed=embed)
        except: ...
async def main_menu_2(ctx):
    embed = discord.Embed(title='❗｜'+Lang[server_data['language'][str(ctx.guild.id)]]['menu-name'], color=0x81FA28)
    menu_2 = await ctx.send(embed=embed, content='', components=[SelectMenu(placeholder=Lang[server_data['language'][str(ctx.guild.id)]]['menu-select'], options= [
                                                    SelectOption(label=Lang[server_data['language'][str(ctx.guild.id)]]['previous-page'], value=Lang[server_data['language'][str(ctx.guild.id)]]['previous-page'], emoji='⬅'),
                                                    SelectOption(label=prefix+'showwarn', value=prefix+'showwarn', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-showwarn'], emoji='📄'),
                                                    SelectOption(label=prefix+'slowmode', value=prefix+'slowmode', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-slowmoe'], emoji='🐢'),
                                                    SelectOption(label=prefix+'send', value=prefix+'send', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-send'], emoji='📨'),
                                                    SelectOption(label=prefix+'time', value=prefix+'time', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-time'], emoji='⏱'),
                                                    SelectOption(label=prefix+'tlm', value=prefix+'tlm', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-tlm'], emoji='📨'),
                                                    SelectOption(label=prefix+'tempban', value=prefix+'tempban', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-tempban'], emoji='🚫'),
                                                    SelectOption(label=prefix+'tempmute', value=prefix+'tempmute', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-tempmute'], emoji='🔈'),
                                                    SelectOption(label=prefix+'unban', value=prefix+'unban', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-unban'], emoji='⭕'),
                                                    SelectOption(label=prefix+'unmute', value=prefix+'unmute', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-unmute'], emoji='🔊'),
                                                    SelectOption(label=prefix+'uinfo', value=prefix+'uinfo', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-uinfo'], emoji='🕵️'),
                                                    SelectOption(label=prefix+'warn', value=prefix+'warn', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-warn'], emoji='⚠')
                                                ],
                                                custom_id='main_menu_2'
    )])
    while True:
        interaction = await bot.wait_for('select_option', check = lambda inter: inter.custom_id == 'main_menu_2')
        res = interaction.values[0]
        try:
            if res == prefix+'warn':
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'warn '+Lang[server_data['language'][str(ctx.guild.id)]]['@user']+Lang[server_data['language'][str(ctx.guild.id)]]['reason'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'unmute':
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'unmute '+Lang[server_data['language'][str(ctx.guild.id)]]['@user'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'uinfo':
                await interaction.send(Lang[server_data['language'][str(ctx.guild.id)]]['selected']+res)
                await uinfo(interaction)
            elif res == prefix+'unban':
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'unban '+Lang[server_data['language'][str(ctx.guild.id)]]['@user'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'tempmute':
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'tempmute '+Lang[server_data['language'][str(ctx.guild.id)]]['@user']+Lang[server_data['language'][str(ctx.guild.id)]]['duration']+Lang[server_data['language'][str(ctx.guild.id)]]['reason'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'tempban':
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'tempban '+Lang[server_data['language'][str(ctx.guild.id)]]['@user']+Lang[server_data['language'][str(ctx.guild.id)]]['duration']+Lang[server_data['language'][str(ctx.guild.id)]]['reason'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'tlm':
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'tlm '+Lang[server_data['language'][str(ctx.guild.id)]]['message'], color=0xEC2E2E)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['uses'], value=Lang[server_data['language'][str(ctx.guild.id)]]['temp-message'], inline=False)
                await interaction.send(embed=embed)
            elif res == Lang[server_data['language'][str(ctx.guild.id)]]['previous-page']:
                await menu_2.delete()
                await main_menu_1(ctx)
            elif res == prefix+'time':
                await interaction.send(Lang[server_data['language'][str(ctx.guild.id)]]['selected']+res)
                await time(ctx)
            elif res == prefix+'send':
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'send '+Lang[server_data['language'][str(ctx.guild.id)]]['message'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'slowmode':
                await interaction.send(Lang[server_data['language'][str(ctx.guild.id)]]['selected']+res)
                await slowmode(ctx)
            elif res == prefix+'showwarn':
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'showwarn '+Lang[server_data['language'][str(ctx.guild.id)]]['@user'], color=0xEC2E2E)
                await interaction.send(embed=embed)
        except: ...
async def music_menu(ctx):
    embed = discord.Embed(title='❗｜'+Lang[server_data['language'][str(ctx.guild.id)]]['menu-music-name'], color=0x81FA28)
    await ctx.send(embed=embed, content='', components=[SelectMenu(placeholder=Lang[server_data['language'][str(ctx.guild.id)]]['menu-select'], options= [
                                                    SelectOption(label=prefix+'play', value='play', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-play'], emoji='▶'),
                                                    SelectOption(label=prefix+'leave', value='leave', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-leave'], emoji='⏹'),
                                                    SelectOption(label=prefix+'pause', value='pause', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-pause'], emoji='⏸'),
                                                    SelectOption(label=prefix+'resume', value='resume', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-resume'], emoji='⏯'),
                                                    SelectOption(label=prefix+'repeat', value='repeat', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-repeat'], emoji='🔁'),
                                                    SelectOption(label=prefix+'stop', value='stop', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-stop'], emoji='⏹'),
                                                    SelectOption(label=prefix+'volume', value='volume', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-volume'], emoji='🔊'),
                                                    SelectOption(label=prefix+'skip', value='skip', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-skip'], emoji='⏩'),
                                                    SelectOption(label=prefix+'playlist', value='playlist', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-playlist'], emoji='📜'),
                                                    SelectOption(label=prefix+'listmove', value='listmove', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-listmove'], emoji='🔃'),
                                                    SelectOption(label=prefix+'listremove', value='listremove', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-listremove'], emoji='🗑'),
                                                    SelectOption(label=prefix+'listrandom', value='listrandom', description=Lang[server_data['language'][str(ctx.guild.id)]]['menu-message-listrandom'], emoji='🔀'),
                                                    SelectOption(label=prefix+'favorite add', value='favorite add', description=Lang[server_data['language'][str(ctx.guild.id)]]['favorite-menu-add'], emoji='💕'),
                                                    SelectOption(label=prefix+'favorite remove', value='favorite remove', description=Lang[server_data['language'][str(ctx.guild.id)]]['favorite-menu-remove'], emoji='🗑'),
                                                    SelectOption(label=prefix+'favorite list', value='favorite list', description=Lang[server_data['language'][str(ctx.guild.id)]]['favorite-menu-list'], emoji='📜'),
                                                    SelectOption(label=prefix+'favorite play', value='favorite play', description=Lang[server_data['language'][str(ctx.guild.id)]]['favorite-menu-play'], emoji='▶')
                                                ],
                                                custom_id='music_menu'
    )])

@bot.event
async def on_select_option(interaction):
    match interaction.values[0]:
        case 'leave':
            await interaction.send(Lang[server_data['language'][str(interaction.author.guild.id)]]['selected']+interaction.values[0])
            await leave(interaction)
        case 'pause':
            await interaction.send(Lang[server_data['language'][str(interaction.author.guild.id)]]['selected']+interaction.values[0])
            await pause(interaction)
        case 'resume':
            await interaction.send(Lang[server_data['language'][str(interaction.author.guild.id)]]['selected']+interaction.values[0])
            await resume(interaction)
        case 'repeat':
            await interaction.send(Lang[server_data['language'][str(interaction.author.guild.id)]]['selected']+interaction.values[0])
            await repeat(interaction)
        case 'stop':
            await interaction.send(Lang[server_data['language'][str(interaction.author.guild.id)]]['selected']+interaction.values[0])
            await stop(interaction)
        case 'skip':
            await interaction.send(Lang[server_data['language'][str(interaction.author.guild.id)]]['selected']+interaction.values[0])
            await skip(interaction)
        case 'playlist':
            await interaction.send(Lang[server_data['language'][str(interaction.author.guild.id)]]['selected']+interaction.values[0])
            await playlist(interaction)
        case 'listrandom':
            await interaction.send(Lang[server_data['language'][str(interaction.author.guild.id)]]['selected']+interaction.values[0])
            await listrandom(interaction)
        case 'favorite list':
            await interaction.send(Lang[server_data['language'][str(interaction.author.guild.id)]]['selected']+interaction.values[0])
            await favorite(interaction, 'list')

@bot.event
async def on_ready():
    print(global_Lang['server-added'], len(bot.guilds))
    member_count = 0
    guild_dict = {}
    for i in range(len(bot.guilds)):
        guild_dict[bot.guilds[i].id] = bot.guilds[i].name
        print(bot.guilds[i].id, ':', bot.guilds[i].name, f'({bot.guilds[i].member_count})')
        member_count += bot.guilds[i].member_count
    server_data['guilds'] = guild_dict
    with open("database/serverdata.json", "w") as serverdata_file:
        json.dump(server_data, serverdata_file, indent = 4)
    load_serverdata() 
    print(global_Lang['member-count'], f'{len(user_salt)} / {member_count}', f'({str((len(user_salt)/member_count)*100)[:5]} %)',end='\n\n')
    print(now_time(), global_Lang['login-name'], bot.user)
    match data['custom-activity']:
        case 'playing':
            activity = discord.Game(data['activity-name']) if data['activity-name'] != '' else discord.Game(name=prefix+"menu")
        case 'streaming':
            activity = discord.Streaming(name=data['activity-name'], url=data['activity-streaming-url']) if data['activity-name'] != '' else discord.Streaming(name=prefix+"menu", url=data['activity-streaming-url'])
        case 'listening':
            activity = discord.Activity(type=discord.ActivityType.listening, name=data['activity-name']) if data['activity-name'] != '' else discord.Activity(type=discord.ActivityType.listening, name=prefix+"menu")
        case 'watching':
            activity = discord.Activity(type=discord.ActivityType.watching, name=data['activity-name']) if data['activity-name'] != '' else discord.Activity(type=discord.ActivityType.watching, name=prefix+"menu")
    match data['custom-status']: 
        case 'offline':
            await bot.change_presence(status=discord.Status.offline, activity=activity)
        case 'idle':
            await bot.change_presence(status=discord.Status.idle, activity=activity)
        case 'dnd':
            await bot.change_presence(status=discord.Status.dnd, activity=activity)
        case 'invisible':
            await bot.change_presence(status=discord.Status.invisible, activity=activity)
        case _:
            await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.reply(Lang[server_data['language'][str(ctx.guild.id)]]['unknown-command'])
        return
    if isinstance(error, commands.errors.MemberNotFound):
        await ctx.reply(Lang[server_data['language'][str(ctx.guild.id)]]['unknown-member'])
        return
    raise error

@bot.event
async def on_voice_state_update(member, before, after):
    channel = after.channel
    try:
        if before.channel.members == [] and not before.channel.id in server_data['enter-voice-channel'][str(member.guild.id)]:
            if before.channel.category_id in server_data['voice-category'][str(member.guild.id)] and before.channel.name == member.name + Lang[server_data['language'][str(member.guild.id)]]['create-channel-name']:
                await before.channel.delete()
    except: ...
    if channel == None:
        return
    try:
        if channel.id in server_data['enter-voice-channel'][str(member.guild.id)]:
            guild = after.channel.guild
            private_channels = discord.utils.get(guild.categories, id= server_data['voice-category'][str(member.guild.id)][0])
            voice_channel = await guild.create_voice_channel(member.name + Lang[server_data['language'][str(member.guild.id)]]['create-channel-name'], overwrites=None, category=private_channels, user_limit = 5)
            await member.move_to(voice_channel)
            await voice_channel.set_permissions(member, manage_channels=True, manage_permissions=True)
            print(now_time(), member, Lang[server_data['language'][str(member.guild.id)]]['when-channel-create'])
    except: ...

@bot.command()
async def menu(ctx, page: str='1'):
    match page:
        case '1':
            await main_menu_1(ctx)
        case '2':
            await main_menu_2(ctx)
        case 'music':
            await music_menu(ctx)
        case _:
            await main_menu_1(ctx)

@bot.command()
async def addadmin(ctx, user: discord.Member=None):
    if server_data['commands'][str(ctx.guild.id)]['addadmin']:
        if ctx.author.guild_permissions.administrator:
            global userdata_keys, userdata_values
            if not user:
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'addadmin '+Lang[server_data['language'][str(ctx.guild.id)]]['@user'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed, delete_after=5)
                return
            salt(user.id)
            sha1 = hashlib.sha1(user_salt[str(user.id)].encode('utf-8'))
            sha1.update(str(user.id).encode('utf-8'))
            sha512= hashlib.sha512()
            sha512.update(str(user).encode('utf-8'))
            if str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()) or user.guild_permissions.administrator:
                embed=discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['admin-had'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed)
            else:
                userdata_dict = {}
                for i in range(len(userdata_keys)):
                    userdata_dict[userdata_keys[i]] = userdata_values[i]
                userdata_values_dict = userdata_values[userdata_keys.index('admin')]
                userdata_new_dict = userdata_values_dict[str(ctx.guild.id)]
                userdata_new_dict[str(sha512.hexdigest())] = str(sha1.hexdigest())
                userdata_dict['admin'][str(ctx.guild.id)] = userdata_new_dict
                with open("database/userdata.json", "w") as userdata_file:
                    json.dump(userdata_dict, userdata_file, indent = 4)
                load_userdata()
                embed=discord.Embed(title=str(user)+Lang[server_data['language'][str(ctx.guild.id)]]['admin-added'], color=0x81FA28)
                await ctx.channel.send(embed=embed)
                print(now_time(), str(user)+Lang[server_data['language'][str(ctx.guild.id)]]['admin-added'], Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def addbypass(ctx, user: discord.Member=None):
    if server_data['commands'][str(ctx.guild.id)]['addbypass']:
        if ctx.author.guild_permissions.administrator:
            global userdata_keys, userdata_values
            if not user:
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'addbypass '+Lang[server_data['language'][str(ctx.guild.id)]]['@user'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed, delete_after=5)
            salt(user.id)
            sha1 = hashlib.sha1(user_salt[str(user.id)].encode('utf-8'))
            sha1.update(str(user.id).encode('utf-8'))
            sha512= hashlib.sha512()
            sha512.update(str(user).encode('utf-8'))
            if str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('bypass')][str(ctx.guild.id)].values()) or user.guild_permissions.administrator:
                embed=discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['bypass-had'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed)
            else:
                userdata_dict = {}
                for i in range(len(userdata_keys)):
                    userdata_dict[userdata_keys[i]] = userdata_values[i]
                userdata_values_dict = userdata_values[userdata_keys.index('bypass')]
                userdata_new_dict = userdata_values_dict[str(ctx.guild.id)]
                userdata_new_dict[str(sha512.hexdigest())] = str(sha1.hexdigest())
                userdata_dict['bypass'][str(ctx.guild.id)] = userdata_new_dict
                with open("database/userdata.json", "w") as userdata_file:
                    json.dump(userdata_dict, userdata_file, indent = 4)
                load_userdata()
                embed=discord.Embed(title=str(user)+Lang[server_data['language'][str(ctx.guild.id)]]['bypass-added'], color=0x81FA28)
                await ctx.channel.send(embed=embed)
                print(now_time(), str(user)+Lang[server_data['language'][str(ctx.guild.id)]]['bypass-added'], Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def ban(ctx, user: discord.Member=None, options='None', *, reason='None'):
    if server_data['commands'][str(ctx.guild.id)]['ban']:
        ctx_sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        ctx_sha1.update(str(ctx.author.id).encode('utf-8'))
        await ctx.message.delete()
        if not user:
            embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'ban '+Lang[server_data['language'][str(ctx.guild.id)]]['@user']+Lang[server_data['language'][str(ctx.guild.id)]]['reason'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed, delete_after=5)
        elif options == '--sync' and ctx.author.id == data['owner-id']:
            embed=discord.Embed(title=str(user)+Lang[server_data['language'][str(ctx.guild.id)]]['user-banned'], description=Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason']+reason, color=0x81FA28)
            try:
                await user.send(embed=embed)
            except: ...
            await ctx.guild.ban(user, reason=reason)
            await ctx.channel.send(embed=embed)
            print(now_time(), str(user), Lang[server_data['language'][str(ctx.guild.id)]]['user-banned'], Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason'], reason, Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
        elif ctx.author.guild_permissions.administrator or str(ctx_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            salt(user.id)
            user_sha1 = hashlib.sha1(user_salt[str(user.id)].encode('utf-8'))
            user_sha1.update(str(user.id).encode('utf-8'))
            if str(user_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('bypass')][str(ctx.guild.id)].values()) or user.guild_permissions.administrator:
                await error_code.bypass(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
            else:
                embed=discord.Embed(title=str(user)+Lang[server_data['language'][str(ctx.guild.id)]]['user-banned'], description=Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason']+options, color=0x81FA28)
                try:
                    await user.send(embed=embed)
                except: ...
                await ctx.guild.ban(user, reason=reason)
                await ctx.channel.send(embed=embed)
                print(now_time(), str(user), Lang[server_data['language'][str(ctx.guild.id)]]['user-banned'], Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason'], options, Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def clear(ctx, limit=0, member: discord.Member=None):
    if server_data['commands'][str(ctx.guild.id)]['clear']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            await ctx.message.delete()
            if limit == 0:
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description='', color=0xEC2E2E)
                embed.add_field(name=prefix+'clear '+Lang[server_data['language'][str(ctx.guild.id)]]['count'], value=Lang[server_data['language'][str(ctx.guild.id)]]['message-clear-tip']+Lang[server_data['language'][str(ctx.guild.id)]]['count']+Lang[server_data['language'][str(ctx.guild.id)]]['message-clear-tip-count'], inline=False)
                embed.add_field(name=prefix+'clear '+Lang[server_data['language'][str(ctx.guild.id)]]['count']+Lang[server_data['language'][str(ctx.guild.id)]]['@user'], value=Lang[server_data['language'][str(ctx.guild.id)]]['message-clear-tip']+Lang[server_data['language'][str(ctx.guild.id)]]['@user']+Lang[server_data['language'][str(ctx.guild.id)]]["someone's"]+' '+Lang[server_data['language'][str(ctx.guild.id)]]['count']+Lang[server_data['language'][str(ctx.guild.id)]]['message-clear-tip-count'], inline=False)
                await ctx.channel.send(embed=embed, delete_after=3)
                return
            msg = []
            if not member:
                try:
                    await ctx.channel.purge(limit=limit)
                except: ...
                print(now_time(), str(limit), Lang[server_data['language'][str(ctx.guild.id)]]['message-cleared'], Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
                embed = discord.Embed(title='🗑｜'+str(limit)+Lang[server_data['language'][str(ctx.guild.id)]]['message-cleared'], color=0x81FA28)
                await ctx.channel.send(embed=embed, delete_after=3)
                return
            async for m in ctx.channel.history():
                if len(msg) == limit:
                    break
                if m.author == member:
                    msg.append(m)
            await ctx.channel.delete_messages(msg)
            embed = discord.Embed(title='🗑｜'+str(member)+Lang[server_data['language'][str(ctx.guild.id)]]["someone's"]+' '+str(limit)+Lang[server_data['language'][str(ctx.guild.id)]]['message-cleared'], color=0x81FA28)
            await ctx.channel.send(embed=embed, delete_after=3)
            print(now_time(), str(member), Lang[server_data['language'][str(ctx.guild.id)]]["someone's"], str(limit), Lang[server_data['language'][str(ctx.guild.id)]]['message-cleared'], Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def chlang(ctx, language=''):
    if server_data['commands'][str(ctx.guild.id)]['chlang']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            if language == '':
                lang_search_list = []
                op = []
                num = 0
                for i in list(Lang.keys()):
                    with open('lang/'+i+'.json', 'r', encoding = "utf8") as lang_list:
                        lang_name = json.load(lang_list)
                    lang_search_list.append(i)
                    op.append(SelectOption(label=lang_name['name'], value=str(num), emoji='🔍'))
                    num += 1
                sele = await ctx.reply(content='', components=[SelectMenu(placeholder=Lang[server_data['language'][str(ctx.guild.id)]]['menu-select'], options= op,
                                                custom_id='lang_select'
                )])
                interaction = await bot.wait_for('select_option', check = lambda inter: inter.custom_id == 'lang_select')
                res = interaction.values[0]
                for j in range(len(op)):
                    try:
                        if res == str(j):
                            await ctx.message.delete()
                            await sele.delete()
                            language = lang_search_list[j]
                            serverdata_dict = {}
                            for i in range(len(serverdata_keys)):
                                serverdata_dict[serverdata_keys[i]] = serverdata_values[i]
                            serverdata_values_dict = serverdata_values[serverdata_keys.index('language')]
                            serverdata_values_dict[str(ctx.guild.id)] = language
                            serverdata_dict['language'] = serverdata_values_dict
                            with open("database/serverdata.json", "w") as serverdata_file:
                                json.dump(serverdata_dict, serverdata_file, indent = 4)
                            load_serverdata()
                            embed = discord.Embed(title='🇺🇳｜'+Lang[server_data['language'][str(ctx.guild.id)]]['lang-changed'], color=0x81FA28)
                            await interaction.send(embed=embed)
                            print(now_time(), Lang[server_data['language'][str(ctx.guild.id)]]['lang-changed'], language, Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
                            break
                        else:
                            continue
                    except:
                        return
            else:
                await ctx.message.delete()
                if '_' in language:
                    language = re.sub('_', '-', language)
                checked = await lang.chlang_check(ctx, language, Lang[server_data['language'][str(ctx.guild.id)]], data)
                if not checked:
                    return
                serverdata_dict = {}
                for i in range(len(serverdata_keys)):
                    serverdata_dict[serverdata_keys[i]] = serverdata_values[i]
                serverdata_values_dict = serverdata_values[serverdata_keys.index('language')]
                serverdata_values_dict[str(ctx.guild.id)] = language
                serverdata_dict['language'] = serverdata_values_dict
                with open("database/serverdata.json", "w") as serverdata_file:
                    json.dump(serverdata_dict, serverdata_file, indent = 4)
                load_serverdata()
                embed = discord.Embed(title='🇺🇳｜'+Lang[server_data['language'][str(ctx.guild.id)]]['lang-changed'], color=0x81FA28)
                await ctx.channel.send(embed=embed)
                print(now_time(), Lang[server_data['language'][str(ctx.guild.id)]]['lang-changed'], language, Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def copy(ctx, delete=''):
    if server_data['commands'][str(ctx.guild.id)]['copy']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            await ctx.message.delete()
            if delete == '':
                await ctx.channel.clone()
                print(now_time(), ctx.channel, Lang[server_data['language'][str(ctx.guild.id)]]['channel-copied'], Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
            elif delete == '-d':
                await ctx.channel.clone()
                await ctx.channel.delete()
                print(now_time(), ctx.channel, Lang[server_data['language'][str(ctx.guild.id)]]['channel-copied-deleted'], Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def clearwarn(ctx, member: discord.Member=None, options=''):
    if server_data['commands'][str(ctx.guild.id)]['clearwarn']:
        ctx_sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        ctx_sha1.update(str(ctx.author.id).encode('utf-8'))
        member_sha1 = hashlib.sha1(user_salt[str(member.id)].encode('utf-8'))
        member_sha1.update(str(member.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(ctx_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            if not member:
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'clearwarn '+Lang[server_data['language'][str(ctx.guild.id)]]['@user']+' (-a)', color=0xEC2E2E)
                await ctx.channel.send(embed=embed, delete_after=5)
            else:
                if int(user_data['warns'][str(ctx.guild.id)][str(member_sha1.hexdigest())]) == 0:
                    await ctx.channel.send(Lang[server_data['language'][str(ctx.guild.id)]]['user-nowarn'])
                    return
                else:
                    userdata_dict = {}
                    if options == '':
                        for i in range(len(userdata_keys)):
                            userdata_dict[userdata_keys[i]] = userdata_values[i]
                        userdata_values_dict = userdata_values[userdata_keys.index('warns')]
                        userdata_new_dict = userdata_values_dict[str(ctx.guild.id)]
                        userdata_new_dict[str(member_sha1.hexdigest())] = str(int(user_data['warns'][str(ctx.guild.id)][str(member_sha1.hexdigest())]) - 1)
                        userdata_dict['warns'][str(ctx.guild.id)] = userdata_new_dict
                        with open('database/userdata.json', 'w') as f:
                            json.dump(userdata_dict, f, indent = 4)
                        load_userdata()
                        embed = discord.Embed(title=member.name+Lang[server_data['language'][str(ctx.guild.id)]]['warn-amount']+user_data['warns'][str(ctx.guild.id)][str(member_sha1.hexdigest())], color=0xEC2E2E)
                        await ctx.channel.send(embed=embed)
                        print(now_time(), str(member), Lang[server_data['language'][str(ctx.guild.id)]]['warn-amount'], user_data['warns'][str(ctx.guild.id)][str(member_sha1.hexdigest())], Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
                    elif options == '-a':
                        user_data['warns'][str(ctx.guild.id)][str(member_sha1.hexdigest())] = '0'
                        with open('database/userdata.json', 'w') as f:
                            json.dump(user_data, f, indent = 4)
                        load_userdata()
                        embed = discord.Embed(title=member.name+Lang[server_data['language'][str(ctx.guild.id)]]['warn-cleared-all'], color=0xEC2E2E)
                        await ctx.channel.send(embed=embed)
                        print(now_time(), str(member), Lang[server_data['language'][str(ctx.guild.id)]]['warn-cleared-all'], Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def cd(ctx):
    if server_data['commands'][str(ctx.guild.id)]['cd']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            await ctx.channel.delete()
            print(now_time(), ctx.channel, Lang[server_data['language'][str(ctx.guild.id)]]['channel-deleted'], Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def ci(ctx):
    if server_data['commands'][str(ctx.guild.id)]['ci']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            await ctx.message.delete()
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False, view_channel=False)
            await ctx.send(Lang[server_data['language'][str(ctx.guild.id)]]['channel-invisibled'])
            print(now_time(), ctx.channel, Lang[server_data['language'][str(ctx.guild.id)]]['channel-invisibled'], Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def exit(ctx):
    if server_data['commands'][str(ctx.guild.id)]['exit']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            if ctx.author.id != data['owner-id']:
                await ctx.send(Lang[server_data['language'][str(ctx.guild.id)]]['not-owner'], delete_after=3)
                return
            reset_confirm = await ctx.reply(Lang[server_data['language'][str(ctx.guild.id)]]['RESET-confirm'], components = [ActionRow(
                    Button(label=Lang[server_data['language'][str(ctx.guild.id)]]['RESET-confirm-button'], style='3', custom_id='confirm'),
                    Button(label=Lang[server_data['language'][str(ctx.guild.id)]]['RESET-cancel-button'], style='4', custom_id='cancel')
            )])
            interaction = await bot.wait_for('button_click', check = lambda inter: inter.user == ctx.author)
            res = interaction.custom_id
            if res == 'confirm':
                await reset_confirm.delete()
                await interaction.send(Lang[server_data['language'][str(ctx.guild.id)]]['RESET-resetted'])
                sys.exit()
            else:
                await reset_confirm.delete()
                await interaction.send(Lang[server_data['language'][str(ctx.guild.id)]]['RESET-canceled'])
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def gay(ctx, member: discord.Member=None):
    if server_data['commands'][str(ctx.guild.id)]['gay']:
        if member == None:
            embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'gay '+Lang[server_data['language'][str(ctx.guild.id)]]['@user'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed, delete_after=5)
            await asyncio.sleep(5)
            await ctx.message.delete()
        else:
            gay = str(random.randrange(101))+'% gay'
            embed = discord.Embed(title=gay, color=0x4b49d8)
            embed.set_author(name=member, icon_url=member.avatar_url)
            await ctx.channel.send(embed=embed, delete_after=5)
            print(now_time() ,member, gay)
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def kick(ctx, user: discord.Member=None, options='None', *, reason='None'):
    if server_data['commands'][str(ctx.guild.id)]['kick']:
        ctx_sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        ctx_sha1.update(str(ctx.author.id).encode('utf-8'))
        await ctx.message.delete()
        if not user:
            embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'kick '+Lang[server_data['language'][str(ctx.guild.id)]]['@user']+Lang[server_data['language'][str(ctx.guild.id)]]['reason'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed, delete_after=5)
        elif options == '--sync' and ctx.author.id == data['owner-id']:
            embed=discord.Embed(title=str(user)+Lang[server_data['language'][str(ctx.guild.id)]]['user-kicked'], description=Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason']+reason, color=0x81FA28)
            try:
                await user.send(embed=embed)
            except: ...
            await ctx.guild.kick(user, reason=reason)
            await ctx.channel.send(embed=embed)
            print(now_time(), str(user), Lang[server_data['language'][str(ctx.guild.id)]]['user-kicked'], Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason'], reason, Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
        elif ctx.author.guild_permissions.administrator or str(ctx_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            salt(user.id)
            user_sha1 = hashlib.sha1(user_salt[str(user.id)].encode('utf-8'))
            user_sha1.update(str(user.id).encode('utf-8'))
            if str(user_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('bypass')][str(ctx.guild.id)].values()) or user.guild_permissions.administrator:
                await error_code.bypass(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
            else:
                embed=discord.Embed(title=str(user)+Lang[server_data['language'][str(ctx.guild.id)]]['user-kicked'], description=Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason']+options, color=0x81FA28)
                try:
                    await user.send(embed=embed)
                except: ...
                await ctx.guild.kick(user, reason=options)
                await ctx.channel.send(embed=embed)
                print(now_time(), str(user), Lang[server_data['language'][str(ctx.guild.id)]]['user-kicked'], Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason'], options, Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def mute(ctx, user: discord.Member=None, options='None', *, reason='None'):
    if server_data['commands'][str(ctx.guild.id)]['mute']:
        ctx_sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        ctx_sha1.update(str(ctx.author.id).encode('utf-8'))
        if not user:
            embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'mute '+Lang[server_data['language'][str(ctx.guild.id)]]['@user']+Lang[server_data['language'][str(ctx.guild.id)]]['reason'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed, delete_after=5)
        elif options == '--sync' and ctx.author.id == data['owner-id']:
            guild = ctx.guild
            mutedRole = discord.utils.get(guild.roles, name=Lang[server_data['language'][str(ctx.guild.id)]]['mute-role-name'])
            all_roles = await guild.fetch_roles()
            num_roles = len(all_roles)
            if not mutedRole:
                mutedRole = await guild.create_role(name=Lang[server_data['language'][str(ctx.guild.id)]]['mute-role-name'])
                await mutedRole.edit(position=num_roles - 2)
                for channel in guild.channels:
                    await channel.set_permissions(mutedRole, speak=False, send_messages=False)
            await user.add_roles(mutedRole, reason=reason)
            embed=discord.Embed(title=str(user)+Lang[server_data['language'][str(ctx.guild.id)]]['user-muted'], description=Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason']+reason, color=0x81FA28)
            await ctx.channel.send(embed=embed)
            await user.send(embed=embed)
            print(now_time(), str(user), Lang[server_data['language'][str(ctx.guild.id)]]['user-muted'], Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason'], reason, Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
        elif ctx.author.guild_permissions.administrator or str(ctx_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            salt(user.id)
            user_sha1 = hashlib.sha1(user_salt[str(user.id)].encode('utf-8'))
            user_sha1.update(str(user.id).encode('utf-8'))
            if str(user_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('bypass')][str(ctx.guild.id)].values()) or user.guild_permissions.administrator:
                await error_code.bypass(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
            else:
                mutedRole = discord.utils.get(ctx.guild.roles, name=Lang[server_data['language'][str(ctx.guild.id)]]['mute-role-name'])
                all_roles = await ctx.guild.fetch_roles()
                num_roles = len(all_roles)
                if not mutedRole:
                    mutedRole = await ctx.guild.create_role(name=Lang[server_data['language'][str(ctx.guild.id)]]['mute-role-name'])
                    await mutedRole.edit(position=num_roles - 2)
                    for channel in ctx.guild.channels:
                        await channel.set_permissions(mutedRole, speak=False, send_messages=False)
                await user.add_roles(mutedRole, reason=options)
                embed=discord.Embed(title=str(user)+Lang[server_data['language'][str(ctx.guild.id)]]['user-muted'], description=Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason']+options, color=0x81FA28)
                await ctx.channel.send(embed=embed)
                await user.send(embed=embed)
                print(now_time(), str(user), Lang[server_data['language'][str(ctx.guild.id)]]['user-muted'], Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason'], options, Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def ping(ctx, ip: str='', options=''):
    if server_data['commands'][str(ctx.guild.id)]['ping']:
        if ip == '':
            embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'ping [IP]', color=0xEC2E2E)
            await ctx.channel.send(embed=embed, delete_after=5)
        else:
            TTL = str(random.randrange(50, 200))
            suc = fail = ms = 0
            ping_list = []
            info = ''
            if options == '-a':
                for i in range(4):
                    response = pin(ip)
                    if response:
                        host_ip = socket.gethostbyname(ip)
                        delay = str(int(response*1000))+'ms'
                        ping_list.append(delay)
                        info += Lang[server_data['language'][str(ctx.guild.id)]]['reply_from']+host_ip+Lang[server_data['language'][str(ctx.guild.id)]]['bytes_time']+delay+' TTL='+TTL+'\n'
                        await asyncio.sleep(response)
                        suc += 1
                        ms += int(response*1000)
                    else:
                        try:
                            host_ip = socket.gethostbyname(ip)
                        except:
                            host_ip = ''
                        info += Lang[server_data['language'][str(ctx.guild.id)]]['ping-timeout']+'\n'
                        ping_list.append('N/A')
                        fail += 1
                ping_list.sort()
                embed = discord.Embed(title='Ping '+ip+' ['+host_ip+']: '+Lang[server_data['language'][str(ctx.guild.id)]]['with_32_bytes']+':', description=info, color=0x00AAAA)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['ping_stat'], value=Lang[server_data['language'][str(ctx.guild.id)]]['packet']+str(suc)+Lang[server_data['language'][str(ctx.guild.id)]]['lost']+str(fail)+' ('+str(int(fail/4*100))+Lang[server_data['language'][str(ctx.guild.id)]]['lost_%']+')', inline=False)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['round_trip_times'], value=Lang[server_data['language'][str(ctx.guild.id)]]['minimum']+ping_list[0]+Lang[server_data['language'][str(ctx.guild.id)]]['maximum']+ping_list[-1]+Lang[server_data['language'][str(ctx.guild.id)]]['average']+str(int(ms/4))+'ms', inline=False)
                await ctx.send(embed=embed)
            else:
                response = pin(ip)
                if response:
                    host_ip = socket.gethostbyname(ip)
                    delay = str(int(response*1000))+'ms'
                    info += Lang[server_data['language'][str(ctx.guild.id)]]['reply_from']+host_ip+Lang[server_data['language'][str(ctx.guild.id)]]['bytes_time']+delay+' TTL='+TTL+'\n'
                    embed = discord.Embed(title='Ping '+ip+' ['+host_ip+']: '+Lang[server_data['language'][str(ctx.guild.id)]]['with_32_bytes']+':', description=info, color=0x00AAAA)
                    await ctx.send(embed=embed)
                else:
                    try:
                        host_ip = socket.gethostbyname(ip)
                    except:
                        host_ip = ''
                    delay = Lang[server_data['language'][str(ctx.guild.id)]]['ping-timeout']
                    embed = discord.Embed(title='Ping '+ip+' ['+host_ip+']: '+Lang[server_data['language'][str(ctx.guild.id)]]['with_32_bytes']+':', description=delay, color=0x00AAAA)
                    await ctx.send(embed=embed)
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def RESET(ctx):
    if data['command-reset']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            if ctx.author.id != data['owner-id']:
                await ctx.send(Lang[server_data['language'][str(ctx.guild.id)]]['not-owner'], delete_after=3)
                return
            if not data['debug-mode']:
                await ctx.send(Lang[server_data['language'][str(ctx.guild.id)]]['reset-error'], delete_after=3)
                return
            else:
                reset_confirm = await ctx.reply(Lang[server_data['language'][str(ctx.guild.id)]]['RESET-confirm'], components = [ActionRow(
                    Button(label=Lang[server_data['language'][str(ctx.guild.id)]]['RESET-confirm-button'], style='3', custom_id='confirm'),
                    Button(label=Lang[server_data['language'][str(ctx.guild.id)]]['RESET-cancel-button'], style='4', custom_id='cancel')
                )])
                interaction = await bot.wait_for('button_click', check = lambda inter: inter.user == ctx.author)
                res = interaction.custom_id
                if res == 'confirm':
                    await reset_confirm.delete()
                    await interaction.send(Lang[server_data['language'][str(ctx.guild.id)]]['RESET-resetted'])
                    reset.reset_config()
                    sys.exit()
                else:
                    await reset_confirm.delete()
                    await interaction.send(Lang[server_data['language'][str(ctx.guild.id)]]['RESET-canceled'])
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
        
@bot.command()
async def reload(ctx):
    global data, prefix
    if server_data['commands'][str(ctx.guild.id)]['reload']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            await ctx.message.delete()
            add_lang()
            load_userdata()
            load_serverdata()
            data = json.load(open('config.json'))
            self_test.check_config()
            match data['custom-activity']:
                case 'playing':
                    activity = discord.Game(data['activity-name']) if data['activity-name'] != '' else discord.Game(name=prefix+"menu")
                case 'streaming':
                    activity = discord.Streaming(name=data['activity-name'], url=data['activity-streaming-url']) if data['activity-name'] != '' else discord.Streaming(name=prefix+"menu", url=data['activity-streaming-url'])
                case 'listening':
                    activity = discord.Activity(type=discord.ActivityType.listening, name=data['activity-name']) if data['activity-name'] != '' else discord.Activity(type=discord.ActivityType.listening, name=prefix+"menu")
                case 'watching':
                    activity = discord.Activity(type=discord.ActivityType.watching, name=data['activity-name']) if data['activity-name'] != '' else discord.Activity(type=discord.ActivityType.watching, name=prefix+"menu")
            match data['custom-status']: 
                case 'offline':
                    await bot.change_presence(status=discord.Status.offline, activity=activity)
                case 'idle':
                    await bot.change_presence(status=discord.Status.idle, activity=activity)
                case 'dnd':
                    await bot.change_presence(status=discord.Status.dnd, activity=activity)
                case 'invisible':
                    await bot.change_presence(status=discord.Status.invisible, activity=activity)
                case _:
                    await bot.change_presence(status=discord.Status.online, activity=activity)
            try:
                embed = discord.Embed(title='🔄｜'+Lang[server_data['language'][str(ctx.guild.id)]]['reloaded'], color=0x81FA28)
                await ctx.channel.send(embed=embed)
                print(now_time(), Lang[server_data['language'][str(ctx.guild.id)]]['reloaded'], Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
            except:
                print(now_time(), 'Could not pass language setting, end the bot!')
                embed = discord.Embed(title='⚠｜ Could not pass language setting, end the bot!', color=0xEC2E2E)
                await ctx.send(embed=embed)
                self_test.error()
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def removeadmin(ctx, user: discord.Member=None):
    if server_data['commands'][str(ctx.guild.id)]['removeadmin']:
        if ctx.author.guild_permissions.administrator:
            if not user:
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'removeadmin '+Lang[server_data['language'][str(ctx.guild.id)]]['@user'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed, delete_after=5)
            else:
                userdata_dict = {}
                try:
                    sha512= hashlib.sha512()
                    sha512.update(str(user).encode('utf-8'))
                    del user_data['admin'][str(ctx.guild.id)][str(sha512.hexdigest())]
                    for i in range(len(userdata_keys)):
                        userdata_dict[userdata_keys[i]] = userdata_values[i]
                    with open("database/userdata.json", "w") as userdata_file:
                        json.dump(userdata_dict, userdata_file, indent = 4)
                    load_userdata()
                    embed=discord.Embed(title=str(user)+Lang[server_data['language'][str(ctx.guild.id)]]['admin-removed'], color=0x81FA28)
                    await ctx.channel.send(embed=embed)
                    print(now_time(), str(user)+Lang[server_data['language'][str(ctx.guild.id)]]['admin-removed'], Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
                except:
                    embed=discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['not-in-admin'], color=0xEC2E2E)
                    await ctx.channel.send(embed=embed)      
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def removebypass(ctx, user: discord.Member=None):
    if server_data['commands'][str(ctx.guild.id)]['removebypass']:
        if ctx.author.guild_permissions.administrator:
            if not user:
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'removebypass '+Lang[server_data['language'][str(ctx.guild.id)]]['@user'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed, delete_after=5)
            else:
                userdata_dict = {}
                try:
                    sha512= hashlib.sha512()
                    sha512.update(str(user).encode('utf-8'))
                    del user_data['bypass'][str(ctx.guild.id)][str(sha512.hexdigest())]
                    for i in range(len(userdata_keys)):
                        userdata_dict[userdata_keys[i]] = userdata_values[i]
                    with open("database/userdata.json", "w") as userdata_file:
                        json.dump(userdata_dict, userdata_file, indent = 4)
                    load_userdata()
                    embed=discord.Embed(title=str(user)+Lang[server_data['language'][str(ctx.guild.id)]]['bypass-removed'], color=0x81FA28)
                    await ctx.channel.send(embed=embed)
                    print(now_time(), str(user)+Lang[server_data['language'][str(ctx.guild.id)]]['bypass-removed'], Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
                except:
                    embed=discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['not-in-bypass'], color=0xEC2E2E)
                    await ctx.channel.send(embed=embed)
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def showwarn(ctx, member: discord.Member=None):
    if server_data['commands'][str(ctx.guild.id)]['showwarn']:
        ctx_sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        ctx_sha1.update(str(ctx.author.id).encode('utf-8'))
        member_sha1 = hashlib.sha1(user_salt[str(member.id)].encode('utf-8'))
        member_sha1.update(str(member.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(ctx_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            if not member:
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'showwarn '+Lang[server_data['language'][str(ctx.guild.id)]]['@user'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed, delete_after=5)
            else:
                embed = discord.Embed(title=member.name+Lang[server_data['language'][str(ctx.guild.id)]]['warn-amount']+user_data['warns'][str(ctx.guild.id)][str(member_sha1.hexdigest())], color=0xEC2E2E)
                await ctx.channel.send(embed=embed)
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def slowmode(ctx, seconds: int=0):
    if server_data['commands'][str(ctx.guild.id)]['slowmode']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            await ctx.channel.edit(slowmode_delay=seconds)
            embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['slowmode-message']+str(seconds)+Lang[server_data['language'][str(ctx.guild.id)]]['slowmode-seconds'], color=0xEC2E2E)
            await ctx.send(embed=embed) 
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def send(ctx, user: discord.Member=None, *, message=''):
    if server_data['commands'][str(ctx.guild.id)]['send']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        await ctx.message.delete()
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            if message == '':
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'send '+Lang[server_data['language'][str(ctx.guild.id)]]['message'], color=0xEC2E2E)
            else:
                try:
                    await user.send(message)
                except:
                    embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['send-fail'], description=Lang[server_data['language'][str(ctx.guild.id)]]['send-fail-reason'], color=0xEC2E2E)
                else:
                    embed = discord.Embed(title='📨｜'+Lang[server_data['language'][str(ctx.guild.id)]]['send-success'], color=0x81FA28)
            await ctx.channel.send(embed=embed, delete_after=5)
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def add(ctx, options: str='', *, id: str=''):
    if server_data['commands'][str(ctx.guild.id)]['add']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            if options == '':
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], color=0xEC2E2E)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-picture-only-channel'], value=prefix+'add picture-only-channel'+Lang[server_data['language'][str(ctx.guild.id)]]['channel']+' ...', inline=False)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-chat-filter'], value=prefix+'add chat-filter'+Lang[server_data['language'][str(ctx.guild.id)]]['regex'], inline=False)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-enter-voice-channel'], value=prefix+'add enter-voice-channel'+Lang[server_data['language'][str(ctx.guild.id)]]['channel']+' ...', inline=False)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-voice-category'], value=prefix+'add voice-category'+Lang[server_data['language'][str(ctx.guild.id)]]['category'], inline=False)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-reaction-roles'], value=prefix+'add reaction-roles'+Lang[server_data['language'][str(ctx.guild.id)]]['reaction']+Lang[server_data['language'][str(ctx.guild.id)]]['role'], inline=False)
                await ctx.channel.send(embed=embed)
                return
            if options == 'chat-filter':
                if id == 'default':
                    shutil.copy('database/chatfilter/DEFAULT.txt', 'database/chatfilter/'+str(ctx.guild.id)+'.txt')
                    with open('database/chatfilter/'+str(ctx.guild.id)+'.txt', "r", encoding = "utf8") as words:
                        badwords = words.read().split()
                    id = ''
                    for i in badwords:
                        id += i+'\n'
                else:
                    with open('database/chatfilter/'+str(ctx.guild.id)+'.txt', "r", encoding = "utf8") as words:
                        badwords = words.read().split()
                    if ' ' in ctx.message.content:
                        temp = re.split('\s', id)
                        content = ''
                        for word in temp:
                            content += f'({word})\s'
                        id = content[0:-2]
                    if id not in badwords:
                        with open('database/chatfilter/'+str(ctx.guild.id)+'.txt', "a", encoding = "utf8") as words:
                            words.write(f'{id}\n')
                embed = discord.Embed(title='✅｜'+Lang[server_data['language'][str(ctx.guild.id)]]['add-chat-filter'], description=f'`{id}`', color=0x81FA28)
                if server_data['chat-filter-action'][str(ctx.guild.id)] == 'None':
                    embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['add-chat-filter-next'], value=prefix+'set chat-filter-action'+Lang[server_data['language'][str(ctx.guild.id)]]['action'], inline=False)
                print(now_time(), Lang[server_data['language'][str(ctx.guild.id)]]['add-chat-filter'], id)
                await ctx.channel.send(embed=embed)
                return
            serverdata_dict = {}
            for i in range(len(serverdata_keys)):
                serverdata_dict[serverdata_keys[i]] = serverdata_values[i]
            if options == 'picture-only-channel':
                serverdata_values_dict = serverdata_values[serverdata_keys.index('picture-only-channel')]
                picture_only_channel_list = serverdata_values_dict[str(ctx.guild.id)]
                id_regex = re.compile('\d{18}')
                id_match_word = id_regex.findall(id)
                channels = ''
                for i in id_match_word:
                    if int(i) not in picture_only_channel_list:
                        picture_only_channel_list.append(int(i))
                        channels += str(discord.utils.get(ctx.guild.channels, id= int(i)))+'\n'
                serverdata_values_dict[str(ctx.guild.id)] = picture_only_channel_list
                serverdata_dict['picture-only-channel'] = serverdata_values_dict
                embed = discord.Embed(title='✅｜'+Lang[server_data['language'][str(ctx.guild.id)]]['add-picture-only-channel'], description=channels, color=0x81FA28)
                print(now_time(), Lang[server_data['language'][str(ctx.guild.id)]]['add-picture-only-channel'], '\n', channels)
            if options == 'enter-voice-channel':
                serverdata_values_dict = serverdata_values[serverdata_keys.index('enter-voice-channel')]
                enter_voice_channel_list = serverdata_values_dict[str(ctx.guild.id)]
                id_regex = re.compile('\d{18}')
                id_match_word = id_regex.findall(id)
                channels = ''
                for i in id_match_word:
                    if int(i) not in enter_voice_channel_list:
                        enter_voice_channel_list.append(int(i))
                        channels += str(discord.utils.get(ctx.guild.channels, id= int(i)))+'\n'
                serverdata_values_dict[str(ctx.guild.id)] = enter_voice_channel_list
                serverdata_dict['enter-voice-channel'] = serverdata_values_dict
                embed = discord.Embed(title='✅｜'+Lang[server_data['language'][str(ctx.guild.id)]]['add-enter-voice-channel'], description=channels, color=0x81FA28)
                if server_data['voice-category'][str(ctx.guild.id)] == []:
                    embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['add-enter-voice-channel-next'], value=prefix+'add voice-category'+Lang[server_data['language'][str(ctx.guild.id)]]['category'], inline=False)
                print(now_time(), Lang[server_data['language'][str(ctx.guild.id)]]['add-enter-voice-channel'], '\n', channels)
            if options == 'voice-category':
                serverdata_values_dict = serverdata_values[serverdata_keys.index('voice-category')]
                voice_category_list = serverdata_values_dict[str(ctx.guild.id)]
                id_regex = re.compile('\d{18}')
                id_match_word = id_regex.findall(id)
                channels = ''
                for i in range(len(id_match_word)):
                    if int(id_match_word[0]) not in voice_category_list:
                        voice_category_list.append(int(id_match_word[0]))
                        channels += str(discord.utils.get(ctx.guild.channels, id= int(id_match_word[0])))+'\n'
                serverdata_values_dict[str(ctx.guild.id)] = voice_category_list
                serverdata_dict['voice-category'] = serverdata_values_dict
                embed = discord.Embed(title='✅｜'+Lang[server_data['language'][str(ctx.guild.id)]]['add-voice-category'], description=channels, color=0x81FA28)
                print(now_time(), Lang[server_data['language'][str(ctx.guild.id)]]['add-voice-category'], '\n', channels)
            if options == 'reaction-roles':
                serverdata_values_dict = serverdata_values[serverdata_keys.index('reaction-roles')]
                temp = [i for i in re.split('\s', id) if i != '']
                try:
                    role = discord.utils.get(ctx.guild.roles, id=int(temp[-1][3:-1]))
                    if not role or len(temp) != 2:
                        raise
                    if role.position >= ctx.guild.get_member(bot.user.id).top_role.position:
                        embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['add-reaction-roles-highest'], color=0xEC2E2E)
                        await ctx.reply(embed=embed)
                        return
                except:
                    embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['add-reaction-roles-error'], color=0xEC2E2E)
                    await ctx.reply(embed=embed)
                    return
                serverdata_new_dict = serverdata_values_dict[str(ctx.guild.id)]
                serverdata_new_dict[temp[0]] = temp[-1]
                serverdata_dict['reaction-roles'][str(ctx.guild.id)] = serverdata_new_dict
                embed = discord.Embed(title='✅｜'+Lang[server_data['language'][str(ctx.guild.id)]]['add-reaction-roles'], description=temp[0]+' : '+temp[-1], color=0x81FA28)
                print(now_time(), Lang[server_data['language'][str(ctx.guild.id)]]['add-reaction-roles'], '\n', temp[0], temp[-1])
            with open("database/serverdata.json", "w") as serverdata_file:
                json.dump(serverdata_dict, serverdata_file, indent = 4)
            load_serverdata()
            await ctx.channel.send(embed=embed)
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def remove(ctx, options: str='', *, id: str=''):
    if server_data['commands'][str(ctx.guild.id)]['remove']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            if options == '':
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], color=0xEC2E2E)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-picture-only-channel'], value=prefix+'remove picture-only-channel'+Lang[server_data['language'][str(ctx.guild.id)]]['channel']+' ...', inline=False)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-chat-filter'], value=prefix+'remove chat-filter'+Lang[server_data['language'][str(ctx.guild.id)]]['regex'], inline=False)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-enter-voice-channel'], value=prefix+'remove enter-voice-channel'+Lang[server_data['language'][str(ctx.guild.id)]]['channel']+' ...', inline=False)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-voice-category'], value=prefix+'remove voice-category'+Lang[server_data['language'][str(ctx.guild.id)]]['category'], inline=False)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-reaction-roles'], value=prefix+'remove reaction-roles'+Lang[server_data['language'][str(ctx.guild.id)]]['reaction'], inline=False)
                await ctx.channel.send(embed=embed)
                return
            if options == 'chat-filter':
                with open('database/chatfilter/'+str(ctx.guild.id)+'.txt', "r", encoding = "utf8") as words:
                    badwords = words.read().split()
                if id in badwords:
                    badwords.remove(id)
                    with open('database/chatfilter/'+str(ctx.guild.id)+'.txt', "w", encoding = "utf8") as words:
                        for i in badwords:
                            words.write(f'{i}\n')
                embed = discord.Embed(title='✅｜'+Lang[server_data['language'][str(ctx.guild.id)]]['remove-chat-filter'], description=id, color=0x81FA28)
                print(now_time(), Lang[server_data['language'][str(ctx.guild.id)]]['remove-chat-filter'], id)
                await ctx.channel.send(embed=embed)
                return
            serverdata_dict = {}
            for i in range(len(serverdata_keys)):
                serverdata_dict[serverdata_keys[i]] = serverdata_values[i]
            if options == 'picture-only-channel':
                serverdata_values_dict = serverdata_values[serverdata_keys.index('picture-only-channel')]
                picture_only_channel_list = serverdata_values_dict[str(ctx.guild.id)]
                id_regex = re.compile('\d{18}')
                id_match_word = id_regex.findall(id)
                channels = ''
                for i in id_match_word:
                    if int(i) in picture_only_channel_list:
                        picture_only_channel_list.remove(int(i))
                        channels += str(discord.utils.get(ctx.guild.channels, id= int(i)))+'\n'
                serverdata_values_dict[str(ctx.guild.id)] = picture_only_channel_list
                serverdata_dict['picture-only-channel'] = serverdata_values_dict
                embed = discord.Embed(title='✅｜'+Lang[server_data['language'][str(ctx.guild.id)]]['remove-picture-only-channel'], description=channels, color=0xEC2E2E)
                print(now_time(), Lang[server_data['language'][str(ctx.guild.id)]]['remove-picture-only-channel'], '\n', channels)
            if options == 'enter-voice-channel':
                serverdata_values_dict = serverdata_values[serverdata_keys.index('enter-voice-channel')]
                enter_voice_channel_list = serverdata_values_dict[str(ctx.guild.id)]
                id_regex = re.compile('\d{18}')
                id_match_word = id_regex.findall(id)
                channels = ''
                for i in id_match_word:
                    if int(i) in enter_voice_channel_list:
                        enter_voice_channel_list.remove(int(i))
                        channels += str(discord.utils.get(ctx.guild.channels, id= int(i)))+'\n'
                serverdata_values_dict[str(ctx.guild.id)] = enter_voice_channel_list
                serverdata_dict['enter-voice-channel'] = serverdata_values_dict
                embed = discord.Embed(title='✅｜'+Lang[server_data['language'][str(ctx.guild.id)]]['remove-enter-voice-channel'], description=channels, color=0xEC2E2E)
                print(now_time(), Lang[server_data['language'][str(ctx.guild.id)]]['remove-enter-voice-channel'], '\n', channels)
            if options == 'voice-category':
                serverdata_values_dict = serverdata_values[serverdata_keys.index('voice-category')]
                voice_category_list = serverdata_values_dict[str(ctx.guild.id)]
                id_regex = re.compile('\d{18}')
                id_match_word = id_regex.findall(id)
                channels = ''
                for i in id_match_word:
                    if int(i) in voice_category_list:
                        channels += str(discord.utils.get(ctx.guild.channels, id= int(i)))+'\n'
                serverdata_values_dict[str(ctx.guild.id)] = []
                serverdata_dict['voice-category'] = serverdata_values_dict
                embed = discord.Embed(title='✅｜'+Lang[server_data['language'][str(ctx.guild.id)]]['remove-voice-category'], description=channels, color=0x81FA28)
                print(now_time(), Lang[server_data['language'][str(ctx.guild.id)]]['remove-voice-category'], '\n', channels)
            if options == 'reaction-roles':
                serverdata_dict = server_data
                role = serverdata_dict['reaction-roles'][str(ctx.guild.id)][id]
                del serverdata_dict['reaction-roles'][str(ctx.guild.id)][id]
                embed = discord.Embed(title='✅｜'+Lang[server_data['language'][str(ctx.guild.id)]]['remove-reaction-roles'], description=id+' : '+role, color=0x81FA28)
                print(now_time(), Lang[server_data['language'][str(ctx.guild.id)]]['remove-reaction-roles'], '\n', id, role)
            with open("database/serverdata.json", "w") as serverdata_file:
                json.dump(serverdata_dict, serverdata_file, indent = 4)
            load_serverdata()
            await ctx.channel.send(embed=embed)
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def check(ctx, options: str=''):
    if server_data['commands'][str(ctx.guild.id)]['check']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            if options == 'chat-filter':
                with open('database/chatfilter/'+str(ctx.guild.id)+'.txt', "r", encoding = "utf8") as words:
                    badwords = words.read().split()
                word = ''
                for i in range(len(badwords)):
                    word += badwords[i]+'\n'
                embed = discord.Embed(title='💬｜'+Lang[server_data['language'][str(ctx.guild.id)]]['chat-filter-info'], description=f'`{word}`', color=0x81FA28)
            elif options == 'picture-only-channel':
                serverdata_values_dict = serverdata_values[serverdata_keys.index('picture-only-channel')]
                picture_only_channel_list = serverdata_values_dict[str(ctx.guild.id)]
                channels = ''
                for i in picture_only_channel_list:
                    channels += str(i)+' : '+str(discord.utils.get(ctx.guild.channels, id= i))+'\n'
                embed = discord.Embed(title='📎｜'+Lang[server_data['language'][str(ctx.guild.id)]]['picture-only-channel-info'], description=channels, color=0x81FA28)
            elif options == 'private-voice-channel':
                serverdata_values_dict = serverdata_values[serverdata_keys.index('enter-voice-channel')]
                enter_voice_channel_list = serverdata_values_dict[str(ctx.guild.id)]
                channels = ''
                for i in enter_voice_channel_list:
                    channels += str(i)+' : '+str(discord.utils.get(ctx.guild.channels, id= i))+'\n'
                serverdata_values_dict = serverdata_values[serverdata_keys.index('voice-category')]
                voice_category_list = serverdata_values_dict[str(ctx.guild.id)]
                embed = discord.Embed(title='🔊｜'+Lang[server_data['language'][str(ctx.guild.id)]]['private-voice-channel-info'], description=channels, color=0x81FA28)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['private-voice-channel-category-info'], value=str(voice_category_list[0])+' : '+str(discord.utils.get(ctx.guild.channels, id= voice_category_list[0]))+'\n', inline=False)
            elif options == 'auto-action':
                serverdata_values_dict = serverdata_values[serverdata_keys.index('auto-action')]
                auto_action_list = serverdata_values_dict[str(ctx.guild.id)]
                embed = discord.Embed(title='🛠｜'+Lang[server_data['language'][str(ctx.guild.id)]]['auto-action-info'], description=Lang[server_data['language'][str(ctx.guild.id)]]['set-auto-mute']+str(auto_action_list[0])+Lang[server_data['language'][str(ctx.guild.id)]]['set-auto-kick']+str(auto_action_list[1])+Lang[server_data['language'][str(ctx.guild.id)]]['set-auto-ban']+str(auto_action_list[2]), color=0x81FA28)
            else:
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], color=0xEC2E2E)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['check-chat-filter'], value=prefix+'check chat-filter', inline=False)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['check-picture-only-channel'], value=prefix+'check picture-only-channel', inline=False)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['check-private-voice-channel'], value=prefix+'check private-voice-channel', inline=False)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['check-auto-action'], value=prefix+'check auto-action', inline=False)
            await ctx.channel.send(embed=embed)
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def set(ctx, options: str='', content: str='', TF: str=''):
    if server_data['commands'][str(ctx.guild.id)]['set']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            if options == '':
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], color=0xEC2E2E)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-auto-action'], value=prefix+'set auto-action'+Lang[server_data['language'][str(ctx.guild.id)]]['count']*3, inline=False)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-chat-filter-action'], value=prefix+'set chat-filter-action'+Lang[server_data['language'][str(ctx.guild.id)]]['action'], inline=False)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-music-bot'], value=prefix+'set music-bot'+Lang[server_data['language'][str(ctx.guild.id)]]['true_or_false'], inline=False)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-commands'], value=prefix+'set commands'+Lang[server_data['language'][str(ctx.guild.id)]]['command']+Lang[server_data['language'][str(ctx.guild.id)]]['true_or_false'], inline=False)
                await ctx.channel.send(embed=embed)
                return
            serverdata_dict = {}
            for i in range(len(serverdata_keys)):
                serverdata_dict[serverdata_keys[i]] = serverdata_values[i]
            if options == 'auto-action':
                serverdata_values_dict = serverdata_values[serverdata_keys.index('auto-action')]
                auto_action_list = []
                count_regex = re.compile('\d{1,}')
                count_match_word = count_regex.findall(content)
                for i in count_match_word:
                    if len(auto_action_list) <=2:
                        auto_action_list.append(int(i))
                if len(auto_action_list) == 1:
                    auto_action_list.append(0)
                    auto_action_list.append(0)
                elif len(auto_action_list) == 2:
                    auto_action_list.append(0)
                if auto_action_list[1] <= auto_action_list[0] and auto_action_list[1] != 0:
                    embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['add-auto-action-error-1'], color=0xEC2E2E)
                    await ctx.channel.send(embed=embed)
                    return
                elif auto_action_list[2] <= auto_action_list[1] and auto_action_list[2] != 0:
                    embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['add-auto-action-error-2'], color=0xEC2E2E)
                    await ctx.channel.send(embed=embed)
                    return
                serverdata_values_dict[str(ctx.guild.id)] = auto_action_list
                serverdata_dict['auto-action'] = serverdata_values_dict
                auto_action = Lang[server_data['language'][str(ctx.guild.id)]]['set-auto-mute']+str(auto_action_list[0])+Lang[server_data['language'][str(ctx.guild.id)]]['set-auto-kick']+str(auto_action_list[1])+Lang[server_data['language'][str(ctx.guild.id)]]['set-auto-ban']+str(auto_action_list[2])
                embed = discord.Embed(title='✅｜'+Lang[server_data['language'][str(ctx.guild.id)]]['add-auto-action'], description=auto_action ,color=0x81FA28)
                print(now_time(), Lang[server_data['language'][str(ctx.guild.id)]]['add-auto-action'], auto_action_list[0], auto_action_list[1], auto_action_list[2])
            elif options == 'chat-filter-action':
                serverdata_values_dict = serverdata_values[serverdata_keys.index('chat-filter-action')]
                match content:
                    case 'warn':
                        serverdata_values_dict[str(ctx.guild.id)] = 'warn'
                    case 'mute':
                        serverdata_values_dict[str(ctx.guild.id)] = 'mute'
                    case 'kick':
                        serverdata_values_dict[str(ctx.guild.id)] = 'kick'
                    case 'ban':
                        serverdata_values_dict[str(ctx.guild.id)] = 'ban'
                    case _:
                        content = 'None'
                        serverdata_values_dict[str(ctx.guild.id)] = 'None'
                serverdata_dict['chat-filter-action'] = serverdata_values_dict
                embed = discord.Embed(title='✅｜'+Lang[server_data['language'][str(ctx.guild.id)]]['add-chat-filter-action'], description=content ,color=0x81FA28)
                print(now_time(), Lang[server_data['language'][str(ctx.guild.id)]]['add-chat-filter-action'], content)
            elif options == 'music-bot':
                if content == 'true' or content == 'True':
                    enable = True
                elif content == 'false' or content == 'False':
                    enable = False
                else:
                    embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], color=0xEC2E2E)
                    embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-music-bot'], value=prefix+'set music-bot'+Lang[server_data['language'][str(ctx.guild.id)]]['true_or_false'], inline=False)
                    await ctx.channel.send(embed=embed)
                    return
                serverdata_values_dict = serverdata_values[serverdata_keys.index('music-bot')]
                serverdata_values_dict[str(ctx.guild.id)] = enable
                serverdata_dict['music-bot'] = serverdata_values_dict
                embed = discord.Embed(title='✅｜'+Lang[server_data['language'][str(ctx.guild.id)]]['set-music-bot-true'], color=0x81FA28) if enable else discord.Embed(title='✅｜'+Lang[server_data['language'][str(ctx.guild.id)]]['set-music-bot-false'], color=0xEC2E2E)    
            elif options == 'commands':
                if content not in list(serverdata_values[serverdata_keys.index('commands')][str(ctx.guild.id)].keys()):
                    embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['set-command-error'], color=0xEC2E2E)
                else:
                    if TF == 'true' or TF == 'True':
                        enable = True
                    elif TF == 'false' or TF == 'False':
                        enable = False
                    else:
                        embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], color=0xEC2E2E)
                        embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-commands'], value=prefix+'set commands'+Lang[server_data['language'][str(ctx.guild.id)]]['command']+Lang[server_data['language'][str(ctx.guild.id)]]['true_or_false'], inline=False)
                        await ctx.channel.send(embed=embed)
                        return
                    serverdata_values_dict = serverdata_values[serverdata_keys.index('commands')]
                    serverdata_new_dict = serverdata_values_dict[str(ctx.guild.id)]
                    serverdata_new_dict[content] = enable
                    serverdata_dict['commands'][str(ctx.guild.id)] = serverdata_new_dict
                    embed = discord.Embed(title=content+Lang[server_data['language'][str(ctx.guild.id)]]['set-command-to']+str(enable), color=0x81FA28) if enable else discord.Embed(title=content+Lang[server_data['language'][str(ctx.guild.id)]]['set-command-to']+str(enable), color=0xEC2E2E)
            with open("database/serverdata.json", "w") as serverdata_file:
                json.dump(serverdata_dict, serverdata_file, indent = 4)
            load_serverdata()
            await ctx.channel.send(embed=embed)
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            serverdata_dict = {}
            for i in range(len(serverdata_keys)):
                serverdata_dict[serverdata_keys[i]] = serverdata_values[i]
            if options != 'commands':
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], color=0xEC2E2E)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-commands'], value=prefix+'set commands'+Lang[server_data['language'][str(ctx.guild.id)]]['command']+Lang[server_data['language'][str(ctx.guild.id)]]['true_or_false'], inline=False)
                await ctx.channel.send(embed=embed)
                return
            elif options == 'commands':
                if content not in list(serverdata_values[serverdata_keys.index('commands')][str(ctx.guild.id)].keys()):
                    embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['set-command-error'], color=0xEC2E2E)
                else:
                    if TF == 'true' or TF == 'True':
                        enable = True
                    elif TF == 'false' or TF == 'False':
                        enable = False
                    else:
                        embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], color=0xEC2E2E)
                        embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['set-commands'], value=prefix+'set commands'+Lang[server_data['language'][str(ctx.guild.id)]]['command']+Lang[server_data['language'][str(ctx.guild.id)]]['true_or_false'], inline=False)
                        await ctx.channel.send(embed=embed)
                        return
                    serverdata_values_dict = serverdata_values[serverdata_keys.index('commands')]
                    serverdata_new_dict = serverdata_values_dict[str(ctx.guild.id)]
                    serverdata_new_dict[content] = enable
                    serverdata_dict['commands'][str(ctx.guild.id)] = serverdata_new_dict
                    embed = discord.Embed(title=content+Lang[server_data['language'][str(ctx.guild.id)]]['set-command-to']+str(enable), color=0x81FA28) if enable else discord.Embed(title=content+Lang[server_data['language'][str(ctx.guild.id)]]['set-command-to']+str(enable), color=0xEC2E2E)
            with open("database/serverdata.json", "w") as serverdata_file:
                json.dump(serverdata_dict, serverdata_file, indent = 4)
            load_serverdata()
            await ctx.channel.send(embed=embed)
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def time(ctx):
    if server_data['commands'][str(ctx.guild.id)]['time']:
        await ctx.reply(now_time(), mention_author=True)
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def tlm(ctx, seconds: int=600, *,  message=''):
    if server_data['commands'][str(ctx.guild.id)]['tlm']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            await ctx.message.delete()
            if message == '':
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'tlm '+Lang[server_data['language'][str(ctx.guild.id)]]['message'], color=0xEC2E2E)
                embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['uses'], value=Lang[server_data['language'][str(ctx.guild.id)]]['temp-message'], inline=False)
                await ctx.channel.send(embed=embed, delete_after=5)
            else:
                await ctx.channel.send(message, delete_after=seconds)
                print(now_time(), ctx.author,Lang[server_data['language'][str(ctx.guild.id)]]['sent-temp-message'],message, Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def tempmute(ctx, user: discord.Member=None, duration='0s', options='None', *, reason='None'):
    if server_data['commands'][str(ctx.guild.id)]['tempmute']:
        ctx_sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        ctx_sha1.update(str(ctx.author.id).encode('utf-8'))
        if not user:
            embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'tempmute '+Lang[server_data['language'][str(ctx.guild.id)]]['@user']+Lang[server_data['language'][str(ctx.guild.id)]]['duration']+Lang[server_data['language'][str(ctx.guild.id)]]['reason'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed, delete_after=5)
        elif options == '--sync' and ctx.author.id == data['owner-id']:
            guild = ctx.guild
            mutedRole = discord.utils.get(guild.roles, name=Lang[server_data['language'][str(ctx.guild.id)]]['mute-role-name'])
            all_roles = await guild.fetch_roles()
            num_roles = len(all_roles)
            if not mutedRole:
                mutedRole = await guild.create_role(name=Lang[server_data['language'][str(ctx.guild.id)]]['mute-role-name'])
                await mutedRole.edit(position=num_roles - 2)
                for channel in guild.channels:
                    await channel.set_permissions(mutedRole, speak=False, send_messages=False)
            await user.add_roles(mutedRole, reason=reason)
            embed=discord.Embed(title=str(user)+Lang[server_data['language'][str(ctx.guild.id)]]['user-tempmuted'], description=Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason']+reason, color=0x81FA28)
            await ctx.channel.send(embed=embed)
            await user.send(embed=embed)
            print(now_time(), str(user), Lang[server_data['language'][str(ctx.guild.id)]]['user-tempmuted'], Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason'], reason, Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
            dur_list = []
            dur_list.append(duration)
            for time in dur_list:
                time_dic = {'d': 0, 'h': 0, 'm': 0, 's': 0}
                for t in 'dhms':
                    if time.find(t) != -1:
                        index = time.find(t)
                        time_dic[t] = time[0:index]
                        time = time[index + 1:]
                uptime = int(time_dic['d']) * 24 * 60 * 60 + int(time_dic['h']) * 3600 + int(time_dic['m']) * 60 + int(time_dic['s'])
            await asyncio.sleep(uptime)
            await user.remove_roles(mutedRole)
        elif ctx.author.guild_permissions.administrator or str(ctx_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            salt(user.id)
            user_sha1 = hashlib.sha1(user_salt[str(user.id)].encode('utf-8'))
            user_sha1.update(str(user.id).encode('utf-8'))
            if str(user_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('bypass')][str(ctx.guild.id)].values()) or user.guild_permissions.administrator:
                await error_code.bypass(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
            else:
                guild = ctx.guild
                mutedRole = discord.utils.get(guild.roles, name=Lang[server_data['language'][str(ctx.guild.id)]]['mute-role-name'])
                all_roles = await guild.fetch_roles()
                num_roles = len(all_roles)
                if not mutedRole:
                    mutedRole = await guild.create_role(name=Lang[server_data['language'][str(ctx.guild.id)]]['mute-role-name'])
                    await mutedRole.edit(position=num_roles - 2)
                    for channel in guild.channels:
                        await channel.set_permissions(mutedRole, speak=False, send_messages=False)
                await user.add_roles(mutedRole, reason=options)
                embed=discord.Embed(title=str(user)+Lang[server_data['language'][str(ctx.guild.id)]]['user-tempmuted'], description=Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason']+options, color=0x81FA28)
                await ctx.channel.send(embed=embed)
                await user.send(embed=embed)
                print(now_time(), str(user), Lang[server_data['language'][str(ctx.guild.id)]]['user-tempmuted'], Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason'], options, Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
                dur_list = []
                dur_list.append(duration)
                for time in dur_list:
                    time_dic = {'d': 0, 'h': 0, 'm': 0, 's': 0}
                    for t in 'dhms':
                        if time.find(t) != -1:
                            index = time.find(t)
                            time_dic[t] = time[0:index]
                            time = time[index + 1:]
                    uptime = int(time_dic['d']) * 24 * 60 * 60 + int(time_dic['h']) * 3600 + int(time_dic['m']) * 60 + int(time_dic['s'])
                await asyncio.sleep(uptime)
                await user.remove_roles(mutedRole)
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def tempban(ctx, user: discord.Member=None, duration='0s', options='None', *, reason='None'):
    if server_data['commands'][str(ctx.guild.id)]['tempban']:
        ctx_sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        ctx_sha1.update(str(ctx.author.id).encode('utf-8'))
        if not user:
            embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'tempban '+Lang[server_data['language'][str(ctx.guild.id)]]['@user']+Lang[server_data['language'][str(ctx.guild.id)]]['duration']+Lang[server_data['language'][str(ctx.guild.id)]]['reason'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed, delete_after=5)
        elif options == '--sync' and ctx.author.id == data['owner-id']:
            embed=discord.Embed(title=str(user)+Lang[server_data['language'][str(ctx.guild.id)]]['user-tempbanned'], description=Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason']+options, color=0x81FA28)
            try:
                await user.send(embed=embed)
            except: ...
            await ctx.guild.ban(user, reason=reason)
            await ctx.channel.send(embed=embed)
            print(now_time(), str(user), Lang[server_data['language'][str(ctx.guild.id)]]['user-tempbanned'], Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason'], options, Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
            dur_list = []
            dur_list.append(duration)
            for time in dur_list:
                time_dic = {'d': 0, 'h': 0, 'm': 0, 's': 0}
                for t in 'dhms':
                    if time.find(t) != -1:
                        index = time.find(t)
                        time_dic[t] = time[0:index]
                        time = time[index + 1:]
                uptime = int(time_dic['d']) * 24 * 60 * 60 + int(time_dic['h']) * 3600 + int(time_dic['m']) * 60 + int(time_dic['s'])
            await asyncio.sleep(uptime)
            await user.unban(user)
        elif ctx.author.guild_permissions.administrator or str(ctx_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            salt(user.id)
            user_sha1 = hashlib.sha1(user_salt[str(user.id)].encode('utf-8'))
            user_sha1.update(str(user.id).encode('utf-8'))
            if str(user_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('bypass')][str(ctx.guild.id)].values()) or user.guild_permissions.administrator:
                await error_code.bypass(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
            else:
                embed=discord.Embed(title=str(user)+Lang[server_data['language'][str(ctx.guild.id)]]['user-tempbanned'], description=Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason']+options, color=0x81FA28)
                try:
                    await user.send(embed=embed)
                except: ...
                await ctx.guild.ban(user, reason=reason)
                await ctx.channel.send(embed=embed)
                print(now_time(), str(user), Lang[server_data['language'][str(ctx.guild.id)]]['user-tempbanned'], Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason'], options, Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
                dur_list = []
                dur_list.append(duration)
                for time in dur_list:
                    time_dic = {'d': 0, 'h': 0, 'm': 0, 's': 0}
                    for t in 'dhms':
                        if time.find(t) != -1:
                            index = time.find(t)
                            time_dic[t] = time[0:index]
                            time = time[index + 1:]
                    uptime = int(time_dic['d']) * 24 * 60 * 60 + int(time_dic['h']) * 3600 + int(time_dic['m']) * 60 + int(time_dic['s'])
                await asyncio.sleep(uptime)
                await user.unban(user)
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def unban(ctx, user: discord.User=None):
    if server_data['commands'][str(ctx.guild.id)]['unban']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        await ctx.message.delete()
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            if not user:
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'unban '+Lang[server_data['language'][str(ctx.guild.id)]]['@user'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed, delete_after=5)
            else:
                try:
                    guild = ctx.guild
                    await guild.unban(user)
                    embed = discord.Embed(title=str(user)+Lang[server_data['language'][str(ctx.guild.id)]]['user-unbanned'])
                    await ctx.channel.send(embed=embed)
                    print(now_time(), str(user), Lang[server_data['language'][str(ctx.guild.id)]]['user-unbanned'], Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
                except:
                    embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['user-not-banned'], color=0xEC2E2E)
                    await ctx.channel.send(embed=embed)
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def unmute(ctx, user: discord.Member=None):
    if server_data['commands'][str(ctx.guild.id)]['unmute']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            if not user:
                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'unmute '+Lang[server_data['language'][str(ctx.guild.id)]]['@user'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed, delete_after=5)
            else:
                mutedRole = discord.utils.get(ctx.guild.roles, name=Lang[server_data['language'][str(ctx.guild.id)]]['mute-role-name'])
                await user.remove_roles(mutedRole)
                embed=discord.Embed(title=str(user)+Lang[server_data['language'][str(ctx.guild.id)]]['user-unmuted'], color=0x81FA28)
                await ctx.channel.send(embed=embed)
                await user.send(embed=embed)
                print(now_time(), str(user), Lang[server_data['language'][str(ctx.guild.id)]]['user-unmuted'], Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def uinfo(ctx, target: discord.Member=None):
    if server_data['commands'][str(ctx.guild.id)]['uinfo']:
        ctx_sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        ctx_sha1.update(str(ctx.author.id).encode('utf-8'))
        await ctx.message.delete()
        if ctx.author.guild_permissions.administrator or str(ctx_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            target = target or ctx.author
            salt(target.id)
            target_sha1 = hashlib.sha1(user_salt[str(target.id)].encode('utf-8'))
            target_sha1.update(str(target.id).encode('utf-8'))
            try:
                amount = user_data['warns'][str(ctx.guild.id)][str(target_sha1.hexdigest())]
            except:
                amount = '0'
            embed = discord.Embed(title='🔍｜'+Lang[server_data['language'][str(ctx.guild.id)]]['user-info'], colour=target.colour, timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=target.avatar_url)
            fields = [(Lang[server_data['language'][str(ctx.guild.id)]]['user-info-name'], str(target), True),
                        (Lang[server_data['language'][str(ctx.guild.id)]]['user-info-nickname'], target.nick, True),
	        			(Lang[server_data['language'][str(ctx.guild.id)]]['user-info-id'], target.id, True),
                        (Lang[server_data['language'][str(ctx.guild.id)]]['user-info-permission'], target.guild_permissions.value, True),
	        			(Lang[server_data['language'][str(ctx.guild.id)]]['user-info-bot'], target.bot, True),
	        			(Lang[server_data['language'][str(ctx.guild.id)]]['user-info-toprole'], target.top_role.mention, True),
                        (Lang[server_data['language'][str(ctx.guild.id)]]['user-info-warn'], amount, True),
	        			(Lang[server_data['language'][str(ctx.guild.id)]]['user-info-status'], str(target.status).title(), True),
	        			(Lang[server_data['language'][str(ctx.guild.id)]]['user-info-activity'], f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} {target.activity.name if target.activity else ''}", True),
                        (Lang[server_data['language'][str(ctx.guild.id)]]['user-info-create-at'], target.created_at.strftime("%Y/%m/%d %H:%M:%S"), True),
                        (Lang[server_data['language'][str(ctx.guild.id)]]['user-info-join-at'], target.joined_at.strftime("%Y/%m/%d %H:%M:%S"), True),
	        		    (Lang[server_data['language'][str(ctx.guild.id)]]['user-info-boots'], bool(target.premium_since), True)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await ctx.channel.send(embed=embed)
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.command()
async def warn(ctx, user: discord.Member=None, options='None', *, reason='None'):
    if server_data['commands'][str(ctx.guild.id)]['warn']:
        ctx_sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        ctx_sha1.update(str(ctx.author.id).encode('utf-8'))
        if not user:
            embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['usage'], description=prefix+'warn '+Lang[server_data['language'][str(ctx.guild.id)]]['@user']+Lang[server_data['language'][str(ctx.guild.id)]]['reason'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed, delete_after=5)
            return
        salt(user.id)
        user_sha1 = hashlib.sha1(user_salt[str(user.id)].encode('utf-8'))
        user_sha1.update(str(user.id).encode('utf-8'))
        if options == '--sync' and ctx.author.id == data['owner-id']:
            userdata_dict = {}
            for i in range(len(userdata_keys)):
                userdata_dict[userdata_keys[i]] = userdata_values[i]
            userdata_values_dict = userdata_values[userdata_keys.index('warns')]
            userdata_new_dict = userdata_values_dict[str(ctx.guild.id)]
            try:
                userdata_new_dict[str(user_sha1.hexdigest())] = str(int(user_data['warns'][str(ctx.guild.id)][str(user_sha1.hexdigest())]) + 1)
            except:
                userdata_new_dict[str(user_sha1.hexdigest())] = '1'
            userdata_dict['warns'][str(ctx.guild.id)] = userdata_new_dict
            with open('database/userdata.json', 'w') as f:
                json.dump(userdata_dict, f, indent = 4)
            load_userdata()
            embed=discord.Embed(title=str(user)+Lang[server_data['language'][str(ctx.guild.id)]]['user-warned'], description=Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason']+reason, color=0x81FA28)
            await ctx.channel.send(embed=embed)
            await user.send(embed=embed)
            print(now_time(), str(user), Lang[server_data['language'][str(ctx.guild.id)]]['user-warned'], Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason'], reason, Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
            await auto_action(ctx, user, user_sha1, server_data['auto-action'][str(ctx.guild.id)])
        elif ctx.author.guild_permissions.administrator or str(ctx_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            if str(user_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('bypass')][str(ctx.guild.id)].values()) or user.guild_permissions.administrator:
                await error_code.bypass(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
            else:
                userdata_dict = {}
                for i in range(len(userdata_keys)):
                    userdata_dict[userdata_keys[i]] = userdata_values[i]
                userdata_values_dict = userdata_values[userdata_keys.index('warns')]
                userdata_new_dict = userdata_values_dict[str(ctx.guild.id)]
                try:
                    userdata_new_dict[str(user_sha1.hexdigest())] = str(int(user_data['warns'][str(ctx.guild.id)][str(user_sha1.hexdigest())]) + 1)
                except:
                    userdata_new_dict[str(user_sha1.hexdigest())] = '1'
                userdata_dict['warns'][str(ctx.guild.id)] = userdata_new_dict
                with open('database/userdata.json', 'w') as f:
                    json.dump(userdata_dict, f, indent = 4)
                load_userdata()
                embed=discord.Embed(title=str(user)+Lang[server_data['language'][str(ctx.guild.id)]]['user-warned'], description=Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason']+options, color=0x81FA28)
                await ctx.channel.send(embed=embed)
                await user.send(embed=embed)
                print(now_time(), str(user), Lang[server_data['language'][str(ctx.guild.id)]]['user-warned'], Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason'], options, Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
                await auto_action(ctx, user, user_sha1, server_data['auto-action'][str(ctx.guild.id)])
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@bot.event
async def on_message(message):
    if str(message.channel.type) == 'private':
        print(message.channel, ':', message.content)
        return
    if message.author == bot.user or message.author.bot:
        return
    print(now_time(), message.guild.name, '|', message.author, ':', message.content)
    salt(message.author.id)
    try:
        for j in ['admin', 'bypass']:
            if str(message.guild.id) not in list(userdata_values[userdata_keys.index(j)].keys()):
                userdata_dict = {}
                for i in range(len(userdata_keys)):
                    userdata_dict[userdata_keys[i]] = userdata_values[i]
                userdata_values_dict = userdata_values[userdata_keys.index(j)]
                sha512= hashlib.sha512()
                sha512.update(str(message.author).encode('utf-8'))
                userdata_values_dict[str(message.guild.id)] = {str(sha512.hexdigest()): ''}
                userdata_dict[j] = userdata_values_dict
                with open("database/userdata.json", "w") as userdata_file:
                    json.dump(userdata_dict, userdata_file, indent = 4)
                load_userdata()
        if str(message.guild.id) not in list(userdata_values[userdata_keys.index('warns')].keys()):
            userdata_dict = {}
            for i in range(len(userdata_keys)):
                userdata_dict[userdata_keys[i]] = userdata_values[i]
            userdata_values_dict = userdata_values[userdata_keys.index('warns')]
            user_sha1 = hashlib.sha1(user_salt[str(message.author.id)].encode('utf-8'))
            user_sha1.update(str(message.author.id).encode('utf-8'))
            userdata_values_dict[str(message.guild.id)] = {str(user_sha1.hexdigest()): '0'}
            userdata_dict['warns'] = userdata_values_dict
            with open("database/userdata.json", "w") as userdata_file:
                json.dump(userdata_dict, userdata_file, indent = 4)
            load_userdata()
        for j in ['url', 'title']:
            if str(message.guild.id) not in list(musicdata_values[musicdata_keys.index(j)].keys()):
                musicdata_dict = {}
                for i in range(len(musicdata_keys)):
                    musicdata_dict[musicdata_keys[i]] = musicdata_values[i]
                musicdata_values_dict = musicdata_values[musicdata_keys.index(j)]
                musicdata_values_dict[str(message.guild.id)] = {}
                musicdata_dict[j] = musicdata_values_dict
                with open("database/musicdata.json", "w") as musicdata_file:
                    json.dump(musicdata_dict, musicdata_file, indent = 4)
                load_music()
        for j in ['repeat', 'button_switch']:
            if str(message.guild.id) not in list(musicdata_values[musicdata_keys.index(j)].keys()):
                musicdata_dict = {}
                for i in range(len(musicdata_keys)):
                    musicdata_dict[musicdata_keys[i]] = musicdata_values[i]
                musicdata_values_dict = musicdata_values[musicdata_keys.index(j)]
                musicdata_values_dict[str(message.guild.id)] = False
                musicdata_dict[j] = musicdata_values_dict
                with open("database/musicdata.json", "w") as musicdata_file:
                    json.dump(musicdata_dict, musicdata_file, indent = 4)
                load_music()
        if str(message.guild.id) not in list(server_data['language'].keys()):
            serverdata_dict = {}
            for i in range(len(serverdata_keys)):
                serverdata_dict[serverdata_keys[i]] = serverdata_values[i]
            serverdata_values_dict = serverdata_values[serverdata_keys.index('language')]
            serverdata_values_dict[str(message.guild.id)] = 'zh-tw'
            serverdata_dict['language'] = serverdata_values_dict
            with open("database/serverdata.json", "w") as serverdata_file:
                json.dump(serverdata_dict, serverdata_file, indent = 4)
            load_serverdata()
        for j in ['picture-only-channel', 'enter-voice-channel', 'voice-category']:
            if str(message.guild.id) not in list(server_data[j].keys()):
                serverdata_dict = {}
                for i in range(len(serverdata_keys)):
                    serverdata_dict[serverdata_keys[i]] = serverdata_values[i]
                serverdata_values_dict = serverdata_values[serverdata_keys.index(j)]
                serverdata_values_dict[str(message.guild.id)] = []
                serverdata_dict[j] = serverdata_values_dict
                with open("database/serverdata.json", "w") as serverdata_file:
                    json.dump(serverdata_dict, serverdata_file, indent = 4)
                load_serverdata()
        if str(message.guild.id) not in list(server_data['auto-action'].keys()):
            serverdata_dict = {}
            for i in range(len(serverdata_keys)):
                serverdata_dict[serverdata_keys[i]] = serverdata_values[i]
            serverdata_values_dict = serverdata_values[serverdata_keys.index('auto-action')]
            serverdata_values_dict[str(message.guild.id)] = [0, 0, 0]
            serverdata_dict['auto-action'] = serverdata_values_dict
            with open("database/serverdata.json", "w") as serverdata_file:
                json.dump(serverdata_dict, serverdata_file, indent = 4)
            load_serverdata()
        if str(message.guild.id) not in list(server_data['chat-filter-action'].keys()):
            serverdata_dict = {}
            for i in range(len(serverdata_keys)):
                serverdata_dict[serverdata_keys[i]] = serverdata_values[i]
            serverdata_values_dict = serverdata_values[serverdata_keys.index('chat-filter-action')]
            serverdata_values_dict[str(message.guild.id)] = 'None'
            serverdata_dict['chat-filter-action'] = serverdata_values_dict
            with open("database/serverdata.json", "w") as serverdata_file:
                json.dump(serverdata_dict, serverdata_file, indent = 4)
            load_serverdata()
        if str(message.guild.id) not in list(server_data['music-bot'].keys()):
            serverdata_dict = {}
            for i in range(len(serverdata_keys)):
                serverdata_dict[serverdata_keys[i]] = serverdata_values[i]
            serverdata_values_dict = serverdata_values[serverdata_keys.index('music-bot')]
            serverdata_values_dict[str(message.guild.id)] = True
            serverdata_dict['music-bot'] = serverdata_values_dict
            with open("database/serverdata.json", "w") as serverdata_file:
                json.dump(serverdata_dict, serverdata_file, indent = 4)
            load_serverdata()
        if str(message.guild.id) not in list(server_data['commands'].keys()):
            serverdata_dict = {}
            for i in range(len(serverdata_keys)):
                serverdata_dict[serverdata_keys[i]] = serverdata_values[i]
            serverdata_values_dict = serverdata_values[serverdata_keys.index('commands')]
            serverdata_values_dict[str(message.guild.id)] = {}
            serverdata_dict['commands'] = serverdata_values_dict
            with open("database/serverdata.json", "w") as serverdata_file:
                json.dump(serverdata_dict, serverdata_file, indent = 4)
            load_serverdata()
        command_list = ['add', 'addadmin', 'addbypass', 'ban', 'clear', 'chlang', 'copy', 'clearwarn', 'cd',
                        'ci', 'check', 'exit', 'gay', 'kick', 'mute', 'ping', 'reload', 'remove', 'removeadmin',
                        'removebypass', 'set', 'showwarn', 'slowmode', 'send', 'time', 'tlm', 'tempban', 'tempmute', 'unban',
                        'unmute', 'uinfo', 'warn'
                        ]
        if 'add' not in list(serverdata_values[serverdata_keys.index('commands')][str(message.guild.id)].keys()):
            for j in command_list:
                serverdata_dict = {}
                for i in range(len(serverdata_keys)):
                    serverdata_dict[serverdata_keys[i]] = serverdata_values[i]
                serverdata_values_dict = serverdata_values[serverdata_keys.index('commands')]
                serverdata_new_dict = serverdata_values_dict[str(message.guild.id)]
                if j not in list(serverdata_values[serverdata_keys.index('commands')][str(message.guild.id)].keys()):
                    serverdata_new_dict[j] = True
                serverdata_dict['commands'][str(message.guild.id)] = serverdata_new_dict
            with open("database/serverdata.json", "w") as serverdata_file:
                json.dump(serverdata_dict, serverdata_file, indent = 4)
            load_serverdata()
        if str(message.guild.id) not in list(server_data['reaction-roles'].keys()):
            serverdata_dict = {}
            for i in range(len(serverdata_keys)):
                serverdata_dict[serverdata_keys[i]] = serverdata_values[i]
            serverdata_values_dict = serverdata_values[serverdata_keys.index('reaction-roles')]
            serverdata_values_dict[str(message.guild.id)] = {}
            serverdata_dict['reaction-roles'] = serverdata_values_dict
            with open("database/serverdata.json", "w") as serverdata_file:
                json.dump(serverdata_dict, serverdata_file, indent = 4)
            load_serverdata()
    except: ...
    if message.channel.id in server_data['picture-only-channel'][str(message.author.guild.id)] and message.content != "":
        await message.channel.purge(limit=1)
    if message.content.startswith('!info'):
        embed = discord.Embed(title='❗｜'+'Copyright Notice', description=copyright(), color=0xB51FFB)
        embed.set_footer(text='Version: '+data['version'])
        await message.channel.send(embed=embed)
    if message.content.startswith('!prefix'):
        embed = discord.Embed(title='💻｜'+Lang[server_data['language'][str(message.guild.id)]]['prefix-tip'], description=data['command-prefix'], color=0xB51FFB)
        await message.channel.send(embed=embed)
    if message.content.startswith('!function'):
        embed = discord.Embed(title='', color=0xB51FFB)
        embed2 = discord.Embed(title='', color=0xB51FFB)
        with open('config.json', "r", encoding = "utf8") as file:
            tempdata = json.load(file)
        data_key = list(tempdata.keys())
        data_values = list(tempdata.values())
        enable_value = ''
        disable_value = ''
        if server_data['music-bot'][str(message.author.guild.id)]:
            enable_value += 'music bot'+'\n'
        else:
            disable_value += 'music bot'+'\n'
        if server_data['picture-only-channel'][str(message.author.guild.id)] != []:
            enable_value += 'picture only channel'+'\n'
        else:
            disable_value += 'picture only channel'+'\n'
        if server_data['enter-voice-channel'][str(message.author.guild.id)] != [] and server_data['voice-category'][str(message.author.guild.id)] != []:
            enable_value += 'private voice channel'+'\n'
        else:
            disable_value += 'private voice channel'+'\n'
        with open('database/chatfilter/'+str(message.author.guild.id)+'.txt', "r", encoding = "utf8") as words:
            badwords = words.read().split()
        if badwords != []:
            enable_value += 'chat filter'+'\n'
        else:
            disable_value += 'chat filter'+'\n'
        if server_data['chat-filter-action'][str(message.author.guild.id)] != 'None':
            enable_value += 'chat filter action: '+server_data['chat-filter-action'][str(message.author.guild.id)]+'\n'
        else:
            disable_value += 'chat filter action'+'\n'
        if server_data['reaction-roles'][str(message.author.guild.id)] != {}:
            enable_value += 'reaction roles'+'\n'
        else:
            disable_value += 'reaction roles'+'\n'
        for i in range(3):
            match i:
                case 0:
                    if server_data['auto-action'][str(message.author.guild.id)][i] != 0:
                        enable_value += 'auto mute: '+str(server_data['auto-action'][str(message.author.guild.id)][i])+'\n'
                    else:
                        disable_value += 'auto mute'+'\n'
                case 1:
                    if server_data['auto-action'][str(message.author.guild.id)][i] != 0:
                        enable_value += 'auto kick: '+str(server_data['auto-action'][str(message.author.guild.id)][i])+'\n'
                    else:
                        disable_value += 'auto kick'+'\n'
                case 2:
                    if server_data['auto-action'][str(message.author.guild.id)][i] != 0:
                        enable_value += 'auto ban: '+str(server_data['auto-action'][str(message.author.guild.id)][i])+'\n'
                    else:
                        disable_value += 'auto ban'+'\n'
        for i in [10, 11]:
            if data_values[i] == True:
                enable_value += data_key[i]+'\n'
            else:
                disable_value += data_key[i]+'\n'
        enable_value = Lang[server_data['language'][str(message.guild.id)]]['function-None'] if enable_value == '' else enable_value
        disable_value = Lang[server_data['language'][str(message.guild.id)]]['function-None'] if disable_value == '' else disable_value
        embed.add_field(name='🟢｜'+Lang[server_data['language'][str(message.guild.id)]]['function-enable'], value=enable_value, inline=True)
        embed.add_field(name='🔴｜'+Lang[server_data['language'][str(message.guild.id)]]['function-disable'], value=disable_value, inline=True)
        enable_value = ''
        disable_value = ''
        for i in list(serverdata_values[serverdata_keys.index('commands')][str(message.guild.id)].keys()):
            if server_data['commands'][str(message.guild.id)][i]:
                enable_value += i+'\n'
            else:
                disable_value += i+'\n'
        enable_value = Lang[server_data['language'][str(message.guild.id)]]['function-None'] if enable_value == '' else enable_value
        disable_value = Lang[server_data['language'][str(message.guild.id)]]['function-None'] if disable_value == '' else disable_value
        embed2.add_field(name='🟢｜'+Lang[server_data['language'][str(message.guild.id)]]['function-command-enable'], value=enable_value, inline=True)
        embed2.add_field(name='🔴｜'+Lang[server_data['language'][str(message.guild.id)]]['function-command-disable'], value=disable_value, inline=True)
        await message.channel.send(embed=embed)
        await message.channel.send(embed=embed2)
    url_regex = re.compile('((?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&\'\(\)\*\+,;=.]+)')
    url_match_word = url_regex.findall(message.content)
    if url_match_word:
        for i in range(len(url_match_word)):
            url = url_match_word[i][0]
            response = requests.get(f"https://transparencyreport.google.com/transparencyreport/api/v3/safebrowsing/status?site={url}")
            safe = response.text[17]
            match safe:
                case '2':
                    print(now_time(), url, Lang[server_data['language'][str(message.guild.id)]]['unsafe'])
                    embed = discord.Embed(title='⚠｜'+Lang[server_data['language'][str(message.guild.id)]]['security_check'], description=url+'\n'+Lang[server_data['language'][str(message.guild.id)]]['google_check']+Lang[server_data['language'][str(message.guild.id)]]['unsafe'], color=0xEC2E2E)
                case '3':
                    print(now_time(), url, Lang[server_data['language'][str(message.guild.id)]]['somesafe'])
                    embed = discord.Embed(title='⚠｜'+Lang[server_data['language'][str(message.guild.id)]]['security_check'], description=url+'\n'+Lang[server_data['language'][str(message.guild.id)]]['google_check']+Lang[server_data['language'][str(message.guild.id)]]['somesafe'], color=0xF2D02A)
            try:
                await message.reply(embed=embed)
            except: ...
    with open('database/chatfilter/'+str(message.author.guild.id)+'.txt', "r", encoding = "utf8") as words:
        badwords = words.read().split()
    if badwords != []:
        user_sha1 = hashlib.sha1(user_salt[str(message.author.id)].encode('utf-8'))
        user_sha1.update(str(message.author.id).encode('utf-8'))
        try:
            if str(user_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('bypass')][str(message.guild.id)].values()) or message.author.guild_permissions.administrator:
                await bot.process_commands(message)
                return
        except: ...
        else:
            with open('database/chatfilter/'+str(message.author.guild.id)+'.txt', "r", encoding = "utf8") as words:
                badwords = words.read().split()
            for i in badwords:
                Regex = re.compile(i)
                match_word = Regex.search(message.content)
                if match_word:
                    embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(message.guild.id)]]['chat-filter'], description=match_word.group(), color=0xEC2E2E)
                    await message.reply(embed=embed, delete_after=5)
                    await message.delete()
                    await message.author.send(embed=embed)
                    print(now_time(), message.author.name, '❌｜'+Lang[server_data['language'][str(message.guild.id)]]['chat-filter'], match_word.group())
                    reason = Lang[server_data['language'][str(message.guild.id)]]['chat-filter-reason']
                    if server_data['chat-filter-action'][str(message.guild.id)] == 'warn':
                        userdata_dict = {}
                        for i in range(len(userdata_keys)):
                            userdata_dict[userdata_keys[i]] = userdata_values[i]
                        userdata_values_dict = userdata_values[userdata_keys.index('warns')]
                        userdata_new_dict = userdata_values_dict[str(message.guild.id)]
                        try:
                            userdata_new_dict[str(user_sha1.hexdigest())] = str(int(user_data['warns'][str(message.guild.id)][str(user_sha1.hexdigest())]) + 1)
                        except:
                            userdata_new_dict[str(user_sha1.hexdigest())] = '1'
                        userdata_dict['warns'][str(message.guild.id)] = userdata_new_dict
                        with open('database/userdata.json', 'w') as f:
                            json.dump(userdata_dict, f, indent = 4)
                        load_userdata()
                        embed=discord.Embed(title=str(message.author)+Lang[server_data['language'][str(message.guild.id)]]['user-warned'], description=Lang[server_data['language'][str(message.guild.id)]]['warn-reason']+reason, color=0x81FA28)
                        await message.channel.send(embed=embed)
                        await message.author.send(embed=embed)
                        print(now_time(), str(message.author), Lang[server_data['language'][str(message.guild.id)]]['user-warned'], Lang[server_data['language'][str(message.guild.id)]]['warn-reason'], reason)
                        await auto_action(message, message.author, user_sha1, server_data['auto-action'][str(message.author.guild.id)])
                    elif server_data['chat-filter-action'][str(message.guild.id)] == 'mute':
                        guild = message.guild
                        mutedRole = discord.utils.get(guild.roles, name=Lang[server_data['language'][str(message.guild.id)]]['mute-role-name'])
                        all_roles = await guild.fetch_roles()
                        num_roles = len(all_roles)
                        if not mutedRole:
                            mutedRole = await guild.create_role(name=Lang[server_data['language'][str(message.guild.id)]]['mute-role-name'])
                            await mutedRole.edit(position=num_roles - 2)
                            for channel in guild.channels:
                                await channel.set_permissions(mutedRole, speak=False, send_messages=False)
                        await message.author.add_roles(mutedRole, reason=reason)
                        embed=discord.Embed(title=str(message.author)+Lang[server_data['language'][str(message.guild.id)]]['user-muted'], description=Lang[server_data['language'][str(message.guild.id)]]['warn-reason']+reason, color=0x81FA28)
                        await message.channel.send(embed=embed)
                        await message.author.send(embed=embed)
                        print(now_time(), str(message.author), Lang[server_data['language'][str(message.guild.id)]]['user-muted'], Lang[server_data['language'][str(message.guild.id)]]['warn-reason'], reason)
                    elif server_data['chat-filter-action'][str(message.guild.id)] == 'kick':
                        embed=discord.Embed(title=str(message.author)+Lang[server_data['language'][str(message.guild.id)]]['user-kicked'], description=Lang[server_data['language'][str(message.guild.id)]]['warn-reason']+reason, color=0x81FA28)
                        try:
                            await message.author.send(embed=embed)
                        except: ...
                        await message.guild.kick(message.author)
                        await message.channel.send(embed=embed)
                        print(now_time(), str(message.author), Lang[server_data['language'][str(message.guild.id)]]['user-kicked'], Lang[server_data['language'][str(message.guild.id)]]['warn-reason'], reason)
                    elif server_data['chat-filter-action'][str(message.guild.id)] == 'ban':
                        embed=discord.Embed(title=str(message.author)+Lang[server_data['language'][str(message.guild.id)]]['user-banned'], description=Lang[server_data['language'][str(message.guild.id)]]['warn-reason']+reason, color=0x81FA28)
                        try:
                            await message.author.send(embed=embed)
                        except: ...
                        await message.guild.ban(message.author, reason=reason)
                        await message.channel.send(embed=embed)
                        print(now_time(), str(message.author), Lang[server_data['language'][str(message.guild.id)]]['user-banned'], Lang[server_data['language'][str(message.guild.id)]]['warn-reason'], reason)
                    return
        await bot.process_commands(message)
        return
    else:
        await bot.process_commands(message)

async def auto_action(ctx, user, user_sha1, auto_action):
    class count:
        mute_count = str(auto_action[0])
        kick_count = str(auto_action[1])
        ban_count = str(auto_action[2])
    match user_data['warns'][str(ctx.guild.id)][str(user_sha1.hexdigest())]:
        case count.mute_count:
            reason = Lang[server_data['language'][str(ctx.guild.id)]]['when-warnings-match']+count.mute_count+Lang[server_data['language'][str(ctx.guild.id)]]['auto-mute-message']
            mutedRole = discord.utils.get(ctx.guild.roles, name=Lang[server_data['language'][str(ctx.guild.id)]]['mute-role-name'])
            all_roles = await ctx.guild.fetch_roles()
            num_roles = len(all_roles)
            if not mutedRole:
                mutedRole = await ctx.guild.create_role(name=Lang[server_data['language'][str(ctx.guild.id)]]['mute-role-name'])
                await mutedRole.edit(position=num_roles - 2)
                for channel in ctx.guild.channels:
                    await channel.set_permissions(mutedRole, speak=False, send_messages=False)
            await user.add_roles(mutedRole, reason=reason)
            embed=discord.Embed(title=str(user)+Lang[server_data['language'][str(ctx.guild.id)]]['user-muted'], description=Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason']+reason, color=0x81FA28)
            await ctx.channel.send(embed=embed)
            await user.send(embed=embed)
            print(now_time(), str(user), Lang[server_data['language'][str(ctx.guild.id)]]['user-muted'], Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason'], reason, Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
        case count.kick_count:
            reason = Lang[server_data['language'][str(ctx.guild.id)]]['when-warnings-match']+count.kick_count+Lang[server_data['language'][str(ctx.guild.id)]]['auto-kick-message']
            embed=discord.Embed(title=str(user)+Lang[server_data['language'][str(ctx.guild.id)]]['user-kicked'], description=Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason']+reason, color=0x81FA28)
            await user.send(embed=embed)
            await ctx.guild.kick(user)
            await ctx.channel.send(embed=embed)
            print(now_time(), str(user), Lang[server_data['language'][str(ctx.guild.id)]]['user-kicked'], Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason'], reason, Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
        case count.ban_count:
            reason = Lang[server_data['language'][str(ctx.guild.id)]]['when-warnings-match']+count.ban_count+Lang[server_data['language'][str(ctx.guild.id)]]['auto-ban-message']
            embed=discord.Embed(title=str(user)+Lang[server_data['language'][str(ctx.guild.id)]]['user-banned'], description=Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason']+reason, color=0x81FA28)
            await user.send(embed=embed)
            await ctx.guild.ban(user, reason=reason)
            await ctx.channel.send(embed=embed)
            print(now_time(), str(user), Lang[server_data['language'][str(ctx.guild.id)]]['user-banned'], Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason'], reason, Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)

@bot.event
async def on_guild_join(guild):
    print(now_time(), global_Lang['server-added'], guild, f'({guild.id})')
    if not os.path.isfile('database/chatfilter/'+str(guild.id)+'.txt'):
        with open('database/chatfilter/'+str(guild.id)+'.txt', 'a') as f:
            f.write('')
    if str(guild.id) not in list(server_data['guilds'].keys()):
        serverdata_dict = {}
        for i in range(len(serverdata_keys)):
            serverdata_dict[serverdata_keys[i]] = serverdata_values[i]
        serverdata_values_dict = serverdata_values[serverdata_keys.index('guilds')]
        serverdata_values_dict[str(guild.id)] = guild.name
        serverdata_dict['guilds'] = serverdata_values_dict
        with open("database/serverdata.json", "w") as serverdata_file:
            json.dump(serverdata_dict, serverdata_file, indent = 4)
        load_serverdata()

@bot.event
async def on_guild_remove(guild):
    del server_data['guilds'][str(guild.id)]
    with open("database/serverdata.json", "w") as serverdata_file:
        json.dump(server_data, serverdata_file, indent = 4)
    load_serverdata()
    print(now_time(), global_Lang['server-left'], guild, f'({guild.id})')

@bot.event
async def on_raw_reaction_add(reaction):
    guild = bot.get_guild(reaction.guild_id)
    try:
        if str(reaction.emoji) in list(server_data['reaction-roles'][str(reaction.guild_id)].keys()):
            role = server_data['reaction-roles'][str(reaction.guild_id)][str(reaction.emoji)][3:-1]
            addrole = discord.utils.get(guild.roles, id=int(role))
            await reaction.member.add_roles(addrole, reason='By reaction')
    except: ...

@bot.event
async def on_raw_reaction_remove(reaction):
    guild = bot.get_guild(reaction.guild_id)
    member = discord.utils.get(guild.members, id=int(reaction.user_id))
    try:
        if str(reaction.emoji) in list(server_data['reaction-roles'][str(reaction.guild_id)].keys()):
            role = server_data['reaction-roles'][str(reaction.guild_id)][str(reaction.emoji)][3:-1]
            removerole = discord.utils.get(guild.roles, id=int(role))
            await member.remove_roles(removerole, reason='By cancel reaction')
    except: ...

# Music bot

def load_music():
    global music_data, musicdata_keys, musicdata_values
    with open('database/musicdata.json', "r", encoding = "utf8") as music_file:
        music_data = json.load(music_file)
    musicdata_keys = list(music_data.keys())
    musicdata_values = list(music_data.values())
load_music()

def clear_music():
    for i in list(music_data['url'].keys()):
        music_data['url'][i] = {}
        music_data['title'][i] = {}
    for k in list(music_data['button_switch'].keys()):
        music_data['button_switch'][k] = False
    with open("database/musicdata.json", "w") as musicdata_file:
        json.dump(music_data, musicdata_file, indent = 4)
    load_music()
clear_music()

def button_switch(ctx, TF='false'):
    musicdata_dict = {}
    for i in range(len(musicdata_keys)):
        musicdata_dict[musicdata_keys[i]] = musicdata_values[i]
    musicdata_values_dict = musicdata_values[musicdata_keys.index('button_switch')]
    if TF == 'true':
        musicdata_values_dict[str(ctx.guild.id)] = True
    else:
        musicdata_values_dict[str(ctx.guild.id)] = False
    musicdata_dict['button_switch'] = musicdata_values_dict
    with open("database/musicdata.json", "w") as musicdata_file:
        json.dump(musicdata_dict, musicdata_file, indent = 4)
    load_music()

ydl_opts = {
        'format': 'bestaudio',
        'noplaylist': True,
        'default_search': 'auto'
    }

async def playit(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    try:
        if not music_data['repeat'][str(ctx.guild.id)]:
            #await ctx.channel.purge(limit=1, check = lambda inter: inter.content == '')
            musicdata_dict = {}
            del music_data['url'][str(ctx.guild.id)][str(list(music_data['url'][str(ctx.guild.id)].keys())[0])]
            del music_data['title'][str(ctx.guild.id)][str(list(music_data['title'][str(ctx.guild.id)].keys())[0])]
            for i in range(len(musicdata_keys)):
                musicdata_dict[musicdata_keys[i]] = musicdata_values[i]
            with open("database/musicdata.json", "w") as musicdata_file:
                json.dump(musicdata_dict, musicdata_file, indent = 4)
            load_music()
            if list(music_data['url'][str(ctx.guild.id)].keys()) == []:
                await asyncio.sleep(2)
                await voice.disconnect()
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(list(music_data['url'][str(ctx.guild.id)].values())[0], download=False)
            if 'entries' in info:
                Url = info['entries'][0]["formats"][0]['url']
            elif 'formats' in info:
                Url = info["formats"][0]['url']
        except:
            Url = list(music_data['url'][str(ctx.guild.id)].values())[0]
        pplayer = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(Url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), 1)
        voice.play(pplayer, after = lambda e: myafter(ctx))
        button_switch(ctx, 'true')
        print('',Lang[server_data['language'][str(ctx.guild.id)]]['music-playing'],list(music_data['title'][str(ctx.guild.id)].values())[0],list(music_data['url'][str(ctx.guild.id)].values())[0],'', sep='\n')
        if not music_data['repeat'][str(ctx.guild.id)]:
            await music_button_1(ctx, info)
    except: ...
        
def myafter(ctx):
    button_switch(ctx)
    fut = asyncio.run_coroutine_threadsafe(playit(ctx), bot.loop)
    fut.result()

async def music_button_1(ctx, info):
    if 'entries' in info:
        Info = info['entries'][0]
    elif 'formats' in info:
        Info = info
    if not music_data['repeat'][str(ctx.guild.id)]:
        embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['music-playing'], description=Info['title'], color=0x79EF2F)
    else:
        embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['music-playing-repeat'], description=Info['title'], color=0x79EF2F)
    embed.set_thumbnail(url=Info.get('thumbnail'))

    seconds = Info['duration']
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['music-uploader'], value=Info.get('uploader'), inline=True)
    embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['music-duration'], value="%d:%02d:%02d" % (h, m, s), inline=True)
    embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['music-like_count'], value=str(Info.get('like_count')), inline=True)
    embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['music-DJ'], value=f'<@{ctx.message.author.id}>', inline=True)
    embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['music-channel'], value=f'<#{ctx.author.voice.channel.id}>', inline=True)
    if music_data['repeat'][str(ctx.guild.id)]:
        embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['music-repeat'], value=Lang[server_data['language'][str(ctx.guild.id)]]['enable'], inline=True)
    else:
        embed.add_field(name=Lang[server_data['language'][str(ctx.guild.id)]]['music-repeat'], value=Lang[server_data['language'][str(ctx.guild.id)]]['disable'], inline=True)
    embed.set_footer(text=now_time(), icon_url=ctx.author.avatar_url)
    repeat_style = '3' if music_data['repeat'][str(ctx.guild.id)] else '2'
    await ctx.send('', embed=embed, components = [ActionRow(
            Button(label=Lang[server_data['language'][str(ctx.guild.id)]]['music-link'], style=ButtonStyle.link, url=Info.get('webpage_url')),
            Button(label=Lang[server_data['language'][str(ctx.guild.id)]]['music-list'], style='2', custom_id='list', emoji='📜'),
            Button(label=Lang[server_data['language'][str(ctx.guild.id)]]['music-repeat'], style=repeat_style, custom_id='repeat', emoji='🔁'),
            Button(label=Lang[server_data['language'][str(ctx.guild.id)]]['music-random'], style='2', custom_id='random', emoji='🔀')),ActionRow(
            Button(label=Lang[server_data['language'][str(ctx.guild.id)]]['music-pause'], style='1', custom_id='pause', emoji='⏸'),
            Button(label=Lang[server_data['language'][str(ctx.guild.id)]]['music-resume'], style='1', custom_id='resume', emoji='⏯'),
            Button(label=Lang[server_data['language'][str(ctx.guild.id)]]['music-stop'], style='4', custom_id='stop', emoji='⏹'),
            Button(label=Lang[server_data['language'][str(ctx.guild.id)]]['music-skip'], style='1', custom_id='skip', emoji='⏩')),ActionRow(
            Button(label=Lang[server_data['language'][str(ctx.guild.id)]]['music-favorite'], style='3', custom_id='favorite', emoji='💕'),
            Button(label=Lang[server_data['language'][str(ctx.guild.id)]]['music-unfavorite'], style='4', custom_id='unfavorite', emoji='💔'))
    ])

@bot.command(aliases=['p', 'PLAY'])
async def play(ctx, *, url: str=''):
    if server_data['music-bot'][str(ctx.guild.id)]:
        if url == '':
            embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['music-url-error'], color=0xEC2E2E)
            await ctx.reply(embed=embed)
            return
        try:
            voiceChannel = discord.utils.get(ctx.guild.voice_channels, id=ctx.author.voice.channel.id)
        except:
            embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['music-user-not-in-channel'], color=0xEC2E2E)
            await ctx.reply(embed=embed)
            return
        try:
            br = mechanize.Browser()
            br.open(url)
        except:
            videossearch = VideosSearch(url, limit=25)
            result = videossearch.result()
            search_url_list = []
            search_title_list = []
            op = []
            num = 0
            if result["result"] == []:
                embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['search_fail'], color=0xEC2E2E)
                await ctx.reply(embed=embed)
                await ctx.message.add_reaction('❌')
                return
            for res in result["result"]:
                search_url_list.append(res["link"])
                search_title_list.append(res['title'])
                op.append(SelectOption(label=res['channel']['name'], value=str(num), description=res['title'], emoji='🔍'))
                num += 1
            embed = discord.Embed(title='🔍｜'+Lang[server_data['language'][str(ctx.guild.id)]]['search_result'], color=0x81FA28)
            sele = await ctx.reply(embed=embed, content='', components=[SelectMenu(placeholder=Lang[server_data['language'][str(ctx.guild.id)]]['menu-select'], options= op,
                                                custom_id='music_select'
            )])
            interaction = await bot.wait_for('select_option', check = lambda inter: inter.custom_id == 'music_select')
            res = interaction.values[0]
            for i in range(len(op)):
                try:
                    if res == str(i):
                        embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['selected'], description=search_title_list[i], color=0x81FA28)
                        await interaction.send(embed=embed)
                        url = search_url_list[i]
                        await sele.delete()
                        break
                    else:
                        continue
                except:
                    await ctx.message.add_reaction('❌')
                    return
        try:
            await voiceChannel.connect()
        except: ...
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        try:
            await ctx.message.add_reaction('✅')
        except:
            return
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
        except:
            await ctx.message.remove_reaction('✅', bot.user)
            await ctx.message.add_reaction('❌')
            embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['music-play-error'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed)
            return
        if 'entries' in info:
            Url = info['entries'][0]["formats"][0]['url']
        elif 'formats' in info:
            Url = info["formats"][0]['url']
        musicdata_dict = {}
        for i in range(len(musicdata_keys)):
            musicdata_dict[musicdata_keys[i]] = musicdata_values[i]
        musicdata_values_dict = musicdata_values[musicdata_keys.index('url')]
        musicdata_new_dict = musicdata_values_dict[str(ctx.guild.id)]
        try:
            musicdata_new_dict[str(int(max(int(num) for num in list(music_data['url'][str(ctx.guild.id)].keys())))+1)] = str(url)
        except:
            musicdata_new_dict[str(len(musicdata_new_dict))] = str(url)
        musicdata_dict['url'][str(ctx.guild.id)] = musicdata_new_dict
        with open("database/musicdata.json", "w") as musicdata_file:
            json.dump(musicdata_dict, musicdata_file, indent = 4)
        musicdata_values_dict = musicdata_values[musicdata_keys.index('title')]
        musicdata_new_dict = musicdata_values_dict[str(ctx.guild.id)]
        try:
            musicdata_new_dict[str(int(max(int(num) for num in list(music_data['title'][str(ctx.guild.id)].keys())))+1)] = str(info['title'])
        except:
            musicdata_new_dict[str(len(musicdata_new_dict))] = str(info['title'])
        musicdata_dict['title'][str(ctx.guild.id)] = musicdata_new_dict
        with open("database/musicdata.json", "w") as musicdata_file:
            json.dump(musicdata_dict, musicdata_file, indent = 4)
        load_music()
        try:
            pplayer = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(Url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), 1)
            voice.play(pplayer, after = lambda e: myafter(ctx))
            button_switch(ctx, 'true')
            print('',Lang[server_data['language'][str(ctx.guild.id)]]['music-playing'],list(music_data['title'][str(ctx.guild.id)].values())[0],list(music_data['url'][str(ctx.guild.id)].values())[0],'', sep='\n')
            await music_button_1(ctx, info)
        except:
            embed = discord.Embed(title='✅｜'+Lang[server_data['language'][str(ctx.guild.id)]]['playlist_added'], color=0x81FA28)
            await ctx.reply(embed=embed)
    
@bot.command()
async def leave(ctx):
    if server_data['music-bot'][str(ctx.guild.id)]:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        try:
            if voice.is_connected():
                await voice.disconnect()
        except:
            embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['music-bot-not-in-channel'], color=0xEC2E2E)
            try:
                await ctx.reply(embed=embed)
            except:
                await ctx.channel.send(embed=embed)

@bot.command()
async def pause(ctx):
    if server_data['music-bot'][str(ctx.guild.id)]:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        try:
            if voice.is_playing():
                voice.pause()
        except:
            embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['music-nothing-playing'], color=0xEC2E2E)
            try:
                await ctx.reply(embed=embed)
            except:
                await ctx.channel.send(embed=embed)

@bot.command()
async def resume(ctx):
    if server_data['music-bot'][str(ctx.guild.id)]:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        try:
            if voice.is_paused():
                voice.resume()
        except:
            embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['music-nothing-pause'], color=0xEC2E2E)
            try:
                await ctx.reply(embed=embed)
            except:
                await ctx.channel.send(embed=embed)

@bot.command()
async def repeat(ctx):
    if server_data['music-bot'][str(ctx.guild.id)]:
        musicdata_dict = {}
        for i in range(len(musicdata_keys)):
            musicdata_dict[musicdata_keys[i]] = musicdata_values[i]
        musicdata_values_dict = musicdata_values[musicdata_keys.index('repeat')]
        if music_data['repeat'][str(ctx.guild.id)]:
            musicdata_values_dict[str(ctx.guild.id)] = False
            embed = discord.Embed(title='🔁｜'+Lang[server_data['language'][str(ctx.guild.id)]]['repeat-disabled'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed)
        else:
            musicdata_values_dict[str(ctx.guild.id)] = True
            embed = discord.Embed(title='🔁｜'+Lang[server_data['language'][str(ctx.guild.id)]]['repeat-enabled'], color=0x81FA28)
            await ctx.channel.send(embed=embed)
        musicdata_dict['repeat'] = musicdata_values_dict
        with open("database/musicdata.json", "w") as musicdata_file:
            json.dump(musicdata_dict, musicdata_file, indent = 4)
        load_music()

@bot.command()
async def stop(ctx):
    if server_data['music-bot'][str(ctx.guild.id)]:
        music_data['url'][str(ctx.guild.id)] = {}
        music_data['title'][str(ctx.guild.id)] = {}
        with open("database/musicdata.json", "w") as musicdata_file:
            json.dump(music_data, musicdata_file, indent = 4)
        load_music()
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        button_switch(ctx)
        try:
            voice.stop()
            await voice.disconnect()
        except:
            embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['music-nothing-playing'], color=0xEC2E2E)
            try:
                await ctx.reply(embed=embed)
            except:
                await ctx.channel.send(embed=embed)
        return

@bot.command()
async def volume(ctx, volume: int=100):
    if server_data['music-bot'][str(ctx.guild.id)]:
        if ctx.voice_client is None:
            embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['music-bot-not-in-channel'], color=0xEC2E2E)
            await ctx.reply(embed=embed)
            return
        before_volume = ctx.voice_client.source.volume * 100
        ctx.voice_client.source.volume = volume / 100
        if before_volume > volume:
            embed = discord.Embed(title='🔉｜'+Lang[server_data['language'][str(ctx.guild.id)]]['volume-changed']+str(before_volume)+'%'+Lang[server_data['language'][str(ctx.guild.id)]]['volume-changed-to']+str(volume)+'%', color=0xEC2E2E)
            await ctx.reply(embed=embed)
        elif before_volume < volume:
            embed = discord.Embed(title='🔊｜'+Lang[server_data['language'][str(ctx.guild.id)]]['volume-changed']+str(before_volume)+'%'+Lang[server_data['language'][str(ctx.guild.id)]]['volume-changed-to']+str(volume)+'%', color=0xEC2E2E)
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(title='❓｜'+Lang[server_data['language'][str(ctx.guild.id)]]['volume-nothing-changed'], color=0xEC2E2E)
            await ctx.reply(embed=embed)

@bot.command()
async def skip(ctx):
    if server_data['music-bot'][str(ctx.guild.id)]:
        button_switch(ctx)
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        try:
            voice.stop()
        except:
            embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['music-nothing-playing'], color=0xEC2E2E)
            try:
                await ctx.reply(embed=embed)
            except:
                await ctx.channel.send(embed=embed)
        return

@bot.command(aliases=['pl'])
async def playlist(ctx):
    if server_data['music-bot'][str(ctx.guild.id)]:
        if list(music_data['title'][str(ctx.guild.id)].keys()) == []:
            embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['music-nothing-playing'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed)
            return
        else:
            embed = discord.Embed(title='📜｜'+Lang[server_data['language'][str(ctx.guild.id)]]['music-list'], color=0x79EF2F)
            for playlist in range(len(list(music_data['title'][str(ctx.guild.id)].keys()))):
                if playlist == 0:
                    if not music_data['repeat'][str(ctx.guild.id)]:
                        embed.add_field(name=list(music_data['title'][str(ctx.guild.id)].values())[playlist], value=Lang[server_data['language'][str(ctx.guild.id)]]['music-playing'], inline=False)
                    else:
                        embed.add_field(name=list(music_data['title'][str(ctx.guild.id)].values())[playlist], value=Lang[server_data['language'][str(ctx.guild.id)]]['music-playing-repeat'], inline=False)
                else:
                    embed.add_field(name=list(music_data['title'][str(ctx.guild.id)].values())[playlist], value='No. '+str(playlist), inline=False)
        await ctx.channel.send(embed=embed)

@bot.command()
async def listmove(ctx, before: int, after: int):
    if server_data['music-bot'][str(ctx.guild.id)]:
        if before == 0:
            embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['move-error'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed)
            return
        elif before > len(list(music_data['url'][str(ctx.guild.id)].keys()))-1 or after > len(list(music_data['url'][str(ctx.guild.id)].keys()))-1:
            embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['out-range'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed)
            return
        musicdata_dict = {}
        move_url_dict = {}
        move_title_dict = {}
        url_list = list(music_data['url'][str(ctx.guild.id)].items())
        title_list = list(music_data['title'][str(ctx.guild.id)].items())
        music_url = url_list[before]
        music_name = title_list[before]
        del url_list[before]
        url_list.insert(after, music_url)
        del title_list[before]
        title_list.insert(after, music_name)
        for i in range(len(url_list)):
            move_url_dict[url_list[i][0]] = url_list[i][1]
            move_title_dict[title_list[i][0]] = title_list[i][1]
        for j in range(len(musicdata_keys)):
            musicdata_dict[musicdata_keys[j]] = musicdata_values[j]
        musicdata_dict['url'][str(ctx.guild.id)] = move_url_dict
        musicdata_dict['title'][str(ctx.guild.id)] = move_title_dict
        with open("database/musicdata.json", "w") as musicdata_file:
            json.dump(musicdata_dict, musicdata_file, indent = 4)
        load_music()
        embed = discord.Embed(title='🔃｜'+Lang[server_data['language'][str(ctx.guild.id)]]['music-moved'], color=0x81FA28)
        await ctx.channel.send(embed=embed)

@bot.command()
async def listremove(ctx, number:int):
    if server_data['music-bot'][str(ctx.guild.id)]:
        if number == 0:
            embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['delete-error'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed)
            return
        elif number > len(list(music_data['url'][str(ctx.guild.id)].keys()))-1:
            embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['out-range'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed)
            return
        musicdata_dict = {}
        num_list = list(music_data['url'][str(ctx.guild.id)].keys())
        for i in range(len(musicdata_keys)):
            musicdata_dict[musicdata_keys[i]] = musicdata_values[i]
        musicdata_values_dict = musicdata_values[musicdata_keys.index('url')]
        musicdata_new_dict = musicdata_values_dict[str(ctx.guild.id)]
        del musicdata_new_dict[num_list[number]]
        musicdata_dict['url'][str(ctx.guild.id)] = musicdata_new_dict
        musicdata_values_dict = musicdata_values[musicdata_keys.index('title')]
        musicdata_new_dict = musicdata_values_dict[str(ctx.guild.id)]
        del musicdata_new_dict[num_list[number]]
        musicdata_dict['title'][str(ctx.guild.id)] = musicdata_new_dict
        with open("database/musicdata.json", "w") as musicdata_file:
            json.dump(musicdata_dict, musicdata_file, indent = 4)
        load_music()
        embed = discord.Embed(title='🗑｜'+Lang[server_data['language'][str(ctx.guild.id)]]['music-deleted'], color=0x81FA28)
        await ctx.channel.send(embed=embed)

@bot.command()
async def listrandom(ctx):
    if server_data['music-bot'][str(ctx.guild.id)]:
        musicdata_dict = {}
        random_dict = {} 
        url_list = list(music_data['url'][str(ctx.guild.id)].items())
        if url_list == []:
            embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['music-nothing-playing'], color=0xEC2E2E)
        else:
            temp = url_list[0]
            url_list.pop(0)
            random.shuffle(url_list)
            url_list.insert(0, temp)
            for i in range(len(url_list)):
                random_dict[url_list[i][0]] = url_list[i][1]
            for j in range(len(musicdata_keys)):
                musicdata_dict[musicdata_keys[j]] = musicdata_values[j]
            musicdata_dict['url'][str(ctx.guild.id)] = random_dict
            with open("database/musicdata.json", "w") as musicdata_file:
                json.dump(musicdata_dict, musicdata_file, indent = 4)
            random_dict = {}
            for i in range(len(url_list)):
                random_dict[url_list[i][0]] = music_data['title'][str(ctx.guild.id)][url_list[i][0]]
            musicdata_dict['title'][str(ctx.guild.id)] = random_dict
            with open("database/musicdata.json", "w") as musicdata_file:
                json.dump(musicdata_dict, musicdata_file, indent = 4)
            load_music()
            embed = discord.Embed(title='🔀｜'+Lang[server_data['language'][str(ctx.guild.id)]]['music-randomed'], color=0x81FA28)
        await ctx.channel.send(embed=embed)

@bot.command(aliases=['f'])
async def favorite(ctx, options='', *, values: str=''):
    if server_data['music-bot'][str(ctx.guild.id)]:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        with open('database/favorite.json', "r", encoding = "utf8") as favorite_file:
            favorite_data = json.load(favorite_file)
        data_keys = list(favorite_data.keys())
        data_values = list(favorite_data.values())
        favorite_dict = {}
        if options == 'add' or options == 'a':
            if values == '':
                embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['favorite-not-url'], color=0xEC2E2E)
                await ctx.reply(embed=embed)
                return
            else:
                try:
                    br = mechanize.Browser()
                    br.open(values)
                except:
                    videossearch = VideosSearch(values, limit=25)
                    result = videossearch.result()
                    search_url_list = []
                    search_title_list = []
                    op = []
                    num = 0
                    if result["result"] == []:
                        embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['search_fail'], color=0xEC2E2E)
                        await ctx.reply(embed=embed)
                        await ctx.message.add_reaction('❌')
                        return
                    for res in result["result"]:
                        search_url_list.append(res["link"])
                        search_title_list.append(res['title'])
                        op.append(SelectOption(label=res['channel']['name'], value=str(num), description=res['title'], emoji='🔍'))
                        num += 1
                    embed = discord.Embed(title='🔍｜'+Lang[server_data['language'][str(ctx.guild.id)]]['search_result'], color=0x81FA28)
                    sele = await ctx.reply(embed=embed, content='', components=[SelectMenu(placeholder=Lang[server_data['language'][str(ctx.guild.id)]]['menu-select'], options= op,
                                                        custom_id='music_select'
                    )])
                    interaction = await bot.wait_for('select_option', check = lambda inter: inter.custom_id == 'music_select')
                    res = interaction.values[0]
                    for i in range(len(op)):
                        try:
                            if res == str(i):
                                embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['selected'], description=search_title_list[i], color=0x81FA28)
                                await interaction.send(embed=embed)
                                values = search_url_list[i]
                                await sele.delete()
                                break
                            else:
                                continue
                        except:
                            await ctx.message.add_reaction('❌')
                            return
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(values, download=False)
                for i in range(len(data_keys)):
                    favorite_dict[data_keys[i]] = data_values[i]
                if not favorite_data.__contains__(str(sha1.hexdigest())):
                    data_values_dict = {str(values): str(info['title'])}  
                else:
                    data_values_dict = data_values[data_keys.index(str(sha1.hexdigest()))]
                    data_values_dict[str(values)] = str(info['title'])
                favorite_dict[str(sha1.hexdigest())] = data_values_dict
                with open("database/favorite.json", "w") as favorite_file:
                    json.dump(favorite_dict, favorite_file, indent = 4)
                embed = discord.Embed(title='✅｜'+Lang[server_data['language'][str(ctx.guild.id)]]['favorite-added'], description=info['title'], color=0x81FA28)
                await ctx.reply(embed=embed)
        elif options == 'remove'or options == 'r':
            if str(sha1.hexdigest()) not in data_keys:
                embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['favorite-list-nothing'], color=0xEC2E2E)
                await ctx.reply(embed=embed)
                return
            if values == '':
                embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['favorite-remove-not-number'], color=0xEC2E2E)
                await ctx.reply(embed=embed)
                return
            remove_dict = data_values[data_keys.index(str(sha1.hexdigest()))]
            remove_keys = list(remove_dict.keys())
            remove_values = list(remove_dict.values())
            try:
                if int(values) > len(remove_keys)-1:
                    embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['out-range'], color=0xEC2E2E)
                    await ctx.reply(embed=embed)
                    return
            except: ...
            if values == '-a':
                embed = discord.Embed(title='🗑｜'+Lang[server_data['language'][str(ctx.guild.id)]]['favorite-remove-all'], color=0x81FA28)
                for remove_url in remove_keys:
                    del favorite_data[str(sha1.hexdigest())][str(remove_url)]
            else:
                embed = discord.Embed(title='🗑｜'+Lang[server_data['language'][str(ctx.guild.id)]]['favorite-removed'], description=remove_values[int(values)], color=0x81FA28)
                remove_url = remove_keys[int(values)]
                del favorite_data[str(sha1.hexdigest())][str(remove_url)]

            for i in range(len(data_keys)):
                favorite_dict[data_keys[i]] = data_values[i]
            with open("database/favorite.json", "w") as config_file:
                json.dump(favorite_dict, config_file, indent = 4)
            await ctx.channel.send(embed=embed)
        elif options == 'list' or options == 'l':
            try:
                list_dict = data_values[data_keys.index(str(sha1.hexdigest()))]
            except:
                embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['favorite-list-nothing'], color=0xEC2E2E)
                await ctx.reply(embed=embed)
                return
            list_keys = list(list_dict.keys())
            if list_keys == []:
                embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['favorite-list-nothing'], color=0xEC2E2E)
            else:
                embed = discord.Embed(title='💕｜'+ctx.author.name+Lang[server_data['language'][str(ctx.guild.id)]]['favorite-list-title'], color=0x79EF2F)
                for favorite_list in range(len(list_keys)):
                    embed.add_field(name=list_dict[list_keys[favorite_list]], value='No. '+str(favorite_list), inline=False)
            await ctx.reply(embed=embed)
        elif options == 'play' or options == 'p':
            if str(sha1.hexdigest()) not in data_keys:
                await ctx.message.remove_reaction('✅', bot.user)
                await ctx.message.add_reaction('❌')
                embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['favorite-list-nothing'], color=0xEC2E2E)
                await ctx.reply(embed=embed)
                return
            try:
                voiceChannel = discord.utils.get(ctx.guild.voice_channels, id=ctx.author.voice.channel.id)
            except:
                embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['music-user-not-in-channel'], color=0xEC2E2E)
                await ctx.reply(embed=embed)
                return
            try:
                await voiceChannel.connect()
            except: ...
            voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
            try:
                await ctx.message.add_reaction('✅')
            except:
                return
            play_dict = data_values[data_keys.index(str(sha1.hexdigest()))]
            play_keys = list(play_dict.keys())
            musicdata_dict = {}
            for i in range(len(musicdata_keys)):
                musicdata_dict[musicdata_keys[i]] = musicdata_values[i]
            if values == '':
                favorite_url_list = []
                favorite_title_list = []
                op = []
                num = 0
                for res in favorite_data[str(sha1.hexdigest())]:
                    favorite_url_list.append(res)
                    favorite_title_list.append(favorite_data[str(sha1.hexdigest())][res])
                    op.append(SelectOption(label=favorite_data[str(sha1.hexdigest())][res], value=str(num), description=res, emoji='🔍'))
                    num += 1
                embed = discord.Embed(title='🔍｜'+Lang[server_data['language'][str(ctx.guild.id)]]['search_result'], color=0x81FA28)
                sele = await ctx.reply(embed=embed, content='', components=[SelectMenu(placeholder=Lang[server_data['language'][str(ctx.guild.id)]]['menu-select'], options= op,
                                                    custom_id='favorite_select'
                )])
                interaction = await bot.wait_for('select_option', check = lambda inter: inter.custom_id == 'favorite_select')
                res = interaction.values[0]
                for i in range(len(op)):
                    try:
                        if res == str(i):
                            embed = discord.Embed(title=Lang[server_data['language'][str(ctx.guild.id)]]['selected'], description=favorite_title_list[i], color=0x81FA28)
                            await interaction.send(embed=embed)
                            values = favorite_url_list[i]
                            await sele.delete()
                            break
                        else:
                            continue
                    except:
                        await ctx.message.add_reaction('❌')
                        return
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(values, download=False)
                if 'entries' in info:
                    Url = info['entries'][0]["formats"][0]['url']
                elif 'formats' in info:
                    Url = info["formats"][0]['url']
                musicdata_values_dict = musicdata_values[musicdata_keys.index('url')]
                musicdata_new_dict = musicdata_values_dict[str(ctx.guild.id)]
                try:
                    musicdata_new_dict[str(int(max(int(num) for num in list(music_data['url'][str(ctx.guild.id)].keys())))+1)] = values
                except:
                    musicdata_new_dict[str(len(musicdata_new_dict))] = values
                musicdata_dict['url'][str(ctx.guild.id)] = musicdata_new_dict
                with open("database/musicdata.json", "w") as musicdata_file:
                    json.dump(musicdata_dict, musicdata_file, indent = 4)
                load_music()
                musicdata_values_dict = musicdata_values[musicdata_keys.index('title')]
                musicdata_new_dict = musicdata_values_dict[str(ctx.guild.id)]
                try:
                    musicdata_new_dict[str(int(max(int(num) for num in list(music_data['title'][str(ctx.guild.id)].keys())))+1)] = str(info['title'])
                except:
                    musicdata_new_dict[str(len(musicdata_new_dict))] = str(info['title'])
                musicdata_dict['title'][str(ctx.guild.id)] = musicdata_new_dict
                with open("database/musicdata.json", "w") as musicdata_file:
                    json.dump(musicdata_dict, musicdata_file, indent = 4)
                load_music()
            elif values == '-a':
                musicdata_values_dict = musicdata_values[musicdata_keys.index('url')]
                musicdata_new_dict = musicdata_values_dict[str(ctx.guild.id)]
                for play_url in play_keys:
                    try:
                        musicdata_new_dict[str(int(max(int(num) for num in list(music_data['url'][str(ctx.guild.id)].keys())))+1)] = str(play_url)
                    except:
                        musicdata_new_dict[str(len(musicdata_new_dict))] = str(play_url)
                musicdata_dict['url'][str(ctx.guild.id)] = musicdata_new_dict
                with open("database/musicdata.json", "w") as musicdata_file:
                    json.dump(musicdata_dict, musicdata_file, indent = 4)
                load_music()
                musicdata_values_dict = musicdata_values[musicdata_keys.index('title')]
                musicdata_new_dict = musicdata_values_dict[str(ctx.guild.id)]
                for play_url in play_keys:
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(play_url, download=False)
                    try:
                        musicdata_new_dict[str(int(max(int(num) for num in list(music_data['title'][str(ctx.guild.id)].keys())))+1)] = str(info['title'])
                    except:
                        musicdata_new_dict[str(len(musicdata_new_dict))] = str(info['title'])
                musicdata_dict['title'][str(ctx.guild.id)] = musicdata_new_dict
                with open("database/musicdata.json", "w") as musicdata_file:
                    json.dump(musicdata_dict, musicdata_file, indent = 4)
                load_music()
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(play_keys[0], download=False)
                if 'entries' in info:
                    Url = info['entries'][0]["formats"][0]['url']
                elif 'formats' in info:
                    Url = info["formats"][0]['url']
            else:
                if int(values) > len(play_keys)-1:
                    await ctx.message.remove_reaction('✅', bot.user)
                    await ctx.message.add_reaction('❌')
                    embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['out-range'], color=0xEC2E2E)
                    await ctx.reply(embed=embed)
                    return
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(play_keys[int(values)], download=False)
                if 'entries' in info:
                    Url = info['entries'][0]["formats"][0]['url']
                elif 'formats' in info:
                    Url = info["formats"][0]['url']
                musicdata_values_dict = musicdata_values[musicdata_keys.index('url')]
                musicdata_new_dict = musicdata_values_dict[str(ctx.guild.id)]
                try:
                    musicdata_new_dict[str(int(max(int(num) for num in list(music_data['url'][str(ctx.guild.id)].keys())))+1)] = str(play_keys[int(values)])
                except:
                    musicdata_new_dict[str(len(musicdata_new_dict))] = str(play_keys[int(values)])
                musicdata_dict['url'][str(ctx.guild.id)] = musicdata_new_dict
                with open("database/musicdata.json", "w") as musicdata_file:
                    json.dump(musicdata_dict, musicdata_file, indent = 4)
                load_music()
                musicdata_values_dict = musicdata_values[musicdata_keys.index('title')]
                musicdata_new_dict = musicdata_values_dict[str(ctx.guild.id)]
                try:
                    musicdata_new_dict[str(int(max(int(num) for num in list(music_data['title'][str(ctx.guild.id)].keys())))+1)] = str(info['title'])
                except:
                    musicdata_new_dict[str(len(musicdata_new_dict))] = str(info['title'])
                musicdata_dict['title'][str(ctx.guild.id)] = musicdata_new_dict
                with open("database/musicdata.json", "w") as musicdata_file:
                    json.dump(musicdata_dict, musicdata_file, indent = 4)
                load_music()
            try:    
                pplayer = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(Url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), 1)
                voice.play(pplayer, after = lambda e: myafter(ctx))
                button_switch(ctx, 'true')
                print('',Lang[server_data['language'][str(ctx.guild.id)]]['music-playing'],list(music_data['title'][str(ctx.guild.id)].values())[0],list(music_data['url'][str(ctx.guild.id)].values())[0],'', sep='\n')
                await music_button_1(ctx, info)
            except:
                embed = discord.Embed(title='✅｜'+Lang[server_data['language'][str(ctx.guild.id)]]['playlist_added'], color=0x81FA28)
                await ctx.reply(embed=embed)
        else:
            await ctx.send(content='', components=[SelectMenu(placeholder=Lang[server_data['language'][str(ctx.guild.id)]]['menu-select'], options= [
                                                    SelectOption(label=prefix+'favorite add', value=prefix+'favorite add', description=Lang[server_data['language'][str(ctx.guild.id)]]['favorite-menu-add'], emoji='💕'),
                                                    SelectOption(label=prefix+'favorite remove', value=prefix+'favorite remove', description=Lang[server_data['language'][str(ctx.guild.id)]]['favorite-menu-remove'], emoji='🗑'),
                                                    SelectOption(label=prefix+'favorite list', value=prefix+'favorite list', description=Lang[server_data['language'][str(ctx.guild.id)]]['favorite-menu-list'], emoji='📜'),
                                                    SelectOption(label=prefix+'favorite play', value=prefix+'favorite play', description=Lang[server_data['language'][str(ctx.guild.id)]]['favorite-menu-play'], emoji='▶')
                                                ],
                                                custom_id='favorite_menu'
                )])

@bot.event
async def on_button_click(interaction):
    salt(interaction.author.id)
    sha1 = hashlib.sha1(user_salt[str(interaction.author.id)].encode('utf-8'))
    sha1.update(str(interaction.author.id).encode('utf-8'))
    if interaction.component.label.startswith("關閉專案"):
        await interaction.send('專案已關閉')
        #await tick_message.set_permissions(interaction.author, send_messages=False, view_channel=False)
        embed = discord.Embed(title='', color=0xEDFA28)
        embed.add_field(name='專案已關閉', value='如要刪除專案請點擊以下按鈕', inline=False)
        await interaction.channel.send(embed=embed)
        await interaction.channel.send('', components = [ActionRow(
                Button(label='刪除專案', style='4', custom_id='delete_tick', emoji='🗑'))
                ])
    elif interaction.component.label.startswith("刪除專案"):
        await interaction.channel.delete()
    if music_data['button_switch'][str(interaction.author.guild.id)]:
        try:
            if interaction.component.label.startswith(Lang[server_data['language'][str(interaction.author.guild.id)]]['music-pause']):
                await interaction.respond(Lang[server_data['language'][str(interaction.author.guild.id)]]['selected']+Lang[server_data['language'][str(interaction.author.guild.id)]]['music-pause'], ephemeral=True)
                await pause(interaction)
            elif interaction.component.label.startswith(Lang[server_data['language'][str(interaction.author.guild.id)]]['music-resume']):
                await interaction.respond(Lang[server_data['language'][str(interaction.author.guild.id)]]['selected']+Lang[server_data['language'][str(interaction.author.guild.id)]]['music-resume'], ephemeral=True)
                await resume(interaction)
            elif interaction.component.label.startswith(Lang[server_data['language'][str(interaction.author.guild.id)]]['music-list']):
                await interaction.respond(Lang[server_data['language'][str(interaction.author.guild.id)]]['selected']+Lang[server_data['language'][str(interaction.author.guild.id)]]['music-list'], ephemeral=True)
                await playlist(interaction)
            elif interaction.component.label.startswith(Lang[server_data['language'][str(interaction.author.guild.id)]]['music-skip']):
                await interaction.respond(Lang[server_data['language'][str(interaction.author.guild.id)]]['selected']+Lang[server_data['language'][str(interaction.author.guild.id)]]['music-skip'], ephemeral=True)
                await skip(interaction)
            elif interaction.component.label.startswith(Lang[server_data['language'][str(interaction.author.guild.id)]]['music-stop']):
                await interaction.respond(Lang[server_data['language'][str(interaction.author.guild.id)]]['selected']+Lang[server_data['language'][str(interaction.author.guild.id)]]['music-stop'], ephemeral=True)
                await stop(interaction)
            elif interaction.component.label.startswith(Lang[server_data['language'][str(interaction.author.guild.id)]]['music-repeat']):
                await interaction.respond(Lang[server_data['language'][str(interaction.author.guild.id)]]['selected']+Lang[server_data['language'][str(interaction.author.guild.id)]]['music-repeat'], ephemeral=True)
                await repeat(interaction)
            elif interaction.component.label.startswith(Lang[server_data['language'][str(interaction.author.guild.id)]]['music-random']):
                await interaction.respond(Lang[server_data['language'][str(interaction.author.guild.id)]]['selected']+Lang[server_data['language'][str(interaction.author.guild.id)]]['music-random'], ephemeral=True)
                await listrandom(interaction)
            elif interaction.component.label.startswith(Lang[server_data['language'][str(interaction.author.guild.id)]]['music-favorite']):
                with open('database/favorite.json', "r", encoding = "utf8") as favorite_file:
                    favorite_data = json.load(favorite_file)
                data_keys = list(favorite_data.keys())
                data_values = list(favorite_data.values())
                favorite_dict = {}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(list(music_data['url'][str(interaction.author.guild.id)].values())[0], download=False)
                for i in range(len(data_keys)):
                    favorite_dict[data_keys[i]] = data_values[i]
                if not favorite_data.__contains__(str(sha1.hexdigest())):
                    data_values_dict = {list(music_data['url'][str(interaction.author.guild.id)].values())[0]: str(info['title'])}
                else:
                    data_values_dict = data_values[data_keys.index(str(sha1.hexdigest()))]
                    data_values_dict[list(music_data['url'][str(interaction.author.guild.id)].values())[0]] = str(info['title'])
                favorite_dict[str(sha1.hexdigest())] = data_values_dict
                with open("database/favorite.json", "w") as favorite_file:
                    json.dump(favorite_dict, favorite_file, indent = 4)
                embed = discord.Embed(title='✅｜'+Lang[server_data['language'][str(interaction.author.guild.id)]]['favorite-added'], description=info['title'], color=0x81FA28)
                await interaction.respond(embed=embed, ephemeral=True)
            elif interaction.component.label.startswith(Lang[server_data['language'][str(interaction.author.guild.id)]]['music-unfavorite']):
                with open('database/favorite.json', "r", encoding = "utf8") as favorite_file:
                    favorite_data = json.load(favorite_file)
                data_keys = list(favorite_data.keys())
                data_values = list(favorite_data.values())
                favorite_dict = {}
                remove_dict = data_values[data_keys.index(str(sha1.hexdigest()))]
                remove_url = list(music_data['url'][str(interaction.author.guild.id)].values())[0]
                try:
                    embed = discord.Embed(title='🗑｜'+Lang[server_data['language'][str(interaction.author.guild.id)]]['favorite-removed'], description=remove_dict[remove_url], color=0x81FA28)
                    await interaction.respond(embed=embed, ephemeral=True)
                    del favorite_data[str(sha1.hexdigest())][str(remove_url)]
                except:
                    embed = discord.Embed(title='❌｜'+Lang[server_data['language'][str(interaction.author.guild.id)]]['favorite-remove-not-favorite'], color=0xEC2E2E)
                    await interaction.respond(embed=embed, ephemeral=True)
                for i in range(len(data_keys)):
                    favorite_dict[data_keys[i]] = data_values[i]
                with open("database/favorite.json", "w") as favorite_file:
                    json.dump(favorite_dict, favorite_file, indent = 4)
        except: ...

# context menu

@interClient.message_command(name = 'Add to chat filter')
async def add_chatfilter(ctx):
    ctx_sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
    ctx_sha1.update(str(ctx.author.id).encode('utf-8'))
    if ctx.author.guild_permissions.administrator or str(ctx_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
        with open('database/chatfilter/'+str(ctx.guild.id)+'.txt', "r", encoding = "utf8") as words:
            badwords = words.read().split()
        if ' ' in ctx.message.content:
            temp = re.split('\s', ctx.message.content)
            content = ''
            for word in temp:
                content += f'({word})\s'
            ctx.message.content = content[0:-2]
        if ctx.message.content not in badwords:
            with open('database/chatfilter/'+str(ctx.guild.id)+'.txt', "a", encoding = "utf8") as words:
                words.write(f'{ctx.message.content}\n')
            embed = discord.Embed(title='✅｜'+Lang[server_data['language'][str(ctx.guild.id)]]['add-chat-filter'], description=f'`{ctx.message.content}`', color=0x81FA28)
        await ctx.respond(embed=embed, ephemeral=True)
    else:
        await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@interClient.message_command(name = 'Link security check')
async def security_check(ctx):
    url_regex = re.compile('(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&\'\(\)\*\+,;=.]+')
    url_match_word = url_regex.search(ctx.message.content)
    if url_match_word:
        response = requests.get(f"https://transparencyreport.google.com/transparencyreport/api/v3/safebrowsing/status?site={url_match_word.group()}")
        safe = response.text[17]
        match safe:
            case '2':
                print(now_time(), url_match_word.group(), Lang[server_data['language'][str(ctx.guild.id)]]['unsafe'])
                embed = discord.Embed(title='⚠｜'+Lang[server_data['language'][str(ctx.guild.id)]]['security_check'], description=url_match_word.group()+'\n'+Lang[server_data['language'][str(ctx.guild.id)]]['google_check']+Lang[server_data['language'][str(ctx.guild.id)]]['unsafe'], color=0xEC2E2E)
            case '3':
                print(now_time(), url_match_word.group(), Lang[server_data['language'][str(ctx.guild.id)]]['somesafe'])
                embed = discord.Embed(title='⚠｜'+Lang[server_data['language'][str(ctx.guild.id)]]['security_check'], description=url_match_word.group()+'\n'+Lang[server_data['language'][str(ctx.guild.id)]]['google_check']+Lang[server_data['language'][str(ctx.guild.id)]]['somesafe'], color=0xF2D02A)
            case _:
                embed = discord.Embed(title='⚠｜'+Lang[server_data['language'][str(ctx.guild.id)]]['security_check'], description=url_match_word.group()+'\n'+Lang[server_data['language'][str(ctx.guild.id)]]['google_check']+Lang[server_data['language'][str(ctx.guild.id)]]['safe'], color=0x81FA28)
    else:
        embed =discord.Embed(title='❌｜'+Lang[server_data['language'][str(ctx.guild.id)]]['not-url'], color=0xEC2E2E)
    await ctx.respond(embed=embed, ephemeral=True)

@interClient.user_command(name = 'Ban')
async def ban_user(ctx):
    salt(ctx.user.id)
    ctx_sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
    ctx_sha1.update(str(ctx.author.id).encode('utf-8'))
    if ctx.author.guild_permissions.administrator or str(ctx_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
        user_sha1 = hashlib.sha1(user_salt[str(ctx.user.id)].encode('utf-8'))
        user_sha1.update(str(ctx.user.id).encode('utf-8'))
        if str(user_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('bypass')][str(ctx.guild.id)].values()) or ctx.user.guild_permissions.administrator:
            await error_code.bypass(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
        else:
            embed=discord.Embed(title=str(ctx.user)+Lang[server_data['language'][str(ctx.guild.id)]]['user-banned'], description=Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason']+'None', color=0x81FA28)
            try:
                await ctx.user.send(embed=embed)
            except: ...
            await ctx.guild.ban(ctx.user, reason='None')
            await ctx.respond(embed=embed, ephemeral=True)
            print(now_time(), str(ctx.user), Lang[server_data['language'][str(ctx.guild.id)]]['user-banned'], Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason'], 'None', Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
    else:
        await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@interClient.user_command(name = 'Kick')
async def kick_user(ctx):
    salt(ctx.user.id)
    ctx_sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
    ctx_sha1.update(str(ctx.author.id).encode('utf-8'))
    if ctx.author.guild_permissions.administrator or str(ctx_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
        user_sha1 = hashlib.sha1(user_salt[str(ctx.user.id)].encode('utf-8'))
        user_sha1.update(str(ctx.user.id).encode('utf-8'))
        if str(user_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('bypass')][str(ctx.guild.id)].values()) or ctx.user.guild_permissions.administrator:
            await error_code.bypass(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
        else:
            embed=discord.Embed(title=str(ctx.user)+Lang[server_data['language'][str(ctx.guild.id)]]['user-kicked'], description=Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason']+'None', color=0x81FA28)
            try:
                await ctx.user.send(embed=embed)
            except: ...
            await ctx.guild.kick(ctx.user, reason='None')
            await ctx.respond(embed=embed, ephemeral=True)
            print(now_time(), str(ctx.user), Lang[server_data['language'][str(ctx.guild.id)]]['user-kicked'], Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason'], 'None', Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
    else:
        await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@interClient.user_command(name = 'Mute')
async def mute_user(ctx):
    salt(ctx.user.id)
    ctx_sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
    ctx_sha1.update(str(ctx.author.id).encode('utf-8'))
    if ctx.author.guild_permissions.administrator or str(ctx_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
        user_sha1 = hashlib.sha1(user_salt[str(ctx.user.id)].encode('utf-8'))
        user_sha1.update(str(ctx.user.id).encode('utf-8'))
        if str(user_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('bypass')][str(ctx.guild.id)].values()) or ctx.user.guild_permissions.administrator:
            await error_code.bypass(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
        else:
            mutedRole = discord.utils.get(ctx.guild.roles, name=Lang[server_data['language'][str(ctx.guild.id)]]['mute-role-name'])
            all_roles = await ctx.guild.fetch_roles()
            num_roles = len(all_roles)
            if not mutedRole:
                mutedRole = await ctx.guild.create_role(name=Lang[server_data['language'][str(ctx.guild.id)]]['mute-role-name'])
                await mutedRole.edit(position=num_roles - 2)
                for channel in ctx.guild.channels:
                    await channel.set_permissions(mutedRole, speak=False, send_messages=False)
            await ctx.user.add_roles(mutedRole, reason='None')
            embed=discord.Embed(title=str(ctx.user)+Lang[server_data['language'][str(ctx.guild.id)]]['user-muted'], description=Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason']+'None', color=0x81FA28)
            await ctx.respond(embed=embed, ephemeral=True)
            await ctx.user.send(embed=embed)
            print(now_time(), str(ctx.user), Lang[server_data['language'][str(ctx.guild.id)]]['user-muted'], Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason'], 'None', Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
    else:
        await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@interClient.user_command(name = 'Warn', guild_ids = guild_id)
async def warn_user(ctx):
    salt(ctx.user.id)
    ctx_sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
    ctx_sha1.update(str(ctx.author.id).encode('utf-8'))
    if ctx.author.guild_permissions.administrator or str(ctx_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
        user_sha1 = hashlib.sha1(user_salt[str(ctx.user.id)].encode('utf-8'))
        user_sha1.update(str(ctx.user.id).encode('utf-8'))
        if str(user_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('bypass')][str(ctx.guild.id)].values()) or ctx.user.guild_permissions.administrator:
            await error_code.bypass(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
        else:
            userdata_dict = {}
            for i in range(len(userdata_keys)):
                userdata_dict[userdata_keys[i]] = userdata_values[i]
            userdata_values_dict = userdata_values[userdata_keys.index('warns')]
            userdata_new_dict = userdata_values_dict[str(ctx.guild.id)]
            try:
                userdata_new_dict[str(user_sha1.hexdigest())] = str(int(user_data['warns'][str(ctx.guild.id)][str(user_sha1.hexdigest())]) + 1)
            except:
                userdata_new_dict[str(user_sha1.hexdigest())] = '1'
            userdata_dict['warns'][str(ctx.guild.id)] = userdata_new_dict
            with open('database/userdata.json', 'w') as f:
                json.dump(userdata_dict, f, indent = 4)
            load_userdata()
            embed=discord.Embed(title=str(ctx.user)+Lang[server_data['language'][str(ctx.guild.id)]]['user-warned'], description=Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason']+'None', color=0x81FA28)
            await ctx.respond(embed=embed, ephemeral=True)
            await ctx.user.send(embed=embed)
            print(now_time(), str(ctx.user), Lang[server_data['language'][str(ctx.guild.id)]]['user-warned'], Lang[server_data['language'][str(ctx.guild.id)]]['warn-reason'], 'None', Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
            await auto_action(ctx, ctx.user, user_sha1, server_data['auto-action'][str(ctx.guild.id)])
    else:
        await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

# slash command

@interClient.slash_command(name = 'time', description="View current time")
async def slash_time(ctx):
    if server_data['commands'][str(ctx.guild.id)]['time']:
        print(ctx)
        await ctx.reply(now_time(), ephemeral=True)
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])

@interClient.slash_command(name = 'language',
                            description="Change the display language",
                            options=[
                                Option("language", "language name", OptionType.STRING)
                            ])
async def slash_chlang(ctx, language=''):
    if server_data['commands'][str(ctx.guild.id)]['chlang']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            if language == '':
                lang_search_list = []
                op = []
                num = 0
                for i in list(Lang.keys()):
                    with open('lang/'+i+'.json', 'r', encoding = "utf8") as lang_list:
                        lang_name = json.load(lang_list)
                    lang_search_list.append(i)
                    op.append(SelectOption(label=lang_name['name'], value=str(num), emoji='🔍'))
                    num += 1
                await ctx.reply(content='', components=[SelectMenu(placeholder=Lang[server_data['language'][str(ctx.guild.id)]]['menu-select'], options= op,
                                                custom_id='lang_select'
                )], ephemeral=True)
                interaction = await bot.wait_for('select_option', check = lambda inter: inter.custom_id == 'lang_select')
                res = interaction.values[0]
                for j in range(len(op)):
                    try:
                        if res == str(j):
                            serverdata_dict = {}
                            for i in range(len(serverdata_keys)):
                                serverdata_dict[serverdata_keys[i]] = serverdata_values[i]
                            serverdata_values_dict = serverdata_values[serverdata_keys.index('language')]
                            serverdata_values_dict[str(ctx.guild.id)] = lang_search_list[j]
                            serverdata_dict['language'] = serverdata_values_dict
                            with open("database/serverdata.json", "w") as serverdata_file:
                                json.dump(serverdata_dict, serverdata_file, indent = 4)
                            load_serverdata()
                            print(now_time(), Lang[server_data['language'][str(ctx.guild.id)]]['lang-changed'], language, Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
                            break
                        else:
                            continue
                    except:
                        return
            else:
                if '_' in language:
                    language = re.sub('_', '-', language)
                checked = await lang.chlang_check(ctx, language, Lang[server_data['language'][str(ctx.guild.id)]], data)
                if not checked:
                    return
                serverdata_dict = {}
                for i in range(len(serverdata_keys)):
                    serverdata_dict[serverdata_keys[i]] = serverdata_values[i]
                serverdata_values_dict = serverdata_values[serverdata_keys.index('language')]
                serverdata_values_dict[str(ctx.guild.id)] = language
                serverdata_dict['language'] = serverdata_values_dict
                with open("database/serverdata.json", "w") as serverdata_file:
                    json.dump(serverdata_dict, serverdata_file, indent = 4)
                load_serverdata()
                embed = discord.Embed(title='🇺🇳｜'+Lang[server_data['language'][str(ctx.guild.id)]]['lang-changed'], color=0x81FA28)
                await ctx.respond(embed=embed, ephemeral=True)
                print(now_time(), Lang[server_data['language'][str(ctx.guild.id)]]['lang-changed'], language, Lang[server_data['language'][str(ctx.guild.id)]]['by'], ctx.author)
        else:
            await error_code.permission(ctx, Lang[server_data['language'][str(ctx.guild.id)]])
    else:
        await error_code.command_disabled(ctx, Lang[server_data['language'][str(ctx.guild.id)]])


if __name__ == '__main__':
    web.keep_alive()
    bot.run(data['token'])


# blind, tempblind, level system, money system, tick

# join role

# online count, total conut