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

from userge import userge, filters, config

PRVT_MSGS = {}
FILTER = filters.create(
    lambda _, __, q: '-' in q.query and q.from_user and q.from_user.id in config.OWNER_ID)


@userge.bot.on_callback_query(filters=filters.regex(pattern=r"prvtmsg\((.+)\)"))
async def prvt_msg(_, c_q: CallbackQuery):
    msg_id = str(c_q.matches[0].group(1))

    if msg_id not in PRVT_MSGS:
        await c_q.answer("message now outdated !", show_alert=True)
        return

    user_id, flname, msg = PRVT_MSGS[msg_id]

    if c_q.from_user.id == user_id or c_q.from_user.id in config.OWNER_ID:
        await c_q.answer(msg, show_alert=True)
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

    PRVT_MSGS[inline_query.id] = (user.id, user.first_name, msg.strip(': '))

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
            thumb_url="https://imgur.com/download/Inyeb1S",
            reply_markup=InlineKeyboardMarkup(prvte_msg)
        )
    ]

    await inline_query.answer(results=results, cache_time=3)
