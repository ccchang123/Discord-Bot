import json

config = {
    "language": "",
    "token": "",
    "command-prefix": "",
    "custom-activity": "",
    "owner-id": "000000000000000000",
    "admin-id-1": "000000000000000000",
    "admin-id-2": "000000000000000000",
    "local-channel-id": "000000000000000000",
    "create-category-id": "000000000000000000",
    "picture-only-channel-id": "000000000000000000",

    "debug-mode": "false",

    "command-ban": "true",
    "command-clear": "true",
    "command-chlang": "true",
    "command-chact": "true",
    "command-copy": "true",
    "command-clearwarn": "true",
    "command-exit": "true",
    "command-gay": "true",
    "command-kick": "true",
    "command-reload": "true",
    "command-showwarn": "true",
    "command-reset": "true",
    "command-time": "true",
    "command-tlm": "true",
    "command-unban": "true",
    "command-warn": "true"
}

warns = {

}

def reset_config():
    reset_config = json.dumps(config, indent = 4)
    reset_warns = json.dumps(warns, indent = 4)
    with open("config.json", "w") as config_file:
        config_file.write(reset_config)
    with open("warns.json", "w") as warns_file:
        warns_file.write(reset_warns)