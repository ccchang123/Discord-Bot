config = {
    "version": "2.6.0",
    "language": "",
    "token": "",
    "command-prefix": "",
    "custom-status": "online",
    "custom-activity": "",
    "owner-id": "000000000000000000",
    "local-channel-id": "000000000000000000",
    "create-category-id": "000000000000000000",
    "picture-only-channel-id": "000000000000000000",
    "ticket-category-id": "000000000000000000",
    "auto-mute": "",
    "auto-kick": "",
    "auto-ban": "",

    "chat-filter": "true",
    "chat-filter-action": "warn",

    "debug-mode": "false",

    "command-addadmin": "true",
    "command-addbypass": "true",
    "command-ban": "true",
    "command-clear": "true",
    "command-chlang": "true",
    "command-chact": "true",
    "command-copy": "true",
    "command-clearwarn": "true",
    "command-cd": "true",
    "command-ci": "true",
    "command-exit": "true",
    "command-gay": "true",
    "command-kick": "true",
    "command-mute": "true",
    "command-ping": "true",
    "command-reload": "true",
    "command-removeadmin": "true",
    "command-removebypass": "true",
	"command-showwarn": "true",
    "command-slowmode": "true",
    "command-send": "true",
    "command-time": "true",
    "command-tlm": "true",
    "command-tempban": "true",
    "command-tempmute": "true",
    "command-unban": "true",
    "command-unmute": "true",
    "command-uinfo": "true",
    "command-warn": "true",

    "command-reset": "true",

    "music-bot": "true"
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