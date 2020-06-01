import os
from pathlib import Path

from userge.utils import runcmd
from userge import userge, Message, Config
from userge.plugins.misc.upload import audio_upload


@userge.on_cmd("spotdl", about={
    'header': "Spotify Downloader",
    'description': "Download Songs via Spotify Links"
                   " or just by giving song names. ",
    'usage': "TODO lol, lemme how this plugin ends to be"})
async def spotify_dl(message: Message):
    await message.edit("Checking? 🧐😳🤔🤔")
    cmd = ''
    link = ''
    song_n = ''
    quality = "mp3"
    try:
        input, quality = message.input_str.split("|")
        if 'spotify.com' in input:
            await message.edit("Link, Hmm")
            link = input
        else:
            await message.edit("🤔Song?")
            song_n = input
    except ValueError:
        input = message.input_str
        if 'spotify.com' in input:
            await message.edit("Link, Hmm")
            link = input
        else:
            await message.edit("🤔Song?")
            song_n = input

    file_n = f"spotify_dl.{quality}"
    path = os.path.join(Config.DOWN_PATH, file_n)
    if song_n or link:
        if 'track/' in link:
            song_n = link
        if not song_n:
            return
        await message.edit("Downloading")
        quality = quality.strip()
        cmd = f"spotdl --song {song_n} -o {quality} -f {path}"
    if cmd:
        stdout, stderr = (await runcmd(cmd))[:2]
        if not os.path.lexists(path):
            await message.err("Download Failed")
            raise Exception(stdout + stderr)
        elif os.path.lexists:
            await message.delete()
            await audio_upload(message.chat.id, Path(path), True)
