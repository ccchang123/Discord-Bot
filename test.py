#from discord.commands import slash_command
#@bot.slash_command(name='123', description='test', guild_ids=[961759312882044990])
import asyncio, youtube_dl, discord, time, random, os, mechanize
from itertools import cycle
from copy import deepcopy
from urllib.parse import urlparse
from youtubesearchpython import VideosSearch
import feedparser
from discord.ext import commands, tasks
from discord_components import *
from discord import opus

bot = discord.Client()

global musik_stopped
global musik_count
global player
global player_repeat
gPlaylist = []
musik_stopped = False
musik_count = 0
player = ""
player_repeat = True
reported_message = ""

async def playit():
    global gPlaylist
    global musik_stopped
    global musik_count
    global player
    global player_repeat
    try:
        if not player_repeat:
            gPlaylist.pop(0)
        print(gPlaylist)
        player.stop()
        await asyncio.sleep(1)
        sourcex = gPlaylist[0]
        br = mechanize.Browser()
        try:
            br.open(sourcex)
        except:
            pass
        try:
            title = br.title()
        except:
            a = urlparse(sourcex)
            title = os.path.basename(a.path)
        try:
            ydl_opts = {"format": "bestaudio"}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(gPlaylist[0], download=False)
                URL = info["formats"][0]["url"]
        except:
            URL = gPlaylist[0]
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(URL, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), 1)
        bot.voice_clients[0].play(source, after=myafter)
        embed = discord.Embed(title="Jetzt spielt:", description=f"[{title}]({sourcex})", color=3566847)
        if not player_repeat:
            player_message = await bot.get_channel(829007032895668267).send(embed=embed)
            await player_message.add_reaction("⏏️")
            await player_message.add_reaction("⏹️")
            await player_message.add_reaction("⏯️")
            await player_message.add_reaction("⏭️")
            await player_message.add_reaction("🔁")
    except:
        if not musik_stopped:
            if musik_count > 1:
               embed = discord.Embed(title="Playlist beendet!", color=3566847)
               await bot.get_channel(829007032895668267).send(embed=embed)
        else:
            await asyncio.sleep(6)
            musik_stopped = False
        

def myafter(error):
    print(f"M-Error: {error}")
    fut = asyncio.run_coroutine_threadsafe(playit(), bot.loop)
    fut.result()


@bot.event
async def on_ready():
    print(bot.user)
    #online,offline,idle,dnd,invisible
    game = discord.Game('test')
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.event
async def on_message(message):
    global gPlaylist
    global musik_stopped
    global musik_count
    global player
    global player_repeat
    if message.author == bot.user:
        return
    if message.author.bot:
        return

    if message.content.startswith("!musik"):
            await message.channel.trigger_typing()
            await asyncio.sleep(0.05)
            embed = discord.Embed(title="Musik - Commands", color=3566847)
            embed.add_field(name="!play URL", value="Spiele den Song bei der URL", inline=False)
            embed.add_field(name="!playlist", value="Listet die Playlist", inline=False)
            embed.add_field(name="!playlist add URL", value="Fügt die URL der Playlist hinzu", inline=False)
            embed.add_field(name="!playlist add URL1, URL2", value="Fügt die URLs der Playlist hinzu", inline=False)
            embed.add_field(name="!playlist remove URL", value="Löscht die URL aus der Playlist", inline=False)
            embed.add_field(name="!playlist clear", value="Leert die Playlist", inline=False)
            embed.add_field(name="!play playlist", value="Spielt die Playlist ab", inline=False)
            embed.add_field(name="!join", value="Bot joint deinem Voice-Channel", inline=False)
            embed.add_field(name="!leave", value="Bot verlässt seinen Voice-Channel", inline=False)
            embed.add_field(name="!pause", value="Pausiert den Song", inline=False)
            embed.add_field(name="!resume", value="Setzt den Song fort", inline=False)
            embed.add_field(name="!stop", value="Stoppt alle Songs und leert die Playlist", inline=False)
            embed.add_field(name="!skip", value="Überspringt den Song", inline=False)
            embed.add_field(name="!repeat", value="Wiederholt den Song in Dauerschleife", inline=False)
            embed.add_field(name="!reactions", value="Erklärt die Reactions", inline=False)
            await message.channel.send(embed=embed)

    if message.content.startswith("!reactions"):
            await message.channel.trigger_typing()
            await asyncio.sleep(0.05)
            embed = discord.Embed(title="Musik - Reactions", color=3566847)
            embed.add_field(name=":play_pause:", value="Pausiert den Song oder setzt ihn fort", inline=False)
            embed.add_field(name=":track_next:", value="Überspringt den Song", inline=False)
            embed.add_field(name=":stop_button:", value="Stoppt alle Songs und leert die Playlist", inline=False)
            embed.add_field(name=":eject:", value="Bot verlässt seinen Voice-Channel", inline=False)
            embed.add_field(name=":arrow_forward:", value="Spielt die Playlist ab", inline=False)
            embed.add_field(name=":repeat:", value="Wiederholt den Song in Dauerschleife", inline=False)
            embed.add_field(name=":recycle:", value="Leert die Playlist", inline=False)
            await message.channel.send(embed=embed)

    if message.content.startswith("!join"):
        if message.channel.id == 829007032895668267:
            try:
                channel = message.author.voice.channel
            except:
                embed = discord.Embed(title="Du bist in keinem Voice-Channel!", color=16711680)
                await message.channel.send(embed=embed)
                return
            voice = discord.utils.get(client.voice_clients, guild=message.guild)
            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()
            embed = discord.Embed(title=f"Channel {channel} beigetreten!")
            await message.channel.send(embed=embed)

    if message.content.startswith("!leave"):
        if message.channel.id == 829007032895668267:
            musik_stopped = True
            gPlaylist.clear()
            voice = discord.utils.get(client.voice_clients, guild=message.guild)
            if voice and voice.is_connected():
                await voice.disconnect()
                embed = discord.Embed(title=f"Channel {voice.channel.name} verlassen!")
                await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(title="Ich bin in keinem Voice-Channel!", color=16711680)
                await message.channel.send(embed=embed)

    if message.content.startswith("!play") and not message.content.startswith("!playlist") and not message.content == "!play playlist":
            #player_repeat = False
            musik_count = 1
            gPlaylist.clear()
            source = message.content.replace("!play ", "")
            br = mechanize.Browser()
            try:
                br.open(source)
            except:
                videossearch = VideosSearch(source, limit=5)
                result = videossearch.result()
                desc = ""
                count = 0
                p_list = []
                for res in result["result"]:
                    p_list.append(res["link"])
                    count += 1
                    desc = desc + f"{count}. [{res['title']}]({res['link']})\n"
                embed = discord.Embed(title="Auf YouTube suchen:", description=desc)
                x = await message.channel.send(embed=embed)
                await x.add_reaction("1️⃣")
                await x.add_reaction("2️⃣")
                await x.add_reaction("3️⃣")
                await x.add_reaction("4️⃣")
                await x.add_reaction("5️⃣")
                def checkmsg(m):
                    return m.channel == message.channel
                def checkreaction(reaction, user):
                    return reaction.message.channel == message.channel and not user.id == 825377881546686474
                pending_tasks = [bot.wait_for("reaction_add", check=checkreaction),
                                 bot.wait_for("message", check=checkmsg)]
                done_tasks, pending_tasks = await asyncio.wait(pending_tasks, return_when=asyncio.FIRST_COMPLETED)
                try:
                    for task in done_tasks:
                        reaction, user = await task
                except:
                    for task in done_tasks:
                        msg2 = await task
                try:
                    if msg2.content == "1":
                        source = p_list[0]
                    elif msg2.content == "2":
                        source = p_list[1]
                    elif msg2.content == "3":
                        source = p_list[2]
                    elif msg2.content == "4":
                        source = p_list[3]
                    elif msg2.content == "5":
                        source = p_list[4]
                    else:
                        await x.delete()
                        return
                except:
                    if reaction.emoji == "1️⃣":
                        source = p_list[0]
                    elif reaction.emoji == "2️⃣":
                        source = p_list[1]
                    elif reaction.emoji == "3️⃣":
                        source = p_list[2]
                    elif reaction.emoji == "4️⃣":
                        source = p_list[3]
                    elif reaction.emoji == "5️⃣":
                        source = p_list[4]
                    else:
                        await x.delete()
                        return
                br.open(source)
            try:
                title = br.title()
                if title == "- YouTube":
                    embed = discord.Embed(title="YouTube Video nicht gefunden!", color=16711680)
                    await message.channel.send(embed=embed)
                    return
            except:
                a = urlparse(source)
                title = os.path.basename(a.path)
            try:
                channel = message.author.voice.channel
            except:
                embed = discord.Embed(title="Du bist in keinem Voice-Channel!", color=16711680)
                await message.channel.send(embed=embed)
                return
            try:
                ydl_opts = {"format": "bestaudio"}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(source, download=False)
                    URL = info["formats"][0]["url"]
            except:
                URL = source
            gPlaylist.append(source)
            player = discord.utils.get(bot.voice_clients, guild=message.guild)
            if player and player.is_connected():
                await player.move_to(channel)
            else:
                player = await channel.connect()
            try:
                pplayer = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(URL, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), 1)
                
                player.play(pplayer, after=myafter)
            except:
                player.stop()
                pplayer = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(URL, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), 1)
                
                player.play(pplayer, after=myafter)
            embed = discord.Embed(title="Jetzt spielt:", description=f"[{title}]({source})")
            player_message = await message.channel.send(embed=embed)
            await player_message.add_reaction("⏏️")
            await player_message.add_reaction("⏹️")
            await player_message.add_reaction("⏯️")
            await player_message.add_reaction("⏭️")
            await player_message.add_reaction("🔁")

    if message.content.startswith("!pause"):
            try:
                player.pause()
            except:
                embed = discord.Embed(title="Derzeit läuft nichts!", color=16711680)
                await message.channel.send(embed=embed)
                return
            embed = discord.Embed(title=f"Pausiert!")
            await message.channel.send(embed=embed)

    if message.content.startswith("!resume"):
            try:
                player.resume()
            except:
                embed = discord.Embed(title="Derzeit läuft nichts!", color=16711680)
                await message.channel.send(embed=embed)
                return
            embed = discord.Embed(title=f"Fortgesetzt!")
            await message.channel.send(embed=embed)

    if message.content.startswith("!repeat"):
            if player_repeat:
                player_repeat = False
                embed = discord.Embed(title="Wiederholung nicht mehr aktiv!")
                await message.channel.send(embed=embed)
            else:
                player_repeat = True
                embed = discord.Embed(title="Wiederholung aktiv!")
                await message.channel.send(embed=embed)

    if message.content.startswith("!stop"):
            musik_stopped = True
            gPlaylist.clear()
            try:
                player.stop()
            except:
                embed = discord.Embed(title="Derzeit läuft nichts!", color=16711680)
                await message.channel.send(embed=embed)
                return
            embed = discord.Embed(title=f"Beendet!")
            await message.channel.send(embed=embed)

    if message.content == "!play playlist" or message.content == "!playlist play":
            if not gPlaylist == []:
                player_repeat = False
                await message.channel.trigger_typing()
                musik_count = 2
                try:
                    channel = message.author.voice.channel
                except:
                    embed = discord.Embed(title="Du bist in keinem Voice-Channel!", color=16711680)
                    await message.channel.send(embed=embed)
                    return
                player = discord.utils.get(client.voice_clients, guild=message.guild)
                if player and player.is_connected():
                    await player.move_to(channel)
                else:
                    player = await channel.connect()
                player.stop()
                await asyncio.sleep(1)
                sourcex = gPlaylist[0]
                br = mechanize.Browser()
                try:
                    br.open(sourcex)
                except:
                    pass
                try:
                    title = br.title()
                except:
                    a = urlparse(sourcex)
                    title = os.path.basename(a.path)
                try:
                    ydl_opts = {"format": "bestaudio"}
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(sourcex, download=False)
                        URL = info["formats"][0]["url"]
                except:
                    URL = gPlaylist[0]
                try:
                    pplayer = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(URL, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), 1)
                    player.play(pplayer, after=myafter)
                except:
                    player.stop()
                    pplayer = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(URL, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), 1)
                    player.play(pplayer, after=myafter)
                embed = discord.Embed(title=f"Jetzt spielt:", description=f"[{title}]({sourcex})")
                player_message = await message.channel.send(embed=embed)
                await player_message.add_reaction("⏏️")
                await player_message.add_reaction("⏹️")
                await player_message.add_reaction("⏯️")
                await player_message.add_reaction("⏭️")
                await player_message.add_reaction("🔁")
            else:
                embed = discord.Embed(title="Die Playlist ist leer!", color=16711680)
                await message.channel.send(embed=embed)
                return

    if message.content.startswith("!playlist add"):
            source = message.content.replace("!playlist add ", "")
            sl = source.split()
            if sl[0] == "random":
                source = source.replace("random ", "")
                setrandom = True
            sourcel = source.split(",")
            try:
                setrandom = setrandom
            except:
                setrandom = False
            if source.startswith("https://www.youtube.com/playlist?"):
                playlist_id = source.replace("https://www.youtube.com/playlist?list=", "")
                feed = feedparser.parse(f"https://www.youtube.com/feeds/videos.xml?playlist_id={playlist_id}")
                entries = feed.entries
                if setrandom:
                    random.shuffle(entries)
                hinzu = ""
                c = 0
                for entry in entries:
                    c += 1
                    if c % 2 == 0:
                        await message.channel.trigger_typing()
                    await asyncio.sleep(0.1)
                    i = entry["link"]
                    musik_count += 1
                    i = i.lstrip()
                    br = mechanize.Browser()
                    try:
                        br.open(i)
                    except:
                        pass
                    try:
                        title = br.title()
                        if title == "- YouTube":
                            embed = discord.Embed(title="YouTube Video nicht gefunden!", color=16711680)
                            await message.channel.send(embed=embed)
                            return
                    except:
                        a = urlparse(source)
                        title = os.path.basename(a.path)
                    gPlaylist.append(i)
                    hinzu = f"{hinzu}- [{title}]({i})\n"
                if setrandom:
                    embed = discord.Embed(title="Zur Playlist hinzugefügt: (random)", description=hinzu)
                else:
                    embed = discord.Embed(title="Zur Playlist hinzugefügt:", description=hinzu)
                m = await message.channel.send(embed=embed)
                await m.add_reaction("▶️")
                return
            if len(sourcel) > 1:
                hinzu = ""
                if setrandom:
                    random.shuffle(sourcel)
                for i in sourcel:
                    musik_count += 1
                    i = i.lstrip()
                    br = mechanize.Browser()
                    try:
                        br.open(i)
                    except:
                        videossearch = VideosSearch(i, limit=5)
                        result = videossearch.result()
                        desc = ""
                        count = 0
                        p_list = []
                        for res in result["result"]:
                            p_list.append(res["link"])
                            count += 1
                            desc = desc + f"{count}. [{res['title']}]({res['link']})\n"
                        embed = discord.Embed(title="Auf YouTube suchen:", description=desc)
                        x = await message.channel.send(embed=embed)
                        await x.add_reaction("1️⃣")
                        await x.add_reaction("2️⃣")
                        await x.add_reaction("3️⃣")
                        await x.add_reaction("4️⃣")
                        await x.add_reaction("5️⃣")
                        def checkmsg(m):
                            return m.channel == message.channel
                        def checkreaction(reaction, user):
                            return reaction.message.channel == message.channel and not user.id == 825377881546686474
                        pending_tasks = [client.wait_for("reaction_add", check=checkreaction),
                                         client.wait_for("message", check=checkmsg)]
                        done_tasks, pending_tasks = await asyncio.wait(pending_tasks, return_when=asyncio.FIRST_COMPLETED)
                        try:
                            for task in done_tasks:
                                reaction, user = await task
                        except:
                            for task in done_tasks:
                                msg2 = await task
                        try:
                            if msg2.content == "1":
                                i = p_list[0]
                            elif msg2.content == "2":
                                i = p_list[1]
                            elif msg2.content == "3":
                                i = p_list[2]
                            elif msg2.content == "4":
                                i = p_list[3]
                            elif msg2.content == "5":
                                i = p_list[4]
                            else:
                                await x.delete()
                                return
                        except:
                            if reaction.emoji == "1️⃣":
                                i = p_list[0]
                            elif reaction.emoji == "2️⃣":
                                i = p_list[1]
                            elif reaction.emoji == "3️⃣":
                                i = p_list[2]
                            elif reaction.emoji == "4️⃣":
                                i = p_list[3]
                            elif reaction.emoji == "5️⃣":
                                i = p_list[4]
                            else:
                                await x.delete()
                                return
                        br.open(i)
                    try:
                        title = br.title()
                        if title == "- YouTube":
                            embed = discord.Embed(title="YouTube Video nicht gefunden!", color=16711680)
                            await message.channel.send(embed=embed)
                            return
                    except:
                        a = urlparse(source)
                        title = os.path.basename(a.path)
                    gPlaylist.append(i)
                    hinzu = f"{hinzu}- [{title}]({i})\n"
                if setrandom:
                    embed = discord.Embed(title="Zur Playlist hinzugefügt: (random)", description=hinzu)
                else:
                    embed = discord.Embed(title="Zur Playlist hinzugefügt:", description=hinzu)
                player_message = await message.channel.send(embed=embed)
                await player_message.add_reaction("▶️")
                return
            musik_count += 1
            br = mechanize.Browser()
            try:
                br.open(source)
            except:
                videossearch = VideosSearch(source, limit=5)
                result = videossearch.result()
                desc = ""
                count = 0
                p_list = []
                for res in result["result"]:
                    p_list.append(res["link"])
                    count += 1
                    desc = desc + f"{count}. [{res['title']}]({res['link']})\n"
                embed = discord.Embed(title="Auf YouTube suchen:", description=desc)
                x = await message.channel.send(embed=embed)
                await x.add_reaction("1️⃣")
                await x.add_reaction("2️⃣")
                await x.add_reaction("3️⃣")
                await x.add_reaction("4️⃣")
                await x.add_reaction("5️⃣")
                def checkmsg(m):
                    return m.channel == message.channel
                def checkreaction(reaction, user):
                    return reaction.message.channel == message.channel and not user.id == 825377881546686474
                pending_tasks = [client.wait_for("reaction_add", check=checkreaction),
                                 client.wait_for("message", check=checkmsg)]
                done_tasks, pending_tasks = await asyncio.wait(pending_tasks, return_when=asyncio.FIRST_COMPLETED)
                try:
                    for task in done_tasks:
                        reaction, user = await task
                except:
                    for task in done_tasks:
                        msg2 = await task
                try:
                    if msg2.content == "1":
                        source = p_list[0]
                    elif msg2.content == "2":
                        source = p_list[1]
                    elif msg2.content == "3":
                        source = p_list[2]
                    elif msg2.content == "4":
                        source = p_list[3]
                    elif msg2.content == "5":
                        source = p_list[4]
                    else:
                        await x.delete()
                        return
                except:
                    if reaction.emoji == "1️⃣":
                        source = p_list[0]
                    elif reaction.emoji == "2️⃣":
                        source = p_list[1]
                    elif reaction.emoji == "3️⃣":
                        source = p_list[2]
                    elif reaction.emoji == "4️⃣":
                        source = p_list[3]
                    elif reaction.emoji == "5️⃣":
                        source = p_list[4]
                    else:
                        await x.delete()
                        return
            try:
                title = br.title()
                if title == "- YouTube":
                    embed = discord.Embed(title="YouTube Video nicht gefunden!", color=16711680)
                    await message.channel.send(embed=embed)
                    return
            except:
                a = urlparse(source)
                title = os.path.basename(a.path)
            gPlaylist.append(source)
            embed = discord.Embed(title=f"Zur Playlist hinzugefügt:!", description=f"[{title}]({source})", color=3566847)
            player_message = await message.channel.send(embed=embed)
            await player_message.add_reaction("▶️")

    if message.content.startswith("!playlist remove"):
            source = message.content.replace("!playlist remove ", "")
            br = mechanize.Browser()
            try:
                br.open(source)
            except:
                embed = discord.Embed(title="Keine gültige mp3-Datei gefunden!", color=16711680)
                await message.channel.send(embed=embed)
                return
            try:
                title = br.title()
                if title == "- YouTube":
                    embed = discord.Embed(title="YouTube Video nicht gefunden!", color=16711680)
                    await message.channel.send(embed=embed)
                    return
            except:
                a = urlparse(source)
                title = os.path.basename(a.path)
            try:
                gPlaylist.remove(source)
                musik_count -= 1
                embed = discord.Embed(title=f"Aus der Playlist entfernt:!", description=f"[{title}]({source})", color=3566847)
                await message.channel.send(embed=embed)
            except:
                embed = discord.Embed(title="Nicht in der Playlist gefunden!", color=16711680)
                await message.channel.send(embed=embed)
                return
            return

    if message.content.startswith("!random") or message.content.startswith("!playlist random"):
            random.shuffle(gPlaylist)
            embed = discord.Embed(title="Gemischt!", color=3566847)
            await message.channel.send(embed=embed)

    if message.content.startswith("!playlist clear"):
            gPlaylist.clear()
            embed = discord.Embed(title=f"Playlist geleert!", color=3566847)
            await message.channel.send(embed=embed)

    if message.content == "!playlist":
            desc = ""
            if gPlaylist == []:
                embed = discord.Embed(title="Die Playlist ist leer!", color=3566847)
                await message.channel.send(embed=embed)
                return
            count = 0
            for i in gPlaylist:
                count += 1
                desc = f"{desc}{count}. {i}\n"
            embed = discord.Embed(title="Playlist:", description=desc, color=3566847)
            player_message = await message.channel.send(embed=embed)
            await player_message.add_reaction("▶️")
            await player_message.add_reaction("♻️")

    if message.content.startswith("!skip"):
            try:
                player.stop()
            except:
                embed = discord.Embed(title="Derzeit läuft nichts!", color=16711680)
                await message.channel.send(embed=embed)
                return
            embed = discord.Embed(title=f"Übersprungen!")
            await message.channel.send(embed=embed)

@bot.event
async def on_reaction_add(reaction, user):
    global player
    global musik_stopped
    global gPlaylist
    global player_repeat
    if not user.id == 825377881546686474:
        if reaction.message.author.id == 413271975775961099:
            if reaction.emoji == "⏯️":
                embed_title = reaction.message.embeds[0].title
                if embed_title == "Jetzt spielt:":
                    if player.is_playing():
                        player.pause()
                    elif player.is_paused():
                        player.resume()
                    await reaction.message.remove_reaction("⏯️", user)
            if reaction.emoji == "⏭️":
                embed_title = reaction.message.embeds[0].title
                if embed_title == "Jetzt spielt:":
                    try:
                        player.stop()
                    except:
                        pass
                    await reaction.message.remove_reaction("⏭️", user)
            if reaction.emoji == "⏹️":
                embed_title = reaction.message.embeds[0].title
                if embed_title == "Jetzt spielt:":
                    musik_stopped = True
                    gPlaylist.clear()
                    try:
                        player.stop()
                    except:
                        pass
                    await reaction.message.remove_reaction("⏹️", user)
            if reaction.emoji == "⏏️":
                embed_title = reaction.message.embeds[0].title
                if embed_title == "Jetzt spielt:":
                    musik_stopped = True
                    gPlaylist.clear()
                    voice = discord.utils.get(bot.voice_clients, guild=reaction.message.guild)
                    if voice and voice.is_connected():
                        await voice.disconnect()
                    await reaction.message.remove_reaction("⏏️", user)
            if reaction.emoji == "▶️":
                embed_title = reaction.message.embeds[0].title
                if embed_title == "Zur Playlist hinzugefügt:" or embed_title == "Playlist:":
                    if not gPlaylist == []:
                        player_repeat = False
                        await reaction.message.channel.trigger_typing()
                        musik_count = 2
                        try:
                            channel = user.voice.channel
                        except:
                            embed = discord.Embed(title="Du bist in keinem Voice-Channel!", color=16711680)
                            await reaction.message.channel.send(embed=embed)
                            await reaction.message.remove_reaction("▶️", user)
                            return
                        player = discord.utils.get(bot.voice_clients, guild=reaction.message.guild)
                        if player and player.is_connected():
                            await player.move_to(channel)
                        else:
                            player = await channel.connect()
                        player.stop()
                        await asyncio.sleep(1)
                        sourcex = gPlaylist[0]
                        br = mechanize.Browser()
                        try:
                            br.open(sourcex)
                        except:
                            pass
                        try:
                            title = br.title()
                        except:
                            a = urlparse(sourcex)
                            title = os.path.basename(a.path)
                        try:
                            ydl_opts = {"format": "bestaudio"}
                            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                                info = ydl.extract_info(sourcex, download=False)
                                URL = info["formats"][0]["url"]
                        except:
                            URL = gPlaylist[0]
                        try:
                            pplayer = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(URL, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), 1)
                            player.play(pplayer, after=myafter)
                        except:
                            player.stop()
                            pplayer = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(URL, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), 1)
                            player.play(pplayer, after=myafter)
                        embed = discord.Embed(title=f"Jetzt spielt:", description=f"[{title}]({sourcex})")
                        player_message = await reaction.message.channel.send(embed=embed)
                        await player_message.add_reaction("⏏️")
                        await player_message.add_reaction("⏹️")
                        await player_message.add_reaction("⏯️")
                        await player_message.add_reaction("⏭️")
                        await player_message.add_reaction("🔁")
                    await reaction.message.remove_reaction("▶️", user)
                    await reaction.message.remove_reaction("▶️", bot.user)
            if reaction.emoji == "♻️":
                embed_title = reaction.message.embeds[0].title
                if embed_title == "Playlist:":
                    if not gPlaylist == []:
                        gPlaylist.clear()
                        embed = discord.Embed(title="Playlist geleert!")
                        await reaction.message.channel.send(embed=embed)
                    await reaction.message.remove_reaction("♻️", user)
            if reaction.emoji == "🔁":
                embed_title = reaction.message.embeds[0].title
                if embed_title == "Jetzt spielt:":
                    if player_repeat:
                        player_repeat = False
                        embed = discord.Embed(title="Wiederholung nicht mehr aktiv!")
                        await reaction.message.channel.send(embed=embed)
                    else:
                        player_repeat = True
                        embed = discord.Embed(title="Wiederholung aktiv!")
                        await reaction.message.channel.send(embed=embed)
                    await reaction.message.remove_reaction("🔁", user)

bot.run("Njk4ODExNzg4MzAwNTE3Mzc2.XpLRMQ.xnR2IZPZqs9_H9kVLffOOrST-qo")