""" google image search """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.


import os
import shutil

from PIL import Image
from google_images_search import GoogleImagesSearch as GIS
from pyrogram import enums
from pyrogram.types import InputMediaPhoto

from userge import userge, Message
from .. import google_img as gimg

PATH = "temp_img_down/"

REQ_ERR = """**Both or any one of the following requirements
are missing:**
»`GCS_API_KEY`
»`GCS_IMAGE_E_ID`

Plz follow below process:
»»For `GCS_API_KEY`:
  •Visit https://console.developers.google.com and among all
 of the Google APIs enable "Custom Search API" for your project.

»»For `GCS_IMAGE_E_ID`:
  •Visit https://cse.google.com/cse/all and in the web form where
 you create/edit your custom search engine enable "Image search"
option and for "Sites to search" option select "Search the entire
 web but emphasize included sites"."""


@userge.on_cmd("gimg", about={
    'header': "Google Image Search",
    'description': "Search and Download Images from"
                   " Google and upload to Telegram",
    'usage': "{tr}gimg [Query]",
    'examples': "{tr}gimg Dogs"})
async def google_img(message: Message):
    if (gimg.GCS_API_KEY and gimg.GCS_IMAGE_E_ID) is None:
        await message.edit(REQ_ERR, disable_web_page_preview=True)
        return
    if os.path.exists(PATH):
        shutil.rmtree(PATH, ignore_errors=True)

    fetcher = GIS(gimg.GCS_API_KEY, gimg.GCS_IMAGE_E_ID)
    query = message.input_str
    search = {'q': query,
              'num': 9,
              'safe': "off",
              'fileType': "jpg",
              'imgType': "photo",
              'imgSize': "HUGE"}
    await message.edit("`Processing...`")
    fetcher.search(search_params=search)
    for image in fetcher.results():
        image.download(PATH)
    if not os.path.exists(PATH):
        await message.edit("Oops, No Results Found")
        return
    ss = []
    for img in os.listdir(PATH):
        imgs = PATH + img
        image = Image.open(imgs)
        if not (image.height <= 1280 and image.width <= 1280):
            image.thumbnail((1280, 1280), Image.ANTIALIAS)
            a_dex = image.mode.find("A")
            if a_dex != -1:
                new_im = Image.new('RGB', image.size, (255, 255, 255))
                new_im.paste(image, mask=image.split()[a_dex])
                new_im.save(imgs, 'JPEG', optimize=True)
        ss.append(InputMediaPhoto(str(imgs)))
        if len(ss) == 9:
            break
    await message.reply_chat_action(enums.ChatAction.UPLOAD_PHOTO)
    await message.reply_media_group(ss, True)
    shutil.rmtree(PATH, ignore_errors=True)
    await message.delete()
