""" Creates random anime sricker """

# by @krishna_singhal

import random
from asyncio import sleep
from random import choice

from userge import userge, Message


@userge.on_cmd("sticker", about={
    'header': "Its a joke with anime sticker",
    'usage': "{tr}sticker [text | reply to message]",
    'example': "{tr}sticker I am fool"})
async def anisti(message: Message):
    """ Creates random anime sticker! """

    text = message.input_or_reply_str
    if not text:
        await message.edit("```Need some text Bruh! ...```", del_in=3)
        return
    try:
        animus = [1, 3, 7, 9, 13, 22, 34, 35, 36, 37, 43, 44, 45, 52, 53, 55]
        stickers = await userge.get_inline_bot_results(
            "stickerizerbot",
            f"#{random.choice(animus)}{text}"
        )
        await userge.send_inline_bot_result(
            chat_id=message.chat.id,
            query_id=stickers.query_id,
            result_id=stickers.results[0].id
        )
        await message.delete()
    except IndexError:
        await message.edit("```List index out of range```", del_in=3)
