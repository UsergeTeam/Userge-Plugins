""" attach link preview to message """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)

from userge import userge, Message


@userge.on_cmd("attach", about={
    'header': "Attach any link's preview in a message",
    'usage': "{tr}attach [link] [reply to a message]"})
async def attach(update: Message):
    """Attach links in message"""
    link = update.text.split()[1]
    replied = update.reply_to_message
    if replied is None or not link:
        await update.reply_text(
            text="`Reply to a text for attachment and provide link as input...`"
        )
        return
    text = replied.text
    await replied.edit_text(text=f"[\u2063]({link}){text}")
    await update.delete()
