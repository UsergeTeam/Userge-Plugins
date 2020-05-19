# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.


from asyncio import sleep
from collections import deque
from userge import userge, Message


@userge.on_cmd("sun$", about="__kensar sun animation__")
async def sun_(message: Message):
    """sun"""
    deq = deque(list("😎🌤🌥☀️⛅️🌦🌞"))
    try:
        for _ in range(32):
            await sleep(0.1)
            await message.edit("".join(deq))
            deq.rotate(1)
    except Exception:
        await message.delete()
