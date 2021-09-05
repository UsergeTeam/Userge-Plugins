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

    if "-c" in m.flags:
        status = "creator"
    elif "-a" in m.flags:
        status = "administrator"
    else:
        await m.err("Invalid flag!")
        return

    c_str = ""
    g_str = ""
    c_n = 0
    g_n = 0

    async for d in m.client.iter_dialogs():
        if d.chat.type in ["group", "supergroup", "channel"]:
            try:
                if (
                    await m.client.get_chat_member(d.chat.id, m.client.id)
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
                        i_l = (await m.client.get_chat(d.chat.id)).invite_link
                        c = (
                            f"[{d.chat.title}]({i_l})\n"
                            + "  "
                            + "**Privacy**: __private__"
                            + " | "
                            + f"**Chat ID**: `{d.chat.id}`"
                        )
                    if d.chat.type == "channel":
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
