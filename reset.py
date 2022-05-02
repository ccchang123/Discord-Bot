config = {
    "version": "2.6.3",
    "language": "",
    "token": "",
    "command-prefix": "",
    "custom-status": "online",
    "custom-activity": "",
    "owner-id": 0,
    "local-channel-id": 0,
    "create-category-id": 0,
    "picture-only-channel-id": 0,
    "ticket-category-id": 0,
    "auto-mute": "",
    "auto-kick": "",
    "auto-ban": "",

    "chat-filter": True,
    "chat-filter-action": "warn",

    "debug-mode": False,

    "commands":{
        "addadmin": True,
        "addbypass": True,
        "ban": True,
        "clear": True,
        "chlang": True,
        "chact": True,
        "copy": True,
        "clearwarn": True,
        "cd": True,
        "ci": True,
        "exit": True,
        "gay": True,
        "kick": True,
        "mute": True,
        "ping": True,
        "reload": True,
        "removeadmin": True,
        "removebypass": True,
        "showwarn": True,
        "slowmode": True,
        "send": True,
        "time": True,
        "tlm": True,
        "tempban": True,
        "tempmute": True,
        "unban": True,
        "unmute": True,
        "uinfo": True,
        "warn": True
    },
    "command-reset": True,

    "music-bot": True
}


salt = {

}

userdata = {
    "admin": {

    },
    "bypass":  {

    },
    "warns":  {

    }
}

import json

def reset_config():
    with open("config.json", "w") as config_file:
        json.dump(config, config_file, indent = 4)
    with open("salt.json", "w") as salt_file:
        json.dump(salt, salt_file, indent = 4)
    with open("userdata.json", "w") as bypass_file:
        json.dump(userdata, bypass_file, indent = 4)
    with open('chatfilter.txt', 'w') as chatfilter_file:
        chatfilter_file.write('')