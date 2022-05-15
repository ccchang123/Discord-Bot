import discord
import json
import os
from lib import self_test

async def chlang_check(message, lang, Lang, data):
    check_config = os.path.isfile('lang/'+lang+'.json')
    if not check_config:
        embed = discord.Embed(title='❌｜'+Lang['language-error'], color=0xEC2E2E)
        await message.channel.send(embed=embed)
        if data['debug-mode']:
            print('load '+lang+' file --- fail')
        return False
    else:
        if data['debug-mode']:
            print('load '+lang+' file --- success')
        return True

def lang_chose(sele, lang_list, data):
    for i in lang_list:
        if sele == i:
            select = 'lang/'+i+'.json'
            check_config = os.path.isfile(select)
            if not check_config:
                if data['debug-mode']:
                    add_lang()
                    print('load '+i+' file --- fail',end='\n\n')
                self_test.error()
            else:
                with open(select, "r", encoding = "utf8") as lang_file:
                    language = json.load(lang_file)
                if data['debug-mode']:
                    add_lang()
                    print('load '+i+' file --- success',end='\n\n')
            return language
    language = None
    return language

def add_lang():
    for i in os.listdir('lang'):
        if i.endswith(".json"):
            print('find the language file:',i)
    print('')