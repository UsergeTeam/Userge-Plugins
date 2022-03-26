# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

from uuid import uuid4

from pyrogram.types import (
    CallbackQuery, InlineQuery, InlineKeyboardButton,
    InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup)
from pyrogram.types import Message as PyroMessage
from userge import userge, filters, config, Message

PRVT_MSGS = {}
FILTER = filters.create(
    lambda _, __, q: '-' in q.query and q.from_user and q.from_user.id in config.OWNER_ID)
MEDIA_FID_S = {}
OMKVU = None
DEEP_LINK_FLITER = filters.create(
    lambda _, __, msg: (
        msg and
        msg.chat and
        msg.chat.type == "private" and
        msg.text and
        msg.text.startswith("/start prvtmsg") and
        msg.from_user and
        not msg.sender_chat))


@userge.bot.on_callback_query(filters=filters.regex(pattern=r"prvtmsg\((.+)\)"))
async def prvt_msg(_, c_q: CallbackQuery):
    msg_id = str(c_q.matches[0].group(1))

    if msg_id not in PRVT_MSGS:
        await c_q.answer("message now outdated !", show_alert=True)
        return

    global OMKVU  # pylint: disable=global-statement
    if not OMKVU:
        OMKVU = (await userge.bot.get_me()).username

    user_id, flname, msg = PRVT_MSGS[msg_id]

    if c_q.from_user.id == user_id or c_q.from_user.id in config.OWNER_ID:
        if isinstance(msg, str):
            await c_q.answer(msg, show_alert=True)
        else:
            await c_q.answer(url=f"https://t.me/{OMKVU}?start=prvtmsg{msg_id}")
    else:
        await c_q.answer(
            f"Only {flname} can see this Private Msg... 😔", show_alert=True)


@userge.bot.on_inline_query(FILTER)
async def inline_answer(_, inline_query: InlineQuery):
    _id, msg = inline_query.query.split('-', maxsplit=1)

    if not (msg and msg.strip().endswith(':')):
        inline_query.stop_propagation()

    try:
        user = await userge.get_users(_id.strip())
    except Exception:  # pylint: disable=broad-except
        inline_query.stop_propagation()
        return

    c_m_e = MEDIA_FID_S.get(msg[:-1])
    if not c_m_e:
        PRVT_MSGS[inline_query.id] = (user.id, user.first_name, msg.strip(': '))
    else:
        PRVT_MSGS[inline_query.id] = (user.id, user.first_name, c_m_e)

    prvte_msg = [[InlineKeyboardButton(
        "Show Message 🔐", callback_data=f"prvtmsg({inline_query.id})")]]

    msg_c = f"🔒 A **private message** to {'@' + user.username}, "
    msg_c += "Only he/she can open it."

    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title=f"A Private Msg to {user.first_name}",
            input_message_content=InputTextMessageContent(msg_c),
            description="Only he/she can open it",
            thumb_url="https://te.legra.ph/file/16133ab3297b3f73c8da5.png",
            reply_markup=InlineKeyboardMarkup(prvte_msg)
        )
    ]

    await inline_query.answer(results=results, cache_time=3)


@userge.bot.on_cmd("secretmsg", about={
    'header': "send a media in bot personal message, and reply <code>{tr}secretmsg</code>",
    'usage': "{tr}secretmsg [reply to media]"})
async def recv_s_m_o(msg: Message):
    if not msg.reply_to_message:
        await msg.reply_text("reply to a media")
    media_type = msg.reply_to_message.media
    if media_type and media_type in [
        "contact",
        "dice",
        "poll",
        "location",
        "venue",
    ]:
        await msg.reply_text("invalid media type")
        return
    media_ifdd = getattr(msg.reply_to_message, media_type)
    if media_type:
        MEDIA_FID_S[
            str(msg.message_id)
        ] = {
            "file_id": media_ifdd.file_id,
            "caption": (msg.reply_to_message.caption and
                        msg.reply_to_message.caption.html) or ""
        }
    else:
        MEDIA_FID_S[
            str(msg.message_id)
        ] = {
            "file_id": "0",
            "caption": (msg.reply_to_message.text and
                        msg.reply_to_message.text.html) or ""
        }
    await msg.reply_text("click here", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
        text="send something",
        switch_inline_query=f"@theuserge - {msg.message_id}:"
    )]]))


@userge.bot.on_message(filters=DEEP_LINK_FLITER)
async def bot_prvtmsg_start_dl(_, message: PyroMessage):
    msg_id = message.text[14:]
    user_id, _, msg = PRVT_MSGS[msg_id]
    # redundant conditional check, to HP UBs
    if msg.from_user.id == user_id or msg.from_user.id in config.OWNER_ID:
        if msg["file_id"] != "0":
            await message.reply_cached_media(
                msg["file_id"],
                caption=msg["caption"],
                parse_mode="html"
            )
        else:
            await message.reply_text(
                msg["caption"],
                parse_mode="html"
            )
    else:
        await message.delete()
