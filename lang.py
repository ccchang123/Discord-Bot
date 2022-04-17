import json
import os
import self_test

def add_lang():
    for i in os.listdir('lang'):
        if i.endswith(".json"):
            print('find the language file:',i)

with open('config.json', "r", encoding = "utf8") as file:
    data = json.load(file)

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

def lang_chose(sele, lang_list):
    for i in lang_list:
        if sele == i:
            select = 'lang/'+i+'.json'
            check_config = os.path.isfile(select)
            if check_config == False:
                if data['debug-mode'] == 'true':
                    add_lang()
                    print('load '+i+' file --- fail',end='\n\n')
                    self_test.error()
            else:
                with open(select, "r", encoding = "utf8") as lang_file:
                    language = json.load(lang_file)
                if data['debug-mode'] == 'true':
                    add_lang()
                    print('load '+i+' file --- ok',end='\n\n')
            return language
    language = None
    return language

