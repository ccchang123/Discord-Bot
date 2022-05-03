import os, json, hashlib, requests

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
        print('load language setting --- success')
    else:
        print('load language setting --- fail')
        error()

    if data['token'] == '':
        if data['debug-mode']:
            print('load token setting --- fail')
        error()
    else:
        if data['debug-mode']:
            print('load token setting --- success')

    if data['command-prefix'] != '':
        if data['debug-mode']:
            print('load command-prefix setting --- success')
    else:
        if data['debug-mode']:
            print('load command-prefix setting --- fail')
        error()
    
    if data['owner-id'] == '':
        if data['debug-mode']:
            print('load owner-id setting --- fail')
        error()
    else:
        if data['debug-mode']:
            print('load owner-id setting --- success')

    if data['local-channel-id'] == '' or data['create-category-id'] == '' or data['picture-only-channel-id'] == '' or data['ticket-category-id'] == '':
        if data['debug-mode']:
           print('load channel-id setting --- fail',end='\n\n')
        error()
    else:
        if data['debug-mode']:
            print('load channel-id setting --- success',end='\n\n')

def check_config():
    try:
        with open('config.json', "r", encoding="utf8") as file:
            data = json.load(file)
        print('load config setting --- success')
    except:
        print('load config setting --- fail')
        error()
    data_list = list(data.values())
    command_data_list = list(data['commands'].values())
    num_list =[14, 16, 18, 19]
    bool_list = [True, False]
    for i in num_list:
        if data_list[i] not in bool_list:
            if data['debug-mode']:
                print('Error: In config setting:', data_list[i],'<-- only can be "true" or "false"')
            error()
    for j in command_data_list:
        if j not in bool_list:
            if data['debug-mode']:
                print('Error: In config setting:', j,'<-- only can be "true" or "false"')
            error()

def check_file():
    file_list = ['salt.json', 'userdata.json', 'chatfilter.txt', 'favorite.json']
    for file in file_list:
        if not os.path.isfile(file):
            print(f'load {file} file --- fail')
            error()
        else:
            print(f'load {file} file --- success')
    if not os.path.isdir('lang/'):
        print('load lang folder --- fail',end='\n\n')
        error()
    else:
        print('load lang folder --- success',end='\n\n')

def check_version(data, version):
    sha512= hashlib.sha512()
    sha512.update(data['version'].encode('utf-8'))
    res = sha512.hexdigest()
    if res != version:
        if data['debug-mode']:
            print('version error!','please use new version!', sep='\n',end='\n\n')
        error()
    else:
        if data['debug-mode']:
            print('version:', data['version'])