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
    if found:
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

    if data['ticket-category-id'] == '':
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
    bool_list = [True, False]
    for i in [10, 11]:
        if data_list[i] not in bool_list:
            if data['debug-mode']:
                print('Error: In config setting:', data_list[i],'<-- only can be "true" or "false"')
            error()
    if data['custom-activity'] not in ['playing', 'streaming', 'listening', 'watching']:
        if data['debug-mode']:
            print('Error: In config setting:', data['custom-activity'],'<-- only can be "playing", "streaming", "listening" or "watching"')
        error()
    if data['custom-activity'] == 'streaming' and data['activity-streaming-url'] == '':
        if data['debug-mode']:
            print('Error: In config setting:', 'activity-streaming-url','<-- please enter a url')
        error()

def check_file():
    for dir in ['lang', 'lib', 'database', 'database/chatfilter']:
        if not os.path.isdir(dir+'/'):
            print(f'load {dir} folder --- fail')
            error()
        else:
            print(f'load {dir} folder --- success')
    print('')
    for file in ['lib/lang.py', 'lib/reset.py', 'lib/error_code.py', 'database/salt.json', 'database/userdata.json', 'database/serverdata.json', 'database/musicdata.json', 'database/favorite.json', 'database/chatfilter/DEFAULT.txt']:
        if not os.path.isfile(file):
            print(f'load {file} file --- fail')
            error()
        else:
            print(f'load {file} file --- success')
    print('')

def check_version(data, version):
    config_sha512= hashlib.sha512()
    config_sha512.update(data['version'].encode('utf-8'))
    config_res = config_sha512.hexdigest()
    try:
        response = requests.get("https://api.github.com/repos/ccchang123/Discord-Bot/releases/latest")
        api_sha512= hashlib.sha512()
        api_sha512.update(response.json()['tag_name'][1:6].encode('utf-8'))
        api_res = api_sha512.hexdigest()
    except:
        api_res = config_res
    if api_res != version or config_res != version:
        if data['debug-mode']:
            print('version error!','please use new version!','Now version: '+response.json()['tag_name'][1:6], sep='\n',end='\n\n')
        error()