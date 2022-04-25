import discord
from datetime import datetime
from discord.ext import commands, tasks
from discord_components import *
from discord.opus import *
from discord import FFmpegPCMAudio
import time, random, asyncio, sys, json, os, re
from ping3 import ping as pin
import logging
import tracemalloc
from pandas import Categorical
import youtube_dl, mechanize
from youtubesearchpython import VideosSearch
import wget, zipfile
import error_code, self_test, reset

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

print('Copyright © 2022 cc_chang.','All rights reserved.',sep='\n' ,end='\n\n')
print('View more information in github:', 'https://github.com/ccchang123/Discord-Bot.git','---------------------------------------------',sep='\n')

if not os.path.isfile('config.json'):
    print('load config file --- fail')
    self_test.error()
else:
    print('load config file --- ok')
    import lang

self_test.check_file()

with open('config.json', "r", encoding = "utf8") as file:
    data = json.load(file)

with open('chatfilter.txt', "r", encoding = "utf8") as words:
    badwords = words.read().split()
#

def load_admin_bypass():
    global bypass_list, admin_list
    admin_list = []
    bypass_list = []
    with open('admin.json', "r", encoding = "utf8") as file:
        admin = json.load(file)
    admin_data_list = list(admin.items())
    
    for i in admin_data_list:
        if data['debug-mode'] == 'true':
           print('Add admin:', i[0]+', id: '+i[1])
        admin_list.append(int(i[1]))

    with open('bypass.json', "r", encoding = "utf8") as file:
        bypass = json.load(file)
    bypass_data_list = list(bypass.items())
    
    for j in bypass_data_list:
        if data['debug-mode'] == 'true':
            print('Bypass user:', j[0]+', id: '+j[1])
        bypass_list.append(int(j[1]))

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

Lang = lang.lang_chose(data['language'], lang_list)

if data['debug-mode'] == 'true':
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

tracemalloc.start()

async def main_menu_1(ctx):
    await ctx.send(content=Lang['menu-name'], components=[Select(placeholder=Lang['menu-select'], options= [
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
                                                    SelectOption(label=prefix+'reload', value=prefix+'reload', description=Lang['menu-message-reload'], emoji='🔄'),
                                                    SelectOption(label=prefix+'removeadmin', value=prefix+'removeadmin', description=Lang['menu-message-removeadmin'], emoji='🗑'),
                                                    SelectOption(label=prefix+'removebypass', value=prefix+'removebypass', description=Lang['menu-message-removebypass'], emoji='🗑'),
                                                    SelectOption(label=prefix+'showwarn', value=prefix+'showwarn', description=Lang['menu-message-showwarn'], emoji='📄'),
                                                    SelectOption(label=prefix+'slowmoe', value=prefix+'slowmoe', description=Lang['menu-message-slowmoe'], emoji='🐢'),
                                                    SelectOption(label=prefix+'time', value=prefix+'time', description=Lang['menu-message-time'], emoji='⏱'),
                                                    SelectOption(label=prefix+'tlm', value=prefix+'tlm', description=Lang['menu-message-tlm'], emoji='📨'),
                                                    SelectOption(label=prefix+'tempban', value=prefix+'tempban', description=Lang['menu-message-tempban'], emoji='🚫'),
                                                    SelectOption(label=prefix+'tempmute', value=prefix+'tempmute', description=Lang['menu-message-tempmute'], emoji='🔈'),
                                                    SelectOption(label=prefix+'unban', value=prefix+'unban', description=Lang['menu-message-unban'], emoji='⭕')
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
            elif res == prefix+'tlm':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'tlm '+Lang['message'], color=0xEC2E2E)
                embed.add_field(name=Lang['uses'], value=Lang['temp-message'], inline=False)
                await interaction.send(embed=embed)
            elif res == prefix+'ban':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'ban '+Lang['@user']+Lang['reason'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'unban':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'unban '+Lang['@user'], color=0xEC2E2E)
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
            elif res == prefix+'slowmoe':
                await interaction.send(Lang['selected']+res)
                await slowmode(ctx)
            elif res == prefix+'cd':
                await interaction.send(Lang['selected']+res)
                await cd(ctx)
            elif res == prefix+'ci':
                await interaction.send(Lang['selected']+res)
                await ci(ctx)
            elif res == prefix+'tempmute':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'tempmute '+Lang['@user']+Lang['duration']+Lang['reason'], color=0xEC2E2E)
                await interaction.send(embed=embed)
            elif res == prefix+'tempban':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'tempban '+Lang['@user']+Lang['duration']+Lang['reason'], color=0xEC2E2E)
                await interaction.send(embed=embed)
        except:
            pass
async def main_menu_2(ctx):
    await ctx.send(content=Lang['menu-name'], components=[Select(placeholder=Lang['menu-select'], options= [
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
        except:
            pass

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
        if before.channel.members == [] and not before.channel.id == int(data['local-channel-id']):
            if before.channel.category_id == int(data['create-category-id']) and before.channel.name == member.name + Lang['create-channel-name']:
                await before.channel.delete()
    except:
        pass
    if channel == None:
        return
    if channel.id == int(data['local-channel-id']):
        guild = after.channel.guild
        private_channels = discord.utils.get(guild.categories, id= int(data['create-category-id']))
        voice_channel = await guild.create_voice_channel(member.name + Lang['create-channel-name'], overwrites=None, category=private_channels, user_limit = 5)
        await member.move_to(voice_channel)
        await voice_channel.set_permissions(member, manage_channels=True, manage_permissions=True)
        print(now_time(), member, Lang['when-channel-create'])

@bot.command()
async def menu(ctx, page: int=1):
    if page == 1:
        await main_menu_1(ctx)
    elif page == 2:
        await main_menu_2(ctx)

@bot.command()
async def addadmin(ctx, user: discord.Member=None):
    if data['command-addadmin'] == 'true':
        if ctx.author.guild_permissions.administrator:
            if not user:
                embed = discord.Embed(title=Lang['usage'], description=prefix+'addadmin '+Lang['@user'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed, delete_after=5)
            elif user.id in admin_list or user.guild_permissions.administrator:
                embed=discord.Embed(title=Lang['admin-had'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed)
            else:
                with open('admin.json', 'r', encoding = "utf8") as f:
                    admins = json.load(f)
                    admins[str(user)] = str(user.id)
                    with open('admin.json', 'w', encoding = "utf8") as f:
                        json.dump(admins, f, indent = 4)
                load_admin_bypass()
                embed=discord.Embed(title=str(user)+Lang['admin-added'], color=0x81FA28)
                await ctx.channel.send(embed=embed)
                print(now_time(), str(user)+Lang['admin-added'])
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def addbypass(ctx, user: discord.Member=None):
    if data['command-addbypass'] == 'true':
        if ctx.author.guild_permissions.administrator:
            if not user:
                embed = discord.Embed(title=Lang['usage'], description=prefix+'addbypass '+Lang['@user'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed, delete_after=5)
            elif user.id in bypass_list or user.guild_permissions.administrator:
                embed=discord.Embed(title=Lang['bypass-had'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed)
            else:
                with open('bypass.json', 'r', encoding = "utf8") as f:
                    bypass = json.load(f)
                    bypass[str(user)] = str(user.id)
                    with open('bypass.json', 'w', encoding = "utf8") as f:
                        json.dump(bypass, f, indent = 4)
                load_admin_bypass()
                embed=discord.Embed(title=str(user)+Lang['bypass-added'], color=0x81FA28)
                await ctx.channel.send(embed=embed)
                print(now_time(), str(user)+Lang['bypass-added'])
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def ban(ctx, user: discord.Member=None, options='None', *, reason='None'):
    if data['command-ban'] == 'true':
        await ctx.message.delete()
        if not user:
            embed = discord.Embed(title=Lang['usage'], description=prefix+'ban '+Lang['@user']+Lang['reason'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed, delete_after=5)
        elif options == '--sync' and ctx.author.id == int(data['owner-id']):
            embed=discord.Embed(title=str(user)+Lang['user-banned'], description=Lang['warn-reason']+reason, color=0x81FA28)
            try:
                await user.send(embed=embed)
            except:
                pass
            await ctx.guild.ban(user, reason=reason)
            await ctx.channel.send(embed=embed)
            print(now_time(), str(user), Lang['user-banned'], Lang['warn-reason'], reason)
        elif ctx.author.guild_permissions.administrator or ctx.author.id in admin_list:
            if user.id in bypass_list or user.guild_permissions.administrator:
                embed = discord.Embed(title=Lang['user-bypassed'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed)
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
    if data['command-clear'] == 'true':
        if ctx.author.guild_permissions.administrator or ctx.author.id in admin_list:
            await ctx.message.delete()
            if limit == 0:
                embed = discord.Embed(title=Lang['usage'], description='', color=0xEC2E2E)
                embed.add_field(name=prefix+'clear '+Lang['count'], value=Lang['message-clear-tip']+Lang['count']+Lang['message-clear-tip-count'], inline=False)
                embed.add_field(name=prefix+'clear '+Lang['count']+Lang['@user'], value=Lang['message-clear-tip']+Lang['@user']+Lang["someone's"]+' '+Lang['count']+Lang['message-clear-tip-count'], inline=False)
                await ctx.channel.send(embed=embed, delete_after=3)
                return
            msg = []
            if not member:
                await ctx.channel.purge(limit=limit)
                print(now_time(), str(limit), Lang['message-cleared'])
                return await ctx.send(str(limit)+Lang['message-cleared'], delete_after=3)
            async for m in ctx.channel.history():
                if len(msg) == limit:
                    break
                if m.author == member:
                    msg.append(m)
            await ctx.channel.delete_messages(msg)
            await ctx.send(str(member.mention)+Lang["someone's"]+' '+str(limit)+Lang['message-cleared'], delete_after=3)
            print(now_time(), str(member.mention), Lang["someone's"], str(limit), Lang['message-cleared'])
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def chlang(ctx, language=''):
    global Lang
    if data['command-chlang'] == 'true':
        if ctx.author.guild_permissions.administrator or ctx.author.id in admin_list:
            await ctx.message.delete()
            if language == '':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'chlang '+Lang['language'], color=0xEC2E2E)
                embed.add_field(name=Lang['uses'], value=Lang['change-lang-message'], inline=False)
                await ctx.channel.send(embed=embed, delete_after=5)
            else:
                checked = await lang.chlang_check(ctx, language, Lang)
                if checked == False:
                    return
                chlang = 'lang/'+language+'.json'
                with open(chlang, "r", encoding = "utf8") as lang_file:
                    Lang = json.load(lang_file)
                await ctx.channel.send(Lang['lang-changed'])
                print(now_time(), Lang['lang-changed'], language)
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def chact(ctx, *, act=''):
    if data['command-chact'] == 'true':
        if ctx.author.guild_permissions.administrator or ctx.author.id in admin_list:
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
    if data['command-copy'] == 'true':
        if ctx.author.guild_permissions.administrator or ctx.author.id in admin_list:
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
    if data['command-clearwarn'] == 'true':
        if ctx.author.guild_permissions.administrator or ctx.author.id in admin_list:
            if not member:
                embed = discord.Embed(title=Lang['usage'], description=prefix+'clearwarn '+Lang['@user']+' (-a)', color=0xEC2E2E)
                await ctx.channel.send(embed=embed, delete_after=5)
            else:
                with open('warns.json', 'r') as f:
                    warns = json.load(f)
                    if not warns.__contains__(str(member.id)) or int(warns[str(member.id)]) == 0:
                        await ctx.channel.send(Lang['user-nowarn'])
                        return
                    else:
                        if options == '':
                            amount = int(warns[str(member.id)]) - 1
                            warns[str(member.id)] = str(amount)
                            with open('warns.json', 'w') as f:
                                json.dump(warns, f, indent = 4)
                            await ctx.channel.send(Lang['warn-amount']+warns[str(member.id)])
                            print(now_time(), str(member), Lang['warn-amount'], warns[str(member.id)])
                        elif options == '-a':
                            warns[str(member.id)] = '0'
                            with open('warns.json', 'w') as f:
                                json.dump(warns, f, indent = 4)
                            await ctx.channel.send(Lang['warn-cleared-all'])
                            print(now_time(), str(member), Lang['warn-cleared-all'])
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def cd(ctx):
    if data['command-cd'] == 'true':
        if ctx.author.guild_permissions.administrator or ctx.author.id in admin_list:
            await ctx.channel.delete()
            print(now_time(), ctx.channel, Lang['channel-deleted'])
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def ci(ctx):
    if data['command-ci'] == 'true':
        if ctx.author.guild_permissions.administrator or ctx.author.id in admin_list:
            await ctx.message.delete()
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False, view_channel=False)
            await ctx.send(Lang['channel-invisibled'])
            print(now_time(), ctx.channel, Lang['channel-invisibled'])
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def exit(ctx):
    if data['command-exit'] == 'true':
        if ctx.author.id != int(data['owner-id']):
            await ctx.send(Lang['not-owner'], delete_after=3)
            return
        if ctx.author.guild_permissions.administrator or ctx.author.id in admin_list:
            await ctx.message.delete()
            game = discord.Game(now_time())
            await bot.change_presence(status=discord.Status.offline, activity=game)
            sys.exit()
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def gay(ctx, member: discord.Member=None):
    if data['command-gay'] == 'true':
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
    if data['command-kick'] == 'true':
        await ctx.message.delete()
        if not user:
            embed = discord.Embed(title=Lang['usage'], description=prefix+'kick '+Lang['@user']+Lang['reason'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed, delete_after=5)
        elif options == '--sync' and ctx.author.id == int(data['owner-id']):
            embed=discord.Embed(title=str(user)+Lang['user-kicked'], description=Lang['warn-reason']+reason, color=0x81FA28)
            try:
                await user.send(embed=embed)
            except:
                pass
            await ctx.guild.kick(user)
            await ctx.channel.send(embed=embed)
            print(now_time(), str(user), Lang['user-kicked'], Lang['warn-reason'], reason)
        elif ctx.author.guild_permissions.administrator or ctx.author.id in admin_list:
            if user.id in bypass_list or user.guild_permissions.administrator:
                embed = discord.Embed(title=Lang['user-bypassed'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed)
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
    if data['command-mute'] == 'true':
        if not user:
            embed = discord.Embed(title=Lang['usage'], description=prefix+'mute '+Lang['@user']+Lang['reason'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed, delete_after=5)
        elif options == '--sync' and ctx.author.id == int(data['owner-id']):
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
        elif ctx.author.guild_permissions.administrator or ctx.author.id in admin_list:
            if user.id in bypass_list or user.guild_permissions.administrator:
                embed = discord.Embed(title=Lang['user-bypassed'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed)
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
async def RESET(ctx):
    if data['command-reset'] == 'true':
        if ctx.author.id != int(data['owner-id']):
            await ctx.send(Lang['not-owner'], delete_after=3)
            return
        if data['debug-mode'] != 'true':
            await ctx.send(Lang['reset-error'], delete_after=3)
            return
        if ctx.author.id == int(data['owner-id']):
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
    if data['command-reload'] == 'true':
        if ctx.author.guild_permissions.administrator or ctx.author.id in admin_list:
            await ctx.message.delete()
            add_lang()
            load_admin_bypass()
            data = json.load(open('config.json'))
            prefix = data['command-prefix']
            Lang = lang.lang_chose(data['language'], lang_list)
            with open('chatfilter.txt', "r", encoding = "utf8") as words:
                badwords = words.read().split()
            if data['custom-activity'] != '':
                game = discord.Game(data['custom-activity'])
            else:
                game = discord.Game(now_time())
            await bot.change_presence(status=discord.Status.online, activity=game)
            try:
                await ctx.channel.send(Lang['reloaded'])
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
    if data['command-removeadmin'] == 'true':
        if ctx.author.guild_permissions.administrator:
            if not user:
                embed = discord.Embed(title=Lang['usage'], description=prefix+'removeadmin '+Lang['@user'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed, delete_after=5)
            else:
                with open('admin.json', 'r', encoding = "utf8") as f:
                    admins = json.load(f)
                    try:
                        del (admins[str(user)])
                        with open('admin.json', 'w', encoding = "utf8") as f:
                            json.dump(admins, f, indent = 4)
                        load_admin_bypass()
                        embed=discord.Embed(title=str(user)+Lang['admin-removed'], color=0x81FA28)
                        await ctx.channel.send(embed=embed)
                        print(now_time(), str(user)+Lang['admin-removed'])
                    except:
                        embed=discord.Embed(title=Lang['not-in-admin'], color=0xEC2E2E)
                        await ctx.channel.send(embed=embed)
                        print(now_time(), Lang['not-in-admin'])
                
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def removebypass(ctx, user: discord.Member=None):
    if data['command-removebypass'] == 'true':
        if ctx.author.guild_permissions.administrator:
            if not user:
                embed = discord.Embed(title=Lang['usage'], description=prefix+'removebypass '+Lang['@user'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed, delete_after=5)
            else:
                with open('bypass.json', 'r', encoding = "utf8") as f:
                    bypass = json.load(f)
                    try:
                        del (bypass[str(user)])
                        with open('bypass.json', 'w', encoding = "utf8") as f:
                            json.dump(bypass, f, indent = 4)
                        load_admin_bypass()
                        embed=discord.Embed(title=str(user)+Lang['bypass-removed'], color=0x81FA28)
                        await ctx.channel.send(embed=embed)
                        print(now_time(), str(user)+Lang['bypass-removed'])
                    except:
                        embed=discord.Embed(title=Lang['not-in-bypass'], color=0xEC2E2E)
                        await ctx.channel.send(embed=embed)
                        print(now_time(), Lang['not-in-bypass'])
                
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def showwarn(ctx, member: discord.Member=None):
    if data['command-showwarn'] == 'true':
        if ctx.author.guild_permissions.administrator or ctx.author.id in admin_list:
            if not member:
                embed = discord.Embed(title=Lang['usage'], description=prefix+'showwarn '+Lang['@user'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed, delete_after=5)
            else:
                with open('warns.json', 'r') as f:
                    warns = json.load(f)
                    await ctx.channel.send(Lang['warn-amount']+warns[str(member.id)])
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def slowmode(ctx, seconds: int=0):
    if data['command-slowmode'] == 'true':
        if ctx.author.guild_permissions.administrator or ctx.author.id in admin_list:
            await ctx.channel.edit(slowmode_delay=seconds)
            embed = discord.Embed(title=Lang['slowmode-message']+str(seconds)+Lang['slowmode-seconds'], color=0xEC2E2E)
            await ctx.send(embed=embed) 
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def time(ctx):
    if data['command-time'] == 'true':
        await ctx.reply(now_time(), mention_author=True)

@bot.command()
async def tlm(ctx, message=''):
    if data['command-tlm'] == 'true':
        if ctx.author.guild_permissions.administrator or ctx.author.id in admin_list:
            await ctx.message.delete()
            if message == '':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'tlm '+Lang['message'], color=0xEC2E2E)
                embed.add_field(name=Lang['uses'], value=Lang['temp-message'], inline=False)
                await ctx.channel.send(embed=embed, delete_after=5)
            else:
                await ctx.channel.send(message, delete_after=600)
                print(now_time(), ctx.author,Lang['sent-temp-message'],message)
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def tempmute(ctx, user: discord.Member=None, duration='0s', options='None', *, reason='None'):
    if data['command-tempmute'] == 'true':
        if not user:
            embed = discord.Embed(title=Lang['usage'], description=prefix+'tempmute '+Lang['@user']+Lang['duration']+Lang['reason'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed, delete_after=5)
        elif options == '--sync' and ctx.author.id == int(data['owner-id']):
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
        elif ctx.author.guild_permissions.administrator or ctx.author.id in admin_list:
            if user.id in bypass_list or user.guild_permissions.administrator:
                embed = discord.Embed(title=Lang['user-bypassed'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed)
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
    if data['command-tempban'] == 'true':
        if not user:
            embed = discord.Embed(title=Lang['usage'], description=prefix+'tempban '+Lang['@user']+Lang['duration']+Lang['reason'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed, delete_after=5)
        elif options == '--sync' and ctx.author.id == int(data['owner-id']):
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
        elif ctx.author.guild_permissions.administrator or ctx.author.id in admin_list:
            if user.id in bypass_list or user.guild_permissions.administrator:
                embed = discord.Embed(title=Lang['user-bypassed'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed)
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
    if data['command-unban'] == 'true':
        await ctx.message.delete()
        if ctx.author.guild_permissions.administrator or ctx.author.id in admin_list:
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
                    embed = discord.Embed(title='該成員未被封鎖', color=0xEC2E2E)
                    await ctx.channel.send(embed=embed)
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def unmute(ctx, user: discord.Member=None):
    if data['command-unmute'] == 'true':
        if ctx.author.guild_permissions.administrator or ctx.author.id in admin_list:
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
    if data['command-uinfo'] == 'true':
        await ctx.message.delete()
        if ctx.author.guild_permissions.administrator or ctx.author.id in admin_list:
            target = target or ctx.author
            with open('warns.json', 'r') as f:
                warns = json.load(f)
            if not warns.__contains__(str(target)):
                amount = '0'
            else:
                amount = warns[str(target)]
            embed = discord.Embed(title=Lang['user-info'], colour=target.colour, timestamp=datetime.utcnow())
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
    if data['command-warn'] == 'true':
        if not user:
            embed = discord.Embed(title=Lang['usage'], description=prefix+'warn '+Lang['@user']+Lang['reason'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed, delete_after=5)
        elif options == '--sync' and ctx.author.id == int(data['owner-id']):
            with open('warns.json', 'r') as f:
                warns = json.load(f)
                if not warns.__contains__(str(user.id)):
                    warns[str(user.id)] = '1'
                else:
                    amount = int(warns[str(user.id)]) + 1
                    warns[str(user.id)] = str(amount)
                with open('warns.json', 'w') as f:
                    json.dump(warns, f, indent = 4)
            embed=discord.Embed(title=str(user)+Lang['user-warned'], description=Lang['warn-reason']+reason, color=0x81FA28)
            await ctx.channel.send(embed=embed)
            await user.send(embed=embed)
            print(now_time(), str(user), Lang['user-warned'], Lang['warn-reason'], reason)
            if warns[str(user.id)] == data['auto-mute'] :
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
            if warns[str(user.id)] == data['auto-kick']:
                reason = Lang['when-warnings-match']+data['auto-mute']+Lang['auto-kick-message']
                embed=discord.Embed(title=str(user)+Lang['user-kicked'], description=Lang['warn-reason']+reason, color=0x81FA28)
                await user.send(embed=embed)
                await ctx.guild.kick(user)
                await ctx.channel.send(embed=embed)
                print(now_time(), str(user), Lang['user-kicked'], Lang['warn-reason'], reason)
            if warns[str(user.id)] == data['auto-ban']:
                reason = Lang['when-warnings-match']+data['auto-mute']+Lang['auto-ban-message']
                embed=discord.Embed(title=str(user)+Lang['user-banned'], description=Lang['warn-reason']+reason, color=0x81FA28)
                await user.send(embed=embed)
                await ctx.guild.ban(user, reason=reason)
                await ctx.channel.send(embed=embed)
                print(now_time(), str(user), Lang['user-banned'], Lang['warn-reason'], reason)
        elif ctx.author.guild_permissions.administrator or ctx.author.id in admin_list:
            if user.id in bypass_list or user.guild_permissions.administrator:
                embed = discord.Embed(title=Lang['user-bypassed'], color=0xEC2E2E)
                await ctx.channel.send(embed=embed)
            else:
                with open('warns.json', 'r') as f:
                    warns = json.load(f)
                    if not warns.__contains__(str(user.id)):
                        warns[str(user.id)] = '1'
                    else:
                        amount = int(warns[str(user.id)]) + 1
                        warns[str(user.id)] = str(amount)
                    with open('warns.json', 'w') as f:
                        json.dump(warns, f, indent = 4)
                embed=discord.Embed(title=str(user)+Lang['user-warned'], description=Lang['warn-reason']+options, color=0x81FA28)
                await ctx.channel.send(embed=embed)
                await user.send(embed=embed)
                print(now_time(), str(user), Lang['user-warned'], Lang['warn-reason'], options)
                if warns[str(user.id)] == data['auto-mute'] :
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
                if warns[str(user.id)] == data['auto-kick']:
                    reason = Lang['when-warnings-match']+data['auto-mute']+Lang['auto-kick-message']
                    embed=discord.Embed(title=str(user)+Lang['user-kicked'], description=Lang['warn-reason']+reason, color=0x81FA28)
                    await user.send(embed=embed)
                    await ctx.guild.kick(user)
                    await ctx.channel.send(embed=embed)
                    print(now_time(), str(user), Lang['user-kicked'], Lang['warn-reason'], reason)
                if warns[str(user.id)] == data['auto-ban']:
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
    if message.author == bot.user or message.author.bot:
        return
    if message.channel.id == int(data['picture-only-channel-id']) and message.content != "":
        await message.channel.purge(limit=1)
    if data['chat-filter'] == 'true':
        if message.author.id in bypass_list or message.author.guild_permissions.administrator:
            await bot.process_commands(message)
            return
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
                        with open('warns.json', 'r') as f:
                            warns = json.load(f)
                            if not warns.__contains__(str(message.author.id)):
                                warns[str(message.author.id)] = '1'
                            else:
                                amount = int(warns[str(message.author.id)]) + 1
                                warns[str(message.author.id)] = str(amount)
                            with open('warns.json', 'w') as f:
                                json.dump(warns, f, indent = 4)
                        embed=discord.Embed(title=str(message.author)+Lang['user-warned'], description=Lang['warn-reason']+reason, color=0x81FA28)
                        await message.channel.send(embed=embed)
                        await message.author.send(embed=embed)
                        print(now_time(), str(message.author), Lang['user-warned'], Lang['warn-reason'], reason)
                        if warns[str(message.author.id)] == data['auto-mute'] :
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
                        if warns[str(message.author.id)] == data['auto-kick']:
                            reason = Lang['when-warnings-match']+data['auto-mute']+Lang['auto-kick-message']
                            embed=discord.Embed(title=str(message.author)+Lang['user-kicked'], description=Lang['warn-reason']+reason, color=0x81FA28)
                            await message.author.send(embed=embed)
                            await message.guild.kick(message.author)
                            await message.channel.send(embed=embed)
                            print(now_time(), str(message.author), Lang['user-kicked'], Lang['warn-reason'], reason)
                        if warns[str(message.author.id)] == data['auto-ban']:
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

global player_repeat
gPlaylist = []
music_name = []
player_repeat = False
button_switch = False

async def playit(ctx):
    global gPlaylist
    global player_repeat, music_name, button_switch
    try:
        if not player_repeat:
            gPlaylist.pop(0)
            music_name.pop(0)
        sourcex = gPlaylist[0]
        br = mechanize.Browser()
        try:
            br.open(sourcex)
        except:
            pass
        try:
            ydl_opts = {
                'format': 'bestaudio',
                'noplaylist': True,
                'default_search': 'auto'
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(gPlaylist[0], download=False)
                if 'entries' in info:
                    Url = info['entries'][0]["formats"][0]['url']
                elif 'formats' in info:
                    Url = info["formats"][0]['url']
        except:
            Url = gPlaylist[0]
        pplayer = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(Url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), 1)
        bot.voice_clients[0].play(pplayer, after = lambda e: myafter(ctx))
        button_switch = True
        if not player_repeat:
            await music_button_1(ctx, sourcex, info)
    except:
        pass
        
def myafter(ctx):
    global button_switch
    button_switch = False
    fut = asyncio.run_coroutine_threadsafe(playit(ctx), bot.loop)
    fut.result()

async def music_button_1(ctx, url, info):
    global player_repeat, after_volume, button_switch
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
    embed.set_footer(text=now_time(), icon_url=ctx.author.avatar_url)
    music_info = await ctx.channel.send(embed=embed)
    music_menu = await ctx.send('', components = [[
        Button(label=Lang['music-link'], style=ButtonStyle.URL, url=Info.get('webpage_url')),
        Button(label=Lang['music-list'], style='2', custom_id='list', emoji='📜'),
        Button(label=Lang['music-repeat'], style='2', custom_id='repeat', emoji='🔁')],[
        Button(label=Lang['music-pause'], style='1', custom_id='pause', emoji='⏸'),
        Button(label=Lang['music-resume'], style='1', custom_id='resume', emoji='⏯'),
        Button(label=Lang['music-stop'], style='4', custom_id='stop', emoji='⏹'),
        Button(label=Lang['music-skip'], style='2', custom_id='skip', emoji='⏩')
    ]])
    while True:
        if button_switch == False: 
            return 
        else:
            interaction = await bot.wait_for('button_click')
            res = interaction.custom_id
            try:
                if res == 'pause':
                    await interaction.send(Lang['selected']+res)
                    await pause(ctx)
                elif res == 'stop':
                    await interaction.send(Lang['selected']+res)
                    await stop(ctx)
                    break
                elif res == 'resume':
                    await interaction.send(Lang['selected']+res)
                    await resume(ctx)
                elif res == 'list':
                    await interaction.send(Lang['selected']+res)
                    await playlist(ctx)
                elif res == 'skip':
                    await interaction.send(Lang['selected']+res)
                    await skip(ctx)
                    break
                elif res == 'repeat':
                    await repeat(ctx)
                    await music_menu.delete()
                    await music_info.delete()
                    await music_button_2(ctx, url, info)
                    return
            except:
                pass
    return
async def music_button_2(ctx, url, info):
    global player_repeat, after_volume, button_switch
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
    embed.set_footer(text=now_time(), icon_url=ctx.author.avatar_url)
    music_info_2 = await ctx.channel.send(embed=embed)
    music_menu_2 = await ctx.send('', components = [[
        Button(label=Lang['music-link'], style=ButtonStyle.URL, url=Info.get('webpage_url')),
        Button(label=Lang['music-list'], style='2', custom_id='list', emoji='📜'),
        Button(label=Lang['music-repeat'], style='3', custom_id='repeat', emoji='🔁')],[
        Button(label=Lang['music-pause'], style='1', custom_id='pause', emoji='⏸'),
        Button(label=Lang['music-resume'], style='1', custom_id='resume', emoji='⏯'),
        Button(label=Lang['music-stop'], style='4', custom_id='stop', emoji='⏹'),
        Button(label=Lang['music-skip'], style='2', custom_id='skip', emoji='⏩')
    ]])
    while True:
        if button_switch == False:
            return
        else:
            interaction = await bot.wait_for('button_click')
            res = interaction.custom_id
            try:
                if res == 'pause':
                    await interaction.send(Lang['selected']+res)
                    await pause(ctx)
                elif res == 'stop':
                    await interaction.send(Lang['selected']+res)
                    await stop(ctx)
                    break
                elif res == 'resume':
                    await interaction.send(Lang['selected']+res)
                    await resume(ctx)
                elif res == 'list':
                    await interaction.send(Lang['selected']+res)
                    await playlist(ctx)
                elif res == 'skip':
                    await interaction.send(Lang['selected']+res)
                    await skip(ctx)
                    break
                elif res == 'repeat':
                    await repeat(ctx)
                    await music_menu_2.delete()
                    await music_info_2.delete()
                    await music_button_1(ctx, url, info)
                    return
            except:
                pass
    return

@bot.command(aliases=['p'])
async def play(ctx, *, url: str=''):
    global music_name, button_switch
    if data['music-bot'] == 'true':
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
        ydl_opts = {
            'format': 'bestaudio',
            'noplaylist': True,
            'default_search': 'auto'
        }
        try:
            await voiceChannel.connect()
        except:
            pass
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        gPlaylist.append(url)
        await ctx.message.add_reaction('✅')
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                Url = info['entries'][0]["formats"][0]['url']
                music_name.append(info['entries'][0]['title'])
            elif 'formats' in info:
                Url = info["formats"][0]['url']
                music_name.append(info['title'])
            
            pplayer = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(Url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), 1)
            voice.play(pplayer, after = lambda e: myafter(ctx))
            button_switch = True
            await music_button_1(ctx, url, info)
        except:
            embed = discord.Embed(title='✅｜'+Lang['playlist_added'], color=0x81FA28)
            await ctx.reply(embed=embed)
    
@bot.command()
async def connect(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    try:
        voiceChannel = discord.utils.get(ctx.guild.voice_channels, id=ctx.author.voice.channel.id)
    except:
        embed = discord.Embed(title='❌｜'+Lang['music-user-not-in-channel'], color=0xEC2E2E)
        await ctx.reply(embed=embed)
        return
    try:
        if voice.is_connected():
            await voice.disconnect()
    except:
        pass
    await voiceChannel.connect()

@bot.command()
async def leave(ctx):
    if data['music-bot'] == 'true':
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        try:
            if voice.is_connected():
                await voice.disconnect()
        except:
            embed = discord.Embed(title='❌｜'+Lang['music-bot-not-in-channel'], color=0xEC2E2E)
            await ctx.reply(embed=embed)

@bot.command()
async def pause(ctx):
    if data['music-bot'] == 'true':
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        try:
            if voice.is_playing():
                voice.pause()
        except:
            embed = discord.Embed(title='❌｜'+Lang['music-nothing-playing'], color=0xEC2E2E)
            await ctx.reply(embed=embed)

@bot.command()
async def resume(ctx):
    if data['music-bot'] == 'true':
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        try:
            if voice.is_paused():
                voice.resume()
        except:
            embed = discord.Embed(title='❌｜'+Lang['music-nothing-pause'], color=0xEC2E2E)
            await ctx.reply(embed=embed)

@bot.command()
async def repeat(ctx):
    if data['music-bot'] == 'true':
        global player_repeat
        if player_repeat:
            player_repeat = False
            embed = discord.Embed(title='🔁｜'+Lang['repeat-disabled'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed)
            return
        else:
            player_repeat = True
            embed = discord.Embed(title='🔁｜'+Lang['repeat-enabled'], color=0x81FA28)
            await ctx.channel.send(embed=embed)
            return

@bot.command()
async def stop(ctx):
    global player_repeat, gPlaylist, music_name, button_switch
    if data['music-bot'] == 'true':
        gPlaylist.clear()
        music_name.clear()
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        player_repeat = False
        button_switch = False
        try:
            voice.stop()
        except:
            embed = discord.Embed(title='❌｜'+Lang['music-nothing-playing'], color=0xEC2E2E)
            await ctx.reply(embed=embed)
        return

@bot.command()
async def volume(ctx, volume: int=100):
    if data['music-bot'] == 'true':
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
    global player_repeat, button_switch
    if data['music-bot'] == 'true':
        player_repeat = False
        button_switch = False
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        try:
            voice.stop()
        except:
            await ctx.channel.send(Lang['music-nothing-playing'])
        return

@bot.command(aliases=['pl'])
async def playlist(ctx):
    global music_name
    if data['music-bot'] == 'true':
        if music_name == []:
            embed = discord.Embed(title='❌｜'+Lang['music-nothing-playing'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed)
            return
        else:
            embed = discord.Embed(title='📜｜'+Lang['music-list'], color=0x79EF2F)
            for playlist in range(len(music_name)):
                if playlist == 0:
                    embed.add_field(name=music_name[playlist], value=Lang['music-playing'], inline=False)
                else:
                    embed.add_field(name=music_name[playlist], value='No. '+str(playlist), inline=False)
        await ctx.send(embed=embed)

@bot.command()
async def listmove(ctx, before: int, after: int):
    global gPlaylist, music_name
    if data['music-bot'] == 'true':
        if before == 0:
            embed = discord.Embed(title='❌｜'+Lang['move-error'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed)
            return
        elif before > len(gPlaylist)-1 or after > len(gPlaylist)-1:
            embed = discord.Embed(title='❌｜'+Lang['out-range'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed)
            return
        music_url = gPlaylist[before]
        music = music_name[before]
        del gPlaylist[before]
        gPlaylist.insert(after, music_url)
        del music_name[before]
        music_name.insert(after, music)
        embed = discord.Embed(title='🔃｜'+Lang['music-moved'], color=0x81FA28)
        await ctx.channel.send(embed=embed)

@bot.command()
async def listremove(ctx, number:int):
    global gPlaylist, music_name
    if data['music-bot'] == 'true':
        if number == 0:
            embed = discord.Embed(title='❌｜'+Lang['delete-error'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed)
            return
        elif number > len(gPlaylist)-1 or number > len(gPlaylist)-1:
            embed = discord.Embed(title='❌｜'+Lang['out-range'], color=0xEC2E2E)
            await ctx.channel.send(embed=embed)
            return
        del gPlaylist[number]
        del music_name[number]
        embed = discord.Embed(title='🗑｜'+Lang['music-deleted'], color=0x81FA28)
        await ctx.channel.send(embed=embed)


#
@bot.command()
async def ping(ctx, *, ip: str=''):
    if data['command-warn'] == 'true':
        TTL = random.randrange(50, 200)
        suc = fail = ms = 0
        ping_list = []
        info = ''
        for i in range(4):
            response = pin(ip)
            if response:
                delay = int(response*1000)
                ping_list.append(delay)
                info += f'回覆自 {ip}: 位元組=32 時間={delay}ms TTL={TTL}\n'
                await asyncio.sleep(response)
                suc += 1
                ms += delay
            else:
                info += f'要求等候逾時\n'
                ping_list.append('N/A')
                fail += 1
        ping_list.sort()
        embed = discord.Embed(title=f'Ping [{ip}] (使用 32 位元組的資料):', description=info, color=0x00AAAA)
        embed.add_field(name=f'{ip} 的 Ping 統計資料:', value=f'封包: 已傳送 = 4，已收到 = {suc}, 已遺失 = {fail} ({float(fail/4*100)}% 遺失)，', inline=False)
        embed.add_field(name='大約的來回時間 (毫秒):', value=f'最小值 = {ping_list[0]}ms，最大值 = {ping_list[-1]}ms，平均 = {int(ms/4)}ms', inline=False)
        await ctx.send(embed=embed)

@bot.command()
async def tick(ctx, category: int=000000000000000000):
    await ctx.message.delete()
    guild = ctx.guild
    Guild = discord.utils.get(guild.categories, id= category)
    if category == 000000000000000000:
        embed = discord.Embed(title=Lang['usage'], description=prefix+'tick '+Lang['category'], color=0xEC2E2E)
        await ctx.channel.send(embed=embed, delete_after=5)
    else:
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
                await tick_create(guild, Guild, interaction)
            else:
                pass

async def tick_create(guild, Guild, member):
    global tick_message
    tick_message = await guild.create_text_channel(str(member.author.name)+' 的專案', overwrites=None, category = Guild)
    await tick_message.set_permissions(member.author, send_messages=True, view_channel=True)
    await tick_message.set_permissions(guild.default_role, send_messages=False, view_channel=False)
    embed = discord.Embed(title='', color=0xEDFA28)
    embed.add_field(name='歡迎來到處理專案', value='管理員會盡快回覆你\n如要關閉專案請點擊以下按鈕', inline=False)
    await tick_message.send(f"<@{member.author.id}>", embed=embed)
    await tick_message.send('', components = [
        Button(label='關閉專案', style='4', custom_id='close_tick', emoji='🔒')])

@bot.event
async def on_button_click(interaction):
    if interaction.component.label.startswith("關閉專案"):
        await interaction.send('專案已關閉')
        await tick_message.set_permissions(interaction.author, send_messages=False, view_channel=False)

bot.run(data['token'])

# music bot(favorite), ticket tool, blind, tempblind

# (voice)channel delete, create
# role delete, create

# online count, total conut

# tempmute, tempban, chatfilter