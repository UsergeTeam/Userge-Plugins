# Plugin by @Krishna_Singhal

from pyrogram.raw import functions
from pyrogram.errors import PeerIdInvalid

from userge import userge, Message


@userge.on_cmd("markread", about={
    'header': "Mark read all chats.",
    'usage': "{tr}markread"},
    allow_via_bot=False, allow_channels=False
)
async def mark_read(msg: Message):
    await msg.edit("Processing...")
    total = 0
    failed = 0

    chats = await userge.send(
        functions.messages.GetAllChats(except_ids=[])
    )
    for i in chats.chats:
        total += 1
        try:
            await userge.read_history(chat_id=i.id)
        except PeerIdInvalid:
            failed += 1
    await msg.edit(f"Marked {total - failed} chats as read from {total}")
