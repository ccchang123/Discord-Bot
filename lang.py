import json

with open('config.json', "r", encoding = "utf8") as file:
    data = json.load(file)

def lang_chose(sele):
    if sele == 'zh-tw':
        with open('lang/zh-tw.json', "r", encoding = "utf8") as lang_file:
            language = json.load(lang_file)
    elif sele == 'en-us':
        with open('lang/en-us.json', "r", encoding = "utf8") as lang_file:
            language = json.load(lang_file)
    return language