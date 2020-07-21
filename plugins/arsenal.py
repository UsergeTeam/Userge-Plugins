import time
import asyncio

from userge import userge, Message


@userge.on_cmd("benall", about={
    'header': "Ban All",
    'description': "Bans All Members of a SuperGroup",
    'usage': "{tr}benall"}, allow_private=False, only_admins=True)
async def ban_all(message: Message):
    chat = message.chat.id
    ben_c = 0
    await message.edit("Hold on Trying to ban all Members")
    async for to_ban in message.client.iter_chat_members(chat):
        user = to_ban.user.id
        await message.client.kick_chat_member(chat, user)
        ben_c += 1
        await asyncio.sleep(0.5)
    await message.edit(f"Banned {ben_c} members in {message.chat.title}")


@userge.on_cmd("keckall", about={
    'header': "Kick All",
    'description': "Kicks All Members of a SuperGroup",
    'usage': "{tr}keckall"}, allow_private=False, only_admins=True)
async def keck_all(message: Message):
    chat = message.chat.id
    keck_c = 0
    await message.edit("Hold on Trying to kick all Members")
    async for to_kick in message.client.iter_chat_members(chat):
        user = to_kick.user.id
        await message.client.kick_chat_member(chat, user, int(time.time() + 60))
        keck_c += 1
        await asyncio.sleep(0.5)
    await message.edit(f"Kicked {keck_c} members in {message.chat.title}")
