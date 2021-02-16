# Userge Plugin for Torrent Search
# Author: Sumanjay (https://github.com/cyberboysumanjay) (@cyberboysumanjay)
# All rights reserved

import requests
from userge import userge, Message


@userge.on_cmd("ts", about={
    'header': "Searches Torrents from Telegram",
    'usage': "Reply to any user's message or enter query",
    'examples': "{tr}ts [query]"})
async def torr_search(message: Message):
    await message.edit("`Searching for available Torrents!`")
    query = message.input_or_reply_str
    r = requests.get(
        "https://api.sumanjay.cf/torrent/?query=" + query)
    try:
        torrents = r.json()
        reply_ = ""
        for torrent in torrents:
            if len(reply_) < 4096:
                try:
                    reply_ = (reply_ + f"\n\n<b>{torrent['name']}</b>\n"
                              f"<b>Size:</b> {torrent['size']}\n"
                              f"<b>Seeders:</b> {torrent['seeder']}\n"
                              f"<b>Leechers:</b> {torrent['leecher']}\n"
                              f"<code>{torrent['magnet']}</code>")
                    await message.edit(text=reply_, parse_mode="html")
                except Exception:
                    pass

        if reply_ == "":
            await message.edit(f"No torrents found for {query}!")
    except Exception:
        await message.edit("Torrent Search API is Down!\nTry again later")
