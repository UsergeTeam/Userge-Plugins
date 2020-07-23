# Userge Plugin for Torrent Search from torrent-paradise.ml
# Author: Nageen (https://github.com/archie9211) (@archie9211)
# All rights reserved

import re

import requests

from userge import userge, Message
from userge.utils import humanbytes


@userge.on_cmd("tstp", about={
    'header': "Torrent Search On torrent-paradise.ml ",
    'description': "Search torrent from different websites"
                   "offered by torrent-paradise, by default limit is 10",
    'usage': "{tr}tstp [query] [-limit]",
    'examples': "{tr}tstp The vampire diaries -l5"})
async def torr_search(message: Message):
    await message.edit("`Searching for available Torrents!`")
    input_ = message.input_or_reply_str
    max_limit = 10
    get_limit = re.compile(r'-l\d*[0-9]')
    query = re.sub(r'-\w*', "", input_).strip()
    r = requests.get(
        "https://torrent-paradise.ml/api/search?q=" + query)
    if get_limit.search(input_) is not None:
        max_limit = int(get_limit.search(input_).group().strip('-l'))
    try:
        torrents = r.json()
        reply_ = ""
        torrents = sorted(torrents, key=lambda i: i['s'], reverse=True)
        for torrent in torrents[:min(max_limit, len(torrents))]:
            if len(reply_) < 4096 and torrent["s"] > 0:
                try:
                    reply_ = (reply_ + f"\n\n<b>{torrent['text']}</b>\n"
                              f"<b>Size:</b> {humanbytes(torrent['len'])}\n"
                              f"<b>Seeders:</b> {torrent['s']}\n"
                              f"<b>Leechers:</b> {torrent['l']}\n"
                              f"<code>magnet:?xt=urn:btih:{torrent['id']}</code>")
                except Exception:
                    pass
        if reply_ == "":
            await message.edit(f"No torrents found for {query}!")
        else:
            await message.edit(text=reply_, parse_mode="html")
    except Exception:
        await message.edit("Torrent Search API is Down!\nTry again later")
