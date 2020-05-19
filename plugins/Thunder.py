

from asyncio import sleep
from collections import deque
from userge import userge, Message


@userge.on_cmd("thunder$", about={'header': "kensar thunder animation"})
async def thunder_(message: Message):
    """thunder"""
    deq = deque(list("☀️🌤️⛅🌥️☁️🌩️🌧️⛈️⚡🌩️🌧️🌦️🌥️⛅🌤️☀️"))
    try:
        for _ in range(32):
            await sleep(0.1)
            await message.edit("".join(deq))
            deq.rotate(1)
    except Exception:
        await message.delete()
