""" Creates random anime sticker """

# by @krishna_singhal

import random
import re
from userge import userge, Message


EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "]+")


def deEmojify(inputString: str) -> str:
    """Remove emojis and other non-safe characters from string"""
    return re.sub(EMOJI_PATTERN, '', inputString)


@userge.on_cmd("sticker", about={
    'header': "Creates random anime sticker",
    'flags': {
        '-f': "To get only girls in anime",
        '-ggl': "To get google search sticker",
        '-mock': "get mock text in sticker"},
    'usage': "{tr}sticker [text | reply to message]\n"
             "{tr}sticker [flags] [text | reply to message]",
    'examples': [
        "{tr}sticker Hello boys and girls",
        "{tr}sticker [flags] Hello boys and girls"]}, allow_via_bot=True)
async def anime_sticker(message: Message):
    """ Creates random anime sticker! """
    if message.reply_to_message:
        text = message.reply_to_message.text
    else:
        text = message.filtered_input_str
    if not text:
        await message.err("```Input not found!...```")
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
    await message.edit("```Lemme create a sticker...```")
    try:
        stickers = await userge.get_inline_bot_results(
            "stickerizerbot",
            f"#{animus}{deEmojify(text)}"
        )
        await userge.send_inline_bot_result(
            chat_id=message.chat.id,
            query_id=stickers.query_id,
            result_id=stickers.results[0].id
        )
        await message.delete()
    except IndexError:
        await message.edit("```List index out of range```", del_in=3)
