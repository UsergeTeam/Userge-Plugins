""" get user details """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

import os

from pyrogram.errors.exceptions.bad_request_400 import BotMethodInvalid
from pyrogram import enums

from userge import userge, Message


@userge.on_cmd("whois", about={
    'header': "use this to get any user details",
    'usage': "just reply to any user message or add user_id or username",
    'examples': "{tr}whois [user_id | username]"}, allow_channels=False)
async def who_is(message: Message):
    await message.edit("`Mengambil informasi dari Durov...!`")
    user_id = message.input_str
    if user_id:
        try:
            from_user = await message.client.get_users(user_id)
            from_chat = await message.client.get_chat(user_id)
        except Exception:  # pylint: disable=broad-except
            await message.err("no valid user_id or message specified")
            return
    elif message.reply_to_message and message.reply_to_message.from_user:
        from_user = await message.client.get_users(message.reply_to_message.from_user.id)
        from_chat = await message.client.get_chat(message.reply_to_message.from_user.id)
    else:
        await message.err("id tidak valid atau pesan yang ditentukan")
        return
    if from_user or from_chat is not None:
        pp_c = await message.client.get_chat_photos_count(from_user.id)
        message_out_str = "<b>USER INFO:</b>\n\n"
        message_out_str += f"<b>🗣 Nama depan:</b> <code>{from_user.first_name}</code>\n"
        message_out_str += f"<b>🗣 Nama akhir:</b> <code>{from_user.last_name}</code>\n"
        message_out_str += f"<b>👤 Username:</b> @{from_user.username}\n"
        message_out_str += f"<b>🏢 DC ID:</b> <code>{from_user.dc_id}</code>\n"
        message_out_str += f"<b>🤖 Apakah bot:</b> <code>{from_user.is_bot}</code>\n"
        message_out_str += f"<b>🚫 Apakah Dibatasi:</b> <code>{from_user.is_scam}</code>\n"
        message_out_str += "<b>✅ Diverifikasi oleh Telegram:</b> "
        message_out_str += f"<code>{from_user.is_verified}</code>\n"
        message_out_str += f"<b>🕵️‍♂️ ID pengguna:</b> <code>{from_user.id}</code>\n"
        message_out_str += f"<b>🖼 Foto Profil:</b> <code>{pp_c}</code>\n"
        try:
            cc_no = len(await message.client.get_common_chats(from_user.id))
        except BotMethodInvalid:
            pass
        else:
            message_out_str += f"<b>👥 Obrolan Umum:</b> <code>{cc_no}</code>\n"
        message_out_str += f"<b>📝 Bio:</b> <code>{from_chat.bio}</code>\n\n"
        message_out_str += f"<b>👁 Terakhir terlihat:</b> <code>{from_user.status}</code>\n"
        message_out_str += "<b>🔗 Tautan Permanen Ke Profil:</b> "
        message_out_str += f"<a href='tg://user?id={from_user.id}'>{from_user.first_name}</a>"

        s_perm = True
        if message.chat.permissions:
            s_perm = bool(message.chat.permissions.can_send_media_messages)
        if from_user.photo and s_perm:
            local_user_photo = await message.client.download_media(
                message=from_user.photo.big_file_id)
            await message.client.send_photo(chat_id=message.chat.id,
                                            photo=local_user_photo,
                                            caption=message_out_str,
                                            parse_mode=enums.ParseMode.HTML,
                                            disable_notification=True)
            os.remove(local_user_photo)
            await message.delete()
        else:
            cuz = "Chat Send Media Forbidden" if not s_perm else "NO DP Found"
            message_out_str = "<b>📷 " + cuz + " 📷</b>\n\n" + message_out_str
            await message.edit(message_out_str)
