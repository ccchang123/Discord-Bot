import json

config = {
    "language": "",
    "token": "",
    "command-prefix": "",
    "custom-status": "online",
    "custom-activity": "",
    "owner-id": "000000000000000000",
    "local-channel-id": "000000000000000000",
    "create-category-id": "000000000000000000",
    "picture-only-channel-id": "000000000000000000",

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
    "command-reload": "true",
    "command-removeadmin": "true",
    "command-removebypass": "true",
	"command-showwarn": "true",
    "command-slowmode": "true",
    "command-time": "true",
    "command-tlm": "true",
    "command-unban": "true",
    "command-unmute": "true",
    "command-uinfo": "true",
    "command-warn": "true",

    "command-reset": "true",

    "music-bot": "true"
}

warns = {

}

bypass = {
    "It is a example_1": "000000000000000000",
    "It is a example_2": "000000000000000000"
}

admin = {
    "It is a example_1": "000000000000000000",
    "It is a example_2": "000000000000000000"
}

def reset_config():
    with open("config.json", "w") as config_file:
        json.dump(config, config_file, indent = 4)
    with open("warns.json", "w") as warns_file:
        json.dump(warns, warns_file, indent = 4)
    with open("bypass.json", "w") as bypass_file:
        json.dump(bypass, bypass_file, indent = 4)
    with open("admin.json", "w") as admin_file:
        json.dump(admin, admin_file, indent = 4)