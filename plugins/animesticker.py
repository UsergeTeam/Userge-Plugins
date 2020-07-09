""" Creates random anime sticker """

# by @krishna_singhal

import random

from userge import userge, Message


@userge.on_cmd("sticker", about={
    'header': "Creates random anime sticker",
    'flags': {
        '-f': "To get only girls in anime",
        '-ggl': "To get google search sticker",
        'mock': "get mock text in sticker"},
    'usage': "{tr}sticker [text | reply to message]\n"
             "{tr}sticker [flags] [text | reply to message]",
    'examples': [
        "{tr}sticker Hello boys and girls",
        "{tr}sticker [flags] Hello boys and girls"]}, allow_via_bot=False)
async def anime_sticker(message: Message):
    """ Creates random anime sticker! """
    if message.reply_to_message:
        text = message.reply_to_message.text
    else:
        text = message.filtered_input_str
    if not text:
        await message.err("```Input not found! ...```")
        return
    if '-f' in message.flags:
        k = [20, 32, 33, 40, 41, 42, 58]
        animus = random.choice(k)
    elif '-ggl' in message.flags:
        animus = 12
    elif '-mock' in message.flags:
        animus = 7
    else:
        k = [1, 3, 7, 9, 13, 22, 34, 35, 36, 37, 43, 44, 45, 52, 53, 55]
        animus = random.choice(k)
    await message.edit("```Lemme create a sticker ...```")
    try:
        stickers = await userge.get_inline_bot_results(
            "stickerizerbot",
            f"#{animus}{text}"
        )
        await userge.send_inline_bot_result(
            chat_id=message.chat.id,
            query_id=stickers.query_id,
            result_id=stickers.results[0].id
        )
        await message.delete()
    except IndexError:
        await message.edit("```List index out of range```", del_in=3)
