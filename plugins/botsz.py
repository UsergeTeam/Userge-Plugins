# Professor | Albert Einstein
# @TheUnusualPsychopath | @Albert_Einetin_TG
# @TrojanzHEX | @CrazyBotsz

import os
import time
import pytz
from datetime import datetime
from userge import userge, Message


@userge.on_cmd("balive",
    about={
        'header': "Pings All Defined Bots",
        'description': "<b>Ping and All bots and check their status.</b>\n\n"
                       "[NOTE]: you can pass multiple ids, seprate them via new line",
        'usage': "{tr}belive [bot id/username]"
    }, allow_via_bot=False
)
async def bots(message: Message):
    msg = "<b>Bots Status\n°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°</b>\n\n"
    await message.edit(first_msg, parse_mode="html")
    if not message.input_str:
        return await message.edit("Bots not found!")
    Bot_List = [bot.strip() for bot in message.input_str.split('\n') if bot.strip()]
    for bot in Bot_List:
        checking = f"<b>⚡ {bot} Status : Checking...⌛</b>\n\n"
        msg += checking
        await message.edit(first_msg, parse_mode="html")
        snt = await userge.send_message(bot, '/start')
        time.sleep(5)
        msg = await userge.get_history(bot, 1)
        if snt.message_id == msg[0].message_id:
            nice = f"<b>⚡ {bot} Status : ❎</b>\n\n"
        else:
            nice = f"<b>⚡ {bot} Status : ✅</b>\n\n"
        first_msg = first_msg.replace(checking, nice)
        await message.edit(first_msg, parse_mode="html")
        await userge.read_history(bot)
    tz = pytz.timezone('Asia/Kolkata')
    time_now = datetime.utcnow().astimezone(tz=tz).strftime("%I:%M %p - %d %B %Y")
    first_msg += f"<code>[Updated on : {time_now}]</code>"
    await message.edit(first_msg, parse_mode="html")


# @CrazyBotsz
# @TheUnusualPsychopath
