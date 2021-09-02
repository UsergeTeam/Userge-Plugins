from userge import userge, Message
from pyrogram.errors import UserNotParticipant, ChannelPrivate


@userge.on_cmd(
    "domain",
    about={
        "header": "Your Domain",
        "flags": {
            "-c": "List all gropus and channels created by you.",
            "-a": "List all gropus and channels administered by you.",
        },
    },
)
async def creator(m: Message):

    await m.edit("__This may take a while, please wait ...__")

    if "-c" in m.input_str:
        status = "creator"
    elif "-a" in m.input_str:
        status = "administrator"
    else:
        await m.err("Invalid flag!")
        return

    c_str = ""
    g_str = ""
    c_n = 0
    g_n = 0

    async for dialog in m.client.iter_dialogs():
        if dialog.chat.type in ["group", "supergroup", "channel"]:
            try:
                if (
                    await m.client.get_chat_member(dialog.chat.id, m.client.id)
                ).status == status:
                    if dialog.chat.username:
                        c = (
                            f"[{dialog.chat.title}](https://t.me/{dialog.chat.username})\n"
                            + "  "
                            + "**Privacy**: __public__"
                            + " | "
                            + f"**Chat ID**: `{dialog.chat.id}`"
                        )
                    else:
                        c = (
                            f"[{dialog.chat.title}]({(await m.client.get_chat(dialog.chat.id)).invite_link})\n"
                            + "  "
                            + "**Privacy**: __private__"
                            + " | "
                            + f"**Chat ID**: `{dialog.chat.id}`"
                        )
                    if dialog.chat.type == "channel":
                        c_n += 1
                        c_str += f"{c_n}. {c}\n"
                    else:
                        g_n += 1
                        g_str += f"{g_n}. {c}\n"
            except UserNotParticipant or ChannelPrivate:
                continue

    await m.edit(
        f"<u>**GROUPS**</u> __({status})__:\n"
        + ("(__None__)" if not g_str else g_str)
        + f"\n<u>**CHANNELS**</u> __({status})__:\n"
        + ("(__None__)" if not c_str else c_str)
    )
