from os import remove
from urllib import parse
from random import choice
import aiohttp
import requests

from userge import userge, Message

BASE_URL = "https://headp.at/pats/{}"
PAT_IMAGE = "pat.jpg"


@userge.on_cmd("pat", about={
    'header': "Give head Pat xD",
    'flags': {'-g': "For Pat Gifs"},
    'usage': "{tr}pat [reply | username]\n{tr}pat -g [reply]"})
async def pat(message: Message):
    username = message.input_str
    reply = message.reply_to_message
    reply_id = reply.message_id if reply else None
    if not username and not reply:
        await message.edit("**Bruh** ~`Reply to a message or provide username`", del_in=3)
        return

    if "-g" in message.flags:
        async with aiohttp.ClientSession() as session:
            r = "https://nekos.life/api/pat"
            async with session.get(r) as request:
                result = await request.json()
                link = result.get("url", None)
                await message.client.send_animation(
                    message.chat.id, animation=link, reply_to_message_id=reply_id)
    else:
        resp = requests.get("http://headp.at/js/pats.json")
        pats = resp.json()
        _pat = BASE_URL.format(parse.quote(choice(pats)))
        with open(PAT_IMAGE, 'wb') as f:
            f.write(requests.get(_pat).content)
        if username:
            await message.reply_photo(
                photo=PAT_IMAGE, caption=username, reply_to_message_id=message.message_id)
        else:
            await message.reply_photo(
                photo=PAT_IMAGE, reply_to_message_id=message.reply_to_message.message_id)

    await message.delete()  # hmm
    remove(PAT_IMAGE)
