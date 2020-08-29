""" AI chatbot """

# AI Chat Bot Module for @theUserge.
# Lydia AI Powered by CoffeeHouse from Intellivoid (Telegram: t.me/Intellivoid)
# Author: Phyco-Ninja (https://github.com/Phyco-Ninja) (@PhycoNinja13b)
# Thanks to @Intellivoid For Creating CoffeeHouse API

import os
import random
import asyncio
from time import time

from coffeehouse.api import API
from coffeehouse.lydia import LydiaAI, Session
from coffeehouse.exception import CoffeeHouseError
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid

from userge import userge, get_collection, Message, filters, pool
from userge.utils import get_file_id_and_ref

LOGGER = userge.getCLogger(__name__)
LYDIA_CHATS = get_collection("LYDIA_CHATS")
CH_LYDIA_API = os.environ.get("CH_LYDIA_API", None)
CUSTOM_REPLY_CHANNEL = int(os.environ.get("CUSTOM_REPLY_CHANNEL", 0))
if CH_LYDIA_API is not None:
    LYDIA = LydiaAI(API(CH_LYDIA_API))

ACTIVE_CHATS = {}
CUSTOM_REPLIES_IDS = []
QUEUE = asyncio.Queue()

LYDIA_API_INFO = """This module uses Lydia AI
Powered by CoffeeHouse API created by @Intellivoid.

Lydia is a Active Machine Learning Chat Bot.
Which can adapt to current user and chat with user
on any given topic."""


async def _init():
    async for chat in LYDIA_CHATS.find({'active': True}):
        ACTIVE_CHATS[chat['_id']] = (chat['session_id'], chat['session_exp'])
    if CUSTOM_REPLY_CHANNEL:
        async for message in userge.iter_history(chat_id=CUSTOM_REPLY_CHANNEL, limit=300):
            CUSTOM_REPLIES_IDS.append(message.message_id)


@userge.on_cmd("lydia", about={
    'header': "Lydia AI Chat Bot",
    'description': "An AI Powered Chat Bot Module"
                   " that uses Lydia AI from CoffeeHouse.\n"
                   "For more info use {tr}lydia -info",
    'flags': {'-on': "Enable AI on replied user",
              '-off': "Disable AI on replied user",
              '-list': "List All users",
              '-info': "Get Info about Lydia"},
    'usage': "{tr}lydia [flag] [reply to user]"})
async def lydia_session(message: Message):
    """ lydia command handler """
    if CH_LYDIA_API is None:
        await message.edit(
            "Please Configure `CH_LYDIA_API` & `CUSTOM_REPLY_CHANNEL`"
            "\n\nAll Instructions are available"
            " in @UnofficialPluginsHelp")
        return
    await message.edit("`processing lydia...`")
    replied = message.reply_to_message
    if '-on' in message.flags and replied:
        user_id = replied.from_user.id
        if user_id in ACTIVE_CHATS:
            await message.edit("AI is already Enabled on Replied User", del_in=3)
            return
        data = await LYDIA_CHATS.find_one({'_id': user_id})
        if not data:
            await message.edit("`creating new session...`")
            ses = await _create_lydia()
            await LYDIA_CHATS.insert_one(
                {'_id': user_id, 'session_id': ses.id, 'session_exp': ses.expires, 'active': True})
            ACTIVE_CHATS[user_id] = (ses.id, ses.expires)
        else:
            await message.edit("`activating session...`")
            await LYDIA_CHATS.update_one({'_id': user_id}, {"$set": {'active': True}})
            ACTIVE_CHATS[user_id] = (data['session_id'], data['session_exp'])
        await message.edit("`AI Enabled for Replied User`", del_in=3)
    elif '-off' in message.flags and replied:
        user_id = replied.from_user.id
        if user_id not in ACTIVE_CHATS:
            await message.edit("How to delete a thing that doesn't Exist?", del_in=3)
            return
        await message.edit("`disactivating session...`")
        await LYDIA_CHATS.update_one({'_id': user_id}, {"$set": {'active': False}})
        del ACTIVE_CHATS[user_id]
        await message.edit("`AI Disable for Replied User`", del_in=3)
    # Group Features Won't be displayed in Help Info For Now 😉
    elif '-enagrp' in message.flags:
        chat_id = message.chat.id
        if chat_id in ACTIVE_CHATS:
            await message.edit("AI is already Enabled on this chat", del_in=3)
            return
        data = await LYDIA_CHATS.find_one({'_id': chat_id})
        if not data:
            await message.edit("`creating new session...`")
            ses = await _create_lydia()
            await LYDIA_CHATS.insert_one(
                {'_id': chat_id, 'session_id': ses.id, 'session_exp': ses.expires, 'active': True})
            ACTIVE_CHATS[chat_id] = (ses.id, ses.expires)
        else:
            await message.edit("`activating session...`")
            await LYDIA_CHATS.update_one({'_id': chat_id}, {"$set": {'active': True}})
            ACTIVE_CHATS[chat_id] = (data['session_id'], data['session_exp'])
        await message.edit("`AI Enabled in Current Chat :D`", del_in=3)
    elif '-disgrp' in message.flags:
        chat_id = message.chat.id
        if chat_id not in ACTIVE_CHATS:
            await message.edit("AI wasn't enabled in current chat. >:(", del_in=3)
            return
        await message.edit("`disactivating session...`")
        await LYDIA_CHATS.update_one({'_id': chat_id}, {"$set": {'active': False}})
        del ACTIVE_CHATS[chat_id]
        await message.edit("`AI Disabled in Current Chat`", del_in=3)
    elif '-grps' in message.flags:
        msg = "**AI Enabled Chats**\n\n"
        for chat_id in ACTIVE_CHATS:
            if not str(chat_id).startswith("-100"):
                continue
            chat_ = await userge.get_chat(chat_id)
            title = chat_.title
            msg += f"{title} {chat_id}\n"
        await message.edit_or_send_as_file(msg)
    elif '-list' in message.flags:
        msg = "**AI Enabled User List**\n\n"
        for user_id in ACTIVE_CHATS:
            if str(user_id).startswith("-100"):
                continue
            try:
                u_info = await userge.get_user_dict(user_id)
                u_men = u_info['mention']
                msg += f"{u_men}\n"
            except PeerIdInvalid:
                msg += f"[user](tg://user?id={user_id}) - `{user_id}`\n"
        await message.edit_or_send_as_file(msg)
    elif '-info' in message.flags:
        await asyncio.gather(
            message.reply_photo(photo="resources/lydia.jpg", caption=LYDIA_API_INFO),
            message.delete()
        )
    else:
        await asyncio.gather(
            message.reply_sticker("CAADAQAEAQAC0rXRRju3sbCT07jIFgQ"),
            message.delete()
        )


@userge.on_filters(~filters.me & ~filters.edited & (filters.mentioned | filters.private), group=2)
async def lydia_ai_chat(message: Message):
    """ incomming message handler """
    if CH_LYDIA_API is None:
        return
    data = ACTIVE_CHATS.get(message.from_user.id, None)
    chat_id = message.from_user.id
    if not data:
        data = ACTIVE_CHATS.get(message.chat.id, None)
        chat_id = message.chat.id
    if data:
        ses_id, ses_time = data
        if int(ses_time) < time():
            ses = await _create_lydia()
            await LYDIA_CHATS.update_one(
                {'_id': chat_id},
                {"$set": {'session_id': ses.id, 'session_exp': ses.expires}})
            ACTIVE_CHATS[chat_id] = (ses.id, ses.expires)
            ses_id = ses.id
        try:
            out = ''
            await userge.send_read_acknowledge(
                chat_id=chat_id,
                message=message,
                clear_mentions=True)
            if not message.media and message.text:
                out = await _think_lydia(ses_id, message.text)
            QUEUE.put_nowait((message, out))
        except CoffeeHouseError as cfe:
            LOGGER.log(f"#CoffeeHouseError {cfe}")
    message.continue_propagation()


@userge.add_task
async def lydia_queue() -> None:
    """ queue handler """
    msg: Message
    out: str
    while True:
        msg, out = await QUEUE.get()
        if (msg is None) or (out is None):
            break
        if msg.text:
            await asyncio.sleep(len(msg.text) / 10)
        if msg.media or not out:
            await _custom_media_reply(msg)
        else:
            await _send_text_like_a_human(msg, out)


# A workaround for replies of Media as per now Lydia can't process Media input,
# And it's logical though. So this func will call custom message input by user
# saved in a channel and reply it to message.
# Idea arised from here (https://t.me/usergeot/157629) thnx 👍
async def _custom_media_reply(message: Message):
    if CUSTOM_REPLIES_IDS:
        await asyncio.sleep(1)
        cus_msg = int(random.choice(CUSTOM_REPLIES_IDS))
        cus_msg = await message.client.get_messages(chat_id=CUSTOM_REPLY_CHANNEL,
                                                    message_ids=cus_msg)
        if cus_msg.service:
            await _custom_media_reply(message)
            return
        if cus_msg.media:
            file_id, file_ref = get_file_id_and_ref(cus_msg)
            try:
                if cus_msg.animation:
                    await message.client.send_animation(
                        chat_id=message.chat.id,
                        animation=file_id,
                        file_ref=file_ref,
                        unsave=True,
                        reply_to_message_id=message.message_id
                    )
                else:
                    action = None
                    if cus_msg.audio:
                        action = "upload_audio"
                    elif cus_msg.document:
                        action = "upload_document"
                    elif cus_msg.photo:
                        action = "upload_photo"
                    elif cus_msg.video:
                        action = "upload_audio"
                    elif cus_msg.voice:
                        action = "record_audio"
                    elif cus_msg.video_note:
                        action = "upload_video_note"
                    if action:
                        await message.reply_chat_action(action)
                    await asyncio.sleep(5)
                    await message.reply_cached_media(
                        file_id=file_id,
                        file_ref=file_ref
                    )
            except Exception as idk:  # pylint: disable=W0703
                LOGGER.log(f"#ERROR: `{idk}`")
                await _custom_media_reply(message)
                return
        if cus_msg.text:
            await _send_text_like_a_human(message, cus_msg.text)


async def _send_text_like_a_human(message: Message, text: str) -> None:
    sleep_time = len(text) // 5 or 1
    count = 0
    while sleep_time > count:
        if not count % 5:
            await message.reply_chat_action("typing")
        await asyncio.sleep(1)
        count += 1
    await message.reply_chat_action("cancel")
    await message.reply(text)


@pool.run_in_thread
def _create_lydia() -> Session:
    return LYDIA.create_session("en")


@pool.run_in_thread
def _think_lydia(ses_id: str, text: str) -> str:
    return LYDIA.think_thought(ses_id, text)
