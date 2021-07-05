""" Music , To Search and Download HQ Music From JioSaavn"""

# Made By Devanagaraj
# https://github.com/Devanagaraj
# Thanks to ARQ API

import os

from aiohttp import ClientSession
from Python_ARQ import ARQ
from userge import Config, Message, userge
from userge.plugins.misc.download import url_download

ARQ_KEY = os.environ.get("ARQ_KEY", None)

# ARQ API
session = ClientSession()
arq = ARQ("https://thearq.tech", ARQ_KEY, session)
saavn = arq.saavn

LOGGER = userge.getLogger(__name__)


@userge.on_cmd(
    "music",
    about={
        "header": "Search and Download Music",
        "description": "It Searches and Downloads Music from JioSaavn in HQ",
        "examples": "{tr}music name",
    },
)
async def music(message: Message):
    if not ARQ_KEY:
        return await message.err(
            "Before using this command, "
            "you have to set this [Environmental var.](https://t.me/UnofficialPluginsHelp/128)",
            disable_web_page_preview=True
        )
    query = message.input_str
    await message.edit(f"Searching for {query} in JioSaavn...")
    try:
        res = await arq.saavn(query)
    except Exception as e:
        return await message.err(str(e))
    if not res.ok:
        return await message.edit("Found Nothing... Try again...")
    song = res.result[0]
    title = song.song
    url = song.media_url
    artist = song.singers
    duration = int(song.duration)
    caption_str = f"`{title}` by `{artist}`"
    pathh, _ = await url_download(message, url)
    temp_name = f"{title}.mp3"
    song_path = os.path.join(Config.DOWN_PATH, str(message.message_id), temp_name)
    os.renames(pathh, song_path)
    await message.reply_audio(
        audio=song_path,
        caption=caption_str,
        duration=duration,
        performer=artist,
        title=title,
        quote=False,
    )
    await message.delete()
    os.remove(song_path)
