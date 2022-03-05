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


import json

import requests

from userge import userge, Message, pool


@userge.on_cmd("azan", about={
    'header': "Islamic Prayers Time",
    'description': "Shows the Islamic prayer times of the given city.",
    'usage': "{tr}azan [city_name]"})
async def _azan(message: Message):
    if " " not in message.text:
        await message.edit("`Send a city name with command`", del_in=5)
        return
    city = message.text.split(" ", 1)[1]
    url = f"http://muslimsalat.com/{city}.json?key=bd099c5825cbedb9aa934e255a81a5fc"
    request = await pool.run_in_thread(requests.get)(url)
    if request.status_code != 200:
        await message.edit(f"`Couldn't fetch any data about the city {city}`", del_in=5)
        return
    result = json.loads(request.text)
    prayer_time = f"<b>Islamic Prayers Time</b>\
            \n\n<b>City     : </b><i>{result['query']}</i>\
            \n<b>Country  : </b><i>{result['country']}</i>\
            \n<b>Date     : </b><i>{result['items'][0]['date_for']}</i>\
            \n<b>Fajr     : </b><i>{result['items'][0]['fajr']}</i>\
            \n<b>Shurooq    : </b><i>{result['items'][0]['shurooq']}</i>\
            \n<b>Dhuhr    : </b><i>{result['items'][0]['dhuhr']}</i>\
            \n<b>Asr    : </b><i>{result['items'][0]['asr']}</i>\
            \n<b>Maghrib    : </b><i>{result['items'][0]['maghrib']}</i>\
            \n<b>Isha     : </b><i>{result['items'][0]['isha']}</i>\
    "
    await message.edit(prayer_time, parse_mode="html")
