"""
Chat info, Join and leave chat, tagall and tag admins

by @Krishna_Singhal
"""

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
import html
import os

from pyrogram.errors.exceptions.bad_request_400 import (
    BadRequest,
    UsernameOccupied,
    UsernameInvalid,
    UsernameNotOccupied,
    PeerIdInvalid)
from pyrogram import enums

from userge import userge, config, Message

LOG = userge.getLogger(__name__)

PATH = config.Dynamic.DOWN_PATH + "chat_pic.jpg"


def mention_html(user_id, name):
    return u'<a href="tg://user?id={}">{}</a>'.format(
        user_id, html.escape(name))


@userge.on_cmd("join", about={
    'header': "Join chat",
    'usage': "{tr}join [chat username | reply to Chat username Text]",
    'examples': "{tr}join UserGeOt"})
async def join_chat(message: Message):
    """ Join chat """
    replied = message.reply_to_message
    if replied:
        text = replied.text
    else:
        text = message.input_str
    if not text:
        await message.edit(
            "```Bruh, Without chat name, I can't Join... :0```", del_in=3)
        return
    try:
        chat = await userge.get_chat(text)
        await userge.join_chat(text)
        await userge.send_message(text, f"```Joined {chat.title} Successfully...```")
    except UsernameNotOccupied:
        await message.edit("```Username, you entered, does not exist... ```", del_in=3)
        return
    except PeerIdInvalid:
        await message.edit("```Chat id, you entered, does not exist... ```", del_in=3)
        return
    else:
        await message.delete()
        await asyncio.sleep(2)


@userge.on_cmd("leave",
               about={'header': "Leave Chat",
                      'usage': "{tr}leave\n{tr}leave [chat username | reply to Chat username text]",
                      'examples': "{tr}leave"},
               allow_private=False)
async def leave_chat(message: Message):
    """ Leave chat """
    await message.edit("`Good bye, Cruel World... :-) `")
    await userge.leave_chat(message.chat.id)


@userge.on_cmd("invite", about={
    'header': "Generate chat Invite link",
    'usage': "{tr}invite\n{tr}invite [Chat Id | Chat Username]"},
    allow_channels=False, allow_private=False)
async def invite_link(message: Message):
    """ Generate invite link """
    chat_id = message.chat.id
    user_id = message.input_str
    if not user_id and message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    if not user_id:
        try:
            chat = await userge.get_chat(chat_id)
            chat_name = chat.title
            if chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                link = await userge.export_chat_invite_link(chat_id)
                await message.edit(
                    "**Invite link Generated Successfully for\n"
                    f"{chat_name}**\n[Click here to join]({link})",
                    disable_web_page_preview=True)
            else:
                await message.err("Requirements doesn't met...")
        except Exception as e_f:
            await message.err(e_f)
    else:
        try:
            await userge.add_chat_members(chat_id, user_id)
            await message.edit("`Invited Successfully...`")
        except Exception as e_f:
            await message.err(e_f)


@userge.on_cmd("tagall", about={
    'header': "Tagall recent 100 members with caption",
    'usage': "{tr}tagall [Text | reply to text Msg]"},
    allow_via_bot=False, allow_private=False, only_admins=True)
async def tagall_(message: Message):
    """ Tag recent members """
    replied = message.reply_to_message
    text = message.input_str
    if not (text or replied):
        await message.err("Without any reason, I will not tag Members...(=_=)")
        return
    c_title = message.chat.title
    c_id = message.chat.id
    await message.edit(f"`Tagging recent members in {c_title}...`")
    text = f"**{text}**\n" if text else ""
    message_id = replied.id if replied else None
    try:
        async for members in message.client.get_chat_members(c_id,
                                                             filter=enums.ChatMembersFilter.RECENT):
            if not members.user.is_bot:
                u_id = members.user.id
                u_name = members.user.username or None
                f_name = (await message.client.get_user_dict(u_id))['fname']
                if u_name:
                    text += f"@{u_name} "
                else:
                    text += f"[{f_name}](tg://user?id={u_id}) "
    except Exception as e:
        text += " " + str(e)
    await message.client.send_message(c_id, text, reply_to_message_id=message_id)
    await message.edit("```Tagged recent Members Successfully...```", del_in=3)


@userge.on_cmd("stagall", about={
    'header': "Silent tag recent 100 members with caption",
    'usage': "{tr}stagall [Text | reply to text Msg]"},
    allow_private=False, allow_via_bot=False, only_admins=True)
async def stagall_(message: Message):
    """ tag recent members without spam """
    chat_id = message.chat.id
    chat = await userge.get_chat(chat_id)
    await message.edit(f"```Tagging everyone in {chat.title}```")
    replied = message.reply_to_message
    text = message.input_str
    if not (text or replied):
        await message.err("Without any reason, I will not tag Members...(=_=)")
        return
    text = f"`{text}`" if text else ""
    message_id = replied.id if replied else None
    async for members in userge.get_chat_members(chat_id):
        if not members.user.is_bot:
            text += mention_html(members.user.id, "\u200b")
    await message.delete()
    await userge.send_message(
        chat_id, text, reply_to_message_id=message_id)


@userge.on_cmd("tadmins", about={
    'header': "Tag admins in group",
    'usage': "{tr}tadmins [Text | reply to text Msg]"},
    allow_private=False)
async def tadmins_(message: Message):
    """ Tag admins in a group """
    replied = message.reply_to_message
    text = message.input_str
    if not (text or replied):
        await message.err("Without any reason, I will not tag Admins...(=_=)")
        return
    c_title = message.chat.title
    c_id = message.chat.id
    await message.edit(f"```Tagging admins in {c_title}...```")
    text = f"**{text}**\n" if text else ""
    message_id = replied.id if replied else None
    try:
        async for members in message.client.get_chat_members(
                c_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            status = members.status
            u_id = members.user.id
            u_name = members.user.username or None
            f_name = (await message.client.get_user_dict(u_id))['fname']
            if status == enums.ChatMemberStatus.ADMINISTRATOR:
                if u_name:
                    text += f"@{u_name} "
                else:
                    text += f"[{f_name}](tg://user?id={u_id}) "
            elif status == enums.ChatMemberStatus.OWNER:
                if u_name:
                    text += f"@{u_name} "
                else:
                    text += f"[{f_name}](tg://user?id={u_id}) "
    except Exception as e:
        text += " " + str(e)
    await message.client.send_message(c_id, text, reply_to_message_id=message_id)
    await message.edit("```Admins tagged Successfully...```", del_in=3)


@userge.on_cmd("schat", about={
    'header': "Update and delete chat info",
    'flags': {
        '-title': "update chat title",
        '-uname': "update chat username",
        '-des': "update chat description",
        '-ddes': "delete chat description"},
    'usage': "{tr}schat [flag]\n"
             "{tr}schat [flags] [input]"},
    allow_via_bot=False, allow_private=False, only_admins=True)
async def set_chat(message: Message):
    """ Set or delete chat info """
    if not message.flags:
        await message.err("```Flags required!...```", del_in=3)
        return
    chat = await userge.get_chat(message.chat.id)
    if '-ddes' in message.flags:
        if not chat.description:
            await message.edit(
                "```Chat already haven't any description...```", del_in=5)
        else:
            await userge.set_chat_description(message.chat.id, "")
            await message.edit("```Chat Description is Successfully removed...```", del_in=3)
    args = message.filtered_input_str
    if not args:
        await message.edit("```Need Text to Update chat info...```", del_in=5)
        return
    if '-title' in message.flags:
        await userge.set_chat_title(message.chat.id, args.strip())
        await message.edit("```Chat Title is Successfully Updated...```", del_in=3)
    elif '-uname' in message.flags:
        try:
            await userge.set_chat_username(message.chat.id, args.strip())
        except ValueError:
            await message.edit("```I think its a private chat...(^_-)```", del_in=3)
            return
        except UsernameInvalid:
            await message.edit("```Username, you entered, is invalid... ```", del_in=3)
            return
        except UsernameOccupied:
            await message.edit(
                "```Username, you entered, is already Occupied... ```", del_in=3)
            return
        else:
            await message.edit("```Chat Username is Successfully Updated...```", del_in=3)
    elif '-des' in message.flags:
        try:
            await userge.set_chat_description(message.chat.id, args.strip())
        except BadRequest:
            await message.edit(
                "```Chat description is Too Long...  ```", del_in=3)
        else:
            await message.edit("```Chat description is Successfully Updated...```", del_in=3)
    else:
        await message.edit("```Invalid args, Check help...```", del_in=5)


@userge.on_cmd('vchat', about={
    'header': "View Chat",
    'flags': {
        '-title': "Print chat title",
        '-uname': "Print chat user name",
        '-des': "Print chat description"},
    'usage': [
        "{tr}vchat [flags]",
        "{tr}vchat : upload chat photo"]},
    allow_private=False)
async def view_chat(message: Message):
    """ View chat info """
    chat_id = message.chat.id
    chat = await userge.get_chat(chat_id)
    if '-title' in message.flags:
        await message.edit("```Checking, wait plox !...```", del_in=3)
        title = chat.title
        await message.edit("<code>{}</code>".format(title), parse_mode=enums.ParseMode.HTML)
    elif '-uname' in message.flags:
        if not chat.username:
            await message.err("```I think its private chat !...( ･ิω･ิ)```", del_in=3)
        else:
            await message.edit("```Checking, wait plox !...```", del_in=3)
            uname = chat.username
            await message.edit("<code>{}</code>".format(uname), parse_mode=enums.ParseMode.HTML)
    elif '-des' in message.flags:
        if not chat.description:
            await message.err("```I think, Chat haven't any description...```", del_in=3)
        else:
            await message.edit("```checking, Wait plox !...```", del_in=3)
            await message.edit("<code>{}</code>".format(chat.description),
                               parse_mode=enums.ParseMode.HTML)
    else:
        if not chat.photo:
            await message.err("```Chat haven't any photo... ```", del_in=3)
        else:
            await message.edit("```Checking chat photo, wait plox !...```", del_in=3)
            await message.client.download_media(chat.photo.big_file_id, file_name=PATH)
            await message.client.send_photo(message.chat.id, PATH)
            if os.path.exists(PATH):
                os.remove(PATH)
