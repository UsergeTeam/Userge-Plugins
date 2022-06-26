""" labstack uploader """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# Userge Plugin for Labstack Uploads (https://up.labstack.com)
# Author: Sumanjay (https://github.com/cyberboysumanjay) (@cyberboysumanjay)
#
# All rights reserved.

import asyncio
import math
import os
import random
import re
import string
from urllib.parse import unquote_plus

import requests
from pySmartDL import SmartDL

from userge import userge, config, Message
from userge.utils import progress, humanbytes


@userge.on_cmd("labstack", about={
    'header': "Uploads and shares files for free on Labstack,"
    "without any restriction on file size and speed.",
    'usage': "{tr}labstack : [Direct Link | Reply to Telegram Media]",
    'examples': "{tr}labstack https://mirror.nforce.com/pub/speedtests/10mb.bin"})
async def labstack(message: Message):
    await message.edit("Initiating...")
    if not os.path.isdir(config.Dynamic.DOWN_PATH):
        os.mkdir(config.Dynamic.DOWN_PATH)

    path_ = message.filtered_input_str
    dl_loc = ""
    if path_:
        is_url = re.search(r"(?:https?|ftp)://[^|\s]+\.[^|\s]+", path_)
        if is_url:
            await message.edit("`Downloading From URL...`")
            if not os.path.isdir(config.Dynamic.DOWN_PATH):
                os.mkdir(config.Dynamic.DOWN_PATH)
            url = is_url[0]
            file_name = unquote_plus(os.path.basename(url))
            if "|" in path_:
                file_name = path_.split("|")[1].strip()
            path_ = os.path.join(config.Dynamic.DOWN_PATH, file_name)
            dl_loc = path_
            try:
                downloader = SmartDL(url, path_, progress_bar=False)
                downloader.start(blocking=False)
                count = 0
                while not downloader.isFinished():
                    if message.process_is_canceled:
                        downloader.stop()
                        raise Exception('Process Cancelled!')
                    total_length = downloader.filesize if downloader.filesize else 0
                    downloaded = downloader.get_dl_size()
                    percentage = downloader.get_progress() * 100
                    speed = downloader.get_speed(human=True)
                    estimated_total_time = downloader.get_eta(human=True)
                    progress_str = \
                        "__{}__\n" + \
                        "```[{}{}]```\n" + \
                        "**Progress** : `{}%`\n" + \
                        "**URL** : `{}`\n" + \
                        "**FILENAME** : `{}`\n" + \
                        "**Completed** : `{}`\n" + \
                        "**Total** : `{}`\n" + \
                        "**Speed** : `{}`\n" + \
                        "**ETA** : `{}`"
                    progress_str = progress_str.format(
                        "Downloading",
                        ''.join((config.FINISHED_PROGRESS_STR
                                 for _ in range(math.floor(percentage / 5)))),
                        ''.join((config.UNFINISHED_PROGRESS_STR
                                 for _ in range(20 - math.floor(percentage / 5)))),
                        round(percentage, 2),
                        url,
                        file_name,
                        humanbytes(downloaded),
                        humanbytes(total_length),
                        speed,
                        estimated_total_time)
                    count += 1
                    if count >= 5:
                        count = 0
                        await message.try_to_edit(progress_str, disable_web_page_preview=True)
                    await asyncio.sleep(1)
            except Exception as d_e:
                await message.err(d_e)
                return
        if "|" in path_:
            path_, file_name = path_.split("|")
            path_ = path_.strip()
            if os.path.isfile(path_):
                new_path = os.path.join(config.Dynamic.DOWN_PATH, file_name.strip())
                os.rename(path_, new_path)
                dl_loc = new_path

    if message.reply_to_message and message.reply_to_message.media:
        dl_loc = await message.client.download_media(
            message=message.reply_to_message,
            file_name=config.Dynamic.DOWN_PATH,
            progress=progress,
            progress_args=(message, "Downloading")
        )

    filesize = os.path.getsize(dl_loc)
    filename = os.path.basename(dl_loc)

    file = {"name": filename, "type": "", "size": int(filesize)}
    user_id = ''.join(
        random.choice(string.ascii_lowercase + string.ascii_uppercase +
                      string.digits) for _ in range(16))
    data = {"ttl": 604800, "files": [file]}
    headers = {
        'up-user-id':
        user_id,
        'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64)'
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    }
    kwargs = dict(headers=headers, verify=False)

    r = requests.post(
        "https://up.labstack.com/api/v1/links", json=data, **kwargs).json()

    files = {
        'files': (filename, open(dl_loc, 'rb')),
    }
    send_url = "https://up.labstack.com/api/v1/links/{}/send".format(
        r['code'])
    response = requests.post(send_url, files=files, **kwargs)
    if response.status_code == 200:
        link = (
            "https://up.labstack.com/api/v1/links/{}/receive".format(r['code']))
        await message.edit(f"**Filename**: `{filename}`\n**Size**: "
                           f"`{humanbytes(filesize)}`\n\n"
                           f"**Link**: {link}\n`Expires in 7 Days`")
    else:
        await message.edit("Request Failed!", del_in=5)
