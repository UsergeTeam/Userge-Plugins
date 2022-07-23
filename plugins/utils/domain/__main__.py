""" see all group and channels """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.


from pyrogram.errors import UserNotParticipant, ChannelPrivate
from pyrogram import enums

from userge import userge, Message


@userge.on_cmd(
    "domain",
    about={
        "header": "Your Domain",
        "flags": {
            "-c": "List all groups and channels created by you.",
            "-a": "List all groups and channels administered by you.",
        },
    },
    allow_via_bot=False
)
async def creator(m: Message):

    await m.edit("__This may take a while, please wait ...__")

    if "-c" in m.flags:
        status = enums.ChatMemberStatus.OWNER
    elif "-a" in m.flags:
        status = enums.ChatMemberStatus.ADMINISTRATOR
    else:
        await m.err("Invalid flag!")
        return

    c_str = ""
    g_str = ""
    c_n = 0
    g_n = 0

    async for d in userge.get_dialogs():
        if d.chat.type in [
            enums.ChatType.GROUP,
            enums.ChatType.SUPERGROUP,
                enums.ChatType.CHANNEL]:
            try:
                if (
                    await userge.get_chat_member(d.chat.id, m.client.id)
                ).status == status:
                    if d.chat.username:
                        c = (
                            f"[{d.chat.title}](https://t.me/{d.chat.username})\n"
                            + "  "
                            + "**Privacy**: __public__"
                            + " | "
                            + f"**Chat ID**: `{d.chat.id}`"
                        )
                    else:
                        i_l = (await userge.get_chat(d.chat.id)).invite_link
                        c = (
                            f"[{d.chat.title}]({i_l})\n"
                            + "  "
                            + "**Privacy**: __private__"
                            + " | "
                            + f"**Chat ID**: `{d.chat.id}`"
                        )
                    if d.chat.type == enums.ChatType.CHANNEL:
                        c_n += 1
                        c_str += f"{c_n}. {c}\n"
                    else:
                        g_n += 1
                        g_str += f"{g_n}. {c}\n"
            except (UserNotParticipant, ChannelPrivate):
                continue

    await m.edit(
        f"<u>**GROUPS**</u> __({status})__:\n"
        + ("(__None__)" if not g_str else g_str)
        + f"\n<u>**CHANNELS**</u> __({status})__:\n"
        + ("(__None__)" if not c_str else c_str)
    )


@userge.on_cmd("stats",
               about="Shows user account stats!",
               allow_via_bot=False)
async def stats(message: Message):
    await message.edit("Processing ...This may take a bit time")
    u = 0
    g = 0
    sg = 0
    c = 0
    b = 0
    a_chat = 0
    async for dialog in userge.get_dialogs():
        if dialog.chat.type == enums.ChatType.PRIVATE:
            u += 1
        elif dialog.chat.type == enums.ChatType.BOT:
            b += 1
        elif dialog.chat.type == enums.ChatType.GROUP:
            g += 1
        elif dialog.chat.type == enums.ChatType.SUPERGROUP:
            sg += 1
            user_s = await dialog.chat.get_member(int(message.client.id))
            if user_s.status in (
                    enums.ChatMemberStatus.OWNER,
                    enums.ChatMemberStatus.ADMINISTRATOR):
                a_chat += 1
        elif dialog.chat.type == enums.ChatType.CHANNEL:
            c += 1
    await message.edit(f'''
You have `{u}` Private Messages.
You are in `{g}` Groups.
You are in `{sg}` Super Groups.
You Are in `{c}` Channels.
You Are Admin in `{a_chat}` Chats.
Bots Started = `{b}`
''')
