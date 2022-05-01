config = {
    "version": "2.6.2",
    "language": "",
    "token": "",
    "command-prefix": "",
    "custom-status": "online",
    "custom-activity": "",
    "owner-id": 000000000000000000,
    "local-channel-id": 000000000000000000,
    "create-category-id": 000000000000000000,
    "picture-only-channel-id": 000000000000000000,
    "ticket-category-id": 000000000000000000,
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


warns = {

}

userdata = {
    "admin": {

    },
    "bypass":  {

    }
}

import json

def reset_config():
    with open("config.json", "w") as config_file:
        json.dump(config, config_file, indent = 4)
    with open("warns.json", "w") as warns_file:
        json.dump(warns, warns_file, indent = 4)
    with open("userdata.json", "w") as bypass_file:
        json.dump(userdata, bypass_file, indent = 4)
    with open('chatfilter.txt', 'w') as chatfilter_file:
        chatfilter_file.write('')