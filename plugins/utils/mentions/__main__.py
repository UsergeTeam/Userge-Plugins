""" Mentions alerter Plugin """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram.errors import PeerIdInvalid, BadRequest
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import enums

from userge import userge, Message, config, filters, get_collection

SAVED_SETTINGS = get_collection("CONFIGS")
TOGGLE = False


@userge.on_start
async def _init():
    global TOGGLE  # pylint: disable=global-statement
    data = await SAVED_SETTINGS.find_one({"_id": "MENTION_TOGGLE"})
    if data:
        TOGGLE = bool(data["data"])


@userge.on_cmd(
    "mentions",
    about="Toggles Mentions, "
          "if enabled Bot will send Message if anyone mention you."
)
async def toggle_mentions(msg: Message):
    """ toggle mentions """
    global TOGGLE  # pylint: disable=global-statement
    if TOGGLE:
        TOGGLE = False
    else:
        TOGGLE = True
    await SAVED_SETTINGS.update_one(
        {"_id": "MENTION_TOGGLE"}, {"$set": {"data": TOGGLE}}, upsert=True
    )
    await msg.edit(f"Mentions Alerter **{'enabled' if TOGGLE else 'disabled'}** Successfully.")


@userge.on_filters(
    ~filters.me & ~filters.bot & ~filters.service
    & (filters.mentioned | filters.private), group=1, allow_via_bot=False)
async def handle_mentions(msg: Message):

    if TOGGLE is False:
        return

    if not msg.from_user or msg.from_user.is_verified:
        return

    if msg.chat.type == enums.ChatType.PRIVATE:
        is_private = True
        link = f"tg://openmessage?user_id={msg.chat.id}&message_id={msg.id}"
        text = f"{msg.from_user.mention} 💻 sent you a **Private message.**"
    else:
        is_private = False
        if msg.chat.type == enums.ChatType.GROUP:
            link = f"tg://openmessage?chat_id={str(msg.chat.id).strip('-')}&message_id={msg.id}"
        else:
            link = msg.link
        text = f"{msg.from_user.mention} 💻 tagged you in **{msg.chat.title}.**"
    text += f"\n\n[Message]({link}):" if not userge.has_bot else "\n\n**Message:**"
    if msg.text:
        text += f"\n`{msg.text}`"
    buttons = [[InlineKeyboardButton(text="📃 Message Link", url=link)]]

    client = userge.bot if userge.has_bot else userge
    if not msg.text:
        if is_private:
            chat_id = config.LOG_CHANNEL_ID
            media_client = userge
        else:
            media_client = client
            chat_id = userge.id if userge.has_bot else config.LOG_CHANNEL_ID
    try:
        if not msg.text:
            try:
                sentMedia = await media_client.copy_message(
                    chat_id,
                    msg.chat.id,
                    msg.id
                )
            except (PeerIdInvalid, BadRequest):
                sentMedia = await userge.copy_message(
                    config.LOG_CHANNEL_ID,
                    msg.chat.id,
                    msg.id
                )
            buttons.append([InlineKeyboardButton(text="📃 Media Link", url=sentMedia.link)])
        await client.send_message(
            chat_id=userge.id if userge.has_bot else config.LOG_CHANNEL_ID,
            text=text,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except PeerIdInvalid:
        if userge.dual_mode:
            await userge.send_message(userge.bot.id, "/start")
            if not msg.text:
                try:
                    sentMedia = await media_client.copy_message(
                        chat_id,
                        msg.chat.id,
                        msg.id
                    )
                except (PeerIdInvalid, BadRequest):
                    sentMedia = await userge.copy_message(
                        config.LOG_CHANNEL_ID,
                        msg.chat.id,
                        msg.id
                    )
                buttons.append([InlineKeyboardButton(text="📃 Media Link", url=sentMedia.link)])
            await client.send_message(
                chat_id=userge.id if userge.has_bot else config.LOG_CHANNEL_ID,
                text=text,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        else:
            raise
