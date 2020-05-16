from random import choice
from urllib import parse
from os import remove
import requests
import asyncio
from userge import userge, Message

BASE_URL = "https://headp.at/pats/{}"
PAT_IMAGE = "pat.jpg"

@userge.on_cmd("pat", about={
    'header': "Give head Pat xD",
    'usage': "{tr}pat [reply | username]"})
async def lastfm(message: Message):

    username = message.input_str
    if not username and not message.reply_to_message:
        await message.edit("**Bruh** ~`Reply to a message or provide username`")
        return 

    resp = requests.get("http://headp.at/js/pats.json")
    pats = resp.json()
    pat = BASE_URL.format(parse.quote(choice(pats)))
    with open(PAT_IMAGE,'wb') as f:
        f.write(requests.get(pat).content)
    if username:
        await message.reply_photo(photo=PAT_IMAGE, caption=username, reply_to_message_id=message.message_id)
    else:
        await message.reply_photo(photo=PAT_IMAGE, reply_to_message_id=message.reply_to_message.message_id)
    await message.delete() # hmm
    remove(PAT_IMAGE)
