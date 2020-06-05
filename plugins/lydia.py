# AI Chat Bot Module for @theUserge.
# Lydia AI Powered by CoffeeHouse from Intellivoid (Telegram: t.me/Intellivoid)
# Author: Phyco-Ninja (https://github.com/Phyco-Ninja) (@PhycoNinja13b)
# Thanks to @Intellivoid For Creating CoffeeHouse API


import os
import random
import asyncio
from time import time

from coffeehouse.lydia import LydiaAI
from coffeehouse.api import API
from coffeehouse.exception import CoffeeHouseError

from userge import userge, get_collection, Message, Filters, Config


LYDIA_SESSION = get_collection("LYDIA_SESSION")
LYDIA_EUL = get_collection("LYDIA_ENABLED_USERS_LIST")
LYDIA_GRP = get_collection("LYDIA_ENABLED_GROUPS")
CH_LYDIA_API = os.environ.get("CH_LYDIA_API", None)
CUSTOM_REPLY_CHANNEL = int(os.environ.get("CUSTOM_REPLY_CHANNEL", 0))
if CH_LYDIA_API is not None:
    ch_api = API(CH_LYDIA_API)
    lydia = LydiaAI(ch_api)

ACTIVE_USER_LIST = []
ENABLED_CHATS = []
CUSTOM_REPLIES = []

LYDIA_API_INFO = """This module uses Lydia AI
Powered by CoffeeHouse API created by @Intellivoid.

Lydia is a Active Machine Learning Chat Bot.
Which can adapt to current user and chat with user
on any given topic. """


async def _init():
    async for user in LYDIA_EUL.find():
        ACTIVE_USER_LIST.append(user['_uid'])
    async for chat in LYDIA_GRP.find():
        ENABLED_CHATS.append(chat['_cid'])
    if CUSTOM_REPLY_CHANNEL:
        async for message in userge.iter_history(chat_id=CUSTOM_REPLY_CHANNEL, limit=300):
            CUSTOM_REPLIES.append(message)


# A workaround for replies of Media as per now Lydia can't process Media input,
# And it's logical though. So this func will call custom message input by user
# saved in a channel and reply it to message.
# Idea arised from here (https://t.me/usergeot/157629) thnx 👍
async def custom_media_reply(message, client):
    global CUSTOM_REPLIES
    cus_msg = random.choice(CUSTOM_REPLIES)
    replied = message.message_id
    if cus_msg.media:
        if cus_msg.sticker:
            await message.reply_sticker(cus_msg.sticker.file_id)
        if (cus_msg.photo or cus_msg.video or cus_msg.animation):
            dls = await client.download_media(message=cus_msg, file_name=Config.DOWN_PATH)
            dls_loc = os.path.join(Config.DOWN_PATH, os.path.basename(dls))
            if cus_msg.photo:
                await message.reply_photo(dls_loc)
            if cus_msg.video:
                await message.reply_video(dls_loc)
            if cus_msg.animation:
                await client.send_animation(
                    chat_id=message.chat.id,
                    animation=dls_loc,
                    unsave=True,
                    reply_to_message_id=replied
                )
            os.remove(dls_loc)
    if cus_msg.text:
        await message.reply(cus_msg.text)


@userge.on_cmd("lydia", about={
    'header': "Lydia AI Chat Bot",
    'description': "An AI Powered Chat Bot Module"
                   " that uses Lydia AI from CoffeeHouse.\n"
                   "For more info use .lydia -info",
    'flags': {'-on': "Enable AI on replied user",
              '-off': "Disable AI on replied user",
              '-list': "List All users",
              '-info': "Get Info about Lydia"},
    'usage': "{tr}lydia [flag] [reply to user]"})
async def lydia_session(message: Message):
    if CH_LYDIA_API is None:
        await message.edit(
            "Please Configure `CH_LYDIA_API` & `CUSTOM_REPLY_CHANNEL`"
            "\n\nAll Instructions are available"
            " in @UnofficialPluginsHelp")

    replied = message.reply_to_message
    if '-on' in message.flags and replied:
        user_id = replied.from_user.id
        if not await LYDIA_SESSION.find_one({'_id': "LYDIA_SES"}):
            ses = lydia.create_session("en")
            await LYDIA_SESSION.insert_one(
                {'_id': "LYDIA_SES", 'session_id': ses.id, 'session_exp': ses.expires})
        if user_id in ACTIVE_USER_LIST:
            await message.edit("AI is already Enabled on Replied User")
            return
        await LYDIA_EUL.insert_one({'_uid': user_id})
        ACTIVE_USER_LIST.append(user_id)
        await message.edit("AI Enabled for Replied User", del_in=2)

    if '-off' in message.flags and replied:
        user_id = replied.from_user.id
        if await LYDIA_EUL.find_one_and_delete({'_uid': user_id}):
            out = "AI Disable for Replied User"
            if user_id in ACTIVE_USER_LIST:
                ACTIVE_USER_LIST.remove(user_id)
        else:
            out = "How to delete a thing that doesn't Exist?"
        await message.edit(out, del_in=5)

    # Group Features Won't be displayed in Help Info For Now 😉
    if '-enagrp' in message.flags:
        chat_id = message.chat.id
        if not await LYDIA_SESSION.find_one({'_id': "LYDIA_SES"}):
            ses = lydia.create_session("en")
            await LYDIA_SESSION.insert_one(
                {'_id': "LYDIA_SES", 'session_id': ses.id, 'session_exp': ses.expires})
        await LYDIA_GRP.insert_one({'_cid': chat_id})
        ENABLED_CHATS.append(chat_id)
        await message.edit("AI Enabled in Current Chat :D")

    if '-disgrp' in message.flags:
        chat_id = message.chat.id
        if await LYDIA_GRP.find_one_and_delete({'_cid': chat_id}):
            out = "AI Disabled in Current Chat"
            if chat_id in ENABLED_CHATS:
                ENABLED_CHATS.remove(chat_id)
        else:
            out = "AI wasn't enabled in current chat. >:("
        await message.edit(out, del_in=5)

    if '-grps' in message.flags:
        msg = "**AI Enabled Chats**\n\n"
        for chat_id in ENABLED_CHATS:
            chat_ = await userge.get_chat(chat_id)
            title = chat_.title
            msg += f"{title} {chat_id}\n"
        await message.edit_or_send_as_file(msg)

    if '-list' in message.flags:
        msg = "**AI Enabled User List**\n\n"
        for user_id in ACTIVE_USER_LIST:
            u_info = await userge.get_user_dict(user_id)
            u_men = u_info['mention']
            msg += f"{u_men}\n"
        await message.edit_or_send_as_file(msg)

    if '-info' in message.flags:
        await message.reply_photo(photo="resources/lydia.jpg", caption=LYDIA_API_INFO)
    if not message.flags:
        await message.reply_sticker("CAADAQAEAQAC0rXRRju3sbCT07jIFgQ")


@userge.on_filters(~Filters.me & (Filters.mentioned | Filters.private))
async def lydia_ai_chat(message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    async for active_ in LYDIA_SESSION.find():
        if (user_id in ACTIVE_USER_LIST) or (chat_id in ENABLED_CHATS):
            if message.media:
                await custom_media_reply(message, userge)
            if not message.media:
                ses_id = active_['session_id']
                ses_exp = active_['session_exp']
                mess_text = message.text
                if int(ses_exp) < time():
                    ses = lydia.create_session("en")
                    ses_id = ses.id
                    ses_exp = ses.expires
                    await LYDIA_SESSION.find_one_and_update(
                        {'uid': "LYDIA_SES"},
                        {"$set": {'session_id': ses_id, 'session_exp': ses_exp}})
                try:
                    output_ = lydia.think_thought(ses_id, mess_text)
                    await message.reply_chat_action("typing")
                    await asyncio.sleep(7)
                    await message.reply_chat_action("typing")
                    await asyncio.sleep(2)
                    await message.reply_chat_action("cancel")
                    await message.reply(output_)
                except CoffeeHouseError:
                    pass
    message.continue_propagation()
