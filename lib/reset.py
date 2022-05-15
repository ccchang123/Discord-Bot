config = {
    "version": "3.0.0",
    "language": "",
    "token": "",
    "command-prefix": "",
    "custom-status": "online",
    "custom-activity": "playing",
    "activity-name": "",
    "activity-streaming-url": "",
    "owner-id": 0,
    "ticket-category-id": 0,

    "debug-mode": False,

    "command-reset": True
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

serverdata = {
    "language": {

    },
    "picture-only-channel": {

    },
    "enter-voice-channel": {

    },
    "voice-category": {

    },
    "auto-action": {
    
    },
    "chat-filter-action": {
        
    },
    "music-bot": {
		
	},
	"commands": {
		
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
    with open("database/serverdata.json", "w") as server_file:
        json.dump(serverdata, server_file, indent = 4)
    with open("database/musicdata.json", "w") as music_file:
        json.dump(musicdata, music_file, indent = 4)