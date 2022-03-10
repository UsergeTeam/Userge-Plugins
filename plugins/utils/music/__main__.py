""" Music , To Search and Download HQ Music From JioSaavn And Deezer"""

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

# Made By Devanagaraj
# Reference https://github.com/Devanagaraj/Tg_Meowzik_Bot
# Thanks to ARQ API

import os

from Python_ARQ import ARQ
from aiohttp import ClientSession

from userge import config, Message, userge
from .. import music
from ...misc.download import url_download

# ARQ API
session = ClientSession()
arq = ARQ(
    "https://thearq.tech", music.ARQ_KEY, session
) if music.ARQ_KEY else None

LOGGER = userge.getLogger(__name__)


@userge.on_cmd(
    "saavn",
    about={
        "header": "Search and Download Music",
        "description": "It Searches and Downloads Music from JioSaavn in HQ",
        "examples": "{tr}saavn name",
    },
)
async def savn(message: Message):
    if not music.ARQ_KEY:
        return await message.err(
            "Before using this command, "
            "you have to set this [Environmental var.](https://t.me/UsergePlugins/128)",
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
    song_path = os.path.join(config.Dynamic.DOWN_PATH, temp_name)
    os.rename(pathh, song_path)
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


@userge.on_cmd(
    "deezer",
    about={
        "header": "Download from Deezer",
        "options": {"-f": "Sends High Res Flac from Deezer"},
        "examples": ["{tr}deezer Song name", "{tr}deezer -f Song name"],
    },
    del_pre=True,
)
async def deeza(message: Message):
    if not music.ARQ_KEY:
        return await message.err(
            "Before using this command, "
            "you have to set this [Environmental var.](https://t.me/UsergePlugins/128)",
            disable_web_page_preview=True
        )
    query = str(message.filtered_input_str)
    await message.edit(f"Searching for {query} in Deezer...")
    try:
        res = await arq.deezer(query, 1, 9 if message.flags else 3)
    except Exception as e:
        return await message.err(str(e))
    if not res.ok:
        return await message.edit("Found Nothing... Try again...")
    song = res.result[0]
    title = song.title
    url = song.url
    thumb = song.thumbnail
    artist = song.artist
    duration = int(song.duration)
    caption_str = f"`{title}` by `{artist}`"
    pathh, _ = await url_download(message, url)
    thumby, _ = await url_download(message, thumb)
    if pathh.endswith("m4a"):
        temp_name = f"{title}.mp3"
    else:
        temp_name = f"{title}.flac"
    song_path = os.path.join(config.Dynamic.DOWN_PATH, temp_name)
    os.rename(pathh, song_path)
    await message.reply_audio(
        audio=song_path,
        thumb=thumby,
        caption=caption_str,
        duration=duration,
        performer=artist,
        title=title,
        quote=False,
    )
    await message.delete()
    os.remove(song_path)
