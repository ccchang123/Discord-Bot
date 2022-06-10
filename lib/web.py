from flask import Flask, render_template
from threading import Thread
import json

app = Flask('', template_folder='database/templates', static_folder='database/templates')

@app.route('/')
def main():
    with open('database/serverdata.json', "r", encoding = "utf8") as file:
        server_data = json.load(file)
    data = json.dumps(server_data, sort_keys=True, indent=4, separators=(',', ':'))
    with open('database/musicdata.json', "r", encoding = "utf8") as file:
        music_data = json.load(file)
    music_data = json.dumps(music_data, sort_keys=True, indent=4, separators=(',', ':'))
    return render_template('index.html', data=data, music_data=music_data)

def run():
    app.run(host='0.0.0.0', port=5000)

def keep_alive():
    server = Thread(target=run)
    server.start()

#run()