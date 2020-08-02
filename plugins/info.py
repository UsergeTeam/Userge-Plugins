""" To check User's Info, Is Banned or Not """

# By @Krishna_Singhal

import spamwatch
import requests
from datetime import datetime

from userge import userge, Config, Message, get_collection

GBAN_USER_BASE = get_collection("GBAN_USER")


@userge.on_cmd("info", about={
    'header': "To check User's info",
    'usage': "{tr}info [for own info]\n"
             "{tr}info [Username | User Id]\n"
             "{tr}info [reply to User]"}, allow_via_bot=False)
async def info(msg: Message):
    """ To check User's info """
    await msg.edit("```Checking...```")
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
        await msg.edit("```I don't know that User...```", del_in=5)
        return
    await msg.edit("```Getiing Info...```")
    l_name = user.last_name or ''
    if user.username:
        username = '@' + user.username
    else:
        username = None
    common_chats = await msg.client.get_common_chats(user.id)
    user_info = f"""
**About [{user.first_name} {l_name}](tg://user?id={user.id})**:
  - **UserID**: `{user.id}`
  - **Username**: `{username}`
  - **Last Online**: `{last_online(user)}`
  - **Common Groups**: `{len(common_chats)}`
  - **Contact**: `{user.is_contact}`
        """
    if user:
        if Config.SPAM_WATCH_API:
            status = spamwatch.Client(Config.SPAM_WATCH_API).get_ban(user.id)
            if status is False:
                user_info += "\n**SpamWatch Banned** : `False`\n"
            else:
                user_info += "\n**SpamWatch Banned** : `True`\n"
                user_info += f"**•Reason** : `str({status.reason or None})`\n"
                user_info += f"**•Message** : `str({status.message or None})`\n"
        else:
            user_info += "\n**SpamWatch Banned** : `To get this Info, Set Var`\n"
        cas_banned = requests.get(f'https://api.cas.chat/check?user_id={user.id}').json()
        if cas_banned['ok']:
            reason = cas_banned['result']['messages'][0] or None
            user_info += "**AntiSpam Banned** : `True`\n"
            user_info += f"**•Reason** : `{reason}`\n"
        else:
            user_info += "**AntiSpam Banned** : `False`\n"
        user_gbanned = await GBAN_USER_BASE.find_one({'user_id': user.id})
        if user_gbanned:
            user_info += "**User GBanned** : `True`\n"
            user_info += f"**•Reason** : `{user_gbanned['reason'] or None}`"
        else:
            user_info += "**User Gbanned** : `False`"
        await msg.edit(user_info, disable_web_page_preview=True)


def last_online(user):
    time = ""
    if user.is_bot:
        time += "🤖 Bot :("
    elif user.status == 'recently':
        time += "Recently"
    elif user.status == 'within_week':
        time += "Within the last week"
    elif user.status == 'within_month':
        time += "Within the last month"
    elif user.status == 'long_time_ago':
        time += "A long time ago :("
    elif user.status == 'online':
        time += "Currently Online"
    elif user.status == 'offline':
        time += datetime.fromtimestamp(user.last_online_date).strftime("%a, %d %b %Y, %H:%M:%S")
    return time
