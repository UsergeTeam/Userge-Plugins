""" Music , To Search and Download HQ Music From JioSaavn"""

# Made By Devanagaraj
# https://github.com/Devanagaraj
# Thanks to ARQ API

import os
from random import randint
from userge import userge, Message, Config, pool
from userge.utils import time_formatter, humanbytes
from userge.plugins.misc.download import url_download
from Python_ARQ import ARQ
from aiohttp import ClientSession

ARQ_KEY = os.environ.get("ARQ_KEY", None)

# ARQ API and Bot Initialize---------------------------------------------------
session = ClientSession()
arq = ARQ("https://thearq.tech",ARQ_KEY,session)
saavn = arq.saavn

LOGGER = userge.getLogger(__name__)

@userge.on_cmd("music", about={'header': "Search and Download Music",
                                'description': 'It Searches and Downloads Top Music result from JioSaavn in HQ',
                                'examples': '{tr}Song name'})
async def music(message: Message):
    query = message.text.split(None, 1)[1]
    await message.edit(f"Searching for {query} in JioSaavn...")
    try:
        res = await arq.saavn(query)
    except Exception as a:
        await message.err(str(a))
    if not res.ok:
        await message.edit("Found Nothing... Try again...")
        return
    song = res['result'][0]
    sname = song['song']
    slink = song['media_url']
    singers =song['singers']
    sduration = int(song['duration'])
    caption_str = f"`{sname}` by `{singers}`"
    pathh, secs = await url_download(message,slink)
    temp_name = f"{randint(6969, 6999)}.mp3"
    song_path = os.path.join(Config.DOWN_PATH, temp_name)
    os.rename(pathh,song_path)
    await message.reply_audio(
                        audio=song_path,
                        caption=caption_str,
                        duration=sduration,
                        performer=singers,
                        title=sname
                    )
    await message.delete()
    os.remove(song_path)
    
