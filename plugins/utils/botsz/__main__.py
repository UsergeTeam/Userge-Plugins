""" Pings All Defined Bots """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.


# Professor | Albert Einstein
# @TheUnusualPsychopath | @Albert_Einetin_TG
# @TrojanzHEX | @CrazyBotsz

import time
from datetime import datetime

import pytz

from userge import userge, Message
from pyrogram import enums


@userge.on_cmd(
    "balive", about={
        'header': "Pings All Defined Bots",
        'description': "<b>Pings All bots you mention and check their status.</b>\n\n"
                       "[NOTE]: you can pass multiple ids, seprate them via new line",
        'usage': "{tr}balive [bot id/username]"}, allow_via_bot=False)
async def bots(message: Message):
    _msg = "<b>Bots Status\n°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°</b>\n\n"
    await message.edit(_msg, parse_mode=enums.ParseMode.HTML)
    if not message.input_str:
        return await message.edit("Bots not found!")
    Bot_List = [bot.strip() for bot in message.input_str.split('\n') if bot.strip()]
    for bot in Bot_List:
        checking = f"<b>⚡ {bot} Status : Checking...⌛</b>\n\n"
        _msg += checking
        await message.edit(_msg, parse_mode=enums.ParseMode.HTML)
        snt = await userge.send_message(bot, '/start')
        time.sleep(5)
        msg = [msg async for msg in userge.get_chat_history(bot, 1)]
        if snt.id == msg[0].id:
            nice = f"<b>⚡ {bot} Status : ❎</b>\n\n"
        else:
            nice = f"<b>⚡ {bot} Status : ✅</b>\n\n"
        _msg = _msg.replace(checking, nice)
        await message.edit(_msg, parse_mode=enums.ParseMode.HTML)
        await userge.read_chat_history(bot)
    tz = pytz.timezone('Asia/Kolkata')
    time_now = datetime.utcnow().astimezone(tz=tz).strftime("%I:%M %p - %d %B %Y")
    _msg += f"<code>[Updated on : {time_now}]</code>"
    await message.edit(_msg, parse_mode=enums.ParseMode.HTML)
