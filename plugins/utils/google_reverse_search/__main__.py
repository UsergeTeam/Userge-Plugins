""" google reverse search """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.


import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from pyrogram import enums

from userge import userge, Message, config
from userge.utils import take_screen_shot


@userge.on_cmd("grs", about={
    'header': "Google Reverse Search",
    'description': "Reverse Search any Image/Gif",
    'usage': "{tr}grs [Reply to image | gif]"})
async def google_rs(message: Message):
    start = datetime.now()
    dis_loc = ''
    base_url = "https://www.google.com"
    out_str = "Reply to an image to do Google Reverse Search"
    if message.reply_to_message:
        await message.edit("Downloading Media to my Local")
        message_ = message.reply_to_message
        if message_.sticker and message_.sticker.file_name.endswith('.tgs'):
            await message.edit('Bruh, Searching Animated Sticker is no(T YET) implemented')
            return
        if message_.photo or message_.animation or message_.sticker:
            dis = await message.client.download_media(
                message=message_,
                file_name=config.Dynamic.DOWN_PATH
            )
            dis_loc = os.path.join(config.Dynamic.DOWN_PATH, os.path.basename(dis))
        if message_.animation:
            await message.edit("Converting this Gif to Image")
            img_file = os.path.join(config.Dynamic.DOWN_PATH, "grs.jpg")
            await take_screen_shot(dis_loc, 0, img_file)
            if not os.path.lexists(img_file):
                await message.err("Something went wrong in Conversion")
                return
            dis_loc = img_file
        if dis_loc:
            search_url = "{}/searchbyimage/upload".format(base_url)
            multipart = {
                "encoded_image": (dis_loc, open(dis_loc, "rb")),
                "image_content": ""
            }
            google_rs_response = requests.post(search_url, files=multipart, allow_redirects=False)
            the_location = google_rs_response.headers.get("Location")
            os.remove(dis_loc)
        else:
            await message.edit("No one's gonna help ya (¬_¬)")
            return
        await message.edit("Found Google Result. Lemme pass some Soup;)!")
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"
        }
        response = requests.get(the_location, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        try:
            prs_div = soup.find_all("div", {"class": "r5a77d"})[0]
        except IndexError:
            return await message.err("Index went out of range, Maybe no results were found")
        prs_anchor_element = prs_div.find("a")
        prs_url = base_url + prs_anchor_element.get("href")
        prs_text = prs_anchor_element.text
        img_size_div = soup.find(id="jHnbRc")
        img_size = img_size_div.find_all("div")
        end = datetime.now()
        ms = (end - start).seconds
        out_str = f"""{img_size}

<b>Possible Related Search</b>: <a href="{prs_url}">{prs_text}</a>
<b>More Info</b>: Open this <a href="{the_location}">Link</a>

<b>Time Taken</b>: {ms} seconds"""
    await message.edit(out_str, parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
