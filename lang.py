import json
import os
import self_test

with open('config.json', "r", encoding = "utf8") as file:
    data = json.load(file)

def check(lang):
    check_config = os.path.isfile('lang/'+lang+'.json')
    if check_config == False:
        print('load '+lang+' file --- fail')
        self_test.error()
    else:
        print('load '+lang+' file --- ok')

async def chlang_check(message, lang, Lang):
    check_config = os.path.isfile('lang/'+lang+'.json')
    if check_config == False:
        await message.channel.send(Lang['language-error'])
        if data['debug-mode'] == 'true':
            print('load '+lang+' file --- fail')
        return False
    else:
        if data['debug-mode'] == 'true':
            print('load '+lang+' file --- ok')

def lang_chose(sele):
    if sele == 'zh-tw':
        check(sele)
        with open('lang/zh-tw.json', "r", encoding = "utf8") as lang_file:
            language = json.load(lang_file)
    elif sele == 'zh-cn':
        check(sele)
        with open('lang/zh-cn.json', "r", encoding = "utf8") as lang_file:
            language = json.load(lang_file)
    elif sele == 'en-us':
        check(sele)
        with open('lang/en-us.json', "r", encoding = "utf8") as lang_file:
            language = json.load(lang_file)
    return language