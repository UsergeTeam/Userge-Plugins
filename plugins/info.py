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
             "{tr}info [reply to User]"})
async def info(msg: Message):
    """ To check User's info """
    await msg.edit("```Checking...```")
    args = msg.input_str
    replied = msg.reply_to_message
    if args:
        user_id = args
    elif replied:
        if replied.forward_from:
            user_id = args or replied.forward_from.id
        else:
            user_id = args or replied.from_user.id
    else:
        user_id = msg.from_user.id
    try:
        user = await msg.client.get_users(user_id)
    except Exception:
        await msg.edit("```I don't know about that User...```", del_in=5)
        return
    await msg.edit("```Getiing Info...```")
    if user.last_name:
        l_name = user.last_name
    else:
        l_name = ''
    if user.username:
        username = '@' + user.username
    else:
        username = ''
    common_chats = await msg.client.get_common_chats(user.id)
    user_info = f"""
**About [{user.first_name} {l_name}](tg://user?id={user.id})**:
  - **UserID**: `{user.id}`
  - **Username**: {username}
  - **Last Online**: `{Online(user)}`
  - **Common Groups**: `{len(common_chats)}`
  - **Contact**: `{user.is_contact}`
        """
    if user:
        if Config.SPAM_WATCH_API:
            status = spamwatch.Client(Config.SPAM_WATCH_API).get_ban(user.id)
            if status == False:
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


def Online(user):
    LastOnline = ""
    if user.is_bot:
        LastOnline += "🤖 Bot :("
    elif user.status == 'recently':
        LastOnline += "Recently"
    elif user.status == 'within_week':
        LastOnline += "Within the last week"
    elif user.status == 'within_month':
        LastOnline += "Within the last month"
    elif user.status == 'long_time_ago':
        LastOnline += "A long time ago :("
    elif user.status == 'online':
        LastOnline += "Currently Online"
    elif user.status == 'offline':
        LastOnline += datetime.fromtimestamp(user.status.date).strftime("%a, %d %b %Y, %H:%M:%S")
    return LastOnline
