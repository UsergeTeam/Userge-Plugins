import os
import shutil
from pathlib import Path

from userge import userge, Message
from userge.plugins.misc.upload import audio_upload
from userge.plugins.tools.executor import Term

TEMP_DIR = "spotdl/"


@userge.on_cmd("spotdl", about={
    'header': "Spotify Downloader",
    'description': "Download Songs via Spotify Links"
                   " or just by giving song names. ",
    'usage': "{tr}spotdl [Spotify Link or Song Name]|[Quality (optional)]",
    'examples': "{tr}spotdl https://open.spotify.com/track/0Cy7wt6IlRfBPHXXjmZbcP|flac"})
async def spotify_dl(message: Message):
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    await message.edit("Checking? 🧐😳🤔🤔")
    cmd = ''
    link = ''
    song_n = ''
    quality = "mp3"
    if "|" in message.input_str:
        input_, quality = message.input_str.split("|")
        if 'spotify.com' in input_:
            await message.edit("Link, Hmm, Make sure to give valid one")
            link = input_
        else:
            await message.edit("🤔Song? Searching...")
            song_n = input_
    else:
        input_ = message.input_str
        if 'spotify.com' in input_:
            await message.edit("Link, Hmm, Make sure to gave valid one")
            link = input_
        else:
            await message.edit("🤔Song? Searching....")
            song_n = input_

    if song_n or link:
        if 'track/' in link:
            song_n = link
        if not song_n:
            await message.edit("Selling Brain is not yet Legalized")
            return
        await message.edit("Downloading")
        quality = quality.strip()  # Just for Precautions 🤷‍♂
        cmd = f"cd {TEMP_DIR} && spotdl {song_n}"
    if cmd:
        runn = await Term.execute(cmd)
        while not runn.finished:
            await asyncio.sleep(0.5)
            await message.try_to_edit(f"<code>{runn.read_line}</code>")
        if len(os.listdir(TEMP_DIR)) <= 1:
            await message.err("Download Failed.")
        else:
            await message.delete()
            for track in os.listdir(TEMP_DIR):
                if track.startswith("Temp"):
                    continue
                track_loc = TEMP_DIR + track
                await audio_upload(message, Path(track_loc), True)
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
