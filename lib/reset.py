config = {
    "version": "2.7.0",
    "language": "",
    "token": "",
    "command-prefix": "",
    "custom-status": "online",
    "custom-activity": "",
    "owner-id": 0,
    "enter-private-voice-channel-id": 0,
    "private-voice-category-id": 0,
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

musicdata = {
    "url": {

    },
    "title":  {

    },
    "repeat":  {

    },
    "button_switch": {

    }
}

import json

def reset_config():
    with open("config.json", "w") as config_file:
        json.dump(config, config_file, indent = 4)
    with open("database/salt.json", "w") as salt_file:
        json.dump(salt, salt_file, indent = 4)
    with open("database/userdata.json", "w") as user_file:
        json.dump(userdata, user_file, indent = 4)
    with open("database/musicdata.json", "w") as music_file:
        json.dump(musicdata, music_file, indent = 4)
    with open('database/chatfilter.txt', 'w') as chatfilter_file:
        chatfilter_file.write('')