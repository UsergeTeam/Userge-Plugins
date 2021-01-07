# Professor | Albert Einstein
# @TheUnusualPsychopath | @Albert_Einetin_TG
# @TrojanzHEX | @CrazyBotsz

import os
import time
import pytz
from datetime import datetime
from userge import userge, Message

UpdatesChannel = os.environ.get("UPDATES_CHANNEL", "@UsergeOT")
BOTSZ = os.environ.get("BOTSZ", "UsergeBot, Userge_Git_Bot")
Botsz = []
if BOTSZ:
    Botsz = [i and i.strip() for i in BOTSZ.split(',')]

@userge.on_cmd("balive", about={
    'header': "Pings All Defined Bots",
    'description': "<b>Ping and Updates The Status Of All Defined Bots In 'BOTSZ' var</b>\n\n"
                   "Available Vars:\n\n"
                   "UPDATES_CHANNEL : Provide Your Channel Name With @\n\n"
                   "BOTSZ : Define All Your Bot's Username With Out @ And Seperate Each With ','"
})
async def bots(message: Message):
    first_msg = f"<b>Bots Status @{UpdatesChannel}\n°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°</b>\n\n"
    reply = await message.edit(first_msg, parse_mode="html")
    for bot in Botsz:
        checking = f"<b>⚡ @{bot} Status : Checking...⌛</b>\n\n"
        first_msg += checking
        await reply.edit_text(first_msg, parse_mode="html")
        snt = await userge.send_message(bot, '/start')
        time.sleep(5)
        msg = await userge.get_history(bot, 1)
        if snt.message_id == msg[0].message_id:
            nice = f"<b>⚡ @{bot} Status : ❎</b>\n\n"
        else:
            nice = f"<b>⚡ @{bot} Status : ✅</b>\n\n"
        first_msg = first_msg.replace(checking, nice)
        await reply.edit_text(first_msg, parse_mode="html")
        await userge.read_history(bot)
    tz = pytz.timezone('Asia/Kolkata')
    time_now = datetime.utcnow().astimezone(tz=tz).strftime("%I:%M %p - %d %B %Y")
    first_msg += f"<code>[Updated on : {time_now}]</code>"
    await reply.edit_text(first_msg, parse_mode="html")


# @CrazyBotsz
# @TheUnusualPsychopath
