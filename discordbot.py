from calendar import c
import discord
from datetime import datetime
from discord.ext import commands, tasks
from discord_components import *
from discord.opus import *
from discord import FFmpegPCMAudio
import time, random, asyncio, sys, json, os, re
from ping3 import ping as pin
import logging
import socket
import tracemalloc
from pandas import Categorical
import youtube_dl, mechanize
from youtubesearchpython import VideosSearch
import wget, zipfile
import hashlib
from lib import error_code, self_test, reset

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
                 uggcf://ovg.yl/3l0ysWZ\n
    Pbclevtug © 2022 pp_punat. Nyy evtugf erfreirq.\n
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

with open('database/chatfilter.txt', "r", encoding = "utf8") as words:
    badwords = words.read().split()
#

version = '17c5ec67312c2f62b4fa014ad42c581514c9fcbdbab0637e9959fa60fa938e334fe1af631af44ecc90d3e96de196bf14edc7369932b153e033fb29ae4426bb45'
self_test.check_version(data, version)

def load_admin_bypass():
    global user_data, userdata_keys, userdata_values
    with open('database/userdata.json', "r", encoding = "utf8") as userdata_file:
        user_data = json.load(userdata_file)
    userdata_keys = list(user_data.keys())
    userdata_values = list(user_data.values())

def add_lang():
    global lang_list
    lang_list = []
    for k in os.listdir('lang'):
        if k.endswith(".json"):
            lang = k.split(".",2)
            lang_list.append(lang[0])

add_lang()
load_admin_bypass()
self_test.check(data, lang_list)

Lang = lang.lang_chose(data['language'], lang_list, data)

print(Lang['version'], data['version'])
if data['debug-mode']:
    FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    logging.basicConfig(level=logging.NOTSET, filename='BotLog.log', filemode='w', format=FORMAT)
    print(Lang['debug-enabled'])
else:
    print(Lang['debug-disabled'])

prefix = data['command-prefix']
intents = discord.Intents.all()
intents.members = True
intents.guilds = True
bot = ComponentsBot(data['command-prefix'])
bot.remove_command('help')

def now_time():
    now = datetime.now()
    date_time = '<'+now.strftime("%Y-%m-%d, %H:%M:%S")+'>'
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
    menu_1 = await ctx.send(content=Lang['menu-name'], components=[Select(placeholder=Lang['menu-select'], options= [
                                                    SelectOption(label=Lang['menu-music'], value=Lang['menu-music'], emoji='🎧'),
                                                    SelectOption(label=prefix+'addadmin', value=prefix+'addadmin', description=Lang['menu-message-addadmin'], emoji='🛠'),
                                                    SelectOption(label=prefix+'addbypass', value=prefix+'addbypass', description=Lang['menu-message-addbypass'], emoji='✅'),
                                                    SelectOption(label=prefix+'ban', value=prefix+'ban', description=Lang['menu-message-ban'], emoji='🚫'),
                                                    SelectOption(label=prefix+'clear', value=prefix+'clear', description=Lang['menu-message-clear'], emoji='🗑'),
                                                    SelectOption(label=prefix+'chlang', value=prefix+'chlang', description=Lang['menu-message-chlang'], emoji='🇺🇳'),
                                                    SelectOption(label=prefix+'chact', value=prefix+'chact', description=Lang['menu-message-chact'], emoji='🎊'),
                                                    SelectOption(label=prefix+'copy', value=prefix+'copy', description=Lang['menu-message-copy'], emoji='✂'),
                                                    SelectOption(label=prefix+'copy -d', value=prefix+'copy'+'-d', description=Lang['menu-message-copy-delete'], emoji='✂'),
                                                    SelectOption(label=prefix+'clearwarn', value=prefix+'clearwarn', description=Lang['menu-message-clearwarn'], emoji='🗑'),
                                                    SelectOption(label=prefix+'cd', value=prefix+'cd', description=Lang['menu-message-cd'], emoji='🗑'),
                                                    SelectOption(label=prefix+'ci', value=prefix+'ci', description=Lang['menu-message-ci'], emoji='😎'),
                                                    SelectOption(label=prefix+'exit', value=prefix+'exit', description=Lang['menu-message-exit'], emoji='⏹'),
                                                    SelectOption(label=prefix+'gay', value=prefix+'gay', description=Lang['menu-message-gay'], emoji='👨‍❤️‍👨'),
                                                    SelectOption(label=prefix+'kick', value=prefix+'kick', description=Lang['menu-message-kick'], emoji='🦵'),
                                                    SelectOption(label=prefix+'mute', value=prefix+'mute', description=Lang['menu-message-mute'], emoji='🔈'),
                                                    SelectOption(label=prefix+'ping', value=prefix+'ping', description=Lang['menu-message-ping'], emoji='📌'),
                                                    SelectOption(label=prefix+'reload', value=prefix+'reload', description=Lang['menu-message-reload'], emoji='🔄'),
                                                    SelectOption(label=prefix+'removeadmin', value=prefix+'removeadmin', description=Lang['menu-message-removeadmin'], emoji='🗑'),
                                                    SelectOption(label=prefix+'removebypass', value=prefix+'removebypass', description=Lang['menu-message-removebypass'], emoji='🗑'),
                                                    SelectOption(label=prefix+'showwarn', value=prefix+'showwarn', description=Lang['menu-message-showwarn'], emoji='📄'),
                                                    SelectOption(label=prefix+'slowmode', value=prefix+'slowmode', description=Lang['menu-message-slowmoe'], emoji='🐢'),
                                                    SelectOption(label=prefix+'send', value=prefix+'send', description=Lang['menu-message-send'], emoji='📨'),
                                                    SelectOption(label=prefix+'time', value=prefix+'time', description=Lang['menu-message-time'], emoji='⏱'),
                                                    SelectOption(label=Lang['next-page'], value=Lang['next-page'], emoji='➡')
                                                ],
                                                custom_id='main_menu_1'
    )])
    while True:
        interaction = await bot.wait_for('select_option', check = lambda inter: inter.custom_id == 'main_menu_1')
        res = interaction.values[0]
        try:
            if res == prefix+'time':
                await interaction.send(Lang['selected']+res)
                await time(ctx)
            elif res == prefix+'clear':
                embed = discord.Embed(title=Lang['usage'], description='', color=0xEC2E2E)
                embed.add_field(name=prefix+'clear '+Lang['count'], value=Lang['message-clear-tip']+Lang['count']+Lang['message-clear-tip-count'], inline=False)
                embed.add_field(name=prefix+'clear '+Lang['count']+Lang['@user'], value=Lang['message-clear-tip']+Lang['@user']+Lang["someone's"]+' '+Lang['count']+Lang['message-clear-tip-count'], inline=False)
                await interaction.send(embed=embed)
            elif res == prefix+'chlang':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'chlang '+Lang['language'], color=0xEC2E2E)
                embed.add_field(name=Lang['uses'], value=Lang['change-lang-message'], inline=False)
                await interaction.send(embed=embed)
            elif res == prefix+'chact':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'chact '+Lang['message'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'copy':
                await interaction.send(Lang['selected']+res)
                await copy(ctx)
            elif res == prefix+'copy'+'-d':
                await interaction.send(Lang['selected']+res)
                await copy(ctx, '-d')
            elif res == prefix+'gay':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'gay '+Lang['@user'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'exit':
                await interaction.send(Lang['selected']+res)
                await exit(ctx)
            elif res == prefix+'reload':
                await interaction.send(Lang['selected']+res)
                await reload(ctx)
            elif res == prefix+'ban':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'ban '+Lang['@user']+Lang['reason'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'kick':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'kick '+Lang['@user']+Lang['reason'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'clearwarn':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'clearwarn '+Lang['@user']+' (-a)', color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'showwarn':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'showwarn '+Lang['@user'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'addbypass':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'addbypass '+Lang['@user'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'addadmin':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'addadmin '+Lang['@user'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'removebypass':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'removebypass '+Lang['@user'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'removeadmin':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'removeadmin '+Lang['@user'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'mute':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'mute '+Lang['@user']+Lang['reason'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'slowmode':
                await interaction.send(Lang['selected']+res)
                await slowmode(ctx)
            elif res == prefix+'cd':
                await interaction.send(Lang['selected']+res)
                await cd(ctx)
            elif res == prefix+'ci':
                await interaction.send(Lang['selected']+res)
                await ci(ctx)
            elif res == prefix+'ping':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'ping [IP]', color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'send':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'send '+Lang['message'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == Lang['menu-music']:
                await menu_1.delete()
                await music_menu(ctx)
            elif res == Lang['next-page']:
                await menu_1.delete()
                await main_menu_2(ctx)
        except:
            pass
async def main_menu_2(ctx):
    menu_2 = await ctx.send(content=Lang['menu-name'], components=[Select(placeholder=Lang['menu-select'], options= [
                                                    SelectOption(label=Lang['previous-page'], value=Lang['previous-page'], emoji='⬅'),
                                                    SelectOption(label=prefix+'tlm', value=prefix+'tlm', description=Lang['menu-message-tlm'], emoji='📨'),
                                                    SelectOption(label=prefix+'tempban', value=prefix+'tempban', description=Lang['menu-message-tempban'], emoji='🚫'),
                                                    SelectOption(label=prefix+'tempmute', value=prefix+'tempmute', description=Lang['menu-message-tempmute'], emoji='🔈'),
                                                    SelectOption(label=prefix+'unban', value=prefix+'unban', description=Lang['menu-message-unban'], emoji='⭕'),
                                                    SelectOption(label=prefix+'unmute', value=prefix+'unmute', description=Lang['menu-message-unmute'], emoji='🔊'),
                                                    SelectOption(label=prefix+'uinfo', value=prefix+'uinfo', description=Lang['menu-message-uinfo'], emoji='🕵️'),
                                                    SelectOption(label=prefix+'warn', value=prefix+'warn', description=Lang['menu-message-warn'], emoji='⚠')
                                                ],
                                                custom_id='main_menu_2'
    )])
    while True:
        interaction = await bot.wait_for('select_option', check = lambda inter: inter.custom_id == 'main_menu_2')
        res = interaction.values[0]
        try:
            if res == prefix+'warn':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'warn '+Lang['@user']+Lang['reason'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'unmute':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'unmute '+Lang['@user'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'uinfo':
                await interaction.send(Lang['selected']+res)
                await uinfo(ctx)
            elif res == prefix+'unban':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'unban '+Lang['@user'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'tempmute':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'tempmute '+Lang['@user']+Lang['duration']+Lang['reason'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'tempban':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'tempban '+Lang['@user']+Lang['duration']+Lang['reason'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'tlm':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'tlm '+Lang['message'], color=0xEC2E2E)
                embed.add_field(name=Lang['uses'], value=Lang['temp-message'], inline=False)
                await interaction.send(embed=embed)
            elif res == Lang['previous-page']:
                await menu_2.delete()
                await main_menu_1(ctx)
        except:
            pass
async def music_menu(ctx):
    await ctx.send(content=Lang['menu-music-name'], components=[Select(placeholder=Lang['menu-select'], options= [
                                                    SelectOption(label=prefix+'play', value=prefix+'play', description=Lang['menu-message-play'], emoji='▶'),
                                                    SelectOption(label=prefix+'leave', value=prefix+'leave', description=Lang['menu-message-leave'], emoji='⏹'),
                                                    SelectOption(label=prefix+'pause', value=prefix+'pause', description=Lang['menu-message-pause'], emoji='⏸'),
                                                    SelectOption(label=prefix+'resume', value=prefix+'resume', description=Lang['menu-message-resume'], emoji='⏯'),
                                                    SelectOption(label=prefix+'repeat', value=prefix+'repeat', description=Lang['menu-message-repeat'], emoji='🔁'),
                                                    SelectOption(label=prefix+'stop', value=prefix+'stop', description=Lang['menu-message-stop'], emoji='⏹'),
                                                    SelectOption(label=prefix+'volume', value=prefix+'volume', description=Lang['menu-message-volume'], emoji='🔊'),
                                                    SelectOption(label=prefix+'skip', value=prefix+'skip', description=Lang['menu-message-skip'], emoji='⏩'),
                                                    SelectOption(label=prefix+'playlist', value=prefix+'playlist', description=Lang['menu-message-playlist'], emoji='📜'),
                                                    SelectOption(label=prefix+'listmove', value=prefix+'listmove', description=Lang['menu-message-listmove'], emoji='🔃'),
                                                    SelectOption(label=prefix+'listremove', value=prefix+'listremove', description=Lang['menu-message-listremove'], emoji='🗑'),
                                                    SelectOption(label=prefix+'listrandom', value=prefix+'listrandom', description=Lang['menu-message-listrandom'], emoji='🔀'),
                                                    SelectOption(label=prefix+'favorite add', value=prefix+'favorite add', description=Lang['favorite-menu-add'], emoji='💕'),
                                                    SelectOption(label=prefix+'favorite remove', value=prefix+'favorite remove', description=Lang['favorite-menu-remove'], emoji='🗑'),
                                                    SelectOption(label=prefix+'favorite list', value=prefix+'favorite list', description=Lang['favorite-menu-list'], emoji='📜'),
                                                    SelectOption(label=prefix+'favorite play', value=prefix+'favorite play', description=Lang['favorite-menu-play'], emoji='▶')
                                                ],
                                                custom_id='music_menu'
    )])

@bot.event
async def on_ready():
    print(now_time(), Lang['login-name'], bot.user)
    if data['custom-activity'] != '':
        game = discord.Game(data['custom-activity'])
    else:
        game = discord.Game(now_time())
    #online,offline,idle,dnd,invisible
    if data['custom-status'] == 'offline':
        await bot.change_presence(status=discord.Status.offline, activity=game)
    elif data['custom-status'] == 'idle':
        await bot.change_presence(status=discord.Status.idle, activity=game)
    elif data['custom-status'] == 'dnd':
        await bot.change_presence(status=discord.Status.dnd, activity=game)
    elif data['custom-status'] == 'invisible':
        await bot.change_presence(status=discord.Status.invisible, activity=game)
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.event
async def on_voice_state_update(member, before, after):
    channel = after.channel
    try:
        if before.channel.members == [] and not before.channel.id == data['enter-private-voice-channel-id']:
            if before.channel.category_id == int(data['private-voice-category-id']) and before.channel.name == member.name + Lang['create-channel-name']:
                await before.channel.delete()
    except:
        pass
    if channel == None:
        return
    if channel.id == int(data['enter-private-voice-channel-id']):
        guild = after.channel.guild
        private_channels = discord.utils.get(guild.categories, id= data['private-voice-category-id'])
        voice_channel = await guild.create_voice_channel(member.name + Lang['create-channel-name'], overwrites=None, category=private_channels, user_limit = 5)
        await member.move_to(voice_channel)
        await voice_channel.set_permissions(member, manage_channels=True, manage_permissions=True)
        print(now_time(), member, Lang['when-channel-create'])

@bot.command()
async def menu(ctx, page: str='1'):
    if page == '1':
        await main_menu_1(ctx)
    elif page == '2':
        await main_menu_2(ctx)
    elif page == 'music':
        await music_menu(ctx)

@bot.command()
async def addadmin(ctx, user: discord.Member=None):
    if data['commands']['addadmin']:
        if ctx.author.guild_permissions.administrator:
            global userdata_keys, userdata_values
            if not user:
                embed = discord.Embed(title=Lang['usage'], description=prefix+'addadmin '+Lang['@user'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed, delete_after=5)
                return
            salt(user.id)
            sha1 = hashlib.sha1(user_salt[str(user.id)].encode('utf-8'))
            sha1.update(str(user.id).encode('utf-8'))
            sha512= hashlib.sha512()
            sha512.update(str(user).encode('utf-8'))
            if str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()) or user.guild_permissions.administrator:
                embed=discord.Embed(title='❌｜'+Lang['admin-had'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed)
            else:
                userdata_dict = {}
                userdata_values_dict = {}
                userdata_new_dict = {}
                with open('database/userdata.json', "r", encoding = "utf8") as userdata_file:
                    user_data = json.load(userdata_file)
                userdata_keys = list(user_data.keys())
                userdata_values = list(user_data.values())
                for i in range(len(userdata_keys)):
                    userdata_dict[userdata_keys[i]] = userdata_values[i]
                userdata_values_dict = userdata_values[userdata_keys.index('admin')]
                userdata_new_dict = userdata_values_dict[str(ctx.guild.id)]
                userdata_new_dict[str(sha512.hexdigest())] = str(sha1.hexdigest())
                userdata_dict['admin'][str(ctx.guild.id)] = userdata_new_dict
                with open("database/userdata.json", "w") as userdata_file:
                    json.dump(userdata_dict, userdata_file, indent = 4)
                load_admin_bypass()
                embed=discord.Embed(title=str(user)+Lang['admin-added'], color=0x81FA28)
                await ctx.channel.send(embed=embed)
                print(now_time(), str(user)+Lang['admin-added'])
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def addbypass(ctx, user: discord.Member=None):
    if data['commands']['addbypass']:
        if ctx.author.guild_permissions.administrator:
            global userdata_keys, userdata_values
            if not user:
                embed = discord.Embed(title=Lang['usage'], description=prefix+'addbypass '+Lang['@user'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed, delete_after=5)
            salt(user.id)
            sha1 = hashlib.sha1(user_salt[str(user.id)].encode('utf-8'))
            sha1.update(str(user.id).encode('utf-8'))
            sha512= hashlib.sha512()
            sha512.update(str(user).encode('utf-8'))
            if str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('bypass')][str(ctx.guild.id)].values()) or user.guild_permissions.administrator:
                embed=discord.Embed(title='❌｜'+Lang['bypass-had'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed)
            else:
                userdata_dict = {}
                userdata_values_dict = {}
                userdata_new_dict = {}
                with open('database/userdata.json', "r", encoding = "utf8") as userdata_file:
                    user_data = json.load(userdata_file)
                userdata_keys = list(user_data.keys())
                userdata_values = list(user_data.values())
                for i in range(len(userdata_keys)):
                    userdata_dict[userdata_keys[i]] = userdata_values[i]
                userdata_values_dict = userdata_values[userdata_keys.index('bypass')]
                userdata_new_dict = userdata_values_dict[str(ctx.guild.id)]
                userdata_new_dict[str(sha512.hexdigest())] = str(sha1.hexdigest())
                userdata_dict['bypass'][str(ctx.guild.id)] = userdata_new_dict
                with open("database/userdata.json", "w") as userdata_file:
                    json.dump(userdata_dict, userdata_file, indent = 4)
                load_admin_bypass()
                embed=discord.Embed(title=str(user)+Lang['bypass-added'], color=0x81FA28)
                await ctx.channel.send(embed=embed)
                print(now_time(), str(user)+Lang['bypass-added'])
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def ban(ctx, user: discord.Member=None, options='None', *, reason='None'):
    if data['commands']['ban']:
        ctx_sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        ctx_sha1.update(str(ctx.author.id).encode('utf-8'))
        user_sha1 = hashlib.sha1(user_salt[str(user.id)].encode('utf-8'))
        user_sha1.update(str(user.id).encode('utf-8'))
        await ctx.message.delete()
        if not user:
            embed = discord.Embed(title=Lang['usage'], description=prefix+'ban '+Lang['@user']+Lang['reason'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed, delete_after=5)
        elif options == '--sync' and ctx.author.id == data['owner-id']:
            embed=discord.Embed(title=str(user)+Lang['user-banned'], description=Lang['warn-reason']+reason, color=0x81FA28)
            try:
                await user.send(embed=embed)
            except:
                pass
            await ctx.guild.ban(user, reason=reason)
            await ctx.channel.send(embed=embed)
            print(now_time(), str(user), Lang['user-banned'], Lang['warn-reason'], reason)
        elif ctx.author.guild_permissions.administrator or str(ctx_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            if str(user_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('bypass')][str(ctx.guild.id)].values()) or user.guild_permissions.administrator:
                await error_code.bypass(ctx, Lang)
            else:
                embed=discord.Embed(title=str(user)+Lang['user-banned'], description=Lang['warn-reason']+options, color=0x81FA28)
                try:
                    await user.send(embed=embed)
                except:
                    pass
                await ctx.guild.ban(user, reason=reason)
                await ctx.channel.send(embed=embed)
                print(now_time(), str(user), Lang['user-banned'], Lang['warn-reason'], options)
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def clear(ctx, limit=0, member: discord.Member=None):
    if data['commands']['clear']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            await ctx.message.delete()
            if limit == 0:
                embed = discord.Embed(title=Lang['usage'], description='', color=0xEC2E2E)
                embed.add_field(name=prefix+'clear '+Lang['count'], value=Lang['message-clear-tip']+Lang['count']+Lang['message-clear-tip-count'], inline=False)
                embed.add_field(name=prefix+'clear '+Lang['count']+Lang['@user'], value=Lang['message-clear-tip']+Lang['@user']+Lang["someone's"]+' '+Lang['count']+Lang['message-clear-tip-count'], inline=False)
                await ctx.channel.send(embed=embed, delete_after=3)
                return
            msg = []
            if not member:
                try:
                    await ctx.channel.purge(limit=limit)
                except:
                    pass
                print(now_time(), str(limit), Lang['message-cleared'])
                embed = discord.Embed(title='🗑｜'+str(limit)+Lang['message-cleared'], color=0x81FA28)
                await ctx.channel.send(embed=embed, delete_after=3)
                return
            async for m in ctx.channel.history():
                if len(msg) == limit:
                    break
                if m.author == member:
                    msg.append(m)
            await ctx.channel.delete_messages(msg)
            embed = discord.Embed(title='🗑｜'+str(member)+Lang["someone's"]+' '+str(limit)+Lang['message-cleared'], color=0x81FA28)
            await ctx.channel.send(embed=embed, delete_after=3)
            print(now_time(), str(member), Lang["someone's"], str(limit), Lang['message-cleared'])
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def chlang(ctx, language=''):
    global Lang
    if data['commands']['chlang']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            await ctx.message.delete()
            if language == '':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'chlang '+Lang['language'], color=0xEC2E2E)
                embed.add_field(name=Lang['uses'], value=Lang['change-lang-message'], inline=False)
                await ctx.channel.send(embed=embed, delete_after=5)
            else:
                checked = await lang.chlang_check(ctx, language, Lang, data)
                if not checked:
                    return
                chlang = 'lang/'+language+'.json'
                with open(chlang, "r", encoding = "utf8") as lang_file:
                    Lang = json.load(lang_file)
                embed = discord.Embed(title='🇺🇳｜'+Lang['lang-changed'], color=0x81FA28)
                await ctx.channel.send(embed=embed)
                print(now_time(), Lang['lang-changed'], language)
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def chact(ctx, *, act=''):
    if data['commands']['chact']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            await ctx.message.delete()
            if act == '':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'chact '+Lang['message'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed, delete_after=5)
            else:
                game = discord.Game(act)
                await bot.change_presence(status=discord.Status.online, activity=game)
                await ctx.channel.send(Lang['activity-changed']+' '+act)
                print(now_time(), Lang['activity-changed'], act)
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def copy(ctx, delete=''):
    if data['commands']['copy']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            await ctx.message.delete()
            if delete == '':
                await ctx.channel.clone()
                print(now_time(), ctx.channel, Lang['channel-copied'])
            elif delete == '-d':
                await ctx.channel.clone()
                await ctx.channel.delete()
                print(now_time(), ctx.channel, Lang['channel-copied-deleted'])
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def clearwarn(ctx, member: discord.Member=None, options=''):
    if data['commands']['clearwarn']:
        ctx_sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        ctx_sha1.update(str(ctx.author.id).encode('utf-8'))
        member_sha1 = hashlib.sha1(user_salt[str(member.id)].encode('utf-8'))
        member_sha1.update(str(member.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(ctx_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            if not member:
                embed = discord.Embed(title=Lang['usage'], description=prefix+'clearwarn '+Lang['@user']+' (-a)', color=0xEC2E2E)
                await ctx.channel.send(embed=embed, delete_after=5)
            else:
                if int(user_data['warns'][str(ctx.guild.id)][str(member_sha1.hexdigest())]) == 0:
                    await ctx.channel.send(Lang['user-nowarn'])
                    return
                else:
                    with open('database/userdata.json', 'w') as f:
                        json.dump(user_data, f, indent = 4)
                    clearwarn_dict = {}
                    clearwarn_values_dict = {}
                    clearwarn_new_dict = {}
                    if options == '':
                        for i in range(len(userdata_keys)):
                            clearwarn_dict[userdata_keys[i]] = userdata_values[i]
                        clearwarn_values_dict = userdata_values[userdata_keys.index('warns')]
                        clearwarn_new_dict = clearwarn_values_dict[str(ctx.guild.id)]
                        clearwarn_new_dict[str(member_sha1.hexdigest())] = str(int(user_data['warns'][str(ctx.guild.id)][str(member_sha1.hexdigest())]) - 1)
                        clearwarn_dict['warns'][str(ctx.guild.id)] = clearwarn_new_dict
                        with open('database/userdata.json', 'w') as f:
                            json.dump(clearwarn_dict, f, indent = 4)
                        load_admin_bypass()
                        embed = discord.Embed(title=member.name+Lang['warn-amount']+user_data['warns'][str(ctx.guild.id)][str(member_sha1.hexdigest())], color=0xEC2E2E)
                        await ctx.channel.send(embed=embed)
                        print(now_time(), str(member), Lang['warn-amount'], user_data['warns'][str(ctx.guild.id)][str(member_sha1.hexdigest())])
                    elif options == '-a':
                        user_data['warns'][str(ctx.guild.id)][str(member_sha1.hexdigest())] = '0'
                        with open('database/userdata.json', 'w') as f:
                            json.dump(user_data, f, indent = 4)
                        load_admin_bypass()
                        embed = discord.Embed(title=member.name+Lang['warn-cleared-all'], color=0xEC2E2E)
                        await ctx.channel.send(embed=embed)
                        print(now_time(), str(member), Lang['warn-cleared-all'])
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def cd(ctx):
    if data['commands']['cd']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            await ctx.channel.delete()
            print(now_time(), ctx.channel, Lang['channel-deleted'])
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def ci(ctx):
    if data['commands']['ci']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            await ctx.message.delete()
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False, view_channel=False)
            await ctx.send(Lang['channel-invisibled'])
            print(now_time(), ctx.channel, Lang['channel-invisibled'])
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def exit(ctx):
    if data['commands']['exit']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            if ctx.author.id != data['owner-id']:
                await ctx.send(Lang['not-owner'], delete_after=3)
                return
            await ctx.message.delete()
            game = discord.Game(now_time())
            await bot.change_presence(status=discord.Status.offline, activity=game)
            sys.exit()
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def gay(ctx, member: discord.Member=None):
    if data['commands']['gay']:
        if member == None:
            embed = discord.Embed(title=Lang['usage'], description=prefix+'gay '+Lang['@user'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed, delete_after=5)
            await asyncio.sleep(5)
            await ctx.message.delete()
        else:
            embed = discord.Embed(title=str(random.randrange(100))+'% gay', color=0x4b49d8)
            embed.set_author(name=member, icon_url=member.avatar_url)
            await ctx.channel.send(embed=embed, delete_after=5)
            await asyncio.sleep(5)
            await ctx.message.delete()

@bot.command()
async def kick(ctx, user: discord.Member=None, options='None', *, reason='None'):
    if data['commands']['kick']:
        ctx_sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        ctx_sha1.update(str(ctx.author.id).encode('utf-8'))
        user_sha1 = hashlib.sha1(user_salt[str(user.id)].encode('utf-8'))
        user_sha1.update(str(user.id).encode('utf-8'))
        await ctx.message.delete()
        if not user:
            embed = discord.Embed(title=Lang['usage'], description=prefix+'kick '+Lang['@user']+Lang['reason'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed, delete_after=5)
        elif options == '--sync' and ctx.author.id == data['owner-id']:
            embed=discord.Embed(title=str(user)+Lang['user-kicked'], description=Lang['warn-reason']+reason, color=0x81FA28)
            try:
                await user.send(embed=embed)
            except:
                pass
            await ctx.guild.kick(user)
            await ctx.channel.send(embed=embed)
            print(now_time(), str(user), Lang['user-kicked'], Lang['warn-reason'], reason)
        elif ctx.author.guild_permissions.administrator or str(ctx_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            if str(user_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('bypass')][str(ctx.guild.id)].values()) or user.guild_permissions.administrator:
                await error_code.bypass(ctx, Lang)
            else:
                embed=discord.Embed(title=str(user)+Lang['user-kicked'], description=Lang['warn-reason']+options, color=0x81FA28)
                try:
                    await user.send(embed=embed)
                except:
                    pass
                await ctx.guild.kick(user)
                await ctx.channel.send(embed=embed)
                print(now_time(), str(user), Lang['user-kicked'], Lang['warn-reason'], options)
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def mute(ctx, user: discord.Member=None, options='None', *, reason='None'):
    if data['commands']['mute']:
        ctx_sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        ctx_sha1.update(str(ctx.author.id).encode('utf-8'))
        user_sha1 = hashlib.sha1(user_salt[str(user.id)].encode('utf-8'))
        user_sha1.update(str(user.id).encode('utf-8'))
        if not user:
            embed = discord.Embed(title=Lang['usage'], description=prefix+'mute '+Lang['@user']+Lang['reason'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed, delete_after=5)
        elif options == '--sync' and ctx.author.id == data['owner-id']:
            guild = ctx.guild
            mutedRole = discord.utils.get(guild.roles, name=Lang['mute-role-name'])
            all_roles = await guild.fetch_roles()
            num_roles = len(all_roles)
            if not mutedRole:
                mutedRole = await guild.create_role(name=Lang['mute-role-name'])
                await mutedRole.edit(position=num_roles - 2)
                for channel in guild.channels:
                    await channel.set_permissions(mutedRole, speak=False, send_messages=False)
            await user.add_roles(mutedRole, reason=reason)
            embed=discord.Embed(title=str(user)+Lang['user-muted'], description=Lang['warn-reason']+reason, color=0x81FA28)
            await ctx.channel.send(embed=embed)
            await user.send(embed=embed)
            print(now_time(), str(user), Lang['user-muted'], Lang['warn-reason'], reason)
        elif ctx.author.guild_permissions.administrator or str(ctx_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            if str(user_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('bypass')][str(ctx.guild.id)].values()) or user.guild_permissions.administrator:
                await error_code.bypass(ctx, Lang)
            else:
                guild = ctx.guild
                mutedRole = discord.utils.get(guild.roles, name=Lang['mute-role-name'])
                all_roles = await guild.fetch_roles()
                num_roles = len(all_roles)
                if not mutedRole:
                    mutedRole = await guild.create_role(name=Lang['mute-role-name'])
                    await mutedRole.edit(position=num_roles - 2)
                    for channel in guild.channels:
                        await channel.set_permissions(mutedRole, speak=False, send_messages=False)
                await user.add_roles(mutedRole, reason=options)
                embed=discord.Embed(title=str(user)+Lang['user-muted'], description=Lang['warn-reason']+options, color=0x81FA28)
                await ctx.channel.send(embed=embed)
                await user.send(embed=embed)
                print(now_time(), str(user), Lang['user-muted'], Lang['warn-reason'], options)
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def ping(ctx, ip: str='', options=''):
    if data['commands']['ping']:
        if ip == '':
            embed = discord.Embed(title=Lang['usage'], description=prefix+'ping [IP]', color=0xEC2E2E)
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
                        info += Lang['reply_from']+host_ip+Lang['bytes_time']+delay+' TTL='+TTL+'\n'
                        await asyncio.sleep(response)
                        suc += 1
                        ms += int(response*1000)
                    else:
                        host_ip = ''
                        info += Lang['ping-timeout']+'\n'
                        ping_list.append('N/A')
                        fail += 1
                ping_list.sort()
                embed = discord.Embed(title='Ping '+ip+' ['+host_ip+']: '+Lang['with_32_bytes']+':', description=info, color=0x00AAAA)
                embed.add_field(name=Lang['ping_stat'], value=Lang['packet']+str(suc)+Lang['lost']+str(fail)+' ('+str(int(fail/4*100))+Lang['lost_%']+')', inline=False)
                embed.add_field(name=Lang['round_trip_times'], value=Lang['minimum']+ping_list[0]+Lang['maximum']+ping_list[-1]+Lang['average']+str(int(ms/4))+'ms', inline=False)
                await ctx.send(embed=embed)
            else:
                response = pin(ip)
                if response:
                    host_ip = socket.gethostbyname(ip)
                    delay = str(int(response*1000))+'ms'
                    info += Lang['reply_from']+host_ip+Lang['bytes_time']+delay+' TTL='+TTL+'\n'
                    embed = discord.Embed(title='Ping '+ip+' ['+host_ip+']: '+Lang['with_32_bytes']+':', description=info, color=0x00AAAA)
                    await ctx.send(embed=embed)
                else:
                    try:
                        host_ip = socket.gethostbyname(ip)
                    except:
                        host_ip = ''
                    delay = Lang['ping-timeout']
                    embed = discord.Embed(title='Ping '+ip+' ['+host_ip+']: '+Lang['with_32_bytes']+':', description=delay, color=0x00AAAA)
                    await ctx.send(embed=embed)

@bot.command()
async def RESET(ctx):
    if data['command-reset']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            if ctx.author.id != data['owner-id']:
                await ctx.send(Lang['not-owner'], delete_after=3)
                return
            if not data['debug-mode']:
                await ctx.send(Lang['reset-error'], delete_after=3)
                return
            else:
                reset_confirm = await ctx.reply(Lang['RESET-confirm'], components = [[
                    Button(label=Lang['RESET-confirm-button'], style='3', custom_id='confirm'),
                    Button(label=Lang['RESET-cancel-button'], style='4', custom_id='cancel')
                ]])
                interaction = await bot.wait_for('button_click', check = lambda inter: inter.user == ctx.author)
                res = interaction.custom_id
                if res == 'confirm':
                    await reset_confirm.delete()
                    await interaction.send(Lang['RESET-resetted'])
                    reset.reset_config()
                    sys.exit()
                else:
                    await reset_confirm.delete()
                    await interaction.send(Lang['RESET-canceled'])
        else:
            await error_code.permission(ctx, Lang)
        
@bot.command()
async def reload(ctx):
    global data, prefix, Lang, badwords
    if data['commands']['reload']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            await ctx.message.delete()
            add_lang()
            load_admin_bypass()
            data = json.load(open('config.json'))
            prefix = data['command-prefix']
            Lang = lang.lang_chose(data['language'], lang_list, data)
            with open('database/chatfilter.txt', "r", encoding = "utf8") as words:
                badwords = words.read().split()
            if data['custom-activity'] != '':
                game = discord.Game(data['custom-activity'])
            else:
                game = discord.Game(now_time())
            await bot.change_presence(status=discord.Status.online, activity=game)
            try:
                embed = discord.Embed(title='🔄｜'+Lang['reloaded'], color=0x81FA28)
                await ctx.channel.send(embed=embed)
                print(now_time(), Lang['reloaded'])
            except:
                print(now_time(), 'Could not pass language setting, end the bot!')
                embed = discord.Embed(title='⚠｜ Could not pass language setting, end the bot!', color=0xEC2E2E)
                await ctx.send(embed=embed)
                self_test.error()
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def removeadmin(ctx, user: discord.Member=None):
    if data['commands']['removeadmin']:
        if ctx.author.guild_permissions.administrator:
            if not user:
                embed = discord.Embed(title=Lang['usage'], description=prefix+'removeadmin '+Lang['@user'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed, delete_after=5)
            else:
                userdata_dict = {}
                with open('database/userdata.json', "r", encoding = "utf8") as userdata_file:
                    user_data = json.load(userdata_file)
                userdata_keys = list(user_data.keys())
                userdata_values = list(user_data.values())
                try:
                    sha512= hashlib.sha512()
                    sha512.update(str(user).encode('utf-8'))
                    del user_data['admin'][str(ctx.guild.id)][str(sha512.hexdigest())]
                    for i in range(len(userdata_keys)):
                        userdata_dict[userdata_keys[i]] = userdata_values[i]
                    with open("database/userdata.json", "w") as userdata_file:
                        json.dump(userdata_dict, userdata_file, indent = 4)
                    load_admin_bypass()
                    embed=discord.Embed(title=str(user)+Lang['admin-removed'], color=0x81FA28)
                    await ctx.channel.send(embed=embed)
                    print(now_time(), str(user)+Lang['admin-removed'])
                except:
                    embed=discord.Embed(title='❌｜'+Lang['not-in-admin'], color=0xEC2E2E)
                    await ctx.channel.send(embed=embed)
                    print(now_time(), Lang['not-in-admin'])
                
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def removebypass(ctx, user: discord.Member=None):
    if data['commands']['removebypass']:
        if ctx.author.guild_permissions.administrator:
            if not user:
                embed = discord.Embed(title=Lang['usage'], description=prefix+'removebypass '+Lang['@user'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed, delete_after=5)
            else:
                userdata_dict = {}
                with open('database/userdata.json', "r", encoding = "utf8") as userdata_file:
                    user_data = json.load(userdata_file)
                userdata_keys = list(user_data.keys())
                userdata_values = list(user_data.values())
                try:
                    sha512= hashlib.sha512()
                    sha512.update(str(user).encode('utf-8'))
                    del user_data['bypass'][str(ctx.guild.id)][str(sha512.hexdigest())]
                    for i in range(len(userdata_keys)):
                        userdata_dict[userdata_keys[i]] = userdata_values[i]
                    with open("database/userdata.json", "w") as userdata_file:
                        json.dump(userdata_dict, userdata_file, indent = 4)
                    load_admin_bypass()
                    embed=discord.Embed(title=str(user)+Lang['bypass-removed'], color=0x81FA28)
                    await ctx.channel.send(embed=embed)
                    print(now_time(), str(user)+Lang['bypass-removed'])
                except:
                    embed=discord.Embed(title='❌｜'+Lang['not-in-bypass'], color=0xEC2E2E)
                    await ctx.channel.send(embed=embed)
                    print(now_time(), Lang['not-in-bypass'])
                
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def showwarn(ctx, member: discord.Member=None):
    if data['commands']['showwarn']:
        ctx_sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        ctx_sha1.update(str(ctx.author.id).encode('utf-8'))
        member_sha1 = hashlib.sha1(user_salt[str(member.id)].encode('utf-8'))
        member_sha1.update(str(member.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(ctx_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            if not member:
                embed = discord.Embed(title=Lang['usage'], description=prefix+'showwarn '+Lang['@user'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed, delete_after=5)
            else:
                embed = discord.Embed(title=member.name+Lang['warn-amount']+user_data['warns'][str(ctx.guild.id)][str(member_sha1.hexdigest())], color=0xEC2E2E)
                await ctx.channel.send(embed=embed)
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def slowmode(ctx, seconds: int=0):
    if data['commands']['slowmode']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            await ctx.channel.edit(slowmode_delay=seconds)
            embed = discord.Embed(title=Lang['slowmode-message']+str(seconds)+Lang['slowmode-seconds'], color=0xEC2E2E)
            await ctx.send(embed=embed) 
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def send(ctx, user: discord.Member=None, *, message=''):
    if data['commands']['send']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        await ctx.message.delete()
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            if message == '':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'send '+Lang['message'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed, delete_after=5)
            else:
                try:
                    await user.send(message)
                except:
                    embed = discord.Embed(title='❌｜'+Lang['send-fail'], color=0xEC2E2E)
                    await ctx.channel.send(embed=embed, delete_after=5)
                else:
                    embed = discord.Embed(title='📨｜'+Lang['send-success'], color=0x81FA28)
                    await ctx.channel.send(embed=embed, delete_after=5)
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def time(ctx):
    if data['commands']['time']:
        await ctx.reply(now_time(), mention_author=True)

@bot.command()
async def tlm(ctx, seconds: int=600, *,  message=''):
    if data['commands']['tlm']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            await ctx.message.delete()
            if message == '':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'tlm '+Lang['message'], color=0xEC2E2E)
                embed.add_field(name=Lang['uses'], value=Lang['temp-message'], inline=False)
                await ctx.channel.send(embed=embed, delete_after=5)
            else:
                await ctx.channel.send(message, delete_after=seconds)
                print(now_time(), ctx.author,Lang['sent-temp-message'],message)
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def tempmute(ctx, user: discord.Member=None, duration='0s', options='None', *, reason='None'):
    if data['commands']['tempmute']:
        ctx_sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        ctx_sha1.update(str(ctx.author.id).encode('utf-8'))
        user_sha1 = hashlib.sha1(user_salt[str(user.id)].encode('utf-8'))
        user_sha1.update(str(user.id).encode('utf-8'))
        if not user:
            embed = discord.Embed(title=Lang['usage'], description=prefix+'tempmute '+Lang['@user']+Lang['duration']+Lang['reason'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed, delete_after=5)
        elif options == '--sync' and ctx.author.id == data['owner-id']:
            guild = ctx.guild
            mutedRole = discord.utils.get(guild.roles, name=Lang['mute-role-name'])
            all_roles = await guild.fetch_roles()
            num_roles = len(all_roles)
            if not mutedRole:
                mutedRole = await guild.create_role(name=Lang['mute-role-name'])
                await mutedRole.edit(position=num_roles - 2)
                for channel in guild.channels:
                    await channel.set_permissions(mutedRole, speak=False, send_messages=False)
            await user.add_roles(mutedRole, reason=reason)
            embed=discord.Embed(title=str(user)+Lang['user-tempmuted'], description=Lang['warn-reason']+reason, color=0x81FA28)
            await ctx.channel.send(embed=embed)
            await user.send(embed=embed)
            print(now_time(), str(user), Lang['user-tempmuted'], Lang['warn-reason'], reason)
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
            if str(user_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('bypass')][str(ctx.guild.id)].values()) or user.guild_permissions.administrator:
                await error_code.bypass(ctx, Lang)
            else:
                guild = ctx.guild
                mutedRole = discord.utils.get(guild.roles, name=Lang['mute-role-name'])
                all_roles = await guild.fetch_roles()
                num_roles = len(all_roles)
                if not mutedRole:
                    mutedRole = await guild.create_role(name=Lang['mute-role-name'])
                    await mutedRole.edit(position=num_roles - 2)
                    for channel in guild.channels:
                        await channel.set_permissions(mutedRole, speak=False, send_messages=False)
                await user.add_roles(mutedRole, reason=options)
                embed=discord.Embed(title=str(user)+Lang['user-tempmuted'], description=Lang['warn-reason']+options, color=0x81FA28)
                await ctx.channel.send(embed=embed)
                await user.send(embed=embed)
                print(now_time(), str(user), Lang['user-tempmuted'], Lang['warn-reason'], options)
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
            await error_code.permission(ctx, Lang)

@bot.command()
async def tempban(ctx, user: discord.Member=None, duration='0s', options='None', *, reason='None'):
    if data['commands']['tempban']:
        ctx_sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        ctx_sha1.update(str(ctx.author.id).encode('utf-8'))
        user_sha1 = hashlib.sha1(user_salt[str(user.id)].encode('utf-8'))
        user_sha1.update(str(user.id).encode('utf-8'))
        if not user:
            embed = discord.Embed(title=Lang['usage'], description=prefix+'tempban '+Lang['@user']+Lang['duration']+Lang['reason'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed, delete_after=5)
        elif options == '--sync' and ctx.author.id == data['owner-id']:
            embed=discord.Embed(title=str(user)+Lang['user-tempbanned'], description=Lang['warn-reason']+options, color=0x81FA28)
            try:
                await user.send(embed=embed)
            except:
                pass
            await ctx.guild.ban(user, reason=reason)
            await ctx.channel.send(embed=embed)
            print(now_time(), str(user), Lang['user-tempbanned'], Lang['warn-reason'], options)
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
            if str(user_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('bypass')][str(ctx.guild.id)].values()) or user.guild_permissions.administrator:
                await error_code.bypass(ctx, Lang)
            else:
                embed=discord.Embed(title=str(user)+Lang['user-tempbanned'], description=Lang['warn-reason']+options, color=0x81FA28)
                try:
                    await user.send(embed=embed)
                except:
                    pass
                await ctx.guild.ban(user, reason=reason)
                await ctx.channel.send(embed=embed)
                print(now_time(), str(user), Lang['user-tempbanned'], Lang['warn-reason'], options)
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
            await error_code.permission(ctx, Lang)

@bot.command()
async def unban(ctx, user: discord.User=None):
    if data['commands']['unban']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        await ctx.message.delete()
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            if not user:
                embed = discord.Embed(title=Lang['usage'], description=prefix+'unban '+Lang['@user'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed, delete_after=5)
            else:
                try:
                    guild = ctx.guild
                    await guild.unban(user)
                    embed = discord.Embed(title=str(user)+Lang['user-unbanned'])
                    await ctx.channel.send(embed=embed)
                    print(now_time(), str(user), Lang['user-unbanned'])
                except:
                    embed = discord.Embed(title='❌｜'+Lang['user-not-banned'], color=0xEC2E2E)
                    await ctx.channel.send(embed=embed)
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def unmute(ctx, user: discord.Member=None):
    if data['commands']['unmute']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        if ctx.author.guild_permissions.administrator or str(sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            if not user:
                embed = discord.Embed(title=Lang['usage'], description=prefix+'unmute '+Lang['@user'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed, delete_after=5)
            else:
                mutedRole = discord.utils.get(ctx.guild.roles, name=Lang['mute-role-name'])
                await user.remove_roles(mutedRole)
                embed=discord.Embed(title=str(user)+Lang['user-unmuted'], color=0x81FA28)
                await ctx.channel.send(embed=embed)
                await user.send(embed=embed)
                print(now_time(), str(user), Lang['user-unmuted'])
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def uinfo(ctx, target: discord.Member=None):
    if data['commands']['uinfo']:
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
            embed = discord.Embed(title='🔍｜'+Lang['user-info'], colour=target.colour, timestamp=datetime.utcnow())
            embed.set_thumbnail(url=target.avatar_url)

            fields = [(Lang['user-info-name'], str(target), True),
                        (Lang['user-info-nickname'], target.nick, True),
	        			(Lang['user-info-id'], target.id, True),
                        (Lang['user-info-permission'], target.guild_permissions.value, True),
	        			(Lang['user-info-bot'], target.bot, True),
	        			(Lang['user-info-toprole'], target.top_role.mention, True),
                        (Lang['user-info-warn'], amount, True),
	        			(Lang['user-info-status'], str(target.status).title(), True),
	        			(Lang['user-info-activity'], f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} {target.activity.name if target.activity else ''}", True),
                        (Lang['user-info-create-at'], target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                        (Lang['user-info-join-at'], target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
	        		    (Lang['user-info-boots'], bool(target.premium_since), True)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await ctx.send(embed=embed)
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def warn(ctx, user: discord.Member=None, options='None', *, reason='None'):
    if data['commands']['warn']:
        salt(user.id)
        ctx_sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        ctx_sha1.update(str(ctx.author.id).encode('utf-8'))
        user_sha1 = hashlib.sha1(user_salt[str(user.id)].encode('utf-8'))
        user_sha1.update(str(user.id).encode('utf-8'))
        if not user:
            embed = discord.Embed(title=Lang['usage'], description=prefix+'warn '+Lang['@user']+Lang['reason'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed, delete_after=5)
        elif options == '--sync' and ctx.author.id == data['owner-id']:
            with open('database/userdata.json', 'r') as f:
                warns = json.load(f)
            warns_keys = list(warns.keys())
            warns_values = list(warns.values())
            warns_dict = {}
            warn_values_dict = {}
            warn_new_dict = {}
            for i in range(len(warns_keys)):
                warns_dict[warns_keys[i]] = warns_values[i]

            warn_values_dict = warns_values[warns_keys.index('warns')]
            warn_new_dict = warn_values_dict[str(ctx.guild.id)]
            try:
                warn_new_dict[str(user_sha1.hexdigest())] = str(int(warns['warns'][str(ctx.guild.id)][str(user_sha1.hexdigest())]) + 1)
            except:
                warn_new_dict[str(user_sha1.hexdigest())] = '1'
            warns_dict['warns'][str(ctx.guild.id)] = warn_new_dict
            with open('database/userdata.json', 'w') as f:
                json.dump(warns_dict, f, indent = 4)
            load_admin_bypass()
            embed=discord.Embed(title=str(user)+Lang['user-warned'], description=Lang['warn-reason']+reason, color=0x81FA28)
            await ctx.channel.send(embed=embed)
            await user.send(embed=embed)
            print(now_time(), str(user), Lang['user-warned'], Lang['warn-reason'], reason)
            if user_data['warns'][str(ctx.guild.id)][str(user_sha1.hexdigest())] == data['auto-mute'] :
                reason = Lang['when-warnings-match']+data['auto-mute']+Lang['auto-mute-message']
                guild = ctx.guild
                mutedRole = discord.utils.get(guild.roles, name=Lang['mute-role-name'])
                all_roles = await guild.fetch_roles()
                num_roles = len(all_roles)
                if not mutedRole:
                    mutedRole = await guild.create_role(name=Lang['mute-role-name'])
                    await mutedRole.edit(position=num_roles - 2)
                    for channel in guild.channels:
                        await channel.set_permissions(mutedRole, speak=False, send_messages=False)
                await user.add_roles(mutedRole, reason=reason)
                embed=discord.Embed(title=str(user)+Lang['user-muted'], description=Lang['warn-reason']+reason, color=0x81FA28)
                await ctx.channel.send(embed=embed)
                await user.send(embed=embed)
                print(now_time(), str(user), Lang['user-muted'], Lang['warn-reason'], reason)
            if user_data['warns'][str(ctx.guild.id)][str(user_sha1.hexdigest())] == data['auto-kick']:
                reason = Lang['when-warnings-match']+data['auto-mute']+Lang['auto-kick-message']
                embed=discord.Embed(title=str(user)+Lang['user-kicked'], description=Lang['warn-reason']+reason, color=0x81FA28)
                await user.send(embed=embed)
                await ctx.guild.kick(user)
                await ctx.channel.send(embed=embed)
                print(now_time(), str(user), Lang['user-kicked'], Lang['warn-reason'], reason)
            if user_data['warns'][str(ctx.guild.id)][str(user_sha1.hexdigest())] == data['auto-ban']:
                reason = Lang['when-warnings-match']+data['auto-mute']+Lang['auto-ban-message']
                embed=discord.Embed(title=str(user)+Lang['user-banned'], description=Lang['warn-reason']+reason, color=0x81FA28)
                await user.send(embed=embed)
                await ctx.guild.ban(user, reason=reason)
                await ctx.channel.send(embed=embed)
                print(now_time(), str(user), Lang['user-banned'], Lang['warn-reason'], reason)
        elif ctx.author.guild_permissions.administrator or str(ctx_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('admin')][str(ctx.guild.id)].values()):
            if str(user_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('bypass')][str(ctx.guild.id)].values()) or user.guild_permissions.administrator:
                await error_code.bypass(ctx, Lang)
            else:
                with open('database/userdata.json', 'r') as f:
                    warns = json.load(f)
                warns_keys = list(warns.keys())
                warns_values = list(warns.values())
                warns_dict = {}
                warn_values_dict = {}
                warn_new_dict = {}
                for i in range(len(warns_keys)):
                    warns_dict[warns_keys[i]] = warns_values[i]

                warn_values_dict = warns_values[warns_keys.index('warns')]
                warn_new_dict = warn_values_dict[str(ctx.guild.id)]
                try:
                    warn_new_dict[str(user_sha1.hexdigest())] = str(int(warns['warns'][str(ctx.guild.id)][str(user_sha1.hexdigest())]) + 1)
                except:
                    warn_new_dict[str(user_sha1.hexdigest())] = '1'
                warns_dict['warns'][str(ctx.guild.id)] = warn_new_dict
                with open('database/userdata.json', 'w') as f:
                    json.dump(warns_dict, f, indent = 4)
                load_admin_bypass()
                embed=discord.Embed(title=str(user)+Lang['user-warned'], description=Lang['warn-reason']+options, color=0x81FA28)
                await ctx.channel.send(embed=embed)
                await user.send(embed=embed)
                print(now_time(), str(user), Lang['user-warned'], Lang['warn-reason'], options)
                if user_data['warns'][str(ctx.guild.id)][str(user_sha1.hexdigest())] == data['auto-mute'] :
                    reason = Lang['when-warnings-match']+data['auto-mute']+Lang['auto-mute-message']
                    guild = ctx.guild
                    mutedRole = discord.utils.get(guild.roles, name=Lang['mute-role-name'])
                    all_roles = await guild.fetch_roles()
                    num_roles = len(all_roles)
                    if not mutedRole:
                        mutedRole = await guild.create_role(name=Lang['mute-role-name'])
                        await mutedRole.edit(position=num_roles - 2)
                        for channel in guild.channels:
                            await channel.set_permissions(mutedRole, speak=False, send_messages=False)
                    await user.add_roles(mutedRole, reason=reason)
                    embed=discord.Embed(title=str(user)+Lang['user-muted'], description=Lang['warn-reason']+reason, color=0x81FA28)
                    await ctx.channel.send(embed=embed)
                    await user.send(embed=embed)
                    print(now_time(), str(user), Lang['user-muted'], Lang['warn-reason'], reason)
                if user_data['warns'][str(ctx.guild.id)][str(user_sha1.hexdigest())] == data['auto-kick']:
                    reason = Lang['when-warnings-match']+data['auto-mute']+Lang['auto-kick-message']
                    embed=discord.Embed(title=str(user)+Lang['user-kicked'], description=Lang['warn-reason']+reason, color=0x81FA28)
                    await user.send(embed=embed)
                    await ctx.guild.kick(user)
                    await ctx.channel.send(embed=embed)
                    print(now_time(), str(user), Lang['user-kicked'], Lang['warn-reason'], reason)
                if user_data['warns'][str(ctx.guild.id)][str(user_sha1.hexdigest())] == data['auto-ban']:
                    reason = Lang['when-warnings-match']+data['auto-mute']+Lang['auto-ban-message']
                    embed=discord.Embed(title=str(user)+Lang['user-banned'], description=Lang['warn-reason']+reason, color=0x81FA28)
                    await user.send(embed=embed)
                    await ctx.guild.ban(user, reason=reason)
                    await ctx.channel.send(embed=embed)
                    print(now_time(), str(user), Lang['user-banned'], Lang['warn-reason'], reason)
        else:
            await error_code.permission(ctx, Lang)

@bot.event
async def on_message(message):
    global badwords
    if str(message.channel.type) == 'private':
        print(message.channel, ':', message.content)
    if message.author == bot.user or message.author.bot:
        return
    salt(message.author.id)
    if message.channel.id == data['picture-only-channel-id'] and message.content != "":
        await message.channel.purge(limit=1)
    try:
        if str(message.guild.id) not in list(userdata_values[userdata_keys.index('admin')].keys()):
            userdata_dict = {}
            userdata_values_dict = {}
            for i in range(len(userdata_keys)):
                userdata_dict[userdata_keys[i]] = userdata_values[i]
            userdata_values_dict = userdata_values[userdata_keys.index('admin')]
            sha512= hashlib.sha512()
            sha512.update(str(message.author).encode('utf-8'))
            userdata_values_dict[str(message.guild.id)] = {str(sha512.hexdigest()): ''}
            userdata_dict['admin'] = userdata_values_dict
            with open("database/userdata.json", "w") as userdata_file:
                json.dump(userdata_dict, userdata_file, indent = 4)
            load_admin_bypass()
        if str(message.guild.id) not in list(userdata_values[userdata_keys.index('bypass')].keys()):
            userdata_dict = {}
            userdata_values_dict = {}
            for i in range(len(userdata_keys)):
                userdata_dict[userdata_keys[i]] = userdata_values[i]
            userdata_values_dict = userdata_values[userdata_keys.index('bypass')]
            sha512= hashlib.sha512()
            sha512.update(str(message.author).encode('utf-8'))
            userdata_values_dict[str(message.guild.id)] = {str(sha512.hexdigest()): ''}
            userdata_dict['bypass'] = userdata_values_dict
            with open("database/userdata.json", "w") as userdata_file:
                json.dump(userdata_dict, userdata_file, indent = 4)
            load_admin_bypass()
        if str(message.guild.id) not in list(userdata_values[userdata_keys.index('warns')].keys()):
            userdata_dict = {}
            userdata_values_dict = {}
            for i in range(len(userdata_keys)):
                userdata_dict[userdata_keys[i]] = userdata_values[i]
            userdata_values_dict = userdata_values[userdata_keys.index('warns')]
            user_sha1 = hashlib.sha1(user_salt[str(message.author.id)].encode('utf-8'))
            user_sha1.update(str(message.author.id).encode('utf-8'))
            userdata_values_dict[str(message.guild.id)] = {str(user_sha1.hexdigest()): '0'}
            userdata_dict['warns'] = userdata_values_dict
            with open("database/userdata.json", "w") as userdata_file:
                json.dump(userdata_dict, userdata_file, indent = 4)
            load_admin_bypass()
        if str(message.guild.id) not in list(musicdata_values[musicdata_keys.index('url')].keys()):
            musicdata_dict = {}
            musicdata_values_dict = {}
            for i in range(len(musicdata_keys)):
                musicdata_dict[musicdata_keys[i]] = musicdata_values[i]
            musicdata_values_dict = musicdata_values[musicdata_keys.index('url')]
            musicdata_values_dict[str(message.guild.id)] = {}
            musicdata_dict['url'] = musicdata_values_dict
            with open("database/musicdata.json", "w") as userdata_file:
                json.dump(musicdata_dict, userdata_file, indent = 4)
            load_music()
        if str(message.guild.id) not in list(musicdata_values[musicdata_keys.index('title')].keys()):
            musicdata_dict = {}
            musicdata_values_dict = {}
            for i in range(len(musicdata_keys)):
                musicdata_dict[musicdata_keys[i]] = musicdata_values[i]
            musicdata_values_dict = musicdata_values[musicdata_keys.index('title')]
            musicdata_values_dict[str(message.guild.id)] = {}
            musicdata_dict['title'] = musicdata_values_dict
            with open("database/musicdata.json", "w") as userdata_file:
                json.dump(musicdata_dict, userdata_file, indent = 4)
            load_music()
        if str(message.guild.id) not in list(musicdata_values[musicdata_keys.index('repeat')].keys()):
            musicdata_dict = {}
            musicdata_values_dict = {}
            for i in range(len(musicdata_keys)):
                musicdata_dict[musicdata_keys[i]] = musicdata_values[i]
            musicdata_values_dict = musicdata_values[musicdata_keys.index('repeat')]
            musicdata_values_dict[str(message.guild.id)] = False
            musicdata_dict['repeat'] = musicdata_values_dict
            with open("database/musicdata.json", "w") as userdata_file:
                json.dump(musicdata_dict, userdata_file, indent = 4)
            load_music()
        if str(message.guild.id) not in list(musicdata_values[musicdata_keys.index('button_switch')].keys()):
            musicdata_dict = {}
            musicdata_values_dict = {}
            for i in range(len(musicdata_keys)):
                musicdata_dict[musicdata_keys[i]] = musicdata_values[i]
            musicdata_values_dict = musicdata_values[musicdata_keys.index('button_switch')]
            musicdata_values_dict[str(message.guild.id)] = False
            musicdata_dict['button_switch'] = musicdata_values_dict
            with open("database/musicdata.json", "w") as userdata_file:
                json.dump(musicdata_dict, userdata_file, indent = 4)
            load_music()
    except:
        pass
    if message.content.startswith('!info'):
        embed = discord.Embed(title='❗｜'+'Copyright Notice', description=copyright(), color=0xB51FFB)
        embed.set_footer(text='Version: '+data['version'])
        await message.channel.send(embed=embed)
    if message.content.startswith('!prefix'):
        embed = discord.Embed(title='💻｜'+Lang['prefix-tip'], description=data['command-prefix'], color=0xB51FFB)
        await message.channel.send(embed=embed)
    if message.content.startswith('!function'):
        embed = discord.Embed(title='', color=0xB51FFB)
        embed2 = discord.Embed(title='', color=0xB51FFB)
        with open('config.json', "r", encoding = "utf8") as file:
            tempdata = json.load(file)
        data_key = list(tempdata.keys())
        data_values = list(tempdata.values())
        data_command_key = list(tempdata['commands'].keys())
        data_command_values = list(tempdata['commands'].values())
        num_list =[14, 16, 18, 19]
        enable_value = ''
        disable_value = ''
        for i in num_list:
            if data_values[i] == True:
                enable_value += data_key[i]+'\n'
            else:
                disable_value += data_key[i]+'\n'
        embed.add_field(name='🟢｜'+Lang['function-enable'], value=enable_value, inline=True)
        if enable_value == '':
            disable_value = Lang['function-None']
        if disable_value == '':
            disable_value = Lang['function-None']
        embed.add_field(name='🔴｜'+Lang['function-disable'], value=disable_value, inline=True)
        enable_value = ''
        disable_value = ''
        for i in range(len(data_command_values)):
            if data_command_values[i] == True:
                enable_value += data_command_key[i]+'\n'
            else:
                disable_value += data_command_key[i]+'\n'
        embed2.add_field(name='🟢｜'+Lang['function-command-enable'], value=enable_value, inline=True)
        if enable_value == '':
            disable_value = Lang['function-None']
        if disable_value == '':
            disable_value = Lang['function-None']
        embed2.add_field(name='🔴｜'+Lang['function-command-disable'], value=disable_value, inline=True)
        await message.channel.send(embed=embed)
        await message.channel.send(embed=embed2)
    if data['chat-filter']:
        user_sha1 = hashlib.sha1(user_salt[str(message.author.id)].encode('utf-8'))
        user_sha1.update(str(message.author.id).encode('utf-8'))
        try:
            if str(user_sha1.hexdigest()) in list(userdata_values[userdata_keys.index('bypass')][str(message.guild.id)].values()) or message.author.guild_permissions.administrator:
                await bot.process_commands(message)
                return
        except:
            pass
        else:
            for i in badwords:
                Regex = re.compile(i)
                match_word = Regex.search(message.content)
                if match_word:
                    await message.delete()
                    embed = discord.Embed(title='❌｜'+Lang['chat-filter'], description=match_word.group(), color=0xEC2E2E)
                    await message.channel.send(f"<@{message.author.id}>", embed=embed, delete_after=5)
                    await message.author.send(embed=embed)
                    print(now_time(), message.author.name, '❌｜'+Lang['chat-filter'], match_word.group())
                    reason = Lang['chat-filter-reason']
                    if data['chat-filter-action'] == 'warn':
                        with open('database/userdata.json', 'r') as f:
                            warns = json.load(f)
                        warns_keys = list(warns.keys())
                        warns_values = list(warns.values())
                        warns_dict = {}
                        warn_values_dict = {}
                        warn_new_dict = {}
                        for i in range(len(warns_keys)):
                            warns_dict[warns_keys[i]] = warns_values[i]

                        warn_values_dict = warns_values[warns_keys.index('warns')]
                        warn_new_dict = warn_values_dict[str(message.guild.id)]
                        try:
                            warn_new_dict[str(user_sha1.hexdigest())] = str(int(warns['warns'][str(message.guild.id)][str(user_sha1.hexdigest())]) + 1)
                        except:
                            warn_new_dict[str(user_sha1.hexdigest())] = '1'
                        warns_dict['warns'][str(message.guild.id)] = warn_new_dict
                        with open('database/userdata.json', 'w') as f:
                            json.dump(warns_dict, f, indent = 4)
                        load_admin_bypass()
                        embed=discord.Embed(title=str(message.author)+Lang['user-warned'], description=Lang['warn-reason']+reason, color=0x81FA28)
                        await message.channel.send(embed=embed)
                        await message.author.send(embed=embed)
                        print(now_time(), str(message.author), Lang['user-warned'], Lang['warn-reason'], reason)
                        if user_data['warns'][str(message.guild.id)][str(user_sha1.hexdigest())] == data['auto-mute'] :
                            reason = Lang['when-warnings-match']+data['auto-mute']+Lang['auto-mute-message']
                            guild = message.guild
                            mutedRole = discord.utils.get(guild.roles, name=Lang['mute-role-name'])
                            all_roles = await guild.fetch_roles()
                            num_roles = len(all_roles)
                            if not mutedRole:
                                mutedRole = await guild.create_role(name=Lang['mute-role-name'])
                                await mutedRole.edit(position=num_roles - 2)
                                for channel in guild.channels:
                                    await channel.set_permissions(mutedRole, speak=False, send_messages=False)
                            await message.author.add_roles(mutedRole, reason=reason)
                            embed=discord.Embed(title=str(message.author)+Lang['user-muted'], description=Lang['warn-reason']+reason, color=0x81FA28)
                            await message.channel.send(embed=embed)
                            await message.author.send(embed=embed)
                            print(now_time(), str(message.author), Lang['user-muted'], Lang['warn-reason'], reason)
                        if user_data['warns'][str(message.guild.id)][str(user_sha1.hexdigest())] == data['auto-kick']:
                            reason = Lang['when-warnings-match']+data['auto-mute']+Lang['auto-kick-message']
                            embed=discord.Embed(title=str(message.author)+Lang['user-kicked'], description=Lang['warn-reason']+reason, color=0x81FA28)
                            await message.author.send(embed=embed)
                            await message.guild.kick(message.author)
                            await message.channel.send(embed=embed)
                            print(now_time(), str(message.author), Lang['user-kicked'], Lang['warn-reason'], reason)
                        if user_data['warns'][str(message.guild.id)][str(user_sha1.hexdigest())] == data['auto-ban']:
                            reason = Lang['when-warnings-match']+data['auto-mute']+Lang['auto-ban-message']
                            embed=discord.Embed(title=str(message.author)+Lang['user-banned'], description=Lang['warn-reason']+reason, color=0x81FA28)
                            await message.author.send(embed=embed)
                            await message.guild.ban(message.author, reason=reason)
                            await message.channel.send(embed=embed)
                            print(now_time(), str(message.author), Lang['user-banned'], Lang['warn-reason'], reason)
                    elif data['chat-filter-action'] == 'mute':
                        guild = message.guild
                        mutedRole = discord.utils.get(guild.roles, name=Lang['mute-role-name'])
                        all_roles = await guild.fetch_roles()
                        num_roles = len(all_roles)
                        if not mutedRole:
                            mutedRole = await guild.create_role(name=Lang['mute-role-name'])
                            await mutedRole.edit(position=num_roles - 2)
                            for channel in guild.channels:
                                await channel.set_permissions(mutedRole, speak=False, send_messages=False)
                        await message.author.add_roles(mutedRole, reason=reason)
                        embed=discord.Embed(title=str(message.author)+Lang['user-muted'], description=Lang['warn-reason']+reason, color=0x81FA28)
                        await message.channel.send(embed=embed)
                        await message.author.send(embed=embed)
                        print(now_time(), str(message.author), Lang['user-muted'], Lang['warn-reason'], reason)
                    elif data['chat-filter-action'] == 'kick':
                        embed=discord.Embed(title=str(message.author)+Lang['user-kicked'], description=Lang['warn-reason']+reason, color=0x81FA28)
                        try:
                            await message.author.send(embed=embed)
                        except:
                            pass
                        await message.guild.kick(message.author)
                        await message.channel.send(embed=embed)
                        print(now_time(), str(message.author), Lang['user-kicked'], Lang['warn-reason'], reason)
                    elif data['chat-filter-action'] == 'ban':
                        embed=discord.Embed(title=str(message.author)+Lang['user-banned'], description=Lang['warn-reason']+reason, color=0x81FA28)
                        try:
                            await message.author.send(embed=embed)
                        except:
                            pass
                        await message.guild.ban(message.author, reason=reason)
                        await message.channel.send(embed=embed)
                        print(now_time(), str(message.author), Lang['user-banned'], Lang['warn-reason'], reason)
                    return
        await bot.process_commands(message)
        return
    else:
        await bot.process_commands(message)

# Music bot

def load_music():
    global music_data, musicdata_keys, musicdata_values
    with open('database/musicdata.json', "r", encoding = "utf8") as music_file:
        music_data = json.load(music_file)
    musicdata_keys = list(music_data.keys())
    musicdata_values = list(music_data.values())
load_music()

def clear_music():
    musicdata_dict = {}
    for i in range(len(musicdata_keys)):
        musicdata_dict[musicdata_keys[i]] = musicdata_values[i]
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
        'noplaylist': False,
        'default_search': 'auto'
    }

async def playit(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    try:
        if not music_data['repeat'][str(ctx.guild.id)]:
            await ctx.channel.purge(limit=1, check = lambda inter: inter.content == '')
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
            Url = info["formats"][0]['url']
        except:
            Url = list(music_data['url'][str(ctx.guild.id)].values())[0]
        pplayer = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(Url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), 1)
        voice.play(pplayer, after = lambda e: myafter(ctx))
        button_switch(ctx, 'true')
        print('',Lang['music-playing'],list(music_data['title'][str(ctx.guild.id)].values())[0],list(music_data['url'][str(ctx.guild.id)].values())[0],'', sep='\n')
        if not music_data['repeat'][str(ctx.guild.id)]:
            await music_button_1(ctx, info)
    except:
        pass
        
def myafter(ctx):
    button_switch(ctx)
    fut = asyncio.run_coroutine_threadsafe(playit(ctx), bot.loop)
    fut.result()

async def music_button_1(ctx, info):
    if 'entries' in info:
        Info = info['entries'][0]
    elif 'formats' in info:
        Info = info
    embed = discord.Embed(title=Lang['music-playing'], description=Info['title'], color=0x79EF2F)
    embed.set_thumbnail(url=Info.get('thumbnail'))

    seconds = Info['duration']
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    embed.add_field(name=Lang['music-uploader'], value=Info.get('uploader'), inline=True)
    embed.add_field(name=Lang['music-duration'], value="%d:%02d:%02d" % (h, m, s), inline=True)
    embed.add_field(name=Lang['music-like_count'], value=str(Info.get('like_count')), inline=True)
    embed.add_field(name=Lang['music-DJ'], value=f'<@{ctx.message.author.id}>', inline=True)
    embed.add_field(name=Lang['music-channel'], value=f'<#{ctx.author.voice.channel.id}>', inline=True)
    if music_data['repeat'][str(ctx.guild.id)]:
        embed.add_field(name=Lang['music-repeat'], value=Lang['enable'], inline=True)
    else:
        embed.add_field(name=Lang['music-repeat'], value=Lang['disable'], inline=True)
    embed.set_footer(text=now_time(), icon_url=ctx.author.avatar_url)
    await ctx.channel.send(embed=embed)
    await ctx.send('', components = [[
        Button(label=Lang['music-link'], style=ButtonStyle.URL, url=Info.get('webpage_url')),
        Button(label=Lang['music-list'], style='2', custom_id='list', emoji='📜'),
        Button(label=Lang['music-repeat'], style='2', custom_id='repeat', emoji='🔁'),
        Button(label=Lang['music-random'], style='2', custom_id='random', emoji='🔀')],[
        Button(label=Lang['music-pause'], style='1', custom_id='pause', emoji='⏸'),
        Button(label=Lang['music-resume'], style='1', custom_id='resume', emoji='⏯'),
        Button(label=Lang['music-stop'], style='4', custom_id='stop', emoji='⏹'),
        Button(label=Lang['music-skip'], style='2', custom_id='skip', emoji='⏩')],[
        Button(label=Lang['music-favorite'], style='3', custom_id='favorite', emoji='💕'),
        Button(label=Lang['music-unfavorite'], style='4', custom_id='unfavorite', emoji='💔')
    ]])

@bot.command(aliases=['p'])
async def play(ctx, *, url: str=''):
    if data['music-bot']:
        if url == '':
            embed = discord.Embed(title='❌｜'+Lang['music-url-error'], color=0xEC2E2E)
            await ctx.reply(embed=embed)
            return
        try:
            voiceChannel = discord.utils.get(ctx.guild.voice_channels, id=ctx.author.voice.channel.id)
        except:
            embed = discord.Embed(title='❌｜'+Lang['music-user-not-in-channel'], color=0xEC2E2E)
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
            for res in result["result"]:
                search_url_list.append(res["link"])
                search_title_list.append(res['title'])
                op.append(SelectOption(label=res['channel']['name'], value=str(num), description=res['title'], emoji='🔍'))
                num += 1
            sele = await ctx.reply(content=Lang['search_result'], components=[Select(placeholder=Lang['menu-select'], options= op,
                                                custom_id='music_select'
            )])
            interaction = await bot.wait_for('select_option', check = lambda inter: inter.custom_id == 'music_select')
            res = interaction.values[0]
            for i in range(25):
                try:
                    if res == str(i):
                        embed = discord.Embed(title=Lang['selected'], description=search_title_list[i], color=0x81FA28)
                        await interaction.send(embed=embed)
                        url = search_url_list[i]
                        await sele.delete()
                        break
                except:
                    pass
        try:
            await voiceChannel.connect()
        except:
            pass
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        Url = info["formats"][0]['url']
        musicdata_dict = {}
        musicdata_values_dict = {}
        musicdata_new_dict = {}
        for i in range(len(musicdata_keys)):
            musicdata_dict[musicdata_keys[i]] = musicdata_values[i]
        musicdata_values_dict = musicdata_values[musicdata_keys.index('url')]
        musicdata_new_dict = musicdata_values_dict[str(ctx.guild.id)]
        try:
            musicdata_new_dict[str(int(list(music_data['url'][str(ctx.guild.id)].keys()).max())+1)] = str(url)
        except:
            musicdata_new_dict[str(len(musicdata_new_dict))] = str(url)
        musicdata_dict['url'][str(ctx.guild.id)] = musicdata_new_dict
        with open("database/musicdata.json", "w") as musicdata_file:
            json.dump(musicdata_dict, musicdata_file, indent = 4)
        musicdata_values_dict = musicdata_values[musicdata_keys.index('title')]
        musicdata_new_dict = musicdata_values_dict[str(ctx.guild.id)]
        try:
            musicdata_new_dict[str(int(list(music_data['title'][str(ctx.guild.id)].keys()).max())+1)] = str(info['title'])
        except:
            musicdata_new_dict[str(len(musicdata_new_dict))] = str(info['title'])
        musicdata_dict['title'][str(ctx.guild.id)] = musicdata_new_dict
        with open("database/musicdata.json", "w") as musicdata_file:
            json.dump(musicdata_dict, musicdata_file, indent = 4)
        load_music()
        await ctx.message.add_reaction('✅')
        try:
            pplayer = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(Url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), 1)
            voice.play(pplayer, after = lambda e: myafter(ctx))
            button_switch(ctx, 'true')
            print('',Lang['music-playing'],list(music_data['title'][str(ctx.guild.id)].values())[0],list(music_data['url'][str(ctx.guild.id)].values())[0],'', sep='\n')
            await music_button_1(ctx, info)
        except:
            embed = discord.Embed(title='✅｜'+Lang['playlist_added'], color=0x81FA28)
            await ctx.reply(embed=embed)
    
@bot.command()
async def leave(ctx):
    if data['music-bot']:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        try:
            if voice.is_connected():
                await voice.disconnect()
        except:
            embed = discord.Embed(title='❌｜'+Lang['music-bot-not-in-channel'], color=0xEC2E2E)
            await ctx.reply(embed=embed)

@bot.command()
async def pause(ctx):
    if data['music-bot']:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        try:
            if voice.is_playing():
                voice.pause()
        except:
            embed = discord.Embed(title='❌｜'+Lang['music-nothing-playing'], color=0xEC2E2E)
            await ctx.reply(embed=embed)

@bot.command()
async def resume(ctx):
    if data['music-bot']:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        try:
            if voice.is_paused():
                voice.resume()
        except:
            embed = discord.Embed(title='❌｜'+Lang['music-nothing-pause'], color=0xEC2E2E)
            await ctx.reply(embed=embed)

@bot.command()
async def repeat(ctx):
    if data['music-bot']:
        musicdata_dict = {}
        for i in range(len(musicdata_keys)):
            musicdata_dict[musicdata_keys[i]] = musicdata_values[i]
        musicdata_values_dict = musicdata_values[musicdata_keys.index('repeat')]
        if music_data['repeat'][str(ctx.guild.id)]:
            musicdata_values_dict[str(ctx.guild.id)] = False
            embed = discord.Embed(title='🔁｜'+Lang['repeat-disabled'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed)
        else:
            musicdata_values_dict[str(ctx.guild.id)] = True
            embed = discord.Embed(title='🔁｜'+Lang['repeat-enabled'], color=0x81FA28)
            await ctx.channel.send(embed=embed)
        musicdata_dict['repeat'] = musicdata_values_dict
        with open("database/musicdata.json", "w") as musicdata_file:
            json.dump(musicdata_dict, musicdata_file, indent = 4)
        load_music()

@bot.command()
async def stop(ctx):
    if data['music-bot']:
        musicdata_dict = {}
        musicdata_values_dict = {}
        for i in range(len(musicdata_keys)):
            musicdata_dict[musicdata_keys[i]] = musicdata_values[i]
        musicdata_values_dict = musicdata_values[musicdata_keys.index('repeat')]
        musicdata_values_dict[str(ctx.guild.id)] = False
        music_data['url'][str(ctx.guild.id)] = {}
        music_data['title'][str(ctx.guild.id)] = {}
        music_data['repeat'] = musicdata_values_dict
        with open("database/musicdata.json", "w") as musicdata_file:
            json.dump(music_data, musicdata_file, indent = 4)
        load_music()
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        button_switch(ctx)
        try:
            voice.stop()
            await voice.disconnect()
        except:
            embed = discord.Embed(title='❌｜'+Lang['music-nothing-playing'], color=0xEC2E2E)
            await ctx.reply(embed=embed)
        return

@bot.command()
async def volume(ctx, volume: int=100):
    if data['music-bot']:
        if ctx.voice_client is None:
            await ctx.send(Lang['music-bot-not-in-channel'])
            return
        before_volume = ctx.voice_client.source.volume * 100
        ctx.voice_client.source.volume = volume / 100
        if before_volume > volume:
            embed = discord.Embed(title='🔉｜'+Lang['volume-changed']+str(before_volume)+'%'+Lang['volume-changed-to']+str(volume)+'%', color=0xEC2E2E)
            await ctx.reply(embed=embed)
        elif before_volume < volume:
            embed = discord.Embed(title='🔊｜'+Lang['volume-changed']+str(before_volume)+'%'+Lang['volume-changed-to']+str(volume)+'%', color=0xEC2E2E)
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(title='❓｜'+Lang['volume-nothing-changed'], color=0xEC2E2E)
            await ctx.reply(embed=embed)

@bot.command()
async def skip(ctx):
    if data['music-bot']:
        button_switch(ctx)
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        try:
            voice.stop()
        except:
            await ctx.channel.send(Lang['music-nothing-playing'])
        return

@bot.command(aliases=['pl'])
async def playlist(ctx):
    if data['music-bot']:
        if list(music_data['title'][str(ctx.guild.id)].keys()) == []:
            embed = discord.Embed(title='❌｜'+Lang['music-nothing-playing'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed)
            return
        else:
            embed = discord.Embed(title='📜｜'+Lang['music-list'], color=0x79EF2F)
            for playlist in range(len(list(music_data['title'][str(ctx.guild.id)].keys()))):
                if playlist == 0:
                    if not music_data['repeat'][str(ctx.guild.id)]:
                        embed.add_field(name=list(music_data['title'][str(ctx.guild.id)].values())[playlist], value=Lang['music-playing'], inline=False)
                    else:
                        embed.add_field(name=list(music_data['title'][str(ctx.guild.id)].values())[playlist], value=Lang['music-playing-repeat'], inline=False)
                else:
                    embed.add_field(name=list(music_data['title'][str(ctx.guild.id)].values())[playlist], value='No. '+str(playlist), inline=False)
        await ctx.channel.send(embed=embed)

@bot.command()
async def listmove(ctx, before: int, after: int):
    global gPlaylist, music_name
    if data['music-bot']:
        if before == 0:
            embed = discord.Embed(title='❌｜'+Lang['move-error'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed)
            return
        elif before > len(list(music_data['url'][str(ctx.guild.id)].keys()))-1 or after > len(list(music_data['url'][str(ctx.guild.id)].keys()))-1:
            embed = discord.Embed(title='❌｜'+Lang['out-range'], color=0xEC2E2E)
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
        embed = discord.Embed(title='🔃｜'+Lang['music-moved'], color=0x81FA28)
        await ctx.channel.send(embed=embed)

@bot.command()
async def listremove(ctx, number:int):
    if data['music-bot']:
        if number == 0:
            embed = discord.Embed(title='❌｜'+Lang['delete-error'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed)
            return
        elif number > len(list(music_data['url'][str(ctx.guild.id)].keys()))-1:
            embed = discord.Embed(title='❌｜'+Lang['out-range'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed)
            return
        musicdata_dict = {}
        musicdata_values_dict = {}
        musicdata_new_dict = {}
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
        embed = discord.Embed(title='🗑｜'+Lang['music-deleted'], color=0x81FA28)
        await ctx.channel.send(embed=embed)

@bot.command()
async def listrandom(ctx):
    if data['music-bot']:
        musicdata_dict = {}
        random_dict = {} 
        url_list = list(music_data['url'][str(ctx.guild.id)].items())
        if url_list == []:
            embed = discord.Embed(title='❌｜'+Lang['music-nothing-playing'], color=0xEC2E2E)
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
            embed = discord.Embed(title='🔀｜'+Lang['music-randomed'], color=0x81FA28)
        await ctx.channel.send(embed=embed)

@bot.command(aliases=['f'])
async def favorite(ctx, options='', *, values: str=''):
    if data['music-bot']:
        sha1 = hashlib.sha1(user_salt[str(ctx.author.id)].encode('utf-8'))
        sha1.update(str(ctx.author.id).encode('utf-8'))
        with open('database/favorite.json', "r", encoding = "utf8") as favorite_file:
            favorite_data = json.load(favorite_file)
        data_keys = list(favorite_data.keys())
        data_values = list(favorite_data.values())
        favorite_dict = {}
        data_values_dict = {}

        if options == 'add' or options == 'a':
            if values == '':
                embed = discord.Embed(title='❌｜'+Lang['favorite-not-url'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed)
                return
            else:
                try:
                    br = mechanize.Browser()
                    br.open(values)
                except:
                    embed = discord.Embed(title='❌｜'+Lang['favorite-error-url'], color=0xEC2E2E)
                    await ctx.channel.send(embed=embed)
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
                embed = discord.Embed(title='✅｜'+Lang['favorite-added'], description=info['title'], color=0x81FA28)
                await ctx.reply(embed=embed)
        elif options == 'remove'or options == 'r':
            if values == '':
                embed = discord.Embed(title='❌｜'+Lang['favorite-remove-not-number'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed)
                return
            remove_dict = data_values[data_keys.index(str(sha1.hexdigest()))]
            remove_keys = list(remove_dict.keys())
            remove_values = list(remove_dict.values())
            try:
                if int(values) > len(remove_keys)-1:
                    embed = discord.Embed(title='❌｜'+Lang['out-range'], color=0xEC2E2E)
                    await ctx.channel.send(embed=embed)
                    return
            except:
                pass
            if values == '-a':
                embed = discord.Embed(title='🗑｜'+Lang['favorite-remove-all'], color=0x81FA28)
                for remove_url in remove_keys:
                    del favorite_data[str(sha1.hexdigest())][str(remove_url)]
            else:
                embed = discord.Embed(title='🗑｜'+Lang['favorite-removed'], description=remove_values[int(values)], color=0x81FA28)
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
                embed = discord.Embed(title='❌｜'+Lang['favorite-list-nothing'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed)
                return
            list_keys = list(list_dict.keys())
            if list_keys == []:
                embed = discord.Embed(title='❌｜'+Lang['favorite-list-nothing'], color=0xEC2E2E)
            else:
                embed = discord.Embed(title='💕｜'+ctx.author.name+Lang['favorite-list-title'], color=0x79EF2F)
                for favorite_list in range(len(list_keys)):
                    embed.add_field(name=list_dict[list_keys[favorite_list]], value='No. '+str(favorite_list), inline=False)
            await ctx.channel.send(embed=embed)
        elif options == 'play' or options == 'p':
            if values == '':
                embed = discord.Embed(title='❌｜'+Lang['favorite-play-not-number'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed)
                return
            play_dict = data_values[data_keys.index(str(sha1.hexdigest()))]
            play_keys = list(play_dict.keys())
            try:
                voiceChannel = discord.utils.get(ctx.guild.voice_channels, id=ctx.author.voice.channel.id)
            except:
                embed = discord.Embed(title='❌｜'+Lang['music-user-not-in-channel'], color=0xEC2E2E)
                await ctx.reply(embed=embed)
                return
            try:
                await voiceChannel.connect()
            except:
                pass
            await ctx.message.add_reaction('✅')
            voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
            musicdata_dict = {}
            musicdata_values_dict = {}
            musicdata_new_dict = {}
            for i in range(len(musicdata_keys)):
                musicdata_dict[musicdata_keys[i]] = musicdata_values[i]
            if values == '-a':
                musicdata_values_dict = musicdata_values[musicdata_keys.index('url')]
                musicdata_new_dict = musicdata_values_dict[str(ctx.guild.id)]
                for play_url in play_keys:
                    try:
                        musicdata_new_dict[str(int(list(music_data['url'][str(ctx.guild.id)].keys()).max())+1)] = str(play_url)
                    except:
                        musicdata_new_dict[str(len(musicdata_new_dict))] = str(play_url)
                musicdata_dict['url'][str(ctx.guild.id)] = musicdata_new_dict
                with open("database/musicdata.json", "w") as musicdata_file:
                    json.dump(musicdata_dict, musicdata_file, indent = 4)
                musicdata_values_dict = musicdata_values[musicdata_keys.index('title')]
                musicdata_new_dict = musicdata_values_dict[str(ctx.guild.id)]
                for play_url in play_keys:
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(play_url, download=False)
                    try:
                        musicdata_new_dict[str(int(list(music_data['title'][str(ctx.guild.id)].keys()).max())+1)] = str(info['title'])
                    except:
                        musicdata_new_dict[str(len(musicdata_new_dict))] = str(info['title'])
                musicdata_dict['title'][str(ctx.guild.id)] = musicdata_new_dict
                with open("database/musicdata.json", "w") as musicdata_file:
                    json.dump(musicdata_dict, musicdata_file, indent = 4)
                load_music()
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(play_keys[0], download=False)
                Url = info["formats"][0]['url']
            else:
                if int(values) > len(play_keys)-1:
                    embed = discord.Embed(title='❌｜'+Lang['out-range'], color=0xEC2E2E)
                    await ctx.channel.send(embed=embed)
                    return
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(play_keys[int(values)], download=False)
                Url = info["formats"][0]['url']
                musicdata_values_dict = musicdata_values[musicdata_keys.index('url')]
                musicdata_new_dict = musicdata_values_dict[str(ctx.guild.id)]
                try:
                    musicdata_new_dict[str(int(list(music_data['url'][str(ctx.guild.id)].keys()).max())+1)] = str(play_keys[int(values)])
                except:
                    musicdata_new_dict[str(len(musicdata_new_dict))] = str(play_keys[int(values)])
                musicdata_dict['url'][str(ctx.guild.id)] = musicdata_new_dict
                with open("database/musicdata.json", "w") as musicdata_file:
                    json.dump(musicdata_dict, musicdata_file, indent = 4)
                musicdata_values_dict = musicdata_values[musicdata_keys.index('title')]
                musicdata_new_dict = musicdata_values_dict[str(ctx.guild.id)]
                try:
                    musicdata_new_dict[str(int(list(music_data['title'][str(ctx.guild.id)].keys()).max())+1)] = str(info['title'])
                except:
                    musicdata_new_dict[str(len(musicdata_new_dict))] = str(info['title'])
                musicdata_dict['title'][str(ctx.guild.id)] = musicdata_new_dict
                with open("database/musicdata.json", "w") as musicdata_file:
                    json.dump(musicdata_dict, musicdata_file, indent = 4)
                load_music()
                await ctx.message.add_reaction('✅')
            try:    
                pplayer = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(Url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), 1)
                voice.play(pplayer, after = lambda e: myafter(ctx))
                button_switch(ctx, 'true')
                print('',Lang['music-playing'],list(music_data['title'][str(ctx.guild.id)].values())[0],list(music_data['url'][str(ctx.guild.id)].values())[0],'', sep='\n')
                await music_button_1(ctx, info)
            except:
                embed = discord.Embed(title='✅｜'+Lang['playlist_added'], color=0x81FA28)
                await ctx.reply(embed=embed)
        else:
            await ctx.send(content='', components=[Select(placeholder=Lang['menu-select'], options= [
                                                    SelectOption(label=prefix+'favorite add', value=prefix+'favorite add', description=Lang['favorite-menu-add'], emoji='💕'),
                                                    SelectOption(label=prefix+'favorite remove', value=prefix+'favorite remove', description=Lang['favorite-menu-remove'], emoji='🗑'),
                                                    SelectOption(label=prefix+'favorite list', value=prefix+'favorite list', description=Lang['favorite-menu-list'], emoji='📜'),
                                                    SelectOption(label=prefix+'favorite play', value=prefix+'favorite play', description=Lang['favorite-menu-play'], emoji='▶')
                                                ],
                                                custom_id='favorite_menu_'
                )])

#            

@bot.command()
async def tick(ctx):
    await ctx.message.delete()
    category = data['ticket-category-id']
    guild = ctx.guild
    Guild = discord.utils.get(guild.categories, id= category)
    await tick_create(ctx, guild, Guild)

async def tick_create(ctx, guild, Guild):
    global tick_message
    embed = discord.Embed(title='', color=0x79EF2F)
    embed.add_field(name='創立私人處理專案', value='點擊以下按鈕創建專案', inline=False)
    await ctx.channel.send(embed=embed)
    await ctx.send('', components = [
        Button(label='創立私人處理專案', style='3', custom_id='create_tick', emoji='📩')])
    while True:
        interaction = await bot.wait_for('button_click')
        res_create = interaction.custom_id
        if res_create == 'create_tick':
            await interaction.send(Lang['selected']+res_create)
            tick_message = await guild.create_text_channel(str(interaction.author.name)+' 的專案', overwrites=None, category = Guild)
            await tick_message.set_permissions(interaction.author, send_messages=True, view_channel=True)
            await tick_message.set_permissions(guild.default_role, send_messages=False, view_channel=False)
            embed = discord.Embed(title='', color=0xEDFA28)
            embed.add_field(name='歡迎來到處理專案', value='管理員會盡快回覆你\n如要關閉專案請點擊以下按鈕', inline=False)
            await tick_message.send(f"<@{interaction.author.id}>", embed=embed)
            await tick_message.send('', components = [
                Button(label='關閉專案', style='4', custom_id='close_tick', emoji='🔒')])
        else:
            pass

@bot.event
async def on_button_click(interaction):
    sha1 = hashlib.sha1(user_salt[str(interaction.author.id)].encode('utf-8'))
    sha1.update(str(interaction.author.id).encode('utf-8'))
    if interaction.component.label.startswith("關閉專案"):
        await interaction.send('專案已關閉')
        await tick_message.set_permissions(interaction.author, send_messages=False, view_channel=False)
        embed = discord.Embed(title='', color=0xEDFA28)
        embed.add_field(name='專案已關閉', value='如要刪除專案請點擊以下按鈕', inline=False)
        await interaction.channel.send(embed=embed)
        await interaction.channel.send('', components = [
                Button(label='刪除專案', style='4', custom_id='delete_tick', emoji='🗑')])
    elif interaction.component.label.startswith("刪除專案"):
        await interaction.channel.delete()
    elif interaction.component.label.startswith(Lang['music-pause']) and music_data['button_switch'][str(interaction.author.guild.id)]:
        await interaction.send(Lang['selected']+Lang['music-pause'])
        await pause(interaction)
    elif interaction.component.label.startswith(Lang['music-resume']) and music_data['button_switch'][str(interaction.author.guild.id)]:
        await interaction.send(Lang['selected']+Lang['music-resume'])
        await resume(interaction)
    elif interaction.component.label.startswith(Lang['music-list']) and music_data['button_switch'][str(interaction.author.guild.id)]:
        await interaction.send(Lang['selected']+Lang['music-list'])
        await playlist(interaction)
    elif interaction.component.label.startswith(Lang['music-skip']) and music_data['button_switch'][str(interaction.author.guild.id)]:
        await interaction.send(Lang['selected']+Lang['music-skip'])
        await skip(interaction)
    elif interaction.component.label.startswith(Lang['music-stop']) and music_data['button_switch'][str(interaction.author.guild.id)]:
        await interaction.send(Lang['selected']+Lang['music-stop'])
        await stop(interaction)
    elif interaction.component.label.startswith(Lang['music-repeat']) and music_data['button_switch'][str(interaction.author.guild.id)]:
        await interaction.send(Lang['selected']+Lang['music-repeat'])
        await repeat(interaction)
    elif interaction.component.label.startswith(Lang['music-random']) and music_data['button_switch'][str(interaction.author.guild.id)]:
        await interaction.send(Lang['selected']+Lang['music-random'])
        await listrandom(interaction)
    elif interaction.component.label.startswith(Lang['music-favorite']) and music_data['button_switch'][str(interaction.author.guild.id)]:
        with open('database/favorite.json', "r", encoding = "utf8") as favorite_file:
            favorite_data = json.load(favorite_file)
        data_keys = list(favorite_data.keys())
        data_values = list(favorite_data.values())
        favorite_dict = {}
        data_values_dict = {}
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
        embed = discord.Embed(title='✅｜'+Lang['favorite-added'], description=info['title'], color=0x81FA28)
        await interaction.send(embed=embed)
    elif interaction.component.label.startswith(Lang['music-unfavorite']) and music_data['button_switch'][str(interaction.author.guild.id)]:
        with open('database/favorite.json', "r", encoding = "utf8") as favorite_file:
            favorite_data = json.load(favorite_file)
        data_keys = list(favorite_data.keys())
        data_values = list(favorite_data.values())
        favorite_dict = {}
        data_values_dict = {}
        remove_dict = data_values[data_keys.index(str(sha1.hexdigest()))]

        remove_url = list(music_data['url'][str(interaction.author.guild.id)].values())[0]
        try:
            embed = discord.Embed(title='🗑｜'+Lang['favorite-removed'], description=remove_dict[remove_url], color=0x81FA28)
            del favorite_data[str(sha1.hexdigest())][str(remove_url)]
        except:
            embed = discord.Embed(title='❌｜'+Lang['favorite-remove-not-favorite'], color=0xEC2E2E)
        for i in range(len(data_keys)):
            favorite_dict[data_keys[i]] = data_values[i]
        with open("database/favorite.json", "w") as config_file:
            json.dump(favorite_dict, config_file, indent = 4)
        await interaction.send(embed=embed)


bot.run(data['token'])


# blind, tempblind, level system, money system, root

# auto role

# online count, total conut