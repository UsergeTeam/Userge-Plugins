import os
import shutil
import asyncio
from pathlib import Path

from userge import userge, Message
from userge.plugins.misc.upload import audio_upload
from userge.plugins.tools.executor import Term

TEMP_DIR = "spotdl/"


@userge.on_cmd("spotdl", about={
    'header': "Spotify Downloader",
    'description': "Download Songs via Spotify Links"
                   " or just by giving song names. ",
    'usage': "{tr}spotdl [Spotify Link or Song Name]",
    'examples': "{tr}spotdl https://open.spotify.com/track/0Cy7wt6IlRfBPHXXjmZbcP"})
async def spotify_dl(message: Message):
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    song_or_link = message.input_str
    await message.edit(f"`Downloading {song_or_link} ...`")
    cmd = f"cd {TEMP_DIR} && spotdl {song_or_link}"
    runn = await Term.execute(cmd)
    while not runn.finished:
        await asyncio.sleep(1)
        if runn.read_line:
            await message.try_to_edit(f">><code>{runn.read_line}</code>")
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
