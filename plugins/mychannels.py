from userge import userge, Message
from pyrogram.errors import UserNotParticipant, ChannelPrivate


@userge.on_cmd('creator', about="List all gropus and channels created by you.")
async def creator(m: Message):
    await m.edit("__This may take a while, please wait ...__")
    c_list = ""
    g_list = ""
    c_n = 0
    g_n = 0
    async for dialog in m.client.iter_dialogs():
        if dialog.chat.type in ['group', 'supergroup', 'channel']:
            if dialog.chat.is_creator:
                if dialog.chat.username:
                    c = f"[{dialog.chat.title}](https://t.me/{dialog.chat.username}) \
                        (public) [`{dialog.chat.id}`]\n"
                else:
                    c = f"[{dialog.chat.title}]({(await m.client.get_chat(dialog.chat.id)).invite_link}) \
                        (private) [`{dialog.chat.id}`]\n"
                if dialog.chat.type == 'channel':
                    c_n += 1
                    c_list += f"{c_n}. {c}"
                else:
                    g_n += 1
                    g_list += f"{g_n}. {c}"
    await m.edit("<u>**GROUPS**</u> __(creator)__:\n" \
        + ('(__None__)' if not g_list else g_list) \
            + "\n<u>**CHANNELS**</u> __(creator)__:\n" \
                + ('(__None__)' if not c_list else c_list))


@userge.on_cmd('admin', about="List all groups and channels you have administrative privilege on.")
async def admin(m: Message):
    await m.edit("__This may take a while, please wait ...__")
    c_list = ""
    g_list = ""
    c_n = 0
    g_n = 0
    async for dialog in m.client.iter_dialogs():
        if dialog.chat.type in ['group', 'supergroup', 'channel']:
            try:
                status = (await m.client.get_chat_member(dialog.chat.id, m.client.id)).status
                if status == 'administrator':
                    if dialog.chat.username:
                        c = f"[{dialog.chat.title}](https://t.me/{dialog.chat.username}) \
                            (public) [`{dialog.chat.id}`]\n"
                    else:
                        c = f"[{dialog.chat.title}]({(await m.client.get_chat(dialog.chat.id)).invite_link}) \
                            (private) [`{dialog.chat.id}`]\n"
                    if dialog.chat.type == 'channel':
                        c_n += 1
                        c_list += f"{c_n}. {c}"
                    else:
                        g_n += 1
                        g_list += f"{g_n}. {c}"
            except UserNotParticipant or ChannelPrivate:
                continue
    await m.edit("<u>**GROUPS**</u> __(administrator)__:\n" \
        + ('(__None__)' if not g_list else g_list) \
            + "\n<u>**CHANNELS**</u> __(administrator)__:\n" \
                + ('(__None__)' if not c_list else c_list))
