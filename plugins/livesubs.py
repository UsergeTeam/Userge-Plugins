""" Live subs count """

import asyncio

from pyrogram.errors import FloodWait
from userge import userge, Message


@userge.on_cmd("livesubs", about={
    'header': "Live Subscriber count for Public Groups and Channels",
    'usage': "{tr}livesubs [chat id]"})
async def live_subs(msg: Message):
    input_ = msg.input_str
    chat = msg.chat if msg.chat.type != "private" else None
    if input_:
        try:
            chat = await msg.client.get_chat(input_)
        except Exception:
            await msg.err("Chat Id Invalid")
    if chat:
        username = f"@{chat.username}" if chat.username else chat.title
        while True:
            if msg.process_is_canceled:
                await msg.edit("`Live subs request Cancelled`")
                break
            try:
                subs = await msg.client.get_chat_members_count(chat.id)
                await msg.edit(
                    f"**Live Members Count of {username}**\n\n"
                    f"Members = `{subs}`"
                )
                await asyncio.sleep(3)
            except FloodWait as fw:
                await asyncio.sleep(fw.x)
    else:
        await msg.err("chat id required")
