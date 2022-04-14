import json

config = {
    "language": "",
    "token": "",
    "command-prefix": ".",
    "custom-activity": "",
    "owner-id": "000000000000000000",
    "admin-id-1": "000000000000000000",
    "admin-id-2": "000000000000000000",
    "local-channel-id": "000000000000000000",
    "create-category-id": "000000000000000000",
    "picture-only-channel-id": "000000000000000000",

    "debug-mode": "false",

    "command-gay": "true",
    "command-time": "true",
    "command-exit": "true",
    "command-tlm": "true",
    "command-copy": "true",
    "command-reload": "true",
    "command-chlang": "true",
    "command-chact": "true",
    "command-clear": "true",
    "command-reset": "true"
}

def reset_config():
    reset = json.dumps(config, indent = 4)
    with open("config.json", "w") as outfile:
        outfile.write(reset)