# by the unknown

import asyncio

from userge import userge, Message


@userge.on_cmd("spam$", about={'header': "THE SPAMMER"})
async def spam_func(message: Message):
    animation_chars = [
        "YOU", "ARE", "A", "REAL", "SPAMMER", "THAT", "I", "HAVE", "SEEN",
        "YOU ARE A REAL SPAMMER THAT I HAVE SEEN",
    ]
    for i in range(10):
        await asyncio.sleep(0.3)
        await message.edit(animation_chars[i])
