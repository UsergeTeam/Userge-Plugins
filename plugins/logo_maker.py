# © JigarVarma2005
# Logo maker using brandcrowd.com
# Moded from @JVToolsBot by @UniversalBotsUpdate

import os
from typing import List, Tuple

import aiohttp
import aiofiles
from bs4 import BeautifulSoup

from pyrogram.types import InputMediaPhoto

from userge import userge, Message

LOG = userge.getLogger(__name__)
STATUS = {}
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
    group: List[InputMediaPhoto] = []
    paths: List[str] = []
    src: str = "Source: <a href='https://www.brandcrowd.com{}'>Here</a>"
    count: int = 1
    file_name: str = "logo_{}.jpg"
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
                    await status.edit(f"`Uploading Batch {batch}...`")
                    await message.reply_media_group(group)
                except Exception as pyro:
                    LOG.exception(pyro)
                batch += 1
                group.clear()
            count += 1
        except Exception as e:
            LOG.exception(e)

    if len(group) >= 2:
        await status.edit(f"`Uploading Batch {batch}`")
        await message.reply_media_group(group)
    elif len(group) == 1:
        await message.reply_photo(group[0].media, caption=group[0].caption)
    STATUS[""] = False
    for path in paths:
        if os.path.lexists(path):
            os.remove(path)
    await status.delete()


@userge.on_cmd("logo", about={
    'header': "Get a logo from brandcrowd",
    'usage': "{tr}logo text:keyword",
    'examples': [
        "{tr}logo Userge", "{tr}logo Userge:bot"
    ]
})
async def jv_logo_maker(message: Message):
    """ make logos """
    if STATUS.get("", False):
        return await message.err("Let the current process be completed!!")
    STATUS[""] = True
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
        await message.err("No Logos for Ya 😒😒😏")
        return
    await dispatch(message, logos)
