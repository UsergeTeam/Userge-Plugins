""" check user's info """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.


# By @Krishna_Singhal

import json
from typing import Optional

import aiohttp
import spamwatch
from UsergeAntiSpamApi import Client

from pyrogram.types import User
from pyrogram import enums

from userge import userge, Message, get_collection
from .. import info

GBAN_USER_BASE = get_collection("GBAN_USER")
GMUTE_USER_BASE = get_collection("GMUTE_USER")
LOG = userge.getLogger(__name__)


@userge.on_cmd("info", about={
    'header': "To check User's info",
    'usage': "{tr}info [for own info]\n"
             "{tr}info [Username | User Id]\n"
             "{tr}info [reply to User]"}, allow_via_bot=False)
async def _info(msg: Message):
    """ To check User's info """
    await msg.edit("`Checking...`")
    user_id = msg.input_str
    replied = msg.reply_to_message
    if not user_id:
        if replied:
            user_id = replied.forward_from.id if replied.forward_from else replied.from_user.id
        else:
            user_id = msg.from_user.id
    try:
        user = await msg.client.get_users(user_id)
    except Exception:
        await msg.edit("I don't know that User...")
        return
    await msg.edit("`Getting Info...`")
    l_name = user.last_name or ''
    if user.username:
        username = '@' + user.username
    else:
        username = '`None`'
    common_chats = await msg.client.get_common_chats(user.id)
    user_info = f"""
**About [{user.first_name} {l_name}](tg://user?id={user.id})**:
  - **UserID**: `{user.id}`
  - **Data Center**: `{user.dc_id}`
  - **Username**: {username}
  - **Last Online**: `{last_online(user)}`
  - **Common Groups**: `{len(common_chats)}`
  - **Contact**: `{user.is_contact}`
"""
    if user:
        if info.USERGE_ANTISPAM_API:
            try:
                ban = Client(info.USERGE_ANTISPAM_API).getban(user.id)
            except Exception as err:
                return await msg.err(err)
            if not ban:
                user_info += "\n**Userge Antispam API Banned** : `False`"
            else:
                user_info += "\n**Userge Antispam API Banned** : `True`"
                user_info += f"\n    **● Reason** : `{reduce_spam(ban.reason or None)}`"
        if info.SPAM_WATCH_API:
            status = spamwatch.Client(info.SPAM_WATCH_API).get_ban(user.id)
            if status is False:
                user_info += "\n**SpamWatch Banned** : `False`"
            else:
                user_info += "\n**SpamWatch Banned** : `True`"
                user_info += f"\n    **● Reason** : `{reduce_spam(status.reason or None)}`"
                user_info += f"\n    **● Message** : `{reduce_spam(status.message or None)}`"

        async with aiohttp.ClientSession() as ses, ses.get(
            f'https://api.cas.chat/check?user_id={user.id}'
        ) as c_s:
            cas_banned = json.loads(await c_s.text())
        user_gbanned = await GBAN_USER_BASE.find_one({'user_id': user.id})
        user_gmuted = await GMUTE_USER_BASE.find_one({'user_id': user.id})

        if cas_banned['ok']:
            reason = cas_banned['result']['messages'][0] or None
            user_info += "\n**CAS AntiSpam Banned** : `True`"
            user_info += f"\n    **● Reason** : `{reduce_spam(reason)}`"
        else:
            user_info += "\n**CAS AntiSpam Banned** : `False`"
        if user_gmuted:
            user_info += "\n**User GMuted** : `True`"
            user_info += f"\n    **● Reason** : `{reduce_spam(user_gmuted['reason'] or None)}`"
        else:
            user_info += "\n**User GMuted** : `False`"
        if user_gbanned:
            user_info += "\n**User GBanned** : `True`"
            user_info += f"\n    **● Reason** : `{reduce_spam(user_gbanned['reason'] or None)}`"
        else:
            user_info += "\n**User Gbanned** : `False`"
        await msg.edit_or_send_as_file(text=user_info, disable_web_page_preview=True)


def reduce_spam(text: Optional[str]) -> Optional[str]:
    if text and len(text) > 100:
        return text[:97] + "..."
    return text


def last_online(user: User):
    time = ""
    if user.is_bot:
        time += "🤖 Bot :("
    elif user.status == enums.UserStatus.RECENTLY:
        time += "Recently"
    elif user.status == enums.UserStatus.LAST_WEEK:
        time += "Within the last week"
    elif user.status == enums.UserStatus.LAST_MONTH:
        time += "Within the last month"
    elif user.status == enums.UserStatus.LONG_AGO:
        time += "A long time ago :("
    elif user.status == enums.UserStatus.ONLINE:
        time += "Currently Online"
    elif user.status == enums.UserStatus.OFFLINE:
        time += user.last_online_date.strftime("%a, %d %b %Y, %H:%M:%S")
    return time
