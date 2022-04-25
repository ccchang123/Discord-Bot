import os

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

    if data['local-channel-id'] == '' or data['create-category-id'] == '' or data['picture-only-channel-id'] == '':
        if data['debug-mode'] == 'true':
           print('load channel-id setting --- fail',end='\n\n')
        error()
    else:
        if data['debug-mode'] == 'true':
            print('load channel-id setting --- ok',end='\n\n')

def check_file():
    if not os.path.isfile('warns.json'):
        print('load warns file --- fail')
        error()
    else:
        print('load warns file --- ok')

    if not os.path.isfile('admin.json'):
        print('load admin file --- fail')
        error()
    else:
        print('load admin file --- ok')

    if not os.path.isfile('bypass.json'):
        print('load bypass file --- fail')
        error()
    else:
        print('load bypass file --- ok')
    
    if not os.path.isfile('chatfilter.txt'):
        print('load chatfilter file --- fail')
        error()
    else:
        print('load chatfilter file --- ok')

    if not os.path.isdir('lang/'):
        print('load lang folder --- fail',end='\n\n')
        error()
    else:
        print('load lang folder --- ok',end='\n\n')
