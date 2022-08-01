""" setup gban """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved

import asyncio
from typing import AsyncGenerator, Tuple

from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired, UserAdminInvalid, ChannelInvalid)
from pyrogram import enums

from userge import userge, Message, get_collection
from .. import gban
from ...builtin import sudo

GBAN_USER_BASE = get_collection("GBAN_USER")
WHITELIST = get_collection("WHITELIST_USER")
CHANNEL = userge.getCLogger(__name__)
LOG = userge.getLogger(__name__)


@userge.on_start
async def _init() -> None:
    async for i in WHITELIST.find():
        gban.WHITE_CACHE[int(i['user_id'])] = i['firstname']


async def _add_whitelist(firstname: str, user_id: int) -> None:
    gban.WHITE_CACHE[user_id] = firstname
    await WHITELIST.insert_one({'firstname': firstname, 'user_id': user_id})


async def _remove_whitelist(user_id: int) -> None:
    del gban.WHITE_CACHE[user_id]
    await WHITELIST.delete_one({'user_id': user_id})


async def _iter_whitelist() -> AsyncGenerator[Tuple[int, str], None]:
    for _ in gban.WHITE_CACHE.items():
        yield _


@userge.on_cmd("gban", about={
    'header': "Global Ban Pengguna",
    'description': "Menambahkan Pengguna ke Daftar GBan Anda. "
                   "Banned pengguna yang Dicekal Secara Global jika mereka bergabung atau mengirim pesan. "
                   "[CATATAN: Hanya berfungsi di grup tempat Anda menjadi admin.]",
    'examples': "{tr}gban [id user | balas pesan] [alasan di gban] (mandatory)"},
    allow_channels=False, allow_bots=False)
async def gban_user(message: Message):
    """ ban pengguna secara global """
    await message.edit("`Proses Gban...`")
    user_id, reason = message.extract_user_and_text
    if not user_id:
        await message.err("user_id tidak valid atau pesan yang ditentukan")
        return
    get_mem = await message.client.get_user_dict(user_id)
    firstname = get_mem['fname']
    if not reason:
        await message.edit(
            f"**#Aborted**\n\n**Gbanning** of [{firstname}](tg://user?id={user_id}) "
            "Aborted coz No reason of gban provided by banner", del_in=5)
        return
    user_id = get_mem['id']
    if user_id == message.client.id:
        await message.edit(r"Blok. Ngapain gban gw sendiri ¯\(°_o)/¯")
        return
    if user_id in sudo.USERS:
        await message.edit(
            "Pengguna itu ada di daftar sudo, Aku tidak bisa ban dia.\n\n"
            "**Tips:** Hapus dia dari Daftar Sudo dan coba lagi. (¬_¬)", del_in=5)
        return
    found = await GBAN_USER_BASE.find_one({'user_id': user_id})
    if found:
        await message.edit(
            "**#Already_GBanned**\n\nPengguna sudah ada di daftar GBan saya.\n"
            f"**Alasan GBan:** `{found['reason']}`", del_in=5)
        return
    await message.edit(r"\\**#GBanned_User**//"
                       f"\n\n**Nama depan:** [{firstname}](tg://user?id={user_id})\n"
                       f"**ID pengguna:** `{user_id}`\n**Alasan:** `{reason}`")
    # TODO: can we add something like "GBanned by {any_sudo_user_fname}"
    if message.client.is_bot:
        chats = [message.chat]
    else:
        chats = await message.client.get_common_chats(user_id)
    gbanned_chats = []
    for chat in chats:
        try:
            await chat.ban_member(user_id)
            gbanned_chats.append(chat.id)
            await CHANNEL.log(
                r"\\**#Antispam_Log**//"
                f"\n**Pengguna:** [{firstname}](tg://user?id={user_id})\n"
                f"**ID pengguna:** `{user_id}`\n"
                f"**Obrolan:** {chat.title}\n"
                f"**ID Obrolan:** `{chat.id}`\n"
                f"**Alasan:** `{reason}`\n\n$GBAN #id{user_id}")
        except (ChatAdminRequired, UserAdminInvalid, ChannelInvalid):
            pass
    await GBAN_USER_BASE.insert_one({'firstname': firstname,
                                     'user_id': user_id,
                                     'reason': reason,
                                     'chat_ids': gbanned_chats})
    if gban.FBAN_CHAT_ID and not message.client.is_bot:
        mention = None  # to avoid peer id invalid
        if message.reply_to_message and message.reply_to_message.from_user:
            mention = message.reply_to_message.from_user.mention
        elif message.entities:
            for i in message.entities:
                if i.type == enums.MessageEntityType.TEXT_MENTION:
                    mention = i.user.mention
                    break
        if mention:
            await message.client.send_message(
                gban.FBAN_CHAT_ID,
                f"/fban {mention} {reason}"
            )
            await CHANNEL.log(f'$FBAN #prid{user_id} ⬆️')
    replied = message.reply_to_message
    if replied:
        if replied.text:
            await CHANNEL.fwd_msg(replied)
        await CHANNEL.log(f'$GBAN #prid{user_id} ⬆️')
    LOG.info("G-Banned %s", str(user_id))


@userge.on_cmd("ungban", about={
    'header': "Lepas ban global pengguna",
    'description': "Menghapus pengguna dari Daftar Gban Anda",
    'examples': "{tr}ungban [id pengguna | balas pesan]"},
    allow_channels=False, allow_bots=False)
async def ungban_user(message: Message):
    """ unban global pengguna """
    await message.edit("`UnGBanning...`")
    user_id, _ = message.extract_user_and_text
    if not user_id:
        await message.err("user-id tidak ditemukan")
        return
    get_mem = await message.client.get_user_dict(user_id)
    firstname = get_mem['fname']
    user_id = get_mem['id']
    found = await GBAN_USER_BASE.find_one({'user_id': user_id})
    if not found:
        await message.edit("`Pengguna Tidak Ditemukan di Daftar Gban Saya`", del_in=5)
        return
    if 'chat_ids' in found:
        for chat_id in found['chat_ids']:
            try:
                await userge.unban_chat_member(chat_id, user_id)
                await CHANNEL.log(
                    r"\\**#Antispam_Log**//"
                    f"\n**Pengguna:** [{firstname}](tg://user?id={user_id})\n"
                    f"**ID pengguna:** `{user_id}`\n\n"
                    f"$UNGBAN #id{user_id}")
            except (ChatAdminRequired, UserAdminInvalid, ChannelInvalid):
                pass
    await message.edit(r"\\**#UnGbanned_User**//"
                       f"\n\n**Nama depan:** [{firstname}](tg://user?id={user_id})\n"
                       f"**ID pengguna:** `{user_id}`")
    await GBAN_USER_BASE.delete_one({'firstname': firstname, 'user_id': user_id})
    if gban.FBAN_CHAT_ID and not message.client.is_bot:
        mention = None  # to avoid peer id invalid
        if message.reply_to_message and message.reply_to_message.from_user:
            mention = message.reply_to_message.from_user.mention
        elif message.entities:
            for i in message.entities:
                if i.type == enums.MessageEntityType.TEXT_MENTION:
                    mention = i.user.mention
                    break
        if mention:
            await message.client.send_message(
                gban.FBAN_CHAT_ID,
                f"/unfban {mention}"
            )
            await CHANNEL.log(f'$UNFBAN #prid{user_id} ⬆️')
    LOG.info("UnGbanned %s", str(user_id))


@userge.on_cmd("glist", about={
    'header': "Dapatkan Daftar Pengguna yang Di-GBan",
    'description': "Dapatkan daftar pengguna terbaru yang diblokir oleh Anda.",
    'examples': "Blok. Hanya ketik {tr}glist"},
    allow_channels=False)
async def list_gbanned(message: Message):
    """ vies gbanned users """
    msg = ''
    async for c in GBAN_USER_BASE.find():
        msg += ("**Pengguna** : " + str(c['firstname']) + "-> **ID** : "
                + str(c['user_id']) + " is **GBan karena** : " + str(c.get('reason')) + "\n\n")
    await message.edit_or_send_as_file(
        f"**--Daftar Pengguna yang Di-GBan Secara Global--**\n\n{msg}" if msg else "`glist kosong!`")


@userge.on_cmd("whitelist", about={
    'header': "Daftar Putih Pengguna",
    'description': "Gunakan daftar putih untuk menambahkan pengguna untuk melewati banned",
    'usage': "{tr}whitelist [id user | balas pesan pengguna]",
    'examples': "{tr}whitelist 5231147869"},
    allow_channels=False, allow_bots=False)
async def whitelist(message: Message):
    """ tambahkan pengguna ke daftar putih """
    user_id, _ = message.extract_user_and_text
    if not user_id:
        await message.err("user-id tidak ditemukan")
        return
    get_mem = await message.client.get_user_dict(user_id)
    firstname = get_mem['fname']
    user_id = int(get_mem['id'])
    found = await gban.is_whitelist(user_id)
    if found:
        await message.edit("`Pengguna Sudah di Daftar Putih Saya`", del_in=5)
        return
    await asyncio.gather(
        _add_whitelist(firstname, user_id),
        message.edit(
            r"\\**#Whitelisted_User**//"
            f"\n\n**Nama depan:** [{firstname}](tg://user?id={user_id})\n"
            f"**ID pengguna:** `{user_id}`"),
        CHANNEL.log(
            r"\\**#Antispam_Log**//"
            f"\n**Pengguna:** [{firstname}](tg://user?id={user_id})\n"
            f"**ID pengguna:** `{user_id}`\n"
            f"**Chat:** {message.chat.title}\n"
            f"**ID obrolan:** `{message.chat.id}`\n\n$WHITELISTED #id{user_id}")
    )
    LOG.info("WhiteListed %s", str(user_id))


@userge.on_cmd("rmwhite", about={
    'header': "Menghapus Pengguna dari Daftar Putih",
    'description': "Gunakan untuk menghapus pengguna dari Daftar Putih",
    'useage': "{tr}rmwhite [id pengguna | balas pesan pengguna]",
    'examples': "{tr}rmwhite 5231147869"},
    allow_channels=False, allow_bots=False)
async def rmwhitelist(message: Message):
    """ hapus pengguna dari daftar putih """
    user_id, _ = message.extract_user_and_text
    if not user_id:
        await message.err("user-id tidak ditemukan")
        return
    get_mem = await message.client.get_user_dict(user_id)
    firstname = get_mem['fname']
    user_id = int(get_mem['id'])
    found = await gban.is_whitelist(user_id)
    if not found:
        await message.edit("`Pengguna Tidak Ditemukan di Daftar Putih Saya`", del_in=5)
        return
    await asyncio.gather(
        _remove_whitelist(user_id),
        message.edit(
            r"\\**#Removed_Whitelisted_User**//"
            f"\n\n**Nama depan:** [{firstname}](tg://user?id={user_id})\n"
            f"**ID pengguna:** `{user_id}`"),
        CHANNEL.log(
            r"\\**#Antispam_Log**//"
            f"\n**Pengguna:** [{firstname}](tg://user?id={user_id})\n"
            f"**ID pengguna:** `{user_id}`\n"
            f"**Obrolan:** {message.chat.title}\n"
            f"**ID Obrolan:** `{message.chat.id}`\n\n$RMWHITELISTED #id{user_id}")
    )
    LOG.info("WhiteListed %s", str(user_id))


@userge.on_cmd("listwhite", about={
    'header': "Dapatkan Daftar Pengguna yang Masuk Daftar Putih",
    'description': "Dapatkan daftar pengguna terbaru yang masuk Daftar Putih oleh Anda.",
    'examples': "Blok. Hanya ketik {tr}listwhite"},
    allow_channels=False)
async def list_white(message: Message):
    """ list whitelist """
    msg = ''
    async for user_id, firstname in _iter_whitelist():
        msg += f"**Pengguna** : {firstname} -> **ID** : {user_id}\n"
    await message.edit_or_send_as_file(
        f"**--Daftar Pengguna yang Masuk Daftar Putih--**\n\n{msg}" if msg else "`daftar putih kosong!`")
