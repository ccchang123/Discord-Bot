import discord, json, os, asyncio, youtube_dl
from datetime import datetime
from discord_slash import SlashCommand
from discord_components import *
import error_code, self_test, reset
from discord import *
""" check_config = os.path.isfile('config.json')
if check_config == False:
    print('load config file --- fail')
    self_test.error()
else:
    print('load config file --- ok')
    import lang
with open('config.json', "r", encoding = "utf8") as file:
    data = json.load(file)
def load_admin_bypass():
    global bypass_list, admin_list
    admin_list = []
    bypass_list = []
    with open('admin.json', "r", encoding = "utf8") as file:
        admin = json.load(file)
    admin_data_list = list(admin.items())
    
    for i in admin_data_list:
        if data['debug-mode'] == 'true':
           print('Add admin:', i[0]+', id: '+i[1])
        admin_list.append(int(i[1]))

    with open('bypass.json', "r", encoding = "utf8") as file:
        bypass = json.load(file)
    bypass_data_list = list(bypass.items())
    
    for j in bypass_data_list:
        if data['debug-mode'] == 'true':
            print('Bypass user:', j[0]+', id: '+j[1])
        bypass_list.append(int(j[1]))

def add_lang():
    global lang_list
    lang_list = []
    for k in os.listdir('lang'):
        if k.endswith(".json"):
            lang = k.split(".",2)
            lang_list.append(lang[0])
add_lang()
load_admin_bypass()
self_test.check(data, lang_list)

Lang = lang.lang_chose(data['language'], lang_list)
prefix = data['command-prefix']
intents = discord.Intents.all()
bot = ComponentsBot(data['command-prefix'])

@bot.command()
async def tick(ctx, category: int=000000000000000000):
    await ctx.message.delete()
    guild = ctx.guild
    Guild = discord.utils.get(guild.categories, id= category)
    if category == 000000000000000000:
        embed = discord.Embed(title=Lang['usage'], description=prefix+'tick '+Lang['category'], color=0xEC2E2E)
        await ctx.channel.send(embed=embed, delete_after=5)
    else:
        embed = discord.Embed(title='', color=0x79EF2F)
        embed.add_field(name='創立私人處理專案', value='點擊以下按鈕創建專案', inline=False)
        await ctx.channel.send(embed=embed)
        await ctx.send('', components = [
            Button(label='創立私人處理專案', style='3', custom_id='create_tick', emoji='📩')])
        while True:
            interaction = await bot.wait_for('button_click')
            res_create = interaction.custom_id
            if res_create == 'create_tick':
                await interaction.send(Lang['selected']+res_create)
                await tick_create(guild, Guild, interaction)
            else:
                pass

async def tick_create(guild, Guild, member):
    global tick_message
    tick_message = await guild.create_text_channel(str(member.author.name)+' 的專案', overwrites=None, category = Guild)
    await tick_message.set_permissions(member.author, send_messages=True, view_channel=True)
    await tick_message.set_permissions(guild.default_role, send_messages=False, view_channel=False)
    embed = discord.Embed(title='', color=0xEDFA28)
    embed.add_field(name='歡迎來到處理專案', value='管理員會盡快回覆你\n如要關閉專案請點擊以下按鈕', inline=False)
    await tick_message.send(f"<@{member.author.id}>", embed=embed)
    await tick_message.send('', components = [
        Button(label='關閉專案', style='4', custom_id='close_tick', emoji='🔒')]) """
with open('config.json', "r", encoding = "utf8") as file:
    data = json.load(file)

bot = ComponentsBot(data['command-prefix'])
slash = SlashCommand(bot, sync_commands=True)

def now_time():
    now = datetime.now()
    date_time = '<'+now.strftime("%Y-%m-%d, %H:%M:%S")+'>'
    return date_time

@bot.command()
async def time(ctx):
    if data['command-time'] == 'true':
        await ctx.reply(now_time(), mention_author=True)

@slash.slash(name='time', description='test')
async def time(ctx):
    if data['command-time'] == 'true':
        await ctx.send(now_time())

bot.run(data['token'])

"""
with open('favorite.json', "r", encoding = "utf8") as favorite_file:
    favorite_data = json.load(favorite_file)
data_keys = list(favorite_data.keys())
data_values = list(favorite_data.values())
favorite_dict = {}
data_values_dict = {}
for i in range(len(data_keys)):
    favorite_dict[data_keys[i]] = data_values[i]
if not favorite_data.__contains__(str(interaction.author.id)):
    data_values_dict = {str(now_playing_url): str(info['title'])}
                
else:
    data_values_dict = data_values[data_keys.index(str(interaction.author.id))]
    data_values_dict[str(now_playing_url)] = str(info['title'])
favorite_dict[str(interaction.author.id)] = data_values_dict

with open("favorite.json", "w") as favorite_file:
    json.dump(favorite_dict, favorite_file, indent = 4)


userdata_dict = {}
userdata_values_dict = {}
userdata_new_dict = {}
with open('userdata.json', "r", encoding = "utf8") as userdata_file:
    user_data = json.load(userdata_file)
#print(user_data)
userdata_keys = list(user_data.keys())
userdata_values = list(user_data.values())

#print(userdata_keys)
#print(list(userdata_values[userdata_keys.index('admin')].keys()))

for i in range(len(userdata_keys)):
    userdata_dict[userdata_keys[i]] = userdata_values[i]

userdata_values_dict = userdata_values[userdata_keys.index('admin')]

userdata_new_dict = userdata_values_dict['1234']
userdata_new_dict['name_2'] = 'hello'
userdata_dict['admin']['1234'] = userdata_new_dict

with open("userdata.json", "w") as userdata_file:
    json.dump(userdata_dict, userdata_file, indent = 4)

with open('userdata.json', "r", encoding = "utf8") as userdata_file:
    user_data = json.load(userdata_file)
userdata_keys = list(user_data.keys())
userdata_values = list(user_data.values())


del user_data['admin']['855360476430598164']['\u2764\u5f35\uff5c\u90b1#2040']

for i in range(len(userdata_keys)):
    userdata_dict[userdata_keys[i]] = userdata_values[i]
with open("userdata.json", "w") as userdata_file:
    json.dump(userdata_dict, userdata_file, indent = 4) """