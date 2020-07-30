""" To check User's Info based on SpamWatch """

# By @Krishna_Singhal

from datetime import datetime
import spamwatch

from userge import userge, Config, Message


@userge.on_cmd("info", about={
    'header': "To check User's info and Check SpamWatch Info",
    'usage': "{tr}info [for own info]\n"
             "{tr}info [Username | User Id]\n"
             "{tr}info [reply to User]"})
async def info(msg: Message):
    """ To check User's info """
    await msg.edit("```Checking...```")
    args = msg.input_str
    replied = msg.reply_to_message
    if args:
        user = args
    elif replied:
        if replied.forward_from:
            user = args or replied.forward_from.id
        else:
            user = args or replied.from_user.id
    else:
        user = msg.from_user.id
    try:
        User = await msg.client.get_users(user)
    except Exception:
        await msg.edit("```I don't know that User...```", del_in=5)
        return
    await msg.edit("```Getiing Info...```")
    if User.last_name:
        l_name = User.last_name
    else:
        l_name = ''
    if User.username:
        username = '@' + User.username
    else:
        username = ''
    common_chats = await msg.client.get_common_chats(User.id)
    User_info = f"""
**About [{User.first_name} {l_name}](tg://user?id={User.id})**:
  - **UserID**: `{User.id}`
  - **Username**: {username}
  - **Last Online**: `{LastOnline(User)}`
  - **Common Groups**: `{len(common_chats)}`
  - **Contact**: `{User.is_contact}`
        """
    if User:
        if Config.SPAM_WATCH_API:
            status = spamwatch.Client(Config.SPAM_WATCH_API).get_ban(User.id)
            if status == 'False':
                User_info += "\n**SpamWatch Banned** : `False` ✅"
            else:
                User_info += "\n**SpamWatch Banned** : `True` ❌\n"
                User_info += f"**•Reason** : `{status.reason}`\n"
                User_info += f"**•Message** : `{status.message}`"
            await msg.edit(User_info, disable_web_page_preview=True)
        else:
            User_info += "\n**SpamWatch Banned** : `To get this Info, Set Var`"
            await msg.edit(User_info, disable_web_page_preview=True)


def LastOnline(User):
    LastOnline = ""
    if User.is_bot:
        LastOnline += "🤖 Bot :("
    elif User.status == 'recently':
        LastOnline += "Recently"
    elif User.status == 'within_week':
        LastOnline += "Within the last week"
    elif User.status == 'within_month':
        LastOnline += "Within the last month"
    elif User.status == 'long_time_ago':
        LastOnline += "A long time ago :("
    elif User.status == 'online':
        LastOnline += "Currently Online"
    elif User.status == 'offline':
        LastOnline += datetime.fromtimestamp(User.status.date).strftime("%a, %d %b %Y, %H:%M:%S")
    return LastOnline
