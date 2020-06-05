""" AI chatbot """

# AI Chat Bot Module for @theUserge.
# Lydia AI Powered by CoffeeHouse from Intellivoid (Telegram: t.me/Intellivoid)
# Author: Phyco-Ninja (https://github.com/Phyco-Ninja) (@PhycoNinja13b)
# Thanks to @Intellivoid For Creating CoffeeHouse API


import os
import random
import asyncio
# from time import time

from coffeehouse.lydia import LydiaAI
from coffeehouse.api import API
from coffeehouse.exception import CoffeeHouseError

from userge import userge, get_collection, Message, Filters, Config


LYDIA_CHATS = get_collection("LYDIA_CHATS")
CH_LYDIA_API = os.environ.get("CH_LYDIA_API", None)
CUSTOM_REPLY_CHANNEL = int(os.environ.get("CUSTOM_REPLY_CHANNEL", 0))
if CH_LYDIA_API is not None:
    LYDIA = LydiaAI(API(CH_LYDIA_API))

ACTIVE_CHATS = {}
CUSTOM_REPLIES = []

LYDIA_API_INFO = """This module uses Lydia AI
Powered by CoffeeHouse API created by @Intellivoid.

Lydia is a Active Machine Learning Chat Bot.
Which can adapt to current user and chat with user
on any given topic. """


async def _init():
    async for chat in LYDIA_CHATS.find({'active': True}):
        ACTIVE_CHATS[chat['_id']] = (chat['session_id'], chat['session_exp'])
    if CUSTOM_REPLY_CHANNEL:
        async for message in userge.iter_history(chat_id=CUSTOM_REPLY_CHANNEL, limit=300):
            CUSTOM_REPLIES.append(message)


# A workaround for replies of Media as per now Lydia can't process Media input,
# And it's logical though. So this func will call custom message input by user
# saved in a channel and reply it to message.
# Idea arised from here (https://t.me/usergeot/157629) thnx 👍
async def custom_media_reply(message: Message):
    global CUSTOM_REPLIES
    if CUSTOM_REPLIES:
        cus_msg = random.choice(CUSTOM_REPLIES)
        replied = message.message_id
        if cus_msg.media:
            if cus_msg.sticker:
                await message.reply_sticker(cus_msg.sticker.file_id)
            if (cus_msg.photo or cus_msg.video or cus_msg.animation):
                dls = await userge.download_media(message=cus_msg, file_name=Config.DOWN_PATH)
                if cus_msg.photo:
                    await message.reply_photo(dls)
                if cus_msg.video:
                    await message.reply_video(dls)
                if cus_msg.animation:
                    await userge.send_animation(
                        chat_id=message.chat.id,
                        animation=dls,
                        unsave=True,
                        reply_to_message_id=replied
                    )
                os.remove(dls)
        if cus_msg.text:
            await message.reply(cus_msg.text)


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
    if CH_LYDIA_API is None:
        await message.edit(
            "Please Configure `CH_LYDIA_API` & `CUSTOM_REPLY_CHANNEL`"
            "\n\nAll Instructions are available"
            " in @UnofficialPluginsHelp")
        return

    replied = message.reply_to_message
    if '-on' in message.flags and replied:
        user_id = replied.from_user.id
        if user_id in ACTIVE_CHATS:
            await message.edit("AI is already Enabled on Replied User")
            return
        data = await LYDIA_CHATS.find_one({'_id': user_id})
        if not data:
            await message.edit("`creating new session...`")
            ses = LYDIA.create_session("en")
            await LYDIA_CHATS.insert_one(
                {'_id': user_id, 'session_id': ses.id, 'session_exp': ses.expires, 'active': True})
            ACTIVE_CHATS[user_id] = (ses.id, ses.expires)
        else:
            await message.edit("`activating session...`")
            await LYDIA_CHATS.update_one({'_id': user_id}, {'active': True})
            ACTIVE_CHATS[user_id] = (data['session_id'], data['session_exp'])
        await message.edit("`AI Enabled for Replied User`", del_in=2)

    elif '-off' in message.flags and replied:
        user_id = replied.from_user.id
        if user_id not in ACTIVE_CHATS:
            await message.edit("How to delete a thing that doesn't Exist?", del_in=5)
            return
        await message.edit("`disactivating session...`")
        await LYDIA_CHATS.update_one({'_id': user_id}, {'active': False})
        del ACTIVE_CHATS[user_id]
        await message.edit("`AI Disable for Replied User`", del_in=5)

    # Group Features Won't be displayed in Help Info For Now 😉
    elif '-enagrp' in message.flags:
        chat_id = message.chat.id
        if chat_id in ACTIVE_CHATS:
            await message.edit("AI is already Enabled on this chat")
            return
        data = await LYDIA_CHATS.find_one({'_id': chat_id})
        if not data:
            await message.edit("`creating new session...`")
            ses = LYDIA.create_session("en")
            await LYDIA_CHATS.insert_one(
                {'_id': chat_id, 'session_id': ses.id, 'session_exp': ses.expires, 'active': True})
            ACTIVE_CHATS[chat_id] = (ses.id, ses.expires)
        else:
            await message.edit("`activating session...`")
            await LYDIA_CHATS.update_one({'_id': chat_id}, {'active': True})
            ACTIVE_CHATS[chat_id] = (data['session_id'], data['session_exp'])
        await message.edit("`AI Enabled in Current Chat :D`")

    elif '-disgrp' in message.flags:
        chat_id = message.chat.id
        if chat_id not in ACTIVE_CHATS:
            await message.edit("AI wasn't enabled in current chat. >:(", del_in=5)
            return
        await message.edit("`disactivating session...`")
        await LYDIA_CHATS.update_one({'_id': chat_id}, {'active': False})
        del ACTIVE_CHATS[chat_id]
        await message.edit("`AI Disabled in Current Chat`", del_in=5)

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
            u_info = await userge.get_user_dict(user_id)
            u_men = u_info['mention']
            msg += f"{u_men}\n"
        await message.edit_or_send_as_file(msg)

    elif '-info' in message.flags:
        await message.reply_photo(photo="resources/lydia.jpg", caption=LYDIA_API_INFO)
    else:
        await message.reply_sticker("CAADAQAEAQAC0rXRRju3sbCT07jIFgQ")


@userge.on_filters(~Filters.me & (Filters.mentioned | Filters.private))
async def lydia_ai_chat(message: Message):
    """ incomming message handler """
    if CH_LYDIA_API is None:
        return
    data = ACTIVE_CHATS.get(message.from_user.id, None) or ACTIVE_CHATS.get(message.chat.id, None)
    if data:
        if message.media:
            await custom_media_reply(message)
        else:
            ses = LYDIA.get_session(data[0])
            mess_text = message.text
            # if int(ses_exp) < time():
            #     ses = lydia.create_session("en")
            #     ses_id = ses.id
            #     ses_exp = ses.expires
            #     await LYDIA_SESSION.find_one_and_update(
            #         {'uid': "LYDIA_SES"},
            #         {"$set": {'session_id': ses_id, 'session_exp': ses_exp}})
            try:
                output_ = LYDIA.think_thought(ses.id, mess_text)
                await message.reply_chat_action("typing")
                await asyncio.sleep(7)
                await message.reply_chat_action("typing")
                await asyncio.sleep(2)
                await message.reply_chat_action("cancel")
                await message.reply(output_)
            except CoffeeHouseError:
                pass
    message.continue_propagation()
