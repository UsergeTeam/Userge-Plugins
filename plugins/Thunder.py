import os
import time
from re import sub
from asyncio import sleep
from collections import deque
from random import choice, getrandbits, randint 
import wget
import requests
from cowpy import cow 
from userge import userge, Message

@userge.on_cmd("thunder$", about="__kensar thunder animation__")
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