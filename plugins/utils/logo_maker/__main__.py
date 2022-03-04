""" get logo from brandcrowd """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.


# © JigarVarma2005
# Logo maker using brandcrowd.com

import os
import shutil
from typing import List, Tuple

import aiofiles
import aiohttp
from bs4 import BeautifulSoup
from pyrogram.types import InputMediaPhoto

from userge import userge, Message

LOG = userge.getLogger(__name__)
STATUS = False
URI = "https://www.brandcrowd.com/maker/logos"
HEADERS = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37'
                         '.0.2062.124 Safari/537.36'}


async def logo_maker(text: str, keyword: str = "name"):
    """ fetch logos from website """
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        resp = await session.get(
            URI, params={'text': text, 'SearchText': keyword}
        )
        soup = BeautifulSoup(await resp.text(), "lxml")
    embed = soup.findAll("div", {'class': "responsive-embed"})
    img_tags = [(i.find("img"), i.find("a")) for i in embed]
    logos = []
    for img in img_tags:
        src = img[0].get("src")
        if src:
            logos.append(
                (src, getattr(img[1], 'get', {}.get)("href", ""))
            )
    return logos


async def download(uri: str, file_name: str):
    """ download a uri """
    if not os.path.exists("temp_logos/"):
        os.mkdir("temp_logos/")
    async with \
            aiofiles.open(file_name, "wb+") as file, \
            aiohttp.ClientSession(headers=HEADERS) as session, \
            session.get(uri) as response:
        while 1:
            chunk = await response.content.read(512)
            if not chunk:
                return file_name
            await file.write(chunk)


async def dispatch(message: Message, logos: List[Tuple[str]]):
    """ dispatch logos to chat """
    global STATUS  # pylint: disable=global-statement
    group: List[InputMediaPhoto] = []
    paths: List[str] = []
    src: str = "Source: <a href='https://www.brandcrowd.com{}'>Here</a>"
    count: int = 1
    file_name: str = "temp_logos/logo_{}.jpg"
    status = await message.edit("`Beginning To Dispatch Content...`")
    batch = 1
    for logo in logos:
        direct, source = logo
        try:
            loc = await download(direct, file_name.format(count))
            paths.append(loc)
            group.append(InputMediaPhoto(loc, caption=src.format(source)))
            if len(group) == 10:
                try:
                    await status.edit(
                        f"`Uploading Batch {batch}/{round(len(logos) / 10)}...`")
                    await message.reply_media_group(group)
                except Exception as pyro:
                    LOG.exception(pyro)
                batch += 1
                group.clear()
            count += 1
        except Exception as e:
            LOG.exception(e)

    if len(group) >= 2:
        await status.edit(
            f"`Uploading Batch {batch}/{round(len(logos)/10)}`")
        await message.reply_media_group(group)
    elif len(group) == 1:
        await message.reply_photo(group[0].media, caption=group[0].caption)
    await status.delete()
    STATUS = False
    if os.path.exists("temp_logos/"):
        shutil.rmtree("temp_logos/", ignore_errors=True)


@userge.on_cmd("logo", about={
    'header': "Get a logo from brandcrowd",
    'usage': "{tr}logo text:keyword",
    'examples': [
        "{tr}logo Userge", "{tr}logo Userge:bot"
    ]
})
async def jv_logo_maker(message: Message):
    """ make logos """
    global STATUS  # pylint: disable=global-statement
    if STATUS:
        return await message.err("Let the current process be completed!!")
    STATUS = True
    jv_text = message.input_str
    if not jv_text:
        return await message.err("Input Required!!")
    await message.edit("Please wait...")

    type_keyword = "name"
    type_text = jv_text
    if ':' in jv_text:
        type_text, type_keyword = jv_text.split(":", 1)
    try:
        logos = await logo_maker(type_text, type_keyword)
    except Exception as e:
        LOG.exception(e)
        STATUS = False
        return await message.err("No Logos for Ya 😒😒😏")
    await dispatch(message, logos)
