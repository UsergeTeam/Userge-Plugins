""" purge messages """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

from datetime import datetime

from userge import userge, Message


@userge.on_cmd("purge", about={
    'header': "purge messages from user",
    'flags': {
        '-u': "get user_id from replied message",
        '-l': "message limit : max 1000, def 10"},
    'usage': "reply {tr}purge to the start message to purge.\n"
             "use {tr}purge [user_id | user_name] to purge messages from that user or use flags",
    'examples': ['{tr}purge', '{tr}purge -u', '{tr}purge [user_id | user_name]']}, del_pre=True)
async def purge_(message: Message):
    await message.edit("`purging ...`")

    from_user_id = None

    if message.reply_to_message:
        start_message = message.reply_to_message_id
        limit = message.id - start_message
        if 'u' in message.flags:
            from_user_id = message.reply_to_message.from_user.id
    else:
        limit = min(1000, int(message.flags.get('l') or 10))
        start_message = message.id - limit

    if not from_user_id and message.filtered_input_str:
        from_user_id = (await message.client.get_users(message.filtered_input_str)).id

    purged_messages_count = 0
    list_of_messages = []

    async def delete_msgs():
        nonlocal purged_messages_count
        await message.client.delete_messages(
            chat_id=message.chat.id,
            message_ids=list_of_messages
        )
        purged_messages_count += len(list_of_messages)
        list_of_messages.clear()

    async def handle_msg(_msg):
        if from_user_id and _msg.from_user and _msg.from_user.id != from_user_id:
            return
        list_of_messages.append(_msg.id)
        if len(list_of_messages) >= 100:
            await delete_msgs()

    start_t = datetime.now()
    stop_message = message.id

    if message.client.is_bot:
        for stop_id in range(stop_message, start_message - 1, -200):
            ids = range(stop_id, max(stop_id - 200, start_message - 1), -1)
            for msg in await message.client.get_messages(
                    chat_id=message.chat.id, replies=0, message_ids=ids):
                await handle_msg(msg)
    else:
        async for msg in message.client.get_chat_history(
                chat_id=message.chat.id, limit=limit, offset_id=stop_message):
            if msg.id < start_message:
                break
            await handle_msg(msg)

    if list_of_messages:
        await delete_msgs()

    end_t = datetime.now()
    time_taken_s = (end_t - start_t).seconds
    out = f"<u>purged</u> {purged_messages_count} messages in {time_taken_s} seconds."
    await message.edit(out, del_in=3)
