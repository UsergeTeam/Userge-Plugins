""" Url shortener """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

# By @Krishna_Singhal

import gdshortener
from pyrogram.errors import YouBlockedUser

from userge import userge, Message
from userge.utils.exceptions import StopConversation


@userge.on_cmd("bitly", about={
    'header': "Shorten Any Url using bit.ly",
    'usage': "{tr}bitly [link or reply]"}, allow_via_bot=False)
async def bitly(msg: Message):
    url = msg.input_or_reply_str
    if not url:
        await msg.err("need url to shorten")
        return
    try:
        async with userge.conversation("Sl_BitlyBot") as conv:
            try:
                await conv.send_message("/start")
            except YouBlockedUser:
                await userge.unblock_user("Sl_BitlyBot")
                await conv.send_message("/start")
            await conv.get_response(mark_read=True)
            await conv.send_message(url)
            shorten_url = (
                await conv.get_response(mark_read=True)
            ).text.split('\n', maxsplit=1)[-1]
            await msg.edit(f"`{shorten_url}`", disable_web_page_preview=True)
    except StopConversation:
        await msg.err("bot is down")


@userge.on_cmd("isgd", about={
    'header': "Shorten Any Url using is.gd",
    'usage': "{tr}isgd [link or reply]"})
async def is_gd(msg: Message):
    url = msg.input_or_reply_str
    if not url:
        await msg.err("need url to shorten")
        return
    s = gdshortener.ISGDShortener()
    try:
        s_url, stats = s.shorten(url, log_stat=True)
    except Exception as er:
        await msg.err(str(er))
    else:
        await msg.edit(
            f"**Shortened URL:**\n`{s_url}`\n\n**Stats:** `{stats}`",
            disable_web_page_preview=True
        )


@userge.on_cmd("statsisgd", about={
    'header': "Convert is.gd url into original URl.",
    'usage': "{tr}statsisgd [link or reply]"})
async def stats_is_gd(msg: Message):
    url = msg.input_or_reply_str
    if not url:
        await msg.err("need url to check stats")
        return
    s = gdshortener.ISGDShortener()
    try:
        original_url = s.lookup(url)
    except Exception as er:
        await msg.err(str(er))
    else:
        await msg.edit(
            f"**URL:** `{original_url}`",
            disable_web_page_preview=True
        )
