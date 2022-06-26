""" self destructable message """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
from userge import userge, Message
from pyrogram.raw.types import (
    UpdateReadChannelOutbox,
    UpdateReadHistoryOutbox,
    PeerUser,
    PeerChannel)
from pyrogram.raw.base import Update, Peer
from pyrogram import ContinuePropagation
from pyrogram import enums

MSGS = {}


@userge.on_cmd("sd (?:(\\d+)?\\s?(.+))", about={
    'header': "make self-destructable messages",
    'usage': "{tr}sd [test]\n{tr}sd [timeout in seconds] [text]"})
async def selfdestruct(message: Message):
    seconds = int(message.matches[0].group(1) or 10)
    text = str(message.matches[0].group(2))
    if message.client.is_bot:
        if message.chat.type == enums.ChatType.PRIVATE:
            return await message.edit(text=text, del_in=seconds)
    else:
        if message.chat.type == enums.ChatType.BOT or message.chat.id == message.from_user.id:
            return await message.edit(text=text, del_in=seconds)
    msg = await message.edit(text=text)

    MSGS[msg.chat.id] = MSGS.get(msg.chat.id, []) + \
        [{'msg': msg.id, 'del_in': seconds}]


@userge.on_raw_update(group=-2)
async def raw_handler(_, update: Update, *__):
    if isinstance(update, (UpdateReadChannelOutbox, UpdateReadHistoryOutbox)):
        chat_id = get_chat_id(getattr(update, 'peer', None)) or int(
            '-100' + str(getattr(update, 'channel_id', 0)))
        msgs = MSGS.get(chat_id)
        if msgs:
            MSGS[chat_id] = []  # clear the fetched list
            msg_ids = list(filter(lambda _: _['msg'] <= update.max_id, msgs))
            del_in_time = set()
            for msg_dict in msg_ids:
                msgs.remove(msg_dict)
                if msg_dict['del_in'] not in del_in_time:
                    del_in_time.add(msg_dict['del_in'])
            MSGS[chat_id] += msgs  # re-adding unread msgs
            old_sleep = 0
            for sec in del_in_time:
                await asyncio.sleep(sec - old_sleep)
                msg_list = [msg_dict['msg']
                            for msg_dict in msg_ids if msg_dict['del_in'] == sec]
                await userge.delete_messages(chat_id, msg_list)
                old_sleep = sec
    raise ContinuePropagation


def get_chat_id(peer: Peer) -> int:
    if not peer:
        return None
    if isinstance(peer, PeerChannel):
        chat_id = int('-100' + str(peer.channel_id))
    elif isinstance(peer, PeerUser):
        chat_id = peer.user_id
    else:
        chat_id = peer.chat_id
    return chat_id
