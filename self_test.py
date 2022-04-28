import os, json

def error():
    error = input('Press Enter to continue')
    exit()

def check(data, lang_list):
    global error
    for language_set in lang_list:
        if data['language'] == language_set:
            found = True
            break
        else:
            found = False
    if found == True :
        print('load language setting --- ok')
    else:
        print('load language setting --- fail')
        error()

    if data['token'] != '':
        if data['debug-mode'] == 'true':
            print('load token setting --- ok')
    else:
        if data['debug-mode'] == 'true':
            print('load token setting --- fail')
            error()

    if data['command-prefix'] != '':
        if data['debug-mode'] == 'true':
            print('load command-prefix setting --- ok')
    else:
        if data['debug-mode'] == 'true':
            print('load command-prefix setting --- fail')
            error()
    
    if data['owner-id'] == '':
        if data['debug-mode'] == 'true':
            print('load owner-id setting --- fail')
        error()
    else:
        if data['debug-mode'] == 'true':
            print('load owner-id setting --- ok')

    if data['local-channel-id'] == '' or data['create-category-id'] == '' or data['picture-only-channel-id'] == '' or data['ticket-category-id'] == '':
        if data['debug-mode'] == 'true':
           print('load channel-id setting --- fail',end='\n\n')
        error()
    else:
        if data['debug-mode'] == 'true':
            print('load channel-id setting --- ok',end='\n\n')

    with open('config.json', "r", encoding="utf8") as file:
        data = json.load(file)
    data_list = list(data.values())
    bool_list = ['true', 'false']
    if data_list[14] not in bool_list:
        if data['debug-mode'] == 'true':
            print('in config setting:', data_list[14],'<-- only can be "true" or "false"')
        error()
    for i in range(16, len(data_list)):
        if data_list[i] != 'true' and 'false':
            if data['debug-mode'] == 'true':
                print('in config setting:', data_list[i],'<-- only can be "true" or "false"')
            error()

def check_file():
    file_list = ['warns.json', 'userdata.json', 'chatfilter.txt', 'favorite.json']
    for file in file_list:
        if not os.path.isfile(file):
            print(f'load {file} file --- fail')
            error()
        else:
            print(f'load {file} file --- ok')
    if not os.path.isdir('lang/'):
        print('load lang folder --- fail',end='\n\n')
        error()
    else:
        print('load lang folder --- ok',end='\n\n')
