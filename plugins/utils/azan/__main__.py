""" Islamic Prayers Time """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.
# Azan Module
# By: Safone (https://github.com/AsmSafone)

import aiohttp
import os

from userge import userge, Message


@userge.on_cmd(
    "azan",
    about={
        "header": "Islamic Prayers Time",
        "description": "Shows the Islamic prayer times of the given city.",
        "usage": "{tr}azan [city_name]",
    },
)
async def azan(msg: Message):
    """Azan handler, get an time for Islamic prayer."""
    city = msg.input_str
    if not city:
        city = os.environ.get("COUNTRY_CITY")
        if city is None:
            return msg.edit(f"`Please input Country, or set datetime env`", del_in=5)
    async with aiohttp.ClientSession() as ses:
        url = f"http://muslimsalat.com/{city}.json?key=bd099c5825cbedb9aa934e255a81a5fc"
        async with ses.get(url) as resp:
            if resp.status != 200:
                return msg.edit(f"**Something wrong!**\n`Unable to process your request`", del_in=5)
            res = await resp.json()
            timefor = f"__{res['query']}, {res['country']}, {res['items'][0]['date_for']}__\n"
            string = (
                f"\n**Fajr     :** __{res['items'][0]['fajr']}__"
                f"\n**Shurooq  :** __{res['items'][0]['shurooq']}__"
                f"\n**Dhuhr    :** __{res['items'][0]['dhuhr']}__"
                f"\n**Asr      :** __{res['items'][0]['asr']}__"
                f"\n**Maghrib  :** __{res['items'][0]['maghrib']}__"
                f"\n**Isha     :** __{res['items'][0]['isha']}__"
            )
    return await msg.edit(f"**Islamic prayer times**\n{timefor}{string}")
