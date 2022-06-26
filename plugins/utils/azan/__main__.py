""" Islamic Prayers Time """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.
#
# Azan Module
# By: Safone (https://github.com/AsmSafone)

import os
from json import dumps

import aiohttp

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
    city = msg.input_str or os.environ.get("COUNTRY_CITY")
    if not city:
        return await msg.err("Please input Country, or set datetime env")
    async with aiohttp.ClientSession() as ses:
        url = f"https://muslimsalat.com/{city}.json?key=bd099c5825cbedb9aa934e255a81a5fc"
        async with ses.get(url) as resp:
            if resp.status != 200:
                return await msg.err("Unable to process your request")
            res = await resp.json()
        if res['status_code'] == 0:
            return await msg.err(dumps(res['status_error']))
        timefor = f"__{res['query']}, {res['country']}, {res['items'][0]['date_for']}.__\n"
        out_str = (
            "**Islamic prayer times**"
            f"\n{timefor}"
            f"\n**Fajr          :** __{res['items'][0]['fajr']}__"
            f"\n**Shurooq  :** __{res['items'][0]['shurooq']}__"
            f"\n**Dhuhr      :** __{res['items'][0]['dhuhr']}__"
            f"\n**Asr           :** __{res['items'][0]['asr']}__"
            f"\n**Maghrib  :** __{res['items'][0]['maghrib']}__"
            f"\n**Isha          :** __{res['items'][0]['isha']}__"
        )
        await msg.edit(out_str)
