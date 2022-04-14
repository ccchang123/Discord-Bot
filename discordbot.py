import discord
from datetime import datetime
from discord.ext import tasks, commands
from discord_components import *
import random
import asyncio
import sys
import json
import os
import logging
import tracemalloc
import error_code, self_test, reset

print('Copyright © 2022 cc_chang.','All rights reserved.',sep='\n' ,end='\n\n')
print('View more information in github:', 'https://github.com/ccchang123/Discord-Bot.git','---------------------------------------------',sep='\n')

check_config = os.path.isfile('config.json')
if check_config == False:
    print('load config file --- fail')
    self_test.error()
else:
    print('load config file --- ok')
    import lang

check_lang = os.path.isdir('lang/')
if check_lang == False:
    print('load lang folder --- fail',end='\n\n')
    self_test.error()
else:
    print('load lang folder --- ok',end='\n\n')

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

prefix = data['command-prefix']
intents = discord.Intents.all()
bot = ComponentsBot(data['command-prefix'])

def now_time():
    now = datetime.now()
    date_time = '<'+now.strftime("%Y-%m-%d, %H:%M:%S")+'>'
    return date_time

tracemalloc.start()

async def main_menu(ctx):
    await ctx.send(content=Lang['menu-name'], components=[Select(
                                                placeholder=Lang['menu-select'],
                                                options= [
                                                    SelectOption(label=prefix+'clear',value=prefix+'clear'),
                                                    SelectOption(label=prefix+'chlang',value=prefix+'chlang'),
                                                    SelectOption(label=prefix+'chact',value=prefix+'chact'),
                                                    SelectOption(label=prefix+'copy',value=prefix+'copy'),
                                                    SelectOption(label=prefix+'copy -d',value=prefix+'copy'+'-d'),
                                                    SelectOption(label=prefix+'exit',value=prefix+'exit'),
                                                    SelectOption(label=prefix+'gay',value=prefix+'gay'),
                                                    SelectOption(label=prefix+'reload',value=prefix+'reload'),
                                                    SelectOption(label=prefix+'time',value=prefix+'time'),
                                                    SelectOption(label=prefix+'tlm',value=prefix+'tlm')
                                                ],
                                                custom_id='main_menu'
    )])
    interaction = await bot.wait_for('select_option', check=lambda inter: inter.custom_id == 'main_menu' and inter.user == ctx.author)
    res = interaction.values[0]
    if res == prefix+'time':
        await interaction.send(Lang['selected']+res)
        await time(ctx)
    elif res == prefix+'clear':
        await interaction.send(Lang['selected']+res)
        await clear(ctx)
    elif res == prefix+'chlang':
        await interaction.send(Lang['selected']+res)
        await chlang(ctx)
    elif res == prefix+'chact':
        await interaction.send(Lang['selected']+res)
        await chact(ctx)
    elif res == prefix+'copy':
        await interaction.send(Lang['selected']+res)
        await copy(ctx)
    elif res == prefix+'copy'+'-d':
        await interaction.send(Lang['selected']+res)
        await copy(ctx, '-d')
    elif res == prefix+'gay':
        await interaction.send(Lang['selected']+res)
        await gay(ctx)
    elif res == prefix+'exit':
        await interaction.send(Lang['selected']+res)
        await exit(ctx)
    elif res == prefix+'reload':
        await interaction.send(Lang['selected']+res)
        await reload(ctx)
    elif res == prefix+'tlm':
        await interaction.send(Lang['selected']+res)
        await tlm(ctx)

@bot.event
async def on_ready():
    print(now_time(), Lang['login-name'], bot.user)
    if data['custom-activity'] != '':
        game = discord.Game(data['custom-activity'])
    else:
        game = discord.Game(now_time())
    #online,offline,idle,dnd,invisible
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
    if channel.id == int(data['local-channel-id']):
        guild = after.channel.guild
        private_channels = discord.utils.get(guild.categories, id= int(data['create-category-id']))
        voice_channel = await guild.create_voice_channel(member.name + Lang['create-channel-name'], overwrites=None, category=private_channels)
        await member.move_to(voice_channel)
        await voice_channel.set_permissions(member, manage_channels=True, manage_permissions=True)
        print(now_time(), member.name, Lang['when-channel-create'])

@bot.command()
async def menu(ctx):
    await main_menu(ctx)

@bot.command()
async def clear(ctx, limit=0, member: discord.Member=None):
    if data['command-clear'] == 'true':
        if ctx.author.id == int(data['admin-id-1']) or ctx.author.id == int(data['admin-id-2']) or ctx.author.id == int(data['owner-id']):
            await ctx.message.delete()
            if limit == 0:
                embed = discord.Embed(title=Lang['usage'], description='', color=0x4b49d8)
                embed.add_field(name=prefix+'clear '+Lang['count'], value=Lang['message-clear-tip']+Lang['count']+Lang['message-clear-tip-count'], inline=False)
                embed.add_field(name=prefix+'clear '+Lang['count']+Lang['@user'], value=Lang['message-clear-tip']+Lang['@user']+Lang["someone's"]+' '+Lang['count']+Lang['message-clear-tip-count'], inline=False)
                await ctx.channel.send(embed=embed, delete_after=3)
                return
            msg = []
            if not member:
                await ctx.channel.purge(limit=limit)
                return await ctx.send(str(limit)+Lang['message-cleared'], delete_after=3)
            async for m in ctx.channel.history():
                if len(msg) == limit:
                    break
                if m.author == member:
                    msg.append(m)
            await ctx.channel.delete_messages(msg)
            await ctx.send(str(member.mention)+Lang["someone's"]+' '+str(limit)+Lang['message-cleared'], delete_after=3)
    else:
        await error_code.permission(ctx, Lang)

@bot.command()
async def chlang(ctx, language=''):
    global Lang
    if data['command-chlang'] == 'true':
        if ctx.author.id == int(data['admin-id-1']) or ctx.author.id == int(data['admin-id-2']) or ctx.author.id == int(data['owner-id']):
            await ctx.message.delete()
            if language == '':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'chlang '+Lang['language'], color=0x4b49d8)
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
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def chact(ctx, act=''):
    if data['command-chact'] == 'true':
        if ctx.author.id == int(data['admin-id-1']) or ctx.author.id == int(data['admin-id-2']) or ctx.author.id == int(data['owner-id']):
            await ctx.message.delete()
            if act == '':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'chact '+Lang['message'], color=0x4b49d8)
                await ctx.channel.send(embed=embed, delete_after=5)
            else:
                game = discord.Game(act)
                await bot.change_presence(status=discord.Status.online, activity=game)
                await ctx.channel.send(Lang['activity-changed']+' '+act)
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def exit(ctx):
    if data['command-exit'] == 'true':
        if ctx.author.id == int(data['admin-id-1']) or ctx.author.id == int(data['admin-id-2']) or ctx.author.id == int(data['owner-id']):
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
            embed = discord.Embed(title=Lang['usage'], description=prefix+'gay '+Lang['@user'], color=0x4b49d8, icon_url='https://cdn.discordapp.com/avatars/413271975775961099/687e9729272d78c5b774e006ef4bd2e6.png?size=4096')
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
async def RESET(ctx):
    if data['command-reset'] == 'true':
        if ctx.author.id != int(data['owner-id']):
            await ctx.send(Lang['not-owner'], delete_after=3)
            return
        if data['debug-mode'] != 'true':
            await ctx.send(Lang['reset-error'], delete_after=3)
            return
        if ctx.author.id == int(data['admin-id-1']) or ctx.author.id == int(data['admin-id-2']) or ctx.author.id == int(data['owner-id']):
            reset.reset_config()
            sys.exit()
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def reload(ctx):
    global data, prefix, Lang
    if data['command-reload'] == 'true':
        if ctx.author.id == int(data['admin-id-1']) or ctx.author.id == int(data['admin-id-2']) or ctx.author.id == int(data['owner-id']):
            print(now_time(), Lang['reloaded'])
            await ctx.message.delete()
            data = json.load(open('config.json'))
            prefix = data['command-prefix']
            Lang = lang.lang_chose(data['language'])
            if data['custom-activity'] != '':
                game = discord.Game(data['custom-activity'])
            else:
                game = discord.Game(now_time())
            await bot.change_presence(status=discord.Status.online, activity=game)
            await ctx.channel.send(Lang['reloaded'])
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def time(ctx):
    if data['command-time'] == 'true':
        await ctx.reply(now_time(), mention_author=True)

@bot.command()
async def tlm(ctx, message=''):
    if data['command-tlm'] == 'true':
        if ctx.author.id == int(data['admin-id-1']) or ctx.author.id == int(data['admin-id-2']) or ctx.author.id == int(data['owner-id']):
            await ctx.message.delete()
            if message == '':
                embed = discord.Embed(title=Lang['usage'], description=prefix+'tlm '+Lang['message'], color=0x4b49d8)
                embed.add_field(name=Lang['uses'], value=Lang['temp-message'], inline=False)
                await ctx.channel.send(embed=embed, delete_after=5)
            else:
                await ctx.channel.send(message, delete_after=600)
                print(now_time(), ctx.author,Lang['sent-temp-message'],message)
        else:
            await error_code.permission(ctx, Lang)

@bot.command()
async def copy(ctx, delete=''):
    if data['command-copy'] == 'true':
        if ctx.author.id == int(data['admin-id-1']) or ctx.author.id == int(data['admin-id-2']) or ctx.author.id == int(data['owner-id']):
            await ctx.message.delete()
            if delete == '':
                await ctx.channel.clone()
            elif delete == '-d':
                await ctx.channel.clone()
                await ctx.channel.delete()
        else:
            await error_code.permission(ctx, Lang)

@bot.event
async def on_message(message):
    global data, prefix, Lang
    admin = False
    if message.author.id == int(data['admin-id-1']) or message.author.id == int(data['admin-id-2']) or message.author.id == int(data['owner-id']):
        admin = True
    if message.author == bot.user:
        return

    if message.channel.id == int(data['picture-only-channel-id']) and message.content != "":
        await message.channel.purge(limit=1)
    await bot.process_commands(message)

bot.run(data['token'])
