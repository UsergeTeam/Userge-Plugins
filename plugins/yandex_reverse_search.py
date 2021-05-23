# Userge Plugin for Labstack Uploads (https://up.labstack.com)
# Author: Sumanjay (https://github.com/cyberboysumanjay) (@cyberboysumanjay)
# All rights reserved.

import os
import string
import random
from typing import Dict

import requests

from userge import userge, Config, Message, pool
from userge.utils import progress


@userge.on_cmd("yrs", about={
    'header': "Yandex Reverse Search",
    'description': "Reverse Search any Image/sticker",
    'usage': "{tr}yrs [Reply to image | sticker]",
    'note': "Gif & Animated Stickers won't work!"})
async def labstack(message: Message):

    await message.edit("Found Yandex Result. Lemme pass some Soup!")
    if not os.path.isdir(Config.DOWN_PATH):
        os.mkdir(Config.DOWN_PATH)

    dl_loc = None

    if message.reply_to_message and message.reply_to_message.media:
        dl_loc = await message.client.download_media(
            message=message.reply_to_message,
            file_name=Config.DOWN_PATH,
            progress=progress,
            progress_args=(message, "Found Yandex Result. Lemme pass some Soup!")
        )
    else:
        return await message.err("Media not found!")

    filesize = os.path.getsize(dl_loc)
    filename = os.path.basename(dl_loc)

    file = {"name": filename, "type": "", "size": int(filesize)}
    user_id = ''.join(random.choice(
        string.ascii_lowercase + string.ascii_uppercase + string.digits
    ) for _ in range(16))
    data = {"ttl": 604800, "files": [file]}
    headers = {
        'up-user-id': user_id,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/83.0.4103.97 Safari/537.36'
    }
    r = (await _post(
        url="https://up.labstack.com/api/v1/links",
        json=data,
        headers=headers
    )).json()

    files = {
        'files': (filename, open(dl_loc, 'rb')),
    }
    send_url = "https://up.labstack.com/api/v1/links/{}/send".format(r['code'])
    response = await _post(url=send_url, headers=headers, files=files)
    if (response.status_code) == 200:
        link = (
            "https://yandex.com/images/search?rpt=imageview&url="
            f"https://up.labstack.com/api/v1/links/{r['code']}/receive"
        )
        await message.edit(f"**Yandex Search Link**: {link}")
    else:
        await message.edit("Request Failed!", del_in=5)


@pool.run_in_thread
def _post(
    url: str,
    headers: dict,
    json: Dict[str, str] = None,
    files: Dict[str, str] = None
):
    args = {'url': url, 'headers': headers}
    if files:
        args['files'] = files
    elif json:
        args['json'] = json

    return requests.post(**args)
