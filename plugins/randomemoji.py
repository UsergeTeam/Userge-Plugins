"""
GET random emoji in Image Format.
Usage - .randomemoji.
"""

# By - SantaYamin aka Nikola.N

import os

from multiutility import EmojiCreator
from userge import Message, userge

Emoji = EmojiCreator()


@userge.on_cmd(
    "randomemoji",
    about={"header": "Get a Random Emoji in Image Format", "usage": "{tr}randomemoji"},
)
async def app(message: Message):
    msg_ = await message.edit("Generating RaNDOmEMoJi for YoU...")
    emoji = Emoji.get_random()
    await msg_.reply_photo(emoji, caption="**---- Random Emoji ----**", quote=False)
    os.remove(emoji)
    await msg_.delete()
