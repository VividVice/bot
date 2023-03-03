import discord
from discord.ext import commands
import os
import ffmpeg
from mp3_downloader import *
import asyncio
import time
import nacl
from requests import get

intents = discord.Intents.all()
intents.members = True
intents.guilds = True
intents.messages = True
intents.reactions = True
intents.voice_states = True
intents.typing = True  # Enable the GUILD_MESSAGE_TYPING intent
bot = commands.Bot(command_prefix='!', intents=intents)

voice_client = None
playing = False
source = None
queue = []
name = ""

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')


def get_mp3_filenames():
    filenames = []
    for file in os.listdir('music'):
        if file.endswith('.mp3'):
            filenames.append(os.path.splitext(file)[0])

    # Sort filenames by modification time (newest to oldest)
    filenames = sorted(filenames, key=lambda f: os.path.getmtime(f"music/{f}.mp3"), reverse=True)

    return filenames


@bot.command()
async def play(ctx, url=None):
    global playing
    global source
    global voice_client
    global queue
    global name

    print("it was called")
    if url:
        prepLink(url)
        name = get_name_from_link(url)
        time.sleep(2)
    else:
        await ctx.send("You need a link")
        return

    filenames = get_mp3_filenames()
    filename = filenames[0]
    voice_channel = ctx.author.voice.channel

    if voice_channel:
        if voice_client and voice_client.channel == voice_channel:
            voice = voice_client
        else:
            voice = await voice_channel.connect()
            voice_client = voice
        if voice.is_playing():
            queue.append(filename)
            print(queue)
            await ctx.send(f"Added {name} to the queue")
            return
        else:
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(f"music/{filename}.mp3"))
            voice.play(source=source)
            playing = True
            await ctx.send(f"Now playing {name}")
        while voice.is_playing() or voice.is_paused():
            await asyncio.sleep(1)
        playing = False
        if playing == False:
            delete_file = str(filename) + ".mp3"
            voice.stop()
            voice.cleanup()
            if delete_file in os.listdir('music'):
                os.remove(f"music/{filename}.mp3")
            else:
                pass
            await play_next(ctx, voice_client)
    else:
        await ctx.send("You need to be in a voice channel to use this command!")

# , after=lambda e: play_next(ctx, voice_client) if e else None

async def play_next(ctx, voice_client):
    global playing
    global queue
    global name
    print("playing next")
    if len(queue) >= 1:
        file = queue[0]
        filename = file
        queue.pop(0)
        await ctx.send(f"Now playing {name}")
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(f"music/{filename}.mp3"))
        voice_client.play(source)
        playing = True
        while voice_client.is_playing() or voice_client.is_paused():
            await asyncio.sleep(1)
        playing = False
        if playing == False:
            delete_file = str(filename) + ".mp3"
            voice_client.stop()
            voice_client.cleanup()
            if delete_file in os.listdir('music'):
                os.remove(f"music/{filename}.mp3")
            else:
                pass

@bot.command()
async def stop(ctx):
    global voice_client
    global queue
    global counter
    if voice_client:
        voice_client.stop()
        voice_client.cleanup()
        await ctx.send("Stopped playing")
        queue = []
        counter = 1
        time.sleep(1)
        for file in os.listdir('music'):
            if file.endswith('.mp3'):
                os.remove(f"music/{file}")
        return

@bot.command()
async def pause(ctx):
    global voice_client
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        await ctx.send("Paused playback")
    else:
        await ctx.send("Not currently playing a song")

@bot.command()
async def skip(ctx):
    global voice_client
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await ctx.send("skipped playing song")
    else:
        await ctx.send("Not currently playing a song")

@bot.command()
async def resume(ctx):
    global voice_client
    if voice_client and voice_client.is_paused():
        voice_client.resume()
        await ctx.send("Resumed playback.")
    else:
        await ctx.send("Not currently paused.")

bot.run('TOKEN HERE')
