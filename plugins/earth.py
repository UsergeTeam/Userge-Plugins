from asyncio import sleep
from collections import deque

from userge import userge, Message


@userge.on_cmd("earth$", about={'header': "Beautiful Earth Animation"})
async def sun_(message: Message):
    """earth"""
    deq = deque(list("🌏🌍🌎🌎🌍🌏🌍🌎"))
    try:
        for _ in range(32):
            await sleep(0.3)
            await message.edit("".join(deq))
            deq.rotate(1)
    except Exception:
        await message.delete()
